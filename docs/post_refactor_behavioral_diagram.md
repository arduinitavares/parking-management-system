# Post-Refactor Behavioral Architecture

This document presents the behavioral UML sequence for the refactored EasyParkPlus system. It illustrates the dynamic interactions and decoupled message-passing facilitated by the Strategy, Repository, and Observer design patterns.

## Mermaid Sequence Diagram: Vehicle Allocation (Park)

This diagram demonstrates how the `ParkingLot` delegates allocation logic to a `Strategy` and state persistence to a `Repository`, finally notifying the `UI` via an `Observer`.

```mermaid
sequenceDiagram
    participant User as Actor (User)
    participant UI as UI Boundary (Tkinter/UIState)
    participant PL as Controller (ParkingLot)
    participant PS as Strategy (ParkingStrategy)
    participant RP as Persistence (Repository)
    participant OB as Observer (TkinterDisplayObserver)

    User->>UI: Input Vehicle Data (Reg, Make, etc.)
    User->>UI: Click "Park Car"
    UI->>PL: park_car()
    
    rect rgb(240, 240, 240)
        Note over PL, PS: Strategy Pattern Selection
        PL->>PS: allocate_slot(lot, data...)
        
        alt is Electric
            PS->>RP: EVRepository.get_empty_ev_slot()
            RP-->>PS: slot_id
            PS->>RP: EVRepository.add(slot_id, ElectricVehicle)
        else is Regular
            PS->>RP: VehicleRepository.get_empty_slot()
            RP-->>PS: slot_id
            PS->>RP: VehicleRepository.add(slot_id, Vehicle)
        end
        PS-->>PL: slot_number
    end

    PL->>OB: notify("display_update", message)
    OB->>UI: tfield.insert(message)
    UI-->>User: Visual Confirmation ([ACTION: Park Car])
```

## Behavioral Improvements & EV Integration

1. **Decoupled Data Flow:** The diagram shows that the `ParkingLot` (Controller) no longer manages the vehicle list directly. It delegates to the `Strategy` for logic and the `Repository` for storage.
2. **EV Charging Integration:** The sequence explicitly branches to the `EVRepository` when the electric flag is detected, ensuring EV-specific attributes (like charge levels) are managed within their own domain context.
3. **Observer Encapsulation:** Unlike the legacy code where the domain logic updated the UI directly (monolithic anti-pattern), the refactored flow uses a push-based `notify()` mechanism. This ensures the domain logic remains "UI-ignorant."
4. **Behavioral Accuracy:** This sequence represents the removal of the *Control Coupling* anti-pattern, as the `ParkingLot` no longer contains the internal branching logic for specific vehicle types; it simply executes the polymorphic `allocate_slot` method.
