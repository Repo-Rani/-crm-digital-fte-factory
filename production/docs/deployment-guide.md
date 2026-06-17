# Deployment Guide: TechFlow Digital FTE

This guide provides step-by-step instructions for deploying the TechFlow Customer Success Agent in both local and production environments.

## 1. Local Deployment (Docker Compose)
The easiest way to get started is using Docker Compose.

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### Steps
1.  **Clone the Repo**: `git clone <url> && cd hackathon-5/production`
2.  **Configure Environment**:
    ```bash
    cp .env.example .env
    # Add your OPENAI_API_KEY
    ```
3.  **Start Services**: `docker-compose up -d --build`
4.  **Initialize Database**: The database schema and initial knowledge base seeding are handled automatically on startup.
5.  **Access API**: The API is available at `http://localhost:8000`.

## 2. Channel Setup

### Gmail Integration
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project and enable the **Gmail API**.
3.  Configure the OAuth Consent Screen (Internal or External).
4.  Create **OAuth 2.0 Client IDs** (Desktop app).
5.  Download the `credentials.json` and place it in `production/`.
6.  The first time the agent runs, it will open a browser for you to authorize the application.

### WhatsApp (Twilio) Integration
1.  Sign up for a [Twilio Account](https://www.twilio.com/).
2.  Go to Messaging > Try it Out > Send a WhatsApp Message to set up the **Twilio Sandbox**.
3.  Add your `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` to your `.env` file.
4.  Configure the sandbox webhook URL to point to your public API endpoint: `https://your-domain.com/webhooks/whatsapp`.

## 3. Kubernetes Deployment (Production)
The system is K8s-ready and can be deployed using the manifests in `production/k8s/`.

### Deployment Steps
1.  **Create Namespace**: `kubectl apply -f production/k8s/namespace.yaml`
2.  **Configure Secrets**: Update `production/k8s/secrets.yaml` with your base64-encoded credentials and apply: `kubectl apply -f production/k8s/secrets.yaml`
3.  **Apply ConfigMap**: `kubectl apply -f production/k8s/configmap.yaml`
4.  **Deploy Postgres**: `kubectl apply -f production/k8s/postgres-deployment.yaml`
5.  **Deploy API & Workers**:
    ```bash
    kubectl apply -f production/k8s/api-deployment.yaml
    kubectl apply -f production/k8s/worker-deployment.yaml
    ```
6.  **Setup External Access**: `kubectl apply -f production/k8s/service.yaml` and `kubectl apply -f production/k8s/ingress.yaml`

## 4. Monitoring & Troubleshooting
- **Logs**: Use `docker-compose logs -f api` or `kubectl logs -f deployment/fte-api`.
- **Metrics**: Access the metrics dashboard via `python production/monitoring/metrics_dashboard.py`.
- **Common Issues**:
    - **Kafka Connection**: Ensure Kafka and Zookeeper are healthy before the API/Workers start.
    - **Postgres Vector**: If semantic search fails, ensure the `vector` extension is enabled in Postgres.
