# Anti-Pattern Catalog

This catalog records the anti-patterns that are verifiably present in the current Parking Lot Manager prototype. Each entry is tied to a precise source location and includes a minimal reproducible example, the local impact on this codebase, and a conceptual remediation path for later refactoring work. Where a finding maps cleanly to `docs/master_anti_pattern_catalog.md`, the canonical anti-pattern name and normalized severity are used.

## Coverage Note

The codebase was checked against the assignment's example anti-pattern categories by reviewing `ParkingManager.py`, `Vehicle.py`, and `ElectricVehicle.py`. The entries below cover only issues that are observable in the current prototype. `try/except` misuse, broad imports in the `from module import *` or `import *` sense, and passing mutable arguments were not observed in the current code.

## References

The explanations below paraphrase general guidance from these sources rather than reproducing them verbatim:

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Suryanarayana, G., Samarthyam, G., & Sharma, T. (2014). *Refactoring for Software Design Smells*. Morgan Kaufmann.

## 1. Broken Inheritance / Incorrect OO Reuse

- **Category:** Broken inheritance / incorrect OO reuse
- **Severity:** Critical
- **Source location:** `ElectricVehicle.py`, `class ElectricCar` (lines 28-33) and `class ElectricBike` (lines 36-40)
- **Minimal reproducible example:**

```python
from ElectricVehicle import ElectricVehicle, ElectricCar

car = ElectricCar("ABC123", "Tesla", "Model 3", "red")

print(hasattr(car, "charge"))              # True
print(isinstance(car, ElectricVehicle))    # False
```

- **Why this is an anti-pattern here:** `ElectricCar` and `ElectricBike` call `ElectricVehicle.__init__` directly, but neither class actually inherits from `ElectricVehicle`. That copies state into the object without making it part of the EV type hierarchy, so polymorphic checks and shared behavior contracts break immediately.
- **Impact:** High defect risk and maintainability cost. Future EV-specific logic such as charging workflows, shared validation, or typed collections can behave incorrectly because these objects are not recognized as `ElectricVehicle` instances.
- **Recommended remediation:** Declare the inheritance explicitly and use `super().__init__(...)` so EV subclasses participate in the real class hierarchy instead of manually borrowing base initialization code.

## 2. Layering Violations / Layer Skipping

- **Category:** Architecture Anti-Patterns
- **Severity:** High
- **Source location:** `ParkingManager.py`, module-level GUI state (lines 6-29); consumed from `status` (lines 117-145), `chargeStatus` (lines 136-145), `slotNumByReg` (lines 248-260), `slotNumByColor` (lines 262-268), `regNumByColor` (lines 270-276), and `main` (lines 300-410)
- **Minimal reproducible example:**

```python
import tkinter as tk

root = tk.Tk()
num_value = tk.StringVar()
ev_car_value = tk.IntVar()
tfield = tk.Text(root, width=70, height=15)

class ParkingLot:
    def status(self):
        tfield.insert(tk.INSERT, "Vehicles\n")
```

- **Why this is an anti-pattern here:** The parking domain code bypasses a clean presentation-to-domain boundary and reaches directly into Tkinter state. `ParkingLot` methods read shared `StringVar` and `IntVar` values and write directly to `tfield`, so the domain layer is coupled to GUI concerns instead of receiving plain inputs and returning plain results.
- **Impact:** Lowers testability and maintainability. The parking logic cannot be reused without the GUI globals, and replacing or restructuring the UI requires changes inside domain methods.
- **Recommended remediation:** Encapsulate Tkinter widgets and form state inside a UI/controller class, and pass only the required domain inputs into `ParkingLot` methods instead of reading and writing module-level state directly.

## 3. Overly Nested Conditionals

- **Category:** Superfluous / lengthy / nested conditional statements
- **Severity:** High
- **Source location:** `ParkingManager.py`, `ParkingLot.park` (lines 64-89)
- **Minimal reproducible example:**

```python
def park(self, regnum, make, model, color, ev, motor):
    if self.numOfOccupiedEvSlots < self.evCapacity or self.numOfOccupiedSlots < self.capacity:
        slotid = -1
        if ev == 1:
            if self.numOfOccupiedEvSlots < self.evCapacity:
                slotid = self.getEmptyEvSlot()
                if motor == 1:
                    self.evSlots[slotid] = ElectricVehicle.ElectricBike(regnum, make, model, color)
                else:
                    self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum, make, model, color)
        else:
            if self.numOfOccupiedSlots < self.capacity:
                slotid = self.getEmptySlot()
                if motor == 1:
                    self.slots[slotid] = Vehicle.Car(regnum, make, model, color)
                else:
                    self.slots[slotid] = Vehicle.Motorcycle(regnum, make, model, color)
```

- **Why this is an anti-pattern here:** One method mixes capacity checks, EV routing, vehicle-type branching, slot lookup, slot assignment, and counter updates in one nested control structure. The logic is hard to scan and requires the reader to keep multiple state conditions in mind at once.
- **Impact:** Increases defect risk and makes modifications harder. Small behavioral changes, such as adding new vehicle categories or adjusting capacity rules, are more likely to introduce regressions because the method is already cognitively dense.
- **Recommended remediation:** Flatten the control flow with guard clauses and split the responsibilities into smaller helper methods or strategy-like branches for regular versus electric parking paths.

## 4. Duplicated Code

- **Category:** Code-Level Anti-Patterns
- **Severity:** High
- **Source location:** `ParkingManager.py`, `getSlotNumFromColor` (lines 166-174), `getSlotNumFromMake` (lines 176-184), `getSlotNumFromModel` (lines 186-194), `getSlotNumFromColorEv` (lines 218-226), `getSlotNumFromMakeEv` (lines 228-236), and `getSlotNumFromModelEv` (lines 238-246)
- **Minimal reproducible example:**

```python
def getSlotNumFromMake(self, make):
    slotnums = []
    for i in range(len(self.slots)):
        if self.slots[i] == -1:
            continue
        if self.slots[i].make == make:
            slotnums.append(str(i + 1))
    return slotnums

def getSlotNumFromMakeEv(self, color):
    slotnums = []
    for i in range(len(self.evSlots)):
        if self.evSlots[i] == -1:
            continue
        if self.evSlots[i].make == make:
            slotnums.append(str(i + 1))
    return slotnums
```

- **Why this is an anti-pattern here:** The regular-slot and EV-slot lookup helpers are near-copy clones that differ mainly by collection name and attribute. Those clones have already drifted: `getSlotNumFromMakeEv` compares against undefined `make`, and `getSlotNumFromModelEv` similarly uses undefined `model`. The copy-paste defect is a symptom of the broader duplication.
- **Impact:** Immediate runtime defect risk and higher maintenance cost. Every lookup change has to be repeated across parallel methods, which makes inconsistent behavior and missed fixes more likely.
- **Recommended remediation:** Extract shared slot-search helpers that accept a slot collection and predicate or attribute name, then reuse them for regular and EV lookups. Add focused tests for each lookup path to catch divergence early.

## 5. Dead Code / Unused Abstractions

- **Category:** Dead code / unnecessary abstractions
- **Severity:** Medium
- **Source location:** `Vehicle.py`, `class Truck` (lines 29-35) and `class Bus` (lines 47-53); `ParkingManager.py`, `getEmptyLevel` (lines 60-62) and `edit` (lines 107-115)
- **Minimal reproducible example:**

```python
class Truck(Vehicle):
    def __init__(self, regnum, make, model, color):
        Vehicle.__init__(self, regnum, make, model, color)

    def getType(self):
        return "Truck"

def edit(self, slotid, regnum, make, model, color, ev):
    if ev == 1:
        self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum, make, model, color)
        return True
    else:
        self.slots[slotid] = Vehicle.Car(regnum, make, model, color)
        return True
```

- **Why this is an anti-pattern here:** These symbols are defined, but they are not part of the active prototype flow. No code instantiates `Truck` or `Bus`, the GUI exposes no edit action, and `getEmptyLevel` is likewise unused. An additional smaller instance of the same smell is the unused `sys` import at `ParkingManager.py` line 3.
- **Impact:** Inflates the maintenance surface and blurs the actual scope of the prototype. Future readers must spend time deciding whether these paths are intentional features, abandoned work, or required behavior.
- **Recommended remediation:** Remove or quarantine unused code until a real feature requires it, or document it explicitly as planned future scope outside the active prototype path.

## 6. Returning Different Types / Implicit `None` Contract

- **Category:** Returning different types in a function
- **Severity:** Medium
- **Source location:** `ParkingManager.py`, `getEmptySlot` (lines 50-53), `getEmptyEvSlot` (lines 55-58), and `getEmptyLevel` (lines 60-62)
- **Minimal reproducible example:**

```python
def getEmptySlot(self):
    for i in range(len(self.slots)):
        if self.slots[i] == -1:
            return i
    # falls through and returns None

def getEmptyLevel(self):
    if self.numOfOccupiedEvSlots == 0 and self.numOfOccupiedSlots == 0:
        return self.level
    # falls through and returns None
```

- **Why this is an anti-pattern here:** These helpers return an `int` on success and implicitly return `None` otherwise, but the contract is not stated anywhere in the API. Callers have to infer the failure mode from the implementation, and the three helpers do not communicate that they are partial lookups rather than guaranteed value providers.
- **Impact:** Raises defect risk and makes behavior harder to reason about. A caller can easily treat the result as an integer and fail later with a confusing error, especially if future refactoring changes when these helpers are called.
- **Recommended remediation:** Make the return contract explicit by documenting or annotating `Optional[int]`, or replace the implicit `None` path with a clearer domain-specific failure signal that callers must handle deliberately.

## 7. Clumsy Loop Statements / Redundant `continue`

- **Category:** Clumsy, unnecessary loop statements
- **Severity:** Low
- **Source location:** `ParkingManager.py`, `status` (lines 117-145), `chargeStatus` (lines 136-145), `getSlotNumFromRegNum` (lines 157-164), and `getSlotNumFromRegNumEv` (lines 208-216)
- **Minimal reproducible example:**

```python
for i in range(len(self.slots)):
    if self.slots[i] != -1:
        output = str(i + 1)
        tfield.insert(tk.INSERT, output)
    else:
        continue
```

- **Why this is an anti-pattern here:** The `continue` branch adds noise without changing behavior because the loop would advance naturally after the `if` block anyway. The same pattern appears in multiple search and reporting methods, which makes simple loops look more complex than they are.
- **Impact:** Primarily hurts readability. Redundant control-flow statements make the code harder to skim and reinforce a verbose style in already repetitive methods.
- **Recommended remediation:** Remove redundant `else: continue` branches and keep only the positive condition, or iterate directly over filtered slot values when that better matches the intent.

## 8. Lack of Comments / Docstrings and Low-Value Comments

- **Category:** Lack of comments or useless comments
- **Severity:** Low
- **Source location:** `Vehicle.py`, public classes and methods (lines 1-53); `ElectricVehicle.py`, public classes and methods (lines 1-40); `ParkingManager.py`, `#Parking Lot class` comment (line 31)
- **Minimal reproducible example:**

```python
#Parking Lot class
class ParkingLot:
    def status(self):
        ...

class Vehicle:
    def getMake(self):
        return self.make
```

- **Why this is an anti-pattern here:** The one comment shown above only restates the obvious, while the public classes and methods across the prototype have no docstrings describing expectations, side effects, or domain intent. The result is a mismatch between low-value commentary and missing useful documentation.
- **Impact:** Slows onboarding and maintenance. Readers must infer basic behavior, assumptions, and invariants from implementation details instead of from concise API-level documentation.
- **Recommended remediation:** Add short docstrings where behavior or domain rules are not obvious, and replace obvious comments with documentation that explains intent, constraints, or non-obvious side effects.

## 9. God Object / Blob

- **Category:** Object-Oriented Design Anti-Patterns
- **Severity:** Critical
- **Source location:** `ParkingManager.py`, `class ParkingLot` (lines 32-297); representative methods at `park` (lines 64-89), `status` (lines 117-145), `slotNumByReg` (lines 248-260), and `makeLot` (lines 278-281)
- **Minimal reproducible example:**

```python
class ParkingLot:
    def park(self, regnum, make, model, color, ev, motor):
        ...

    def status(self):
        tfield.insert(tk.INSERT, output)

    def makeLot(self):
        self.createParkingLot(int(num_value.get()), int(ev_value.get()), int(level_value.get()))
```

- **Why this is an anti-pattern here:** `ParkingLot` centralizes parking rules, slot allocation, search helpers, report formatting, and Tkinter event-handling wrappers in one class. That gives it many unrelated reasons to change and makes it the dominant coordination point for the whole prototype.
- **Impact:** The class becomes the main defect hotspot. Domain changes, lookup changes, and GUI changes all accumulate in the same type, which makes testing, reuse, and refactoring harder.
- **Recommended remediation:** Split `ParkingLot` into a focused domain object for parking behavior, a query/reporting component, and a Tkinter controller or view layer that handles form input and widget output.

## 10. Inappropriate Intimacy / Deficient Encapsulation

- **Category:** Object-Oriented Design Anti-Patterns
- **Severity:** High
- **Source location:** `Vehicle.py`, `class Vehicle` (lines 2-19); `ElectricVehicle.py`, `class ElectricVehicle` (lines 1-25); consumed from `ParkingManager.py`, `status` (lines 117-145), `getRegNumFromColor` (lines 147-155), and `getRegNumFromColorEv` (lines 197-206)
- **Minimal reproducible example:**

```python
class Vehicle:
    def __init__(self, regnum, make, model, color):
        self.color = color
        self.regnum = regnum

def getRegNumFromColor(self, color):
    for i in self.slots:
        if i.color == color:
            regnums.append(i.regnum)
```

- **Why this is an anti-pattern here:** Vehicle objects expose mutable fields directly, and `ParkingLot` reaches into those internals throughout search and reporting logic. That tightly couples `ParkingLot` to the exact field layout of vehicle classes instead of to stable behavior-level APIs.
- **Impact:** Weakens encapsulation and spreads domain knowledge across classes. Any change to vehicle representation or validation rules can ripple into many parking methods.
- **Recommended remediation:** Encapsulate vehicle state behind properties or intent-level methods such as `matches_color()` and `registration_number()`, and move vehicle-specific logic closer to the owning types.

## 11. Hidden Temporal Coupling

- **Category:** Dependency Anti-Patterns
- **Severity:** Medium
- **Source location:** `ParkingManager.py`, `ParkingLot.__init__` (lines 33-40), `createParkingLot` (lines 42-48), `getEmptySlot` (lines 50-53), `getEmptyEvSlot` (lines 55-58), and `park` (lines 64-89)
- **Minimal reproducible example:**

```python
def __init__(self):
    self.capacity = 0
    self.evCapacity = 0

def createParkingLot(self, capacity, evcapacity, level):
    self.slots = [-1] * capacity
    self.evSlots = [-1] * evcapacity

def getEmptySlot(self):
    for i in range(len(self.slots)):
        ...
```

- **Why this is an anti-pattern here:** Correct behavior depends on calling `createParkingLot()` before any parking or lookup operation, but the class does not make that lifecycle requirement explicit. The object appears usable after construction even though its core collections do not exist yet.
- **Impact:** Makes the API easy to misuse. A caller can trigger failures far away from the real cause by invoking parking behavior before initialization has completed.
- **Recommended remediation:** Initialize slot collections in the constructor or a factory, or model initialization as an explicit state so uninitialized lots cannot expose operational methods.
