# EV Charging Station Management: Subdomain Analysis

## 1. Subdomain Scope Definition
As EasyParkPlus scales toward a multi-facility architecture, the management of specialized physical hardware—specifically Electric Vehicle (EV) chargers—must be explicitly bounded to prevent polluting the Core Domain (Parking Allocation).

### Included in Scope:
- **Charger Status Tracking:** Monitoring the operational availability of a charging station (e.g., Available, Charging, Offline).
- **Session Lifecycles:** Initiating, monitoring the active progress of (e.g., battery percentage markers), and terminating a physical charging event.
- **Hardware Mapping:** Maintaining the relationship between a specific physical charging unit and the physical parking slot it services.

### Excluded from Scope (Out-of-Scope):
- **Resource Allocation Rules:** The decision of *which* vehicle is allowed to enter the physical EV parking bay remains strictly within the Core Domain (Parking Allocation & Resource Management).
- **Billing and Energy Pricing:** Metering energy costs, executing financial transactions for power consumed, or fluctuating power grid pricing algorithms.
- **Third-Party Grid Orchestration:** External load-balancing negotiations with municipal power grids.

## 2. Subdomain Classification Rationale
**Classification: Supporting Subdomain**

While EV Charging is heavily featured in the product vision and presents a significant differentiator from legacy parking systems, it is ultimately a **Supporting Subdomain** rather than the Core Domain. 
- **Business Value:** The facility's primary business driver is the orchestration of parking space. EV charging is a highly valuable *amenity* attached to that space, but the system must still function perfectly for standard vehicles without it.
- **Complexity:** The logic required to track an ongoing charge session is standard telemetry. It does not carry the deep, competitive algorithmic complexity found in the Core Domain's multi-facility capacity and allocation routers.

## 3. Integration Points with the Core Domain
The EV Charging Subdomain cannot operate in isolation; it must communicate precisely with the Core Domain (Parking Allocation) while respecting strict boundaries.

- **Slot State Synchronization:** When the Core Domain officially allocates an EV to a parking bay, it must emit an event indicating the bay is now occupied by a valid entity. The EV Subdomain listens for this event to unlock or prepare the associated charging hardware.
- **Session Yielding:** Upon completion of a charge or the physical departure of the vehicle, the EV Subdomain notifies the Core Domain that the session has concluded, allowing the Core Domain to evaluate if the physical slot should be cleared or flagged for an overstay.
- **Boundary Enforcement:** The EV Subdomain dictates *charging state* (e.g., "Vehicle battery is at 80%"), while the Core Domain dictates *occupancy state* (e.g., "Slot 4 is occupied by RegNum XYZ").
