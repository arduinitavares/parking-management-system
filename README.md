# EasyParkPlus: Quick-Start Guide

Welcome to the EasyParkPlus Parking Management System refactoring project. This document is designed to help onboarding developers rapidly locate our implemented architecture patterns and execute their supporting boundary tests.

## 1. Concrete Design Pattern Locations
We are actively refactoring the single-lot prototype's architecture to eliminate critical tech debt (e.g., "God Object" and "Overly Nested Conditionals"). 

### Pattern #1: Strategy Pattern
- **Intent:** Abstracts divergent parking allocation algorithms (verifying capacity constraints, managing array indices, and triggering subclass instantiations) into interchangeable objects based on vehicle category (EV vs. Regular), enforcing the Open/Closed Principle.
- **Location:** `parking_manager.py`
  - *Abstractions:* `ParkingStrategy`, `RegularParkingStrategy`, `ElectricParkingStrategy`
  - *Context Logic:* Delegated exclusively within the `ParkingLot.park` method.

### Pattern #2: Observer Pattern
- **Intent:** Slices the core `ParkingLot` domain structure away from the static Tkinter desktop rendering bindings (`tfield`, `StringVar`) using a publisher-subscriber event model to broadcast state mutations cleanly.
- **Location:** `parking_manager.py`
  - *Context Logic:* Applied natively during status readouts (`status`, `charge_status`) and mutating actions (`park_car`, `make_lot`).

---

## 2. Automated Test Execution
The architectural patterns are defended by Python's standard `unittest` framework running identically in CI and local setups via modern `uv` dependency wrapping. Our tests intelligently mock GUI initialization to allow for fully headless validations.

From this project root directory (`/Users/aaat/projects/parking-management-system`), run the commands below:

**To execute the entire project behavioral suite:**
```bash
uv run python -m unittest discover tests/
```

**To run targeted boundaries during refactoring:**
```bash
# Validate Pattern #1 (Strategy):
uv run python -m unittest tests/test_park.py

# Validate Pattern #2 (Observer):
uv run python -m unittest tests/test_observer.py
```

*(A successful run will indicate the exact number of passed tests in `< 1.000s` and conclude with `OK`)*
