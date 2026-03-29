# Developer Guide: Observer Pattern (Pattern #2)

## Intent
The Observer Pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. In this application, it is used to decouple the core `ParkingLot` domain model from the Tkinter GUI. This resolves "Anti-Pattern 1: God Object" and "Anti-Pattern 2: Layering Violations" by removing direct UI widget manipulations from business logic.

## Pattern Structure & Code Locations
The implementation is contained within `parking_manager.py` and consists of three primary components:

### 1. The Observer Interface
An abstract base class that defines the update contract for any listener interested in Parking Lot events.
- **Code Location:** `parking_manager.py` (Line 137, `class ParkingObserver(ABC)`)
- **Key Method:** `update(self, event_type: str, message: str) -> None`

### 2. The Subject (Publisher)
The `ParkingLot` class maintains a list of observers and broadcasts notifications during state changes (parking, status checks, error reporting).
- **Code Location:** `parking_manager.py` (Line 160, `class ParkingLot`)
- **Key Methods:** `attach(observer)`, `notify(event_type, message)`

### 3. The Concrete Observer
A specialized class that handles the actual rendering of messages to the Tkinter `tfield` widget.
- **Code Location:** `parking_manager.py` (Line 147, `class TkinterDisplayObserver`)

## Executing the Test Suite
The Observer implementation is verified using standard Python `unittest` via the `uv` tool. The tests use mocks to simulate the UI state and verify that the domain logic correctly triggers notifications.

To verify the Observer logic and UI decoupling, run:
```bash
uv run python -m unittest tests/test_observer.py
```

### Verified Scenarios:
1. **test_nominal_status_output**: Asserts that `ParkingLot.status()` correctly triggers the observer to update the UI with vehicle data.
2. **test_edge_ui_rejection**: Asserts that internal domain errors (like a full parking lot) are broadcast via the observer rather than printed directly, ensuring the UI receives the error message.
