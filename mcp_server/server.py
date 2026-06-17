import asyncio
import json
import uuid
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from src.agent.prototype_agent import CustomerSuccessAgent
from src.agent.models import Channel, Priority, ResolutionStatus

# Initialize agent
agent = CustomerSuccessAgent()

server = Server("customer-success-fte")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="search_knowledge_base",
            description="Search product documentation for relevant answers",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="create_ticket",
            description="Log a new customer issue in the memory system",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "issue": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
                    "channel": {"type": "string", "enum": ["email", "whatsapp", "web_form"]},
                    "customer_name": {"type": "string"}
                },
                "required": ["customer_id", "issue", "priority", "channel"],
            },
        ),
        types.Tool(
            name="get_customer_history",
            description="Retrieve previous interactions for a customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "max_messages": {"type": "integer", "default": 10}
                },
                "required": ["customer_id"],
            },
        ),
        types.Tool(
            name="escalate_to_human",
            description="Flag a ticket for human intervention",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "reason": {"type": "string"},
                    "channel": {"type": "string"}
                },
                "required": ["ticket_id", "customer_id", "reason", "channel"],
            },
        ),
        types.Tool(
            name="send_response",
            description="Format and send an outbound response to the customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "message": {"type": "string"},
                    "channel": {"type": "string"},
                    "customer_name": {"type": "string"}
                },
                "required": ["ticket_id", "customer_id", "message", "channel"],
            },
        ),
        types.Tool(
            name="analyze_sentiment",
            description="Calculate sentiment score for a given text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "customer_id": {"type": "string"}
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="update_ticket_status",
            description="Update the resolution status of an existing ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["open", "pending", "resolved", "escalated"]}
                },
                "required": ["customer_id", "status"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if not arguments:
        raise ValueError("Missing arguments")

    if name == "search_knowledge_base":
        results = agent.search_knowledge_base(arguments["query"], arguments.get("max_results", 5))
        return [types.TextContent(type="text", text=json.dumps(results, indent=2))]

    elif name == "create_ticket":
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        agent.memory.get_or_create(
            arguments["customer_id"], 
            arguments.get("customer_name", "Customer"),
            arguments["channel"]
        )
        return [types.TextContent(type="text", text=json.dumps({
            "ticket_id": ticket_id,
            "status": "created",
            "message": "Ticket logged successfully"
        }))]

    elif name == "get_customer_history":
        history = agent.memory.get_history_for_agent(arguments["customer_id"], arguments.get("max_messages", 10))
        return [types.TextContent(type="text", text=json.dumps(history, indent=2))]

    elif name == "escalate_to_human":
        agent.memory.update_resolution_status(arguments["customer_id"], ResolutionStatus.ESCALATED)
        return [types.TextContent(type="text", text=json.dumps({
            "escalation_id": f"ESC-{arguments['ticket_id']}",
            "status": "escalated",
            "reason": arguments["reason"]
        }))]

    elif name == "send_response":
        formatted = agent.format_for_channel(
            arguments["message"], 
            Channel(arguments["channel"]), 
            arguments.get("customer_name", "Customer")
        )
        agent.memory.add_message(arguments["customer_id"], "agent", formatted, arguments["channel"])
        return [types.TextContent(type="text", text=json.dumps({
            "status": "sent",
            "formatted_response": formatted
        }))]

    elif name == "analyze_sentiment":
        score = agent.analyze_sentiment(arguments["text"])
        label = "neutral"
        if score > 0.6: label = "positive"
        elif score < 0.4: label = "negative"
        
        return [types.TextContent(type="text", text=json.dumps({
            "score": score,
            "label": label
        }))]

    elif name == "update_ticket_status":
        agent.memory.update_resolution_status(arguments["customer_id"], ResolutionStatus(arguments["status"]))
        return [types.TextContent(type="text", text=json.dumps({
            "status": "updated",
            "new_status": arguments["status"]
        }))]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_server):
        await server.run(
            read_stream,
            write_server,
            InitializationOptions(
                server_name="customer-success-fte",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
