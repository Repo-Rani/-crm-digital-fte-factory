"""
Database query functions for Customer Success FTE.
All functions use asyncpg connection pool for async PostgreSQL access.
"""

import asyncpg
import os
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

_pool = None

async def get_db_pool() -> Optional[asyncpg.Pool]:
    """
    Get or create the database connection pool.
    MOCK MODE: Returns None if DB is unreachable.
    """
    global _pool
    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=int(os.getenv("POSTGRES_PORT", 5432)),
                database=os.getenv("POSTGRES_DB", "fte_db"),
                user=os.getenv("POSTGRES_USER", "fte_user"),
                password=os.getenv("POSTGRES_PASSWORD"),
                min_size=1,
                max_size=5,
                command_timeout=5
            )
        except Exception as e:
            logger.error(f"❌ DB Pool Error: {e}. System will run in MOCK mode.")
            return None
    return _pool

# ============================================================
# CUSTOMER FUNCTIONS
# ============================================================

async def get_or_create_customer(email: str = None, phone: str = None, name: str = "") -> str:
    """
    Find existing customer or create new one.
    Email is primary key — phone is secondary (WhatsApp).
    If customer contacts via phone and we already have their email,
    link the records via customer_identifiers.
    Returns: customer UUID as string
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Try email first (primary identifier)
        if email:
            customer = await conn.fetchrow(
                "SELECT id FROM customers WHERE email = $1", email
            )
            if customer:
                # Update name if provided and missing
                if name and not customer.get('name'):
                    await conn.execute("UPDATE customers SET name = $1 WHERE id = $2", name, customer['id'])
                return str(customer['id'])
            
            # Create new customer with email
            customer_id = await conn.fetchval(
                "INSERT INTO customers (email, name) VALUES ($1, $2) RETURNING id",
                email, name
            )
            # Register email as identifier
            await conn.execute("""
                INSERT INTO customer_identifiers (customer_id, identifier_type, identifier_value)
                VALUES ($1, 'email', $2)
                ON CONFLICT (identifier_type, identifier_value) DO NOTHING
            """, customer_id, email)
            return str(customer_id)

        # Try phone (WhatsApp)
        if phone:
            identifier = await conn.fetchrow("""
                SELECT customer_id FROM customer_identifiers
                WHERE identifier_type = 'whatsapp' AND identifier_value = $1
            """, phone)
            if identifier:
                return str(identifier['customer_id'])
            
            # Create new customer with phone only
            customer_id = await conn.fetchval(
                "INSERT INTO customers (phone, name) VALUES ($1, $2) RETURNING id",
                phone, name
            )
            await conn.execute("""
                INSERT INTO customer_identifiers (customer_id, identifier_type, identifier_value)
                VALUES ($1, 'whatsapp', $2)
                ON CONFLICT (identifier_type, identifier_value) DO NOTHING
            """, customer_id, phone)
            return str(customer_id)

        raise ValueError("Must provide email or phone to identify customer")

async def find_customer(email: str = None, phone: str = None) -> Optional[Dict[str, Any]]:
    """
    Look up customer by email or phone.
    Returns full customer record with conversation count, or None if not found.
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        if email:
            row = await conn.fetchrow("""
                SELECT c.*, 
                       COUNT(DISTINCT conv.id) as conversation_count,
                       MAX(conv.started_at) as last_contact
                FROM customers c
                LEFT JOIN conversations conv ON conv.customer_id = c.id
                WHERE c.email = $1
                GROUP BY c.id
            """, email)
        elif phone:
            row = await conn.fetchrow("""
                SELECT c.*,
                       COUNT(DISTINCT conv.id) as conversation_count,
                       MAX(conv.started_at) as last_contact
                FROM customers c
                JOIN customer_identifiers ci ON ci.customer_id = c.id
                LEFT JOIN conversations conv ON conv.customer_id = c.id
                WHERE ci.identifier_type = 'whatsapp' AND ci.identifier_value = $1
                GROUP BY c.id
            """, phone)
        else:
            return None
        return dict(row) if row else None

# ============================================================
# CONVERSATION FUNCTIONS
# ============================================================

async def get_or_create_conversation(customer_id: str, channel: str) -> str:
    """
    Get active conversation within last 24 hours, or create a new one.
    Returns: conversation UUID as string
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Check for active conversation in last 24h
        active = await conn.fetchrow("""
            SELECT id FROM conversations
            WHERE customer_id = $1
              AND status = 'active'
              AND started_at > NOW() - INTERVAL '24 hours'
            ORDER BY started_at DESC
            LIMIT 1
        """, customer_id)
        
        if active:
            return str(active['id'])
            
        # Create new conversation
        conversation_id = await conn.fetchval("""
            INSERT INTO conversations (customer_id, initial_channel, status)
            VALUES ($1, $2, 'active')
            RETURNING id
        """, customer_id, channel)
        return str(conversation_id)

async def update_conversation_sentiment(conversation_id: str, sentiment: float):
    """Update the sentiment score on a conversation."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE conversations SET sentiment_score = $1 WHERE id = $2
        """, sentiment, conversation_id)

async def resolve_conversation(conversation_id: str, resolution_type: str, escalated_to: str = None):
    """Mark conversation as resolved or escalated."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        status = 'escalated' if escalated_to or resolution_type == 'escalated' else 'resolved'
        await conn.execute("""
            UPDATE conversations
            SET status = $1,
                ended_at = NOW(),
                resolution_type = $2,
                escalated_to = $3
            WHERE id = $4
        """, status, resolution_type, escalated_to, conversation_id)

# ============================================================
# MESSAGE FUNCTIONS
# ============================================================

async def store_message(
    conversation_id: str,
    channel: str,
    direction: str,
    role: str,
    content: str,
    tokens_used: int = None,
    latency_ms: int = None,
    tool_calls: List[Dict[str, Any]] = None,
    channel_message_id: str = None,
    delivery_status: str = 'pending'
) -> str:
    """Store a message (inbound or outbound) in the database."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        message_id = await conn.fetchval("""
            INSERT INTO messages (
                conversation_id, channel, direction, role, content,
                tokens_used, latency_ms, tool_calls, channel_message_id, delivery_status
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id
        """, conversation_id, channel, direction, role, content,
             tokens_used, latency_ms, json.dumps(tool_calls or []),
             channel_message_id, delivery_status)
        return str(message_id)

async def update_delivery_status(channel_message_id: str, status: str):
    """Update message delivery status from webhook callback."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE messages SET delivery_status = $1
            WHERE channel_message_id = $2
        """, status, channel_message_id)

async def load_conversation_history(conversation_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Load message history for a conversation, formatted for agent context."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT role, content, channel, created_at
            FROM messages
            WHERE conversation_id = $1
            ORDER BY created_at ASC
            LIMIT $2
        """, conversation_id, limit)
        return [{"role": r['role'], "content": r['content'],
                 "channel": r['channel'], "timestamp": r['created_at'].isoformat()}
                for r in rows]

async def get_customer_history_across_channels(customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get full customer history across ALL channels.
    This is what the agent uses to understand returning customers.
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT m.role, m.content, m.channel, m.created_at,
                   c.initial_channel as conversation_channel,
                   c.status as conversation_status
            FROM conversations c
            JOIN messages m ON m.conversation_id = c.id
            WHERE c.customer_id = $1
            ORDER BY m.created_at DESC
            LIMIT $2
        """, customer_id, limit)
        return [dict(r) for r in rows]

# ============================================================
# TICKET FUNCTIONS
# ============================================================

async def create_ticket_record(
    conversation_id: str,
    customer_id: str,
    source_channel: str,
    category: str = None,
    priority: str = 'medium'
) -> str:
    """Create a support ticket in the database. Returns ticket UUID."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        ticket_id = await conn.fetchval("""
            INSERT INTO tickets (conversation_id, customer_id, source_channel, category, priority, status)
            VALUES ($1, $2, $3, $4, $5, 'open')
            RETURNING id
        """, conversation_id, customer_id, source_channel, category, priority)
        return str(ticket_id)

async def get_ticket_by_id(ticket_id: str) -> Optional[Dict[str, Any]]:
    """Get ticket with its messages."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        ticket = await conn.fetchrow("""
            SELECT t.*, 
                   c.initial_channel,
                   c.status as conversation_status
            FROM tickets t
            JOIN conversations c ON c.id = t.conversation_id
            WHERE t.id = $1
        """, ticket_id)
        if not ticket:
            return None
        
        messages = await conn.fetch("""
            SELECT role, content, channel, created_at, delivery_status
            FROM messages
            WHERE conversation_id = $1
            ORDER BY created_at ASC
        """, ticket['conversation_id'])
        
        result = dict(ticket)
        result['messages'] = [dict(m) for m in messages]
        result['last_updated'] = messages[-1]['created_at'].isoformat() if messages else result['created_at'].isoformat()
        return result

async def update_ticket_status(ticket_id: str, status: str, resolution_notes: str = None):
    """Update ticket status and optionally add resolution notes."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE tickets
            SET status = $1,
                resolution_notes = COALESCE($2, resolution_notes),
                resolved_at = CASE WHEN $1 = 'resolved' THEN NOW() ELSE resolved_at END
            WHERE id = $3
        """, status, resolution_notes, ticket_id)

# ============================================================
# KNOWLEDGE BASE FUNCTIONS
# ============================================================

async def search_knowledge_base_semantic(query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Semantic search using pgvector cosine similarity.
    query_embedding: list of 1536 floats from OpenAI embeddings API
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT title, content, category,
                   1 - (embedding <=> $1::vector) as similarity
            FROM knowledge_base
            ORDER BY embedding <=> $1::vector
            LIMIT $2
        """, query_embedding, limit)
        return [dict(r) for r in rows if r['similarity'] > 0.7]

async def seed_knowledge_base_from_docs(docs_path: str):
    """
    Load product-docs.md from Phase 1 context into knowledge_base table.
    Splits by section (## headings), generates embeddings, stores in DB.
    """
    from openai import AsyncOpenAI
    import re

    client = AsyncOpenAI()

    if not os.path.exists(docs_path):
        logger.error(f"Documentation file not found at {docs_path}")
        return

    with open(docs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by ## headings
    sections = re.split(r'\n## ', content)
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        # Check if already seeded
        count = await conn.fetchval("SELECT COUNT(*) FROM knowledge_base")
        if count > 0:
            logger.info("Knowledge base already seeded. Skipping.")
            return

        for section in sections:
            if not section.strip() or len(section.strip()) < 50:
                continue
            
            lines = section.strip().split('\n')
            title = lines[0].strip('# ')
            body = '\n'.join(lines[1:]).strip()

            try:
                # Generate embedding
                response = await client.embeddings.create(
                    input=f"{title}\n{body}",
                    model="text-embedding-ada-002"
                )
                embedding = response.data[0].embedding

                await conn.execute("""
                    INSERT INTO knowledge_base (title, content, embedding)
                    VALUES ($1, $2, $3::vector)
                """, title, body, embedding)
            except Exception as e:
                logger.error(f"Failed to embed section '{title}': {e}")

    logger.info(f"Knowledge base seeding complete.")

# ============================================================
# METRICS FUNCTIONS
# ============================================================

async def record_metric(metric_name: str, value: float, channel: str = None, dimensions: Dict[str, Any] = None):
    """Record a performance metric."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO agent_metrics (metric_name, metric_value, channel, dimensions)
            VALUES ($1, $2, $3, $4)
        """, metric_name, value, channel, json.dumps(dimensions or {}))

async def get_channel_metrics_24h() -> Dict[str, Any]:
    """Get performance metrics per channel for last 24 hours. Returns mock data if DB is offline."""
    try:
        pool = await get_db_pool()
        if not pool:
            raise Exception("DB Pool Offline")
            
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT
                    initial_channel as channel,
                    COUNT(*) as total_conversations,
                    AVG(sentiment_score) as avg_sentiment,
                    COUNT(*) FILTER (WHERE status = 'escalated') as escalations,
                    COUNT(*) FILTER (WHERE status = 'resolved') as resolved
                FROM conversations
                WHERE started_at > NOW() - INTERVAL '24 hours'
                GROUP BY initial_channel
            """)
            return {row['channel']: dict(row) for row in rows}
    except Exception:
        # RETURN MOCK DATA FOR DEMO
        return {
            "web_form": {"total_conversations": 0, "resolved": 0, "avg_sentiment": 0},
            "email": {"total_conversations": 0, "resolved": 0, "avg_sentiment": 0},
            "whatsapp": {"total_conversations": 0, "resolved": 0, "avg_sentiment": 0}
        }
