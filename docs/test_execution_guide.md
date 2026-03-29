# Test Execution Procedure Guide

This guide ensures any developer onboarding to the Parking Lot Manager project understands exactly how to trigger the automated safety nets for the specific design pattern examples. The project leverages native Python `unittest` discovery executed within a guaranteed `uv` dependency wrapper.

## Prerequisites
Your terminal terminal must be operating from the workspace root:
```bash
cd /Users/aaat/projects/parking-management-system
```

## Running the Complete Suite (All Patterns)

To execute all tests simultaneously (which currently validates Pattern #1 boundaries while guaranteeing no regressions trigger anywhere else), use the discovery flag. This is the single required command to green-light the entire architecture:

```bash
uv run python -m unittest discover tests/
```
Expect output confirming successful discovery: `Ran X tests in Y.YYYs ... OK`.

---

## Pattern-Specific Execution Commands

If an engineer needs to run checks isolated to a specific pattern's behavior during refactoring, they can target individual module files within the `tests/` structure.

### Pattern Example #1 (Strategy Pattern)
The Strategy Pattern governs the allocation behavior spanning the `park` method boundaries. It isolates the EV vs Regular bounds checking logic.

**Target Command:**
```bash
uv run python -m unittest tests/test_park.py
```

### Pattern Example #2 (Observer Pattern)
The Observer Pattern decouples the core `ParkingLot` domain layer from directly updating `tkinter` global states.

*(Note: Once Pattern #2 implementation is physically finalized into a file like `tests/test_observer.py`, the specific check command below acts as the targeted boundary run)*

**Target Command:**
```bash
uv run python -m unittest tests/test_observer.py
```
