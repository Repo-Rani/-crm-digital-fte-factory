# API Documentation: TechFlow Customer Success Agent

This document details the available endpoints for the TechFlow Digital FTE API. All request and response bodies use JSON format unless otherwise specified.

## Core Endpoints

### 1. Health Check
`GET /health`
Returns the current health status of the system, including component connectivity.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-05-04T12:00:00Z",
  "version": "1.0.0",
  "components": {
    "database": "connected",
    "kafka": "connected"
  }
}
```

### 2. Support Form Submission
`POST /support/submit`
Submits a new support request from the web form.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Login Issue",
  "category": "technical",
  "message": "I cannot log in to my account since this morning.",
  "priority": "high"
}
```

**Response**:
```json
{
  "ticket_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Thank you! Our AI assistant will respond to your email shortly.",
  "estimated_response_time": "~1 hour"
}
```

### 3. Ticket Status
`GET /support/ticket/{ticket_id}`
Retrieves the current status and message history for a specific ticket.

**Response**:
```json
{
  "ticket_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "open",
  "category": "technical",
  "messages": [...],
  "created_at": "2024-05-04T12:00:00Z",
  "last_updated": "2024-05-04T12:05:00Z"
}
```

## Channel Webhooks

### 4. Gmail Webhook
`POST /webhooks/gmail`
Handles Pub/Sub notifications from the Gmail API.

### 5. WhatsApp Webhook
`POST /webhooks/whatsapp`
Handles incoming messages from Twilio. Expects `application/x-www-form-urlencoded` data.

**Response**: TwiML XML to acknowledge or reply.

## Metrics & Observability

### 6. Channel Metrics
`GET /metrics/channels`
Returns interaction statistics per channel for the last 24 hours.

**Response**:
```json
{
  "email": { "total": 150, "resolved": 120, "escalated": 30 },
  "whatsapp": { "total": 80, "resolved": 70, "escalated": 10 },
  "web_form": { "total": 200, "resolved": 180, "escalated": 20 }
}
```

## Error Codes
- `400 Bad Request`: Validation failure.
- `401 Unauthorized`: Missing or invalid credentials.
- `404 Not Found`: Resource not found.
- `429 Too Many Requests`: Rate limit exceeded.
- `500 Internal Server Error`: Server-side processing error.
