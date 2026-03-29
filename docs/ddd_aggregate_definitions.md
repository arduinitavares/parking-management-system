# Parking Domain: Aggregate Definitions

This document identifies the foundational Aggregates and Aggregate Roots for the EasyParkPlus Parking Management System. Each aggregate establishes a conceptual consistency boundary to ensure data integrity during distributed multi-facility operations.

---

## 1. Facility Aggregate
- **Bounded Context:** Facility Management
- **Aggregate Root:** `Facility`
- **Conceptual Boundary:** This aggregate encapsulates the complete physical topology of a single enterprise location. It ensures that changes to the hierarchy (Floors, Zones, and physical Slot coordinates) are consistent with the facility's identity and global capacity constraints. 
  - *Internal Components:* Facility Metadata, Levels, Zones, Physical Slots.
  - *Consistency Rule:* You cannot mutate a Level or Zone without going through the Facility root, ensuring that the total sum of partitioned capacities never exceeds the facility's licensed structural limit.

---

## 2. Allocation Aggregate
- **Bounded Context:** Parking Allocation
- **Aggregate Root:** `Allocation`
- **Conceptual Boundary:** This aggregate represents the singular lifecycle of a vehicle's residence within the parking network. It acts as the primary transaction boundary for real-time occupancy.
  - *Internal Components:* Allocation ID, Vehicle Metadata, Entry/Exit Timestamps, Occupied Slot reference.
  - *Consistency Rule:* An Allocation must remain atomic. You cannot "Check-in" a vehicle without a confirmed free slot state, and a slot cannot be "Released" without terminating the associated Allocation entity. This ensures that the system's current inventory state is always perfectly synchronized with the physical reality.

---

## 3. Account Activity Aggregate
- **Bounded Context:** Audit & Logging
- **Aggregate Root:** `AuditEntry`
- **Conceptual Boundary:** This aggregate ensures the immutability and provenance of a single recorded system mutation.
  - *Internal Components:* Event ID, Timestamp, Actor ID (Staff), Payload (the change that occurred).
  - *Consistency Rule:* Once created, an AuditEntry cannot be altered or deleted. It represents a finalized historical footprint of a domain event.

---

## 4. Model Constraints & Scope Verification
- **Implementation Agnostic:** This model defines conceptual boundaries and does not map to specific Python modules, class inheritance structures, or database schemas.
- **Exclusion of EV Charging:** Detailed EV charging state aggregates (e.g., "Charging Session," "Power Meter") are explicitly **out-of-scope** for this deliverable and are deferred to the specialized EV Design milestone. 
- **Business Scope:** This model strictly covers confirmed domain areas (Allocation, Topology, Auditing). No assumptions regarding reservations, dynamic pricing, or commercial enforcement aggregates have been introduced.
