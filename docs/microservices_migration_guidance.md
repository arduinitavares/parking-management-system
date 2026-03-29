# EasyParkPlus: Consolidated Microservices Migration Guidance

This document provides the definitive implementation roadmap and risk mitigation strategy for transitioning the EasyParkPlus system from a modular monolith to a distributed microservices architecture using the Strangler Fig pattern.

---

## 1. Strangler Fig Migration Phases

We will migrate the system in three distinct phases, ensuring data integrity and zero customer downtime.

| Phase | Strategy | Action | Success Criteria |
| :--- | :--- | :--- | :--- |
| **P1: Shadow** | **Transform** | Wrap legacy component in a proxy; asynchronously forward traffic to the new service. | 14 days of 100% Data Parity between stores. |
| **P2: Route** | **Co-exist** | Implement `RestRepository` adapter in monolith; toggle traffic via DI Container. | 100% traffic successfully routed for 7 days. |
| **P3: Purge** | **Eliminate** | Physically remove legacy code, internal tables, and dual-write logic from monolith. | Zero legacy code remaining in production. |

---

## 2. Risk Matrix & Mitigation

| Phase | Category | Risk | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **P1** | Technical | **Data Drift**: New service state differs from legacy. | Mandatory daily parity auditing and shadow-log analysis. |
| **P2** | Business | **System Latency**: Dual-writing increases response times. | Use **Transactional Outbox** for non-blocking asynchronous updates. |
| **P2** | Technical | **Split Brain**: Partial updates in one store only. | Implement **Distributed Transaction / Saga** patterns for critical flows. |
| **P3** | Technical | **Orphaned Data**: Legacy tables taking up resources. | Formal data migration checkout before final table dropping. |

---

## 3. Deployment Safety: First Phase Rollback

To ensure the safety of the initial "Facility Management" migration, the following protocols are mandated:

### Success Criteria (P1 Exit)
- **Log Parity:** Automated comparison of Mono-DB vs. Service-DB results showing 0% variance.
- **Latency Impact:** Overhead of the audit proxy must remain `<15ms`.
- **Infrastructure:** Microservice must pass 500 simultaneous request load tests.

### Rollback Procedure (Emergency Only)
1. **Toggle Change:** In the `DIContainer`, switch the `FacilityRepository` binding from `RestAdapter` back to `InMemoryRepository`.
2. **Restart:** Re-trigger the monolith deployment to pick up the legacy repository binding.
3. **Data Re-sync (if needed):** In P2, the Mono-DB is the source of truth, so no data restoration is required during an emergency rollback.

---

## 4. Target Architecture References

This guidance relies on the following structural specifications for the target microservices:

- **Service Registry:** [Microservices Catalog](file:///Users/aaat/projects/parking-management-system/docs/microservices_catalog.md) (Defines all 4 service boundaries).
- **Data Blueprint:** [Per-Service Database Concepts](file:///Users/aaat/projects/parking-management-system/docs/ev_charging_db_schema.md) (Defines the Relational vs. Time-Series split).
- **Communication:** [API Sketches Master](file:///Users/aaat/projects/parking-management-system/docs/service_communication_sketches.md) (Defines the REST/Event bridge).
