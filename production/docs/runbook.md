# Incident Response Runbook

This runbook defines the procedures for responding to service interruptions and performance degradation for the TechFlow Digital FTE.

## Severity Levels

| Level | Description | Target Resolution |
|-------|-------------|-------------------|
| **P1** | Total system outage; all channels down. | < 2 Hours |
| **P2** | One major channel down (e.g., Gmail) or high latency (> 10s). | < 4 Hours |
| **P3** | Minor feature issues; low accuracy; isolated errors. | < 24 Hours |
| **P4** | Documentation typos; non-critical monitoring issues. | Next Release |

## Procedures

### P1: Total System Outage
1.  **Verify Outage**: Check `/health` endpoint and K8s pod status.
2.  **Notify Stakeholders**: Post update to status page and internal Slack channel.
3.  **Check Infrastructure**: 
    - Check Postgres connectivity.
    - Check Kafka connectivity.
    - Check OpenAI API status (external).
4.  **Restart Services**: Perform a rolling restart of all deployments: `kubectl rollout restart deployment/fte-api`.
5.  **Rollback**: If outage started after a deployment, rollback immediately: `kubectl rollout undo deployment/fte-api`.

### P2: Channel Specific Outage
1.  **Identify Channel**: Check per-channel logs (`docker-compose logs gmail_handler`).
2.  **Gmail Issues**:
    - Check `token.json` expiration.
    - Verify Google Cloud Pub/Sub subscription.
3.  **WhatsApp Issues**:
    - Check Twilio console for 5xx errors.
    - Verify webhook signature validation logic.
4.  **Web Form Issues**:
    - Verify Kafka `tickets_incoming` topic is receiving messages.

### P3: Performance Issues
1.  **High Latency**: 
    - Check database index health (`schema.sql`).
    - Scale workers: `kubectl scale deployment/fte-worker --replicas=10`.
2.  **Low Accuracy**: 
    - Review `production/agent/prompts.py`.
    - Update `knowledge_base` with latest documentation.

## Escalation Contacts
- **Primary On-Call**: +1 (555) 012-3456
- **Engineering Lead**: engineering-lead@techflow.io
- **Cloud Infrastructure**: devops-team@techflow.io
