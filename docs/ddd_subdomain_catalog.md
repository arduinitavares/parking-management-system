# EasyParkPlus: Subdomain Catalog

This document identifies the supporting and generic subdomains that surround the **Parking Allocation & Resource Management** core domain, enabling the system to scale to multiple facilities and handle specialized hardware.

## 1. Supporting Subdomains
Supporting subdomains are custom-built for the business but do not contain the primary competitive complexity of the core domain.

### Facility Hierarchy Management
- **Business Function:** Models the physical infrastructure of the parking network (Facilities, Floors, specialized Zones).
- **In-Scope:** Defining facility metadata (address, total capacity), floor layouts, and managing the hierarchical relationship between a "Parking Lot" and its sub-sections.
- **Out-of-Scope:** Real-time occupancy tracking (Core Domain logic) and financial asset management of the property.

### EV Charging Station Management
- **Business Function:** Orchestrates the lifecycle of electric vehicle charging hardware.
- **In-Scope:** Charger hardware status (Active/Idle/Fault), charging session telemetry (battery %), and hardware-to-slot mapping.
- **Out-of-Scope:** Energy billing (Generic Subdomain) and the initial allocation of vehicles to EV slots (Core Domain).

---

## 2. Generic Subdomains
Generic subdomains provide common capabilities that can be fulfilled by off-the-shelf software or standard library implementations.

### Identity & Access Management (IAM)
- **Business Function:** Manages system users (Administrators, Attendants) and their permissions.
- **In-Scope:** Authentication, role-based access control (RBAC) to management functions, and user profile management.
- **Out-of-Scope:** Customer/Driver loyalty programs or public-facing user accounts.

### Audit & Activity Logging
- **Business Function:** Provides a historical record of all system state changes for compliance and troubleshooting.
- **In-Scope:** Capturing timestamps and snapshots of allocation events, hardware state changes, and administrative actions.
- **Out-of-Scope:** Real-time analytics or predictive reporting.

### Notification & Messaging
- **Business Function:** Disseminates alerts and internal system updates.
- **In-Scope:** Broadcasting UI updates (Observer implementation), system health alerts, and internal event messaging between subdomains.
- **Out-of-Scope:** Marketing communications or external customer SMS/Email services.
