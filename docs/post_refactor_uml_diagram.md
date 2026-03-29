# Post-Refactor Structural Architecture

This document contains the structural UML representation of the modernized `EasyParkPlus` codebase. It highlights the successful remediation of legacy anti-patterns (global variables, monolithic classes) through the explicit decoupling of domain models, persistence layers, and UI views using industry-standard design patterns.

## Mermaid Class Diagram

```mermaid
classDiagram
    %% Core Domain Aggregation
    class ParkingLot {
        -int capacity
        -int ev_capacity
        -int level
        -List~ParkingObserver~ _observers
        -VehicleRepository vehicle_repo
        -EVRepository ev_repo
        -UIState ui_state
        +park(regnum, make, model, color, ev, motor) int
        +leave(slotid, ev) bool
        +status() void
        +attach(observer: ParkingObserver) void
        +notify(event_type, message) void
    }

    %% Dependency Injection (Anti-Pattern: Global State -> Resolved)
    class DIContainer {
        -dict _services
        +register_instance(type, instance)
        +resolve(type) instance
    }
    DIContainer ..> ParkingLot : injects dependencies
    DIContainer ..> VehicleRepository : instantiates
    DIContainer ..> EVRepository : instantiates

    %% Repository Pattern (Data Storage Decoupling)
    class Repository~T, ID~ {
        <<interface>>
        +add(ID, T)
        +get(ID)
        +update(ID, T)
        +remove(ID)
        +find_by(**kwargs)
    }

    class InMemoryRepository~T, str~ {
        -dict _store
        +add(ID, T)
        +find_by(**kwargs)
    }

    class VehicleRepository {
        %% Manages Regular Active Allocations
    }

    class EVRepository {
        %% Manages EV Active Allocations
    }

    Repository <|.. InMemoryRepository : implements
    InMemoryRepository <|-- VehicleRepository : extends
    InMemoryRepository <|-- EVRepository : extends
    
    ParkingLot o-- VehicleRepository : aggregates
    ParkingLot o-- EVRepository : aggregates

    %% Strategy Pattern (Anti-Pattern: Control Coupling -> Resolved)
    class ParkingStrategy {
        <<interface>>
        +allocate_slot(lot, regnum, make, model, color, motor) int
    }

    class RegularParkingStrategy {
        +allocate_slot() int
    }

    class ElectricParkingStrategy {
        +allocate_slot() int
    }

    ParkingStrategy <|.. RegularParkingStrategy : implements
    ParkingStrategy <|.. ElectricParkingStrategy : implements
    ParkingLot ..> ParkingStrategy : uses contextually

    %% Observer Pattern (Anti-Pattern: Presentation Monolith -> Resolved)
    class ParkingObserver {
        <<interface>>
        +update(event_type, message)
    }

    class TkinterDisplayObserver {
        -tk.Text tfield
        +update(event_type, message)
    }

    ParkingObserver <|.. TkinterDisplayObserver : implements
    ParkingLot o-- ParkingObserver : manages

    %% Vehicle Domain Hierarchy
    class Vehicle {
        <<Entity>>
        +str regnum
        +str make
        +str model
        +str color
    }
    
    class ElectricVehicle {
        <<Entity>>
        +int charge
    }

    Vehicle <|-- Car
    Vehicle <|-- Truck
    Vehicle <|-- Motorcycle
    
    ElectricVehicle <|-- ElectricCar
    ElectricVehicle <|-- ElectricBike
    
    VehicleRepository *-- Vehicle : stores
    EVRepository *-- ElectricVehicle : stores
```

## Highlights & Structural Improvements

1. **Strategy Pattern Illustration:** The `ParkingLot` context dynamically selects between `RegularParkingStrategy` and `ElectricParkingStrategy`. This resolved the legacy branching logic mapping (Control Coupling Anti-Pattern).
2. **Repository Pattern Illustration:** The `InMemoryRepository` decouples the aggregate domain logic (`ParkingLot`) from physical storage operations. This resolved the monolithic array-looping logic mapping (God Class Anti-Pattern).
3. **Observer Pattern Illustration:** The `TkinterDisplayObserver` is injected asynchronously mapped via logic events (`notify()`), completely detaching UI view operations from domain algorithms (Presentation logic leak).
4. **Dependency Injection & Multi-Facility Support:** Because `DIContainer` is responsible for registering state instances, a larger system can easily instantiate multiple `ParkingLot` models and inject disparate `VehicleRepositories` dynamically, enabling multi-lot operation.
