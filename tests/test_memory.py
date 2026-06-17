import pytest
from src.agent.memory import ConversationMemory
from src.agent.models import ResolutionStatus

@pytest.fixture
def memory():
    return ConversationMemory()

def test_new_customer_state(memory):
    state = memory.get_or_create("user@test.com", "Test User", "email", email="user@test.com")
    assert state.customer_id == "user@test.com"
    assert state.customer_name == "Test User"
    assert "email" in state.channels_used

def test_add_message_and_history(memory):
    customer_id = "user@test.com"
    memory.get_or_create(customer_id, "Test User", "email")
    memory.add_message(customer_id, "customer", "Hello", "email", sentiment=0.5, topics=["greeting"])
    memory.add_message(customer_id, "agent", "Hi there", "email")
    
    history = memory.get_history_for_agent(customer_id)
    assert len(history) == 2
    assert history[0]["role"] == "customer"
    assert history[1]["role"] == "agent"

def test_cross_channel_merging(memory):
    # First contact via email
    memory.get_or_create("alice@startup.com", "Alice", "email", email="alice@startup.com")
    memory.add_message("alice@startup.com", "customer", "Email message", "email")
    
    # Second contact via whatsapp (different ID but same email provided in metadata)
    state = memory.get_or_create("+923001234567", "Alice", "whatsapp", email="alice@startup.com", phone="+923001234567")
    
    assert state.customer_email == "alice@startup.com"
    assert state.customer_phone == "+923001234567"
    assert "email" in state.channels_used
    assert "whatsapp" in state.channels_used
    assert len(state.messages) == 1 # The email message is there

def test_sentiment_trend(memory):
    customer_id = "user@test.com"
    memory.get_or_create(customer_id, "Test User", "email")
    memory.update_sentiment_trend(customer_id, 0.8)
    memory.update_sentiment_trend(customer_id, 0.5)
    memory.update_sentiment_trend(customer_id, 0.2)
    
    assert memory.is_sentiment_declining(customer_id) is True

def test_daily_report(memory):
    memory.get_or_create("u1@test.com", "U1", "email")
    memory.update_sentiment_trend("u1@test.com", 0.8)
    memory.update_resolution_status("u1@test.com", ResolutionStatus.RESOLVED)
    
    memory.get_or_create("u2@test.com", "U2", "whatsapp")
    memory.update_sentiment_trend("u2@test.com", 0.2)
    memory.update_resolution_status("u2@test.com", ResolutionStatus.ESCALATED)
    
    report = memory.generate_daily_report()
    assert report["total_conversations"] == 2
    assert report["escalation_rate_percent"] == 50.0
    assert report["resolution_rate_percent"] == 50.0
