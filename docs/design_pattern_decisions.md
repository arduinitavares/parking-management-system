# Design Pattern Decision Record

This document records the selection and rationale for two design patterns to be implemented in the Parking Lot Manager codebase. These patterns establish reusable examples for codebase health improvement and address specific high-risk anti-patterns identified in the codebase health assessment.

## 1. Strategy Pattern

### Selected Pattern
**Strategy Pattern** (Behavioral)

### Implementation Scope and Workflow
- **Code Area:** `ParkingManager.py`, specifically the `ParkingLot.park` method (lines 64-89), as well as related slot-assignment logic.
- **Workflow:** Vehicle entry and slot allocation. The workflow will delegate the underlying logic of evaluating capacity, selecting a slot, and instantiating the correct vehicle type to a specialized strategy object rather than relying on inline branching within the `park` method.

### Problems Addressed
This pattern addresses the following issues identified in the codebase quality analysis:
- **Anti-Pattern 3 (Overly Nested Conditionals):** The `park` method currently mixes capacity checking, electric vehicle (EV) routing, and model construction in one dense block of `if/else` statements.
- **Health Assessment Priority 3 (Branch-heavy slot allocation flow):** The domain logic is brittle, hard to read, and difficult to extend.

### Technical Rationale
The Strategy pattern "defines a family of algorithms, encapsulates each one, and makes them interchangeable" (Gamma et al., 1994). By extracting the allocation algorithms into distinct strategy classes (e.g., `RegularParkingStrategy` and `ElectricParkingStrategy`), we flatten the control flow in the core `ParkingLot` orchestrator. This introduces the Open/Closed Principle: if future iterations require new vehicle categories (such as oversized vehicles or EV fast-charging priority slots), a new strategy can be introduced without modifying the monolithic `park` method.

## 2. Observer Pattern

### Selected Pattern
**Observer Pattern** (Behavioral)

### Implementation Scope and Workflow
- **Code Area:** `ParkingManager.py` (lines 117-145, 300-410). The boundary separating the `ParkingLot` domain logic (e.g., methods like `status` and `chargeStatus`) from the module-level Tkinter GUI state (`tfield`, `StringVar`, `IntVar`).
- **Workflow:** UI updates and reporting flow. The interaction model will be inverted so that the domain layer (`ParkingLot`) publishes state-change events upon mutations (like successful parking or departure), and independent presentation-layer subscribers listen to those events to update the UI components.

### Problems Addressed
This pattern addresses the following critical issues:
- **Anti-Pattern 2 (Layering Violations / Layer Skipping):** Domain code bypasses the presentation boundary and assigns output strings directly to Tkinter widgets.
- **Anti-Pattern 9 (God Object / Blob):** `ParkingLot` centralizes both core domain rules and GUI orchestrations.
- **Health Assessment Priority 1 (Tkinter globals plus ParkingLot acting as both UI and domain layer):** Resolving this direct coupling is necessary to unblock test automation.

### Technical Rationale
The Observer pattern "defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically" (Gamma et al., 1994). Implementing this pattern will completely decouple the `ParkingLot` behavior from the desktop-specific GUI mechanisms. The domain objects will no longer require `import tkinter` or direct access to global rendering variables. This architectural separation immediately restores unit testability, allowing automated test suites to instantiate and validate the `ParkingLot` without bootstrapping a graphical display environment.

## References

- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
