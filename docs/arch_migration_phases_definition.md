# EasyParkPlus: Strangler Fig Migration Phases

This document defines the formal lifecycle for incrementally migrating components from the refactored monolith to the microservices architecture. It establishes the technical criteria and business readiness scores required for each transition.

---

## Phase 1: Identify & Shadow
**Objective:** Validate that the new microservice is functionally equivalent to the legacy monolith component.

### Checklist
- [ ] **Infrastructure Setup:** Deploy the target microservice and its database.
- [ ] **Audit Proxy:** Wrap the legacy component (e.g., `FacilityManager`) in an audit proxy.
- [ ] **Shadow Logging:** Capture all monolith inputs/outputs and forward them asynchronously to the microservice.
- [ ] **Data Consistency Audit:** Run a daily report on response parity.

| Criteria Type | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Technical** | Service deployed; Monitoring active. | 14 days of 100% Data Parity in logs. |
| **Business** | Low-risk candidate selected (Facility). | Verification report signed by Lead Arch. |

---

## Phase 2: Intercept & Route
**Objective:** Transition to the new service as the "Authoritative" source for selected traffic.

### Checklist
- [ ] **Adapter Pattern implementation:** Create a `RestRepository` adapter in the monolith.
- [ ] **Dual-Write Configuration:** Configure the adapter to write to both the Monolith DB and the Service DB.
- [ ] **Gradual Routing:** Divert 10% of traffic, incrementally scaling to 100%.
- [ ] **Observability Monitoring:** Monitor latency and error rates for the new service path.

| Criteria Type | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Technical** | Shadowing period complete; Zero data drift. | 100% Traffic successfully routed for 7 days. |
| **Business** | Rollback plan (DI Toggle) tested. | Zero reported customer regressions. |

---

## Phase 3: Final Cutover & Decommission
**Objective:** Eliminate the legacy logic and maximize system performance.

### Checklist
- [ ] **Legacy Deletion:** Remove the local logic and internal DB tables from the monolith.
- [ ] **Code Cleanup:** Remove the "Dual-Write" logic from the adapters (Simplified REST client).
- [ ] **System Audit:** Final performance benchmark for the fully decoupled system.

| Criteria Type | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Technical** | Service established as Single Source of Truth. | Zero legacy code in production. |
| **Business** | Maintenance window for final cleanup. | Migration Story Closed. |
