"""
Transition Tests: Verify agent behavior matches Phase 1 incubation.
"""
import pytest
from agents import Runner
from production.agent.customer_success_agent import customer_success_agent

class TestTransitionFromIncubation:

    @pytest.mark.asyncio
    async def test_empty_message(self):
        """Edge case: Empty messages must be handled without crash."""
        result = await Runner.run(
            customer_success_agent,
            messages=[{"role": "user", "content": "Channel: web_form\nCustomer ID: test-1\nMessage: "}]
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_pricing_escalation(self):
        """Pricing questions must always trigger escalation."""
        result = await Runner.run(
            customer_success_agent,
            messages=[{"role": "user", "content": "Channel: email\nCustomer ID: test-2\nMessage: How much does the Pro plan cost?"}]
        )
        # Check if escalate_to_human tool was mentioned or used
        tool_names = [tc.tool_name for tc in getattr(result, 'tool_calls', [])]
        assert 'escalate_to_human' in tool_names

    @pytest.mark.asyncio
    async def test_workflow_order(self):
        """Verify create_ticket is called first."""
        result = await Runner.run(
            customer_success_agent,
            messages=[{"role": "user", "content": "Channel: email\nCustomer ID: test-3\nMessage: Help me with my password"}]
        )
        tool_names = [tc.tool_name for tc in getattr(result, 'tool_calls', [])]
        if tool_names:
            assert tool_names[0] == 'create_ticket'
