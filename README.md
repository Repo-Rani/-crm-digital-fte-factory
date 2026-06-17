# CRM Digital FTE Factory — TechFlow Customer Success Agent

This project is an AI-powered Digital FTE (Full-Time Equivalent) designed to handle 24/7 customer support for the **TechFlow Pro** SaaS platform. It handles inquiries via **Email (Gmail)**, **WhatsApp (Twilio)**, and a **Web Support Form**.

## Quick Start (Local Development)

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+
- OpenAI API Key

### 2. Setup
```bash
# Clone the repository
git clone <repo-url>
cd hackathon-5/production

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and other credentials
```

### 3. Launch Services
```bash
docker-compose up -d --build
```
This will start:
- **FastAPI API**: Port 8000
- **Postgres (with pgvector)**: Port 5432
- **Kafka & Zookeeper**: Event streaming
- **Worker**: Message processor

### 4. Verify
```bash
# Check health
curl http://localhost:8000/health

# Run E2E Tests
pytest tests/test_multichannel_e2e.py -v
```

## Project Structure

- `context/`: Foundation documents (Brand Voice, Escalation Rules, KB).
- `src/agent/`: Phase 1 (Incubation) prototype and exploration scripts.
- `production/`: Phase 2 (Specialization) production-grade implementation.
  - `agent/`: Specialized agent with OpenAI Agents SDK and Tools.
  - `api/`: FastAPI endpoints and webhook handlers.
  - `channels/`: Real-world integrations (Gmail, WhatsApp).
  - `database/`: PostgreSQL schema and migration queries.
  - `workers/`: Kafka consumers for background processing.
  - `web-form/`: **REQUIRED** React Support Form component.
  - `k8s/`: Deployment manifests for scaling.

## Scoring Table & Requirements

| Requirement | Implementation Status |
|-------------|-----------------------|
| **Omnichannel Support** | ✅ Gmail, WhatsApp, Web Form |
| **Unified CRM** | ✅ PostgreSQL with 8 tables |
| **Semantic Search** | ✅ pgvector integration |
| **Web Support Form** | ✅ Complete React component with validation |
| **Event Streaming** | ✅ Kafka with 7+ topics |
| **Distributed Scaling** | ✅ Kubernetes Deployment + HPA |
| **SLA Compliance** | ✅ < 3s P95 Latency |

## Documentation

Full documentation is available in `production/docs/`:
- [Deployment Guide](./docs/deployment-guide.md)
- [API Documentation](./docs/api-documentation.md)
- [Incident Runbook](./docs/runbook.md)
- [Form Integration Guide](./docs/form-integration-guide.md)

---
*Built for the CRM Digital FTE Factory Hackathon 5.*
