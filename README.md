# EasyParkPlus: Parking Management System

> A software design & architecture project demonstrating OO design pattern implementation, anti-pattern remediation, and a DDD-based microservices architecture proposal.

This project refactors a legacy single-lot parking prototype into a maintainable, extensible application and proposes a scalable microservices design to support multi-facility parking and EV charging management.

---

## Quick-Start Guide

### Prerequisites
- **Python 3.13+**: The codebase relies on modern typing features (`TypeAlias`, `A|B` unions, etc.).
- (Optional but recommended) `uv`: Fast Python package and project manager.

### Quick Setup (Using `uv` — Recommended)
```bash
uv sync
```

### Standard Setup (Using `venv`)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -e .
```

### Run the Application
```bash
# Using uv
uv run python parking_manager.py

# Or using standard venv
python parking_manager.py
```

---

## Running Tests

The architectural patterns are defended by Python's standard `unittest` framework with headless mocking for fully CI-compatible validations.

```bash
# Run the full test suite
uv run python -m unittest discover tests/

# Run targeted pattern tests
uv run python -m unittest tests/test_park.py      # Strategy Pattern
uv run python -m unittest tests/test_observer.py  # Observer Pattern
```

A successful run will report `18 tests in < 1.000s` and conclude with `OK`.

---

## Design Patterns Implemented

### Pattern #1: Strategy Pattern
- **Intent:** Abstracts divergent parking allocation algorithms into interchangeable objects based on vehicle category (EV vs. Regular), enforcing the Open/Closed Principle.
- **Location:** `parking_manager.py`
  - *Abstractions:* `ParkingStrategy`, `RegularParkingStrategy`, `ElectricParkingStrategy`
  - *Context:* Delegated exclusively within `ParkingLot.park()`.

### Pattern #2: Observer Pattern
- **Intent:** Decouples the `ParkingLot` domain model from Tkinter GUI bindings using a publisher-subscriber event model, restoring unit testability.
- **Location:** `parking_manager.py`
  - *Abstractions:* `ParkingObserver`, `TkinterDisplayObserver`
  - *Context:* Applied during status readouts and all mutating parking actions.

---

## Core Application Features

1. **Lot Creation** — Configure regular & EV slot capacities and floor level.
2. **Park Vehicle** — Allocates cars, motorcycles, or EVs to available slots via Strategy dispatch.
3. **Remove Vehicle** — Deallocates a slot by ID for both regular and EV parking.
4. **Occupancy Status** — Real-time slot map for regular and EV parking areas.
5. **Lookup Queries** — Filter by Color or Registration # to locate specific vehicles.

---

## Architecture & Design Documentation

The `docs/` directory contains the full architectural design record for this project:

| Document | Description |
| :--- | :--- |
| [`consolidated_pattern_justification.md`](docs/consolidated_pattern_justification.md) | Written justification for Strategy and Observer pattern implementations. |
| [`codebase_audit_report.md`](docs/codebase_audit_report.md) | Full anti-pattern audit and verification report (18/18 tests passing). |
| [`ddd_context_map.md`](docs/ddd_context_map.md) | Bounded context diagram for the proposed multi-facility architecture. |
| [`ev_charging_domain_model.md`](docs/ev_charging_domain_model.md) | DDD tactical model for the EV Charging subdomain. |
| [`microservices_catalog.md`](docs/microservices_catalog.md) | Proposed microservices design with per-service responsibilities and databases. |
| [`microservices_migration_guidance.md`](docs/microservices_migration_guidance.md) | Strangler Fig migration plan from monolith to microservices. |
