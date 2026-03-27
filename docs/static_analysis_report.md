# Parking Lot Manager Static Analysis and Linter Baseline

## Baseline Verification

This analysis is based on the unmodified prototype source files currently present in the repository.

- Reviewed source scope: `ParkingManager.py`, `Vehicle.py`, `ElectricVehicle.py`, `pyproject.toml`
- Baseline proof: `git diff --name-only HEAD -- ParkingManager.py Vehicle.py ElectricVehicle.py pyproject.toml` returned no source-file differences
- Repository state during analysis: the only untracked changes in the worktree were documentation files, not application source files

## Current System Behavior Snapshot

The current system is a Tkinter desktop prototype for operating a single parking lot in memory.

- A user creates one lot with regular-slot capacity, EV-slot capacity, and floor number.
- A user can park a regular vehicle or EV, remove a vehicle, inspect lot status, inspect EV charge status, and look up slots or registration numbers by registration number or color.
- All operational state is stored in one `ParkingLot` object plus module-level Tkinter variables in `ParkingManager.py`.
- The prototype has no persistence, no API surface, and no multi-lot workflow.

## Tooling Run

Static inspection was run against the executable Python application modules in the repository.

| Tool | Command | Result |
| --- | --- | --- |
| Ruff | `uvx ruff check ParkingManager.py Vehicle.py ElectricVehicle.py` | 4 findings, all in `ParkingManager.py` |
| Pylint | `uvx pylint ParkingManager.py Vehicle.py ElectricVehicle.py --score=n` | 212 findings total: 163 in `ParkingManager.py`, 25 in `ElectricVehicle.py`, 24 in `Vehicle.py` |
| Basedpyright | `uvx basedpyright ParkingManager.py Vehicle.py ElectricVehicle.py` | 9 errors and 370 warnings; diagnostics were heavily concentrated in `ParkingManager.py` and `ElectricVehicle.py` |

## Key Findings

### Ruff

- `ParkingManager.py:3`: unused `sys` import
- `ParkingManager.py:234`: undefined name `make`
- `ParkingManager.py:244`: undefined name `model`
- `ParkingManager.py:279`: unused local variable `res`

### Pylint

- `ParkingManager.py:32`: `ParkingLot` has too many instance attributes and too many public methods, reinforcing that it acts as a god object
- `ParkingManager.py:64` and `ParkingManager.py:107`: `park` and `edit` take too many arguments
- `ParkingManager.py:50`, `ParkingManager.py:55`, `ParkingManager.py:60`: inconsistent return paths in helper methods
- `ParkingManager.py:234` and `ParkingManager.py:244`: undefined variables `make` and `model`
- `ParkingManager.py:43-44`: `slots` and `evSlots` are defined outside `__init__`
- `ParkingManager.py:300`: `main` has too many local variables and too many statements
- `ElectricVehicle.py:30` and `ElectricVehicle.py:38`: `ElectricVehicle.__init__` is called from non-parent classes

### Basedpyright

- `ElectricVehicle.py:30` and `ElectricVehicle.py:38`: hard type errors confirm that `ElectricCar` and `ElectricBike` are not assignable to `ElectricVehicle` even though they call its initializer
- `ParkingManager.py:43-44`: `slots` and `evSlots` are flagged as uninitialized instance variables
- `ParkingManager.py:234` and `ParkingManager.py:244`: undefined variables `make` and `model`
- `ParkingManager.py:8`: `root.resizable(0,0)` is flagged because Tkinter expects boolean arguments
- The remaining warning volume is dominated by missing type annotations and unknown member types, which indicates weak type clarity rather than isolated defects

## Prioritized Risk Areas

### Priority 1: `ParkingManager.py` is the primary hotspot

- **Locations:** `ParkingManager.py:6-29`, `ParkingManager.py:32-297`, `ParkingManager.py:300-414`
- **Tool evidence:** all Ruff findings, 163 Pylint findings, and the majority of Basedpyright diagnostics cluster here
- **Why it is highest risk:** This one module holds Tkinter globals, the main domain class, lookup logic, formatting, and UI bootstrap code. The concentration of diagnostics and responsibilities makes it the clearest refactoring priority.

### Priority 2: broken EV inheritance in `ElectricVehicle.py`

- **Locations:** `ElectricVehicle.py:28-40`
- **Tool evidence:** Pylint reports `non-parent-init-called`; Basedpyright raises hard type errors for passing `ElectricCar` and `ElectricBike` where `ElectricVehicle` is expected
- **Why it is high risk:** This is a correctness issue, not just a style issue. The EV model is structurally inconsistent, which can break future charging or polymorphic workflows.

### Priority 3: duplicated EV lookup helpers in `ParkingManager.py`

- **Locations:** `ParkingManager.py:218-246`
- **Tool evidence:** Ruff, Pylint, and Basedpyright all flag the undefined names in `getSlotNumFromMakeEv` and `getSlotNumFromModelEv`
- **Why it is high risk:** This is already defect-level duplication. The clone family has drifted into behavior that can fail at runtime.

### Priority 4: weak initialization and implicit contracts in `ParkingManager.py`

- **Locations:** `ParkingManager.py:43-44`, `ParkingManager.py:50-60`
- **Tool evidence:** Pylint flags attributes defined outside `__init__` and inconsistent returns; Basedpyright flags uninitialized instance variables
- **Why it is high risk:** These patterns make object state harder to reason about and increase the chance of order-dependent failures during future changes.

### Priority 5: repository-wide readability and type-clarity debt

- **Locations:** `ParkingManager.py`, `Vehicle.py`, `ElectricVehicle.py`
- **Tool evidence:** large volumes of missing-docstring, naming-style, long-line, and missing-type-annotation warnings
- **Why it matters:** These findings are lower severity than the structural defects above, but they still reduce readability, slow onboarding, and make the code harder to evolve safely.

## Assessment Summary

The static-analysis baseline confirms that the highest-risk areas are concentrated in `ParkingManager.py`, with a second critical hotspot in `ElectricVehicle.py`. The most actionable defects are the broken EV inheritance model, the duplicated EV lookup helpers with undefined names, and the oversized `ParkingLot` / `main` routines that concentrate too much responsibility in one module.

## Citation Note

This report uses repository-local evidence only. No external references were required.
