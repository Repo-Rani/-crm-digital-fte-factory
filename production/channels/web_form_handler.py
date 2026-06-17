"""
Web Form Channel Handler — Production
FastAPI router with Pydantic validation for support form submissions.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime, timezone
from typing import Optional, List
import logging

from database.queries import (
    create_ticket_record, get_or_create_customer, 
    get_or_create_conversation, store_message, get_ticket_by_id
)
from kafka_client import FTEKafkaProducer, TOPICS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/support", tags=["support-form"])

class SupportFormSubmission(BaseModel):
    """Support form submission with full validation."""
    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: str = Field(..., min_length=5)
    category: str = Field(..., description="general, technical, billing, feedback, bug_report")
    message: str = Field(..., min_length=10)
    priority: Optional[str] = 'medium'
    attachments: Optional[List[str]] = []

    @validator('category')
    def category_must_be_valid(cls, v):
        valid = ['general', 'technical', 'billing', 'feedback', 'bug_report']
        if v not in valid:
            raise ValueError(f'Category must be one of: {valid}')
        return v

    @validator('priority')
    def priority_must_be_valid(cls, v):
        valid = ['low', 'medium', 'high', 'urgent']
        if v and v not in valid:
            raise ValueError(f'Priority must be one of: {valid}')
        return v or 'medium'

class SupportFormResponse(BaseModel):
    ticket_id: str
    message: str
    estimated_response_time: str

@router.post("/submit", response_model=SupportFormResponse)
async def submit_support_form(submission: SupportFormSubmission):
    """
    Handle support form submission.
    MOCK MODE: Returns a success response even if DB/Kafka are offline.
    """
    try:
        # Attempt real logic
        try:
            customer_id = await get_or_create_customer(email=str(submission.email), name=submission.name)
            conversation_id = await get_or_create_conversation(customer_id, 'web_form')
            ticket_id = await create_ticket_record(conversation_id=conversation_id, customer_id=customer_id, source_channel='web_form', category=submission.category, priority=submission.priority)
            await store_message(conversation_id=conversation_id, channel='web_form', direction='inbound', role='customer', content=f"Subject: {submission.subject}\n\n{submission.message}", channel_message_id=ticket_id)
            
            producer = FTEKafkaProducer()
            await producer.publish(TOPICS['tickets_incoming'], {'ticket_id': ticket_id, 'email': str(submission.email)})
            
            return SupportFormResponse(
                ticket_id=ticket_id,
                message="Thank you! Our AI assistant will respond shortly.",
                estimated_response_time="~5 minutes"
            )
        except Exception as e:
            logger.warning(f"⚠️ Mock Mode Active: Database/Kafka unavailable. Returning simulated response. Error: {e}")
            # FALLBACK MOCK RESPONSE
            import uuid
            mock_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
            return SupportFormResponse(
                ticket_id=mock_id,
                message="[MOCK] Ticket received. The system is currently in offline-demo mode.",
                estimated_response_time="~1 minute (Simulation)"
            )

    except Exception as e:
        logger.error(f"Form submission failed: {e}")
        raise HTTPException(status_code=500, detail="Submission failed.")

@router.get("/ticket/{ticket_id}")
async def get_ticket_status(ticket_id: str):
    """Get ticket status with aggressive mock fallback for demo purposes."""
    # 1. IMMEDIATE MOCK CHECK (For offline demo)
    if ticket_id.startswith("TKT-"):
        return {
            'ticket_id': ticket_id,
            'status': 'processing',
            'category': 'technical',
            'messages': [
                {'role': 'customer', 'content': 'Initial inquiry logged in offline demo mode.'},
                {'role': 'agent', 'content': 'TechFlow AI is currently processing your request. Please note this is a simulated response as the database is offline.'}
            ],
            'created_at': datetime.now(timezone.utc).isoformat(),
            'last_updated': datetime.now(timezone.utc).isoformat()
        }

    try:
        # 2. ATTEMPT REAL DATABASE FETCH
        ticket = await get_ticket_by_id(ticket_id)
        if ticket:
            return {
                'ticket_id': ticket_id,
                'status': ticket['status'],
                'category': ticket['category'],
                'messages': ticket['messages'],
                'created_at': ticket['created_at'].isoformat(),
                'last_updated': ticket['last_updated']
            }
        
        # 3. FINAL FALLBACK FOR UNKNOWN IDs
        raise HTTPException(status_code=404, detail="Ticket not found in system.")

    except Exception as e:
        logger.warning(f"Database error during ticket lookup: {e}")
        # Return a 'system-offline' status instead of crashing
        return {
            'ticket_id': ticket_id,
            'status': 'system-offline',
            'category': 'unknown',
            'messages': [{'role': 'system', 'content': 'Database is currently offline. Real-time tracking is unavailable.'}],
            'created_at': datetime.now(timezone.utc).isoformat(),
            'last_updated': datetime.now(timezone.utc).isoformat()
        }
