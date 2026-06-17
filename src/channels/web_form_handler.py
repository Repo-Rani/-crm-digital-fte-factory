import time
from typing import Dict, Any

class WebFormHandler:
    def simulate_form_submission(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts web form ticket to raw format.
        """
        return {
            "channel": "web_form",
            "customer_email": ticket.get("customer_email"),
            "customer_name": ticket.get("customer_name"),
            "subject": ticket.get("subject"),
            "message": ticket.get("content"),
            "category": ticket.get("category"),
            "priority": ticket.get("priority"),
            "timestamp": ticket.get("timestamp"),
            "form_submission_id": f"sub_{int(time.time())}",
            "ip_address": "127.0.0.1"
        }

    def simulate_form_response(self, submission_id: str, response_text: str) -> Dict[str, Any]:
        """
        Returns simulated response JSON as if API returned it.
        """
        print(f"[WEB FORM SIMULATION] Responding to {submission_id}")
        return {
            "status": "responded",
            "submission_id": submission_id,
            "response": response_text,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
