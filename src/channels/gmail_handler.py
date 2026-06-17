import time
from typing import Dict, Any

class GmailHandler:
    def simulate_incoming_email(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a ticket from sample-tickets.json into the raw email format.
        """
        return {
            "channel": "email",
            "customer_email": ticket.get("customer_email"),
            "customer_name": ticket.get("customer_name"),
            "subject": ticket.get("subject"),
            "content": ticket.get("content"),
            "timestamp": ticket.get("timestamp"),
            "gmail_message_id": f"msg_{int(time.time())}",
            "gmail_thread_id": f"thread_{ticket.get('id')}"
        }

    def simulate_send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Simulates sending an email.
        """
        print(f"[GMAIL SIMULATION] Sending to {to}: {body[:100]}...")
        return {
            "status": "sent",
            "message_id": f"sim_{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
