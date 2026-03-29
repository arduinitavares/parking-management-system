# Execution Evidence: Demonstration Scenarios

This document outlines the standard operating procedures required to validate the core functionality of the EasyParkPlus Parking Management System. Evaluation scenarios are designed to confirm architectural parity and demonstrate the successful integration of the Strategy, Repository, and Observer design patterns.

---

## Phase 1: Lot Initialization
**Objective:** Validate system capacity configuration and multi-type vehicle environment bootstrapping.
1. **Inputs Configuration:**
   - Number of Regular Spaces: `2`
   - Number of EV Spaces: `1`
   - Floor Level: `1`
2. **Operation:** Execute the **"Create Parking Lot"** command.
3. **Validation Criteria:** The system interface must broadcast confirmation: *"Created a parking lot with 2 regular slots and 1 ev slots on level: 1"*, confirming the Observer pattern successfully updated the view.

---

## Phase 2: Multi-Type Vehicle Parking (Strategy Pattern Validation)
**Objective:** Verify that the system transparently routes incoming vehicles to the correct sub-domain repositories using the implemented allocation strategies.
1. **Scenario 2A (Regular Combustion Vehicle):**
   - Make: `Toyota` | Model: `Camry` | Color: `Red` | Reg #: `REG-001`
   - Execute **"Park Car"**. 
   - *Confirmation:* System allocates Slot #1 in the Standard Repository.
2. **Scenario 2B (Electric Vehicle):**
   - Make: `Tesla` | Model: `Model 3` | Color: `White` | Reg #: `EV-999`
   - Activate **"Electric"** toggle.
   - Execute **"Park Car"**. 
   - *Confirmation:* System allocates Slot #1 in the EV Repository (verifying independent index paths).
3. **Scenario 2C (Regular Motorcycle):**
   - Make: `Honda` | Model: `CBR600` | Color: `Black` | Reg #: `MOTO-50`
   - Activate **"Motorcycle"** toggle (Deactivate "Electric").
   - Execute **"Park Car"**. 
   - *Confirmation:* System allocates Slot #2 in the Standard Repository.

---

## Phase 3: Status & Search Operations (Repository Query Validation)
**Objective:** Demonstrate accurate data retrieval capabilities across disparate data models.
1. **Global Occupancy Check:** Execute **"Current Lot Status"**. 
   - *Confirmation:* The output interface successfully segregates and lists both Regular and EV tracking tables.
2. **Deterministic Lookup (Registration ID):** 
   - Field Input: `EV-999` (in the Registration # search prompt).
   - Execute **"Get Slot ID by Registration #"**. 
   - *Confirmation:* System returns identification for Slot 1.
3. **Categorical Lookup (Color Grouping):**
   - Field Input: `Red`
   - Execute **"Get Slot ID by Color"**. 
   - *Confirmation:* System returns identification for Slot 1.
4. **Subsequent Categorical Lookup:**
   - Field Input: `Black` (replacing previous entry).
   - Execute **"Get Slot ID by Color"**. 
   - *Confirmation:* System dynamically retrieves Slot 2, proving the persistence query boundaries operate accurately over time.

---

## Phase 4: EV Domain Specification
**Objective:** Verify EV-specific attributes are persistently decoupled from the standard vehicle models.
1. **Operation:** Execute **"EV Charge Status"**.
2. **Validation Criteria:** The output explicitly lists the Tesla vehicle (`EV-999`) and displays the battery parameter initialized to standard properties (`0%`).

---

## Phase 5: Removal & Capacity Governance
**Objective:** Validate state mutation algorithms and rigorous boundary conditions when deallocating.
1. **Deallocation Process:**
   - Field Input: `1` (in the Slot # prompt).
   - Ensure "Remove EV?" is deactivated.
   - Execute **"Remove Car"**.
2. **State Validation:** Execute **"Current Lot Status"** to confirm Slot #1 has been purged from active tracking.
3. **Hard Constraint Validation (Full Lot Handling):**
   - Attempt to park an additional regular vehicle.
   - *Confirmation:* Because the two regular slots are now fully populated by other vehicles (assuming another was added), the system must intercept the command and gracefully log: *"Sorry, parking lot is full"*, proving out-of-bounds errors are caught by the Strategy constraints.
