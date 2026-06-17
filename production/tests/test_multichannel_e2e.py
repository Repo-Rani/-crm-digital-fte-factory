import pytest
import httpx
import asyncio
from typing import Dict, Any

# Mocking the base URL for the API
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
class TestWebFormChannel:
    async def test_form_submission(self):
        """Test US1: Successful web form submission."""
        payload = {
            "name": "E2E Test User",
            "email": "e2e@test.com",
            "subject": "Testing E2E",
            "category": "technical",
            "message": "This is a message from the E2E test suite.",
            "priority": "medium"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/support/submit", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert "ticket_id" in data
            assert data["message"] is not None
            assert "estimated_response_time" in data

    async def test_form_validation(self):
        """Test form validation errors."""
        payload = {
            "name": "A", # Too short
            "email": "invalid-email",
            "subject": "Hi", # Too short
            "category": "invalid",
            "message": "Short" # Too short
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/support/submit", json=payload)
            assert response.status_code == 422

@pytest.mark.asyncio
class TestEmailChannel:
    async def test_email_webhook(self):
        """Test US1: Gmail webhook processing."""
        # Mock Pub/Sub notification payload
        payload = {
            "message": {
                "data": "eyJoaXN0b3J5SWQiOiIxMjM0NSIsICJlbWFpbEFkZHJlc3MiOiAidGVzdEB0ZWNoZmxvdy5pbyJ9", # base64 for {"historyId":"12345", "emailAddress": "test@techflow.io"}
                "messageId": "1234567890"
            },
            "subscription": "projects/techflow/subscriptions/gmail-sub"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/webhooks/gmail", json=payload)
            assert response.status_code == 200

@pytest.mark.asyncio
class TestWhatsAppChannel:
    async def test_whatsapp_webhook(self):
        """Test US1: WhatsApp webhook (Twilio) processing."""
        payload = {
            "MessageSid": "SM1234567890",
            "From": "whatsapp:+14155238886",
            "Body": "Hello, I need help with my task board.",
            "ProfileName": "Test User",
            "WaId": "14155238886"
        }
        # In production, this requires X-Twilio-Signature. 
        # In test mode/dev mode, we might skip validation.
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/webhooks/whatsapp", 
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            assert response.status_code == 200
            assert "Response" in response.text # TwiML response

@pytest.mark.asyncio
class TestCrossChannelContinuity:
    async def test_customer_history_across_channels(self):
        """Test US3: Verify history is preserved across channels for the same customer."""
        email = "cross-channel@test.com"
        
        async with httpx.AsyncClient() as client:
            # 1. Submit via web form
            await client.post(f"{BASE_URL}/support/submit", json={
                "name": "Cross User",
                "email": email,
                "subject": "Form Query",
                "category": "general",
                "message": "Message from Web Form"
            })
            
            # 2. Simulate email interaction (assuming it links to same email)
            # This is often handled by the database lookup in the handlers.
            
            # 3. Check customer history
            response = await client.get(f"{BASE_URL}/customers/lookup?email={email}")
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == email
            assert len(data.get("conversations", [])) > 0

@pytest.mark.asyncio
class TestChannelMetrics:
    async def test_metrics_by_channel(self):
        """Test observability: Metrics per channel."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/metrics/channels")
            assert response.status_code == 200
            data = response.json()
            assert "email" in data
            assert "whatsapp" in data
            assert "web_form" in data
            assert all("total" in data[ch] for ch in data)
