import pytest
import json
import asyncio
from mcp_server.server import handle_call_tool

@pytest.mark.asyncio
async def test_mcp_search_kb():
    args = {"query": "password reset", "max_results": 1}
    response = await handle_call_tool("search_knowledge_base", args)
    assert len(response) == 1
    results = json.loads(response[0].text)
    assert len(results) > 0
    assert "Password Reset" in results[0]["title"]

@pytest.mark.asyncio
async def test_mcp_create_ticket():
    args = {
        "customer_id": "mcp@test.com",
        "issue": "help",
        "priority": "low",
        "channel": "email"
    }
    response = await handle_call_tool("create_ticket", args)
    result = json.loads(response[0].text)
    assert result["status"] == "created"
    assert "TKT-" in result["ticket_id"]

@pytest.mark.asyncio
async def test_mcp_analyze_sentiment():
    args = {"text": "I love this app!"}
    response = await handle_call_tool("analyze_sentiment", args)
    result = json.loads(response[0].text)
    assert result["score"] > 0.6
    assert result["label"] == "positive"

@pytest.mark.asyncio
async def test_mcp_send_response():
    args = {
        "ticket_id": "TKT-123",
        "customer_id": "mcp@test.com",
        "message": "Here is your answer",
        "channel": "email",
        "customer_name": "MCP User"
    }
    response = await handle_call_tool("send_response", args)
    result = json.loads(response[0].text)
    assert result["status"] == "sent"
    assert "Hi MCP User" in result["formatted_response"]
