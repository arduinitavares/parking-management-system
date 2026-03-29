# EasyParkPlus: Subdomain Scope Definitions

This document provides formal scope statements for each subdomain identified in the EasyParkPlus Parking Management System. These statements are written in business/domain language to facilitate stakeholder alignment and ensure clear boundaries for future microservices development.

---

## 1. Core Domain: Parking Allocation & Resource Management
**Strategic Purpose:** Efficiently mapping physical slots to vehicles across multiple levels and facilities.

| Business Function | Inclusion Statement | Exclusion Statement |
| :--- | :--- | :--- |
| **Space Inventory** | Continuous tracking of occupied vs. free slots across facilities. | Managing property lease or site maintenance documents. |
| **Allocation Logic** | Decisions on where a vehicle can park based on vehicle type and slot availability. | Pre-booking or advance reservation of specific bays. |
| **Occupancy State** | Handling the "Check-in" (Entry) and "Check-out" (Exit) lifecycle of a vehicle-slot binding. | Financial transaction processing or payment collection. |

---

## 2. Supporting Subdomain: Facility Hierarchy Management
**Strategic Purpose:** Defining the physical structure and organization of the parking facilities.

| Business Function | Inclusion Statement | Exclusion Statement |
| :--- | :--- | :--- |
| **Facility Modeling** | Creating and storing metadata for specific facilities (address, operating hours, floor counts). | Real-time monitoring of people or objects inside a facility. |
| **Physical Topology** | Mapping the layout of floors, zones (e.g., Premium, EV, Motorcycle), and bay numbers. | Tracking the specific vehicle occupying a bay at any given time. |

---

## 3. Supporting Subdomain: EV Charging Station Management
**Strategic Purpose:** Orchestrating and monitoring specialized hardware for electric vehicle services.

| Business Function | Inclusion Statement | Exclusion Statement |
| :--- | :--- | :--- |
| **Charger Telemetry** | Reading hardware status (online/offline) and session energy delivery (completion %). | Managing energy utility contracts or grid-load balancing. |
| **Hardware Binding** | Defining which specific physical slot is powered by which charging unit. | Enforcing if a vehicle *should* be allowed to enter the EV slot. |

---

## 4. Generic Subdomain: Identity & Access Management (IAM)
**Strategic Purpose:** Securing system access and managing administrative roles.

| Business Function | Inclusion Statement | Exclusion Statement |
| :--- | :--- | :--- |
| **Staff Authentication** | Verifying identity for Facility Managers, Attendants, and IT Support. | Managing consumer/end-user account profiles or loyalty logs. |
| **Authorization** | Defining role-based permissions to execute administrative actions (e.g., "Create Lot"). | Storing non-access related personnel data (e.g., HR records). |

---

## 5. Generic Subdomain: Audit & Activity Logging
**Strategic Purpose:** Maintaining an immutable transaction trail for behavioral compliance.

| Business Function | Inclusion Statement | Exclusion Statement |
| :--- | :--- | :--- |
| **System Event Log** | Capturing state changes across subdomains with precise timestamps for troubleshooting. | Managing legal compliance documentation or long-term financial audits. |
| **Data Provenance** | Tracking "who" performed a change to a facility configuration or allocation state. | Providing real-time dashboard analytics or business intelligence reports. |

---

## 6. Generic Subdomain: Notification & Messaging
**Strategic Purpose:** Harmonizing cross-domain communication and internal system updates.

| Business Function | Inclusion Statement | Exclusion Statement |
| :--- | :--- | :--- |
| **System Broadcasts** | Relaying internal events between subdomains and the presentation layer. | Sending customer-facing promotional emails or SMS notifications. |
| **Operational Alerts** | Notifying personnel of critical hardware faults or system-level anomalies. | Providing general customer support help-desk functionality. |
