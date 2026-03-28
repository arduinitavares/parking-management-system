# Primary User-Facing Flows and System Interactions

Based on an analysis of the baseline codebase (`ParkingManager.py`), the Parking Lot Manager system exposes several primary workflows to the end user via a Tkinter Graphical User Interface.

## 1. System Initialization (Lot Creation)
- **User Action**: The user enters the desired dimensions of the physical lot: number of Regular spaces, number of EV (Electric Vehicle) spaces, and the Floor level. They click "Create Parking Lot".
- **System Interaction**: The UI calls `ParkingLot.createParkingLot()`, which allocates two finite, fixed-size lists (arrays) in memory. A confirmation snippet detailing the resulting layout is pushed onto the system's text display field.

## 2. Vehicle Entry (Park Car)
- **User Action**: The user inputs attributes for an arriving vehicle: Make, Model, Color, and Registration `#`. They denote if it is an EV or a Motorcycle via checkboxes, then click "Park Car".
- **System Interaction**: The system triggers `ParkingLot.park()`. It validates domain limits (if capacity exists in either the regular or EV buckets) and seeks an empty slot index. A domain object (`Car`, `Motorcycle`, `ElectricCar`, `ElectricBike`) is instantiated and stored in the respective array. The system issues a string output with the allocated slot ID, or an error if the lot is full.

## 3. Vehicle Exit (Remove Car)
- **User Action**: When a vehicle departs, the user inputs the known Slot `#`, toggles the "Remove EV?" checkbox according to the vehicle type, and clicks "Remove Car".
- **System Interaction**: The GUI executes `ParkingLot.leave()`, which directly overrides the specified array index back to `-1` (empty state) and decrements the respective counter for occupied spaces. Updates the UI log with the success status.

## 4. Search and Retrieval (Queries)
Users can actively query the system's real-time state via several dedicated searches:
- **Get Slot ID by Registration #**: Returns a specific slot identification given an exact plate number.
- **Get Slot ID by Color**: Returns a comma-separated list of slot numbers containing vehicles of a matched color.
- **Get Registration # by Color**: Returns a comma-separated list of license plates belonging to vehicles of a requested color.
- **System Interaction**: In each scenario, the `ParkingLot` class aggressively iterates over both regular and EV array stores, inspecting individual object attributes (e.g. `i.color == color`), accumulating hits, and rendering them back to the Tkinter text component.

## 5. Operational Status Reporting
- **Current Lot Status**: Upon clicking this button, the console lists all currently populated slots, segregated by Regular Vehicles and Electric Vehicles, formatting their metrics (Slot, Floor, Reg No., Color, Make, Model) evenly.
- **EV Charge Status**: Returns a specific view localized to Electric Vehicles, itemizing the same physical locations but specifically enumerating the battery charge percentage attribute of the `ElectricVehicle` domain objects.
- **System Interaction**: Both reporting flows sequentially iterate through the arrays, skipping `-1` indicators, and concatenating structured string formats before injecting the resultant blob into the `tfield` variable in the UI.

## Architectural Review Notes & Iteration Findings

Following an initial review from the architecture/lead engineering perspective (informed by `codebase_health_assessment.md`), we have iterated on these documented flows to highlight structural risks intrinsic to the baseline application:

1. **Tight GUI-to-Domain Coupling (P1 Risk)**: Across all five workflows, the UI orchestrates state read/write directly with the `ParkingLot` object. Most critically, methods inside the domain tier (e.g., `ParkingLot.status()`, `ParkingLot.park()`) contain literal `tfield.insert(...)` calls. This violation of the MVC/Separation of Concerns principle makes the data layer entirely dependent on a Tkinter GUI context.
2. **Brittle Search Implementation (P2 Risk)**: The query operations iterated over raw arrays and contain copy-paste discrepancies. Specifically, EV lookup flows attempt to reference undefined `make` and `model` variables (present in regular car lookups but mishandled when copied to EV variants). This necessitates logic extraction and abstraction during refactoring.
3. **Broken EV Modeling (P4 Risk)**: The "Park Car" flow instantiates EV objects that circumvent proper inheritance from `ElectricVehicle`—a major liability anticipating the upcoming EV Charging Station Management feature request.
