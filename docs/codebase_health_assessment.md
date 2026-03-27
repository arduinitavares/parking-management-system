# Parking Lot Manager Baseline Codebase Health Assessment

## Assessment Scope

This assessment captures the state of the originally downloaded prototype before any source-code remediation work.

- Baseline commit inspected: `2a1eb4e095be1569047f32eae5299257c35a71ae`
- Repository state at evidence-collection time: clean working tree on `main` (`git status --short --branch` returned `## main...origin/main`)
- Source files reviewed for behavior and risk: `ParkingManager.py`, `Vehicle.py`, `ElectricVehicle.py`, `pyproject.toml`
- Repository automation/configuration areas reviewed: `.github/`, project root, `docs/`
- Source-history verification: `ParkingManager.py`, `Vehicle.py`, and `ElectricVehicle.py` each trace only to the repository's initial implementation commit (`c211dc9`), and `git diff --name-only HEAD -- ParkingManager.py Vehicle.py ElectricVehicle.py pyproject.toml` returned no differences for the assessed source files

## Current System Behavior Baseline

The current system is a single-process Tkinter desktop prototype for managing one parking lot in memory.

### What the system does now

1. Creates one parking lot with a regular-slot capacity, EV-slot capacity, and floor number via `ParkingLot.createParkingLot` in `ParkingManager.py`.
2. Parks either a regular vehicle or an electric vehicle through `ParkingLot.park`, using checkboxes to distinguish EV and motorcycle flows.
3. Removes a vehicle from a slot through `ParkingLot.leave`.
4. Displays the current regular and EV occupancy through `ParkingLot.status`.
5. Displays EV charge levels through `ParkingLot.chargeStatus`.
6. Supports lookups by registration number and color through `slotNumByReg`, `slotNumByColor`, and `regNumByColor`.

### Key workflow observations

- All state is held in memory inside one `ParkingLot` object plus module-level Tkinter globals in `ParkingManager.py`; there is no persistence layer, service boundary, or database.
- The UI exposes only one lot-management screen and one level at a time, so this is a single-lot prototype rather than a multi-site system.
- EV charge is observable but not meaningfully managed in the UI: EV instances start with `charge = 0`, and no UI workflow updates charge after parking.
- The application logic is tightly coupled to the Tkinter GUI because parking operations write directly to `tfield` and read directly from `StringVar` / `IntVar` values.

## Existing Test Coverage Metrics and CI Results

### Test automation baseline

| Check | Evidence | Result |
| --- | --- | --- |
| Test file inventory | `find . -maxdepth 3 \( -name 'test*' -o -name '*test*.py' -o -name '.coveragerc' -o -name 'coverage*' \)` | No test modules or coverage configuration were found in the tracked codebase. |
| `unittest` discovery | `python3 -m unittest discover -v` | `Ran 0 tests in 0.000s` and `NO TESTS RAN` (exit code 5). |
| `pytest` collection | `python3 -m pytest --collect-only` | Failed because `pytest` is not installed in the current project environment: `No module named pytest`. |
| Coverage tooling | `python3 -m coverage run -m unittest discover` | Failed because `coverage` is not installed in the current project environment: `No module named coverage`. |
| Project dependency declaration | `pyproject.toml` | No test runner, coverage tool, or CI-oriented dependency is declared. Only `ipykernel` is listed. |

### Coverage conclusion

The codebase does not currently provide a measurable automated coverage baseline. The strongest verifiable signal is that the repository contains zero discoverable automated tests, so there is no existing line or branch coverage report to collect from the unmodified baseline.

### CI baseline

| Check | Evidence | Result |
| --- | --- | --- |
| GitHub Actions workflows | `find .github -maxdepth 3 -type f` | No `.github/workflows/*` files exist. The only tracked file under `.github/` is `.github/agents/AntiPatternScout.agent.md`. |
| Other in-repo CI config | repository inventory | No other CI configuration files or badges were found in the repository root or docs. |

### CI conclusion

There are no existing CI results to report because the repository does not define an in-repo CI pipeline. In practical terms, the current baseline has no automated pull-request or branch validation signal.

## Prioritized Code Health Risks

The detailed anti-pattern inventory is recorded in `docs/anti_pattern_catalog.md`. The list below prioritizes the highest-risk areas for remediation planning based on defect likelihood, blast radius, and the degree to which they block future testing and architectural cleanup.

### Module Risk Summary

| Priority | Module / area | Size signal | Overall risk | Why it is a hotspot |
| --- | --- | --- | --- | --- |
| P1 | `ParkingManager.py` | 414 lines; 27 function definitions | Critical | The module combines Tkinter globals, the `ParkingLot` domain object, query logic, formatting, and the entire UI bootstrap path in one place. |
| P2 | `ElectricVehicle.py` | 41 lines; 3 classes | High | The EV hierarchy is structurally incorrect, which creates correctness risk in a small but central domain model. |
| P3 | `Vehicle.py` | 56 lines; 5 classes | Medium | The module is simple, but it leaks internal state broadly and includes unused abstractions that add maintenance noise. |
| P4 | `pyproject.toml` / repository automation surface | 9 lines; no test or CI tooling declared | Medium | The project configuration shows no built-in support for automated testing, coverage, or CI validation. |

### Hotspot Catalog

Priorities are ordered by four factors: defect likelihood, blast radius, impact on testability, and concentration of unrelated responsibilities.

| Priority | Hotspot | Location | Risk types | Why this hotspot matters now |
| --- | --- | --- | --- | --- |
| P1 | Tkinter globals plus `ParkingLot` acting as both UI and domain layer | `ParkingManager.py:6-29`, `ParkingManager.py:32-297`, `ParkingManager.py:300-414` | Maintainability, testability, readability, change amplification | The dominant module in the prototype owns UI state, orchestration, business logic, and display output, so almost any change collides here. |
| P2 | Duplicated lookup helpers, including live copy-paste defects | `ParkingManager.py:166-246` | Error-proneness, maintainability, regression risk | Near-duplicate methods have already drifted into broken behavior: EV lookup helpers reference undefined names (`make`, `model`). |
| P3 | Branch-heavy slot allocation flow | `ParkingManager.py:64-89` | Readability, extensibility, defect risk | `ParkingLot.park` handles capacity checks, EV routing, vehicle construction, slot assignment, and counter mutation in one nested routine. |
| P4 | Broken EV type hierarchy | `ElectricVehicle.py:28-40` | Correctness, maintainability, extensibility | `ElectricCar` and `ElectricBike` borrow initialization from `ElectricVehicle` without inheriting from it, so polymorphism is already broken. |
| P5 | Public mutable vehicle state and weak encapsulation | `Vehicle.py:2-19`, `ElectricVehicle.py:1-25`, consumed in `ParkingManager.py:117-145`, `ParkingManager.py:147-155`, `ParkingManager.py:197-206` | Maintainability, error-proneness, testability | `ParkingLot` reaches directly into vehicle fields, which spreads domain knowledge and couples many methods to representation details. |
| P6 | Missing automated safety net | repository-wide absence of `tests/`, coverage config, and `.github/workflows`; `pyproject.toml:1-9` | Testability, operational risk | The code already contains brittle areas, but the repository has no tests, no coverage report, and no CI gate to catch regressions. |
| P7 | Unused code paths and abstractions | `Vehicle.py:29-53`, `ParkingManager.py:60-62`, `ParkingManager.py:107-115` | Readability, maintainability | `Truck`, `Bus`, `getEmptyLevel`, and `edit` expand the code surface without participating in the observable prototype workflow. |

### Priority 1: `ParkingManager.py` is both the UI layer and the domain layer

- **Locations:** module-level Tkinter state (`ParkingManager.py:6-29`), `ParkingLot` core behavior (`ParkingManager.py:32-297`), GUI construction in `main` (`ParkingManager.py:300-414`)
- **Risk:** `ParkingLot` mixes slot allocation, query logic, status formatting, and direct Tkinter interaction in one module/class.
- **Why this is highest risk:** This file is the central change hotspot. Any future work on parking rules, UI behavior, error handling, or test automation will hit the same tightly coupled code paths, which makes isolated testing and safe refactoring difficult.

### Priority 2: EV lookup helpers in `ParkingManager.py` already contain copy-paste defects

- **Locations:** `getSlotNumFromMakeEv` (`ParkingManager.py:228-236`), `getSlotNumFromModelEv` (`ParkingManager.py:238-246`)
- **Risk:** Both methods reference undefined variables (`make` and `model`) instead of their parameters, indicating duplicated code that has drifted into runtime-failure territory.
- **Why this is high risk:** These are immediate error-proneness issues in user-visible query paths. The absence of tests or CI means defects of this type can remain latent until manual execution reaches the affected branch.

### Priority 3: EV subtype modeling is broken in `ElectricVehicle.py`

- **Locations:** `ElectricCar` (`ElectricVehicle.py:28-33`), `ElectricBike` (`ElectricVehicle.py:36-40`)
- **Risk:** EV subclasses call `ElectricVehicle.__init__` directly but do not inherit from `ElectricVehicle`, so they acquire fields like `charge` without participating in the actual EV type hierarchy.
- **Why this is high risk:** This undermines correctness for any future EV-specific behavior, including charging workflows, validation, or polymorphic handling. For example, an `ElectricCar` instance has a `charge` field but `isinstance(car, ElectricVehicle)` is false.

### Priority 4: There is no automated regression safety net

- **Locations:** repository-wide absence of `tests/`, coverage config, and `.github/workflows`; dependency declaration in `pyproject.toml:1-8`
- **Risk:** The prototype has no test suite, no coverage reporting, and no CI gate.
- **Why this is high risk:** The code already contains defect-prone duplication and coupling. Without automated verification, later remediation work will have weak feedback loops and a higher chance of introducing behavior regressions.

### Priority 5: Vehicle modeling and unused code increase maintenance noise

- **Locations:** unused vehicle subclasses `Truck` and `Bus` in `Vehicle.py:29-53`; unused or weakly integrated helpers such as `getEmptyLevel` (`ParkingManager.py:60-62`) and `edit` (`ParkingManager.py:107-115`)
- **Risk:** The codebase exposes abstractions and methods that are not part of the observable prototype workflow, which blurs the real scope of the application.
- **Why this matters:** This is lower priority than the issues above, but it still harms readability and increases the surface area a maintainer must inspect before making changes.

## Assessment Summary

The baseline prototype is a small, single-lot desktop application with clear user workflows, but it has no automated test coverage, no CI pipeline, and several high-risk design defects concentrated in `ParkingManager.py` and `ElectricVehicle.py`. The most urgent remediation target is the coupling between GUI state and parking logic because that coupling amplifies nearly every other quality risk and blocks clean testability improvements.

## Citation Note

This assessment was produced from repository-local evidence only. No external references were required for the findings above, so there are no external citations to include in this document.
