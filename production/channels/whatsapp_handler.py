"""
WhatsApp Channel Handler — Production via Twilio
Handles webhook validation, incoming message processing,
and outbound message sending.
"""

import os
import logging
from datetime import datetime, timezone
from twilio.rest import Client
from twilio.request_validator import RequestValidator
from fastapi import Request, HTTPException
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class WhatsAppHandler:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.validator = RequestValidator(self.auth_token)
        else:
            self.client = None
            self.validator = None
            logger.warning("Twilio credentials missing. WhatsApp handler limited.")

    async def validate_webhook(self, request: Request) -> bool:
        """Validate incoming Twilio webhook signature."""
        if os.getenv('ENVIRONMENT') == 'development':
            return True  # Skip for local sandbox testing

        if not self.validator:
            return False

        signature = request.headers.get('X-Twilio-Signature', '')
        url = str(request.url)
        form_data = await request.form()
        params = dict(form_data)
        
        return self.validator.validate(url, params, signature)

    async def process_webhook(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming WhatsApp message from Twilio."""
        phone = form_data.get('From', '').replace('whatsapp:', '')
        return {
            'channel': 'whatsapp',
            'channel_message_id': form_data.get('MessageSid'),
            'customer_phone': phone,
            'customer_name': form_data.get('ProfileName', 'Customer'),
            'content': form_data.get('Body', ''),
            'received_at': datetime.now(timezone.utc).isoformat(),
            'metadata': {
                'wa_id': form_data.get('WaId'),
                'status': form_data.get('SmsStatus')
            }
        }

    async def send_message(self, to_phone: str, body: str) -> Dict[str, Any]:
        """Send WhatsApp message via Twilio."""
        if not self.client:
            raise RuntimeError("Twilio client not initialized")

        if not to_phone.startswith('whatsapp:'):
            to_phone = f'whatsapp:{to_phone}'

        try:
            # Simple single-message send for MVP
            message = self.client.messages.create(
                body=body,
                from_=self.whatsapp_number,
                to=to_phone
            )
            logger.info(f"WhatsApp sent to {to_phone}: {message.sid}")
            return {'channel_message_id': message.sid, 'delivery_status': message.status}
        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {to_phone}: {e}")
            return {'channel_message_id': None, 'delivery_status': 'failed'}
