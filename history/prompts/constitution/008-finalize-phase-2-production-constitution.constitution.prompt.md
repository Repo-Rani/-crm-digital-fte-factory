---
id: 008
title: "Finalize Phase 2 Production Constitution"
stage: constitution
date: 2026-04-27
surface: "agent"
model: "gemini-2.0-flash"
feature: "none"
branch: "003-customer-success-ai"
user: "HP"
command: "/sp.constitution"
labels: ["constitution", "phase-2", "governance", "production-ready"]
links:
  spec: "specs/customer-success-fte-spec.md"
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: sp.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
/sp.constitution # CLAUDE.md — Phase 2: Specialization Constitution
# CRM Digital FTE Factory — Hackathon 5
# Customer Success AI Agent — Production System

---

## CRITICAL RULES (Read Before Starting Anything)

1. **Phase 1 must already be complete.** All context files, prototype_agent.py, memory.py, skills.py, and MCP server must exist and pass their tests.
2. **You are NOW an engineer, not an explorer.** Write production-grade code: async/await everywhere, proper error handling, connection pools, structured logging, retry logic.
3. **Claude Code stays your tool.** You use Claude Code (Claude CLI) to BUILD everything below. You are the director giving precise instructions.
4. **Web Support Form is REQUIRED** — 10 marks depend on it. Build it completely. Do not skip or stub it.
5. **PostgreSQL IS the CRM** — No Salesforce, no HubSpot. Build your own.
6. **Twilio Sandbox is enough** — You do NOT need a production WhatsApp Business account.
7. **Never hardcode secrets** — Always use environment variables and `.env` files.

**Total time budget: Hours 17–40 (23 hours)**

---

## PHASE 2 FOLDER STRUCTURE

Create this production folder alongside (not replacing) the Phase 1 folder:

```
crm-fte-hackathon/
├── [Phase 1 folders remain as-is]
│
└── production/
    ├── agent/
    │   ├── __init__.py
    │   ├── customer_success_agent.py   ← OpenAI Agents SDK agent
    │   ├── tools.py                    ← @function_tool definitions
    │   ├── prompts.py                  ← System prompt (extracted from Phase 1)
    │   └── formatters.py              ← Channel-specific formatting
    │
    ├── channels/
    │   ├── __init__.py
    │   ├── gmail_handler.py            ← Real Gmail API integration
    │   ├── whatsapp_handler.py         ← Real Twilio WhatsApp integration
    │   └── web_form_handler.py         ← FastAPI router + Pydantic models
    │
    ├── workers/
    │   ├── __init__.py
    │   ├── message_processor.py        ← Kafka consumer → agent → DB → reply
    │   └── metrics_collector.py        ← Background metrics aggregation
    │
    ├── api/
    │   ├── __init__.py
    │   └── main.py                    ← FastAPI application (all endpoints)
    │
    ├── database/
    │   ├── schema.sql                  ← PostgreSQL schema (8 tables)
    │   ├── queries.py                  ← All DB access functions
    │   └── migrations/
    │       └── 001_initial.sql
    │
    ├── kafka_client.py                 ← Kafka producer + consumer classes
    │
    ├── web-form/
    │   ├── SupportForm.jsx            ← REQUIRED: Complete React component
    │   ├── package.json
    │   └── README.md
    │
    ├── tests/
    │   ├── test_transition.py          ← Verify prototype → production parity
    │   ├── test_multichannel_e2e.py    ← End-to-end tests all channels
    │   └── load_test.py               ← Locust load test
    │
    ├── k8s/
    │   ├── namespace.yaml
    │   ├── configmap.yaml
    │   ├── secrets.yaml
    │   ├── postgres-deployment.yaml
    │   ├── api-deployment.yaml
    │   ├── worker-deployment.yaml
    │   ├── services.yaml
    │   ├── hpa.yaml
    │   └── pdb.yaml
    │
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env.example
    ├── requirements.txt
    └── kafka_client.py
```

[...rest of the multi-line Phase 2 instruction...]
```

## Response snapshot

I updated the project constitution from version 1.0.0 to 2.0.0, formally transitioning the project to Phase 2 (Production Specialization). This update mandates production-grade engineering standards, a distributed architecture using FastAPI and Kafka, and strict data persistence in PostgreSQL.

## Outcome

- ✅ Impact: Project governance is now aligned with production-grade engineering requirements for Phase 2.
- 🧪 Tests: none
- 📁 Files: `.specify/memory/constitution.md` updated.
- 🔁 Next prompts: "/sp.specify Implement the feature specification based on the updated constitution."
- 🧠 Reflection: The transition from a "discovery" mindset to an "engineering" mindset was successfully codified in the constitution.

## Evaluation notes (flywheel)

- Failure modes observed: Manual sync impact report generation is turn-intensive but necessary for traceability.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Automate the Sync Impact Report generation using a dedicated script.
