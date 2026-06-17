---
id: 009
title: Update Constitution to Phase 3 Integration and Testing
stage: constitution
date: 2026-05-03
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: HP
command: /sp.constitution
labels: ["constitution", "phase-3", "integration-testing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .gemini/commands/sp.constitution.toml
tests:
  - none
---

## Prompt

/sp.constitution analyze my this project propelry read all folder and files with accuracy after that good understanding and good knowledge of this project do this # CLAUDE.md — Phase 3: Integration & Testing Constitution
# CRM Digital FTE Factory — Hackathon 5
# Customer Success AI Agent — Production Validation & 24-Hour Operation

---

## CRITICAL RULES (Read Before Starting Anything)

1. **Phase 1 AND Phase 2 must be 100% complete.** All services must be running: PostgreSQL, Kafka, FastAPI, Worker pods.
2. **Phase 3 is about PROVING the system works** — not building new features. You are now a QA Engineer + DevOps Engineer.
3. **Every test must run against the real running system** — no mocks, no stubs, no `unittest.mock` unless explicitly stated.
4. **The 24-hour test is the final boss.** Your system must handle 200+ real messages across 3 channels without crashing.
5. **Chaos testing is mandatory.** Kill pods every 2 hours during the 24-hour test and verify zero message loss.
6. **Documentation is scored (5 marks).** Runbook, deployment guide, and API docs must be complete.
7. **Metrics must be real.** Screenshot your uptime, P95 latency, escalation rate from actual Kafka/DB data.

**Total time budget: Hours 41–48 (7–8 hours)**

---

[... truncated in PHR for brevity but preserved full user input in actual file ...]

## Response snapshot

I have updated the project constitution to version 3.0.0, incorporating the Phase 3: Integration & Testing principles. This includes new mandatory rules for real-world validation, chaos testing, and observability. I also synchronized the `sp.constitution.toml` command file to remove agent-specific references and verified that all SDD templates align with the new principles.

## Outcome

- ✅ Impact: Project governance updated to reflect the final integration and testing phase, establishing clear completion criteria and operational standards.
- 🧪 Tests: No code tests run; constitution validation performed.
- 📁 Files: Updated `.specify/memory/constitution.md` and `.gemini/commands/sp.constitution.toml`.
- 🔁 Next prompts: Proceed with building specifications or implementation plans for Phase 3 components.
- 🧠 Reflection: The update was straightforward due to the detailed Phase 3 requirements provided. Ensuring template synchronization was a key step in maintaining SDD integrity.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A.
- Prompt variant (if applicable): null.
- Next experiment (smallest change to try): null.
