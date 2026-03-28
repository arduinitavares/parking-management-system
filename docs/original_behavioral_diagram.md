# Original System Design: Behavioral Diagram

## Vehicle Entry Workflow (Pre-Refactor)

This artifact captures the **Original** behavioral sequence of the Parking Lot Manager system before any architectural refactoring. It describes one concrete, end-to-end system flow: a user parking a new vehicle (vehicle entry), highlighting the tight coupling between the Tkinter GUI and domain objects in the baseline system.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant GUI as Tkinter UI (main)
    participant PL as ParkingLot
    participant V as Vehicle / ElectricVehicle

    Note over User,V: Start Condition: App is running, Parking Lot is initialized

    User->>GUI: Enters details and clicks "Park Car"
    GUI->>GUI: Retrieves tk.StringVars (reg, make, model, color, ev, motor)
    GUI->>PL: park(regnum, make, model, color, ev, motor)
    
    rect rgb(200, 220, 240)
        Note over PL, V: Availability Check & Allocation
        alt is EV (ev == 1)
            PL->>PL: Check numOfOccupiedEvSlots < evCapacity
            PL->>PL: getEmptyEvSlot()
            PL->>V: Instantiate ElectricBike() or ElectricCar()
            PL-->>PL: Assign instance to evSlots[] array
            PL-->>PL: Increment evCounters
        else is Regular Vehicle
            PL->>PL: Check numOfOccupiedSlots < capacity
            PL->>PL: getEmptySlot()
            PL->>V: Instantiate Motorcycle() or Car()
            PL-->>PL: Assign instance to slots[] array
            PL-->>PL: Increment counters
        end
    end
    
    PL-->>GUI: Return allocated slotid (or -1 if full)
    
    alt slotid == -1
        GUI->>GUI: tfield.insert("Sorry, parking lot is full\n")
        GUI-->>User: Displays error message
    else slotid > -1
        GUI->>GUI: tfield.insert("Allocated slot number: [id]\n")
        GUI-->>User: Displays allocated slot number
    end
    
    Note over User,V: End Condition: Vehicle object created in array, slot ID displayed to user
```

## Architectural Review Notes & Iteration Findings

Following an initial review from an architecture/lead engineering perspective (informed by `codebase_health_assessment.md`), the following intrinsic anti-patterns and code health risks are illuminated by this flowchart:

1. **GUI/Domain Blurring (P1 Risk)**: The sequence demonstrates that `ParkingLot` performs both array-management operations (`getEmptyEvSlot()`) AND raw GUI manipulations (`GUI-->>GUI: tfield.insert`). Any attempt to write automated tests or separate the presentation tier is blocked by this design.
2. **Branch-Heavy Allocation Methods (P3 Risk)**: The `park(...)` interaction handles too many responsibilities—capacity checking, sorting between EV and Regular, object instantiation, tracking count—all in one nested monolithic routine.
3. **Weak Encapsulation (P5 Risk)**: The domain object exposes its raw slot arrays (`evSlots[]`, `slots[]`) directly for mutation without abstraction, risking state corruption and race conditions if this prototype is ever scaled or operated asynchronously.
