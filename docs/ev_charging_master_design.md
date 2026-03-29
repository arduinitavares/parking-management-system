# EasyParkPlus: EV Charging Master Design Document

This document defines the comprehensive architectural and functional design for the Electric Vehicle (EV) Charging Management system within the EasyParkPlus distributed network.

---

## 1. Functional Requirements
- **Start/Stop Charging:** Authorized workflows for initiating and terminating energy transfer events.
- **Real-Time Monitoring:** Continuous tracking of State of Charge (SoC) and active power draw.
- **Hardware Fault Detection:** Automated detection of offline states, grid loss, or connector-related errors.
- **Energy Metrology:** Accurate calculation of energy delivered (kWh) for billing purposes.

---

## 2. Domain-Specific Business Rules
- **Dynamic Pricing:** Energy rates vary based on time-of-day (Peak vs. Off-peak) and facility-level occupancy.
- **Reservation Policies:** EV-capable slots can be held for up to 15 minutes post-arrival.
- **Peak Hour Management:** Capacity limiting and load-shedding protocols to protect the local power grid.
- **Idle Fee Logic:** Automatic imposition of overstay fees once charging is complete, incentivizing slot turnover.

---

## 3. Integration Architecture
The EV Charging service operates as a **Supporting Subdomain**, integrating with the **Parking Allocation** (Core) and **Facility Management** (Supporting) services via asynchronous events.

| Trigger Event | Source | Resulting Action |
| :--- | :--- | :--- |
| `VehicleParked` | Parking Core | Initializes the assigned Charging Station (Station-to-Slot mapping). |
| `VehicleExited` | Parking Core | Force-terminates any active session and releases the hardware. |
| `ChargingFaulted` | EV Service | Notifies the Core to potentially re-allocate the vehicle to a functional bay. |

---

## 4. API & Database Concept

### RESTful API Specification
- **Client Endpoints:** `POST /session/start`, `POST /session/stop`, `GET /session/monitor`.
- **Internal Endpoints:** `POST /internal/authorize` (for Parking Core), `GET /internal/metrics` (for Facility Management).

### Persistence Layer Schema
- **Metadata Tables:** `charging_stations` (Registry), `charging_sessions` (Transactions).
- **Time-Series Table:** `session_metrics` (High-frequency SoC and Power Draw telemetry).

---

## 5. Scalability & Multi-Facility Considerations
- **Facility-Scoped Operations:** All API paths and database records are explicitly bound to a `facility_id`.
- **Decentralized Control:** Each facility can operate its charging logic independently if the central system is temporarily unreachable, ensuring high availability (Offline Mode).
