import time
from typing import Dict, Any

class WhatsAppHandler:
    def simulate_incoming_whatsapp(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts WhatsApp ticket to raw format with Twilio-style fields.
        """
        return {
            "channel": "whatsapp",
            "customer_phone": ticket.get("customer_phone"),
            "customer_name": ticket.get("customer_name"),
            "content": ticket.get("content"),
            "timestamp": ticket.get("timestamp"),
            "twilio_message_sid": f"SM_{int(time.time())}",
            "from_number": ticket.get("customer_phone"),
            "to_number": "+14155551234"  # Simulated TechFlow number
        }

    def simulate_send_whatsapp(self, to_number: str, body: str) -> Dict[str, Any]:
        """
        Simulates sending WhatsApp message.
        Validates: body must be ≤ 300 characters.
        """
        if len(body) > 300:
            raise ValueError(f"WhatsApp message exceeds 300 character limit: {len(body)}")
            
        print(f"[WHATSAPP SIMULATION] Sending to {to_number}: {body}")
        return {
            "status": "sent",
            "sid": f"SM_sim_{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
