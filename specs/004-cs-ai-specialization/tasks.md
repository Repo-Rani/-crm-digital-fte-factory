---

description: "Actionable task list for CS AI Production Specialization (Phase 2)"
---

# Tasks: CS AI Production Specialization (Phase 2)

**Input**: Design documents from `/specs/004-cs-ai-specialization/`
**Prerequisites**: plan.md (required), spec.md (required)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All paths are relative to the project root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic production structure

- [ ] T001 Initialize production project structure (`production/agent`, `production/channels`, `production/api`, etc.)
- [ ] T002 Create `production/requirements.txt` with all production dependencies
- [ ] T003 Create `production/.env.example` with required production variables
- [ ] T004 Implement production `Dockerfile` for multi-stage builds
- [ ] T005 Implement `production/docker-compose.yml` for local service orchestration (Postgres, Kafka)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Write `production/database/schema.sql` with all 8 CRM tables and indexes
- [ ] T007 Implement `production/database/queries.py` with asyncpg connection pooling
- [ ] T008 [P] Implement `production/kafka_client.py` for async event streaming
- [ ] T009 Port system prompts to `production/agent/prompts.py`
- [ ] T010 Implement core agent tools in `production/agent/tools.py` using OpenAI Agents SDK
- [ ] T011 [P] Implement `production/agent/formatters.py` for channel-specific response logic
- [ ] T012 Initialize `production/agent/customer_success_agent.py` with tools and prompts
- [ ] T013 Implement KB seeding logic in `production/database/queries.py` using pgvector

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Web Support Form (Priority: P1) 🎯 MVP

**Goal**: Provide a production-grade React support form with backend integration

**Independent Test**: Render `SupportForm.jsx`, submit valid data, and verify ticket creation in Postgres.

### Implementation for User Story 1

- [ ] T014 [P] [US1] Create `production/channels/web_form_handler.py` with FastAPI router and Pydantic models
- [ ] T015 [US1] Implement `production/web-form/SupportForm.jsx` React component with full validation
- [ ] T016 [US1] Add `POST /support/submit` logic to publish normalized message to Kafka
- [ ] T017 [US1] Add `GET /support/ticket/{id}` endpoint for status checking
- [ ] T018 [US1] Add integration test for web form flow in `production/tests/test_multichannel_e2e.py`

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Real-time WhatsApp Support (Priority: P1)

**Goal**: Real Twilio integration for WhatsApp messaging

**Independent Test**: Send a message to Twilio Sandbox and verify agent response via Kafka worker.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement `production/channels/whatsapp_handler.py` with Twilio signature validation
- [ ] T020 [US2] Implement WhatsApp message normalization and publishing in `production/api/main.py`
- [ ] T021 [US2] Implement outbound WhatsApp reply logic in `production/agent/tools.py`
- [ ] T022 [US2] Add unit test for WhatsApp handler in `production/tests/test_multichannel_e2e.py`

**Checkpoint**: User Stories 1 and 2 are both independently functional.

---

## Phase 5: User Story 3 - Unified Cross-Channel Continuity (Priority: P2)

**Goal**: Seamless customer recognition and history across all channels

**Independent Test**: Submit form then send email/WhatsApp and verify history continuity.

### Implementation for User Story 3

- [ ] T023 [P] [US3] Implement `production/channels/gmail_handler.py` with OAuth2 and Pub/Sub support
- [ ] T024 [US3] Implement identity merging logic in `production/database/queries.py`
- [ ] T025 [US3] Implement `production/workers/message_processor.py` unified worker loop
- [ ] T026 [US3] Add transition parity test in `production/tests/test_transition.py`

**Checkpoint**: All user stories are now independently functional and integrated via Kafka.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and deployment readiness

- [ ] T027 [P] Create 9 Kubernetes manifests in `production/k8s/` (HPA, PDB, Services)
- [ ] T028 Implement `production/tests/load_test.py` using Locust
- [ ] T029 Perform final code cleanup and structured logging verification
- [ ] T030 Validate and update `production/web-form/README.md` for form integration

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Stories (Phase 3+)**: All depend on Foundational completion.
- **Polish (Final Phase)**: Depends on all user stories being complete.

### Implementation Strategy

- **MVP First**: Complete US1 (Web Form) first to establish the baseline production flow.
- **Incremental Delivery**: Add US2 (WhatsApp) and then US3 (Unified History/Email) sequentially.

---

## Parallel Opportunities

- T006, T008, T011 can run in parallel during Foundation.
- Once Foundation is complete, T014 (US1), T019 (US2), and T023 (US3) can start in parallel.
- All test tasks marked [P] can run in parallel with their respective implementations.
