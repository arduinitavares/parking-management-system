# Software Engineering Anti-Pattern Catalog (up to March 2026)

## 1. Overview

This report presents a consolidated catalog of software engineering anti-patterns across code-level, object-oriented design, architecture, microservices, testing, and data/database domains, synthesized from classic sources (Fowler, GoF, Suryanarayana), Clean Code/Architecture guidance, static analysis rule sets, and recent academic and industrial literature up to March 2026.[^1][^2][^3][^4][^5][^6][^7][^8]
Anti-patterns are organized for use in learning, static analysis tooling, AI code-review agents, and architecture assessment, with a consistent schema per anti-pattern.

## 2. Categorized Taxonomy

### 2.1 Top-Level Categories

The catalog uses the following top-level categories (anti-patterns may belong to multiple categories):

- Code-Level Anti-Patterns
- Object-Oriented Design Anti-Patterns
- Architecture Anti-Patterns
- Microservices Anti-Patterns
- Testing Anti-Patterns
- Data / Database Anti-Patterns
- Dependency Anti-Patterns
- Performance Anti-Patterns
- Maintainability Anti-Patterns (cross-cutting)
- Organizational / Process Anti-Patterns (limited coverage)

### 2.2 Anti-Patterns by Category

#### Code-Level Anti-Patterns

- Duplicated Code (DRY Violation)  
- Long Method  
- Large Class  
- Long Parameter List  
- Feature Envy[^2][^9][^10][^1]
- Data Clumps[^9][^2]
- Primitive Obsession  
- Magic Numbers / Strings  
- Dead Code / Dead Function[^5]
- God Condition (Complex Conditional)  
- Inconsistent Naming  

#### Object-Oriented Design Anti-Patterns

- God Class / God Object[^3][^11]
- Divergent Change[^2]
- Shotgun Surgery[^12][^2]
- Inappropriate Intimacy[^10]
- Message Chains (Train Wreck / Law of Demeter Violation)[^10]
- Middle Man[^10]
- Refused Bequest  
- Parallel Inheritance Hierarchies[^12][^10]
- Anemic Domain Model  
- Service Locator  

#### Architecture Anti-Patterns

- Big Ball of Mud  
- Layer Skipping / Bypassed Layers  
- Unstable Interface / Unstable Dependency[^4][^13]
- Cyclic Package / Module Dependencies[^4]
- Hardcoded Environment / Configuration  
- Shared Library as Integration Point (God Library)  

#### Microservices Anti-Patterns

- Distributed Monolith[^14][^15][^16][^17]
- Shared Database / Shared Schema Integration[^16][^8][^14]
- Chatty Services / Chatty Interfaces[^15][^18][^17][^11][^14]
- Nanoservices (Over-Decomposition)  
- Wrong Bounded Context / Entity Service[^15]
- Synchronous Dependency Chain (Deep Synchronous Call Graph)[^14][^15]
- Smart UI / API Gateway God Service  

#### Testing Anti-Patterns

- Fragile / Brittle Tests (Low "resistance to refactoring")[^19][^20]
- Flaky Tests  
- Over-Mocking / Mockery[^21][^20][^22][^19]
- Mystery Guest[^23][^22]
- Slow Tests  
- Assertion Roulette[^22]

#### Data / Database Anti-Patterns

- God Table[^6][^7]
- Entity-Attribute-Value (EAV) Abuse  
- Polymorphic Association Table  
- Overloaded Column / Semantic Overloading  
- Shared Database / Shared Schema Integration (also microservices)[^8]

#### Dependency Anti-Patterns

- Cyclic Package / Module Dependencies[^4]
- Concrete Dependency (Ignoring Dependency Inversion)  
- Hidden Temporal Coupling  
- Service Locator (also design)  

#### Performance Anti-Patterns

- N+1 Query  
- Chatty Remote Calls / Chatty Services[^17][^11][^14]
- Synchronous Dependency Chain (also microservices)  
- Premature Optimization  

#### Maintainability Anti-Patterns (Cross-Cutting Tags)

These are tags applied across the catalog, not separate entries:

- Low Cohesion
- High Coupling
- Poor Separation of Concerns
- Lack of Encapsulation
- Low Testability
- High Change-Proneness / Error-Proneness[^13][^4]

## 3. Master Anti-Pattern Catalog

Each anti-pattern below is presented with a fixed schema suitable for rule design and AI-based detection.

***

### 3.1 Duplicated Code (DRY Violation)

- **Category**: Code, Maintainability, Performance  
- **Description**: The same or very similar logic appears in multiple locations instead of being factored into a single abstraction.[^9][^5][^2]
- **Symptoms**:  
  - Copy–paste blocks differing only slightly (e.g., literals, variable names).  
  - Parallel changes required across multiple files when requirements evolve.  
  - Inconsistent behavior because only some clones were updated.  
- **Why It’s Bad**: Increases change effort, introduces divergence bugs, and complicates reasoning about behavior; changes become error-prone and expensive.  
- **Detection Heuristics**:  
  - Textual or token-based clone detection (Type 1–3 clones).  
  - High similarity subtrees in AST across different locations.  
  - Lint rule: same sequence of method calls or conditionals repeated in multiple functions.  
- **Severity**: High (escalates with clone size and spread).  
- **Example** (pseudocode):  
  ```python
  def calculate_invoice_total(lines):
      total = 0
      for line in lines:
          total += line.price * (1 + line.tax_rate)
      return total

  def calculate_quote_total(lines):  # duplicated logic
      total = 0
      for line in lines:
          total += line.price * (1 + line.tax_rate)
      return total
  ```  
- **Refactoring / Solution**: Extract shared logic into a single function or class (Extract Method, Extract Class), parameterize behavior where needed, and remove clones.[^24][^9]
- **Related Patterns**: Template Method, Strategy, Composite.  
- **Sources**: Fowler – Refactoring; Industrial Logic "Smells to Refactorings" quick reference; Clean Code smells and heuristics.[^5][^2][^9]

***

### 3.2 Long Method

- **Category**: Code, Maintainability  
- **Description**: A method or function is too long, performing multiple responsibilities instead of one coherent task.[^2][^9][^5]
- **Symptoms**:  
  - Many lines of code (context-dependent, but often 30+ in high-level languages).  
  - Mixed levels of abstraction (high-level orchestration and low-level details together).  
  - Difficult to name the method succinctly.  
- **Why It’s Bad**: Reduces readability, testability, and reuse; increases cognitive load and makes local changes risky.  
- **Detection Heuristics**:  
  - Thresholds on LOC, cyclomatic complexity, or nesting depth.  
  - Multiple distinct logical segments (comments like `// step 1`, `// step 2`) inside a single method.  
  - Many local variables and branches.  
- **Severity**: Medium to High (depending on complexity and criticality).  
- **Example**: A controller method that validates input, queries multiple repositories, applies complex business rules, and builds responses in one function.  
- **Refactoring / Solution**: Extract Method, Introduce Parameter Object, Move Method to domain objects, Split Phase.[^9][^2]
- **Related Patterns**: Facade (if method represents external API and delegates); Command.  
- **Sources**: Fowler – Refactoring; Industrial Logic smell catalog; Clean Code function guidelines.[^5][^2][^9]

***

### 3.3 Large Class

- **Category**: Code, Design, Maintainability  
- **Description**: A class or module has too many responsibilities, fields, or methods, effectively acting as a mini-god object.[^11][^3][^2]
- **Symptoms**:  
  - High LOC, many fields, many public methods.  
  - Methods that operate on disjoint subsets of fields.  
  - Multiple unrelated concerns mixed (e.g., persistence, UI, business rules).  
- **Why It’s Bad**: Violates Single Responsibility Principle (SRP), increases coupling, and becomes a hotspot for bugs and change conflicts.  
- **Detection Heuristics**:  
  - LOC and method-count thresholds per class.  
  - Low cohesion metrics (e.g., LCOM), clusters of methods using disjoint field groups.  
  - High fan-in and fan-out relative to other classes.  
- **Severity**: High.  
- **Example**: A `UserManager` class that handles authentication, authorization, profile CRUD, email sending, and reporting.  
- **Refactoring / Solution**: Extract Class, Extract Module, move responsibilities into cohesive domain services or entities, introduce interfaces around distinct responsibilities.[^3][^9]
- **Related Patterns**: Facade, Service, Repository, Domain Service.  
- **Sources**: Fowler code smells; Suryanarayana structural design smells (God Class, Multifaceted Abstraction); Clean Code SRP guidance.[^3][^2][^5]

***

### 3.4 Long Parameter List

- **Category**: Code, Design  
- **Description**: Methods accept many parameters, often with related values that conceptually belong together.[^2][^5]
- **Symptoms**:  
  - 4+ parameters regularly, especially with multiple booleans or related fields.  
  - Many overloads that differ only slightly.  
- **Why It’s Bad**: Hard to call correctly, encourages duplication at call sites, and hides missing abstractions (e.g., value objects).  
- **Detection Heuristics**:  
  - Parameter-count thresholds on method signatures.  
  - Presence of multiple boolean or enum flags.  
  - Calls where many parameters are literals.  
- **Severity**: Medium.  
- **Example**: `create_user(name, email, street, city, zip, country, is_admin, is_active, send_welcome_email)`  
- **Refactoring / Solution**: Introduce Parameter Object, encapsulate related fields in value objects, use configuration objects or builders where appropriate.[^2]
- **Related Patterns**: Builder, Value Object.  
- **Sources**: Fowler – Long Parameter List; Clean Code function argument heuristics.[^5][^2]

***

### 3.5 Feature Envy

- **Category**: Code, Design  
- **Description**: A method uses more data from another object/module than from its own, indicating misplaced behavior.[^1][^9][^10][^2]
- **Symptoms**:  
  - Method performs long sequences of `other.getX()` / `other.y()` calls.  
  - Domain logic implemented in service classes instead of the data-owning entities.  
- **Why It’s Bad**: Increases coupling, reduces cohesion, and makes changes require touching distant classes; harms encapsulation.  
- **Detection Heuristics**:  
  - Count field/method accesses grouped by target type; flag methods where accesses to another type dominate.  
  - Law-of-Demeter violations combined with foreign data usage.  
- **Severity**: Medium to High (especially in domain code).  
- **Example**: Order-total calculations implemented in `OrderService` but operating only on `Order`'s fields.  
- **Refactoring / Solution**: Move Method to the data-owning class, introduce domain behavior in entities/value objects; reduce anemic domain model.  
- **Related Patterns**: Domain Model, Rich Domain Model, Tell-Don’t-Ask.  
- **Sources**: Fowler – Feature Envy; online smell catalog; Industrial Logic refactoring guide.[^1][^9][^2]

***

### 3.6 Data Clumps

- **Category**: Code, Design  
- **Description**: Groups of variables or fields that always appear together but are not modeled as an explicit type.[^9][^2]
- **Symptoms**:  
  - Same tuple of parameters passed to many functions (e.g., `street, city, zip, country`).  
  - Several fields on multiple classes with identical meaning.  
- **Why It’s Bad**: Duplication of structure and validation rules; missed abstractions; difficult to change consistently.  
- **Detection Heuristics**:  
  - Frequent co-occurrence of variable/parameter name sets across methods/classes.  
  - Similar field groups in multiple classes.  
- **Severity**: Medium.  
- **Example**: Address fields duplicated on `User`, `Order`, `Invoice`, each with their own validation.  
- **Refactoring / Solution**: Introduce Value Object / data type encapsulating the clump; replace parameter lists with the new type.  
- **Related Patterns**: Value Object, Parameter Object.  
- **Sources**: Fowler – Data Clumps; Industrial Logic mapping.[^9][^2]

***

### 3.7 Primitive Obsession

- **Category**: Code, Design  
- **Description**: Use of primitive types (strings, integers) instead of small, domain-specific types for concepts such as money, email, or coordinates.[^25][^5]
- **Symptoms**:  
  - Many methods taking `string` or `int` where a richer type exists conceptually.  
  - Duplicated validation logic for the same domain concept.  
- **Why It’s Bad**: Weak typing, scattered validation, increased bug risk from value/units confusion.  
- **Detection Heuristics**:  
  - Frequent string parameters/fields with similar names across the codebase.  
  - Heuristics on common domain keywords (`email`, `currency`, `amount`, `country_code`).  
- **Severity**: Medium.  
- **Example**: Representing money as `double amount` and `string currency` everywhere.  
- **Refactoring / Solution**: Introduce small, immutable value objects; encapsulate invariants and units.  
- **Related Patterns**: Value Object, Type-Safe Enums.  
- **Sources**: Clean Code primitives guidance; Clean-Code-Smells-and-Heuristics listing.[^25][^5]

***

### 3.8 Magic Numbers / Strings

- **Category**: Code  
- **Description**: Use of literal constants with implicit meaning embedded directly in code instead of named constants or enums.[^5]
- **Symptoms**:  
  - Hard-coded values like `42`, `0.15`, `"gold"` without explanation.  
  - Duplicated literals spread throughout code.  
- **Why It’s Bad**: Obscures intent, complicates changes, and risks inconsistent updates.  
- **Detection Heuristics**:  
  - Non-trivial numeric literals not part of simple arithmetic.  
  - Repeated string literals used in conditionals or switches.  
- **Severity**: Low to Medium (higher for business-critical constants).  
- **Example**: `if (user.age > 18) { ... }` instead of using a named constant like `LEGAL_AGE`.  
- **Refactoring / Solution**: Replace Magic Number/String with Named Constant or Enum.  
- **Related Patterns**: Enum, Configuration Object.  
- **Sources**: Clean Code heuristics on literals.[^5]

***

### 3.9 Dead Code / Dead Function

- **Category**: Code, Maintainability  
- **Description**: Functions, classes, variables, or branches that are never executed or referenced.[^5]
- **Symptoms**:  
  - Unused functions or classes.  
  - Commented-out blocks of old code.  
- **Why It’s Bad**: Increases noise and maintenance cost; misleads readers and tools; may hide obsolete behavior.  
- **Detection Heuristics**:  
  - Static reachability / usage analysis: declarations without references.  
  - Build-time or linter warnings for unused symbols.  
- **Severity**: Low per instance, but High in aggregate.  
- **Example**: Legacy `calculate_discount_v1` kept but never called.  
- **Refactoring / Solution**: Delete unused code; rely on version control for history.  
- **Related Patterns**: None (negative of refactoring discipline).  
- **Sources**: Clean Code "Dead Function" and commented-out code smells.[^5]

***

### 3.10 God Condition (Complex Conditional)

- **Category**: Code, Maintainability  
- **Description**: Extremely complex boolean expressions mixing many conditions with nested `and`/`or`/`not` operators.  
- **Symptoms**:  
  - Conditionals hard to understand or test.  
  - Many duplicated parts of the condition.  
- **Why It’s Bad**: Hard to reason about, easy to break with small changes, and inhibits reuse of conditional logic.  
- **Detection Heuristics**:  
  - Threshold on boolean expression length (AST nodes) and nesting depth.  
  - Repeated sub-expressions inside conditionals.  
- **Severity**: Medium.  
- **Example**:  
  ```java
  if (user != null && user.isActive() && !user.isBanned() &&
      (role == ADMIN || (role == EDITOR && featureFlags.isEnabled("X"))) &&
      !request.isFromBlacklistedIp()) {
      ...
  }
  ```  
- **Refactoring / Solution**: Extract Conditionals into well-named methods or predicate objects; use Guard Clauses; apply Specification pattern.  
- **Related Patterns**: Specification, Guard Clauses.  
- **Sources**: Condition complexity smells in refactoring literature and Clean Code discussions.[^2][^5]

***

### 3.11 Inconsistent Naming

- **Category**: Code, Maintainability  
- **Description**: Names that do not follow consistent conventions or domain language, or that misrepresent behavior.  
- **Symptoms**:  
  - Same concept named differently across modules.  
  - Functions whose names do not match side effects.  
- **Why It’s Bad**: Hurts readability, leads to misunderstandings, and undermines domain-driven design.  
- **Detection Heuristics**:  
  - Heuristics over identifier names vs domain glossary.  
  - Static checks for naming conventions; similarity analysis across types.  
- **Severity**: Medium (high in domain-intensive code).  
- **Example**: `Customer`, `Client`, `User` used interchangeably.  
- **Refactoring / Solution**: Rename methods/classes to match ubiquitous language; enforce naming conventions via linters.  
- **Related Patterns**: Ubiquitous Language (DDD).  
- **Sources**: Clean Code naming principles; DDD discussions.[^25][^5]

***

### 3.12 God Class / God Object

- **Category**: Design, Architecture, Maintainability  
- **Description**: A single class or component that knows too much, does too much, and centralizes many responsibilities.[^11][^3]
- **Symptoms**:  
  - Very large class with many unrelated methods and fields.  
  - High coupling and fan-in/fan-out.  
  - Many tests targeting this single type; bug hotspot.  
- **Why It’s Bad**: Violates SRP and often OCP; becomes a bottleneck for change and a single point of failure.  
- **Detection Heuristics**:  
  - Size and cohesion metrics; high centrality in dependency graph.  
  - Change-history analysis: frequently modified file with many co-changing neighbors.  
- **Severity**: Critical in core domains.  
- **Example**: A `CustomerManager` class handling persistence, business rules, API orchestration, and reporting.  
- **Refactoring / Solution**: Extract Classes and Services; distribute responsibilities across well-defined aggregates and domain services; introduce interfaces.  
- **Related Patterns**: Facade (as a stable boundary), Domain Service, Repository.  
- **Sources**: Suryanarayana design smells (God Class); system design anti-pattern literature.[^11][^3]

***

### 3.13 Divergent Change

- **Category**: Design, Maintainability  
- **Description**: A class that is changed for many different reasons when different kinds of requirements evolve.[^12][^2]
- **Symptoms**:  
  - One file touched by many unrelated features over time.  
  - Mixed responsibilities such that different stories modify different parts of the same class.  
- **Why It’s Bad**: Indicates poor separation of concerns and missing abstractions; raises change-risk and conflict likelihood.  
- **Detection Heuristics**:  
  - Change-history mining: file with high change entropy (many distinct change topics).  
  - Static analysis: roles in the class that access disjoint sets of collaborators.  
- **Severity**: High.  
- **Example**: `Invoice` class changed when tax rules, discount policies, and PDF layout change.  
- **Refactoring / Solution**: Split class by reason for change (Extract Class, Split Phase); reorganize around cohesive responsibilities.  
- **Related Patterns**: SRP, Modularity, Microservices bounded contexts.  
- **Sources**: Fowler’s change-preventer smells; Shotgun Surgery and Divergent Change discussions.[^12][^2]

***

### 3.14 Shotgun Surgery

- **Category**: Design, Architecture, Maintainability  
- **Description**: A small change requires many edits across multiple classes or modules.[^12][^2]
- **Symptoms**:  
  - Scattered logic for a single concern.  
  - Change sets regularly touching many files in different packages.  
- **Why It’s Bad**: High change cost, increased chance of errors and omissions, fragile design.  
- **Detection Heuristics**:  
  - Co-change analysis: requirement-level changes affecting many files.  
  - Static: same conditional or duplicated behavior repeated across many classes.  
- **Severity**: High to Critical.  
- **Example**: Energy check duplicated in every character action method instead of centralized.  
- **Refactoring / Solution**: Introduce a dedicated abstraction that encapsulates the concern; Move Method; Extract Class; use appropriate GoF patterns (Strategy, Template Method).  
- **Related Patterns**: Strategy, Template Method, Observer.  
- **Sources**: Fowler – Shotgun Surgery; online smell catalog.[^12][^2]

***

### 3.15 Inappropriate Intimacy

- **Category**: Design, Dependency  
- **Description**: Two classes or modules know too much about each other’s internals, often manipulating private data via accessors or friends.[^10]
- **Symptoms**:  
  - Extensive use of getters/setters of another class for complex manipulations.  
  - Mutual dependencies between two classes.  
- **Why It’s Bad**: Tight coupling, fragile to refactoring, breaks encapsulation, and complicates independent testing.  
- **Detection Heuristics**:  
  - High bidirectional coupling between two types.  
  - Many calls across a pair of classes, often to internal-looking APIs.  
- **Severity**: High.  
- **Example**: `Order` and `Invoice` classes modifying each other’s internal collections.  
- **Refactoring / Solution**: Move responsibilities to a single owner; introduce mediating abstractions; reduce public surface area and encapsulate invariants.  
- **Related Patterns**: Mediator, Facade, Encapsulation.  
- **Sources**: Fowler coupler smells; OOP smell lists.[^10]

***

### 3.16 Message Chains (Train Wreck)

- **Category**: Design, Dependency  
- **Description**: Long chains of calls such as `a.getB().getC().getD()` that navigate through object graphs, violating the Law of Demeter.[^10]
- **Symptoms**:  
  - Frequent dots in call expressions.  
  - Breakage when internal structure changes.  
- **Why It’s Bad**: Exposes internal structure, couples clients to navigation paths, and reduces encapsulation.  
- **Detection Heuristics**:  
  - Threshold on member-access chain length in AST.  
  - Detection of Law-of-Demeter violations.  
- **Severity**: Medium.  
- **Example**: `order.getCustomer().getAddress().getCity()`  
- **Refactoring / Solution**: Introduce methods that hide navigation (`order.getCustomerCity()`); move behavior closer to data.  
- **Related Patterns**: Law of Demeter, Tell-Don’t-Ask, Facade.  
- **Sources**: Fowler – Message Chains; OOP smell catalogs.[^10]

***

### 3.17 Middle Man

- **Category**: Design  
- **Description**: A class that exists primarily to delegate to another class, adding little or no value.[^10]
- **Symptoms**:  
  - Methods that are thin wrappers delegating almost every call.  
  - Class disappears without loss of behavior when inlined.  
- **Why It’s Bad**: Adds indirection and complexity without clear benefit.  
- **Detection Heuristics**:  
  - Methods whose body is a single delegation statement.  
  - High ratio of delegating methods to real logic.  
- **Severity**: Low to Medium.  
- **Example**: A `UserService` that forwards every call directly to `UserRepository` without adding invariants or orchestration.  
- **Refactoring / Solution**: Inline Middle Man or move behavior into the delegating or delegated class as appropriate.  
- **Related Patterns**: Facade (when explicit intent exists), Proxy.  
- **Sources**: Fowler coupler smells.[^10]

***

### 3.18 Refused Bequest

- **Category**: Design  
- **Description**: A subclass inherits methods or data it does not need, or overrides inherited behavior in incompatible ways.  
- **Symptoms**:  
  - Subclass overriding most inherited methods with empty or exception-throwing bodies.  
  - Subclass using only a subset of base-class state.  
- **Why It’s Bad**: Violates Liskov Substitution and signals a wrong inheritance hierarchy.  
- **Detection Heuristics**:  
  - Subclasses overriding many methods with trivial/no-op implementations.  
  - Class hierarchies where some leaf types never use base fields.  
- **Severity**: Medium.  
- **Example**: `Square` inheriting from `Rectangle` but overriding width/height semantics.  
- **Refactoring / Solution**: Replace inheritance with composition; extract common parts into a separate component; redesign hierarchy.  
- **Related Patterns**: Composition over Inheritance.  
- **Sources**: Classic OO smell discussions; LSP literature.[^3]

***

### 3.19 Parallel Inheritance Hierarchies

- **Category**: Design, Dependency  
- **Description**: Two or more class hierarchies that must evolve in lockstep such that creating a subclass in one requires creating a counterpart in another.  
- **Symptoms**:  
  - Naming symmetry between hierarchies (`CarModel`/`CarModelDTO`).  
  - Boilerplate factory/switch logic tying hierarchies together.  
- **Why It’s Bad**: Increases maintenance overhead and coupling, and often indicates missing abstraction.  
- **Detection Heuristics**:  
  - Pattern-based pairing of type names across packages.  
  - Co-change analysis of paired classes.  
- **Severity**: Medium.  
- **Example**: Adding a new `ProductType` always requires adding a new handler, DTO, permission, etc.  
- **Refactoring / Solution**: Introduce common abstraction (e.g., Strategy, Visitor); collapse redundant hierarchies where possible.  
- **Related Patterns**: Strategy, Visitor, Abstract Factory.  
- **Sources**: Fowler change-preventer smells.[^12][^10]

***

### 3.20 Anemic Domain Model

- **Category**: Design, Architecture  
- **Description**: Domain entities contain only data, with business logic pushed into service classes or transaction scripts.  
- **Symptoms**:  
  - Domain classes with only getters/setters.  
  - Large service classes implementing complex domain rules.  
- **Why It’s Bad**: Violates encapsulation and SRP at the domain level; spreads invariants; increases shotgun surgery.  
- **Detection Heuristics**:  
  - Entities with many fields but no domain methods.  
  - Services with domain-semantics names manipulating raw entities.  
- **Severity**: High in complex domains.  
- **Example**: `Order` as a pure data holder while `OrderService` implements all pricing and state transitions.  
- **Refactoring / Solution**: Move domain logic into entities/value objects; introduce aggregates and domain services per DDD.  
- **Related Patterns**: Domain Model, Rich Domain Model.  
- **Sources**: DDD and Clean Architecture discussions; microservice smell literature.[^15][^25]

***

### 3.21 Service Locator

- **Category**: Design, Dependency  
- **Description**: A global registry or locator used to retrieve dependencies by name or type instead of explicit injection.  
- **Symptoms**:  
  - Static calls like `ServiceLocator.get("X")` spread across code.  
  - Hidden dependencies not visible in constructor or method signatures.  
- **Why It’s Bad**: Obscures dependencies, hinders testability, and couples code to a global mechanism.  
- **Detection Heuristics**:  
  - Calls to known locator types or `GlobalContext`.  
  - Static calls in otherwise injectable classes.  
- **Severity**: Medium to High.  
- **Example**: Controllers pulling repositories from a static `ApplicationContext`.  
- **Refactoring / Solution**: Replace with explicit dependency injection, constructor injection, or inversion-of-control container usage.  
- **Related Patterns**: Dependency Injection, Inversion of Control.  
- **Sources**: DI/IoC best practices in Clean Architecture and modern frameworks.[^25]

***

### 3.22 Big Ball of Mud

- **Category**: Architecture, Maintainability  
- **Description**: A system with little discernible architecture, ad hoc structure, and pervasive coupling; modules and layers are blurred.  
- **Symptoms**:  
  - Unclear boundaries between subsystems.  
  - Cross-cutting dependencies everywhere; hard to identify responsibility.  
- **Why It’s Bad**: Hard to understand, test, and evolve; changes ripple unpredictably; refactoring becomes extremely costly.  
- **Detection Heuristics**:  
  - High average and maximum module coupling; dense dependency graph.  
  - Lack of clear dependency direction; layering violations common.  
- **Severity**: Critical.  
- **Example**: Large legacy monolith where all packages import each other arbitrarily.  
- **Refactoring / Solution**: Introduce modular boundaries; apply architectural refactoring toward layered, hexagonal, or modular monolith; enforce dependency rules.  
- **Related Patterns**: Layered Architecture, Hexagonal Architecture, Bounded Context.  
- **Sources**: Classic Big Ball of Mud pattern; architecture anti-pattern literature.[^13][^4][^11]

***

### 3.23 Layer Skipping / Bypassed Layers

- **Category**: Architecture, Dependency  
- **Description**: Higher layers directly access lower-level layers, bypassing designated intermediate layers (e.g., UI directly querying the database).  
- **Symptoms**:  
  - Presentation code accessing repositories or SQL directly.  
  - Domain layer reaching into infrastructure details.  
- **Why It’s Bad**: Breaks layering and separation of concerns; makes changing one layer’s contract difficult.  
- **Detection Heuristics**:  
  - Static dependency analysis against allowed layer dependency rules.  
  - Violations of architectural constraints (e.g., using ArchUnit-style rules).  
- **Severity**: High.  
- **Example**: React component calling REST endpoints and then constructing SQL queries on the client.  
- **Refactoring / Solution**: Enforce layering; introduce application services; move data access into proper infrastructure adapters.  
- **Related Patterns**: Layered Architecture, Clean Architecture, Ports and Adapters.  
- **Sources**: Architecture anti-pattern classifications; Clean Architecture guidance.[^4][^25]

***

### 3.24 Unstable Interface / Unstable Dependency

- **Category**: Architecture, Dependency  
- **Description**: A module or interface heavily depended on (high fan-in) but itself depends on many other modules and changes frequently.[^13][^4]
- **Symptoms**:  
  - Central modules that change often and cause widespread recompilation/regression.  
  - Violation of Stable Dependencies Principle.  
- **Why It’s Bad**: Creates architectural hotspots for bugs and change-proneness; undermines modularity.  
- **Detection Heuristics**:  
  - Graph-theoretic metrics on dependency graph (fan-in, fan-out, change frequency).  
- **Severity**: Critical.  
- **Example**: Core `util` library referenced everywhere but frequently modified to support new features.  
- **Refactoring / Solution**: Extract stable interfaces; move volatile details behind stable abstractions; reduce dependencies of core modules.  
- **Related Patterns**: Stable Dependencies Principle, Facade, Plug-in architectures.  
- **Sources**: Architecture anti-patterns empirically linked to change- and error-proneness.[^13][^4]

***

### 3.25 Cyclic Package / Module Dependencies

- **Category**: Architecture, Dependency  
- **Description**: Two or more packages/modules that depend on each other, forming cycles in the dependency graph.  
- **Symptoms**:  
  - Difficulties in independent builds or deployments.  
  - Changes in one module requiring recompilation of the others.  
- **Why It’s Bad**: Prevents independent evolution and reuse; complicates testing and deployment; often associated with architecture anti-patterns.[^4]
- **Detection Heuristics**:  
  - Graph cycle detection over package/module dependencies.  
- **Severity**: High.  
- **Example**: `billing` imports `customer`, and `customer` imports `billing`.  
- **Refactoring / Solution**: Break cycles by introducing interfaces, moving shared abstractions to a lower-level module, or reassigning responsibilities.  
- **Related Patterns**: Dependency Inversion, Common Closure Principle.  
- **Sources**: Architecture anti-pattern studies and structural metrics research.[^13][^4]

***

### 3.26 Hardcoded Environment / Configuration

- **Category**: Architecture, DevOps  
- **Description**: Environment-specific values (URLs, credentials, feature flags) hardcoded into code instead of external configuration.  
- **Symptoms**:  
  - Source code containing hostnames, ports, secrets.  
  - Multiple `if env == "prod"` style branches.  
- **Why It’s Bad**: Hinders deployment flexibility, increases risk of leaking secrets, and complicates testing and scaling.  
- **Detection Heuristics**:  
  - Pattern-matching for URL/host/credential-like literals.  
  - Conditionals on environment names.  
- **Severity**: High (security and operability implications).  
- **Example**: `const DB_URL = "jdbc:postgresql://prod-db:5432/..."` in source code.  
- **Refactoring / Solution**: Externalize configuration; use environment variables, config files, or parameter stores; adopt 12-factor app practices.  
- **Related Patterns**: Externalized Configuration, 12-Factor App.  
- **Sources**: DevOps best practices and cloud architecture guidance.[^11]

***

### 3.27 Shared Library as Integration Point (God Library)

- **Category**: Architecture, Dependency  
- **Description**: Multiple services or modules integrate primarily via a large shared library that contains business logic instead of using clear APIs.  
- **Symptoms**:  
  - Many applications depend on the same fat library.  
  - Difficulty upgrading one consumer without impacting others.  
- **Why It’s Bad**: Couples services at binary level, undermines autonomy; changes in the library ripple to all dependents.  
- **Detection Heuristics**:  
  - Static dependency graph showing a central large library used by many executables.  
- **Severity**: High in microservice environments.  
- **Example**: All microservices share `company-core.jar` that encodes key business flows.  
- **Refactoring / Solution**: Move integration to explicit service APIs or events; slim libraries to shared utilities and contracts.  
- **Related Patterns**: Shared Kernel (DDD, used sparingly), Published Language, API-first integration.  
- **Sources**: Microservice and DDD anti-pattern discussions.[^16][^15]

***

### 3.28 Distributed Monolith

- **Category**: Microservices, Architecture  
- **Description**: A system deployed as multiple services but with tight runtime and release coupling, behaving like a monolith over the network.[^17][^14][^16]
- **Symptoms**:  
  - Services must be deployed together; shared release cycle.  
  - Extensive synchronous communication and shared databases.  
- **Why It’s Bad**: Combines operational complexity of microservices with change coupling of a monolith; poor resilience and scalability.  
- **Detection Heuristics**:  
  - Runtime tracing showing long chains of synchronous calls for common use cases.  
  - Co-deployment/co-release of many services; shared DB schemas.  
- **Severity**: Critical.  
- **Example**: Order flow requiring synchronous calls across 6 services, all of which must be updated together.  
- **Refactoring / Solution**: Redesign bounded contexts; introduce asynchronous communication; decouple data ownership; move toward modular monolith or true microservices.  
- **Related Patterns**: Bounded Context, Saga, Event-Driven Architecture.  
- **Sources**: Microservices anti-pattern literature and tertiary studies on microservice smells.[^14][^16][^17][^15]

***

### 3.29 Shared Database / Shared Schema Integration

- **Category**: Microservices, Data, Architecture  
- **Description**: Multiple services or systems directly share the same database schema/tables as an integration mechanism.[^7][^8][^16][^14]
- **Symptoms**:  
  - Many services with direct access to `Customer` or `Order` tables.  
  - Database schema changes requiring coordination across teams.  
- **Why It’s Bad**: Breaks encapsulation and ownership; couples services at the persistence level; creates contention and change risk.[^8]
- **Detection Heuristics**:  
  - Schema analysis: same table used by many services.  
  - Connection-string reuse across independently deployed services.  
- **Severity**: Critical in distributed systems.  
- **Example**: Analytics, billing, and CRM microservices all reading/writing `users` table.  
- **Refactoring / Solution**: Each service owns its database; expose data via APIs or events; introduce reporting/warehouse databases fed from owned stores.  
- **Related Patterns**: Database per Service, Published Language, CQRS + Event Sourcing.  
- **Sources**: Microservice anti-pattern articles; INNOQ discussion on shared DB as bad API; data modeling anti-pattern literature.[^7][^16][^8][^14]

***

### 3.30 Chatty Services / Chatty Interfaces

- **Category**: Microservices, Performance, Dependency  
- **Description**: Excessive fine-grained remote calls between services or layers instead of coarse, meaningful operations.[^18][^16][^17][^14][^15][^11]
- **Symptoms**:  
  - Multiple sequential network calls to fulfill a single user request.  
  - Remote getters used like in-process object navigation.  
- **Why It’s Bad**: High latency, network overhead, and increased failure surface; undermines resilience.  
- **Detection Heuristics**:  
  - Traces showing many calls between same pair of services in one request.  
  - Static analysis of clients calling many small methods on a remote API.  
- **Severity**: High.  
- **Example**: Order creation that calls customer, inventory, pricing, and payment services synchronously in series for each line item.  
- **Refactoring / Solution**: Design coarse-grained APIs; use API composition or CQRS; aggregate data in read models; use async messaging.  
- **Related Patterns**: API Gateway, Aggregator, Saga, Bulkhead.  
- **Sources**: Microservice anti-patterns; system design anti-patterns.[^18][^16][^17][^14][^15][^11]

***

### 3.31 Nanoservices (Over-Decomposition)

- **Category**: Microservices, Architecture  
- **Description**: Splitting functionality into services that are too small and granular, often performing trivial tasks.  
- **Symptoms**:  
  - Services with very few endpoints or minimal logic.  
  - High operational overhead relative to behavior.  
- **Why It’s Bad**: Management and deployment overhead; chatty communication; unclear domain boundaries.  
- **Detection Heuristics**:  
  - Services with very small codebases but full deployment pipelines.  
  - Many services participating in a single business transaction.  
- **Severity**: Medium to High.  
- **Example**: Separate "email sender", "email template", and "email audit" services for simple notifications.  
- **Refactoring / Solution**: Merge nanoservices into cohesive domain services; reassess bounded contexts.  
- **Related Patterns**: Modular Monolith, Bounded Context.  
- **Sources**: Microservices practice literature and anti-pattern discussions.[^16][^14]

***

### 3.32 Wrong Bounded Context / Entity Service

- **Category**: Microservices, Architecture, Data  
- **Description**: Services organized around CRUD for entities (e.g., `CustomerService`) rather than around domain capabilities, leading to cross-context leakage.[^15]
- **Symptoms**:  
  - Generic entity services used by many unrelated workflows.  
  - Business rules requiring coordination across multiple CRUD services.  
- **Why It’s Bad**: Poor alignment to domain model; leads to distributed monolith and shared database issues.  
- **Detection Heuristics**:  
  - Services named after generic entities (Customer, Product) with broad responsibilities.  
  - Cross-team dependencies on the same entity service.  
- **Severity**: High.  
- **Example**: `CustomerService` used for marketing, billing, support, KYC, each with different views of "customer".  
- **Refactoring / Solution**: Recut services along bounded contexts (e.g., BillingCustomer, MarketingCustomer); establish clear ownership and integration contracts.  
- **Related Patterns**: Bounded Context, Context Map.  
- **Sources**: DDD and microservice smell catalogs.[^15]

***

### 3.33 Synchronous Dependency Chain

- **Category**: Microservices, Performance, Dependency  
- **Description**: Deep chains of synchronous calls where one service directly calls another, and so on, for a single user operation.[^14][^15]
- **Symptoms**:  
  - Long critical paths in traces.  
  - Many services must be up to serve a request.  
- **Why It’s Bad**: Latency amplification, cascading failures, and tight runtime coupling.  
- **Detection Heuristics**:  
  - Distributed tracing analysis for call depth and fan-out.  
  - Static detection of synchronous HTTP/RPC calls inside request handlers.  
- **Severity**: High.  
- **Example**: `API Gateway → Service A → Service B → Service C → DB` all synchronously in the hot path.  
- **Refactoring / Solution**: Introduce async messaging, sagas, or orchestration; cache data; collapse some services.  
- **Related Patterns**: Saga, Event-Driven Architecture, Circuit Breaker.  
- **Sources**: Microservice architecture smell literature.[^14][^15]

***

### 3.34 Smart UI / API Gateway God Service

- **Category**: Microservices, Architecture  
- **Description**: UI or API gateway accumulating business logic and orchestration instead of delegating to backend services.  
- **Symptoms**:  
  - Complex decision making and workflows in UI/gateway.  
  - Many direct calls from UI to multiple backend services with business rules embedded.  
- **Why It’s Bad**: Hard to reuse logic across channels; hinders evolution; leads to distributed monolith centered on gateway.  
- **Detection Heuristics**:  
  - LOC and complexity metrics for UI/gateway components.  
  - Domain operations implemented directly in controllers or gateway routes.  
- **Severity**: High.  
- **Example**: React application orchestrating multi-step payment flows with extensive rules.  
- **Refactoring / Solution**: Move orchestration into backend application services; keep UI/gateway thin.  
- **Related Patterns**: Backend For Frontend (BFF), Application Service.  
- **Sources**: Microservices best practices.[^16][^14]

***

### 3.35 Fragile / Brittle Tests

- **Category**: Testing, Maintainability  
- **Description**: Tests that break with small, behavior-preserving refactorings or minor implementation changes.[^20][^19][^22]
- **Symptoms**:  
  - Tests failing when method signatures or internal structure change, even if behavior remains.  
  - Overly specific assertions on internals.  
- **Why It’s Bad**: Discourages refactoring; inflates maintenance cost; erodes trust in tests.  
- **Detection Heuristics**:  
  - Tests accessing private state or detailed implementation via reflection.  
  - High coupling between tests and internal structure; frequent test churn in VCS.  
- **Severity**: High.  
- **Example**: Test asserting exact sequence of method calls to collaborators instead of observable outcomes.  
- **Refactoring / Solution**: Test via public behavior; avoid assertions on implementation details; favor classicist style over interaction-heavy tests when possible.  
- **Related Patterns**: London vs. classical testing schools; FIRST test principles.  
- **Sources**: Unit Testing Principles, Practices, and Patterns; testing anti-pattern catalogs.[^19][^20][^22]

***

### 3.36 Flaky Tests

- **Category**: Testing  
- **Description**: Tests that pass or fail nondeterministically without changes to the code under test.  
- **Symptoms**:  
  - Intermittent failures in CI; rerunning makes them pass.  
  - Timeouts or order-dependent behavior.  
- **Why It’s Bad**: Reduces confidence in test suite; wastes time; hides real issues.  
- **Detection Heuristics**:  
  - CI history analysis for intermittent failures.  
  - Usage of time, randomness, or external resources without control.  
- **Severity**: High.  
- **Example**: Test relying on real network or clock without isolation.  
- **Refactoring / Solution**: Remove non-determinism; control time and randomness; isolate from external systems with stable contracts.  
- **Related Patterns**: Hermetic Tests, Test Doubles.  
- **Sources**: Testing literature and anti-pattern lists.[^23][^22]

***

### 3.37 Over-Mocking / Mockery

- **Category**: Testing, Design  
- **Description**: Tests that use excessive mocks/stubs such that they validate mock configuration rather than real behavior.[^21][^20][^22][^19]
- **Symptoms**:  
  - Test setup longer than test logic.  
  - Tests that fail when refactoring internal collaboration patterns.  
- **Why It’s Bad**: Fragile tests; obscures intent; makes refactorings costly.  
- **Detection Heuristics**:  
  - High ratio of mocking-library calls in tests.  
  - Many expectations on collaboration sequences.  
- **Severity**: Medium to High.  
- **Example**: Unit test mocking every repository and mapper, asserting exact call order.  
- **Refactoring / Solution**: Prefer integration tests with real components where feasible; limit mocks to external boundaries; assert outcomes instead of interactions.  
- **Related Patterns**: Interaction vs state-based testing.  
- **Sources**: Unit Testing Principles; testing anti-pattern guides.[^20][^22][^19][^21]

***

### 3.38 Mystery Guest

- **Category**: Testing  
- **Description**: Tests that rely on external, hidden fixtures or state instead of explicitly setting up data in the test.[^22][^23]
- **Symptoms**:  
  - Tests that refer to data "already in the database".  
  - Implicit assumptions about environment, files, or data.  
- **Why It’s Bad**: Hard to understand, debug, and maintain; brittle to environment changes.  
- **Detection Heuristics**:  
  - Tests that perform queries without explicit prior setup.  
  - References to data seeded elsewhere or to shared external resources.  
- **Severity**: Medium.  
- **Example**: `User.objects.get(email="[email protected]")` in tests without local creation.  
- **Refactoring / Solution**: Make all fixtures explicit and local to tests or shared builders; isolate test data creation; use factories.  
- **Related Patterns**: Test Data Builder, Object Mother.  
- **Sources**: Testing anti-pattern catalogs and tools.[^23][^22]

***

### 3.39 Slow Tests

- **Category**: Testing, Performance  
- **Description**: Tests that take long to run, slowing feedback cycles and discouraging frequent execution.  
- **Symptoms**:  
  - Test suite taking many minutes or hours.  
  - Tests interacting with real databases, networks, browsers in large volumes.  
- **Why It’s Bad**: Encourages infrequent runs; delays feedback; contributes to flaky behavior.  
- **Detection Heuristics**:  
  - Per-test runtime profiling; thresholds for slow tests.  
  - Tests invoking external resources without stubbing.  
- **Severity**: Medium to High (for core suites).  
- **Example**: UI end-to-end tests covering scenarios better handled by fast unit/integration tests.  
- **Refactoring / Solution**: Layer test pyramid; move some checks to unit/integration level; parallelize; mock expensive external dependencies appropriately.  
- **Related Patterns**: Test Pyramid, FIRST tests.  
- **Sources**: Testing practices literature.[^19][^20]

***

### 3.40 Assertion Roulette

- **Category**: Testing  
- **Description**: Tests with many assertions and no clear explanation of which behavior each assertion validates, making failures hard to interpret.[^22]
- **Symptoms**:  
  - Multiple unlabelled assertions in a test.  
  - Failures without clear message about what went wrong.  
- **Why It’s Bad**: Slows debugging; reduces maintainability of tests.  
- **Detection Heuristics**:  
  - Tests containing many bare `assert` calls without messages.  
  - Complex composite assertions on large outputs.  
- **Severity**: Low to Medium.  
- **Example**: Single test validating an entire API response with many unrelated expectations.  
- **Refactoring / Solution**: Split tests by concern; add descriptive failure messages; use custom matchers.  
- **Related Patterns**: Single-assertion tests where practical; FIRST principles.  
- **Sources**: Testing anti-pattern catalog.[^22]

***

### 3.41 God Table

- **Category**: Data, Architecture  
- **Description**: A single database table that accumulates many unrelated concerns, often with dozens of loosely related columns.[^6][^7]
- **Symptoms**:  
  - Very wide table with many nullable columns and overloaded semantics.  
  - Table accessed by many modules/contexts for different purposes.  
- **Why It’s Bad**: Tight coupling between unrelated data; poor performance; difficult schema evolution; risk of inconsistent updates.[^6][^7]
- **Detection Heuristics**:  
  - Table column count and nullability metrics.  
  - Access patterns from different services/modules.  
- **Severity**: High.  
- **Example**: `users` table with authentication, preferences, billing, and emergency contacts.  
- **Refactoring / Solution**: Normalize into cohesive tables per concern; assign clear ownership; introduce views or APIs for composed views.  
- **Related Patterns**: Normalization, Bounded Context, Database per Service.  
- **Sources**: Data modeling anti-pattern articles.[^7][^6]

***

### 3.42 Entity-Attribute-Value (EAV) Abuse

- **Category**: Data, Performance, Maintainability  
- **Description**: Overuse of generic EAV schemas to model many different concepts, leading to opaque and inefficient data structures.  
- **Symptoms**:  
  - Central `entity`, `attribute`, `value` tables storing most domain data.  
  - Complex queries reconstructing entities at runtime.  
- **Why It’s Bad**: Poor type safety, hard to query and optimize, difficult to enforce constraints.  
- **Detection Heuristics**:  
  - Presence of generic key–value tables used by many features.  
- **Severity**: Medium to High.  
- **Example**: Using EAV to store all user profile fields instead of schema.  
- **Refactoring / Solution**: Denormalize back into explicit tables for stable attributes; restrict EAV to truly dynamic, low-volume metadata.  
- **Related Patterns**: Metadata tables, Schema evolution techniques.  
- **Sources**: Database anti-pattern literature.[^6]

***

### 3.43 Polymorphic Association Table

- **Category**: Data, Design  
- **Description**: Table containing a foreign key plus a type discriminator to reference multiple parent tables (e.g., `subject_type` + `subject_id`).  
- **Symptoms**:  
  - Columns like `parent_id` + `parent_type` used for many relations.  
- **Why It’s Bad**: Weak referential integrity, complicated joins, and brittle polymorphism.  
- **Detection Heuristics**:  
  - Existence of `*_type` with corresponding `*_id` columns.  
- **Severity**: Medium.  
- **Example**: `comments` table that can belong to `Post`, `Photo`, `Video` via type+id.  
- **Refactoring / Solution**: Separate association tables per parent type; use proper foreign keys or join tables.  
- **Related Patterns**: Join Table, Class Table Inheritance.  
- **Sources**: Data modeling anti-pattern coverage.[^6]

***

### 3.44 Overloaded Column / Semantic Overloading

- **Category**: Data, Maintainability  
- **Description**: Single column used for multiple semantics depending on context (e.g., storing different kinds of codes or states in the same field).  
- **Symptoms**:  
  - Column values with many meanings; conditional logic in application interpreting it.  
- **Why It’s Bad**: Hard to audit and evolve; increases risk of inconsistent usage.  
- **Detection Heuristics**:  
  - High cardinality and variety of values; complex application-level switch on column.  
- **Severity**: Medium.  
- **Example**: Column `status` used to represent both lifecycle state and error conditions.  
- **Refactoring / Solution**: Split into separate columns or tables; clarify semantics with enumerations.  
- **Related Patterns**: Explicit Schema, Proper Normalization.  
- **Sources**: Database design best practices.[^6]

***

### 3.45 Concrete Dependency (Ignoring Dependency Inversion)

- **Category**: Dependency, Design  
- **Description**: High-level modules directly depend on low-level implementation details instead of abstractions, violating Dependency Inversion Principle (DIP).  
- **Symptoms**:  
  - Core use cases depending directly on frameworks, ORMs, or concrete infrastructure.  
- **Why It’s Bad**: Ties business logic to specific technologies; hinders testing and evolution.  
- **Detection Heuristics**:  
  - References to framework types in domain core; absence of interfaces at boundaries.  
- **Severity**: High.  
- **Example**: Domain services directly using HTTP clients or SQL queries.  
- **Refactoring / Solution**: Introduce interfaces and ports; inject implementations from infrastructure layer.  
- **Related Patterns**: Ports and Adapters, Dependency Inversion, Hexagonal Architecture.  
- **Sources**: SOLID and Clean Architecture guidance.[^25]

***

### 3.46 Hidden Temporal Coupling

- **Category**: Dependency, Maintainability  
- **Description**: Correct behavior requires functions or operations to be called in a specific order, but this dependency is not explicit in the API.  
- **Symptoms**:  
  - Comments like "call `init()` before `use()`".  
  - Subtle bugs when operations are invoked in a different order.  
- **Why It’s Bad**: Hard to use APIs correctly and safely; leads to subtle state bugs.  
- **Detection Heuristics**:  
  - Mutating methods on types with separate `initialize` or `open` methods; static analysis of required preconditions.  
- **Severity**: Medium.  
- **Example**: `connect()`, `send()`, `close()` methods where forgetting `connect()` produces runtime errors.  
- **Refactoring / Solution**: Encapsulate states with explicit types (State pattern); enforce correct sequencing through APIs.  
- **Related Patterns**: State, Fluent interfaces with staged builders.  
- **Sources**: Design smell literature.[^3]

***

### 3.47 N+1 Query

- **Category**: Performance, Data  
- **Description**: Executing an initial query followed by one query per returned row to fetch associated data, instead of a single join or batch.  
- **Symptoms**:  
  - Loops issuing queries inside; poor performance on large datasets.  
- **Why It’s Bad**: Quadratic-like behavior in terms of database round-trips; significant latency and load.  
- **Detection Heuristics**:  
  - Static: ORM usage patterns with lazy-loaded relations accessed in loops.  
  - Runtime: query logs with many similar statements per request.  
- **Severity**: High in high-traffic paths.  
- **Example**: For each `Order`, querying its `OrderLines` separately.  
- **Refactoring / Solution**: Use eager loading, joins, or batch fetching; cache results; reshape queries.  
- **Related Patterns**: Unit of Work, Repository, Batch Fetching.  
- **Sources**: ORM and performance best practices.[^6]

***

### 3.48 Premature Optimization

- **Category**: Performance, Maintainability  
- **Description**: Introducing complex optimizations before profiling or evidence of need, often at the expense of clarity.  
- **Symptoms**:  
  - Micro-optimizations in non-critical paths; hand-rolled data structures without need.  
- **Why It’s Bad**: Increases complexity and bug risk; locks in designs without proven benefit.  
- **Detection Heuristics**:  
  - Complex code in areas without measured bottlenecks; absence of performance tests justifying complexity.  
- **Severity**: Medium.  
- **Example**: Manual caching layers added everywhere before observing latency issues.  
- **Refactoring / Solution**: Simplify; rely on profiler-guided optimization; apply YAGNI.  
- **Related Patterns**: Simple Design, YAGNI.  
- **Sources**: General performance engineering and system design anti-patterns.[^11]


## 4. Top 25 Most Important Anti-Patterns (Impact on System Quality)

The following 25 anti-patterns are prioritized by impact on maintainability, evolvability, and system risk in modern systems:

1. God Class / God Object  
2. Big Ball of Mud  
3. Distributed Monolith  
4. Shared Database / Shared Schema Integration  
5. Cyclic Package / Module Dependencies  
6. Unstable Interface / Unstable Dependency  
7. Shotgun Surgery  
8. Divergent Change  
9. Anemic Domain Model  
10. Service Locator  
11. Duplicated Code (DRY Violation)  
12. Long Method  
13. Large Class  
14. Feature Envy  
15. Chatty Services / Chatty Interfaces  
16. Nanoservices (Over-Decomposition)  
17. Wrong Bounded Context / Entity Service  
18. Fragile / Brittle Tests  
19. Flaky Tests  
20. Over-Mocking / Mockery  
21. God Table  
22. N+1 Query  
23. Concrete Dependency (Ignoring DIP)  
24. Hardcoded Environment / Configuration  
25. Premature Optimization  

These are strong candidates for high-priority rules and AI detectors because they correlate with error-proneness, change-proneness, runtime failures, and operational pain in empirical studies and industry experience.[^7][^15][^4][^13][^6]

## 5. Top 25 Most Detectable Anti-Patterns (Static / Automated Detection)

The following anti-patterns are prioritized by how amenable they are to static analysis (structural metrics, AST patterns, dependency graphs) and repository mining:

1. Duplicated Code (clone detection)  
2. Long Method (LOC/complexity thresholds)  
3. Large Class (size and cohesion metrics)  
4. Long Parameter List (signature analysis)  
5. Feature Envy (field/method access distribution)  
6. Data Clumps (co-occurring parameter/field sets)  
7. Primitive Obsession (primitive fields for domain concepts)  
8. Magic Numbers / Strings (literal detection)  
9. Dead Code / Dead Function (unused symbols)  
10. God Condition (boolean expression complexity)  
11. Message Chains (Law-of-Demeter violations)  
12. Middle Man (delegation-only methods)  
13. God Class / God Object (size and centrality metrics)  
14. Cyclic Package / Module Dependencies (graph cycles)  
15. Layer Skipping / Bypassed Layers (architecture rules)  
16. Unstable Interface / Unstable Dependency (fan-in/fan-out + change history)  
17. Distributed Monolith (trace depth + co-deployment analysis)[^16][^14][^15]
18. Shared Database / Shared Schema Integration (schema access across services)[^8][^7]
19. Chatty Services / Chatty Interfaces (call-count and RPC patterns)[^18][^17][^14]
20. Nanoservices (service size and call graph role)  
21. Wrong Bounded Context / Entity Service (entity-centric service naming and usage)  
22. God Table (schema metrics)  
23. Polymorphic Association Table (type+id column pattern)  
24. Overloaded Column / Semantic Overloading (value diversity + switch logic)  
25. N+1 Query (queries-in-loops / ORM access patterns)  

These anti-patterns are good starting points for static analyzers, linters, and AI agents because they map to identifiable structural or behavioral signatures found in code, schemas, and runtime traces.[^24][^4][^9][^2][^6]

## 6. Anti-Pattern → Refactoring Pattern Mapping

The following table maps selected anti-patterns to canonical refactorings (primarily Fowler-style) and related design/architecture patterns for remediation.[^24][^9][^2]

| Anti-Pattern | Key Refactorings | Supporting Patterns |
|--------------|------------------|---------------------|
| Duplicated Code | Extract Method; Extract Class; Pull Up Method | Template Method; Strategy |
| Long Method | Extract Method; Introduce Parameter Object; Replace Temp with Query | Command; Facade |
| Large Class | Extract Class; Extract Module; Hide Delegate | Facade; Domain Service |
| Long Parameter List | Introduce Parameter Object; Preserve Whole Object | Value Object; Builder |
| Feature Envy | Move Method; Extract Class | Rich Domain Model; Tell-Don’t-Ask |
| Data Clumps | Introduce Parameter Object; Extract Class | Value Object |
| Primitive Obsession | Introduce Class; Replace Primitive with Object | Value Object; Type Object |
| Magic Numbers / Strings | Replace Magic Number with Symbolic Constant | Enum / Constant Object |
| Dead Code / Dead Function | Remove Dead Code | N/A |
| God Condition | Decompose Conditional; Introduce Specification | Specification; Guard Clauses |
| God Class / God Object | Extract Class; Extract Module; Move Method; Replace Inheritance with Delegation | Facade; Domain Service; Bounded Context |
| Divergent Change | Extract Class; Split Phase | SRP; Layered Architecture |
| Shotgun Surgery | Move Method; Extract Class; Inline Class (to re-centralize) | Strategy; Template Method |
| Inappropriate Intimacy | Move Method; Hide Delegate; Encapsulate Field | Mediator; Facade |
| Message Chains | Hide Delegate; Introduce Intermediate Method | Law of Demeter; Facade |
| Middle Man | Inline Class; Remove Middle Man | Direct collaboration; Facade where justified |
| Refused Bequest | Replace Inheritance with Delegation; Extract Superclass (if hierarchy is wrong) | Composition over Inheritance |
| Parallel Inheritance Hierarchies | Move Methods/Fields; Collapse Hierarchy | Strategy; Visitor |
| Anemic Domain Model | Move Method to domain entities; Introduce Domain Service only for cross-aggregate logic | Domain Model; Aggregate |
| Service Locator | Introduce Dependency Injection; Parameterize/Constructor Injection | Ports and Adapters; Dependency Inversion |
| Big Ball of Mud | Extract Module; Introduce Layer; Split System by Context | Layered Architecture; Hexagonal |
| Layer Skipping | Move Methods to proper layer; Introduce Application Service | Clean Architecture |
| Cyclic Dependencies | Introduce Interface; Move Class; Extract Module | Dependency Inversion |
| Distributed Monolith | Identify Bounded Contexts; Split services by context; Replace synchronous calls with async messaging | Bounded Context; Saga; Event-Driven |
| Shared Database / Shared Schema | Database per Service; Introduce API/Events as integration; Extract read models | CQRS; Event Sourcing; Published Language |
| Chatty Services | Introduce API composition; Coalesce operations; Cache results | Aggregator; API Gateway |
| Nanoservices | Merge services; Extract cohesive capabilities | Modular Monolith; Bounded Context |
| Wrong Bounded Context | Context mapping; Service decomposition/recomposition | Bounded Context; Context Map |
| Fragile / Brittle Tests | Refactor tests to assert behavior, not internals; Introduce higher-level integration tests | Test Pyramid; FIRST |
| Over-Mocking / Mockery | Reduce mocks; Prefer real collaborators or simpler fakes | Classicist Testing; Test Data Builder |
| God Table | Normalize schema; Extract Tables; Introduce foreign-keyed tables | 3NF; Star Schema for analytics |
| N+1 Query | Introduce eager loading; Batch queries | Repository; Unit of Work |

## 7. Anti-Pattern → SOLID Violation Mapping

The table below indicates the primary SOLID principles most often violated by each anti-pattern (some violate multiple):

| Anti-Pattern | S (SRP) | O (OCP) | L (LSP) | I (ISP) | D (DIP) |
|--------------|---------|---------|---------|---------|---------|
| Duplicated Code | ✓ (changes not localized) | – | – | – | – |
| Long Method | ✓ | – | – | – | – |
| Large Class | ✓ | ✓ (hard to extend safely) | – | – | – |
| Long Parameter List | ✓ (missing abstraction) | – | – | – | – |
| Feature Envy | ✓ (behavior in wrong place) | – | – | – | – |
| Data Clumps | ✓ | – | – | – | – |
| Primitive Obsession | ✓ | – | – | – | – |
| God Class / God Object | ✓ | ✓ | – | – | – |
| Divergent Change | ✓ | ✓ | – | – | – |
| Shotgun Surgery | ✓ | ✓ | – | – | – |
| Inappropriate Intimacy | ✓ | – | – | – | – |
| Message Chains | – | – | – | – | ✓ (missing proper abstractions) |
| Middle Man | – | – | – | – | – (mostly complexity) |
| Refused Bequest | – | – | ✓ | – | – |
| Parallel Inheritance Hierarchies | ✓ | ✓ | – | ✓ (improper interfaces) | – |
| Anemic Domain Model | ✓ | – | – | – | – |
| Service Locator | – | – | – | – | ✓ |
| Big Ball of Mud | ✓ | ✓ | – | – | ✓ |
| Layer Skipping | ✓ | ✓ | – | – | ✓ |
| Unstable Interface / Dependency | – | ✓ | – | – | ✓ |
| Cyclic Dependencies | – | – | – | – | ✓ |
| Distributed Monolith | ✓ | ✓ | – | – | ✓ |
| Shared Database / Shared Schema | ✓ | ✓ | – | – | ✓ |
| Chatty Services | – | – | – | – | ✓ (poor boundary design) |
| Nanoservices | ✓ | – | – | – | – |
| Wrong Bounded Context | ✓ | ✓ | – | – | ✓ |
| Fragile / Brittle Tests | – | – | – | – | – (test design issue) |
| Over-Mocking / Mockery | – | – | – | – | – |
| God Table | ✓ | ✓ | – | – | – |
| N+1 Query | – | – | – | – | – (performance, not SOLID) |
| Concrete Dependency (Ignoring DIP) | – | – | – | – | ✓ |
| Hidden Temporal Coupling | ✓ | – | – | – | – |
| Premature Optimization | ✓ | – | – | – | – |

This mapping helps AI agents reason not only about symptoms but also about underlying principles, guiding better suggestions that reference SOLID and canonical refactorings.[^3][^25][^5]

---

## References

1. [Feature Envy - Code Smells](https://luzkan.github.io/smells/feature-envy/) - If a method inside a class manipulates more features (be it fields or methods) of another class more...

2. [Code Smells and Its type (With Example) | PDF - Slideshare](https://www.slideshare.net/slideshow/code-smells-and-its-type-with-example/71069735) - Several types of code smells are described in detail, including duplicate code, long methods, large ...

3. [Refactoring for Software Design Smells: Managing Technical Debt](https://books.google.com/books/about/Refactoring_for_Software_Design_Smells.html?id=GGZ1oAEACAAJ) - Refactoring for Software Design Smells presents 25 structural design smells, their role in identifyi...

4. [Architecture Anti-Patterns: Automatically Detectable Violations of ...](https://researchwith.stevens.edu/en/publications/architecture-anti-patterns-automatically-detectable-violations-of/)

5. [GitHub - janaipakos/Clean-Code-Smells-and-Heuristics: A reference of code smells from Martin Fowler's Refactoring and Robert C Martin's Clean Code](https://github.com/janaipakos/Clean-Code-Smells-and-Heuristics) - A reference of code smells from Martin Fowler's Refactoring and Robert C Martin's Clean Code - janai...

6. [Recognizing and Preventing Common Data Modeling Anti-Patterns](https://www.cloudthat.com/resources/blog/recognizing-and-preventing-common-data-modeling-anti-patterns/) - Why it's problematic: God tables create tight coupling between unrelated data, make queries slower, ...

7. [Recognizing and Preventing Common Data Modeling Anti- ...](https://www.cloudthat.com/resources/blog/recognizing-and-preventing-common-data-modeling-anti-patterns) - Data modelling is the backbone of any successful application. Good models age well, scale well, and ...

8. [Your Database Table is an awful API - INNOQ](https://www.innoq.com/en/blog/2026/02/your-database-table-is-an-awful-api/) - Shared tables turn your persistence model into an integration contract – breaking information hiding...

9. [[PDF] Smells to Refactorings Quick Reference Guide - Industrial Logic](https://www.industriallogic.com/img/blog/2005/09/smellstorefactorings.pdf) - Feature Envy: Data and behavior that acts on that data belong together. When a method makes too many...

10. [OOP Code Smells by Martin Fowler and Kent Beck ... - GitHub Gist](https://gist.github.com/tgroshon/8715d054b341ed9c2a89f48356829c09) - OOP Code smells ; Couplers: binds objects together. feature envy (send more messages to object than ...

11. [System Design Anti-Patterns: Common Mistakes & How to Avoid Them ⚠️](https://www.youtube.com/watch?v=5AhXQWCIheo) - Learn about common system design anti-patterns and how to avoid them! 🚀 This video explores frequent...

12. [Shotgun Surgery - Code Smells](https://luzkan.github.io/smells/shotgun-surgery/) - The smell symptom of the Shotgun Surgery code is detected by the unnecessary requirement of changing...

13. [1](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf)

14. [Microservices Anti-Patterns: Common Mistakes and How to Avoid ...](https://dilendra.neocities.org/dilendra-portfolio/articles/microservices-anti-patterns) - 1. The Distributed Monolith. This occurs when microservices are tightly coupled despite being distri...

15. [5.4. Summary Of Results](https://arxiv.org/html/2602.07147v1)

16. [10 Microservices Anti-Patterns to Avoid for Scalable Applications](https://dzone.com/articles/10-microservices-anti-patterns-you-need-to-avoid) - Avoid common microservices pitfalls like distributed monoliths, shared databases, and chatty communi...

17. [Microservices Anti-Patterns: Strategies for Scalability & Performance](https://www.findernest.com/en/blog/microservices-anti-patterns-strategies-for-scalability-performance) - The Distributed Monolith: This anti-pattern occurs when microservices are tightly coupled and interd...

18. [Anti-patterns (distributed monolith, chatty services) in Microservices](https://leyaa.ai/codefly/learn/microservices/part-3/microservices-antipatterns-distributed-monolith-chatty-services/complexity) - Analyze Anti-patterns (distributed monolith, chatty services) in Microservices for scalability. Thro...

19. [5 Mocks and test fragility · Unit Testing Principles, Practices, and Patterns](https://livebook.manning.com/book/unit-testing/chapter-5/v-3/) - Differentiating mocks from stubs · Defining observable behavior and implementation details · Underst...

20. [Chapter 5. Mocks and test fragility · Unit Testing Principles, Practices, and Patterns](https://livebook.manning.com/book/unit-testing/chapter-5/) - Differentiating mocks from stubs · Defining observable behavior and implementation details · Underst...

21. [Testing Anti-Patterns - SkillsHunt](https://skillshunt.io/skills/superpowers/testing-anti-patterns)

22. [Anti-Patterns](https://digitaltapestry.net/testify/manual/AntiPatterns.html)

23. [testing-anti-patterns skill by chunkytortoise/enterprisehub - playbooks](https://playbooks.com/skills/chunkytortoise/enterprisehub/testing-anti-patterns) - This skill helps identify and prevent testing anti-patterns to improve reliability, speed, and maint...

24. [Mapping Code Smells and Refactorings Accurately](https://tusharma.in/preprints/ESEM2025_Smells_Refactoring_Mapping.pdf)

25. [Clean Code: The Good, the Bad and the Ugly](https://gerlacdt.github.io/blog/posts/clean_code/) - Clean Code by Robert C. Martin is a seminal programming book. A whole generation of developers, incl...

