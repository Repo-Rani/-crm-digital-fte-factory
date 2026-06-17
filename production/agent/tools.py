"""
Production agent tools using OpenAI Agents SDK @function_tool decorator.
Each tool connects to PostgreSQL and real channel APIs.
All tools have Pydantic input validation and full error handling.
"""

from agents import function_tool
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import logging
import os
from openai import AsyncOpenAI

from database.queries import (
    get_db_pool, get_or_create_conversation,
    create_ticket_record, get_customer_history_across_channels,
    search_knowledge_base_semantic, update_ticket_status,
    record_metric, store_message
)
from kafka_client import FTEKafkaProducer, TOPICS

logger = logging.getLogger(__name__)
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_embedding(text: str) -> List[float]:
    """Generate OpenAI embedding for semantic search."""
    response = await openai_client.embeddings.create(
        input=text, model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# ---- Pydantic Input Schemas ----

class KnowledgeSearchInput(BaseModel):
    query: str = Field(..., description="The search query for the product documentation")
    max_results: int = Field(5, description="Maximum number of results to return")

class TicketInput(BaseModel):
    customer_id: str = Field(..., description="UUID of the customer")
    issue: str = Field(..., description="Brief description of the customer issue")
    priority: str = Field("medium", description="Priority level: low, medium, high, urgent")
    category: Optional[str] = Field(None, description="Issue category: technical, billing, general")
    channel: str = Field(..., description="Channel ticket originated from: email, whatsapp, web_form")

class EscalationInput(BaseModel):
    ticket_id: str = Field(..., description="UUID of the ticket to escalate")
    reason: str = Field(..., description="Reason for escalation")
    urgency: str = Field("normal", description="Urgency: normal, high, urgent")

class ResponseInput(BaseModel):
    ticket_id: str = Field(..., description="UUID of the ticket being responded to")
    message: str = Field(..., description="The response message text")
    channel: str = Field(..., description="Target channel: email, whatsapp, web_form")

# ---- Tools ----

@function_tool
async def search_knowledge_base(input: KnowledgeSearchInput) -> str:
    """Search product documentation for relevant information.
    Use this when the customer asks questions about features, troubleshooting, or how-to.
    """
    try:
        embedding = await generate_embedding(input.query)
        results = await search_knowledge_base_semantic(embedding, input.max_results)
        
        if not results:
            return json.dumps({"found": False, "message": "No relevant documentation found."})
            
        formatted = []
        for r in results:
            formatted.append(f"**{r['title']}** (similarity: {r['similarity']:.2f})\n{r['content'][:400]}")
            
        return json.dumps({
            "found": True, 
            "count": len(results), 
            "results": "\n\n---\n\n".join(formatted)
        })
    except Exception as e:
        logger.error(f"KB search failed: {e}")
        return json.dumps({"found": False, "message": "Knowledge base temporarily unavailable."})

@function_tool
async def create_ticket(input: TicketInput) -> str:
    """Create a support ticket for tracking. 
    ALWAYS create a ticket at the START of every new interaction.
    """
    try:
        # Resolve or create conversation
        conv_id = await get_or_create_conversation(input.customer_id, input.channel)
        
        ticket_id = await create_ticket_record(
            conversation_id=conv_id,
            customer_id=input.customer_id,
            source_channel=input.channel,
            category=input.category,
            priority=input.priority
        )
        
        return json.dumps({"ticket_id": str(ticket_id), "status": "open", "channel": input.channel})
    except Exception as e:
        logger.error(f"create_ticket failed: {e}")
        return json.dumps({"error": str(e)})

@function_tool
async def get_customer_history(customer_id: str) -> str:
    """Get customer's complete interaction history across ALL channels.
    Use this to understand context from previous interactions.
    """
    try:
        history = await get_customer_history_across_channels(customer_id, limit=20)
        return json.dumps({
            "customer_id": customer_id,
            "history_count": len(history),
            "history": history[:10]  # Return last 10 for context window efficiency
        })
    except Exception as e:
        logger.error(f"get_customer_history failed: {e}")
        return json.dumps({"history_count": 0, "history": []})

@function_tool
async def escalate_to_human(input: EscalationInput) -> str:
    """Escalate conversation to human support.
    Use this for pricing inquiries, refund requests, legal threats, or complex issues.
    """
    try:
        await update_ticket_status(input.ticket_id, 'escalated', f"Escalated via agent: {input.reason}")
        
        # Notify via Kafka
        producer = FTEKafkaProducer()
        await producer.publish(TOPICS['escalations'], {
            'event_type': 'escalation',
            'ticket_id': input.ticket_id,
            'reason': input.reason,
            'urgency': input.urgency
        })
        
        await record_metric('escalation', 1.0, dimensions={'reason': input.reason})
        
        resp_times = {'urgent': '1 hour', 'high': '4 hours', 'normal': '24 hours'}
        return json.dumps({
            "status": "escalated",
            "ticket_id": input.ticket_id,
            "expected_response": resp_times.get(input.urgency, '24 hours'),
            "customer_message": f"I've flagged your case for our specialist team. They will respond within {resp_times.get(input.urgency, '24 hours')}. Reference: {input.ticket_id}"
        })
    except Exception as e:
        logger.error(f"escalate_to_human failed: {e}")
        return json.dumps({"status": "escalation_failed", "error": str(e)})

@function_tool
async def send_response(input: ResponseInput) -> str:
    """Send response to customer via their current channel.
    The response will be automatically formatted for the channel.
    """
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            # Fetch conversation ID for storage
            conv_row = await conn.fetchrow(
                "SELECT conversation_id FROM tickets WHERE id = $1", 
                input.ticket_id
            )
            
        if not conv_row:
            return json.dumps({"status": "failed", "error": "Ticket not found"})
            
        conv_id = str(conv_row['conversation_id'])
        
        # Note: Actual delivery to Gmail/Twilio happens via channel handlers in workers.
        # This tool marks it as 'ready' and stores it in the DB audit trail.
        
        await store_message(
            conversation_id=conv_id,
            channel=input.channel,
            direction='outbound',
            role='agent',
            content=input.message,
            delivery_status='pending' # Worker will update once real API confirms
        )
        
        return json.dumps({
            "status": "queued",
            "channel": input.channel,
            "ticket_id": input.ticket_id
        })
    except Exception as e:
        logger.error(f"send_response failed: {e}")
        return json.dumps({"status": "failed", "error": str(e)})
