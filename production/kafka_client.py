"""
Kafka Client — Producer and Consumer for multi-channel FTE.
Uses aiokafka for async Kafka operations.
"""

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import os
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Callable

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Topic registry — ALL topics used by the system
TOPICS = {
    'tickets_incoming':   'fte.tickets.incoming',       # All channels → unified queue
    'email_inbound':      'fte.channels.email.inbound',
    'whatsapp_inbound':   'fte.channels.whatsapp.inbound',
    'webform_inbound':    'fte.channels.webform.inbound',
    'email_outbound':     'fte.channels.email.outbound',
    'whatsapp_outbound':  'fte.channels.whatsapp.outbound',
    'escalations':        'fte.escalations',
    'metrics':            'fte.metrics',
    'dlq':                'fte.dlq'  # Dead Letter Queue for failed processing
}

class FTEKafkaProducer:
    def __init__(self):
        self.producer = None

    async def start(self):
        if self.producer:
            return
            
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
            acks='all',            # Wait for all replicas (durability)
            retry_backoff_ms=300,
            request_timeout_ms=10000
        )
        await self.producer.start()
        logger.info("Kafka producer started")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            self.producer = None

    async def publish(self, topic: str, event: Dict[str, Any]):
        """Publish event with automatic timestamp injection."""
        if not self.producer:
            await self.start()
            
        event['_published_at'] = datetime.now(timezone.utc).isoformat()
        await self.producer.send_and_wait(topic, event)
        logger.debug(f"Published to {topic}")

class FTEKafkaConsumer:
    def __init__(self, topics: List[str], group_id: str):
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )

    async def start(self):
        await self.consumer.start()
        logger.info(f"Kafka consumer started for group: {self.consumer._group_id}")

    async def stop(self):
        await self.consumer.stop()

    async def consume(self, handler: Callable):
        """Consume messages indefinitely, calling handler for each."""
        try:
            async for msg in self.consumer:
                try:
                    await handler(msg.topic, msg.value)
                except Exception as e:
                    logger.error(f"Handler error for topic {msg.topic}: {e}", exc_info=True)
        finally:
            await self.stop()
