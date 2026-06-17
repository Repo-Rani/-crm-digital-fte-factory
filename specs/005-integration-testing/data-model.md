# Data Model: Phase 3 Integration & Testing

## Entities

### Test Result (JSON)
Stored in `simulation_results.json` and `chaos_results.json`.

| Field | Type | Description |
|-------|------|-------------|
| start_time | ISO8601 | Test start timestamp |
| end_time | ISO8601 | Test completion timestamp |
| total_sent | int | Total messages/actions attempted |
| total_success | int | Total successful completions |
| uptime_percent | float | (success / sent) * 100 |
| p95_latency_ms | float | 95th percentile response time |
| by_channel | dict | counts per channel (email, whatsapp, web_form) |
| errors | list[dict] | Details of failures (channel, error, time) |
| cycles | int | Number of chaos cycles performed |

### SLI Metric (extracted from DB)
Aggregated data points for the metrics dashboard.

| Metric | Source | Rule/Validation |
|--------|--------|-----------------|
| Escalation Rate | `conversations` table | `count(escalated) / total` |
| Avg Sentiment | `conversations` table | Mean of `sentiment_score` |
| P95 Latency | `agent_metrics` table | 95th percentile of `metric_value` |
| DLQ Events | `agent_metrics` table | Count of `dlq_event` recorded |

## Validation Rules

- **Uptime**: Must be >= 99.9% for 24-hour test.
- **Latency**: P95 must be < 3000ms under load.
- **Message Integrity**: `count(sent)` must equal `count(db_records)` + `count(errors)`.
- **Chaos Recovery**: System must return HTTP 200 on `/health` within 120s of pod termination.
