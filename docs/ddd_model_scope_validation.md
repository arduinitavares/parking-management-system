# Model Scope Validation: EV Charging Boundaries

This document serves as the formal architectural validation for the EasyParkPlus Parking Management System's domain models. It ensures that the current conceptual models (Aggregates, Entities, and Value Objects) strictly adhere to the business boundaries and avoid premature integration of EV Charging logic.

## 1. Review of Parking Conceptual Focus

A comprehensive review of the current deliverables (`ddd_concept_catalog.md` and `ddd_aggregate_definitions.md`) has been conducted to confirm a pure parking-allocative focus.

*   **Parking Allocation Context:** Successfully identifies core entities like `Allocation` and `Allocation Slot` without coupling them to power or charging metrics. The `Vehicle Profile` correctly treats an "EV" status purely as a constraint marker (is it allowed in an EV space?) rather than an active battery load.
*   **Facility Management Context:** Successfully defines static geographical layouts (`Facility`, `Floor Level`, `Parking Zone`) without entangling physical hardware states (e.g., active Charger terminals vs. dormant terminals).

## 2. Validation of Excluded EV Charging Scope

To prevent scope creep and maintain architectural modularity, the following EV-specific domain concepts have been explicitly excluded from the current parking management models:

*   **Charging Session Tracking:** Entities responsible for initiating, monitoring (e.g., battery percentage), and securely terminating an electrical charge.
*   **Charger Hardware State:** Entities representing the physical diagnostic health and the active delivery phase of a Charger Terminal.
*   **Grid Telemetry / Energy Metrics:** Value objects that capture voltages, kilowatts, and charge curve histories. 
*   *Note:* These elements are strictly deferred to the upcoming specialized "EV Charging Domain Model" milestone.

## 3. Explicit Boundary Between Allocation and EV Subdomains

The validation confirms that the boundary between the Core Domain (Allocation) and the Supporting Subdomain (EV Charging) relies on a clean, unidirectional conceptual event hand-off rather than shared models.

1.  **Authorization (Core -> EV):** The Parking Allocation Context handles the business rules to allow an EV into a specialized slot. Once check-in is verified, it logically grants permission for a session to begin.
2.  **Telemetry (EV -> Core):** The EV Charging Subdomain owns the entire lifecycle of the electricity transfer. It notifies the Core Domain only when the session concludes (or faults), ensuring the core occupancy state machine is never polluted with real-time hardware diagnostics.

**Conclusion:** The Domain Model for Parking Management is validated as robust, parking-centric, and successfully modularized against EV Charging scope creep.
