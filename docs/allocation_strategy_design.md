# Strategy Pattern Design: Allocation Algorithms

This design document outlines the Strategy Pattern implementation intended to decouple the complex vehicle allocation logic within the EasyParkPlus `ParkingLot` module. By encapsulating allocation rules into discrete strategies, we remove anti-pattern condition branching (e.g., massive if-else blocks checking `ev == 1`) from the core context.

## 1. Strategy Contract & Interface Design

The foundational element of the pattern is the generic interface that all concrete allocation algorithms must implement.

- **Interface:** `ParkingStrategy (ABC)`
- **Execute Method:** `allocate_slot(lot: ParkingLot, regnum: str, make: str, model: str, color: str, motor: int) -> int`
- **Contract:** The execute method requires a reference to the `ParkingLot` state object. It evaluates capacity constraints, finds an appropriate empty slot identifier, instantiates the target `Vehicle` entity, inserts it into the state array, and returns the one-based integer `slot_id`. If allocation fails (due to capacity), it must return `-1`.

## 2. Allocation Algorithm Variants

We are mapping the previously monolithic `park()` logic into two distinct, scalable concrete strategies:

### Variant A: `RegularParkingStrategy`
- **Responsibility:** Handles the dimensioning and placement of standard internal combustion engine (ICE) cars and motorcycles.
- **State Targets:** Interacts exclusively with `lot.slots`, `lot.num_of_occupied_slots`, and `lot.capacity`.
- **Entity Creation:** Instantiates `Vehicle.Car` or `Vehicle.Motorcycle`.

### Variant B: `ElectricParkingStrategy`
- **Responsibility:** Governs the specialized placement rules for electric vehicles (EVs) seeking charging infrastructure.
- **State Targets:** Interacts exclusively with `lot.ev_slots`, `lot.num_of_occupied_ev_slots`, and `lot.ev_capacity`.
- **Entity Creation:** Instantiates `ElectricVehicle.ElectricCar` or `ElectricVehicle.ElectricBike`.

## 3. Strategy Selection and Configuration

Strategy selection happens at runtime dynamically, driven by the attributes of the incoming vehicle. 

- **Context Object:** `ParkingLot` 
- **Selection Point:** The updated `park()` method acts as the client context router.
- **Configuration Logic:**
  - The client UI or API provides a raw `ev` parameter (0 or 1).
  - The `park()` method intercepts this parameter.
  - If `ev == 1`, it configures the internal strategy state to `ElectricParkingStrategy()`.
  - If `ev == 0`, it configures the strategy state to `RegularParkingStrategy()`.
  - Once configured, it actively delegates the parking request by calling `strategy.allocate_slot()`, entirely abstracting away the differing internal array manipulation rules.

## Outcome
This design officially breaks the "God Object" anti-pattern in `ParkingLot`, shifting algorithmic responsibility outward. Future requirements (like "Premium Pass Allocation") will simply require a new class inheriting from `ParkingStrategy`, adhering to the Open-Closed Principle.
