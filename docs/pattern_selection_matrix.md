# Pattern Selection Matrix

This matrix maps the selected design patterns to the specific anti-patterns and codebase health risks they are intended to resolve within the Parking Lot Manager prototype.

| Design Pattern | Target Code Area / Workflow | Primary Anti-Pattern Addressed | Secondary Health Risk Addressed | Expected Architectural Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Strategy Pattern (Behavioral)** | `ParkingManager.py`: `ParkingLot.park` (Lines 64-89) | **Anti-Pattern 3**: Overly Nested Conditionals. Mixes routing, bounds checking, and construction. | **Health Assessment P3**: Branch-heavy slot allocation flow. | Flattens control flow by encapsulating slot allocation algorithms into interchangeable strategy classes (e.g., `RegularParkingStrategy`, `ElectricParkingStrategy`). Enables adherence to the Open/Closed Principle. |
| **Observer Pattern (Behavioral)** | `ParkingManager.py`: `ParkingLot` boundary to Tkinter global state (Lines 117-145, 300-410) | **Anti-Pattern 2 & 9**: Layering Violations / Layer Skipping and God Object / Blob. | **Health Assessment P1**: Tkinter globals plus `ParkingLot` acting as both UI and domain layer. | Decouples the domain logic from the Tkinter GUI. `ParkingLot` publishes state-change events rather than directly mutating text fields, restoring automated testability to the monolithic domain object. |
