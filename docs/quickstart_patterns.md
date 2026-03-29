# Quick-Start: Design Pattern Examples & Testing

This guide helps developers quickly locate the applied design patterns in the Parking Lot Manager codebase and execute their corresponding automated test suites. It focuses strictly on discovery and execution to rapidly onboard engineers.

## 1. Strategy Pattern Example
- **Code Locations:** 
  - `parking_manager.py` (Classes: `ParkingStrategy`, `RegularParkingStrategy`, `ElectricParkingStrategy`)
  - Integration: `ParkingLot.park` method
- **Intent:** Encapsulates the specific parking allocation algorithms (capacity bounds-checking, vehicle array insertions, and subclass instantiations). This flattens former legacy nesting loops and enables the addition of future vehicle workflows without modifying the `park` orchestrator.

## 2. Observer Pattern Example
- **Code Locations:** 
  - `parking_manager.py` (UI/Domain boundaries inside `ParkingLot`)
- **Intent:** Decouples the core parking domain logic from the global Tkinter desktop environment bindings (`tfield`, `StringVar`). By shifting to a publisher-subscriber model, the `ParkingLot` logic broadcasts changes instead of artificially mutating the display.

## How to Run Automated Tests

The behavioral integrity of the design patterns is safeguarded by Python's native `unittest` engine. To ensure exact dependency alignment, tests should be executed via `uv`.

1. Ensure your terminal is in the project root: 
   `cd /Users/aaat/projects/parking-management-system`
2. Run the test discovery framework to cleanly execute all pattern configurations in a headless context:
   ```bash
   uv run python -m unittest discover tests/
   ```

*(For granular validation of the Strategy pattern exclusively, you can run: `uv run python -m unittest tests/test_park.py`)*
