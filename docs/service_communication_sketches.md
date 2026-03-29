# EasyParkPlus: Service-to-Service Communication Sketches

This document defines the inter-service communication contracts, message formats, and resilience protocols for the EasyParkPlus distributed system.

---

## 1. Synchronous REST Endpoints (Real-Time Queries)

| Service | Endpoint | Method | Purpose | Timeout | Retry |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Facility** | `/v1/internal/facilities/{id}/availability` | `GET` | Instant capacity check. | 500ms | 3x Exponential |
| **Billing** | `/v1/internal/prices/calculate` | `POST` | Real-time quote for charging session. | 1s | 1x Fallback |
| **EV** | `/v1/internal/stations/{id}/authorize` | `POST` | Pre-authorize a hardware unit. | 2s | No Retry |

### Resilience Policy: Circuit Breaker
- **Error Threshold:** >50% failure rate over a 10s sliding window.
- **Sleep Window:** 30s before attempting a Half-Open state.
- **Default Fallback:** Return cached/stale data or a predefined "Safe Mode" response.

---

## 2. Asynchronous Event Workflows (Eventual Consistency)

| Topic | Event | Trigger | Consumer | Format |
| :--- | :--- | :--- | :--- | :--- |
| `billing.events` | `PaymentCompleted` | Successful final transaction. | Parking Allocation | JSON/Avro |
| `parking.events` | `SpotReleased` | Vehicle physically exits slot. | Facility Manager | JSON/Avro |
| `ev.events` | `ChargingFaulted` | Hardware fault detected. | Notification | JSON/Avro |

### Sample Schema: `PaymentCompleted`
```json
{
  "event_id": "uuid-1234",
  "allocation_id": "8a990369-1234",
  "transaction_id": "tx-99",
  "amount_paid": "12.50",
  "currency": "USD",
  "timestamp": "2026-03-29T21:26:00Z",
  "correlation_id": "corr-5566"
}
```

---

## 3. Resilience & Messaging Protocols

### Message Reliability (The Outbox Pattern)
Every service must implement the **Transactional Outbox Pattern** to ensure that domain events are not lost if the message broker is unavailable. Events are first committed to the local database before being asynchronously published.

### Error Taxonomy
- `DOMAIN_ERROR`: Inconsistent state (e.g., `ERROR_NO_CAPACITY`). Non-retryable.
- `INFRASTRUCTURE_ERROR`: Network/DB timeout. Candidates for **Circuit Breaker** and **Retries**.
- `CLIENT_ERROR`: Invalid request payload. Non-retryable.

### Event Ordering
- Use **Partition Keys** (e.g., `allocation_id`) to ensure that all events for a single parking session are processed in strict chronological order by the consumers.
