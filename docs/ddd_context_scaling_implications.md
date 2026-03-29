# Bounded Contexts: Multi-Facility Scaling Implications

This analysis annotates the architectural scaling implications for the defined Bounded Contexts as EasyParkPlus evolves from the legacy single-lot prototype into a fully distributed multi-facility network. In accordance with the current milestone constraints, this document strictly concerns *domain boundary transformations* and explicitly excludes service deployments, physical databases, or API endpoint specifications.

## 1. Parking Allocation Context (Core Domain)
**Scaling Impact:** High

### Expected Context Evolution
- **Current State:** The legacy implementation assumes a single, local integer-tracked memory state where one `ParkingLot` instance routes all capacity decisions.
- **Scaling Transformation:** As the system scales to multiple distinct facilities, the Allocation Context must evolve to handle distributed concurrency and aggregate boundaries based fundamentally on a `FacilityIdentifier`. The core logic will shift from simple array index checks (e.g., `slots[i] = -1`) to resolving complex rulesets enforcing maximum capacity guarantees across multiple asynchronous facility checkpoints.

## 2. Facility Management Context (Supporting Subdomain)
**Scaling Impact:** High

### Expected Context Evolution
- **Current State:** The legacy prototype constructs a facility using a rigid set of UI variable casts (`make_lot` with fixed `evcapacity` and `level`).
- **Scaling Transformation:** This context must transform into a robust hierarchical catalog mapping diverse physical locations. The boundary will expand to define "Parking Estates," encapsulating multiple physical structures containing disparate floor configurations and specialized zones (e.g., "Standard," "Premium," "EV-Only").

## 3. EV Charging Context (Supporting Subdomain)
**Scaling Impact:** High

### Expected Context Evolution
- **Current State:** Currently abstracted as assigning an `ElectricVehicle` object into a localized `ev_slots` array alongside simulated status readouts.
- **Scaling Transformation:** The boundary will expand to manage external domain interactions (e.g., physical IoT charging hardware integration). The context must evolve to track dynamic session properties (KW transfer, grid status) spanning multiple diverse hardware providers deployed across isolated geographic facilities, necessitating strict consistency checks against the core Allocation Context.

## 4. Identity & Access Management (IAM) Context (Generic Subdomain)
**Scaling Impact:** Medium

### Expected Context Evolution
- **Scaling Transformation:** As multiple facilities come online, IAM rules will expand from basic system-level permissions to geo-fenced or facility-scoped authorization. The context will evolve to support declarations like "Attendant Alpha can manage overrides exclusively at Facility B."

## 5. Audit & Logging Context (Generic Subdomain)
**Scaling Impact:** Low to Medium

### Expected Context Evolution
- **Scaling Transformation:** The core auditing capability remains stable. The evolution requires standardizing the domain event structure to ensure every logged action carries an explicit topology marker (e.g., `facility_id`, `zone_id`), allowing administrators to trace distributed occurrences accurately across a multi-site network.

## 6. Notification Context (Generic Subdomain)
**Scaling Impact:** Medium

### Expected Context Evolution
- **Current State:** Presently relies on synchronous, in-memory Observer callbacks directed exclusively at a single local screen (`tfield`).
- **Scaling Transformation:** Must evolve into a multi-channel dispatcher capable of routing contextual alerts (e.g., "Hardware Fault") specifically to the attendants stationed at the impacted facility, rather than broadcasting globally to the entire system.

---
*Technical Lead Validation Note: The designated scaling impacts correctly restrict the analysis strictly to logical domain behavior (event routing, concurrency bounds, hierarchical definitions) while adhering identically to the product constraints restricting premature microservice implementation discussions.*
