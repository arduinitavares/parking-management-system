# Developer Guide: Strategy Pattern (Pattern #1)

## Intent
The Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime. In the context of the Parking Lot Manager application, its primary intent is to natively isolate complex branching logic tied to allocating variables (like verifying capacity limitations and indexing into the correct arrays) for different segments. 

By applying this pattern, we successfully strip away deeply-nested conditional statements and enforce the **Open/Closed Principle**. If business requirements eventually demand a new category (e.g., VIP Slots or Oversized Parking), engineers can construct a new strategy class instead of dangerously mutating the monolithic `park` orchestration routing.

## Pattern Structure & Code Locations
The refactoring distributes the domain constraints across three explicit architectural layers found within `parking_manager.py`.

### 1. The Strategy Interface
The abstract base class (`ABC`) that enforces all dynamic allocation flows strictly adhere to the designated method signature.
- **Code Location:** `parking_manager.py` (Line 40, `class ParkingStrategy(ABC)`)
- **Key Method:** `allocate_slot(self, lot, regnum, make, model, color, motor) -> int`

### 2. Concrete Strategies
Distinct, decoupled algorithms directly managing the array indexing, bounds-checking, and polymorphic instantiation for the targeted segment types.
- **Code Location (Regular):** `parking_manager.py` (Line 57, `class RegularParkingStrategy`)
- **Code Location (EV):** `parking_manager.py` (Line 99, `class ElectricParkingStrategy`)

### 3. The Context Driver
The central `ParkingLot` object provides the dataset (occupancy metrics, list references) and acts as the orchestrator to inject the incoming data down into the generated strategy.
- **Code Location:** `parking_manager.py` (Line 139, `class ParkingLot`)
- **Usage Area:** Inside `ParkingLot.park` (Line 183), an `if ev == 1:` guard selects the underlying Strategy class, instantiates it, and delegates the routing operation to it.

## Executing the Test Suite
The operational behavior of the Strategy interfaces is fortified by regression tests leveraging Python's `unittest` framework dynamically run inside our modern `uv` workspace constraint map.

To verify pattern logic locally and ensure no architectural structural compromises are introduced, navigate to the root workspace directory and execute:
```bash
uv run python -m unittest tests/test_park.py
```

This triggers 4 headless scenarios:
1. `test_nominal_park_regular_car`: Generates bounds and tests positive allocation metrics.
2. `test_nominal_park_ev_car`: Tests successful EV branch propagation and initialization bounds.
3. `test_edge_case_lot_full`: Purposely overfills Regular capacity limits to test strategy `-1` rejection fallbacks.
4. `test_edge_case_ev_lot_full`: Purposely overfills EV capacity limits (while bypassing regular checking) to verify isolated bounds defense.

*(Note: Safe headless testing is possible because `test_park.py` automatically injects a patched interface over tkinter, blocking external GUI/display requests).*
