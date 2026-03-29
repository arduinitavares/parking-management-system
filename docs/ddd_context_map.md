# EasyParkPlus: Bounded Context Map

This diagram illustrates the high-level integration relationships between the Bounded Contexts identified in the EasyParkPlus Domain-Driven Design analysis. The map highlights conceptual collaborations and data dependencies, purposefully excluding technical deployment details, database schemas, or specific API endpoints.

```mermaid
flowchart TD
    %% Core Domain Definition
    Core[("Parking Allocation Context\n(Core Domain)")]

    %% Supporting Subdomains Definitions
    Facility["Facility Management Context\n(Supporting)"]
    EV["EV Charging Context\n(Supporting)"]

    %% Generic Subdomains Definitions
    IAM["IAM Context\n(Generic)"]
    Audit["Audit & Logging Context\n(Generic)"]
    Notify["Notification Context\n(Generic)"]

    %% Core Business Integration Relationships
    Facility -- "Defines physical topology\n[Upstream]" --> Core
    Core -- "Authorizes vehicle slot occupancy\n[Upstream]" --> EV
    EV -- "Reports hardware charge status\n[Downstream]" --> Core

    %% Generic Cross-Cutting Concerns
    IAM -. "Enforces access roles" .-> Facility
    IAM -. "Enforces access roles" .-> Core

    Core -. "Logs state mutations" .-> Audit
    Facility -. "Logs configuration changes" .-> Audit
    EV -. "Logs session telemetry" .-> Audit
    
    Core -. "Broadcasts occupancy events" .-> Notify
    EV -. "Broadcasts hardware faults" .-> Notify

    classDef core fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef support fill:#cce5ff,stroke:#007bff,stroke-width:2px;
    classDef generic fill:#f8d7da,stroke:#dc3545,stroke-width:1px;

    class Core core;
    class Facility,EV support;
    class IAM,Audit,Notify generic;
```

### Context Integration Summary
- **Facility Management -> Parking Allocation:** Facility defined parameters (like total EV capacities and floor counts) act as the foundational upstream data dependency that restricts the mathematical rules of the Parking Allocation context.
- **Parking Allocation <-> EV Charging:** A bidirectional relationship exists where Parking Allocation dictates *who* is allowed in an EV slot (Upstream Authorization), while EV Charging continuously reports *what* is happening at the hardware level back to the core system (Downstream Telemetry).
- **Generic Dependencies:** The IAM, Audit, and Notification generic domains act as cross-cutting infrastructural companions. Operations across the distinct supporting and core boundaries rely natively on these contexts for unified security, legal audit tracking, and system-wide visibility.
