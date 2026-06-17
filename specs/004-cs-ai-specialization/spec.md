# Feature Specification: CS AI Production Specialization (Phase 2)

**Feature Branch**: `004-cs-ai-specialization`  
**Created**: 2026-04-27  
**Status**: Draft  
**Input**: Phase 2 — Production System Specialization for Customer Success AI Agent.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Web Support Form Interaction (Priority: P1)

A customer encounters an issue and navigates to the TechFlow support page. They fill out a React-based support form with their name, email, issue category, and a detailed message. Upon submission, they receive an immediate ticket ID and an estimated response time.

**Why this priority**: The web form is a required, high-value component (10 marks) providing a structured entry point for production support.

**Independent Test**: Can be tested by rendering the `SupportForm.jsx` component, filling it with valid data, and verifying the successful generation of a ticket ID from the API.

**Acceptance Scenarios**:

1. **Given** the support form is loaded, **When** a user submits valid details, **Then** a ticket is created in PostgreSQL and a success message with a UUID is displayed.
2. **Given** an invalid email address, **When** the user clicks submit, **Then** client-side validation prevents submission and shows an error message.

---

### User Story 2 - Real-time WhatsApp Support (Priority: P1)

A customer sends a WhatsApp message to the TechFlow support number (Twilio Sandbox). The system identifies the customer via their phone number, retrieves their history from the PostgreSQL CRM, and the AI agent provides a concise, channel-appropriate response (under 300 characters).

**Why this priority**: Real API integration (Twilio) is a core requirement for Phase 2 production specialization.

**Independent Test**: Send a WhatsApp message to the Sandbox number and verify a response is received within 3 seconds, following the concise WhatsApp brand voice.

**Acceptance Scenarios**:

1. **Given** a WhatsApp message from a known customer, **When** processed by the worker, **Then** the agent greets them and provides a response based on KB info.

---

### User Story 3 - Unified Cross-Channel Continuity (Priority: P2)

A customer who previously used the web form sends a follow-up email. The system recognizes the email address, links the interaction to the same customer UUID in the PostgreSQL CRM, and the AI agent references the previous web form ticket context.

**Why this priority**: Essential for operational excellence and maintaining a high-quality customer experience across distributed channels.

**Independent Test**: Submit a web form, then send an email from the same address, and verify the `get_customer_history` tool returns the web form interaction.

**Acceptance Scenarios**:

1. **Given** an existing customer record, **When** a message arrives from a different channel with a matching identifier, **Then** the interaction is appended to the unified history.

---

### Edge Cases

- **Service Degradation**: If Kafka or PostgreSQL is temporarily unavailable, the API should handle the failure gracefully (e.g., DLQ for Kafka, error responses for API).
- **Extreme Payload**: Handle messages exceeding the defined character/word limits (Email: 500w, WA: 300c) by truncating with a polite "read more" hint.
- **Empty/Gibberish Input**: Agent should detect low sentiment or lack of intent and escalate to a human agent immediately.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: **Multi-Channel API Integration**: System MUST integrate with real Gmail (OAuth2) and Twilio (WhatsApp) APIs.
- **FR-002**: **Distributed Event Processing**: All incoming messages MUST be published to a Kafka bus (`fte.tickets.incoming`) for asynchronous processing by worker pods.
- **FR-003**: **PostgreSQL CRM**: System MUST use PostgreSQL as the primary CRM, implementing the 8-table schema (customers, identifiers, conversations, messages, tickets, KB, configs, metrics).
- **FR-004**: **Semantic Knowledge Retrieval**: Product documentation MUST be stored with `pgvector` embeddings and retrieved using semantic search (min similarity 0.7).
- **FR-005**: **OpenAI Agents SDK**: The core agent logic MUST be implemented using the OpenAI Agents SDK, employing exactly 5 `@function_tool` definitions.
- **FR-006**: **Production Web Form**: A complete React-based support form MUST be provided, including full client-side validation and ticket status checking.
- **FR-007**: **Kubernetes Readiness**: The system MUST be deployable to Kubernetes with HPA (auto-scaling), PDB (survivability), and health checks.

### Key Entities *(include if feature involves data)*

- **Customer**: Unified record linked to multiple identifiers (Email, Phone).
- **Conversation**: 24-hour session window grouping multiple messages.
- **Ticket**: Distinct support issue with status tracking (Open, Processing, Resolved, Escalated).
- **Message**: Individual interaction record with direction, role, and channel metadata.
- **KnowledgeBaseEntry**: Documentation chunk with title, content, and vector embedding.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **System Uptime**: API and Worker pods maintain >99.9% uptime under 24-hour continuous operation.
- **SC-002**: **Response Latency**: 95% of automated responses are generated and sent (or stored) in under 3,000 milliseconds.
- **SC-003**: **Escalation Accuracy**: System correctly escalates at least 90% of pricing, refund, and legal requests to human agents.
- **SC-004**: **Scalability**: System handles 100+ concurrent requests in load testing with P95 latency < 3 seconds.
- **SC-005**: **Data Integrity**: 100% of messages processed are correctly logged with channel-specific metadata in the PostgreSQL CRM.
