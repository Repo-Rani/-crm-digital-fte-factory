<!--
Sync Impact Report:
Version Change: 2.0.0 -> 3.0.0
Modified Principles:
  - VI. Phase 2: Production-Grade Specialization -> VI. Phase 3: Integration & Testing Focus
Added Principles:
  - X. Real-World Validation (New)
  - XI. Chaos & Resilience (New)
  - XII. Observability & Real Metrics (New)
Added Sections:
  - Phase 3: Integration & Testing Principles
  - Phase 3 Completion Criteria (24-Hour Test)
Removed Sections:
  - Phase 2 Completion Criteria
Templates Requiring Updates:
  - .specify/templates/plan-template.md (✅ checked/aligned)
  - .specify/templates/spec-template.md (✅ checked/aligned)
  - .specify/templates/tasks-template.md (✅ checked/aligned)
  - .gemini/commands/sp.constitution.toml (✅ updated)
Follow-up TODOs: None
-->
# Customer Success AI Agent - Phase 3: Integration & Testing Constitution

## Core Principles

### I. Channel Agnostic Support
The agent MUST provide 24/7 customer support across three primary channels: Gmail (Email), WhatsApp, and Web Form. Production implementation MUST use real APIs (Gmail API, Twilio).

### II. Knowledge-Driven Responses
All product questions MUST be answered using an authoritative knowledge base stored in PostgreSQL with `pgvector` for semantic search.

### III. Comprehensive Interaction Tracking
All customer interactions MUST be tracked in the PostgreSQL CRM (8 tables) and include relevant channel metadata.

### IV. Intelligent Escalation
Complex issues MUST be automatically escalated to human agents based on predefined rules. Escalations MUST be published as events to Kafka.

### V. Persistent Conversation Memory
The agent MUST maintain and remember conversation history across channels using the PostgreSQL CRM as the source of truth.

### VI. Phase 3: Integration & Testing Focus
The primary objective for Phase 3 is to PROVE the system works as a whole. You are now a QA + DevOps Engineer. Focus is on validation, resilience, and operational readiness, NOT new features.

## Production Readiness Principles

### VII. Distributed Architecture
The system MUST use a distributed architecture: FastAPI for the API layer and Kafka-based workers for message processing to ensure scalability and reliability.

### VIII. Strict Data Persistence
PostgreSQL IS the CRM. No external CRMs (Salesforce/HubSpot) are allowed. The schema MUST be strictly followed and include all 8 defined tables.

### IX. Production Safety & Secrets
NEVER hardcode secrets. All credentials (OpenAI, Twilio, Gmail, Postgres) MUST be managed via environment variables and `.env` files.

## Phase 3: Integration & Testing Principles

### X. Real-World Validation
Every test MUST run against the real running system (PostgreSQL, Kafka, FastAPI, Workers). No mocks or stubs allowed unless explicitly stated.

### XI. Chaos & Resilience
Chaos testing is MANDATORY. The system MUST survive pod kills (every 2 hours during long tests) with zero message loss and recovery within 120 seconds.

### XII. Observability & Real Metrics
Metrics MUST be real, derived from actual DB/Kafka data.
- **Uptime**: > 99.9%
- **P95 Latency**: < 3000ms
- **Escalation Rate**: < 25%

## Phase 3 Completion Criteria (24-Hour Test)

Phase 3 is considered complete ONLY when all of the following checks pass:
- **Phase 1 & 2** are 100% complete and verified.
- **E2E Suite**: `pytest production/tests/test_multichannel_e2e.py` passes with all 5 test classes.
- **Load Test**: Locust test shows < 3s P95 latency under 100+ concurrent requests with < 1% failure rate.
- **Chaos Test**: At least 3 cycles of pod killing pass with zero message loss.
- **24-Hour Test**: System handles 200+ real messages over 24 hours with > 99.9% uptime.
- **Documentation**: Runbook, Deployment Guide, API Docs, and Form Integration Guide are complete.
- **Metrics**: `monitoring/metrics_dashboard.py` is functional and shows real-time SLA compliance.

## Governance

This constitution governs the principles and guidelines for the CRM Digital FTE Factory - Hackathon 5, specifically for Phase 3: Integration & Testing.
Amendments require a documented proposal and lead approval. All changes MUST be reflected in `LAST_AMENDED_DATE` and `CONSTITUTION_VERSION`.

**Version**: 3.0.0 | **Ratified**: 2026-04-19 | **Last Amended**: 2026-05-03
