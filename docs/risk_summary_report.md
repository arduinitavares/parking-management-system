# Parking Lot Manager Risk Summary Report

## Baseline Verification

This report is based on the unmodified prototype source files currently in the repository:

- Assessed source files: `ParkingManager.py`, `Vehicle.py`, `ElectricVehicle.py`, `pyproject.toml`
- Baseline evidence: `git diff --name-only HEAD -- ParkingManager.py Vehicle.py ElectricVehicle.py pyproject.toml` returned no source-file differences
- Repository history check: `ParkingManager.py`, `Vehicle.py`, and `ElectricVehicle.py` trace back to the repository's initial implementation commit in this repo

## Current System Behavior

The current application is a Tkinter desktop prototype for managing a single parking lot in memory.

- Users create one lot with regular-slot capacity, EV-slot capacity, and a floor number.
- Users can park regular vehicles and EVs, remove vehicles, view lot status, view EV charge status, and query slots or registration numbers by registration number or color.
- All runtime state lives in one `ParkingLot` object and module-level Tkinter variables in `ParkingManager.py`.
- The application does not persist data, expose an API, or support multi-lot workflows.

## Top Risks

### P1. `ParkingManager.py` is the main hotspot

- **Locations:** `ParkingManager.py:6-29`, `ParkingManager.py:32-297`, `ParkingManager.py:300-414`
- **Why it is high risk:** The module combines GUI state, domain logic, slot allocation, query helpers, and UI rendering in one place. This creates the largest change hotspot and makes later testing and refactoring difficult.

### P2. Lookup logic in `ParkingManager.py` already contains defect-prone duplication

- **Locations:** `ParkingManager.py:166-246`
- **Why it is high risk:** The regular and EV lookup helpers are copy-paste variants, and the EV helpers `getSlotNumFromMakeEv` and `getSlotNumFromModelEv` already reference undefined names (`make`, `model`), which is a concrete runtime-risk signal.

### P3. EV inheritance is structurally broken

- **Locations:** `ElectricVehicle.py:28-40`
- **Why it is high risk:** `ElectricCar` and `ElectricBike` call `ElectricVehicle.__init__` but do not inherit from `ElectricVehicle`, so EV objects do not participate in the intended type hierarchy.

### P4. There is no automated regression safety net

- **Locations:** repository-wide absence of `tests/`, coverage config, and `.github/workflows`; `pyproject.toml:1-9`
- **Why it is high risk:** The repository currently has no automated tests, no measurable coverage baseline, and no CI validation path, so defects can persist unnoticed.

### P5. Encapsulation and dead-code issues add maintenance drag

- **Locations:** `Vehicle.py:2-19`, `Vehicle.py:29-53`, `ElectricVehicle.py:1-25`, `ParkingManager.py:60-62`, `ParkingManager.py:107-115`
- **Why it is medium risk:** Public mutable fields, unused abstractions (`Truck`, `Bus`), and unused helpers (`getEmptyLevel`, `edit`) increase maintenance noise and couple modules more tightly than necessary.

## Recommended Next-Step Tickets

### Ticket 1: Separate parking domain logic from Tkinter UI wiring

- **Priority:** Highest
- **Scope:** Extract core parking operations and queries out of `ParkingManager.py` into testable domain/application classes.
- **Primary targets:** `ParkingManager.py:6-29`, `ParkingManager.py:32-297`, `ParkingManager.py:300-414`
- **Why this should come first:** It reduces the main hotspot and makes the rest of the codebase easier to test and refactor safely.

### Ticket 2: Fix duplicated EV lookup helpers and consolidate query logic

- **Priority:** High
- **Scope:** Correct the broken EV lookup helpers and replace clone families with shared search logic.
- **Primary targets:** `ParkingManager.py:166-246`
- **Why this should come next:** This area already contains likely runtime defects and is a clear example of error-prone duplication.

### Ticket 3: Repair the EV class hierarchy

- **Priority:** High
- **Scope:** Make `ElectricCar` and `ElectricBike` inherit from `ElectricVehicle` properly and align EV behavior behind a real shared base type.
- **Primary targets:** `ElectricVehicle.py:28-40`
- **Why this matters:** It removes a correctness problem in the EV domain model before new EV behavior is added.

### Ticket 4: Establish an initial automated test and CI baseline

- **Priority:** High
- **Scope:** Add a minimal test runner, baseline unit tests around parking and lookup behavior, coverage tooling, and a simple CI workflow.
- **Primary targets:** repository root, `pyproject.toml`, new `tests/`, new `.github/workflows/`
- **Why this matters:** Later refactoring work needs a feedback loop; without one, high-risk changes stay risky.

### Ticket 5: Reduce representation leakage and remove unused code

- **Priority:** Medium
- **Scope:** Tighten vehicle encapsulation, remove or quarantine unused classes/helpers, and clarify which behaviors are active prototype scope.
- **Primary targets:** `Vehicle.py`, `ElectricVehicle.py`, `ParkingManager.py:60-62`, `ParkingManager.py:107-115`
- **Why this matters:** This lowers maintenance noise and improves readability once the major structural risks are underway.

## Citation Note

This report uses repository-local evidence only and does not rely on external references.
