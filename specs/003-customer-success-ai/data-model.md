# Data Model: Customer Success AI Agent (Phase 1)

This document defines the core data structures used by the Customer Success AI Agent prototype.

## 1. CustomerMessage (Input)
Represents a normalized message from any channel.

| Field | Type | Description |
|-------|------|-------------|
| `channel` | `Channel` (Enum) | `EMAIL`, `WHATSAPP`, `WEB_FORM` |
| `customer_id` | `str` | Primary key: Email address or phone number |
| `customer_name` | `str` | Display name (default: "Customer") |
| `content` | `str` | Normalized message body text |
| `subject` | `Optional[str]` | Subject line (Email only) |
| `phone` | `Optional[str]` | Phone number (WhatsApp only) |
| `timestamp` | `str` | ISO 8601 timestamp |
| `metadata` | `dict` | Extra channel-specific fields |

## 2. AgentResponse (Output)
Represents the result of agent processing.

| Field | Type | Description |
|-------|------|-------------|
| `content` | `str` | Formatted response text ready for sending |
| `channel` | `Channel` | Target channel for the response |
| `should_escalate` | `bool` | True if human intervention is required |
| `escalation_reason` | `Optional[str]` | Reason for escalation (e.g., `refund_request`) |
| `sentiment_score` | `float` | Calculated score (-1.0 to 1.0) |
| `topics_discussed` | `list[str]` | Extracted keywords/categories |
| `resolution_status` | `str` | `resolved`, `pending`, or `escalated` |
| `response_time_ms` | `int` | Total processing duration |

## 3. MessageRecord (Memory Item)
An individual entry in the conversation history.

| Field | Type | Description |
|-------|------|-------------|
| `role` | `str` | `customer` or `agent` |
| `content` | `str` | The message text |
| `channel` | `str` | The channel used for this message |
| `timestamp` | `str` | ISO 8601 timestamp |
| `sentiment_score`| `Optional[float]` | Sentiment for customer messages |
| `topics` | `list[str]` | Extracted topics (agent logic) |

## 4. ConversationState (Persistence)
The full state for a unique customer.

| Field | Type | Description |
|-------|------|-------------|
| `customer_id` | `str` | Primary identifier (Email or Phone) |
| `customer_name` | `str` | Customer's display name |
| `customer_email` | `Optional[str]` | Verified email address |
| `customer_phone` | `Optional[str]` | Verified phone number |
| `channels_used` | `list[str]` | History of all channels used |
| `messages` | `list[MessageRecord]` | Chronological conversation history |
| `sentiment_trend` | `list[float]` | Last 20 sentiment scores |
| `resolution_status` | `ResolutionStatus` | `OPEN`, `PENDING`, `RESOLVED`, `ESCALATED` |
| `last_updated` | `str` | ISO 8601 timestamp |

## 5. SkillDefinition (Metadata)
Definition of an agent capability.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Unique skill name |
| `description` | `str` | What the skill does |
| `trigger` | `SkillTrigger` | When the skill should activate |
| `inputs` | `list[str]` | Required data fields |
| `outputs` | `list[str]` | Provided data fields |
| `constraints` | `list[str]` | Logic limitations |
