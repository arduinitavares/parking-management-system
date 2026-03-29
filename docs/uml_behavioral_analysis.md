# Behavioral UML Analysis: Refactored Interaction Logic

This document maps the dynamic behavior and message-passing sequences of the EasyParkPlus system. It identifies the lifecycle of key operations and documents the data flow improvements resulting from the removal of procedural anti-patterns.

## 1. Core Workflow Mapping

### Workflow A: Vehicle Allocation (Park)
**Sequence:**
1. **Trigger:** UI invokes `parkinglot.park_car()`.
2. **Context Resolution:** `ParkingLot` reads `UIState` variables.
3. **Strategy Delegation:** `ParkingLot` instantiates the appropriate `ParkingStrategy` (Regular or Electric) based on the `ev` flag.
4. **Validation:** `Strategy` queries the corresponding `Repository` (`vehicle_repo` or `ev_repo`) for capacity and empty slots.
5. **Entity Creation:** `Strategy` instantiates a `Vehicle` or `ElectricVehicle` subclass.
6. **Persistence:** `Strategy` calls `repo.add()`.
7. **Notification:** `ParkingLot` calls `notify()`, triggering the `TkinterDisplayObserver` to update the UI text widget.

### Workflow B: Vehicle Deallocation (Remove)
**Sequence:**
1. **Trigger:** UI invokes `parkinglot.remove_car()`.
2. **Identification:** `ParkingLot` calls `leave(slotid, ev)`.
3. **Persistence Mutation:** `Repository` executes `remove(slotid)`, verifying record existence.
4. **Notification:** `ParkingLot` broadcasts the deallocation event to all attached `Observers`.

### Workflow C: Global Status Query
**Sequence:**
1. **Trigger:** UI invokes `parkinglot.status()`.
2. **Data Aggregation:** `ParkingLot` performs a sorted retrieval from both `vehicle_repo` and `ev_repo`.
3. **Streamed Reporting:** `ParkingLot` iterates through records, sending formatted string fragments to `Observers` via `notify()`.

## 2. EV Charging Industry Logic Interactions
The refactored workflow treats EV instances as specialized entities with extended state:
- **Interaction:** When `charge_status()` is invoked, the system strictly targets the `EVRepository` context.
- **Behavior:** This ensures that standard vehicle queries are not bloated by EV-specific logic (Charge %, Plug types), maintaining a clear behavioral boundary between the two domains.

## 3. Data Flow Improvements (Anti-Pattern Remediation)

| Legacy Behavior (Anti-Pattern) | Refactored Behavior (Improved) |
|:-------------------------------|:-------------------------------|
| **Global Access:** Method accessed `global vehicle_list` directly. | **Dependency Injection:** `ParkingLot` receives `Repositories` via constructor; no global scope used. |
| **Control Coupling:** Procedural `if-else` blocks for every vehicle type. | **Strategy Pattern:** Logic is encapsulated in `RegularParkingStrategy` vs `ElectricParkingStrategy`. |
| **Presentation Leak:** Domain logic called `print()` or updated UI widgets directly. | **Observer Pattern:** Domain logic generates events; `Observers` handle UI rendering independently. |
| **Hardcoded Indices:** Manual management of list indices. | **Repository Indexing:** `InMemoryRepository` manages 1-based string IDs, abstracting storage complexity. |

This interaction mapping provides the sequence logic required for the upcoming Behavioral UML Sequence Diagram.
