# EasyParkPlus: External-Facing API Sketches

This document sketches the external RESTful API endpoints for the EasyParkPlus distributed system. These definitions serve as the service-level contracts for client-side integration (Mobile, Kiosk) and hardware controller communication.

---

## 1. Security & Identification Scoping

- **Authentication:** OAuth 2.0 / OpenID Connect with **JWT**.
- **Authorization:** Role-Based Access Control (RBAC) via JWT `scopes`.
- **Facility Scoping:** All operations are scoped per-facility using path parameters to support multi-facility operations.

| Base URL Pattern | Scope |
| :--- | :--- |
| `/v1/facilities/{facility_id}/...` | Explicit resource scoping for every physical location. |

---

## 2. Parking Operations API

| Endpoint | Method | Path | Description |
| :--- | :--- | :--- | :--- |
| **New Reservation** | `POST` | `/v1/facilities/{fid}/reservations` | Pre-books a slot for a specific vehicle type. |
| **Check-In (Enter)** | `POST` | `/v1/facilities/{fid}/allocations/enter` | Authorizes entry and assigns a physical slot. |
| **Check-Out (Exit)**| `POST` | `/v1/facilities/{fid}/allocations/{aid}/exit`| Triggers the exit transition and fee calculation. |
| **Process Payment** | `POST` | `/v1/facilities/{fid}/allocations/{aid}/pay` | Handles the final transaction for the visit. |

### Sample Payload: Check-In (Enter)
```json
// POST /v1/facilities/lot-abc-123/allocations/enter
{
  "registration_number": "XYZ-9876",
  "vehicle_type": "electric",
  "entry_timestamp": "2026-03-29T20:56:00Z"
}

// Response: 201 Created
{
  "allocation_id": "8a990369-1234-abcd",
  "slot_id": "slot-ev-101",
  "assigned_zone": "EV-Level-1"
}
```

---

## 3. EV Charging Operations API

| Endpoint | Method | Path | Description |
| :--- | :--- | :--- | :--- |
| **Start Session** | `POST` | `/v1/facilities/{fid}/stations/{sid}/session/start` | Initiates the power flow (requires valid occupancy). |
| **Stop Session**  | `POST` | `/v1/facilities/{fid}/stations/{sid}/session/stop`  | Terminates the session and returns final metrics. |
| **Monitor Metrics**| `GET` | `/v1/facilities/{fid}/stations/{sid}/session/monitor`| Returns real-time SoC and power draw. |
| **Calculate Cost** | `GET` | `/v1/facilities/{fid}/stations/{sid}/cost` | Current or final cost based on energy/time. |

### Sample Payload: Monitor Session
```json
// GET /v1/facilities/lot-abc-123/stations/stat-77/session/monitor
{
  "session_id": "session-4455",
  "current_soc_percent": 68.5,
  "energy_delivered_kwh": 22.4,
  "current_power_kw": 11.2,
  "estimated_time_to_target": "00:45:00"
}
```

---

## 4. Error Code Schema

| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `ERROR_NO_CAPACITY` | `409 Conflict` | No available slots for the requested vehicle type. |
| `ERROR_STATION_FAULT` | `503 Service Unavailable` | Hardware station is currently offline or faulted. |
| `ERROR_UNAUTHORIZED` | `401 Unauthorized` | Invalid or expired JWT token. |
| `ERROR_FORBIDDEN` | `403 Forbidden` | Insufficient scopes for the requested operation. |
| `ERROR_ENTITY_NOT_FOUND` | `404 Not Found` | The specified Facility, Station, or Allocation ID is invalid. |
