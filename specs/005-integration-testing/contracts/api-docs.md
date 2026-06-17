# API Documentation: Integration & Testing

## Monitoring Endpoints (External for Testing)

### GET /health
- **Description**: System health and channel status.
- **Success Response**: `200 OK`
  ```json
  {
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "3.0.0",
    "channels": {"email": "active", "whatsapp": "active", "web_form": "active"}
  }
  ```

### GET /metrics/channels
- **Description**: Real-time interaction metrics per channel.
- **Success Response**: `200 OK`
  ```json
  {
    "web_form": { "total_conversations": 60, "resolved": 43 },
    "email": { "total_conversations": 45, "resolved": 30 }
  }
  ```

## Internal Validation Logic (Contractual)

- **Simulation Input**: `/support/submit` (JSON)
  - Fields: name, email, subject, category, message, priority.
- **Status Retrieval**: `/support/ticket/{id}` (GET)
  - Returns current workflow status.
- **Customer Lookup**: `/customers/lookup?email={email}` (GET)
  - Returns customer record and linked conversation ID.
