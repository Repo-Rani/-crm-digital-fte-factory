"""
Unified Message Processor — Kafka Consumer
Consumes from fte.tickets.incoming, runs agent, stores results, sends replies.
"""

import asyncio
import logging
from datetime import datetime, timezone

from kafka_client import FTEKafkaConsumer, FTEKafkaProducer, TOPICS
from agent.customer_success_agent import customer_success_agent
from agent.formatters import format_for_channel
from channels.gmail_handler import GmailHandler
from channels.whatsapp_handler import WhatsAppHandler
from database.queries import (
    get_or_create_customer, get_or_create_conversation,
    store_message, load_conversation_history, record_metric,
    get_db_pool
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

class UnifiedMessageProcessor:
    def __init__(self):
        self.gmail = GmailHandler()
        self.whatsapp = WhatsAppHandler()
        self.producer = FTEKafkaProducer()

    async def start(self):
        """Start the message processor."""
        await get_db_pool() # Ensure DB pool ready
        await self.producer.start()
        
        consumer = FTEKafkaConsumer(
            topics=[TOPICS['tickets_incoming']],
            group_id='fte-message-processor'
        )
        await consumer.start()
        logger.info("Message processor started. Listening for tickets...")
        
        try:
            await consumer.consume(self.process_message)
        finally:
            await consumer.stop()
            await self.producer.stop()

    async def process_message(self, topic: str, message: dict):
        """Main processing logic per message."""
        start_time = datetime.now(timezone.utc)
        channel = message.get('channel', 'web_form')
        
        try:
            # 1. Resolve Customer
            customer_id = await get_or_create_customer(
                email=message.get('customer_email'),
                phone=message.get('customer_phone'),
                name=message.get('customer_name', '')
            )

            # 2. Get/Create Conversation
            conversation_id = await get_or_create_conversation(customer_id, channel)

            # 3. Store Inbound (if not web_form)
            if channel != 'web_form':
                await store_message(
                    conversation_id=conversation_id,
                    channel=channel,
                    direction='inbound',
                    role='customer',
                    content=message.get('content', ''),
                    channel_message_id=message.get('channel_message_id')
                )

            # 4. Load Context
            history = await load_conversation_history(conversation_id)
            history_text = '\n'.join([f"{m['role']}: {m['content']}" for m in history[-10:]])

            # 5. Run Agent
            from agents import Runner
            agent_input = f"""
Customer: {message.get('customer_name', 'Customer')}
Channel: {channel}
Customer ID: {customer_id}
Conversation ID: {conversation_id}
Subject: {message.get('subject', 'Support Request')}
Message: {message.get('content', '')}

Recent history:
{history_text}
"""
            result = await Runner.run(
                customer_success_agent,
                messages=[{"role": "user", "content": agent_input}],
                context={
                    'customer_id': customer_id,
                    'conversation_id': conversation_id,
                    'channel': channel,
                    'ticket_subject': message.get('subject', 'Support Request')
                }
            )

            # 6. Post-processing Metrics
            latency_ms = int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000)
            await record_metric('latency_ms', latency_ms, channel=channel)
            
            logger.info(f"✓ Processed {channel} message in {latency_ms}ms")

        except Exception as e:
            logger.error(f"Processing failed: {e}", exc_info=True)
            await self.handle_error(message, e)

    async def handle_error(self, message: dict, error: Exception):
        """Fall back to DLQ on error."""
        await self.producer.publish(TOPICS['dlq'], {
            'original_message': message,
            'error': str(error)
        })

async def main():
    processor = UnifiedMessageProcessor()
    await processor.start()

if __name__ == "__main__":
    asyncio.run(main())
