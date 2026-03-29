# Term Disambiguation Log: EasyParkPlus Domain

This document records the formal semantic disambiguation decisions for terms that overlap across the EasyParkPlus Bounded Contexts. These decisions ensure that developers and stakeholders interpret the language accurately based on the context in which a term is used.

## 1. Term: "Slot"
Overlapping Contexts: **Parking Allocation** vs. **Facility Management**

| Context | Semantic Meaning | Disambiguation Decision |
| :--- | :--- | :--- |
| **Parking Allocation** | A stateful unit of availability (Occupied/Free). | **Standardize as "Allocation Slot"** when referring to the state machine in technical discussion. |
| **Facility Management** | A static physical location or coordinate (Floor 1, Bay 10). | **Standardize as "Physical Slot"** when referring to topological metadata. |

---

## 2. Term: "EV Vehicle"
Overlapping Contexts: **Parking Allocation** vs. **EV Charging**

| Context | Semantic Meaning | Disambiguation Decision |
| :--- | :--- | :--- |
| **Parking Allocation** | A set of allocation constraints (is it allowed in this zone?). | **Standardize as "EV Constraint Profile"** in business logic. |
| **EV Charging** | A physical battery requiring active session management (is it drawing power?). | **Standardize as "Charging Target"** during telemetry discussions. |

---

## 3. Term: "Status"
Overlapping Contexts: **Parking Allocation** vs. **EV Charging** vs. **Audit & Logging**

| Context | Semantic Meaning | Disambiguation Decision |
| :--- | :--- | :--- |
| **Parking Allocation** | Global occupancy read-outs (Capacity % used). | **Standardize as "Inventory Status"**. |
| **EV Charging** | Real-time hardware health (Online/Faulted). | **Standardize as "Diagnostic Status"**. |
| **Audit & Logging** | The historical confirmation of a recorded event. | **Standardize as "Event Integrity"**. |

---

## 4. Term: "Level"
Overlapping Contexts: **Facility Management** vs. **EV Charging**

| Context | Semantic Meaning | Disambiguation Decision |
| :--- | :--- | :--- |
| **Facility Management** | A physical floor elevation (e.g., Level 1, Level 2). | **Maintain as "Floor Level"**. |
| **EV Charging** | The energy percentage in a physical battery (e.g., 80%). | **Standardize as "Charge Percentage"** to prevent collision with floor logic. |

---

## 5. Synonyms & Standardization Decisions
The following terms were identified as synonyms for the same business concept and have been standardized across **all** contexts:

- **"Bay" / "Space" -> Standardized Term: "Slot"**
- **"Floor" / "Elevation" -> Standardized Term: "Level"**
- **"RegNum" / "Plate" -> Standardized Term: "Registration Number"**
- **"Floor Plan" / "Layout" -> Standardized Term: "Topology"**
