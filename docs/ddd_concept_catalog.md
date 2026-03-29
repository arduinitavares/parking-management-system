# EasyParkPlus: Concept Catalog (Entities & Value Objects)

This document catalogs the foundational elements of the domain model for the EasyParkPlus Parking Management System. The elements are classified as either **Entities** (objects defined by their identity and lifecycle) or **Value Objects** (immutable objects defined by their attributes and representing descriptive concepts). 

In accordance with architectural boundaries, this document remains implementation-agnostic and explicitly excludes EV Charging domain models.

---

## 1. Parking Allocation Context

The Parking Allocation context handles the dynamic state of vehicle occupancy.

### Entities
*   **Allocation (Aggregate Root)**
    *   *Description:* The core operational entity representing the lifecycle of a vehicle parked in a slot. It has a distinct identity (e.g., a ticket or transaction ID) that persists from check-in to release.
*   **Allocation Slot**
    *   *Description:* Tracks the real-time availability of a parking space. While tied to a physical coordinate, its identity in this context is based on its state machine (Free vs. Occupied).

### Value Objects
*   **Vehicle Profile**
    *   *Description:* An immutable description of the vehicle seeking parking. Contains attributes like Registration Number, Vehicle Type (Car, Motorcycle, EV constraint marker), Make, Model, and Color. 
*   **Slot Status**
    *   *Description:* An immutable enum or state representing the current condition of an Allocation Slot (e.g., `Free`, `Occupied`).
*   **Allocation Timestamp**
    *   *Description:* A precise date/time marker representing either the Check-in event or the Release event.

---

## 2. Facility Management Context

The Facility Management context defines the static physical infrastructure and capacity constraints of the parking network.

### Entities
*   **Facility (Aggregate Root)**
    *   *Description:* A distinct property or building. It has a unique identity (e.g., "Main Downtown Facility") and acts as the root for all physical configuration changes.
*   **Floor Level**
    *   *Description:* A designated elevation within a Facility holding a specific collection of parking bays. It has an identity within the facility (e.g., "Level 1").
*   **Parking Zone**
    *   *Description:* A logical grouping of bays with specific rules or physical traits (e.g., "Motorcycle Area", "EV Capable Area"). 

### Value Objects
*   **Capacity Limit**
    *   *Description:* An immutable integer representing the maximum permitted number of vehicles for a given Facility, Floor Level, or Parking Zone.
*   **Physical Slot Coordinate**
    *   *Description:* The static identifier mapping a specific bay to its location (e.g., "Level 2, Bay 45"). Changing the bay number effectively describes a different physical space.
*   **Facility Address**
    *   *Description:* The geographical location and descriptive metadata of a Facility.

---

## Note on Scope Boundaries
1.  **EV Charging:** The definition of Chargers, Sessions, and Telemetry (Batteries, Voltages) are excluded from this catalog and deferred to the EV Charging Subdomain specification.
2.  **Unconfirmed Capabilities:** Pricing models (e.g., `HourlyRate`), dynamic enforcement (e.g., `PenaltyNotice`), and advanced planning (e.g., `Reservation`) are currently out of scope and omitted from these core definitions.
