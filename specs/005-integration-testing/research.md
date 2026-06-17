# Research: Phase 3 Integration & Testing

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pytest, pytest-asyncio, httpx, locust, subprocess (for kubectl), asyncpg
**Storage**: PostgreSQL (for metrics extraction), Kafka (for event validation)
**Testing**: Comprehensive E2E, Load, and Chaos testing
**Target Platform**: Docker Compose / Kubernetes (Linux)
**Performance Goals**: < 3000ms P95 latency under 50 concurrent users
**Constraints**: Zero message loss during chaos, > 99.9% uptime over 24h
**Scale/Scope**: 200+ real messages over 24-hour simulation

## Decisions & Rationale

### 1. E2E Testing Strategy
- **Decision**: Use `httpx.AsyncClient` with `pytest-asyncio`.
- **Rationale**: High-performance asynchronous testing matches the FastAPI/Kafka architecture. Allows for real HTTP interactions without blocking.
- **Alternatives**: `requests` (synchronous, slower), `testclient` (FastAPI internal, less "real-world").

### 2. Resilience Validation (Chaos)
- **Decision**: Scripted `kubectl delete pod` triggered by Python `subprocess`.
- **Rationale**: Simplest way to automate "pod killing" without introducing heavy service meshes or chaos monkeys like Chaos Mesh for this specific hackathon scope. Confirms K8s/Docker auto-restart behavior.
- **Alternatives**: Manual pod killing (not repeatable), dedicated chaos engineering platforms (too complex for current phase).

### 3. Observability & SLIs
- **Decision**: Console-based dashboard querying PostgreSQL `conversations` and `agent_metrics` tables every 60s.
- **Rationale**: Uses the existing authoritative source of truth. Provides real-time feedback on escalation rates and latency without needing Grafana/Prometheus setup.
- **Alternatives**: Prometheus/Grafana (high overhead for a 24h test), Log aggregation (harder to extract quantitative SLIs).

### 4. Load Testing
- **Decision**: Locust `HttpUser` with weighted tasks.
- **Rationale**: Standard Python-based load testing tool. Weighted tasks allow simulating a realistic user mix (80% form submissions, 10% health checks, 10% lookups).
- **Alternatives**: Apache JMeter (not Pythonic), `ab` (too simple, no user behavior modeling).

## Constitution Check

| Gate | Status | Justification |
|------|--------|---------------|
| Real-World Validation | ✅ Pass | All tests (E2E, Load, Chaos) targeted at live endpoints. |
| Chaos & Resilience | ✅ Pass | Mandatory pod-kill cycles included in plan. |
| Observability | ✅ Pass | Real-time dashboard using DB metrics is primary monitor. |
| Production Safety | ✅ Pass | All credentials handled via `.env.test` file. |
