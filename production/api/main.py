"""
FastAPI Application — Customer Success FTE API
All channel endpoints + health + metrics.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging

from channels.gmail_handler import GmailHandler
from channels.whatsapp_handler import WhatsAppHandler
from channels.web_form_handler import router as web_form_router
from kafka_client import FTEKafkaProducer, TOPICS
from database.queries import (
    get_db_pool, get_channel_metrics_24h,
    find_customer, load_conversation_history, seed_knowledge_base_from_docs
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Success FTE API",
    description="24/7 AI customer support — Email, WhatsApp, Web Form",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(web_form_router)

gmail_handler = GmailHandler()
whatsapp_handler = WhatsAppHandler()
kafka_producer = FTEKafkaProducer()

@app.on_event("startup")
async def startup():
    try:
        await kafka_producer.start()
        logger.info("Kafka producer started.")
    except Exception as e:
        logger.warning(f"⚠️ Kafka Offline: Background workers will not receive events. Error: {e}")
        
    # Seed knowledge base from Phase 1 docs if table is empty
    try:
        await seed_knowledge_base_from_docs("../context/product-docs.md")
        logger.info("FTE API started. Knowledge base ready.")
    except Exception as e:
        logger.warning(f"⚠️ Database Offline: Knowledge base and metrics will be unavailable. Error: {e}")

@app.on_event("shutdown")
async def shutdown():
    await kafka_producer.stop()

# ---- Health Check ----
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.0.0",
        "channels": {"email": "active", "whatsapp": "active", "web_form": "active"}
    }

# ---- WhatsApp Webhook ----
@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming WhatsApp messages via Twilio webhook."""
    if not await whatsapp_handler.validate_webhook(request):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    form_data = await request.form()
    message = await whatsapp_handler.process_webhook(dict(form_data))

    background_tasks.add_task(
        kafka_producer.publish,
        TOPICS['tickets_incoming'],
        message
    )

    # Return empty TwiML — agent sends reply asynchronously
    return Response(
        content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
        media_type="application/xml"
    )

# ---- Customer Lookup ----
@app.get("/customers/lookup")
async def lookup_customer(email: str = None, phone: str = None):
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")
    customer = await find_customer(email=email, phone=phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# ---- Channel Metrics ----
@app.get("/metrics/channels")
async def get_channel_metrics():
    """Performance metrics per channel for last 24 hours."""
    return await get_channel_metrics_24h()
