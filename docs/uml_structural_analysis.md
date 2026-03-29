# Structural UML Analysis: Refactored Codebase

This document serves as the data extraction baseline for creating the final Mermaid Structural UML Class Diagram for the EasyParkPlus application. It identifies all decoupled entities, relationships, design patterns, and structural readiness for multi-facility support.

## 1. Class and Interface Definitions

### Domain Models
- **`Vehicle` (BaseModel)**: Base class for standard combustion vehicles.
  - Subclasses: `Car`, `Truck`, `Motorcycle`, `Bus`.
- **`ElectricVehicle` (BaseModel)**: Base class for battery-operated vehicles.
  - Subclasses: `ElectricCar`, `ElectricBike`.
- **`ParkingLot`**: Core aggregate root managing state and persistence via injected repositories.

### Persistence Layer (`utils/repository.py`)
- **`Repository[T, ID]`**: Abstract generic interface defining `add`, `get`, `update`, `remove`, `find_by`.
- **`InMemoryRepository[T, str]`**: Concrete implementation of the baseline repository.
  - **`VehicleRepository`**: Extends InMemoryRepository customized for standard vehicles.
  - **`EVRepository`**: Extends InMemoryRepository customized for EVs.

### Interaction Layer
- **`UIState`**: Tkinter string variable manager, decoupling global UI variables from core app logic.
- **`DIContainer`**: Resolves and injects singletons and configurations.

## 2. Design Pattern Mapping

1.  **Strategy Pattern**:
    - **`ParkingStrategy`** (Interface): Defines `allocate_slot()`.
    - **`RegularParkingStrategy`**: Implements allocation logic focusing on `vehicle_repo` state constraints.
    - **`ElectricParkingStrategy`**: Implements allocation logic focusing on `ev_repo` state constraints.
    - *Relationship*: `ParkingLot.park()` contextually instantiates and delegates to strategies during allocation.
2.  **Observer Pattern**:
    - **`ParkingObserver`** (Interface): Defines `update()`.
    - **`TkinterDisplayObserver`**: Concretely prints string events to the injected Tkinter text widget.
    - *Relationship*: `ParkingLot` maintains `_observers: list[ParkingObserver]` and triggers `notify()` on state changes.
3.  **Dependency Injection**:
    - **`DIContainer`**: Bootstraps the Tkinter app, Repositories, UIState, and explicitly injects them into the `ParkingLot` object before launch, removing the legacy global-variable logic.
4.  **Repository Pattern**:
    - Fully decouples data array mutations from the `ParkingLot`. By delegating lookup lists strictly to `.find_by(...)`, the `ParkingLot` class remains ignorant of memory storage specifics.

## 3. Multi-Facility Structural Readiness

The structural transformation explicitly primes the system for **Multi-Lot Operations** without rewriting core definitions. This pathway is supported via:
- **Dependency Injected Models:** Because `ParkingLot` no longer hardcodes references to a global state variable, an encompassing "Facility Manager" module can seamlessly create multiple `ParkingLot` instances (e.g., `NorthLot`, `SouthLot`).
- **Isolated Repositories:** During multi-facility instantiation, `NorthLot` can be injected with its own fresh `VehicleRepository()`, maintaining completely segregated storage vectors from `SouthLot` in memory without clashing.
- **Polymorphic Observers:** A central control system could inject a `WebDashboardObserver` rather than a `TkinterDisplayObserver` into new lots, enabling cloud-based monitoring without touching `ParkingLot` logic.

This analysis provides the definitive blueprint required to draft the upcoming visual UML design block.
