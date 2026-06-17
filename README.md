<<<<<<< HEAD
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
=======
# 🏭 CRM Digital FTE Factory
 
> Build Your First 24/7 AI Employee — From Incubation to Production
 
A production-grade **Digital FTE (Full-Time Equivalent)** — an autonomous AI Customer Success agent that handles support inquiries across **Email (Gmail), WhatsApp, and a Web Form**, tracks every interaction in a self-built PostgreSQL CRM, and runs 24/7 on Kubernetes at a fraction of the cost of a human employee.
 
This project is my submission for **Hackathon 5: The CRM Digital FTE Factory** under the [Agent Factory](https://agentfactory.panaversity.org) curriculum (Panaversity / PIAIC / GIAIC — Certified Agentic AI & Robotics Engineer program).
 
---
 
## 📌 The Problem
 
A growing SaaS company is drowning in customer support inquiries coming in from multiple channels. A human Customer Success FTE costs **~$75,000/year** plus benefits, training, and management overhead.
 
**Goal:** Build a Digital FTE that operates at **under $1,000/year**, available 24/7, with no sick days, no breaks, and no burnout — while matching (or beating) human-level response quality.
 
---
 
## ✨ Features
 
- **Multi-channel intake** — accepts support tickets from Gmail, WhatsApp (via Twilio), and an embeddable Web Support Form
- **Unified Customer CRM** — a custom-built PostgreSQL system (no Salesforce/HubSpot needed) tracking customers, conversations, tickets, and messages across all channels
- **Cross-channel identity resolution** — recognizes the same customer even if they switch from email to WhatsApp mid-conversation
- **Channel-aware responses** — formal/detailed for email, short/conversational for WhatsApp, semi-formal for web
- **Smart escalation** — automatically hands off pricing, legal, refund, or high-frustration conversations to a human
- **Sentiment tracking** — every interaction is scored for customer sentiment and logged for reporting
- **Semantic knowledge search** — pgvector-powered retrieval over product documentation
- **Event-driven architecture** — Kafka streams tickets/messages between intake and processing layers
- **Auto-scaling deployment** — Kubernetes manifests with health checks and multi-pod scaling
- **Built for 24/7 resilience** — survives pod restarts with zero message loss
---
 
## 🏗️ Architecture
 
```
                    MULTI-CHANNEL INTAKE
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │  Gmail   │     │ WhatsApp │     │ Web Form │
   └────┬─────┘     └────┬─────┘     └────┬─────┘
        │                │                │
        └────────────────┼────────────────┘
                          ▼
                  ┌───────────────┐
                  │     Kafka     │  (event streaming)
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐       ┌───────────┐
                  │ Customer      │──────▶│ PostgreSQL│
                  │ Success Agent │       │ (CRM/State)│
                  │ (OpenAI SDK)  │       └───────────┘
                  └───────┬───────┘
                          ▼
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   Gmail API         Twilio API         Web/API
   (reply)            (reply)           (reply)
 
        Deployed on Kubernetes — auto-scaling worker pods
```
 
The system evolved through the **Agent Maturity Model**:
 
1. **Incubation** — explored the problem space and built a working prototype using Claude Code, exposing core capabilities through an MCP server
2. **Specialization** — transformed the prototype into a production-grade Custom Agent using the OpenAI Agents SDK, FastAPI, PostgreSQL, Kafka, and Kubernetes
3. **Integration** — validated the system with multi-channel end-to-end tests, load tests, and a 24-hour continuous operation test
---
 
## 🛠️ Tech Stack
 
| Layer | Technology |
|---|---|
| Agent Framework | OpenAI Agents SDK |
| API Layer | FastAPI |
| Database / CRM | PostgreSQL 16 + pgvector |
| Event Streaming | Apache Kafka |
| Orchestration | Kubernetes |
| Email Channel | Gmail API + Pub/Sub |
| WhatsApp Channel | Twilio WhatsApp API |
| Web Form | Next.js / React |
| Prototyping Tool | Claude Code (MCP Server) |
| Load Testing | Locust |
 
---
 
## 📂 Project Structure
 
```
crm-digital-fte-factory/
├── context/
│   ├── company-profile.md
│   ├── product-docs.md
│   ├── sample-tickets.json
│   ├── escalation-rules.md
│   └── brand-voice.md
├── specs/
│   ├── discovery-log.md
│   └── customer-success-fte-spec.md
├── production/
│   ├── agent/              # OpenAI Agents SDK implementation + prompts
│   ├── api/                # FastAPI channel endpoints
│   ├── channels/           # Gmail, WhatsApp, Web Form handlers
│   ├── db/                 # PostgreSQL schema & migrations
│   ├── kafka/               # Producers/consumers, topic configs
│   └── k8s/                # Kubernetes manifests
├── web-form/                # Next.js Web Support Form (standalone component)
├── tests/
│   ├── test_transition.py
│   ├── e2e/
│   └── load/
└── README.md
```
 
---
 
## 🗄️ CRM Database Schema (Overview)
 
The PostgreSQL database **is** the CRM — no external tool required.
 
| Table | Purpose |
|---|---|
| `customers` | Unified customer record across all channels |
| `customer_identifiers` | Maps email/phone/WhatsApp IDs to a single customer |
| `conversations` | Conversation threads with sentiment & resolution status |
| `messages` | Every inbound/outbound message, tagged by channel |
| `tickets` | Support ticket lifecycle (open → resolved/escalated) |
| `knowledge_base` | Product docs with vector embeddings for semantic search |
| `channel_configs` | Per-channel settings (API keys, response limits) |
| `agent_metrics` | Performance metrics for monitoring/reporting |
 
---
 
## 🚀 Getting Started
 
### Prerequisites
 
- Python 3.11+
- Node.js 18+ (for the Web Form)
- Docker & Docker Desktop
- PostgreSQL 16 with `pgvector` extension
- A Kafka cluster (Confluent Cloud recommended for local dev)
- Gmail API credentials (sandbox)
- Twilio WhatsApp Sandbox account
- minikube or a Kubernetes cluster (for deployment)
### Installation
 
```bash
# Clone the repository
git clone https://github.com/<your-username>/crm-digital-fte-factory.git
cd crm-digital-fte-factory
 
# Install backend dependencies
cd production
pip install -r requirements.txt
 
# Install web form dependencies
cd ../web-form
npm install
```
 
### Environment Variables
 
Create a `.env` file in `production/` with:
 
```
DATABASE_URL=postgresql://user:password@localhost:5432/crm_fte
OPENAI_API_KEY=your_openai_key
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
KAFKA_BOOTSTRAP_SERVERS=your_kafka_broker
```
 
### Run Locally
 
```bash
# Apply the database schema
psql -U user -d crm_fte -f production/db/schema.sql
 
# Start the FastAPI service
uvicorn production.api.main:app --reload
 
# Start the Web Support Form
cd web-form
npm run dev
```
 
### Deploy to Kubernetes
 
```bash
kubectl apply -f production/k8s/
```
 
---
 
## 🧪 Testing
 
```bash
# Run transition / unit tests
pytest production/tests/
 
# Run end-to-end multi-channel tests
pytest tests/e2e/
 
# Run load tests
locust -f tests/load/locustfile.py
```
 
**24-Hour Test Targets:**
- Uptime > 99.9%
- P95 latency < 3 seconds across all channels
- Escalation rate < 25%
- Cross-channel customer identification > 95%
- Zero message loss
---
 
## ✅ Deliverables Status
 
- [ ] Working prototype (Incubation)
- [ ] MCP server with 5+ tools
- [ ] PostgreSQL multi-channel schema
- [ ] OpenAI Agents SDK production implementation
- [ ] Gmail integration
- [ ] WhatsApp/Twilio integration
- [ ] Web Support Form
- [ ] Kafka event streaming
- [ ] Kubernetes deployment manifests
- [ ] Multi-channel E2E test suite
- [ ] 24-hour load test passed
---
 
## 📖 Acknowledgments
 
Built as part of the **CAARE (Certified Agentic AI & Robotics Engineer)** program by [Panaversity](https://panaversity.org) / PIAIC / GIAIC, following the [Agent Maturity Model](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/agent-factory-paradigm/the-2025-inflection-point#the-agent-maturity-model) and Agent Factory paradigm.
 
## 📄 License
 
This project is for educational purposes as part of a certification hackathon.
>>>>>>> b5143947e38da801e75b5f13d7f78caf31270fff
