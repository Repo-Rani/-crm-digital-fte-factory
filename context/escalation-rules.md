# Escalation Rules

This document defines the logic and criteria for escalating a customer interaction from the AI agent to a human support specialist.

## Hard Escalation Triggers (100% Always Escalate)
The AI agent MUST immediately stop processing and escalate the interaction if any of the following are detected:

1.  **Refund Requests**: Any mention of "refund", "money back", "charge dispute", "chargeback", or "reverse charge".
2.  **Pricing Negotiation**: Requests for discounts, lower prices, or price matching (e.g., "can I get a discount", "negotiate price").
3.  **Legal Language**: Use of terms like "lawyer", "attorney", "sue", "legal action", "court", or "GDPR complaint".
4.  **Explicit Human Request**: Customer phrases like "I want a human", "speak to an agent", "real person", or "representative".
5.  **WhatsApp Magic Words**: For the WhatsApp channel only, the words "human", "agent", or "representative" (case-insensitive) trigger escalation regardless of context.
6.  **Profanity**: Any detectable profanity or highly abusive language.
7.  **Security Concerns**: Mentions of "data breach", "unauthorized access", "hacked", "security leak", or "compromised account".

## Conditional Escalation Triggers
Escalate based on specific metrics or context:

1.  **Low Sentiment**: Customer sentiment score falls below 0.3.
2.  **Declining Sentiment**: Sentiment scores are strictly declining over 3 or more consecutive messages.
3.  **Knowledge Base Failure**: No relevant answer found in the knowledge base after 2 search attempts.
4.  **Severe Bug Reports**: Reports involving data loss or affecting multiple users (e.g., "system is down for everyone").

## Escalation Message Templates

| Channel | Template |
|---------|----------|
| **Email** | "I understand this is important. I've flagged your case for our specialist team who will respond within [TIME]. Your reference: [TICKET_ID]." |
| **WhatsApp** | "Got it! Connecting you to our team now. They'll reach out within [TIME] 🙏 Ref: [TICKET_ID]" |
| **Web Form** | "I've escalated your request to our specialist team. Expected response: [TIME]. Reference number: [TICKET_ID]." |

## Target Response Times by Priority
- **Urgent**: Within 1 hour
- **High**: Within 4 hours
- **Medium**: Within 24 hours
- **Low**: Within 48 hours
