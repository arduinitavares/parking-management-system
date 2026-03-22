# Anti-Pattern Catalog

This catalog documents the code smells and anti-patterns identified during the baseline codebase health assessment of the Parking Lot Manager prototype. The findings are categorized according to standard software engineering anti-patterns and include an impact analysis and remediation strategy to guide future refactoring efforts.

**References:**
- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Suryanarayana, G., Samarthyam, G., & Sharma, T. (2014). *Refactoring for Software Design Smells*. Morgan Kaufmann.

---

## 1. Improper Inheritance (Broken Object-Oriented Design)
**Location:** `ElectricVehicle.py` (Lines 23-32, `class ElectricCar` and `class ElectricBike`)
- **Description:** The `ElectricCar` and `ElectricBike` classes call `ElectricVehicle.__init__(self, ...)` in their constructors but do *not* actually inherit from the `ElectricVehicle` base class (e.g., they are defined as `class ElectricCar:` instead of `class ElectricCar(ElectricVehicle):`). Additionally, in `Vehicle.py`, derived classes use explicit base class naming instead of the Pythonic `super()`.
- **Why it is an anti-pattern:** It breaks fundamental Object-Oriented polymorphism. The subclasses are not recognized as instances of the base class by the interpreter (`isinstance` will fail).
- **Impact:** **Defect Risk / Maintainability**. Causes brittle code where shared behaviors won't correctly propagate, leading to severe architectural failures when type-checking or interfacing with polymorphic collections.
- **Remediation:** Conceptually, explicitly declare the inheritance in the class definition and use `super().__init__(...)` to handle base class initialization robustly.
- **Severity:** 🔴 CRITICAL

## 2. Global Variables
**Location:** `ParkingManager.py` (Lines 6-26, Module level)
- **Description:** Extensive use of global variables for Tkinter GUI state (`root`, `command_value`, `num_value`, `ev_value`, etc.) tightly coupled to the top-level of the file.
- **Why it is an anti-pattern:** Global state makes the application state unpredictable, difficult to trace, and nearly impossible to unit test effectively. It tightly couples the domain logic with a specific GUI implementation.
- **Impact:** **Maintainability**. Any part of the application can mutate these variables, leading to hidden side effects and making future UI/Backend decoupling very difficult. 
- **Remediation:** Encapsulate the GUI state within a dedicated UI class or module, passing references to the backend domain models only when required.
- **Severity:** 🟠 HIGH

## 3. Superfluous / Lengthy / Nested Conditional Statements
**Location:** `ParkingManager.py` (Lines 65-87, `park()` method)
- **Description:** The `park()` method contains overly nested `if-else` blocks (up to three levels deep) handling branch logic for different vehicle types and capacity constraints.
- **Why it is an anti-pattern:** Deep nesting increases the cyclomatic complexity of a function. It forces the developer to hold too much context in their head to understand under what precise conditions a block of code executes.
- **Impact:** **Readability / Defect Risk**. Modifying deeply nested code frequently introduces subtle logical bugs and regressions.
- **Remediation:** Apply the "Guard Clauses" pattern (early returns) to flatten conditionals, or extract the varied parking logic out to behavior-specific methods or utilize a behavioral Design Pattern like Strategy or State.
- **Severity:** 🟠 HIGH

## 4. Poor / Non-explicit Variable Names (Defect Causing)
**Location:** `ParkingManager.py` (Lines 233-253, `getSlotNumFromMakeEv()` and `getSlotNumFromModelEv()`)
- **Description:** The method `getSlotNumFromMakeEv(self, color)` accepts an argument named `color`, but the internal logic attempts to lookup `self.evSlots[i].make == make` and `self.evSlots[i].model == model`, both of which are referencing undefined variables because of copy-paste mismanagement. Also heavily uses single-letter vars (`i`, `slots`) and abbreviations (`ev`, `motor`).
- **Why it is an anti-pattern:** Variable names do not express their intent. In this case, mismatched identifiers actually hide a runtime exception (`NameError`).
- **Impact:** **Defect Risk / Readability**. The discrepancies obscure intent and literally break the application runtime when these specific execution paths are evaluated.
- **Remediation:** Rename variables to explicitly state their domain meaning (e.g., `is_electric_vehicle`, `vehicle_make`). Fix parameter signatures to accurately match the consumed variables.
- **Severity:** 🔴 CRITICAL

## 5. Dead Code / Unnecessary Abstractions
**Location:** `Vehicle.py` (Lines 27-45, `class Truck` and `class Bus`)
- **Description:** The `Truck` and `Bus` objects are fully defined but never initialized, referenced, or utilized anywhere in the prototype parking manager logic.
- **Why it is an anti-pattern:** Code that does not execute adds meaningless bulk to the cognitive load of a maintainer reading the file. 
- **Impact:** **Maintainability / Readability**. Over time, dead code rots and confuses engineers trying to establish the boundaries of an application's required feature set.
- **Remediation:** Remove unused classes entirely unless there is a concrete, impending feature requirement, in which case they should be documented as WIP.
- **Severity:** 🟡 MEDIUM

## 6. Returning Different Types / Unreachable Code
**Location:** `ParkingManager.py` (Lines 113-115, `edit()` method)
- **Description:** The `edit()` block contains two sibling `if` logic evaluations that both explicitly `return True`. The immediate next line falls to `return False`, which physically cannot be reached. 
- **Why it is an anti-pattern:** Having isolated code paths that are logically impossible to enter creates confusion. Furthermore, designing operations that fail silently or ambiguously return boolean constants instead of error tracking masks systemic failures.
- **Impact:** **Maintainability**. Misleads developers about the possible return signatures of the function.
- **Remediation:** Clean up redundant conditional pathways. Consider throwing an explicit Exception to represent a failed edit instead of mixing boolean return types on domain mutations.
- **Severity:** 🟡 MEDIUM

## 7. Clumsy, Unnecessary Loop Statements
**Location:** `ParkingManager.py` (Lines 149-179, multiple `getSlotNumFromX` methods)
- **Description:** Loops frequently utilize an inverted continuation pattern: `if (self.slots[i] != -1): [do stuff]; else: continue`.
- **Why it is an anti-pattern:** The `continue` statement is explicitly useless syntactic noise here, as the loop would naturally advance anyway since there is no logic following the block.
- **Impact:** **Readability**. Verbose loops obscure the primary filtering or searching operations they are meant to perform.
- **Remediation:** Restructure iterators to cleanly check truthiness (e.g., `if self.slots[i] != -1:` and process) without writing the explicit `else: continue` fallback.
- **Severity:** 🟡 MEDIUM

## 8. Lack of Comments or Useless Comments
**Location:** Across all files (e.g., `Vehicle.py`, `ElectricVehicle.py`)
- **Description:** Total absence of class and method docstrings. The few comments that do exist (e.g., `#Parking Lot class`) state the obvious.
- **Why it is an anti-pattern:** While code should be self-documenting, the complete omission of API docstrings in shared entity classes obscures expected behaviors—especially data types constraint details or required invariants (e.g. what scale does `setCharge()` expect?).
- **Impact:** **Maintainability**. Lengthens onboarding time and increases the likelihood of developer error when consuming poorly described methods.
- **Remediation:** Add concise Python docstrings to all methods detailing parameter constraints, side effects, and expected return types. 
- **Severity:** 🟡 MEDIUM