# EasyParkPlus: Ubiquitous Language Glossary (Final Draft)

This document establishes the official terminology for the EasyParkPlus Parking Management System. Definitions are intentionally written in pure domain language to facilitate stakeholder alignment and ensure that technical refactoring efforts correctly map back to business concepts.

---

## 1. Parking Allocation & Management (Core Domain)

| Term | Definition |
| :--- | :--- |
| **Allocation** | The official, real-time commitment of a physical slot to a specific vehicle for a duration of time. |
| **Capacity** | The designated numerical limit of vehicles allowed within a facility or a specific zone at one time. |
| **Check-in** | The business process initiated when a vehicle officially consumes an available slot. |
| **Registration Number** | The legal identifier of a vehicle used for allocation tracking and subsequent release. |
| **Release** | The business process initiated when a vehicle vacates a slot, making it available for a new allocation. |
| **Slot** | The atomic unit of facility inventory. An allocation slot is always in one of two states: "Free" or "Occupied." |
| **Vehicle Type** | The categorization of a transient transport entity (e.g., Car, Motorcycle, EV) used to determine its eligibility for specialized zones. |

---

## 2. Facility Management (Supporting Subdomain)

| Term | Definition |
| :--- | :--- |
| **Facility** | A geographically distinct parking enterprise (e.g., "North Main Lot") containing one or more levels and zones. |
| **Level** | A physical floor or vertical division within a facility, used to organize physical slots. |
| **Topology** | The static structural map and configuration of all facilities, levels, and zones in the entire parking network. |
| **Zone** | A subset of slots within a facility that adheres to specific allocation rules (e.g., "EV-Only," "Premium Reservations"). |

---

## 3. EV Charging Station Management (Supporting Subdomain)

| Term | Definition |
| :--- | :--- |
| **Charge Percentage** | The real-time fuel/energy level reported by the vehicle's battery during an active session. |
| **Charger** | The specific physical hardware infrastructure that provides energy to a vehicle parked in an EV-designated slot. |
| **Charging Session** | The active lifecycle of energy transfer between a charger and an electric vehicle, monitored via hardware telemetry. |
| **Telemetry** | The stream of operational health indicators and session metrics emitted by charging hardware. |

---

## 4. Cross-Cutting Systems (Generic Subdomains)

| Term | Definition |
| :--- | :--- |
| **Alert** | A high-priority system signal indicating a business-critical failure (e.g., "Full Facility," "Hardware Fault"). |
| **Audit Log** | A historical, immutable record of all state mutations (allocations, releases, configuration updates) for system accountability. |
| **Staff Member** | Any authorized personnel (Manager, Attendant) with permissions to oversee facility operations. |
| **System Event** | An occurrence within the domain (e.g., "Vehicle Parked") that triggers downstream messaging or logging. |
