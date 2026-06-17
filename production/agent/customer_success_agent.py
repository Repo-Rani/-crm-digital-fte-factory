"""
Production Customer Success Agent using OpenAI Agents SDK.
"""

from agents import Agent
from .tools import (
    search_knowledge_base, create_ticket,
    get_customer_history, escalate_to_human, send_response
)
from .prompts import CUSTOMER_SUCCESS_SYSTEM_PROMPT

customer_success_agent = Agent(
    name="Customer Success FTE",
    model="gpt-4o",
    instructions=CUSTOMER_SUCCESS_SYSTEM_PROMPT,
    tools=[
        search_knowledge_base,
        create_ticket,
        get_customer_history,
        escalate_to_human,
        send_response
    ]
)
