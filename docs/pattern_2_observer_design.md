# Observer Pattern Implementation Design (Pattern #2)

## 1. Mapping Pattern Structure to Target Code Area

The target refactoring area resides at the boundary between the `ParkingLot` domain model and the global Tkinter GUI references inside `parking_manager.py`. Currently, core business methods like `status()`, `charge_status()`, `park_car()`, and `remove_car()` forcibly invoke updates to global UI variables (e.g., `tfield`, `StringVar()`).

The Observer implementation will structurally separate these paradigms:
- **Subject (Publisher):** The `ParkingLot` object will be augmented to act as a publisher. It will store an internal list of registered listeners via an `attach(observer)` method, and trigger them using a `notify()` mechanism.
- **Observer Interface:** We will define an abstract `ParkingObserver(ABC)` interface establishing a strict contract: `update(event_type: str, payload: dict) -> None`.
- **Concrete Observer:** A new `TkinterDisplayObserver` class will be constructed specifically to encapsulate all GUI formatting and insertions (e.g., `tfield.insert()`). It will ingest events broadcast by the `ParkingLot`.
- **Execution Flow:** Rather than reading UI inputs internally or printing directly to `tfield`, the `ParkingLot` will solely return status flags or call `self.notify(...)`. The assigned Observer receives the state dictionary (e.g., successes, error strings, capacity tables) and performs the visual rendering independently.

## 2. Distinctness from Pattern #1

This pattern application represents an explicitly distinct structural use-case compared to Pattern #1:
- **Pattern #1 (Strategy):** Addressed algorithmic constraints, eliminating nested conditionals by exchanging object rules dynamically. It dictates **how decisions are made** (Domain behavior).
- **Pattern #2 (Observer):** Addresses tier separation and event lifecycle management. It dictates **how outputs are communicated** (Presentation behavior). 
The workflows targeted are orthogonal; one focuses on parsing car attributes into slots, while the other abstracts away the global desktop view dependency entirely.

## 3. Specific Anti-Pattern Instances to Remove

- **Anti-Pattern 1 (God Object):** Currently, the `ParkingLot` handles mathematical bounds, storage orchestration, UI event listeners, and direct screen-painting (`status` generating tabs and inserting strings). Extracting the display logic into a dedicated Observer formally removes `ParkingLot`'s status as a God Object.
- **Anti-Pattern 2 (Layering Violations):** `parking_manager.py` features presentation constants (`tk.INSERT`) mixed explicitly within business logic. The Observer pattern inherently neutralizes this layering violation. By enforcing `ParkingLot` to communicate via standard Python primitives (strings, dicts), the core codebase achieves zero dependency on the `tkinter` graphics libraries.
