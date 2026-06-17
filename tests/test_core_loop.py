import pytest
from src.agent.prototype_agent import CustomerSuccessAgent
from src.agent.models import Channel, ResolutionStatus

@pytest.fixture
def agent():
    return CustomerSuccessAgent()

def test_basic_email_query(agent):
    raw_msg = {
        "channel": "email",
        "customer_email": "alice@startup.com",
        "customer_name": "Alice",
        "subject": "Password reset",
        "content": "How do I reset my password?",
        "timestamp": "2024-01-15T09:23:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.channel == Channel.EMAIL
    assert "Hi Alice" in response.content
    assert "Best regards" in response.content
    assert response.should_escalate is False
    assert "password" in response.content.lower()

def test_basic_whatsapp_query(agent):
    raw_msg = {
        "channel": "whatsapp",
        "customer_phone": "+923001234567",
        "customer_name": "Hassan",
        "content": "how reset password",
        "timestamp": "2024-01-15T12:30:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.channel == Channel.WHATSAPP
    assert len(response.content) <= 300
    assert "Hi" not in response.content
    assert response.should_escalate is False

def test_pricing_escalation(agent):
    raw_msg = {
        "channel": "email",
        "customer_email": "frank@sales.com",
        "customer_name": "Frank",
        "content": "Can we get a discount for 50 users?",
        "timestamp": "2024-01-15T16:00:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is True
    assert response.escalation_reason == "pricing_inquiry"

def test_refund_escalation(agent):
    raw_msg = {
        "channel": "email",
        "customer_email": "charlie@agile.io",
        "content": "I want a full refund.",
        "timestamp": "2024-01-15T11:05:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is True
    assert response.escalation_reason == "refund_request"

def test_legal_escalation(agent):
    raw_msg = {
        "channel": "email",
        "customer_email": "eve@legal.net",
        "content": "I will contact my lawyer.",
        "timestamp": "2024-01-15T15:10:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is True
    assert response.escalation_reason == "legal_threat"

def test_angry_customer_escalation(agent):
    raw_msg = {
        "channel": "whatsapp",
        "customer_phone": "+923034445556",
        "content": "THIS APP IS GARBAGE FIX IT NOW",
        "timestamp": "2024-01-15T20:00:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is True
    assert response.sentiment_score < 0.4

def test_human_request_escalation(agent):
    raw_msg = {
        "channel": "whatsapp",
        "customer_phone": "+923019876543",
        "content": "human please",
        "timestamp": "2024-01-15T13:45:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is True
    assert response.escalation_reason == "human_requested"

def test_empty_message_handling(agent):
    raw_msg = {
        "channel": "web_form",
        "customer_email": "test@test.com",
        "message": "",
        "timestamp": "2024-01-15T10:00:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is True # No results + no content
    assert "specialist" in response.content

def test_multiple_questions(agent):
    raw_msg = {
        "channel": "email",
        "customer_email": "alice@startup.com",
        "content": "How do I reset my password and how do I invite team members?",
        "timestamp": "2024-01-15T09:23:00Z"
    }
    response = agent.process_message(raw_msg)
    assert response.should_escalate is False
    assert len(response.content) > 0

def test_cross_channel_memory(agent):
    msg1 = {
        "channel": "email",
        "customer_email": "alice@startup.com",
        "content": "Help with password",
        "timestamp": "2024-01-15T09:00:00Z"
    }
    agent.process_message(msg1)
    
    msg2 = {
        "channel": "whatsapp",
        "customer_phone": "+923001234567",
        "customer_name": "Alice",
        "content": "I also emailed you. My email is alice@startup.com",
        "timestamp": "2024-01-15T10:00:00Z"
    }
    # For prototype, identify via email field in whatsapp
    raw_msg2 = {
        "channel": "whatsapp",
        "customer_phone": "+923001234567",
        "customer_name": "Alice",
        "customer_email": "alice@startup.com",
        "content": "invite members",
        "timestamp": "2024-01-15T10:00:00Z"
    }
    agent.process_message(raw_msg2)
    
    state = agent.memory.get_or_create("alice@startup.com", "Alice", "email")
    assert len(state.messages) >= 4 # 2 sets of customer+agent
    assert "whatsapp" in state.channels_used
    assert "email" in state.channels_used

def test_sentiment_range(agent):
    msg = {
        "channel": "email",
        "customer_email": "test@test.com",
        "content": "This is great, thank you so much!",
        "timestamp": "2024-01-15T10:00:00Z"
    }
    response = agent.process_message(msg)
    assert 0.5 < response.sentiment_score <= 1.0

def test_response_not_empty(agent):
    msg = {
        "channel": "email",
        "customer_email": "test@test.com",
        "content": "hello",
        "timestamp": "2024-01-15T10:00:00Z"
    }
    response = agent.process_message(msg)
    assert response.content != ""
