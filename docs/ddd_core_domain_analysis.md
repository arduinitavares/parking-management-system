# EasyParkPlus: Core Domain Analysis

## 1. Business Requirements and Value Drivers
EasyParkPlus is evolving from a fragile, single-lot prototype into an extensible, multi-facility parking application. Based on the product vision, the primary business value operators driving this architectural transformation are:
- **Scalability:** The ability to orchestrate parking logistics across multiple, geographically separated facilities rather than a single theoretical floor constraint.
- **Resource Optimization:** Dynamically differentiating physical resource types (e.g., standard bays versus Electric Vehicle charging bays) and efficiently assigning varying vehicle profiles (Cars, Motorcycles, EVs) against those physical assets.
- **Predictability & State Consistency:** Establishing reliable occupancy states so that external components or business scaling operations (like deploying additional charging equipment) can rely on a pristine source of truth.

## 2. Highest-Value Business Capabilities
To deliver on those value drivers, the system's most competitive business asset is its native capability to accurately map finite physical space to transient vehicles in real-time. The highest-value operations are:
- Evaluating facility capacity against incoming live parking requests.
- Processing the safe assignment and eventual yielding of slots by users.
- Managing differing rulesets based on vehicle and slot categorizations (e.g., preventing combustion engine cars from consuming EV infrastructure).

## 3. Core Domain Selection Rationale
Based on the analysis, the foundational **Core Domain** of the EasyParkPlus System is **Parking Allocation & Resource Management**.

### Rationale
- **It embodies the primary competitive advantage:** Accurately navigating the complexities of multi-floor, multi-facility, and multi-vehicle-type routing is the central mechanism distinguishing EasyParkPlus from simple static inventory programs. 
- **It is the most complex business logic:** As evidenced by the earlier Strategy anti-pattern cleanups, the logic governing *who* can park *where*, and under what constraint flags, dictates the entire flow of the application.
- **Extensibility bounds:** The entire system relies on the core slot state. Secondary features—such as tracking EV charging metrics or monitoring multi-facility networks—all depend exclusively on the foundational allocation state existing cleanly as the system's master "source of truth."

> **Note on Assumptions:** In alignment with current system boundaries, external business processes commonly associated with commercial facility logistics—such as pre-event reservations, dynamic pricing, and penalty enforcement mechanisms—are actively deemed **out-of-scope** constraints at this development phase, ensuring the domain boundary focuses purely on resource state execution.
