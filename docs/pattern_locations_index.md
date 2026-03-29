# Design Patterns Location Index

This index helps developers quickly locate the exact files containing the codebase's selected design patterns and provides the architectural intent for each implementation.

## Pattern Example #1: Strategy Pattern

**Intent:** Encapsulates the divergent parking allocation algorithms—such as capacity bounds-checking, vehicle array insertions, and type-specific instantiations—so they can be interchanged seamlessly based on the input vehicle category. This resolves deeply nested "if/else" capacity conditionals and enforces the Open/Closed Principle.

- **Primary Framework File:** `parking_manager.py`
  - *Components:* `ParkingStrategy(ABC)`, `RegularParkingStrategy`, `ElectricParkingStrategy`
  - *Context Origin:* Instructed dynamically by the `ParkingLot.park` method.
- **Verification Suite:** `tests/test_park.py`

## Pattern Example #2: Observer Pattern

**Intent:** Decouples the core `ParkingLot` parking data structure from the global Tkinter desktop rendering system (`tfield`, `StringVar`, `IntVar`). By migrating the tight coupling into a publisher-subscriber model, the domain logic broadcasts state changes (e.g., parking allocation success, capacity reached) without knowing about the display layer, thereby removing the "God Object" and "Layering Violation" anti-patterns.

- **Primary Framework File:** `parking_manager.py`
  - *Components:* Expected publisher bindings attached to `ParkingLot` status and mutation functions (`status`, `charge_status`, `park`). 
  - *Subscriber Elements:* The separated `Tkinter` UI component logic initializing standard desktop widgets.
- **Verification Suite:** `tests/test_observer.py` *(Note: Execution bounds pending final observer merge)*
