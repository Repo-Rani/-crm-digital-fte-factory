---
id: 014
title: Project Analysis and Understanding
stage: general
date_iso: 2026-06-16
surface: agent
model: gemini-1.5-pro
feature: none
branch: main
user: HP
command: none
labels: ["analysis", "sdd", "onboarding"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - README.md
  - GEMINI.md
  - .specify/memory/constitution.md
tests_yaml: []
---

# PROMPT_TEXT
analyze kro mere is project or us ki directory ko properly after that good understand i will tell you what you do

# RESPONSE_TEXT
I have completed a comprehensive analysis of the **CRM Digital FTE Factory — TechFlow Customer Success Agent** project.

### Project Overview
This is a production-grade AI Digital FTE designed for the **TechFlow Pro** SaaS platform. The system is currently in **Phase 3: Integration & Testing**, shifting focus from feature development to validation, resilience, and operational readiness.

### Core Architecture & Tech Stack
*   **Omnichannel Gateway**: FastAPI handles Gmail, WhatsApp (Twilio), and React-based Web Support Form inputs.
*   **Event-Driven Processing**: Kafka (7+ topics) orchestrates message processing between the API and background workers.
*   **Unified CRM & Knowledge Base**: PostgreSQL with `pgvector` serves as the single source of truth for both customer data (8 tables) and semantic search.
*   **Infrastructure**: Containerized with Docker and orchestrated via Kubernetes (HPA, PDB, Ingress).
*   **Testing & QA**: Strict mandates for E2E testing (`pytest`), Load testing (Locust), and Chaos testing (surviving pod kills).

### Workspace & Workflow Mandates
1.  **Spec-Driven Development (SDD)**: All work follows the `Spec -> Plan -> Tasks -> Implement` lifecycle.
2.  **Authoritative Verification**: I must verify all assumptions via CLI/MCP tools (no "hallucinated" APIs).
3.  **Audit Trail**: Every interaction is recorded in a **Prompt History Record (PHR)** under `history/prompts/`.
4.  **Governance**: The `.specify/memory/constitution.md` (v3.0.0) governs all architectural and quality standards.

### Current Directory Structure Highlights
*   `production/`: The active, production-grade implementation.
*   `specs/`: Detailed requirement manifests for Phase 1, 2, and 3.
*   `context/`: Foundation documents (Brand Voice, Escalation Rules).
*   `.specify/`: Templates and scripts for the SDD workflow.
*   `history/prompts/`: A complete log of the project's evolution.

**I am ready to proceed. What is our next objective?**
