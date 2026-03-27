# Comprehensive Catalog of Software Engineering Anti-Patterns

## Research basis and synthesis method

### Definitions used in this catalog

This catalog treats an **anti-pattern** as a recurring “solution” that appears to work (or is locally optimizing for something like speed of delivery) but predictably creates negative downstream effects, often with a recognizable set of symptoms and a known recovery path. This framing matches the intent of classic anti-pattern literature: anti-patterns are meant to help you **identify** the failure mode and then apply a **proven corrective strategy** rather than just naming the smell. citeturn11search10turn12search12

A **code smell** is treated as a *surface indicator* that suggests a deeper design problem may exist. This is consistent with the canonical definition (popularized by Fowler, coined by Beck). citeturn12search4 A “smell” is not always a defect; it is a heuristic signal that should trigger analysis, not necessarily immediate refactoring. citeturn12search28turn12search4

This matters for AI/static analysis: many anti-patterns are **probabilistic** detections. Tools like SonarQube explicitly distinguish *bugs*, *vulnerabilities*, and *code smells* (maintainability issues). citeturn18search0 The catalog therefore separates:
- **Recognition signals** (symptoms)
- **Heuristic detectors** (what an automated agent can reasonably infer)
- **Context gates** (when not to flag it, or when severity changes)

### Primary and modern sources emphasized

The catalog is anchored by these primary references and their widely cited successors:

- entity["people","Martin Fowler","software engineer"]; entity["people","Kent Beck","software engineer"]; entity["book","Refactoring: Improving the Design of Existing Code","2nd ed 2018"]. citeturn12search4turn14view0turn14view1  
- entity["people","Girish Suryanarayana","software engineering author"]; entity["people","Ganesh Samarthyam","software engineering author"]; entity["people","Tushar Sharma","software engineering author"]; entity["book","Refactoring for Software Design Smells","2014"] (design smells classified via abstraction/encapsulation/modularization/hierarchy principles). citeturn11search16turn11search5turn11search20  
- entity["book","Design Patterns: Elements of Reusable Object-Oriented Software","1994 gof book"] (for “Related patterns” mapping to classic GoF patterns). citeturn1search12turn5search10  
- entity["book","AntiPatterns: Refactoring Software, Architectures, and Projects","1998"] (software + organizational anti-patterns). citeturn11search10turn11search14  
- entity["people","Bill Karwin","database author"]; entity["book","SQL Antipatterns: Avoiding the Pitfalls of Database Programming","2010"] (database/application SQL antipatterns & TOC). citeturn17view0turn4search5turn4search0turn4search2  
- entity["people","Eric Evans","software author"]; entity["book","Domain-Driven Design: Tackling Complexity in the Heart of Software","2003"] (bounded contexts, anti-corruption layer concept). citeturn5search0turn1search0  
- entity["people","Sam Newman","software author"]; entity["book","Building Microservices","2nd ed 2021"] (microservices pitfalls). citeturn7search0turn10search3turn10search5  
- entity["people","Chris Richardson","software architect"]; entity["book","Microservices Patterns","2018"] plus microservices.io patterns/anti-patterns (database-per-service, shared database, API gateway/BFF, saga). citeturn7search1turn1search2turn1search29turn1search3turn1search1  
- entity["company","Microsoft","software company"] (cloud/performance anti-pattern catalogs). citeturn8view0turn10search20turn1search0  
- entity["company","Amazon Web Services","cloud provider"] (Well-Architected + DevOps guidance anti-patterns). citeturn16search3turn10search28turn10search19  
- entity["company","Google","technology company"] SRE “toil” definition and operational anti-pattern logic. citeturn16search1turn16search9turn16search5  

Academic research (2010–Mar 2026) is used where it directly supports **tool-oriented detection** (architecture smells, microservice smells, test smells) and their observed impacts. For example, Arcan-detectable architecture smells (cyclic dependency, hub-like dependency, unstable dependency) are widely studied and repeatedly used as a tool-detectable smell set in empirical work. citeturn11search21turn11search6turn11search29turn11search2

### Deduplication rules applied

To avoid duplicates yet preserve practical usefulness, this catalog applies the following merging rules:

- **Synonyms merged into one canonical name** (e.g., *God Object / Blob / God Class* become one entry).
- **Umbrella vs leaf**: if an umbrella anti-pattern (e.g., distributed monolith) is mostly the *composition* of leaf anti-patterns (shared database + chatty calls + synchronized deployment), the umbrella entry focuses on system-level symptoms and cross-references leaves.
- **Single “home category”**: each anti-pattern is placed once under the most actionable top-level category (Code, OO design, Architecture, Microservices, Testing, Data/DB, Dependency, Performance, Maintainability, Organizational). Cross-category relevance is handled via “Related patterns” and “SOLID mapping,” not duplicate entries.

### Detection heuristics template for AI agents

Detection heuristics throughout follow a consistent model:

- **Static structural signals**: AST patterns, complexity metrics, dependency graphs, schema/DDL patterns.
- **Behavioral signals**: runtime traces, latency distributions, call graph fan-out, lock contention.
- **Change signals**: Git churn, co-change clusters (shotgun surgery), PR blast radius.
- **Tool alignment**: rulesets from SonarQube, pylint/ruff (derived), PMD metrics. citeturn18search0turn18search2turn18search9turn18search6turn18search32

Because rule thresholds are frequently gamed or misapplied, the catalog treats metrics (cyclomatic/NPath/etc.) as **signals** rather than absolute truth, and explicitly calls out high false-positive zones (e.g., generated code, parser code, code with unavoidable conditionality). citeturn18search14turn18search17

## Categorized taxonomy

This taxonomy is designed to be usable in three contexts: (a) learning/reference, (b) static analysis rule design, (c) architecture quality assessment.

### Code-level anti-pattern clusters

- **Complexity & control flow**: long function; deep nesting; repeated switches; branch explosion; “exception-driven” control flow; hidden control flow (callbacks that look synchronous).
- **State & mutability**: global mutable state; temporal coupling; implicit shared state; “action at a distance.”
- **Naming & clarity**: mysterious names; misleading names; comment-as-deodorant; duplication that masks intent.
- **API & error-handling misuse**: swallowed exceptions; over-broad catches; logging without context; returning sentinel values inconsistently.
- **Security-adjacent code smells**: hardcoded secrets; insecure randomness; string-built queries (overlaps with Data/DB but detectable at code-level).

Code smell framing is consistent with Fowler’s “surface indicator” definition and with SonarQube’s maintainability “code smell” definition. citeturn12search4turn18search0turn18search1

### OO design anti-pattern clusters

Suryanarayana et al. organize design smells by violations of fundamental OO design elements (abstraction, encapsulation, modularization, hierarchy). citeturn11search5turn11search20turn11search16  
Catalog clusters align to that scheme:

- **Abstraction smells**: leaky abstractions; incomplete abstractions; “stringly typed domain.”
- **Encapsulation smells**: data exposure; anemic domain model; inappropriate intimacy.
- **Modularization smells**: feature envy; scattered responsibilities; cyclic package dependencies.
- **Hierarchy smells**: refused bequest; fragile base class; inappropriate inheritance; deep inheritance.

### Architecture anti-pattern clusters

- **Boundary erosion**: Big Ball of Mud; layering violations; dependency inversion violations at system scale.
- **Coupling & change amplification**: unstable dependencies; hub-like components; shared “core” modules that become dumping grounds. citeturn11search6turn11search21turn11search13turn11search2
- **Modernization traps**: “strangler in name only” (partial strangler with continued tight coupling).

### Microservices anti-pattern clusters

- **Distributed coupling**: distributed monolith; lockstep deployments; synchronous cascades.
- **Data ownership violations**: shared database/schema; cross-service joins at runtime; data-leaking boundaries. citeturn4search15turn1search29turn1search2turn4academia41
- **Communication pathologies**: chatty services; API gateway becoming a “mini-monolith”; inconsistent contracts.
- **Ops anti-patterns specific to microservices**: missing observability, missing timeouts/retries, “no versioning strategy” (contract drift).

### Testing anti-pattern clusters

A modern, tool-oriented view treats test smells as patterns in test code and test processes that reduce defect detection and increase cost (flakiness, slow suites, brittle assertions). This is consistent with survey work and the evolving “test smell catalog” literature. citeturn4search0turn0search11turn1search6

### Data/DB anti-pattern clusters

Based on SQL Antipatterns’ structure: logical design, physical design, query anti-patterns, application development anti-patterns. citeturn17view0turn4search5turn4search15

### Dependency and performance clusters

- **Dependency anti-patterns** (static graph & versioning): cyclic dependencies; unstable dependencies; hub-like dependencies; dependency hell; vendoring core libs across repos.
- **Performance anti-patterns**: chatty I/O; extraneous fetching; improper caching; “busy database”; “noisy neighbor”; payload bloat. Microsoft’s cloud anti-pattern catalog is a stable reference set for many of these. citeturn8view0turn11search2

### Organizational/process clusters (optional but included)

These matter because they create systemic conditions that *force* technical anti-patterns: mushroom management; death by planning; continuous obsolescence; “hero culture” operations; siloed ownership (Dev vs Ops). citeturn11search10turn11search14turn16search1

## Master anti-pattern catalog

The catalog entries below are grouped under the requested top-level categories but each entry includes a single “Category:” value chosen from: Code / Design / Architecture / Microservices / Testing / Data.

### Code-Level Anti-Patterns

**Long Function / Long Method**  
Category: Code  
Description: A function grows large enough that it mixes multiple concerns, becomes difficult to name precisely, and resists local reasoning. citeturn14view0turn18search9  
Symptoms: Many local variables; multiple levels of abstraction in one body; branching or early returns dominate; heavy commenting to explain “what.” citeturn18search9turn12search30  
Why It’s Bad: Inflates cognitive load, makes unit testing harder, and increases regression risk during edits. citeturn18search1turn12search28  
Detection Heuristics: Flag when statements > configurable threshold; deep nesting; cyclomatic and/or NPath complexity high; high churn on the function. citeturn18search9turn18search6turn18search25  
Severity: Medium → High (Critical if security-sensitive logic or concurrency).  
Example:
```python
def process_order(order):  # does validation + pricing + persistence + notifications
    # 200+ lines, nested if/else, many temporaries
    ...
```  
Refactoring / Solution: Extract Function; Split Phase; Introduce Parameter Object; extract domain services where boundaries exist. citeturn14view1turn14view0  
Related Patterns: Command; Template Method; Strategy (replace large conditional flows). citeturn5search10  
Sources: Fowler’s smell list and refactoring catalog naming. citeturn14view0turn14view1  

**Deep Nesting / Arrow Code**  
Category: Code  
Description: Excessive nesting (“if/for/try” in “if/for/try”) causes the function structure to encode complex state machines implicitly.  
Symptoms: Indentation dominates; many “else” branches; logic comprehension requires path enumeration. citeturn18search2turn18search32  
Why It’s Bad: Destroys readability and systematically correlates with missed edge cases (paths have no tests).  
Detection Heuristics: Max nesting depth > N; branch count > N; presence of long boolean conditions. citeturn18search2turn18search32  
Severity: Medium (High in error-handling or authorization logic).  
Example:
```python
if a:
    if b:
        try:
            if c:
                ...
        except Exception:
            ...
```  
Refactoring / Solution: Guard clauses; Extract Function; Replace Nested Conditional with Polymorphism/Strategy. citeturn14view1turn5search10  
Related Patterns: Strategy; State. citeturn5search10  
Sources: Static-analysis “too many branches” concept. citeturn18search2turn18search32  

**Repeated Switches / Giant Conditional**  
Category: Code  
Description: Business logic is encoded primarily through repeating `if/elif` chains or `switch`/`match` statements instead of polymorphism or table-driven behavior. citeturn14view0turn12search5  
Symptoms: Same conditional appears in multiple areas (“parallel conditionals”); adding a new type requires editing many files. citeturn12search5turn14view0  
Why It’s Bad: Violates open/closed intent and creates change amplification. citeturn0search6turn0search18  
Detection Heuristics: Detect duplicated discriminant expressions; count of `case` branches; repeated string literals/enums; co-change clusters between the conditional sites.  
Severity: High (Critical if it becomes the core extension point).  
Example:
```python
if kind == "A": ...
elif kind == "B": ...
elif kind == "C": ...
```  
Refactoring / Solution: Strategy/State; Replace Conditional with Polymorphism; use lookup tables or registries when OO polymorphism is heavy. citeturn5search10turn14view1  
Related Patterns: Strategy; State; Factory Method. citeturn5search10  
Sources: Refactoring “Repeated Switches” smell and refactoring patterns list. citeturn14view0turn14view1  

**Magic Literals (Magic Numbers / Magic Strings)**  
Category: Code  
Description: Business/technical constants appear as raw literals with no naming, provenance, or constraints (e.g., `"PENDING"`, `86400`, `0.1`).  
Symptoms: Same literal repeats; unclear units; values changed “by guessing” during debugging. citeturn11search3turn12search12  
Why It’s Bad: Produces silent semantic drift; breaks maintainability and increases defect likelihood on change.  
Detection Heuristics: Literal repetition; suspicious numeric constants; string constants used for states instead of enums; absence of named constants/config.  
Severity: Low → Medium (High when used in security, financial, or safety calculations).  
Example:
```python
timeout = 37  # why 37?
```  
Refactoring / Solution: Replace with named constant; introduce enums/value objects; constrain and validate at boundaries.  
Related Patterns: Value Object; Parameter Object.  
Sources: Widely listed as a code smell/anti-pattern in code-smell catalogs. citeturn11search3turn12search12  

**Global Mutable State (Global Data)**  
Category: Code  
Description: Shared state is globally accessible and mutable, creating hidden couplings and implicit ordering requirements. citeturn14view0turn12search8  
Symptoms: Tests require reset hooks; behavior depends on call order; concurrency bugs appear as “heisenbugs.”  
Why It’s Bad: Makes local reasoning impossible; creates unsafe concurrency and brittle tests.  
Detection Heuristics: Module-level variables mutated; singletons with mutable fields; use of global registries; cross-test pollution signatures. citeturn14view0turn12search8  
Severity: High (Critical in multithreaded/async systems).  
Example:
```python
CACHE = {}
def get_user(id_):
    CACHE[id_] = ...
```  
Refactoring / Solution: Encapsulate Variable; dependency inject state; prefer immutable data; confine mutation. citeturn14view1  
Related Patterns: Dependency Injection; Repository; Immutable Value Objects.  
Sources: Fowler smell list and refactoring catalog. citeturn14view0turn14view1  

**Mutable Shared Data Without Ownership (Mutable Data)**  
Category: Code  
Description: Data structures are mutated across multiple ownership zones (functions/modules), without clear invariants or encapsulation. citeturn14view0turn12search8  
Symptoms: Defensive copying everywhere; “who changed this?” debugging; object state becomes invalid temporarily.  
Why It’s Bad: Creates temporal coupling, increases concurrency hazards, and makes invariants uncheckable.  
Detection Heuristics: Same object passed through many layers and mutated; widespread setter usage; mutation inside getters.  
Severity: Medium → High.  
Example:
```python
user.profile["role"] = "admin"  # mutated anywhere
```  
Refactoring / Solution: Encapsulate Record/Collection; Replace Primitive with Object; copy-on-write. citeturn14view1  
Related Patterns: Immutable Value Object; Builder.  
Sources: Fowler smell list and catalog. citeturn14view0turn14view1  

**Swallowed Exceptions / Error Hiding**  
Category: Code  
Description: Exceptions are caught but ignored (or replaced with generic messages), suppressing the real failure signal.  
Symptoms: `except Exception: pass`; logs with no stack trace or context; “works, except sometimes.” citeturn11search3turn11search26  
Why It’s Bad: Turns defects into silent data corruption or undefined behavior; destroys observability.  
Detection Heuristics: Empty `catch/except`; logging without rethrow/handling; returning default sentinel after exception with no explicit contract.  
Severity: High → Critical (critical if data integrity/security).  
Example:
```python
try:
    write_to_db(x)
except Exception:
    return None  # hides root cause
```  
Refactoring / Solution: Catch specific exceptions; add context; propagate or map to a domain error; use “fail fast” for invariants.  
Related Patterns: Result/Either; Circuit Breaker at boundary (distributed). citeturn1search6  
Sources: Anti-pattern lists include error hiding and emphasize reporting details. citeturn11search3turn11search26  

**Comment-as-Deodorant**  
Category: Code  
Description: Comments exist primarily to explain confusing code rather than intent, often because the code is not self-explanatory. Refactoring often makes such comments unnecessary. citeturn12search9turn12search30  
Symptoms: Long explanatory comments; comments duplicate what code says; comments fall out of date. citeturn12search9  
Why It’s Bad: Comments rot; readers trust comments and misread behavior.  
Detection Heuristics: Large comment blocks preceding complex code; comment-to-code ratio spikes in hotspots; “TODO explain” markers.  
Severity: Low → Medium (High if comments become wrong in safety/security logic).  
Example:
```python
# Calculates price with discount rules (complex)
price = ...
```  
Refactoring / Solution: Rename Variable/Function; Extract Function; Introduce Assertion; replace “explanations” with structure. citeturn14view1turn12search9  
Related Patterns: Self-documenting code is a practice; for OO, Strategy can encode rules. citeturn5search10  
Sources: Fowler refactoring guidance on comments as refactoring trigger. citeturn12search9turn14view1  

**Over-parameterized Functions (Long Parameter List / Too Many Arguments)**  
Category: Code  
Description: Functions take so many parameters that call sites become fragile and meaning depends on argument ordering. citeturn14view0turn12search12  
Symptoms: Many related parameters always passed together; frequent `None`/default placeholders; call sites hard to read.  
Why It’s Bad: Indicates missing abstraction or conflated responsibilities; increases bug surface.  
Detection Heuristics: Parameter count > threshold; repeated parameter clusters across functions (“data clumps”); pylint/ruff warnings. citeturn18search24turn18search5  
Severity: Medium.  
Example:
```python
def create_user(a, b, c, d, e, f): ...
```  
Refactoring / Solution: Introduce Parameter Object; Encapsulate Record; split into cohesive operations. citeturn14view1turn14view0  
Related Patterns: Builder; Facade. citeturn5search10  
Sources: Fowler smell list and refactoring catalog; pylint warnings for excessive arguments. citeturn14view0turn18search24  

**Primitive Obsession / Stringly Typed Domain**  
Category: Design  
Description: Domain concepts are represented with primitives (strings/ints) rather than types that enforce invariants (e.g., `user_id: str`, `currency: str`). citeturn14view0turn12search12  
Symptoms: Repeated validation; “special string values”; inconsistent formatting rules.  
Why It’s Bad: Invariants leak everywhere; errors become runtime-only; refactors become fragile.  
Detection Heuristics: Repeated regex/validation; many functions accept `str` for different semantic roles; magic strings in APIs.  
Severity: Medium → High.  
Example:
```python
def pay(amount: float, currency: str): ...
```  
Refactoring / Solution: Replace Primitive with Object; encapsulate constraints; introduce enums/value objects. citeturn14view1  
Related Patterns: Value Object.  
Sources: Fowler smell list (“Primitive Obsession”) and refactoring. citeturn14view0turn14view1  

**Data Clumps**  
Category: Code  
Description: The same group of variables travels together across APIs because it should be modeled as a cohesive object. citeturn14view0turn12search12  
Symptoms: Same tuple of parameters in many functions; repeated field extraction.  
Why It’s Bad: Expands interface surface and makes change expensive.  
Detection Heuristics: Frequent co-occurrence of the same parameter subset; repeated destructuring; duplicated validation.  
Severity: Medium.  
Example:
```python
def ship(city, state, zip_code, country): ...
```  
Refactoring / Solution: Introduce Parameter Object; Encapsulate Record. citeturn14view1  
Related Patterns: Value Object.  
Sources: Fowler smell list. citeturn14view0turn14view1  

**Inconsistent Null/Sentinel Semantics**  
Category: Code  
Description: APIs mix `None`, empty strings, sentinel values (e.g., `-1`), and exceptions inconsistently to represent absence/failure.  
Symptoms: Call sites contain defensive checks; bugs come from wrong sentinel assumptions (“-1 is valid”).  
Why It’s Bad: Creates implicit contracts, leads to error hiding and subtle correctness issues.  
Detection Heuristics: Mixed patterns in same API family; unused return values; inconsistent docstrings/types.  
Severity: Medium (High when caused by DB “NULL confusion”).  
Example:
```python
return -1  # means "not found" here
```  
Refactoring / Solution: Standardize with Result/Either; use exceptions for exceptional cases, explicit Optional for absence; add type hints/contracts.  
Related Patterns: Null Object (used carefully); Option/Maybe.  
Sources: SQL “NULL misuse” is a known antipattern class (“Fear of the Unknown”). citeturn4search7turn17view0  

### Object-Oriented Design Anti-Patterns

**God Object / Blob (God Class)**  
Category: Design  
Description: A single class accumulates too much responsibility, often becoming the “place where logic goes,” with low cohesion and high coupling. citeturn11search14turn18search1turn12search12  
Symptoms: Many fields/methods; knows too much; orchestrates many “dumb” objects. citeturn11search14turn18search1  
Why It’s Bad: Violates SRP; creates change hotspots; blocks modularization and testing. citeturn15search17turn11search14  
Detection Heuristics: LOC/method count high; LCOM low cohesion; high fan-in/fan-out; “manager/controller” naming.  
Severity: High → Critical (critical if it’s architecture core).  
Example:
```java
class OrderManager { /* validation, pricing, persistence, email, ... */ }
```  
Refactoring / Solution: Extract Class; Move Function/Field; introduce cohesive domain services; enforce boundaries. citeturn14view1turn14view0  
Related Patterns: Facade (as explicit boundary, not dumping ground); Mediator (careful); Command. citeturn5search10  
Sources: AntiPatterns “Blob” and modern smell catalogs. citeturn11search14turn18search1  

**Anemic Domain Model**  
Category: Design  
Description: Domain objects hold data but behavior lives elsewhere (procedural services), undermining encapsulation. citeturn3search10turn5search0  
Symptoms: Entities are mostly getters/setters; business logic in “Service” classes; invariant checks scattered.  
Why It’s Bad: Breaks encapsulation; tends to grow into Transaction Script; increases duplication and inconsistency. citeturn5search0turn9search13  
Detection Heuristics: Domain classes with few non-trivial methods; service classes containing most conditional logic; high “data class” smell frequency. citeturn14view0  
Severity: Medium → High.  
Example:
```java
class Invoice { BigDecimal total; /* getters */ } // all logic elsewhere
```  
Refactoring / Solution: Move behavior into entities/value objects; introduce aggregates; make invariants explicit.  
Related Patterns: Domain Model (vs Transaction Script); Value Object; Specification. citeturn9search13turn5search0  
Sources: Fowler’s definition of the anemic model as an anti-pattern and DDD reference concepts. citeturn3search10turn5search0  

**Refused Bequest / LSP Violation by Inheritance**  
Category: Design  
Description: A subclass inherits behavior/state but does not honor the base class contract, often overriding to “disable” functions or throwing unexpected exceptions. citeturn14view0turn15search2  
Symptoms: Overrides that reduce behavior; unused inherited members; subclass breaks substitutability.  
Why It’s Bad: Violates LSP; forces callers to add type checks; makes hierarchies brittle. citeturn15search2turn15search22  
Detection Heuristics: Override methods throw `UnsupportedOperationException`; conditional on `instanceof` for behavior; tests passing base but failing derived.  
Severity: High.  
Example:
```java
class ReadOnlyList extends List { void add(...) { throw ... } }
```  
Refactoring / Solution: Replace Subclass with Delegate; Split hierarchy; prefer composition; narrow interfaces. citeturn14view1turn15search2  
Related Patterns: Composition over inheritance; Decorator. citeturn5search10  
Sources: Fowler smell list and LSP definition literature. citeturn14view0turn15search2  

**Fat Interface / ISP Violation**  
Category: Design  
Description: Interfaces grow to satisfy many clients, forcing dependents to compile against methods they don’t use. citeturn15search3turn15search23  
Symptoms: Many methods; “god interface”; clients implement no-op methods.  
Why It’s Bad: Creates unnecessary coupling and change amplification; blocks independent deployment in distributed contexts. citeturn15search3turn1search6  
Detection Heuristics: Interfaces with many members and many distinct client subsets; clients calling small subsets; high frequency of “not implemented” or stub code.  
Severity: Medium → High.  
Example:
```java
interface Job { print(); staple(); fax(); scan(); ... } // few clients use all
```  
Refactoring / Solution: Segregate interfaces into role interfaces; depend on minimal abstractions; apply DIP to invert dependencies. citeturn15search3turn0search17  
Related Patterns: Adapter; Facade; Ports & Adapters. citeturn5search10turn1search0  
Sources: Classic ISP definition and history. citeturn15search3turn15search23  

**Feature Envy (Misplaced Behavior)**  
Category: Design  
Description: A method is more interested in another object’s data than its own, suggesting behavior is located in the wrong class. citeturn11search0turn14view0turn11search23  
Symptoms: Many getters on another class; unnecessary exposure of internals. citeturn11search0turn11search23  
Why It’s Bad: Increases coupling, weakens encapsulation, and signals that cohesion boundaries are wrong.  
Detection Heuristics: Count field/method accesses to foreign types vs self; chained getters; high coupling between two classes.  
Severity: Medium.  
Example:
```python
total = order.customer.account.credit_limit - order.total()
```  
Refactoring / Solution: Move Function; Extract Function then Move; Hide Delegate. citeturn11search0turn14view1  
Related Patterns: Tell-Don’t-Ask (practice); Law of Demeter (principle).  
Sources: Fowler refactoring discussion and smell catalogs. citeturn11search0turn14view0  

**Inappropriate Intimacy / Encapsulation Violation**  
Category: Design  
Description: Two classes know too much about each other’s private details (friend-like coupling), often due to leaking fields or exposing internal structure. citeturn11search4turn14view0  
Symptoms: Many getters/setters used externally; frequent access to internal collections; cross-module “reach-in.”  
Why It’s Bad: Refactoring becomes dangerous; invariants cannot be enforced centrally.  
Detection Heuristics: High number of accesses to non-public members; repeated access to internal fields via getters; “internal” packages used widely.  
Severity: Medium → High.  
Example:
```java
customer.getAccount().getLedger().entries.add(...)
```  
Refactoring / Solution: Hide Delegate; Encapsulate Collection; move behavior to the owning class. citeturn14view1turn11search4  
Related Patterns: Facade; Information Hiding.  
Sources: Code smell catalogs and refactoring list. citeturn11search4turn14view1  

**Speculative Generality / Over-Abstracted Design**  
Category: Design  
Description: Abstractions are introduced “for future flexibility” without a present need, creating unused hooks, generic frameworks, and indirection. citeturn14view0turn12search8  
Symptoms: Unused interfaces; “just in case” extension points; abstract base classes with one implementation.  
Why It’s Bad: Indirection cost without payoff; higher cognitive load; slower change.  
Detection Heuristics: Abstract types with one implementer; low usage of extension points; dead code in generic scaffolding.  
Severity: Medium.  
Example:
```java
interface PaymentStrategy { ... } // only one implementation forever
```  
Refactoring / Solution: Inline Class/Function; delete unused abstractions; reintroduce when actual variation emerges. citeturn14view1  
Related Patterns: YAGNI as an engineering constraint. citeturn12search28turn13view1  
Sources: Fowler smell list. citeturn14view0turn13view1  

### Architecture Anti-Patterns

**Big Ball of Mud**  
Category: Architecture  
Description: A system lacks a discernible architecture; boundaries are absent or eroded; components are entangled, and changes have unpredictable side effects. citeturn3search11turn11search30  
Symptoms: No stable modules; “quick fixes” everywhere; build/deploy requires tribal knowledge.  
Why It’s Bad: Change becomes risky and expensive; defects increase; long-term throughput collapses.  
Detection Heuristics: Dense dependency graph; high cyclic dependencies; high co-change across unrelated areas; unclear ownership boundaries. citeturn11search2turn11search25  
Severity: Critical.  
Example (architecture sketch):
```text
UI <--> Services <--> DB
 ^      ^   ^         |
 |______|___|_________|
```
Refactoring / Solution: Introduce seams; modularize by business capability; apply Strangler Fig for incremental replacement. citeturn9search30turn3search11  
Related Patterns: Layered Architecture (with enforcement); Hexagonal/Ports & Adapters; Strangler Fig. citeturn9search30  
Sources: Classic Big Ball of Mud paper and anti-pattern summaries. citeturn3search11turn11search30  

**Architecture by Accretion (Lava Flow)**  
Category: Architecture  
Description: Temporary or experimental code paths harden into “production reality,” leaving strata of dead or obsolete subsystems that are risky to remove. citeturn11search10turn11search3  
Symptoms: “Nobody knows if we can delete that”; unused configs; legacy paths “just in case.”  
Why It’s Bad: Increases cognitive load; blocks modernization; causes security exposure in forgotten components.  
Detection Heuristics: Low runtime usage but high compile-time presence; dead flags; low test coverage in old subsystems; dependency graph includes unused modules.  
Severity: High → Critical (critical if unpatchable components remain).  
Example:
```text
NewBilling -> LegacyBillingAdapter -> LegacyBilling (still shipped)
```
Refactoring / Solution: Instrument usage; kill switches; delete dead paths; apply Strangler where replacement exists. citeturn9search30turn11search34  
Related Patterns: Strangler Fig; Feature Flags (as controlled transition tool). citeturn9search30  
Sources: AntiPatterns catalog includes Lava Flow; modern “dead code” discussions. citeturn11search10turn11search34  

**Layering Violations / Wrong Dependency Direction**  
Category: Architecture  
Description: Lower layers depend on higher layers (or skip layers), undermining modular reasoning and deployability.  
Symptoms: UI imports domain internals; domain calls infrastructure directly; cross-layer utility dumping.  
Why It’s Bad: Breaks isolation; amplifies changes; makes testing and substitution harder.  
Detection Heuristics: Dependency rules violated (package naming layers); upward import edges; circular “layer cycles.”  
Severity: High.  
Example:
```text
domain -> web (should be web -> domain)
```
Refactoring / Solution: Apply Dependency Inversion; introduce ports/adapters; enforce module boundaries. citeturn0search17turn0search0turn0search1  
Related Patterns: DIP; Clean/Hexagonal architecture. citeturn0search17turn0search1  
Sources: “Principles of OOD” series and DIP reference. citeturn0search1turn0search17  

**Hub-like Dependency / God Component**  
Category: Architecture  
Description: A component becomes a central hub depended upon by many others, making it a single point of change and a propagation center for instability. citeturn11search6turn11search13turn11search21  
Symptoms: Many incoming edges; frequent changes trigger widespread rebuilds; “core” module grows without governance.  
Why It’s Bad: Produces cascade failures in change and runtime coupling; reduces testability and maintainability. citeturn11search29turn11search2  
Detection Heuristics: Dependency graph centrality; high fan-in; “hub-like dependency” detectors in tools like Arcan. citeturn11search6turn11search21turn11search37  
Severity: High → Critical (critical if it is deployment bottleneck).  
Example:
```text
20 modules -> shared-core -> utilities + domain + infra mixed
```
Refactoring / Solution: Split by cohesive responsibility; apply stable abstractions; introduce anti-corruption layers for legacy. citeturn1search0turn11search6  
Related Patterns: Facade (explicit boundary); Anti-Corruption Layer. citeturn1search0  
Sources: Architecture smell detector literature (Arcan) and empirical impact studies. citeturn11search21turn11search29  

**Cyclic Dependency at Architecture/Package Level**  
Category: Architecture  
Description: Modules form dependency cycles, preventing independent reasoning, testing, and deployment. citeturn11search21turn11search2  
Symptoms: Breaks require “build everything”; inability to isolate; tangled commissions.  
Why It’s Bad: Cycles are repeatedly linked to higher complexity and degraded quality attributes in empirical studies. citeturn11search2turn11search29  
Detection Heuristics: Graph cycle detection; growth of cycle size over releases; repeated merges create “multi-hubs.” citeturn11search2  
Severity: High.  
Example:
```text
A -> B -> C -> A
```
Refactoring / Solution: Break cycle by introducing interfaces, DIP, or extracting shared abstractions into stable modules; sometimes split responsibilities. citeturn0search17turn11search21  
Related Patterns: DIP; Stable Dependencies Principle (related OOD principles set). citeturn0search1  
Sources: Arcan smell set and evolution studies. citeturn11search21turn11search2  

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["distributed monolith diagram microservices anti-pattern","microservices shared database anti-pattern diagram","hub-like dependency architecture smell diagram","cyclic dependency architecture graph example"],"num_per_query":1}

### Microservices Anti-Patterns

**Distributed Monolith**  
Category: Microservices  
Description: Services are deployed separately but remain tightly coupled (shared data, synchronous chains, lockstep releases), so the architecture keeps monolith coupling while adding distributed-system failure modes. citeturn4search15turn10search5turn7academia41  
Symptoms: Coordinated deployments; many cross-service RPC calls per user action; schema lock-in; changes require multi-service PRs.  
Why It’s Bad: Pays the cost of distribution (latency, partial failure, observability complexity) without gaining independent deployability.  
Detection Heuristics: Co-deploy frequency; cross-service call depth from tracing; shared DB usage; high synchronous fan-out. citeturn1search6turn11search33  
Severity: Critical.  
Example:
```text
Checkout -> Pricing -> Inventory -> Customer -> Payments (sync chain)
```
Refactoring / Solution: Re-cut boundaries using bounded contexts; introduce async messaging for internal workflows; apply database-per-service. citeturn5search0turn1search2turn1search1  
Related Patterns: Database per Service; Saga; API Gateway/BFF (with constraints). citeturn1search2turn1search1turn1search3  
Sources: Microservices data-management issues taxonomy and microservice smells research. citeturn4search15turn4academia41  

**Shared Database (Microservices Data Ownership Violation)**  
Category: Microservices  
Description: Multiple services directly read/write the same database schema, coupling evolution and runtime behavior. microservices.io calls this “more of an anti-pattern” compared to database-per-service. citeturn1search29turn1search2  
Symptoms: Cross-service joins; breaking schema changes; lock contention between “services.”  
Why It’s Bad: Removes service autonomy; increases incident blast radius; creates coordinated deployments via schema change. citeturn1search29turn4search15  
Detection Heuristics: Multiple services share JDBC/connection config; schema/table access observed across services; DB permissions non-segregated.  
Severity: High → Critical.  
Example:
```text
Service A + Service B both update ORDERS table
```
Refactoring / Solution: Database per service (schema- or table-per-service); build integration via APIs/events; migrate incrementally. citeturn1search2turn1search11  
Related Patterns: Database per Service; Saga (for cross-service consistency). citeturn1search2turn1search1  
Sources: microservices.io shared DB warning and alternatives. citeturn1search29turn1search2  

**Chatty Services / Excessive Remote Calls**  
Category: Microservices  
Description: A single user outcome requires many fine-grained RPC calls between services (or client-to-service), producing latency and fragility. Microsoft and microservices.io both highlight request aggregation/roundtrip reduction motivations in gateway patterns. citeturn1search3turn1search22turn8view0  
Symptoms: High p95 latency; many small calls in traces; clients need orchestration logic.  
Why It’s Bad: Latency compounds; failures cascade; increases need for retries/timeouts and makes systems unpredictable.  
Detection Heuristics: Distributed traces show high span count per request; small payload sizes; repeated call patterns across endpoints.  
Severity: High.  
Example:
```text
Mobile app calls 12 services for one screen render
```
Refactoring / Solution: API Gateway / BFF; API Composition; denormalize read models (CQRS). citeturn1search3turn1search11turn1search6turn1search9  
Related Patterns: API Gateway/BFF; CQRS; caching. citeturn1search3turn1search6  
Sources: microservices.io gateway rationale and Microsoft gateway guidance. citeturn1search3turn1search22  

**API Gateway as a Mini-Monolith**  
Category: Microservices  
Description: A single gateway accumulates orchestration for many clients and business domains, becoming a centralized bottleneck. Microsoft explicitly warns that a single gateway serving many clients can bloat and resemble a monolith, recommending segregation (BFF). citeturn1search22turn1search3  
Symptoms: Gateway deploys block all clients; gateway contains domain logic; frequent hotfixes.  
Why It’s Bad: Recreates hub dependency and couples client evolution to a single service.  
Detection Heuristics: Gateway is highest-churn component; largest codebase; contains business rules not routing/aggregation; many downstream dependencies.  
Severity: High.  
Example:
```text
Gateway handles pricing rules + user policy + orchestration for all channels
```
Refactoring / Solution: Split into BFF gateways per client type and/or business boundary; move domain logic to services; keep gateway thin. citeturn1search22turn1search3  
Related Patterns: BFF; Facade (boundary layer). citeturn1search3turn5search10  
Sources: Microsoft guidance and microservices.io gateway pattern. citeturn1search22turn1search3  

**Synchronous Cascade / No Timeouts in Microservice Calls**  
Category: Microservices  
Description: Services call each other synchronously without strict timeouts, bulkheads, and circuit breakers; failures propagate as a cascade. Observability and resilience patterns are called out as key microservice concerns. citeturn1search6turn7search18  
Symptoms: Thread pool exhaustion; retry storms; partial outage becomes full outage.  
Why It’s Bad: Converts partial failures into systemic failures (classic distributed-systems failure mode).  
Detection Heuristics: Missing client-side timeouts; unbounded retries; traces show long synchronous chains; no circuit breaker configuration.  
Severity: Critical.  
Example:
```text
A waits on B waits on C (each with default infinite timeout)
```
Refactoring / Solution: Enforce timeouts; bounded retries with jitter; circuit breakers; redesign with async messaging where appropriate. citeturn1search6turn7search18  
Related Patterns: Circuit Breaker; Bulkhead; Saga instead of distributed ACID. citeturn1search6turn1search1turn7search18  
Sources: Microservice pattern language highlights resilience/observability patterns, and “Release It!” is a classic resilience reference. citeturn1search6turn7search18  

**Cross-Service Transactions Without a Saga Strategy**  
Category: Microservices  
Description: Microservices attempt to preserve monolithic ACID semantics across services via synchronous coordination, without a saga/compensation model. citeturn1search1turn1search9  
Symptoms: Two-phase commit attempts; long distributed locks; “stuck” partial orders.  
Why It’s Bad: Distributed transactions are brittle and operationally expensive; failure recovery is unclear.  
Detection Heuristics: Transaction IDs crossing services; distributed locking; compensations absent; strong consistency enforced via synchronous call chains.  
Severity: High → Critical.  
Example:
```text
OrderService calls PaymentService then InventoryService with rollback “TODO”
```
Refactoring / Solution: Saga (orchestration or choreography); idempotency; outbox pattern for reliable event publication. citeturn1search1turn1search24  
Related Patterns: Saga; Database per Service. citeturn1search1turn1search2  
Sources: Saga pattern definition and context. citeturn1search1turn1search24  

**No Anti-Corruption Layer When Integrating a Legacy/External Domain**  
Category: Microservices  
Description: The internal domain model becomes polluted by external system semantics because integration is done “directly” rather than through a translation boundary. This pattern is explicitly described as first described by Evans and documented by Microsoft and microservices.io. citeturn1search0turn1search4turn5search0  
Symptoms: External IDs and concepts leak into core domain; churn in external system triggers widespread changes.  
Why It’s Bad: Locks internal design to external constraints; degrades evolvability.  
Detection Heuristics: Domain entities include external DTOs; direct dependencies on external API models across codebase; widespread mapping logic duplicated.  
Severity: High.  
Example:
```text
Domain uses ExternalCRMAccountStatus enum everywhere
```
Refactoring / Solution: Introduce anti-corruption layer; isolate mapping; constrain dependencies to dedicated integration module. citeturn1search0turn1search4  
Related Patterns: Adapter; Facade; Strangler (for modernization). citeturn1search0turn9search30  
Sources: Microsoft ACL pattern page and microservices.io ACL refactoring pattern. citeturn1search0turn1search4  

### Testing Anti-Patterns

**Flaky Tests**  
Category: Testing  
Description: Tests that occasionally fail without code changes (timing, concurrency, external dependencies), destroying trust in the suite. citeturn4search0turn0search11  
Symptoms: “Rerun fixes it”; failures correlate with load/time-of-day; order-dependent tests.  
Why It’s Bad: Engineers ignore CI signals; slows delivery; forces manual investigation.  
Detection Heuristics: Historical failure intermittency; correlation with environment variance; tests involving real time, network, randomness without control.  
Severity: High (Critical if CI becomes unreliable gate).  
Example:
```python
assert cache.get("x") == "y"  # depends on background eviction timing
```  
Refactoring / Solution: Control time; use deterministic fakes; isolate external systems; eliminate shared mutable globals.  
Related Patterns: Test Doubles (stubs/fakes); Hermetic tests. citeturn4search0  
Sources: Test smell survey and catalog approach. citeturn4search0turn0search11  

**Over-Mocking / Mock-Driven Brittle Tests**  
Category: Testing  
Description: Tests validate implementation details (interaction sequences) rather than behavior, making refactoring painful. citeturn4search0turn0search11  
Symptoms: Any internal refactor breaks tests; mocks mirror method calls; tests assert call order.  
Why It’s Bad: Locks internal design; causes “test-induced design damage.”  
Detection Heuristics: High mock count per test; assertions mostly on interactions; little state/output verification.  
Severity: Medium → High.  
Example:
```python
mock.assert_called_with(...)  # for every internal step
```  
Refactoring / Solution: Prefer state-based tests; contract tests for boundaries; use fakes; reserve mocks for integration boundaries.  
Related Patterns: Contract tests; Ports & Adapters. citeturn1search6  
Sources: Test smell literature surveys. citeturn4search0turn0search11  

**Slow Test Suite / No Test Pyramid Discipline**  
Category: Testing  
Description: The default test loop is slow because most tests are end-to-end/integration, not unit/component.  
Symptoms: CI takes hours; developers avoid running tests locally.  
Why It’s Bad: Slows feedback and encourages risky changes; increases batch size.  
Detection Heuristics: Test duration telemetry; percentage of tests requiring network/DB; low unit-test ratio.  
Severity: High (Critical in fast-moving systems).  
Example:
```text
Build: 10m, Tests: 120m, most are E2E
```  
Refactoring / Solution: Introduce component tests; isolate boundaries; run E2E on critical flows only; parallelize. citeturn16search19turn16search3  
Related Patterns: Service component test; consumer-driven contracts. citeturn1search6  
Sources: Testing patterns in microservice pattern language; CI/CD anti-pattern framing. citeturn1search6turn16search19  

**Assertion Roulette**  
Category: Testing  
Description: Tests contain many assertions with unclear failure messages, making diagnosis slow. citeturn0search11turn4search0  
Symptoms: “Expected true, got false” with no context; large blocks of asserts.  
Why It’s Bad: Increases MTTR and encourages ignoring failing tests.  
Detection Heuristics: Many asserts per test without message/structure; asserts on booleans; missing descriptive names.  
Severity: Medium.  
Example:
```python
assert a == b
assert c
assert d in e
```  
Refactoring / Solution: Split tests; add assertion messages; use helper asserts; rename tests to intent.  
Related Patterns: Given–When–Then test style; Specification-by-example.  
Sources: Test smell catalogs. citeturn0search11turn4search0  

**Shared Fixture / Inter-test Coupling**  
Category: Testing  
Description: Tests share mutable state (DB rows, cache, filesystem), making them order-dependent and fragile. citeturn4search0turn0search11  
Symptoms: Pass individually but fail as suite; need “reset database” rituals.  
Why It’s Bad: Eliminates isolation; makes failures nondeterministic.  
Detection Heuristics: Shared global fixtures; tests not cleaning up; reliance on previous test artifacts.  
Severity: High.  
Example:
```python
# test_a inserts user; test_b assumes user exists
```  
Refactoring / Solution: One test = one fixture; transactional test isolation; hermetic environments.  
Related Patterns: Test containers; ephemeral environments.  
Sources: Test smell surveys. citeturn4search0turn0search11  

### Data / Database Anti-Patterns

**Entity-Attribute-Value (EAV)**  
Category: Data  
Description: A schema stores attributes as rows (entity, attribute, value) rather than columns, trading structure for flexibility but causing query complexity and loss of constraints; it is explicitly listed as an antipattern in SQL Antipatterns’ logical design section. citeturn17view0turn4search5  
Symptoms: Everything becomes joins and pivots; datatype constraints vanish; indexing becomes hard.  
Why It’s Bad: Performance and correctness problems; schema becomes opaque; prevents relational constraints.  
Detection Heuristics: Presence of “attribute/value” tables; polymorphic value columns; frequent pivot logic; sparse indexing.  
Severity: High.  
Example:
```sql
-- attributes stored as rows
(entity_id, attr_name, attr_value)
```  
Refactoring / Solution: Model frequent attributes as columns; use dependent tables for multi-valued attributes; consider JSON only where justified (and indexed).  
Related Patterns: Schema-per-service (microservices) for ownership clarity; CQRS read models. citeturn1search2turn1search6  
Sources: SQL Antipatterns ToC and logical design antipattern list. citeturn17view0turn4search5  

**Polymorphic Associations (Dual-Purpose Foreign Key)**  
Category: Data  
Description: One foreign key column references multiple parent tables, typically via an extra “type” column; explicitly listed in SQL Antipatterns. citeturn17view0turn4search5  
Symptoms: No real FK constraints; orphan rows; complex joins and conditional logic.  
Why It’s Bad: Referential integrity not enforceable; migrations are risky.  
Detection Heuristics: `parent_id + parent_type`; lack of FK constraints; application-level integrity checks.  
Severity: High.  
Example:
```sql
(parent_type='ORDER', parent_id=123)
```  
Refactoring / Solution: Separate association tables per parent; or use supertype table with strict FK; redesign domain relationships.  
Related Patterns: Table inheritance patterns; DDD aggregates. citeturn5search0turn17view0  
Sources: SQL Antipatterns logical design antipattern list. citeturn17view0turn4search5  

**Naive Trees**  
Category: Data  
Description: Hierarchies are modeled in ways that make querying ancestors/descendants expensive or limited, often leading teams to impose arbitrary depth limits; the SQL Antipatterns extract explicitly describes recognition questions. citeturn4search0turn17view0  
Symptoms: “How many levels do we support?”; complex recursion emulation; frequent self-joins. citeturn4search0  
Why It’s Bad: Queries scale poorly; constraints become ad hoc; maintenance fear emerges. citeturn4search0  
Detection Heuristics: Adjacency list with repeated self-joins; “level” columns; depth assumptions in code.  
Severity: Medium → High (depends on hierarchy size and query load).  
Example:
```sql
-- parent_id adjacency list; depth-limited traversal in application
```  
Refactoring / Solution: Use alternative tree models (closure table, nested sets, path enumeration) according to query patterns. citeturn4search0turn4search7  
Related Patterns: Materialized paths (data modeling); CQRS read models. citeturn1search6  
Sources: SQL Antipatterns extract. citeturn4search0  

**Index Shotgun**  
Category: Data  
Description: Indexes are created “without a plan,” often by adding many indexes reactively; listed explicitly in SQL Antipatterns. citeturn17view0turn4search7  
Symptoms: Write performance degrades; index bloat; inconsistent query plans.  
Why It’s Bad: Indexes are not free—maintenance cost grows; can worsen overall performance.  
Detection Heuristics: Many overlapping indexes; high index-to-table ratio; indexes unused in query plans.  
Severity: Medium → High.  
Example:
```sql
CREATE INDEX ... ON users(col1);
CREATE INDEX ... ON users(col2);
CREATE INDEX ... ON users(col1, col2); -- proliferation
```  
Refactoring / Solution: Measure query patterns; consolidate indexes; remove unused; fix queries first (avoid `SELECT *`).  
Related Patterns: Observability (slow query logs), performance profiling.  
Sources: SQL Antipatterns and modern DB antipattern survey work. citeturn17view0turn4search16  

**Spaghetti Query**  
Category: Data  
Description: A complex problem is attempted in a single, unreadable SQL statement; explicitly listed in SQL Antipatterns query antipatterns and framed as “solve a complex problem in one step.” citeturn4search7turn17view0  
Symptoms: Nested subqueries; hard-to-test query; fragile to schema changes.  
Why It’s Bad: Hard to reason about correctness/performance; encourages copy-paste variants.  
Detection Heuristics: Query length/AST size; nested depth; repeated correlated subqueries; hard-coded business rules in SQL.  
Severity: Medium → High.  
Example:
```sql
SELECT ... FROM ... WHERE ... (SELECT ... (SELECT ...))
```  
Refactoring / Solution: Divide-and-conquer (CTEs, views); materialize intermediate results; move business logic to coherent layer with tests.  
Related Patterns: CQRS read models; query objects. citeturn1search6  
Sources: SQL Antipatterns query antipattern list. citeturn17view0turn4search7  

**Random Selection (ORDER BY RAND() / RANDOM())**  
Category: Data  
Description: Fetching a random row by randomly sorting the whole table; a recognized SQL antipattern with dedicated extract. citeturn4search1turn4search13  
Symptoms: Queries get slower as table grows; full scan + sort.  
Why It’s Bad: O(n log n) scaling; can be catastrophic on large tables.  
Detection Heuristics: `ORDER BY RAND()`/`RANDOM()`; full table sort in query plan.  
Severity: High (for large datasets).  
Example:
```sql
SELECT * FROM users ORDER BY RANDOM() LIMIT 1;
```  
Refactoring / Solution: Use indexed random selection strategies (sample keys, table sampling, precomputed random ids).  
Related Patterns: Caching; precomputed materialized views.  
Sources: SQL Antipatterns extract and educational research on SQL antipattern awareness. citeturn4search1turn4search13  

**SQL Injection**  
Category: Data  
Description: User input is concatenated into SQL strings, allowing adversarial input to change query semantics; explicitly an SQL Antipatterns application antipattern with extract. citeturn4search2turn17view0  
Symptoms: String concatenation in SQL; inconsistent escaping; security incidents.  
Why It’s Bad: Security vulnerability; data exfiltration and corruption risk.  
Detection Heuristics: SQL strings built with `+`/formatting; unparameterized queries; tainted input flows to query builder.  
Severity: Critical.  
Example:
```python
sql = f"SELECT * FROM users WHERE name='{name}'"
```  
Refactoring / Solution: Parameterized queries; prepared statements; validate at boundary; least-privilege DB accounts.  
Related Patterns: Repository; Query Objects.  
Sources: SQL Antipatterns extract and ToC. citeturn4search2turn17view0  

### Dependency Anti-Patterns

**Unstable Dependency (Depend on Volatile Components)**  
Category: Architecture  
Description: Stable components depend on unstable ones, causing volatility to propagate; Unstable Dependency is a core architecture smell detected by tools like Arcan and studied empirically. citeturn11search21turn11search6turn11search13  
Symptoms: Frequent changes in leaf modules force changes upstream; core becomes fragile.  
Why It’s Bad: Increases maintenance cost and reduces testability/maintainability correlations observed for smells. citeturn11search29turn11search25  
Detection Heuristics: Instability metrics (fan-in/out), edges from stable to unstable; Arcan detector output. citeturn11search6turn11search21  
Severity: High.  
Example:
```text
core-domain -> experimental-ui-widget-lib
```  
Refactoring / Solution: Apply DIP; invert dependency via interface; isolate unstable behind adapters. citeturn0search17turn0search0  
Related Patterns: DIP; Anti-corruption layer when external volatility is source. citeturn1search0turn0search17  
Sources: Architectural smell catalogs and tool literature. citeturn11search21turn11search6  

**Version Pinning / Dependency Hell**  
Category: Architecture  
Description: Dependency graph becomes unmanageable due to incompatible versions, lockfiles, and tight transitive constraints; upgrades become “big bang” events.  
Symptoms: Inability to upgrade one library without many; frequent “works on my machine.”  
Why It’s Bad: Security patches delayed; builds become fragile; deployment risk increases.  
Detection Heuristics: High transitive depth; conflicting constraints; frequent lockfile conflicts; large “allowlist” of exceptions.  
Severity: High.  
Example:
```text
libA requires X<2; libB requires X>=2 (deadlock)
```  
Refactoring / Solution: Dependency hygiene; reduce surface area; modularize; adopt compatibility policies; isolate via adapters.  
Related Patterns: Adapter; Semantic Versioning practices.  
Sources: This is a widely observed ecosystem failure mode; for infra drift/“works on my machine” parallels, see configuration drift discussion. citeturn16search20turn16search36  

### Performance Anti-Patterns

**Chatty I/O (Excess Roundtrips)**  
Category: Performance  
Description: Many small calls to a remote resource (DB/service/storage) instead of fewer coarse-grained operations. Microsoft’s cloud performance anti-pattern catalog includes “Chatty I/O.” citeturn8view0  
Symptoms: High latency; low throughput; p95 grows with distance.  
Why It’s Bad: Network and serialization overhead dominate; tail latencies explode.  
Detection Heuristics: Tracing shows many remote spans; N+1 query patterns; repeated single-row requests.  
Severity: High.  
Example:
```text
for each item: fetch price from DB (1000 queries)
```  
Refactoring / Solution: Batch; use joins where safe; add caching; introduce read models.  
Related Patterns: API Gateway aggregation; CQRS read model. citeturn1search22turn1search6  
Sources: Microsoft performance anti-pattern catalog. citeturn8view0  

**Extraneous Fetching / Over-fetching**  
Category: Performance  
Description: Fetching more data than needed (wide “select *”, oversized payloads). Microsoft lists “Extraneous fetching.” citeturn8view0  
Symptoms: Large payload sizes; high memory pressure; slow serialization.  
Why It’s Bad: Wastes resources and increases latency/cost.  
Detection Heuristics: Overly broad select/projections; unused fields in API responses; payload-size telemetry.  
Severity: Medium → High.  
Example:
```sql
SELECT * FROM orders WHERE id = ?
```  
Refactoring / Solution: Explicit projections; shape APIs; pagination; introduce DTOs.  
Related Patterns: CQRS; DTO pattern. citeturn1search6  
Sources: Microsoft performance anti-pattern catalog. citeturn8view0  

**Improper Caching / No Caching**  
Category: Performance  
Description: Caching is absent where needed or implemented incorrectly (wrong TTL, wrong key, stale invalidation), creating correctness risks. Microsoft catalog includes caching anti-patterns. citeturn8view0  
Symptoms: Hot endpoints fully recompute; caches serve stale/conflicting data; “cache stampede.”  
Why It’s Bad: Poor performance and subtle correctness bugs.  
Detection Heuristics: Expensive calls repeated; TTL mismatch; missing invalidation events; stampede under load.  
Severity: Medium → High.  
Example:
```text
Cache key ignores user_id -> serves another user’s data (critical)
```  
Refactoring / Solution: Define caching strategy per data class; add request coalescing; consider write-through/aside patterns.  
Related Patterns: Cache-Aside; Read-through; CQRS read store.  
Sources: Microsoft cloud performance anti-pattern catalog. citeturn8view0  

### Maintainability Anti-Patterns

**Shotgun Surgery**  
Category: Code  
Description: One conceptual change requires many small edits across many modules; Fowler lists it as a smell and refactoring trigger. citeturn14view0turn11search35  
Symptoms: PR touches many files for one feature; repeated similar edits; high co-change. citeturn11search35  
Why It’s Bad: Increases regression risk; slows delivery; indicates missing modular boundaries.  
Detection Heuristics: Co-change clustering in VCS; high fan-out changes; repeated string/field edits.  
Severity: High.  
Example:
```text
Change “tax rule” requires edits in 12 modules
```  
Refactoring / Solution: Move Function/Field to co-locate change; Extract Class; “put things that change together.” citeturn11search35turn15search17  
Related Patterns: SRP; bounded context boundaries. citeturn15search17turn5search0  
Sources: Fowler smell and candidate refactorings in teaching materials. citeturn14view0turn11search35  

**Divergent Change**  
Category: Code  
Description: One module changes for many unrelated reasons; the opposite of shotgun surgery in Fowler’s framing. citeturn14view0turn11search35  
Symptoms: Same file touched for UI changes, DB changes, and business rule changes; “everything depends on it.”  
Why It’s Bad: Indicates SRP violation and predicts growing complexity. citeturn15search17turn14view0  
Detection Heuristics: Change reason clustering shows many clusters for same file; module contains varied dependencies.  
Severity: High.  
Example:
```text
orders.py changes for pricing, shipping, persistence, and UI (“god module”)
```  
Refactoring / Solution: Extract Class/Module; split by reason-to-change; enforce layer separation. citeturn14view1turn15search17  
Related Patterns: SRP; modularization principles. citeturn15search17  
Sources: Fowler smell list and refactoring catalog. citeturn14view0turn14view1  

**Dead Code (Proliferation of Unused Paths)**  
Category: Code  
Description: Code that is never executed/used but remains deployed; increases confusion and risk. citeturn11search34turn14view1  
Symptoms: Unreferenced modules; feature flags abandoned; deprecated endpoints still live.  
Why It’s Bad: Raises maintenance and security risk; complicates refactoring; can hide vulnerabilities.  
Detection Heuristics: No call sites; low coverage; runtime telemetry shows zero hits; static analysis “unused.”  
Severity: Medium → High (Critical if dead code contains exploitable endpoints).  
Example:
```python
def old_payment_flow(): ...
```  
Refactoring / Solution: Remove Dead Code (explicit refactoring); instrument then delete; sunset with feature flags. citeturn14view1turn11search34  
Related Patterns: Strangler Fig (gradual replacement). citeturn9search30  
Sources: Fowler refactoring list includes “Remove Dead Code”; modern anti-pattern discussions. citeturn14view1turn11search34  

### Organizational / Process Anti-Patterns

**Mushroom Management**  
Category: Architecture  
Description: Information is withheld (“keep them in the dark”), creating misalignment and forcing local optimizations that become technical debt. This appears in AntiPatterns organizational anti-patterns lists. citeturn11search10turn11search14  
Symptoms: Surprises late in delivery; unclear requirements; lack of architectural decisions recorded.  
Why It’s Bad: Encourages quick hacks; destroys long-term quality and predictability.  
Detection Heuristics: Not code-detectable; proxy signals include high rework, unclear ownership, frequent “urgent changes.”  
Severity: High.  
Example:
```text
Team learns integration constraint in final week, patches around it everywhere
```  
Refactoring / Solution: Decision records; transparent roadmaps; shared architecture reviews; shorten feedback loops.  
Related Patterns: Conway’s Law awareness (organizational-architecture alignment).  
Sources: AntiPatterns organizational catalog. citeturn11search10turn11search14  

**Manual Deployments (DevOps Anti-Pattern)**  
Category: Architecture  
Description: Deployments done manually lack consistency and increase human error; AWS DevOps guidance explicitly labels manual deployments as an anti-pattern for continuous delivery. citeturn16search3  
Symptoms: “Click ops”; inconsistent procedures; long release windows.  
Why It’s Bad: Slows delivery; creates configuration drift; increases incident rate. citeturn16search3turn16search20  
Detection Heuristics: No pipeline evidence; scripts run manually; approvals logged outside automation; drift detection alerts.  
Severity: High → Critical (critical in regulated/high-availability systems).  
Example:
```text
Release runbook in wiki; only 2 people can do it
```  
Refactoring / Solution: Automate pipeline; infrastructure as code; progressive delivery with observability gates. citeturn16search3turn16search19turn16search1  
Related Patterns: Deployment pipeline; GitOps (as controlled desired state).  
Sources: AWS DevOps anti-pattern guidance and SRE toil framing. citeturn16search3turn16search1  

**Toil Accumulation (Operations as Manual Work)**  
Category: Architecture  
Description: Operational work becomes predominantly manual, repetitive, automatable, tactical, and scales linearly; the SRE book defines “toil” with these attributes. citeturn16search1turn16search5turn16search9  
Symptoms: Ops engineers spend time restarting services, applying repetitive changes, chasing non-actionable alerts.  
Why It’s Bad: Consumes engineering time that should improve reliability; produces burnout and “hero” anti-patterns. citeturn16search1turn16search5  
Detection Heuristics: Ticket taxonomy; repeated manual runbooks; alert volume not correlated with incidents; lack of automation.  
Severity: High.  
Example:
```text
Daily manual schema change + manual rollback practice
```  
Refactoring / Solution: Automate; reduce alerts; self-service; invest in reliability engineering.  
Related Patterns: Error budgets and SLO-driven prioritization (SRE practice).  
Sources: SRE toil definition in Google SRE book/workbook. citeturn16search1turn16search5  

## Priority views for building AI agents

### Top twenty-five most important anti-patterns

Selection criterion: high impact on cost-of-change, reliability/security, and systemic change amplification. (The ordering is pragmatic; exact rank is context-dependent.)

| Rank | Anti-pattern | Why “important” (impact summary) | Typical category |
|---:|---|---|---|
| 1 | Big Ball of Mud | System-wide unpredictability; modernization becomes nearly impossible. citeturn3search11 | Architecture |
| 2 | Distributed Monolith | Worst of both worlds: tight coupling + distributed failures. citeturn4search15 | Microservices |
| 3 | Shared Database (microservices) | Kills service autonomy; creates systemic blast radius. citeturn1search29 | Microservices |
| 4 | Cyclic Dependencies | Strong predictor of rising complexity and hard refactors. citeturn11search2 | Architecture |
| 5 | Unstable Dependency | Volatility propagates into “stable core,” raising maintenance cost. citeturn11search6 | Architecture |
| 6 | Hub-like Dependency / God Component | Central bottleneck; high change amplification. citeturn11search13 | Architecture |
| 7 | God Object / Blob | SRP collapse; drives widespread coupling and brittle design. citeturn11search14turn15search17 | Design |
| 8 | Shotgun Surgery | Changes become high-risk and expensive. citeturn14view0 | Code |
| 9 | Divergent Change | One module becomes the change hotspot; architecture erodes. citeturn14view0 | Code |
| 10 | Swallowed Exceptions | Turns failures into silent corruption; destroys diagnosability. citeturn11search3 | Code |
| 11 | SQL Injection | Critical security exposure. citeturn4search2 | Data |
| 12 | Over-mocking | Locks design; makes refactoring expensive. citeturn4search0 | Testing |
| 13 | Flaky Tests | CI becomes noisy; teams ignore failures. citeturn0search11 | Testing |
| 14 | Slow Test Suite | Feedback loop collapse; encourages risky batching. citeturn16search3 | Testing |
| 15 | Manual Deployments | Drift + human error + slow delivery; directly called out as anti-pattern. citeturn16search3 | Architecture |
| 16 | Configuration Drift / Snowflake Infrastructure | Replication/debug failures; inconsistent environments. citeturn16search20turn16search36 | Architecture |
| 17 | Chatty Services | Latency and brittleness (microservices). citeturn1search3turn8view0 | Microservices |
| 18 | Synchronous Cascades (no timeouts) | Systemic outages via cascade failures. citeturn1search6turn7search18 | Microservices |
| 19 | Anemic Domain Model | Encapsulation failure; grows into script-based design. citeturn3search10 | Design |
| 20 | Fat Interfaces (ISP violation) | Coupling and redeploy cost; hurts modularity. citeturn15search3 | Design |
| 21 | Primitive Obsession | Missing invariants; semantic drift. citeturn14view0 | Design |
| 22 | Long Function | Local complexity and testing cost. citeturn18search9turn14view0 | Code |
| 23 | Repeated Switches | OCP violations; scattered edits per new variant. citeturn0search18turn14view0 | Code |
| 24 | Spaghetti Query | Correctness/performance risk; DB becomes opaque. citeturn17view0 | Data |
| 25 | EAV | Constraint loss and query complexity; performance problems. citeturn17view0 | Data |

### Top twenty-five most detectable anti-patterns

Selection criterion: high precision and strong static/dynamic signals available to an automated agent.

| Rank | Anti-pattern | Why “detectable” | Common detectors/sensors |
|---:|---|---|---|
| 1 | Long Function | Statement counts + complexity metrics. citeturn18search9turn18search6 | AST + metrics |
| 2 | Too many branches / deep nesting | Branch counts; nesting depth; lint rules. citeturn18search2turn18search32 | AST + lints |
| 3 | Dead code | Unused symbols; zero runtime hits; coverage gaps. citeturn14view1 | Static + telemetry |
| 4 | Swallowed exceptions | Empty catch blocks and broad catches. citeturn11search3 | AST |
| 5 | Magic literals | Literal repetition and “suspicious constants.” citeturn11search3 | AST |
| 6 | Long parameter list | Parameter count; repeated arg clusters. citeturn18search24turn14view0 | Lints + AST |
| 7 | Data clumps | Frequent parameter co-occurrence. citeturn14view0 | AST + mining |
| 8 | Duplicate code / copy-paste (if enabled) | Clone detection (token/AST). citeturn11search30turn11search3 | Clone detectors |
| 9 | Cyclic dependencies | Graph cycle detection. citeturn11search2turn11search21 | Dependency graph |
| 10 | Hub-like dependency | Centrality metrics; tool detectors. citeturn11search21turn11search37 | Graph metrics |
| 11 | Unstable dependency | Instability metrics; tool detectors. citeturn11search6turn11search21 | Graph metrics |
| 12 | SQL injection | Taint flows to query strings; pattern match. citeturn4search2 | Static taint |
| 13 | Random selection queries | `ORDER BY RAND/RANDOM`. citeturn4search13 | SQL lint |
| 14 | Spaghetti query | Query length/AST depth thresholds. citeturn17view0 | SQL parse |
| 15 | EAV schema | Known table patterns (attr/value). citeturn17view0 | Schema scan |
| 16 | Polymorphic association | `(type,id)` FK pattern. citeturn17view0 | Schema scan |
| 17 | Index shotgun | Overlapping indexes; unused indexes. citeturn17view0turn4search16 | DB stats |
| 18 | Chatty I/O | Trace span count; N+1 patterns. citeturn8view0 | Tracing |
| 19 | Extraneous fetching | Response-field utilization; payload sizes. citeturn8view0 | Telemetry |
| 20 | Shared database (microservices) | Shared connection strings/schema usage. citeturn1search29 | Config scan |
| 21 | Manual deployments | Pipeline absence + operational logs. citeturn16search3 | CI metadata |
| 22 | Toil | Ticket taxonomy + repeated runbooks (proxy). citeturn16search1 | Ops data |
| 23 | Over-mocking | Mock count/interaction assertions. citeturn4search0 | Test AST |
| 24 | Flaky tests | Historical failure variance (stats). citeturn0search11 | CI history |
| 25 | Slow suite | Test timing telemetry. citeturn16search19 | CI telemetry |

## Anti-pattern mappings

### Anti-pattern to refactoring/pattern mapping

This mapping is intentionally biased toward (a) refactorings explicitly named in Fowler’s refactoring catalog (Extract Function, Introduce Parameter Object, Replace Primitive with Object, etc.), and (b) system-level patterns used in modernization/microservices to recover autonomy (Database per Service, Saga, API Gateway/BFF, Anti-Corruption Layer). citeturn14view1turn1search2turn1search1turn1search3turn1search0turn9search30

| Anti-pattern | Primary refactoring / solution pattern(s) |
|---|---|
| Long Function | Extract Function; Split Phase; Introduce Parameter Object. citeturn14view1 |
| Deep Nesting | Guard clauses; Extract Function; Strategy/State. citeturn14view1turn5search10 |
| Repeated Switches | Replace Conditional with Polymorphism (Strategy/State); Substitute Algorithm. citeturn14view1turn5search10 |
| Global Data / Mutable Data | Encapsulate Variable; Encapsulate Record/Collection; dependency injection. citeturn14view1 |
| Long parameter list / Data clumps | Introduce Parameter Object; Encapsulate Record. citeturn14view1 |
| Feature envy | Move Function; Hide Delegate. citeturn14view1turn11search0 |
| God Object / Blob | Extract Class; Move Function/Field; enforce bounded responsibilities. citeturn14view1turn11search14 |
| Shotgun surgery | Move Function/Field to cohesion; Extract Class; reduce cross-cutting edits. citeturn11search35turn14view1 |
| Divergent change | Extract Class; Split module by reason-to-change. citeturn14view1 |
| Dead code / Lava flow | Remove Dead Code; Strangler Fig for legacy replacement; telemetry-based deletion. citeturn14view1turn9search30 |
| Layering violations | Apply DIP; Ports & Adapters; enforce dependency rules. citeturn0search17turn0search1 |
| Cyclic dependencies | Break cycles by interface extraction; move shared abstractions; invert dependencies. citeturn11search2turn0search17 |
| Hub-like dependency | Decompose hub; introduce explicit facades; separate stable abstractions. citeturn11search6turn1search0 |
| Unstable dependency | Apply DIP/abstractions; isolate volatility behind adapters/ACL. citeturn11search6turn1search0turn0search17 |
| Distributed monolith | Re-cut boundaries (bounded contexts); async messaging; database per service; strangler for gradual adoption. citeturn5search0turn1search2turn9search30 |
| Shared database (microservices) | Database per Service; Saga; API Composition for queries. citeturn1search2turn1search1turn1search11 |
| Chatty services | API Gateway/BFF; API Composition; caching; reduce roundtrips. citeturn1search3turn1search11turn8view0 |
| No ACL | Anti-Corruption Layer (adapter/facade boundary). citeturn1search0turn1search4 |
| Flaky tests | Hermetic tests; control time; isolate state; deterministic fakes. citeturn0search11turn4search0 |
| Over-mocking | Behavioral tests; contract tests; fakes; test boundaries not internals. citeturn4search0turn1search6 |
| Slow test suite | Test pyramid discipline; parallelization; reduce E2E scope. citeturn16search19turn1search6 |
| EAV | Normalize frequent attributes; model as dependent tables; constrain types. citeturn17view0turn4search5 |
| Polymorphic associations | Separate association tables; enforce FKs; structured domain modeling. Almost all technical “mappings” between anti-patterns and refactorings are many-to-many, and they are only valid if the *symptoms* match. Overconfident one-to-one mappings are a common failure mode in AI code review agents (they produce “cargo cult refactors” that move code around without changing the underlying coupling). The catalog therefore always keeps an explicit symptom gate and, where applicable, recommends *instrument-first* approaches (telemetry, tracing, churn analysis) before major architectural moves. citeturn18search14turn11search33turn16search1

### Anti-pattern to SOLID violation mapping

SOLID definitions are taken from canonical essays/articles (OCP/DIP) and SRP clarifications. citeturn15search17turn0search6turn0search17turn15search2turn15search3

Legend: SRP, OCP, LSP, ISP, DIP.

| Anti-pattern | Primary SOLID violation(s) | Notes |
|---|---|---|
| God Object / Blob | SRP (primary), often ISP | One class acts for many “actors.” citeturn15search17 |
| Divergent change | SRP | Multiple reasons-to-change in one module. citeturn15search17 |
| Shotgun surgery | SRP (emergent), DIP (sometimes) | Responsibility scattered; indicates missing boundary abstraction. citeturn15search17turn0search17 |
| Fat interface | ISP | Definition: clients forced to depend on methods they don’t use. citeturn15search3 |
| Refused bequest | LSP | Subtype not substitutable. citeturn15search2 |
| Repeated switches | OCP | New variant forces edits to existing code. citeturn0search6turn0search18 |
| Layering violation | DIP | High-level policies depend on low-level details. citeturn0search17 |
| Unstable dependency | DIP (system-level) | Stability direction is the architectural analogue of DIP. citeturn11search6turn0search17 |
| Feature envy / inappropriate intimacy | SRP + DIP (often), ISP (sometimes) | Misassigned responsibilities and boundary leakage. citeturn11search0turn14view0turn0search17 |
| Anemic domain model | SRP/encapsulation-related (not strictly SOLID-only) | Domain objects lose cohesive responsibility. citeturn3search10turn5search0 |
| SQL injection | N/A | Security defect; not a SOLID mapping issue. citeturn4search2 |
| Manual deployments / toil | N/A | Process/ops anti-patterns; SOLID not directly applicable. citeturn16search3turn16search1 |

## References

Key definitions and catalogs used repeatedly across the above entries include: code smell definition and origins, Fowler’s smell/refactoring naming in Refactoring 2nd edition, Suryanarayana’s PHAME-based design smell classification, database anti-pattern catalogs from SQL Antipatterns, microservices patterns/anti-patterns from microservices.io, cloud performance anti-patterns from Microsoft, DevOps/CD anti-patterns from AWS guidance, and operational toil definition from Google SRE. citeturn12search4turn14view0turn14view1turn11search5turn11search16turn17view0turn4search5turn1search29turn1search2turn8view0turn16search3turn16search1