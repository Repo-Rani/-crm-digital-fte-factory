---
id: 007
title: "Update constitution for Phase 2 Production"
stage: constitution
date: 2026-04-27
surface: "agent"
model: "gemini-2.0-flash"
feature: "none"
branch: "003-customer-success-ai"
user: "HP"
command: "/sp.constitution"
labels: ["constitution", "phase-2", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

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

... [rest of the Phase 2 prompt]

## Response snapshot

Updated the project constitution from version 1.0.0 to 2.0.0 to reflect the transition from incubation to production specialization. Mandated production-grade standards (async/await, structured logging), distributed architecture (FastAPI + Kafka), and strict CRM persistence in PostgreSQL. Added Phase 2 completion criteria and verified template alignment.

## Outcome

- ✅ Impact: Project governance now mandates production-grade standards for Phase 2.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md modified.
- 🔁 Next prompts: "/sp.specify Begin Phase 2 implementation"
- 🧠 Reflection: Moving from "explorer" to "engineer" requires a fundamental shift in principles towards stability, scalability, and security.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
