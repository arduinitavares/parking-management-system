# Repository Pattern Design: Data Access Abstraction

This document outlines the architectural design for decoupling data persistence within the EasyParkPlus Parking Management System. The goal is to replace the hardcoded integer/list arrays currently managing vehicle states with formal Repository interfaces.

## 1. Generic Repository Interface Definition

The `Repository[T, ID]` generic interface establishes a strict contract for data access operations, ensuring that the core business domain logic operates identically regardless of the underlying storage mechanism (in-memory arrays vs. a future external database).

### Generic CRUD Operations
- `add(record_id: ID, entity: T) -> None`
- `get(record_id: ID) -> T`
- `update(record_id: ID, entity: T) -> None`
- `remove(record_id: ID) -> None`

### Generic Query Specifications
- `find_by(**kwargs: Any) -> list[T]`

## 2. Entity-Specific Repository Mapping

Currently, the `ParkingLot` object holds two monolithic lists (`self.slots` and `self.ev_slots`) that pre-allocate empty integers (`-1`) which are replaced by domain objects (`Vehicle` or `ElectricVehicle`).

To implement the Repository pattern, we will consolidate these into explicit storage managers:

- **`VehicleRepository(Repository)`**
  - **Entity**: `Vehicle` (and its subclasses representing standard allocations)
  - **Record ID**: The assigned slot number (e.g., Integer converted to a String) or naturally the vehicle's registration number. For alignment with the current codebase's logic structure, we will map standard vehicles into this repository using their slot bounds context.

- **`EVRepository(Repository)`**
  - **Entity**: `ElectricVehicle` (and its subclasses)
  - **Record ID**: Inherently maps the slot allocation. 

### Implementation Strategy
Rather than allocating `[-1] * capacity` as an exact list structure, the new context will store active models dynamically. The `ParkingLot` will rely on `len(repository._store)` to evaluate current capacity dynamically rather than maintaining raw counters (`num_of_occupied_slots`).

## 3. Query Specification Pattern

The current data query methods inside `ParkingLot` (`get_slot_nums_from_color`, etc.) are coupled directly to inspecting the explicit list loop iterators.

By utilizing the `find_by(**kwargs)` layer explicitly defined in the `Repository` abstract base, complex queries resolve naturally via dynamic trait mapping:

```python
# Instead of manual loops:
def get_reg_nums_from_color(self, color: str) -> list[str]:
    regular_vehicles = self.vehicle_repo.find_by(color=color)
    ev_vehicles = self.ev_repo.find_by(color=color)
    return [v.regnum for v in regular_vehicles + ev_vehicles]
```

This ensures that the business constraints (like evaluating color matches) are evaluated universally downstream dynamically, removing the need for duplicate hardcoded loops as the dataset schema expands.

## Impact
This transition guarantees that the underlying `ParkingLot` logic will no longer require knowledge of how variables are physically persisted or retrieved, delegating all responsibility entirely to the independent Repository implementation mapped by the Dependency Injection framework.
