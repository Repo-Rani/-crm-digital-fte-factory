# Implementation Plan: CS AI Production Specialization (Phase 2)

**Branch**: `004-cs-ai-specialization` | **Date**: 2026-04-27 | **Spec**: [specs/004-cs-ai-specialization/spec.md]

## Summary

The goal of this plan is to transform the Phase 1 prototype into a production-grade distributed system. The architecture transitions from in-memory state and simulated channels to a robust stack featuring FastAPI, Kafka for event streaming, PostgreSQL (CRM) with pgvector for semantic search, and real-world API integrations (Gmail, Twilio). The core agent logic will be re-implemented using the OpenAI Agents SDK with a specialized 5-tool set.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: `fastapi`, `openai-agents`, `aiokafka`, `asyncpg`, `twilio`, `google-api-python-client`, `pgvector`  
**Storage**: PostgreSQL 16 (CRM) + pgvector (Embeddings)  
**Testing**: `pytest`, `pytest-asyncio`, `locust` (Load testing)  
**Target Platform**: Kubernetes (HPA, PDB enabled)  
**Project Type**: Distributed System (API + Workers)  
**Performance Goals**: < 3,000ms response time; > 99.9% uptime; 100+ concurrent requests  
**Constraints**: 23-hour development budget; production-grade async code required

## Constitution Check

- [x] **Production Standards**: All code uses async/await, connection pooling, and structured logging.
- [x] **Distributed Architecture**: Decoupled API layer and Kafka-based processing workers.
- [x] **Strict Data Persistence**: PostgreSQL is the sole source of truth for CRM data (8 tables).
- [x] **Real-world Integration**: Real APIs for Gmail and WhatsApp (Twilio Sandbox).
- [x] **Production Safety**: Secrets managed exclusively via environment variables and `.env`.
- [x] **Scalability**: Kubernetes readiness with HPA and health checks.

## Project Structure

### Documentation (this feature)

```text
specs/004-cs-ai-specialization/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/          
│   └── requirements.md  # Quality checklist (PASSED)
└── tasks.md             # Implementation tasks
```

### Source Code (Production Directory)

```text
production/
├── agent/
│   ├── customer_success_agent.py   # OpenAI Agents SDK setup
│   ├── tools.py                    # @function_tool definitions (5 tools)
│   ├── prompts.py                  # Refined system prompts
│   └── formatters.py               # Channel-specific formatting
├── channels/
│   ├── gmail_handler.py            # OAuth2 + Gmail API
│   ├── whatsapp_handler.py         # Twilio WhatsApp integration
│   └── web_form_handler.py         # FastAPI Support Form router
├── workers/
│   ├── message_processor.py        # Kafka consumer → Agent logic
│   └── metrics_collector.py        # Background metrics aggregation
├── api/
│   └── main.py                     # FastAPI entry point
├── database/
│   ├── schema.sql                  # 8-table CRM schema
│   ├── queries.py                  # Async DB functions
│   └── migrations/                 # Initial migration
├── web-form/
│   ├── SupportForm.jsx             # REQUIRED: React Component
│   └── package.json                # Frontend dependencies
├── tests/
│   ├── test_transition.py          # Parity tests
│   ├── test_multichannel_e2e.py    # End-to-end integration tests
│   └── load_test.py                # Locust performance test
└── k8s/                            # 9 Kubernetes manifests
```

## Implementation Steps

### Phase 1: Infrastructure & Environment
1. Initialize `production/` structure and `requirements.txt`.
2. Configure `.env.example` and `docker-compose.yml` (Postgres, Kafka, Zookeeper).
3. Implement `Dockerfile` for multi-stage production builds.

### Phase 2: Data & Persistence (Ex 2.1)
1. Write `database/schema.sql` with all 8 tables and necessary indexes.
2. Implement `database/queries.py` using `asyncpg` connection pooling.
3. Seed `knowledge_base` from Phase 1 documentation using pgvector.

### Phase 3: Core Event Bus (Ex 2.5)
1. Implement `kafka_client.py` for async producing/consuming.
2. Define the topic registry (incoming, metrics, DLQ).

### Phase 4: Production Agent (Ex 2.3)
1. Port system prompts to `agent/prompts.py`.
2. Implement the 5 core tools in `agent/tools.py` using the OpenAI Agents SDK.
3. Create the `customer_success_agent` instance.

### Phase 5: Channel Real-world APIs (Ex 2.2)
1. Implement `channels/gmail_handler.py` (OAuth2 flow).
2. Implement `channels/whatsapp_handler.py` (Twilio Webhook validation).
3. Build the REQUIRED `web-form/SupportForm.jsx` React component.

### Phase 6: Service Layer (Ex 2.4, 2.6)
1. Implement `api/main.py` with webhook receivers and status endpoints.
2. Implement `workers/message_processor.py` (the unified worker loop).

### Phase 7: Deployment & Verification (Ex 2.7, 3.1)
1. Create all 9 Kubernetes manifests in `k8s/`.
2. Implement E2E and transition tests in `tests/`.
3. Run Locust load test to verify scalability targets.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Kafka Integration | Required for 24/7 reliability and survivability | Simple API calls would block and risk data loss on pod restart |
| pgvector Extension | Semantic search requirements | Keyword matching (Phase 1) lacks production-grade accuracy |
