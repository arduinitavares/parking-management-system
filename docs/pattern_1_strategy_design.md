# Strategy Pattern Implementation Design (Pattern #1)

## 1. Mapping Pattern Structure to Target Code

The target area is the `ParkingLot.park` method in `ParkingManager.py`, which is currently monolithic and contains branching logic for varying slot collections, capacities, and vehicle instantiation types.

- **Context Object:** `ParkingLot` will act as the context that holds the data records (slots, capacity) and orchestrates the strategy invocation.
- **Strategy Interface:** A standard abstract class (e.g., `ParkingStrategy`) defining the contract `allocate_slot(lot, regnum, make, model, color, is_motorcycle) -> int`.
- **Concrete Strategies:**
  - `RegularParkingStrategy`: Applies rules specifically for regular slots. It evaluates against `lot.capacity`, invokes `lot.getEmptySlot()`, and instantiates `Vehicle.Car` or `Vehicle.Motorcycle` based on the motorcycle flag.
  - `ElectricParkingStrategy`: Applies rules specifically for electric slots. It evaluates against `lot.evCapacity`, invokes `lot.getEmptyEvSlot()`, and instantiates `ElectricVehicle.ElectricBike` or `ElectricVehicle.ElectricCar`.

*Workflow transition:* `ParkingLot.park` will use a simple factory/conditional at the top level to instantiate the correct Strategy based on the `ev` parameter and then delegate to it.

## 2. Specific Anti-Pattern Instances to Remove

- **Anti-Pattern 3 (Overly Nested Conditionals):** The current method `park` explicitly spans 5 levels of nesting (`if (self.numOfOccupiedEvSlots < ...)`, `if (ev == 1):`, `if (motor == 1):`, etc.). This entire structure will be replaced by object delegation.
- **Hidden Defect Surface:** The legacy baseline had initialization bugs within the nesting (where `motor=0` randomly swapped objects). The flattened strategy logic inherently guards against copying and pasting deep conditionals like that. 

## 3. Test Coverage Strategy

The test coverage relies on the regression safety net authored in `tests/test_park.py` during the preceding task.

- **Objective:** Pure structure-preserving refactoring. The interface for `ParkingLot.park(self, regnum, make, model, color, ev, motor)` must remain totally identical to external clients (e.g., the Tkinter GUI methods calling it).
- **Nominal Coverage:** The existing `test_nominal_park_regular_car` and `test_nominal_park_ev_car` will guarantee that each concrete strategy correctly modifies state, updates occupancy variables, and stores the correct Vehicle subtype in the array.
- **Edge-Case / Error Coverage:** The existing full-lot rejection tests (`test_edge_case_lot_full`, `test_edge_case_ev_lot_full`) ensure that the localized boundaries inside `allocate_slot` replicate the historical capacity rejections perfectly (returning `-1`).
- **Execution:** We will execute `python3 -m unittest tests/test_park.py` immediately after implementation to detect structural regressions.
