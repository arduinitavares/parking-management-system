# Strangler Fig: Architectural Transition Guidance

This document provides the stepwise playbook for migrating the refactored EasyParkPlus monolith (`parking_manager.py`) to the new microservices architecture. It uses the **Strangler Fig Pattern** to minimize risk and ensure zero-downtime during the transition.

---

## 1. Migration Roadmap

| Phase | Description | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- | :--- |
| **Phase 1: Coexistence** | Microservices operate in "Shadow Mode" alongside the monolith. | Services deployed; empty DBs. | >99% Data parity in local logs. |
| **Phase 2: Transition** | Active traffic is incrementally routed to new services. | Adapters implemented in Monolith. | All subdomains migrated. |
| **Phase 3: Decommission** | Legacy monolithic logic is removed. | 100% Traffic on services for 14 days. | Zero legacy code in production. |

---

## 2. Technical Interception Strategy: The Adapter Pattern

The current **Milestone 3** codebase is already primed for migration via its **Repository Pattern** and **DI Container**.

- **Interception Point:** The `BaseRepository` interface in `utils/repository.py`.
- **Implementation:** Create a new `RestRepository(BaseRepository)` adapter that translates method calls (e.g., `add()`, `get_all()`) into HTTP REST calls to the corresponding microservice (`ParkingService` or `EVService`).
- **Toggle Mechanism:** The `DIContainer` in `parking_manager.py` acts as the master switch. Changing the injected repository type triggers the redirection.

```python
# Example DI Toggle in parking_manager.py
class DIContainer:
    def __init__(self, use_microservices=False):
        if use_microservices:
            # Route to new services
            self.allocation_repo = RestAllocationRepository(api_url="https://api.easypark.com")
        else:
            # Stay in Legacy Mode
            self.allocation_repo = InMemoryRepository()
```

---

## 3. Risk Mitigation & Rollback Procedures

### Data Synchronization: Dual-Write Strategy
During Phase 2, the **Repository Adapters** must perform a "Dual-Write":
1. Write to the new Microservice (Primary).
2. Write to the legacy `InMemoryRepository` (Secondary/Backup).
This ensures that the legacy UI state remains perfectly synchronized with the cloud-based truth.

### Fail-Safe Rollback (Emergency DI Toggle)
If the new service exceeds the following **Rollback Triggers**, the team must toggle the `DIContainer` back to `use_microservices=False`:
- **Latency Spike:** > 200ms increase in check-in duration.
- **Error Rate:** > 1% failure rate on check-out requests.
- **Data Mismatch:** Inconsistency detected between the REST response and the local shadow log.

---

## 4. Multi-Facility Phasing Timeline

1. **Sprint 4 (Weeks 7-8):** Migrate **Facility Management** (The Topology baseline).
2. **Sprint 5 (Weeks 9-10):** Migrate **EV Charging Subdomain** (The new high-value capability).
3. **Sprint 6 (Weeks 11-12):** Migrate **Parking Allocation Core** (Final decommission of the monolith).

> [!IMPORTANT]
> Always migrate the **Facility Management** service first. It provides the metadata (Slots, Layers) required by all other contexts.
