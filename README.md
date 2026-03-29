# EasyParkPlus: Quick-Start Guide

Welcome to the EasyParkPlus Parking Management System refactoring project. This document is designed to help onboarding developers rapidly locate our implemented architecture patterns and execute their supporting boundary tests.

## 1. Concrete Design Pattern Locations
We are actively refactoring the single-lot prototype's architecture to eliminate critical tech debt (e.g., "God Object" and "Overly Nested Conditionals"). 

### Pattern #1: Strategy Pattern
- **Intent:** Abstracts divergent parking allocation algorithms (verifying capacity constraints, managing array indices, and triggering subclass instantiations) into interchangeable objects based on vehicle category (EV vs. Regular), enforcing the Open/Closed Principle.
- **Location:** `parking_manager.py`
  - *Abstractions:* `ParkingStrategy`, `RegularParkingStrategy`, `ElectricParkingStrategy`
  - *Context Logic:* Delegated exclusively within the `ParkingLot.park` method.

### Pattern #2: Observer Pattern
- **Intent:** Slices the core `ParkingLot` domain structure away from the static Tkinter desktop rendering bindings (`tfield`, `StringVar`) using a publisher-subscriber event model to broadcast state mutations cleanly.
- **Location:** `parking_manager.py`
  - *Context Logic:* Applied natively during status readouts (`status`, `charge_status`) and mutating actions (`park_car`, `make_lot`).

---

## 2. Automated Test Execution
The architectural patterns are defended by Python's standard `unittest` framework running identically in CI and local setups via modern `uv` dependency wrapping. Our tests intelligently mock GUI initialization to allow for fully headless validations.

From this project root directory (`/Users/aaat/projects/parking-management-system`), run the commands below:

**To execute the entire project behavioral suite:**
```bash
uv run python -m unittest discover tests/
```

**To run targeted boundaries during refactoring:**
```bash
# Validate Pattern #1 (Strategy):
uv run python -m unittest tests/test_park.py

# Validate Pattern #2 (Observer):
uv run python -m unittest tests/test_observer.py
```

*(A successful run will indicate the exact number of passed tests in `< 1.000s` and conclude with `OK`)*

---

## 3. Setup and Execution Instructions

### Prerequisites
- **Python 3.13+**: The codebase relies on modern typing features (`TypeAlias`, `A|B` unions, etc.).
- (Optional but recommended) `uv`: Fast Python package and project manager.

### Standard Setup (Using standard `venv` and `pip`)
1. **Clone/Extract** the repository and navigate to the root directory.
2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Quick Setup (Using `uv`)
If you have `uv` installed, it simplifies the setup:
```bash
uv sync
```

### Execution Steps
To launch the primary application with its graphical Tkinter interface:
```bash
# Using standard venv
python parking_manager.py

# Or via uv
uv run python parking_manager.py
```

---

## 4. Core Parking Operations

The application provides a comprehensive UI to manage a dedicated parking facility capable of handling regular combustion-engine vehicles and fully electric vehicles (EVs). 

1. **Lot Creation**: Initializes the core dimension of the facility. You can specify:
   - *Number of Regular Spaces*: Slots purely for standard cars/trucks/motorcycles.
   - *Number of EV Spaces*: Dedicated electric charging slots.
   - *Floor Level*: The parking floor identifier (e.g., Level 1).
2. **Park Car**: Allocates an incoming vehicle to an open slot.
   - Takes vehicle parameters: *Make*, *Model*, *Color*, and *Registration #*.
   - Routes transparently to either standard lots or EV lots via the Strategy pattern.
3. **Remove Car**: Deallocates a tracked vehicle freeing up capacity.
   - Provide the specific *Slot ID* and specify if it is an *EV*.
4. **Occupancy Status Checks**: Read real-time parking maps.
   - Use the **Operations / Query** buttons to list *Vehicle Status* across regular slots.
   - View explicit *EV Charge Status*.
   - Filter queries precisely by *Color* or *Registration #* to quickly locate lost vehicles.
