# Pattern Analysis Notes

## 1. High-Risk Areas from Health Assessment
Based on `docs/codebase_health_assessment.md`, the prioritized high-risk areas are:
- **Priority 1 (Critical):** `ParkingManager.py` - The UI layer is acting as the domain layer. The Tkinter module globals and the `ParkingLot` object are tightly coupled, handling both UI output and domain logic.
- **Priority 2 (High):** `ParkingManager.py` - Duplicated lookup helpers (e.g., `getSlotNumFromMakeEv`, `getSlotNumFromModelEv`) containing live copy-paste defects.
- **Priority 3 (High):** `ParkingManager.py` - Branch-heavy slot allocation flow in `ParkingLot.park` handling capacity, EV routing, and object creation.
- **Priority 4 (High):** `ElectricVehicle.py` - Broken EV type hierarchy where subclasses do not properly inherit from the base class.

## 2. Anti-Pattern Instances by Severity
Based on `docs/anti_pattern_catalog.md`, the anti-patterns by severity are:

### Critical
- **Broken Inheritance / Incorrect OO Reuse:** `ElectricCar` and `ElectricBike` fail to properly inherit from `ElectricVehicle` (lines 28-40 in `ElectricVehicle.py`).
- **God Object / Blob:** `ParkingLot` in `ParkingManager.py` centralizes GUI behavior, slot allocation, reporting, and reporting format into one class (lines 32-297 in `ParkingManager.py`).

### High
- **Layering Violations:** `ParkingLot` interacts directly with Tkinter global variables (`tfield`, `StringVar`) instead of decoupling presentation and domain (lines 6-29, 117-145, etc., in `ParkingManager.py`).
- **Overly Nested Conditionals:** The `park` method mixes slot allocation, bounds checking, and vehicle generation in nested `if/else` statements (lines 64-89 in `ParkingManager.py`).
- **Duplicated Code:** Six near-identical lookup functions for slots (e.g., `getSlotNumFromColor`, `getSlotNumFromColorEv`) are present in `ParkingManager.py`.
- **Inappropriate Intimacy:** `ParkingLot` accesses mutable fields of `Vehicle` and `ElectricVehicle` directly, violating encapsulation.

### Medium
- **Dead Code / Unused Abstractions:** Unused classes (`Truck`, `Bus`) and functions (`edit`, `getEmptyLevel`).
- **Returning Different Types:** Helpers like `getEmptySlot` return an integer on success but implicitly return `None` on failure.
- **Hidden Temporal Coupling:** The `ParkingLot` constructor does not initialize slot lists; callers must manually invoke `createParkingLot` first.

### Low
- **Clumsy Loop Statements:** Redundant `else: continue` blocks in loops within `ParkingManager.py`.
- **Lack of Comments:** Missing docstrings for core domain methods and obvious inline comments.

## 3. Recommended Code Areas for Pattern Application
Based on the analysis, the following areas are ideal candidates for design pattern application to resolve high-severity technical debt:

1. **`ParkingLot.park` method (`ParkingManager.py`):**
   - **Target:** The overly nested, branch-heavy logic for capacity checking and object construction.
   - **Candidate Pattern:** Strategy Pattern or Factory Method. Extracting the allocation rules into strategies (e.g., `RegularSlotStrategy` and `EVSlotStrategy`) will resolve the "Overly Nested Conditionals" anti-pattern and improve the maintainability of vehicle routing.

2. **UI-Domain Boundary (`ParkingManager.py`):**
   - **Target:** The direct coupling between `ParkingLot` and Tkinter variables.
   - **Candidate Pattern:** Observer Pattern or Model-View-Controller (MVC). Inverting the dependency so that `ParkingLot` emits state changes to an observer will resolve the "God Object" and "Layering Violations" anti-patterns, dramatically improving testability.

3. **Duplicated Lookup Helpers (`ParkingManager.py`):**
   - **Target:** The repetitive `getSlotNumFrom...` functions.
   - **Candidate Pattern:** Template Method or Strategy Pattern. These could standardize the search algorithm across different vehicle attributes and collections.
