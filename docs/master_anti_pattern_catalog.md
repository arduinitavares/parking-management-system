# Synthesized Software Engineering Anti-Pattern Master Catalog

This document merges the three input catalogs into one normalized, non-redundant reference set for architects, static-analysis tooling, and AI agents.

## Synthesis and normalization rules applied

1. Synonyms were merged into one canonical entry.
2. Each anti-pattern was given one **home category** to avoid duplication; cross-cutting relevance is captured via related patterns, SOLID mapping, and detection strategy tables.
3. Severity was normalized to **Low / Medium / High / Critical**.
4. Detection guidance was rewritten so it is actionable for AST-based tools, dependency analyzers, architecture conformance checks, and runtime observability.

## Canonicalization / alias merge log

- **God Class / God Object / Blob / Large Class / Multifaceted Abstraction** → **God Object / Blob**
- **Long Function / Long Method** → **Long Method / Deep Nesting**
- **Switch Statements / Giant Conditional / God Condition / Repeated Switches** → **Repeated Switches / Giant Conditional**
- **Long Parameter List / Too Many Arguments / Data Clumps** → **Long Parameter List / Data Clumps**
- **Primitive Obsession / Stringly Typed Domain** → **Primitive Obsession**
- **Deficient Encapsulation / Inappropriate Intimacy** → **Inappropriate Intimacy / Deficient Encapsulation**
- **Refused Bequest / Rebellious Hierarchy** → **Refused Bequest**
- **Distributed Monolith / Fake Microservices / Pseudo-Microservices** → **Distributed Monolith**
- **Chatty Interfaces / Chatty Remote Calls / Chatty Services** → **Chatty Services**
- **Nanoservices / Too Many Microservices / 'The More the Merrier'** → **Nanoservices**
- **API Gateway God Service / Smart UI** → **API Gateway Mini-Monolith / Smart UI**
- **Fragile Tests / Brittle Tests** → **Fragile Tests**
- **Over-Mocking / Mockery / The Mockery** → **Over-Mocking**
- **Anal Probe / Testing Implementation Details** → **Testing Implementation Details**
- **Conjoined Twins / Shared Fixture / Inter-test Coupling** → **Shared Fixture / Inter-test Coupling**
- **God Table / Wide Table** → **God Table**
- **EAV / EAV Trap / EAV Abuse** → **EAV Abuse**
- **Polymorphic Association / Dual-Purpose Foreign Key** → **Polymorphic Associations**
- **Monolithic IaC** → **Monolithic Infrastructure as Code**
- **Complicated Serverless Setups / Lambda Pinball** → **Complicated Serverless Setups / Lambda Pinball**
- **Concrete Dependency / Service Locator** → **Concrete Dependency / Service Locator**

## Unified taxonomy

### Code-Level Anti-Patterns
Duplicated Code, Long Method / Deep Nesting, Long Parameter List / Data Clumps, Primitive Obsession, Repeated Switches / Giant Conditional, Swallowed Exceptions / Error Hiding

### Object-Oriented Design Anti-Patterns
Anemic Domain Model, Fat Interface, Feature Envy, God Object / Blob, Inappropriate Intimacy / Deficient Encapsulation, Message Chains, Refused Bequest

### Architecture Anti-Patterns
Big Ball of Mud, Blind Pattern Following / Cargo Cult Architecture, Complicated Serverless Setups / Lambda Pinball, Hardcoded Environment / Configuration, Hub-like Dependency / God Library, Layering Violations / Layer Skipping, Monolithic Infrastructure as Code, Mutable Artifacts, Unstable Dependency

### Microservices Anti-Patterns
API Gateway Mini-Monolith / Smart UI, Chatty Services, Distributed Monolith, Nanoservices, Shared Database, Synchronous Dependency Chain, Wrong Bounded Context / Entity Service

### Testing Anti-Patterns
Assertion Roulette, Flaky Tests, Fragile Tests, Mystery Guest, Over-Mocking, Shared Fixture / Inter-test Coupling, Slow Test Suite, Testing Implementation Details

### Data / Database Anti-Patterns
EAV Abuse, God Table, N+1 Query, Naive Trees, Overloaded Column / Semantic Overloading, Polymorphic Associations, SQL Injection, Spaghetti Query

### Dependency Anti-Patterns
Concrete Dependency / Service Locator, Cyclic Dependencies, Dependency Hell, Hidden Temporal Coupling

### Performance Anti-Patterns
Busy Waiting / Race Hazard, Extraneous Fetching, Improper Caching, Premature Optimization

### Maintainability Anti-Patterns
Dead Code, Divergent Change, Shotgun Surgery, Spaghetti Code

### Organizational Anti-Patterns
Dedicated DevOps Silo, Golden Hammer, Manual Deployments, Toil Accumulation

## Master Anti-Pattern Catalog

## Code-Level Anti-Patterns

### Duplicated Code

**Category**: Code-Level Anti-Patterns
**Description**: The same or near-identical logic is implemented in multiple places instead of being factored behind one abstraction.
**Symptoms**: Copy-paste blocks; parallel edits across files; behavior diverges because one clone is updated and another is not.
**Why It’s Bad**: It multiplies change cost, creates divergence defects, and blocks confident refactoring.
**Detection Heuristics**: Token/AST clone detection; repeated call sequences; high co-change between similar functions.
**Severity**: High
**Example**: Two pricing functions differ only by variable names and drift over time.
**Refactoring / Solution**: Extract Method or Extract Class; parameterize the variation; remove clone families systematically.
**Related Patterns**: Template Method, Strategy, Composite
**SOLID Violations**: SRP (indirect), OCP (indirect)
**Sources**: B, C

### Long Method / Deep Nesting

**Category**: Code-Level Anti-Patterns
**Description**: A function grows until it mixes orchestration, branching, and low-level details in one scope; deep nesting is its usual structural symptom.
**Symptoms**: Large bodies; many temporaries; scrolling to understand a routine; path explosion from nested conditionals and loops.
**Why It’s Bad**: It raises cognitive load, hides invariants, and makes testing and modification high risk.
**Detection Heuristics**: LOC, cyclomatic and NPath complexity, nesting depth, branch count, hotspot churn.
**Severity**: High
**Example**: A checkout function validates input, calculates pricing, writes to the database, and sends notifications.
**Refactoring / Solution**: Extract Function; Split Phase; Replace Temp with Query; move domain logic into cohesive collaborators.
**Related Patterns**: Command, Strategy, Template Method
**SOLID Violations**: SRP
**Sources**: A, B, C

### Long Parameter List / Data Clumps

**Category**: Code-Level Anti-Patterns
**Description**: APIs accept too many arguments, especially recurring groups that should be modeled as one cohesive type.
**Symptoms**: Four-plus related parameters; repeated tuples like street/city/postcode/country; boolean flag soup.
**Why It’s Bad**: Calls become fragile and opaque; the missing abstraction spreads validation and construction logic everywhere.
**Detection Heuristics**: Parameter-count thresholds; repeated parameter co-occurrence; many literal-heavy call sites.
**Severity**: Medium
**Example**: create_user(name, email, street, city, zip_code, country, is_admin, send_welcome)
**Refactoring / Solution**: Introduce Parameter Object; Preserve Whole Object; create immutable value objects for recurring clusters.
**Related Patterns**: Value Object, Builder
**SOLID Violations**: SRP (indirect)
**Sources**: B, C

### Primitive Obsession

**Category**: Code-Level Anti-Patterns
**Description**: Domain concepts are represented with raw strings, numbers, and generic collections instead of small types with invariants.
**Symptoms**: Repeated validation/parsing; semantic strings such as currency or region codes; unit confusion.
**Why It’s Bad**: Type safety is weakened and invariants leak into every caller.
**Detection Heuristics**: Recurrent primitive clusters around domain terms; repeated regex/substring logic; magic strings for state.
**Severity**: Medium
**Example**: Money is passed around as float + currency string in dozens of services.
**Refactoring / Solution**: Replace Primitive with Object; Replace Type Code with Class/Enum; move validation into value objects.
**Related Patterns**: Value Object, Enum
**SOLID Violations**: SRP (indirect), OCP (indirect)
**Sources**: A, B, C

### Repeated Switches / Giant Conditional

**Category**: Code-Level Anti-Patterns
**Description**: Variant behavior is encoded as repeated condition trees instead of extension points such as polymorphism, tables, or registries.
**Symptoms**: Multiple switch/match chains over the same discriminator; adding a new case requires edits in many files.
**Why It’s Bad**: It creates change amplification and tends to violate open/closed design.
**Detection Heuristics**: Repeated discriminant expressions; branch count thresholds; co-change across switch sites.
**Severity**: High
**Example**: Every report type is handled with repeated if/elif chains in controllers, serializers, and validators.
**Refactoring / Solution**: Replace Conditional with Polymorphism; introduce Strategy, State, or a lookup registry.
**Related Patterns**: Strategy, State, Factory Method
**SOLID Violations**: OCP
**Sources**: A, B

### Swallowed Exceptions / Error Hiding

**Category**: Code-Level Anti-Patterns
**Description**: Failures are caught and suppressed, downgraded to vague defaults, or logged without preserving actionable context.
**Symptoms**: Empty catch blocks; broad catch returning None/false; logs with no stack or identifiers.
**Why It’s Bad**: It converts explicit failure into silent corruption and destroys diagnosability.
**Detection Heuristics**: Empty catch/except; broad handlers; default sentinel return after exception; missing rethrow or mapping.
**Severity**: Critical
**Example**: A persistence write fails, but the caller receives None and continues as if the write succeeded.
**Refactoring / Solution**: Catch narrow exceptions; add context; propagate or map to domain errors; fail fast on invariant breaches.
**Related Patterns**: Result/Either, Circuit Breaker at boundaries
**SOLID Violations**: SRP (indirect)
**Sources**: B

## Object-Oriented Design Anti-Patterns

### Anemic Domain Model

**Category**: Object-Oriented Design Anti-Patterns
**Description**: Domain objects hold data while behavior and invariants live in procedural service layers.
**Symptoms**: Entities with getters/setters only; service classes containing most domain rules and state transitions.
**Why It’s Bad**: Encapsulation is lost, invariants scatter, and every change becomes shotgun surgery across services.
**Detection Heuristics**: Data-heavy classes with little behavior; service classes dominating domain semantics; mutation outside aggregates.
**Severity**: High
**Example**: Order is a data bag while OrderService implements pricing, discounting, and status transitions.
**Refactoring / Solution**: Move behavior into entities and value objects; define aggregates and narrow domain services.
**Related Patterns**: Rich Domain Model, Aggregate
**SOLID Violations**: SRP (domain-level), OCP (indirect)
**Sources**: B, C

### Fat Interface

**Category**: Object-Oriented Design Anti-Patterns
**Description**: An interface forces clients to depend on methods they do not need.
**Symptoms**: Many methods with partial implementations; clients using tiny subsets; adapters full of NotImplemented members.
**Why It’s Bad**: It increases coupling and redeploy cost and pushes instability through the type system.
**Detection Heuristics**: Large interface size; low method usage overlap across consumers; stubbed implementations.
**Severity**: High
**Example**: A ReportExporter interface includes print(), email(), archive(), and upload() even when most clients need one capability.
**Refactoring / Solution**: Split interfaces by role; segregate read/write concerns; define smaller protocols.
**Related Patterns**: Role Interface, Hexagonal Port
**SOLID Violations**: ISP
**Sources**: B

### Feature Envy

**Category**: Object-Oriented Design Anti-Patterns
**Description**: A method is more interested in another object's data than in its own state.
**Symptoms**: Long getter chains into another object; service methods manipulating foreign fields extensively.
**Why It’s Bad**: Behavior ends up in the wrong place, increasing coupling and reducing cohesion.
**Detection Heuristics**: Foreign field/method access dominates local access; Law-of-Demeter violations plus data manipulation.
**Severity**: High
**Example**: InvoiceService computes totals exclusively by pulling data from Invoice and LineItem objects.
**Refactoring / Solution**: Move Method; move behavior to the data owner; reshape aggregates.
**Related Patterns**: Tell-Don't-Ask, Rich Domain Model
**SOLID Violations**: SRP
**Sources**: B, C

### God Object / Blob

**Category**: Object-Oriented Design Anti-Patterns
**Description**: A single class centralizes too many responsibilities, collaborators, and reasons to change.
**Symptoms**: Huge class size; low cohesion; many imports; many unrelated public methods; 'Manager'/'Processor' naming.
**Why It’s Bad**: It collapses modularity, becomes a defect hotspot, and blocks independent testing and reuse.
**Detection Heuristics**: LOC and method count; LCOM/cohesion metrics; high fan-in/fan-out; centrality in change graph.
**Severity**: Critical
**Example**: An OrderManager validates requests, calculates tax, writes to storage, publishes events, and sends email.
**Refactoring / Solution**: Extract Class; Move Method/Field; split by responsibility and bounded context.
**Related Patterns**: Facade (explicit boundary, not dumping ground), Domain Service, Command
**SOLID Violations**: SRP, OCP, DIP
**Sources**: A, B, C

### Inappropriate Intimacy / Deficient Encapsulation

**Category**: Object-Oriented Design Anti-Patterns
**Description**: Two classes know or mutate too much of each other's internal state, often through leaky accessors or exposed collections.
**Symptoms**: Public mutable fields; paired classes with dense bidirectional calls; direct collection mutation across boundaries.
**Why It’s Bad**: Encapsulation collapses and small internal changes ripple through multiple modules.
**Detection Heuristics**: Public mutable members; dense pairwise call graphs; getters returning mutable internals.
**Severity**: High
**Example**: UserAccount exposes a mutable roles list that external services edit directly.
**Refactoring / Solution**: Encapsulate Field; return immutable views; move logic to the owning type; narrow public APIs.
**Related Patterns**: Mediator, Facade, Immutable Value Object
**SOLID Violations**: SRP, DIP (indirect)
**Sources**: A, B, C

### Message Chains

**Category**: Object-Oriented Design Anti-Patterns
**Description**: Clients navigate deep object graphs instead of asking one object to perform the needed behavior.
**Symptoms**: Train-wreck calls such as a.b().c().d(); frequent breakage when internal structures change.
**Why It’s Bad**: Callers become tightly coupled to internal object structure and composition choices.
**Detection Heuristics**: Member-access chain length; Law-of-Demeter rules; repeated chained navigation patterns.
**Severity**: Medium
**Example**: order.customer().address().country().currency_code()
**Refactoring / Solution**: Hide Delegate; move behavior closer to the data; expose intent-level methods.
**Related Patterns**: Law of Demeter, Facade
**SOLID Violations**: DIP (indirect)
**Sources**: C

### Refused Bequest

**Category**: Object-Oriented Design Anti-Patterns
**Description**: A subtype inherits a contract it cannot honestly honor and therefore disables or rejects inherited behavior.
**Symptoms**: Overrides that throw UnsupportedOperationException; empty method bodies; subtype only uses a fraction of base behavior.
**Why It’s Bad**: Substitutability is broken and polymorphism becomes unsafe.
**Detection Heuristics**: Subclass overrides that no-op or throw for inherited methods; base contract not honored.
**Severity**: Critical
**Example**: Penguin extends Bird and overrides fly() to throw.
**Refactoring / Solution**: Push behavior down; extract a better hierarchy; prefer composition over inheritance.
**Related Patterns**: Composition over Inheritance, Role Object
**SOLID Violations**: LSP
**Sources**: A, B, C

## Architecture Anti-Patterns

### Big Ball of Mud

**Category**: Architecture Anti-Patterns
**Description**: The system has no stable, enforceable structure; everything can depend on everything.
**Symptoms**: Dense dependency graph; blurred layers; cross-cutting changes; onboarding requires tribal knowledge.
**Why It’s Bad**: The whole system becomes unpredictable and expensive to evolve; architectural recovery dominates feature work.
**Detection Heuristics**: Dependency density; cycles across packages; no consistent direction of dependencies; architecture rule violations.
**Severity**: Critical
**Example**: UI code queries storage directly while domain rules live across controllers, scripts, and templates.
**Refactoring / Solution**: Establish explicit boundaries; refactor toward a modular monolith or hexagonal architecture; enforce rules in CI.
**Related Patterns**: Layered Architecture, Hexagonal Architecture, Strangler Fig
**SOLID Violations**: SRP (system-level), DIP
**Sources**: A, B, C

### Blind Pattern Following / Cargo Cult Architecture

**Category**: Architecture Anti-Patterns
**Description**: A pattern or technology is adopted because it is fashionable, not because the problem demands it.
**Symptoms**: Simple systems built with CQRS, event sourcing, or microservices without measured need; abstraction layers exceed business logic.
**Why It’s Bad**: Accidental complexity increases faster than delivered value.
**Detection Heuristics**: Architecture-review heuristics: abstraction-to-business-logic ratio, unnecessary brokers/orchestrators, low scale but high distributed overhead.
**Severity**: High
**Example**: A five-user internal scheduling tool is built as a globally distributed event-sourced microservice mesh.
**Refactoring / Solution**: Re-scope to the simplest architecture that satisfies current constraints; remove premature layers; prove the need with measurements.
**Related Patterns**: YAGNI, Modular Monolith
**SOLID Violations**: DIP (misapplied), SRP (often indirect)
**Sources**: A, B

### Complicated Serverless Setups / Lambda Pinball

**Category**: Architecture Anti-Patterns
**Description**: Many tiny functions are chained through implicit triggers, creating a fragmented control flow with poor observability.
**Symptoms**: Deep trigger graphs; bucket events and queue hops used as control flow; hard-to-debug cold-start heavy request paths.
**Why It’s Bad**: Latency, operational complexity, and partial-failure recovery all become difficult.
**Detection Heuristics**: Parse cloud resource definitions into a trigger graph; flag deep chains without an explicit orchestrator or state machine.
**Severity**: High
**Example**: API Gateway -> Lambda A -> SQS -> Lambda B -> DynamoDB stream -> Lambda C
**Refactoring / Solution**: Consolidate related behavior; introduce explicit orchestration/state machines; reduce trigger depth.
**Related Patterns**: Workflow Orchestrator, Step Functions, Saga
**SOLID Violations**: SRP (system-level, often indirect)
**Sources**: A

### Hardcoded Environment / Configuration

**Category**: Architecture Anti-Patterns
**Description**: Environment-specific values and secrets are embedded in code or build artifacts instead of externalized configuration.
**Symptoms**: Hostnames, credentials, feature flags, and environment branches in source code.
**Why It’s Bad**: It blocks safe deployment, leaks secrets, and makes environments diverge.
**Detection Heuristics**: Pattern matching for URLs/hosts/credentials; environment-name branching; secret scanning.
**Severity**: High
**Example**: Production DB_URL and API keys are checked into source.
**Refactoring / Solution**: Externalize configuration; use secret stores and environment-specific config injection; adopt 12-factor configuration discipline.
**Related Patterns**: Externalized Configuration, 12-Factor App
**SOLID Violations**: DIP (indirect)
**Sources**: C, B

### Hub-like Dependency / God Library

**Category**: Architecture Anti-Patterns
**Description**: A central component becomes the transit hub for many unrelated dependencies or business flows.
**Symptoms**: One shared library imported everywhere; releases blocked by central module changes; high centrality in graph analysis.
**Why It’s Bad**: Change amplification and bottleneck ownership emerge around one unstable center.
**Detection Heuristics**: Betweenness/centrality metrics; fan-in/fan-out outliers; many executables depending on one fat shared module.
**Severity**: High
**Example**: Every service depends on company-core.jar, which contains business policies, DTOs, and integration helpers.
**Refactoring / Solution**: Split the hub by business capability; keep only thin shared contracts/utilities; publish APIs or events instead of shared logic.
**Related Patterns**: Published Language, Shared Kernel (narrow), Facade
**SOLID Violations**: SRP, DIP
**Sources**: B, C

### Layering Violations / Layer Skipping

**Category**: Architecture Anti-Patterns
**Description**: Code bypasses intended layers and reaches across boundaries directly.
**Symptoms**: Presentation code talks to repositories or SQL; domain code reaches into transport and persistence details.
**Why It’s Bad**: Contracts become unstable, concerns bleed together, and replacing infrastructure becomes expensive.
**Detection Heuristics**: Static dependency rules between layers; forbidden import checks; architecture tests.
**Severity**: High
**Example**: A controller builds SQL and writes directly to the database.
**Refactoring / Solution**: Restore inward dependency flow; introduce application services and adapters; enforce boundaries automatically.
**Related Patterns**: Clean Architecture, Ports and Adapters
**SOLID Violations**: DIP, SRP
**Sources**: B, C

### Monolithic Infrastructure as Code

**Category**: Architecture Anti-Patterns
**Description**: One giant infrastructure state or template manages networking, compute, data, and identity in a single blast radius.
**Symptoms**: Thousands of lines in one root stack; slow plans; fear of any change; pipeline requires broad account permissions.
**Why It’s Bad**: A small mistake can affect the whole platform, and ownership boundaries disappear.
**Detection Heuristics**: Resource-count and blast-radius thresholds; graph analysis of one stack spanning multiple lifecycles/domains.
**Severity**: High
**Example**: A single Terraform root module provisions VPCs, databases, clusters, IAM, and app resources together.
**Refactoring / Solution**: Modularize by lifecycle and ownership; isolate state; reference outputs rather than share one root graph.
**Related Patterns**: Modular IaC, Least Privilege
**SOLID Violations**: SRP (system-level)
**Sources**: A

### Mutable Artifacts

**Category**: Architecture Anti-Patterns
**Description**: Build artifacts can be overwritten or silently changed after publication.
**Symptoms**: Floating tags like latest; rollbacks fetch different bytes than were tested; artifact registry allows tag overwrite.
**Why It’s Bad**: Release integrity and supply-chain trust are lost.
**Detection Heuristics**: Registry policy checks; CI rules for floating tags; immutability flags and signature verification.
**Severity**: Critical
**Example**: myapp:v1.0 is overwritten with a patched image instead of publishing v1.0.1.
**Refactoring / Solution**: Use immutable versioned artifacts, digests, signatures, and registry policies that reject overwrite.
**Related Patterns**: Semantic Versioning, Provenance/SBOM
**SOLID Violations**: None directly
**Sources**: A

### Unstable Dependency

**Category**: Architecture Anti-Patterns
**Description**: A supposedly stable module depends on volatile, frequently changing modules or libraries.
**Symptoms**: Core modules recompile often; small leaf changes ripple upstream; central utilities change constantly.
**Why It’s Bad**: Volatility propagates into the core and erodes modularity.
**Detection Heuristics**: Instability metrics, fan-in/fan-out, change frequency, Arcan-style architectural smell detection.
**Severity**: Critical
**Example**: core-domain depends directly on an experimental UI component package.
**Refactoring / Solution**: Invert the dependency through interfaces and adapters; keep stable policy independent from volatile detail.
**Related Patterns**: Stable Dependencies Principle, Adapter
**SOLID Violations**: DIP
**Sources**: A, B, C

## Microservices Anti-Patterns

### API Gateway Mini-Monolith / Smart UI

**Category**: Microservices Anti-Patterns
**Description**: The gateway or UI accumulates business orchestration and decision logic that should live behind stable backend boundaries.
**Symptoms**: Controllers or frontend routes encode workflows, pricing rules, or state transitions; gateway complexity rivals a service.
**Why It’s Bad**: Business logic becomes channel-specific and the gateway becomes the new monolith.
**Detection Heuristics**: LOC and complexity metrics on gateway/UI layers; orchestration logic and domain decisions in controllers/routes.
**Severity**: High
**Example**: A web client coordinates payment retries, eligibility rules, and stock reservation directly across services.
**Refactoring / Solution**: Move orchestration to application services or dedicated workflow components; keep the gateway focused on aggregation and protocol concerns.
**Related Patterns**: BFF, Application Service
**SOLID Violations**: SRP
**Sources**: B, C

### Chatty Services

**Category**: Microservices Anti-Patterns
**Description**: A business operation requires many fine-grained remote calls rather than a few meaningful ones.
**Symptoms**: High RPC counts per request; services calling remote getters repeatedly; latency dominated by network hops.
**Why It’s Bad**: Tail latency and failure surface expand rapidly as call volume grows.
**Detection Heuristics**: Distributed traces with repeated calls between the same pair of services; static remote-call-in-loop detection.
**Severity**: High
**Example**: For each order line, PricingService calls ProductService three times for individual fields.
**Refactoring / Solution**: Design coarse-grained APIs; aggregate at the edge; use read models or asynchronous propagation.
**Related Patterns**: Aggregator, BFF, CQRS Read Model
**SOLID Violations**: OCP (indirect), DIP (indirect)
**Sources**: A, B, C

### Distributed Monolith

**Category**: Microservices Anti-Patterns
**Description**: Services are deployed separately but remain tightly coupled in release cadence, runtime behavior, and data dependencies.
**Symptoms**: Lockstep deployments; many synchronous dependencies; multiple services must be tested or scaled together.
**Why It’s Bad**: It inherits the operational cost of distribution without the autonomy benefits.
**Detection Heuristics**: Trace depth, co-deployment/co-release analysis, cross-service change coupling, synchronous call chains.
**Severity**: Critical
**Example**: Order processing requires Billing, Inventory, Shipping, and Customer services to be available synchronously.
**Refactoring / Solution**: Redraw boundaries by bounded context; reduce synchronous coupling; prefer asynchronous integration where justified.
**Related Patterns**: Bounded Context, Event-Driven Integration
**SOLID Violations**: SRP (system-level), DIP (indirect)
**Sources**: A, B, C

### Nanoservices

**Category**: Microservices Anti-Patterns
**Description**: Functionality is split into services that are too small to justify their operational overhead.
**Symptoms**: Minimal codebases with full pipelines; many services involved in one simple workflow; trivial services like email-template-service.
**Why It’s Bad**: Operational cost, coordination overhead, and network chatter exceed the value of decomposition.
**Detection Heuristics**: Service size metrics; service-per-transaction count; call graph role analysis.
**Severity**: High
**Example**: Notification flow is split into separate template, sender, audit, and retry services for simple email delivery.
**Refactoring / Solution**: Merge services around cohesive business capabilities; prefer a modular monolith when boundaries are not yet stable.
**Related Patterns**: Modular Monolith, Bounded Context
**SOLID Violations**: SRP (at wrong level, indirect)
**Sources**: A, B, C

### Shared Database

**Category**: Microservices Anti-Patterns
**Description**: Multiple services read and write the same physical schema or tables instead of owning their own persistence.
**Symptoms**: Shared connection strings; schema changes breaking multiple services; table contention across teams.
**Why It’s Bad**: Service autonomy is lost and the database becomes an undocumented integration API.
**Detection Heuristics**: Connection/config analysis; schema access logs by service identity; multiple services mutating same tables.
**Severity**: Critical
**Example**: User and Order services both update the same users table directly.
**Refactoring / Solution**: Adopt database-per-service; publish events or APIs for integration; introduce replication/read models where needed.
**Related Patterns**: Database per Service, CQRS, Published Language
**SOLID Violations**: SRP (ownership), DIP (indirect)
**Sources**: A, B, C

### Synchronous Dependency Chain

**Category**: Microservices Anti-Patterns
**Description**: One request traverses a deep synchronous chain of services in the hot path.
**Symptoms**: Long trace critical paths; each request depends on many services being simultaneously healthy; cascade failures.
**Why It’s Bad**: Latency compounds and resilience collapses under partial failure.
**Detection Heuristics**: Distributed tracing for call depth and fan-out; synchronous HTTP/RPC usage inside request handlers.
**Severity**: Critical
**Example**: Gateway -> Service A -> Service B -> Service C -> DB for one user request.
**Refactoring / Solution**: Break the chain with async messaging, local caches, sagas, or service consolidation; add timeouts and circuit breakers.
**Related Patterns**: Saga, Event-Driven Architecture, Circuit Breaker
**SOLID Violations**: DIP (indirect)
**Sources**: B, C

### Wrong Bounded Context / Entity Service

**Category**: Microservices Anti-Patterns
**Description**: Services are organized around generic CRUD entities instead of business capabilities and context-specific models.
**Symptoms**: CustomerService is consumed by billing, marketing, KYC, and support; one canonical entity leaks across contexts.
**Why It’s Bad**: Context boundaries blur and the system drifts toward a distributed monolith.
**Detection Heuristics**: Entity-centric service names; cross-team dependency concentration on generic services; cross-context field growth.
**Severity**: High
**Example**: A single ProductService serves catalog, pricing, fulfillment, and recommendations.
**Refactoring / Solution**: Re-cut services around bounded contexts; allow distinct models per context; define explicit integration contracts.
**Related Patterns**: Bounded Context, Context Map, Anti-Corruption Layer
**SOLID Violations**: SRP
**Sources**: B, C

## Testing Anti-Patterns

### Assertion Roulette

**Category**: Testing Anti-Patterns
**Description**: A test contains many opaque assertions with poor failure messages, making diagnosis slow.
**Symptoms**: Large blocks of bare asserts; failures such as 'expected false to be true' without context.
**Why It’s Bad**: Mean time to diagnose a failing test rises and teams start ignoring failures.
**Detection Heuristics**: Many assertions per test without labels/helpers; boolean asserts on large objects; missing descriptive names.
**Severity**: Medium
**Example**: One API test validates an entire response with twenty unlabeled asserts.
**Refactoring / Solution**: Split tests by concern; use richer assertions and descriptive names; add intent-revealing helpers.
**Related Patterns**: Given-When-Then, Specification by Example
**SOLID Violations**: None directly
**Sources**: B, C

### Flaky Tests

**Category**: Testing Anti-Patterns
**Description**: Tests pass and fail nondeterministically without relevant code changes.
**Symptoms**: Intermittent CI failures; reruns pass; dependence on time, randomness, order, or shared infrastructure.
**Why It’s Bad**: CI signal becomes noisy and real defects get ignored.
**Detection Heuristics**: Historical intermittency; uncontrolled time/random/network usage; order-dependent suite failures.
**Severity**: Critical
**Example**: A cache test fails depending on background eviction timing.
**Refactoring / Solution**: Control time and randomness; isolate external systems; remove shared mutable state; make tests hermetic.
**Related Patterns**: Hermetic Tests, Test Doubles
**SOLID Violations**: None directly
**Sources**: B, C

### Fragile Tests

**Category**: Testing Anti-Patterns
**Description**: Tests break under behavior-preserving refactors because they are coupled to structure instead of observable outcomes.
**Symptoms**: Internal call-order assertions; failures after harmless refactors; test churn mirrors implementation churn.
**Why It’s Bad**: Refactoring becomes expensive and teams stop trusting tests as safety nets.
**Detection Heuristics**: Frequent VCS churn in tests after internal-only changes; reflection/private-state access; interaction-heavy assertions.
**Severity**: High
**Example**: A test fails because collaborators are called in a different order even though behavior is unchanged.
**Refactoring / Solution**: Assert outcomes through public APIs; reduce interaction assertions; test behavior, not construction details.
**Related Patterns**: FIRST tests, classicist unit testing
**SOLID Violations**: None directly
**Sources**: A, B, C

### Mystery Guest

**Category**: Testing Anti-Patterns
**Description**: A test relies on hidden external fixtures or pre-existing data instead of declaring its own setup.
**Symptoms**: Queries for data 'already in the DB'; hidden files or environment assumptions; test meaning is not local.
**Why It’s Bad**: Tests become hard to understand, reproduce, and evolve.
**Detection Heuristics**: Data access without local setup; references to shared fixture files or seeded records outside the test.
**Severity**: Medium
**Example**: A test fetches [email protected] from the database without creating that user in the test.
**Refactoring / Solution**: Make fixtures explicit and local; use builders/factories; hide shared setup behind readable helpers.
**Related Patterns**: Test Data Builder, Object Mother
**SOLID Violations**: None directly
**Sources**: C

### Over-Mocking

**Category**: Testing Anti-Patterns
**Description**: Tests verify mock configuration and internal collaborations instead of observable behavior.
**Symptoms**: Setup dominates the test; many verify/assert_called_with lines; any internal refactor breaks tests.
**Why It’s Bad**: Tests lock the design, hide intent, and create false confidence from high line coverage.
**Detection Heuristics**: High ratio of mocking API calls to assertions; interaction assertions outnumber state assertions.
**Severity**: High
**Example**: A controller test mocks repository, validator, mapper, publisher, and cache just to verify call order.
**Refactoring / Solution**: Use real domain objects and fakes where possible; reserve mocks for true architectural boundaries.
**Related Patterns**: Contract Test, Ports and Adapters
**SOLID Violations**: None directly
**Sources**: A, B, C

### Shared Fixture / Inter-test Coupling

**Category**: Testing Anti-Patterns
**Description**: Tests share mutable state or depend on execution order.
**Symptoms**: Pass individually but fail as a suite; reset scripts between tests; hidden dependencies on previous test artifacts.
**Why It’s Bad**: Isolation is lost and failures become nondeterministic and expensive to debug.
**Detection Heuristics**: Shared globals/fixtures, uncleaned filesystem/DB state, order-dependent failures, suite-only breakage.
**Severity**: High
**Example**: test_b assumes test_a already inserted a row.
**Refactoring / Solution**: Provide per-test fixtures, transactional isolation, ephemeral environments, and strict cleanup.
**Related Patterns**: Ephemeral Environment, Test Containers
**SOLID Violations**: None directly
**Sources**: B, C

### Slow Test Suite

**Category**: Testing Anti-Patterns
**Description**: The default developer feedback loop is slow because most tests are expensive integration or E2E checks.
**Symptoms**: CI runs take tens of minutes or hours; developers avoid local runs; failures are found in large batches.
**Why It’s Bad**: Slow feedback increases risk and encourages larger, less frequent changes.
**Detection Heuristics**: Per-test runtime telemetry; high proportion of tests needing DB/network/browser; low fast-test ratio.
**Severity**: High
**Example**: Most of the suite launches browsers and real services for scenarios that could be covered at component level.
**Refactoring / Solution**: Rebalance the test pyramid; isolate boundaries; keep only critical E2E paths; parallelize where sound.
**Related Patterns**: Test Pyramid, Consumer-Driven Contract
**SOLID Violations**: None directly
**Sources**: A, B, C

### Testing Implementation Details

**Category**: Testing Anti-Patterns
**Description**: Tests break encapsulation by inspecting private fields or helper methods rather than exercising the public contract.
**Symptoms**: Reflection in tests; VisibleForTesting access widening; assertions on private state.
**Why It’s Bad**: Safe internal refactoring becomes impossible, so tests actively prevent cleanup.
**Detection Heuristics**: Reflection/private-member access in test code; test-only access modifiers; internal-state assertions.
**Severity**: High
**Example**: A unit test calls a private tax_calculation() helper through reflection.
**Refactoring / Solution**: Test public behavior; if private logic is too complex, extract it into a new type with a real contract.
**Related Patterns**: Extract Class, Sociable Unit Tests
**SOLID Violations**: None directly
**Sources**: A, C

## Data / Database Anti-Patterns

### EAV Abuse

**Category**: Data / Database Anti-Patterns
**Description**: Entity-attribute-value schemas are overused for core domain data instead of exceptional dynamic metadata.
**Symptoms**: Most business data lives in entity/attribute/value rows; queries require many pivots and self-joins.
**Why It’s Bad**: Type safety, constraints, and queryability all degrade sharply.
**Detection Heuristics**: Schema scan for attr/value tables; polymorphic value columns; repeated pivot/self-join reconstruction queries.
**Severity**: High
**Example**: User profile fields are reconstructed from fifteen rows in a generic properties table.
**Refactoring / Solution**: Model stable attributes explicitly; use dependent tables or JSON columns only where justified and indexed.
**Related Patterns**: Metadata Table, CQRS Read Model
**SOLID Violations**: None directly
**Sources**: A, B, C

### God Table

**Category**: Data / Database Anti-Patterns
**Description**: One wide table accumulates unrelated concerns and becomes the persistence dumping ground for multiple concepts.
**Symptoms**: Very high column count; many nulls per row; many modules or services depend on the same table for different reasons.
**Why It’s Bad**: Schema evolution becomes risky, indexes perform poorly, and ownership is unclear.
**Detection Heuristics**: DDL metrics for width and sparsity; access logs from many modules/services; overloaded generic column names.
**Severity**: High
**Example**: A single assets table stores both network device attributes and office-furniture attributes.
**Refactoring / Solution**: Normalize into cohesive tables per concern; introduce views/read models for combined reads.
**Related Patterns**: Normalization, Database per Service
**SOLID Violations**: SRP (data ownership, indirect)
**Sources**: A, B, C

### N+1 Query

**Category**: Data / Database Anti-Patterns
**Description**: One query loads parent rows and then one query per parent is issued to load related data.
**Symptoms**: ORM lazy loads inside loops; query logs show many near-identical statements per request.
**Why It’s Bad**: Latency and database load grow with result size and can dominate request cost.
**Detection Heuristics**: Static detection of DB/ORM calls inside loops; runtime clustering of repeated statements per trace.
**Severity**: High
**Example**: For each order in a list, the code separately queries its line items.
**Refactoring / Solution**: Use eager loading, joins, batch fetching, or read models; cache where appropriate.
**Related Patterns**: Batch Fetching, Repository, Unit of Work
**SOLID Violations**: None directly
**Sources**: A, B, C

### Naive Trees

**Category**: Data / Database Anti-Patterns
**Description**: Hierarchies are modeled in ways that make ancestor/descendant queries expensive or depth-limited.
**Symptoms**: Repeated self-joins; manual depth limits; application recursion compensates for schema weakness.
**Why It’s Bad**: Queries scale poorly and hierarchy behavior becomes ad hoc.
**Detection Heuristics**: Adjacency-list plus repeated self-joins; level columns; depth assumptions in code.
**Severity**: Medium
**Example**: Category navigation is limited to four levels because deeper traversal is too expensive.
**Refactoring / Solution**: Choose a tree model that matches query patterns: closure table, path enumeration, or nested sets.
**Related Patterns**: Closure Table, Path Enumeration
**SOLID Violations**: None directly
**Sources**: B

### Overloaded Column / Semantic Overloading

**Category**: Data / Database Anti-Patterns
**Description**: One column stores multiple meanings, units, or logical states depending on context.
**Symptoms**: Generic columns like value, status, code, attr_str_1; application switches on column meaning.
**Why It’s Bad**: Queries and constraints become opaque, and data quality errors are hard to prevent.
**Detection Heuristics**: Column value diversity inconsistent with declared meaning; application-side switches over a column's interpretation.
**Severity**: Medium
**Example**: status_code stores payment state for one row type and shipping state for another.
**Refactoring / Solution**: Split the model by concept; create explicit columns or tables; add domain constraints.
**Related Patterns**: Normalization, Value Object
**SOLID Violations**: None directly
**Sources**: C

### Polymorphic Associations

**Category**: Data / Database Anti-Patterns
**Description**: A relation is modeled as type + id pointing to multiple parent tables instead of a real foreign key.
**Symptoms**: Columns like parent_type and parent_id; no referential integrity; conditional joins everywhere.
**Why It’s Bad**: Integrity becomes application-enforced and migrations become brittle.
**Detection Heuristics**: Schema pattern matching for *_type + *_id; lack of real foreign keys; conditional association logic.
**Severity**: High
**Example**: comments(subject_type, subject_id) can point to posts, photos, or videos.
**Refactoring / Solution**: Use proper association tables or a supertype table with real constraints.
**Related Patterns**: Association Table, Table Inheritance
**SOLID Violations**: None directly
**Sources**: B, C

### SQL Injection

**Category**: Data / Database Anti-Patterns
**Description**: Queries are built by concatenating untrusted input instead of binding parameters.
**Symptoms**: String-built SQL; quote escaping logic in application code; tainted input flows into query text.
**Why It’s Bad**: This is a direct security exposure with potentially catastrophic impact.
**Detection Heuristics**: Taint analysis from input to query string; string concatenation near execute(); missing prepared statements.
**Severity**: Critical
**Example**: SELECT * FROM users WHERE name = '<user_input>'
**Refactoring / Solution**: Use prepared statements and parameter binding; isolate query construction behind safe data access APIs.
**Related Patterns**: Prepared Statement, Query Object
**SOLID Violations**: None directly
**Sources**: B

### Spaghetti Query

**Category**: Data / Database Anti-Patterns
**Description**: A single SQL statement becomes so long and tangled that intent, performance, and correctness are all hard to reason about.
**Symptoms**: Huge joins and subqueries; duplicated predicates; no one can safely change the query.
**Why It’s Bad**: Defects hide in complexity and optimization becomes guesswork.
**Detection Heuristics**: SQL parse-tree depth; statement length; join count; repeated nested subqueries.
**Severity**: Medium
**Example**: A 300-line report query mixes filtering, aggregation, security predicates, and formatting.
**Refactoring / Solution**: Break into views, CTEs, staged queries, or materialized/read models with clear responsibilities.
**Related Patterns**: CQRS Read Model, View
**SOLID Violations**: None directly
**Sources**: B

## Dependency Anti-Patterns

### Concrete Dependency / Service Locator

**Category**: Dependency Anti-Patterns
**Description**: High-level code depends directly on concrete implementations or retrieves collaborators through a global locator.
**Symptoms**: new ConcreteX() spread through policy code; hidden dependencies; poor test seams.
**Why It’s Bad**: It hides coupling, blocks substitution, and makes composition root discipline impossible.
**Detection Heuristics**: Instantiation of concretes in policy modules; calls to locator/global context types; low constructor visibility of dependencies.
**Severity**: High
**Example**: A controller calls ServiceLocator.get('PaymentGateway') inside its method body.
**Refactoring / Solution**: Introduce interfaces and constructor injection; move wiring to the composition root.
**Related Patterns**: Dependency Injection, Inversion of Control
**SOLID Violations**: DIP
**Sources**: C

### Cyclic Dependencies

**Category**: Dependency Anti-Patterns
**Description**: Modules, packages, or components depend on each other in one or more cycles.
**Symptoms**: Independent build or deployment is difficult; a change in one module forces recompilation of others.
**Why It’s Bad**: Cycles prevent independent evolution and often signal muddled responsibility boundaries.
**Detection Heuristics**: Graph cycle detection over packages, modules, services, or architecture components.
**Severity**: High
**Example**: billing imports customer and customer imports billing.
**Refactoring / Solution**: Break the cycle with new abstractions, interfaces, responsibility moves, or a lower shared module with narrow scope.
**Related Patterns**: Dependency Inversion, Common Closure Principle
**SOLID Violations**: DIP (indirect)
**Sources**: A, B, C

### Dependency Hell

**Category**: Dependency Anti-Patterns
**Description**: The dependency graph becomes unmanageable because of incompatible versions and tightly coupled transitive constraints.
**Symptoms**: Upgrade deadlocks; lockfile churn; 'works on my machine' failures; big-bang upgrade projects.
**Why It’s Bad**: Security patches are delayed and builds become fragile and expensive to maintain.
**Detection Heuristics**: Conflicting version constraints; high transitive depth; frequent lockfile conflicts; large exception allowlists.
**Severity**: High
**Example**: libA requires X<2 while libB requires X>=2, blocking both upgrades and security patches.
**Refactoring / Solution**: Reduce dependency surface area; isolate volatile libraries behind adapters; adopt compatibility and upgrade policies.
**Related Patterns**: Adapter, Semantic Versioning
**SOLID Violations**: None directly
**Sources**: B

### Hidden Temporal Coupling

**Category**: Dependency Anti-Patterns
**Description**: Correct behavior depends on call order, but the API does not make that sequencing explicit.
**Symptoms**: Comments like 'call init() first'; state bugs when methods are invoked in another order.
**Why It’s Bad**: The API is easy to misuse and failures appear far from the cause.
**Detection Heuristics**: Separate initialize/open/use methods on mutable types; precondition-sensitive call sequences.
**Severity**: Medium
**Example**: connect() must be called before send(), but the type system does not enforce it.
**Refactoring / Solution**: Encode legal states explicitly; use staged builders, state objects, or lifecycle wrappers.
**Related Patterns**: State, Staged Builder
**SOLID Violations**: None directly
**Sources**: C

## Performance Anti-Patterns

### Busy Waiting / Race Hazard

**Category**: Performance Anti-Patterns
**Description**: Concurrency or waiting logic relies on polling and unsafely shared state instead of proper coordination.
**Symptoms**: Spin loops; sleeps used for synchronization; timing-dependent failures and nondeterministic state corruption.
**Why It’s Bad**: CPU is wasted and concurrency defects become intermittent and hard to reproduce.
**Detection Heuristics**: AST patterns for polling loops and sleep-based synchronization; runtime contention and timing anomalies.
**Severity**: High
**Example**: A worker loops until a flag changes, sleeping 10 ms between checks.
**Refactoring / Solution**: Use proper synchronization primitives, condition variables, queues, and ownership discipline; remove timing assumptions.
**Related Patterns**: Producer-Consumer, Actor Model
**SOLID Violations**: None directly
**Sources**: A

### Extraneous Fetching

**Category**: Performance Anti-Patterns
**Description**: Code fetches much more data than the caller actually needs.
**Symptoms**: SELECT * for narrow views; oversized API payloads; high serialization cost and memory pressure.
**Why It’s Bad**: Latency, resource usage, and cost increase without improving behavior.
**Detection Heuristics**: Projection analysis; unused response fields; payload-size telemetry; wide select statements.
**Severity**: Medium
**Example**: A list endpoint returns full object graphs even though the UI shows only name and status.
**Refactoring / Solution**: Use explicit projections, DTOs, pagination, and shape responses to use cases.
**Related Patterns**: DTO, CQRS Read Model
**SOLID Violations**: None directly
**Sources**: A, B

### Improper Caching

**Category**: Performance Anti-Patterns
**Description**: Caching is absent where clearly needed or implemented with unsafe keys, TTLs, or invalidation behavior.
**Symptoms**: Hot paths recompute everything; stale data served; cache stampedes; user-specific data leaks across keys.
**Why It’s Bad**: Performance suffers and correctness bugs can become severe.
**Detection Heuristics**: Repeated expensive calls; mismatched TTLs; missing invalidation events; cache-key analysis; load spikes on misses.
**Severity**: High
**Example**: A cache key omits user_id and serves one user's data to another.
**Refactoring / Solution**: Choose cache strategy per data class; fix key design; add request coalescing, invalidation, and observability.
**Related Patterns**: Cache-Aside, Read-Through
**SOLID Violations**: None directly
**Sources**: A, B

### Premature Optimization

**Category**: Performance Anti-Patterns
**Description**: Complex optimizations are introduced before profiling or evidence justifies their cost.
**Symptoms**: Hand-rolled caches and data structures in non-hot code; complexity with no benchmark trail.
**Why It’s Bad**: Readability and correctness are traded away without proven benefit.
**Detection Heuristics**: Complex performance code with no associated profiling or performance tests; optimization in low-volume paths.
**Severity**: Medium
**Example**: A custom memory pool is added to a code path called a few hundred times per day.
**Refactoring / Solution**: Simplify first; optimize only after measurement; keep performance decisions traceable to benchmarks.
**Related Patterns**: YAGNI, Simple Design
**SOLID Violations**: None directly
**Sources**: C

## Maintainability Anti-Patterns

### Dead Code

**Category**: Maintainability Anti-Patterns
**Description**: Unused paths, symbols, and obsolete flows remain in the codebase long after they stop serving production behavior.
**Symptoms**: Unused functions; feature-flagged branches never exercised; commented-out old implementations.
**Why It’s Bad**: Noise grows, security risk hides, and reviewers spend time reasoning about behavior that no longer matters.
**Detection Heuristics**: Unused symbol analysis; zero runtime hits; stale feature flags; low coverage plus no call sites.
**Severity**: Medium
**Example**: A deprecated payment flow remains reachable through a forgotten internal endpoint.
**Refactoring / Solution**: Instrument, confirm non-use, then remove; rely on version control for history.
**Related Patterns**: Strangler Fig (for replacements)
**SOLID Violations**: None directly
**Sources**: B, C

### Divergent Change

**Category**: Maintainability Anti-Patterns
**Description**: One module changes for many unrelated reasons and becomes a long-term hotspot.
**Symptoms**: The same class is edited for tax rules, formatting, persistence, and workflow changes.
**Why It’s Bad**: The module becomes unstable, conflict-prone, and hard to reason about.
**Detection Heuristics**: High change entropy by topic; disjoint collaborator clusters inside one class/module.
**Severity**: High
**Example**: Invoice is modified for pricing policy, PDF generation, export format, and storage concerns.
**Refactoring / Solution**: Split by reason to change; extract modules/classes around cohesive responsibilities.
**Related Patterns**: Extract Class, Split Phase
**SOLID Violations**: SRP
**Sources**: B, C

### Shotgun Surgery

**Category**: Maintainability Anti-Patterns
**Description**: A small change requires coordinated edits across many scattered files.
**Symptoms**: One requirement touches numerous classes/packages; same concern appears in many places.
**Why It’s Bad**: Change risk and omission risk rise sharply.
**Detection Heuristics**: Co-change mining; duplicated behavior across modules; broad PR blast radius for small features.
**Severity**: High
**Example**: Adding one validation rule requires edits in controllers, DTOs, services, and repositories.
**Refactoring / Solution**: Centralize the concern in one abstraction; move logic to its owner; remove duplication and repeated conditionals.
**Related Patterns**: Strategy, Template Method, Extract Class
**SOLID Violations**: SRP
**Sources**: B, C

### Spaghetti Code

**Category**: Maintainability Anti-Patterns
**Description**: Control flow and responsibilities are so tangled that local reasoning is difficult even when the system is not yet a full Big Ball of Mud.
**Symptoms**: Inconsistent naming, long methods, global state, and cross-module jumps all appear together.
**Why It’s Bad**: Maintenance cost becomes nonlinear because no single cleanup gives enough leverage.
**Detection Heuristics**: Complexity hotspot clustering; mixed concerns; heavy goto-like control flow or ad hoc branching.
**Severity**: High
**Example**: A batch job script mixes parsing, persistence, retries, formatting, and side effects in one unstructured flow.
**Refactoring / Solution**: Apply incremental refactoring: extract seams, isolate state, replace conditionals, and establish module boundaries.
**Related Patterns**: Strangler Fig, Modular Monolith
**SOLID Violations**: SRP (indirect)
**Sources**: A

## Organizational Anti-Patterns

### Dedicated DevOps Silo

**Category**: Organizational Anti-Patterns
**Description**: One separate team becomes the exclusive owner of deployment and operations concerns for everyone else.
**Symptoms**: Application teams throw work over the wall; ops knowledge is concentrated in one group; delivery queues form around the silo.
**Why It’s Bad**: Ownership and feedback loops are broken, so technical anti-patterns persist longer.
**Detection Heuristics**: Org-chart and ticket-flow analysis; deployment dependency on one team; low service ownership clarity.
**Severity**: Medium
**Example**: Every environment change waits in a centralized DevOps backlog while product teams stay detached from operability.
**Refactoring / Solution**: Move toward platform enablement plus service ownership; keep operational responsibility close to the teams shipping the software.
**Related Patterns**: Platform Team, You Build It You Run It
**SOLID Violations**: None directly
**Sources**: A

### Golden Hammer

**Category**: Organizational Anti-Patterns
**Description**: A familiar tool or pattern is applied to most problems regardless of fit.
**Symptoms**: Every solution becomes microservices, Kafka, CQRS, or a favorite framework; alternatives are not seriously considered.
**Why It’s Bad**: The organization pays repeated complexity taxes because design choices are ideology-driven, not constraint-driven.
**Detection Heuristics**: Architecture decision records show one repeated solution pattern despite very different problem shapes.
**Severity**: Medium
**Example**: A simple reporting tool is forced into an event-sourced architecture because the team used it successfully elsewhere.
**Refactoring / Solution**: Make trade-offs explicit; require alternatives in design reviews; tie architecture choices to measurable constraints.
**Related Patterns**: ADR, Decision Matrix, YAGNI
**SOLID Violations**: None directly
**Sources**: A

### Manual Deployments

**Category**: Organizational Anti-Patterns
**Description**: Releases depend on human-run procedures instead of automated, repeatable pipelines.
**Symptoms**: Click-ops; wiki runbooks; only a few people can ship safely; configuration drift between environments.
**Why It’s Bad**: Delivery slows, incidents rise, and releases are hard to audit or reproduce.
**Detection Heuristics**: Absence of automated pipeline evidence; manual approvals outside tooling; drift alerts; repeated runbook use.
**Severity**: High
**Example**: A release requires a senior engineer to click through cloud consoles in a fixed sequence.
**Refactoring / Solution**: Automate the pipeline, configuration, and rollback path; use progressive delivery with observability gates.
**Related Patterns**: Deployment Pipeline, GitOps
**SOLID Violations**: None directly
**Sources**: B

### Toil Accumulation

**Category**: Organizational Anti-Patterns
**Description**: Operational work stays manual, repetitive, automatable, and linearly scaling instead of being engineered away.
**Symptoms**: Repeated restarts, schema tweaks, alert triage, and ticket handling dominate engineering time.
**Why It’s Bad**: Reliability work is displaced by repetitive work, producing burnout and fragile operations.
**Detection Heuristics**: Ticket taxonomy; repeated runbook steps; alert volume unrelated to incidents; automation gap analysis.
**Severity**: High
**Example**: The team manually drains queues and restarts jobs every morning.
**Refactoring / Solution**: Automate repetitive ops, reduce noisy alerts, self-serve routine tasks, and budget time for reliability engineering.
**Related Patterns**: SRE Error Budgets, Self-Service Ops
**SOLID Violations**: None directly
**Sources**: B

## Top 25 Most Important Anti-Patterns

1. **Big Ball of Mud** — The whole system becomes unpredictable and expensive to evolve; architectural recovery dominates feature work.
2. **Distributed Monolith** — It inherits the operational cost of distribution without the autonomy benefits.
3. **Shared Database** — Service autonomy is lost and the database becomes an undocumented integration API.
4. **God Object / Blob** — It collapses modularity, becomes a defect hotspot, and blocks independent testing and reuse.
5. **Unstable Dependency** — Volatility propagates into the core and erodes modularity.
6. **Cyclic Dependencies** — Cycles prevent independent evolution and often signal muddled responsibility boundaries.
7. **SQL Injection** — This is a direct security exposure with potentially catastrophic impact.
8. **Shotgun Surgery** — Change risk and omission risk rise sharply.
9. **Hub-like Dependency / God Library** — Change amplification and bottleneck ownership emerge around one unstable center.
10. **Mutable Artifacts** — Release integrity and supply-chain trust are lost.
11. **Synchronous Dependency Chain** — Latency compounds and resilience collapses under partial failure.
12. **Divergent Change** — The module becomes unstable, conflict-prone, and hard to reason about.
13. **Blind Pattern Following / Cargo Cult Architecture** — Accidental complexity increases faster than delivered value.
14. **Monolithic Infrastructure as Code** — A small mistake can affect the whole platform, and ownership boundaries disappear.
15. **Flaky Tests** — CI signal becomes noisy and real defects get ignored.
16. **Swallowed Exceptions / Error Hiding** — It converts explicit failure into silent corruption and destroys diagnosability.
17. **Chatty Services** — Tail latency and failure surface expand rapidly as call volume grows.
18. **N+1 Query** — Latency and database load grow with result size and can dominate request cost.
19. **Layering Violations / Layer Skipping** — Contracts become unstable, concerns bleed together, and replacing infrastructure becomes expensive.
20. **Wrong Bounded Context / Entity Service** — Context boundaries blur and the system drifts toward a distributed monolith.
21. **Refused Bequest** — Substitutability is broken and polymorphism becomes unsafe.
22. **Fragile Tests** — Refactoring becomes expensive and teams stop trusting tests as safety nets.
23. **God Table** — Schema evolution becomes risky, indexes perform poorly, and ownership is unclear.
24. **Long Method / Deep Nesting** — It raises cognitive load, hides invariants, and makes testing and modification high risk.
25. **Anemic Domain Model** — Encapsulation is lost, invariants scatter, and every change becomes shotgun surgery across services.

## Top 25 Most Detectable Anti-Patterns

1. **Duplicated Code** — primary sensors: AST
2. **Long Method / Deep Nesting** — primary sensors: AST
3. **Long Parameter List / Data Clumps** — primary sensors: AST
4. **Dead Code** — primary sensors: AST, runtime telemetry
5. **Repeated Switches / Giant Conditional** — primary sensors: AST
6. **Cyclic Dependencies** — primary sensors: dependency graph, architecture rules
7. **Swallowed Exceptions / Error Hiding** — primary sensors: AST, runtime telemetry
8. **God Object / Blob** — primary sensors: AST, dependency graph
9. **Primitive Obsession** — primary sensors: AST
10. **Hub-like Dependency / God Library** — primary sensors: dependency graph, architecture rules
11. **Hardcoded Environment / Configuration** — primary sensors: AST, architecture rules
12. **Testing Implementation Details** — primary sensors: AST
13. **Feature Envy** — primary sensors: AST
14. **Unstable Dependency** — primary sensors: dependency graph, architecture rules
15. **Shared Database** — primary sensors: architecture rules, runtime telemetry
16. **Chatty Services** — primary sensors: architecture rules, runtime telemetry
17. **N+1 Query** — primary sensors: AST, runtime telemetry
18. **Message Chains** — primary sensors: AST
19. **Mutable Artifacts** — primary sensors: architecture rules
20. **Over-Mocking** — primary sensors: AST
21. **EAV Abuse** — primary sensors: architecture rules
22. **SQL Injection** — primary sensors: AST
23. **God Table** — primary sensors: architecture rules
24. **Polymorphic Associations** — primary sensors: architecture rules
25. **Layering Violations / Layer Skipping** — primary sensors: dependency graph, architecture rules

## Anti-Pattern → Refactoring Mapping

| Anti-Pattern | Primary Refactoring / Recovery Strategy | Supporting Patterns |
|---|---|---|
| Big Ball of Mud | Establish explicit boundaries; refactor toward a modular monolith or hexagonal architecture; enforce rules in CI. | Layered Architecture, Hexagonal Architecture, Strangler Fig |
| Blind Pattern Following / Cargo Cult Architecture | Re-scope to the simplest architecture that satisfies current constraints; remove premature layers; prove the need with measurements. | YAGNI, Modular Monolith |
| Complicated Serverless Setups / Lambda Pinball | Consolidate related behavior; introduce explicit orchestration/state machines; reduce trigger depth. | Workflow Orchestrator, Step Functions, Saga |
| Hardcoded Environment / Configuration | Externalize configuration; use secret stores and environment-specific config injection; adopt 12-factor configuration discipline. | Externalized Configuration, 12-Factor App |
| Hub-like Dependency / God Library | Split the hub by business capability; keep only thin shared contracts/utilities; publish APIs or events instead of shared logic. | Published Language, Shared Kernel (narrow), Facade |
| Layering Violations / Layer Skipping | Restore inward dependency flow; introduce application services and adapters; enforce boundaries automatically. | Clean Architecture, Ports and Adapters |
| Monolithic Infrastructure as Code | Modularize by lifecycle and ownership; isolate state; reference outputs rather than share one root graph. | Modular IaC, Least Privilege |
| Mutable Artifacts | Use immutable versioned artifacts, digests, signatures, and registry policies that reject overwrite. | Semantic Versioning, Provenance/SBOM |
| Unstable Dependency | Invert the dependency through interfaces and adapters; keep stable policy independent from volatile detail. | Stable Dependencies Principle, Adapter |
| Duplicated Code | Extract Method or Extract Class; parameterize the variation; remove clone families systematically. | Template Method, Strategy, Composite |
| Long Method / Deep Nesting | Extract Function; Split Phase; Replace Temp with Query; move domain logic into cohesive collaborators. | Command, Strategy, Template Method |
| Long Parameter List / Data Clumps | Introduce Parameter Object; Preserve Whole Object; create immutable value objects for recurring clusters. | Value Object, Builder |
| Primitive Obsession | Replace Primitive with Object; Replace Type Code with Class/Enum; move validation into value objects. | Value Object, Enum |
| Repeated Switches / Giant Conditional | Replace Conditional with Polymorphism; introduce Strategy, State, or a lookup registry. | Strategy, State, Factory Method |
| Swallowed Exceptions / Error Hiding | Catch narrow exceptions; add context; propagate or map to domain errors; fail fast on invariant breaches. | Result/Either, Circuit Breaker at boundaries |
| EAV Abuse | Model stable attributes explicitly; use dependent tables or JSON columns only where justified and indexed. | Metadata Table, CQRS Read Model |
| God Table | Normalize into cohesive tables per concern; introduce views/read models for combined reads. | Normalization, Database per Service |
| N+1 Query | Use eager loading, joins, batch fetching, or read models; cache where appropriate. | Batch Fetching, Repository, Unit of Work |
| Naive Trees | Choose a tree model that matches query patterns: closure table, path enumeration, or nested sets. | Closure Table, Path Enumeration |
| Overloaded Column / Semantic Overloading | Split the model by concept; create explicit columns or tables; add domain constraints. | Normalization, Value Object |
| Polymorphic Associations | Use proper association tables or a supertype table with real constraints. | Association Table, Table Inheritance |
| SQL Injection | Use prepared statements and parameter binding; isolate query construction behind safe data access APIs. | Prepared Statement, Query Object |
| Spaghetti Query | Break into views, CTEs, staged queries, or materialized/read models with clear responsibilities. | CQRS Read Model, View |
| Concrete Dependency / Service Locator | Introduce interfaces and constructor injection; move wiring to the composition root. | Dependency Injection, Inversion of Control |
| Cyclic Dependencies | Break the cycle with new abstractions, interfaces, responsibility moves, or a lower shared module with narrow scope. | Dependency Inversion, Common Closure Principle |
| Dependency Hell | Reduce dependency surface area; isolate volatile libraries behind adapters; adopt compatibility and upgrade policies. | Adapter, Semantic Versioning |
| Hidden Temporal Coupling | Encode legal states explicitly; use staged builders, state objects, or lifecycle wrappers. | State, Staged Builder |
| Dead Code | Instrument, confirm non-use, then remove; rely on version control for history. | Strangler Fig (for replacements) |
| Divergent Change | Split by reason to change; extract modules/classes around cohesive responsibilities. | Extract Class, Split Phase |
| Shotgun Surgery | Centralize the concern in one abstraction; move logic to its owner; remove duplication and repeated conditionals. | Strategy, Template Method, Extract Class |
| Spaghetti Code | Apply incremental refactoring: extract seams, isolate state, replace conditionals, and establish module boundaries. | Strangler Fig, Modular Monolith |
| API Gateway Mini-Monolith / Smart UI | Move orchestration to application services or dedicated workflow components; keep the gateway focused on aggregation and protocol concerns. | BFF, Application Service |
| Chatty Services | Design coarse-grained APIs; aggregate at the edge; use read models or asynchronous propagation. | Aggregator, BFF, CQRS Read Model |
| Distributed Monolith | Redraw boundaries by bounded context; reduce synchronous coupling; prefer asynchronous integration where justified. | Bounded Context, Event-Driven Integration |
| Nanoservices | Merge services around cohesive business capabilities; prefer a modular monolith when boundaries are not yet stable. | Modular Monolith, Bounded Context |
| Shared Database | Adopt database-per-service; publish events or APIs for integration; introduce replication/read models where needed. | Database per Service, CQRS, Published Language |
| Synchronous Dependency Chain | Break the chain with async messaging, local caches, sagas, or service consolidation; add timeouts and circuit breakers. | Saga, Event-Driven Architecture, Circuit Breaker |
| Wrong Bounded Context / Entity Service | Re-cut services around bounded contexts; allow distinct models per context; define explicit integration contracts. | Bounded Context, Context Map, Anti-Corruption Layer |
| Anemic Domain Model | Move behavior into entities and value objects; define aggregates and narrow domain services. | Rich Domain Model, Aggregate |
| Fat Interface | Split interfaces by role; segregate read/write concerns; define smaller protocols. | Role Interface, Hexagonal Port |
| Feature Envy | Move Method; move behavior to the data owner; reshape aggregates. | Tell-Don't-Ask, Rich Domain Model |
| God Object / Blob | Extract Class; Move Method/Field; split by responsibility and bounded context. | Facade (explicit boundary, not dumping ground), Domain Service, Command |
| Inappropriate Intimacy / Deficient Encapsulation | Encapsulate Field; return immutable views; move logic to the owning type; narrow public APIs. | Mediator, Facade, Immutable Value Object |
| Message Chains | Hide Delegate; move behavior closer to the data; expose intent-level methods. | Law of Demeter, Facade |
| Refused Bequest | Push behavior down; extract a better hierarchy; prefer composition over inheritance. | Composition over Inheritance, Role Object |
| Dedicated DevOps Silo | Move toward platform enablement plus service ownership; keep operational responsibility close to the teams shipping the software. | Platform Team, You Build It You Run It |
| Golden Hammer | Make trade-offs explicit; require alternatives in design reviews; tie architecture choices to measurable constraints. | ADR, Decision Matrix, YAGNI |
| Manual Deployments | Automate the pipeline, configuration, and rollback path; use progressive delivery with observability gates. | Deployment Pipeline, GitOps |
| Toil Accumulation | Automate repetitive ops, reduce noisy alerts, self-serve routine tasks, and budget time for reliability engineering. | SRE Error Budgets, Self-Service Ops |
| Busy Waiting / Race Hazard | Use proper synchronization primitives, condition variables, queues, and ownership discipline; remove timing assumptions. | Producer-Consumer, Actor Model |
| Extraneous Fetching | Use explicit projections, DTOs, pagination, and shape responses to use cases. | DTO, CQRS Read Model |
| Improper Caching | Choose cache strategy per data class; fix key design; add request coalescing, invalidation, and observability. | Cache-Aside, Read-Through |
| Premature Optimization | Simplify first; optimize only after measurement; keep performance decisions traceable to benchmarks. | YAGNI, Simple Design |
| Assertion Roulette | Split tests by concern; use richer assertions and descriptive names; add intent-revealing helpers. | Given-When-Then, Specification by Example |
| Flaky Tests | Control time and randomness; isolate external systems; remove shared mutable state; make tests hermetic. | Hermetic Tests, Test Doubles |
| Fragile Tests | Assert outcomes through public APIs; reduce interaction assertions; test behavior, not construction details. | FIRST tests, classicist unit testing |
| Mystery Guest | Make fixtures explicit and local; use builders/factories; hide shared setup behind readable helpers. | Test Data Builder, Object Mother |
| Over-Mocking | Use real domain objects and fakes where possible; reserve mocks for true architectural boundaries. | Contract Test, Ports and Adapters |
| Shared Fixture / Inter-test Coupling | Provide per-test fixtures, transactional isolation, ephemeral environments, and strict cleanup. | Ephemeral Environment, Test Containers |
| Slow Test Suite | Rebalance the test pyramid; isolate boundaries; keep only critical E2E paths; parallelize where sound. | Test Pyramid, Consumer-Driven Contract |
| Testing Implementation Details | Test public behavior; if private logic is too complex, extract it into a new type with a real contract. | Extract Class, Sociable Unit Tests |

## Anti-Pattern → SOLID Violations

| Anti-Pattern | SOLID Principle(s) | Notes |
|---|---|---|
| Duplicated Code | SRP (indirect), OCP (indirect) | Canonical mapping after normalization. |
| Long Method / Deep Nesting | SRP | Canonical mapping after normalization. |
| Repeated Switches / Giant Conditional | OCP | Canonical mapping after normalization. |
| Long Parameter List / Data Clumps | SRP (indirect) | Canonical mapping after normalization. |
| Primitive Obsession | SRP (indirect), OCP (indirect) | Canonical mapping after normalization. |
| Swallowed Exceptions / Error Hiding | SRP (indirect) | Canonical mapping after normalization. |
| God Object / Blob | SRP, OCP, DIP | Canonical mapping after normalization. |
| Anemic Domain Model | SRP (domain-level), OCP (indirect) | Canonical mapping after normalization. |
| Feature Envy | SRP | Canonical mapping after normalization. |
| Inappropriate Intimacy / Deficient Encapsulation | SRP, DIP (indirect) | Canonical mapping after normalization. |
| Message Chains | DIP (indirect) | Canonical mapping after normalization. |
| Refused Bequest | LSP | Canonical mapping after normalization. |
| Fat Interface | ISP | Canonical mapping after normalization. |
| Big Ball of Mud | SRP (system-level), DIP | Canonical mapping after normalization. |
| Layering Violations / Layer Skipping | DIP, SRP | Canonical mapping after normalization. |
| Hub-like Dependency / God Library | SRP, DIP | Canonical mapping after normalization. |
| Unstable Dependency | DIP | Canonical mapping after normalization. |
| Blind Pattern Following / Cargo Cult Architecture | DIP (misapplied), SRP (often indirect) | Canonical mapping after normalization. |
| Hardcoded Environment / Configuration | DIP (indirect) | Canonical mapping after normalization. |
| Monolithic Infrastructure as Code | SRP (system-level) | Canonical mapping after normalization. |
| Complicated Serverless Setups / Lambda Pinball | SRP (system-level, often indirect) | Canonical mapping after normalization. |
| Distributed Monolith | SRP (system-level), DIP (indirect) | Canonical mapping after normalization. |
| Shared Database | SRP (ownership), DIP (indirect) | Canonical mapping after normalization. |
| Chatty Services | OCP (indirect), DIP (indirect) | Canonical mapping after normalization. |
| Nanoservices | SRP (at wrong level, indirect) | Canonical mapping after normalization. |
| Wrong Bounded Context / Entity Service | SRP | Canonical mapping after normalization. |
| Synchronous Dependency Chain | DIP (indirect) | Canonical mapping after normalization. |
| API Gateway Mini-Monolith / Smart UI | SRP | Canonical mapping after normalization. |
| God Table | SRP (data ownership, indirect) | Canonical mapping after normalization. |
| Cyclic Dependencies | DIP (indirect) | Canonical mapping after normalization. |
| Concrete Dependency / Service Locator | DIP | Canonical mapping after normalization. |
| Shotgun Surgery | SRP | Canonical mapping after normalization. |
| Divergent Change | SRP | Canonical mapping after normalization. |
| Spaghetti Code | SRP (indirect) | Canonical mapping after normalization. |

## Anti-Pattern → Detection Strategy Mapping

| Anti-Pattern | AST detectable | Dependency graph detectable | Architecture detectable | Runtime detectable | Primary signals |
|---|---|---|---|---|---|
| API Gateway Mini-Monolith / Smart UI | Yes | No | Yes | No | LOC and complexity metrics on gateway/UI layers; orchestration logic and domain decisions in controllers/routes. |
| Anemic Domain Model | Yes | No | No | No | Data-heavy classes with little behavior; service classes dominating domain semantics; mutation outside aggregates. |
| Assertion Roulette | Yes | No | No | No | Many assertions per test without labels/helpers; boolean asserts on large objects; missing descriptive names. |
| Big Ball of Mud | No | Yes | Yes | No | Dependency density; cycles across packages; no consistent direction of dependencies; architecture rule violations. |
| Blind Pattern Following / Cargo Cult Architecture | No | No | Yes | No | Architecture-review heuristics: abstraction-to-business-logic ratio, unnecessary brokers/orchestrators, low scale but high distributed overhead. |
| Busy Waiting / Race Hazard | Yes | No | No | Yes | AST patterns for polling loops and sleep-based synchronization; runtime contention and timing anomalies. |
| Chatty Services | No | No | Yes | Yes | Distributed traces with repeated calls between the same pair of services; static remote-call-in-loop detection. |
| Complicated Serverless Setups / Lambda Pinball | No | No | Yes | Yes | Parse cloud resource definitions into a trigger graph; flag deep chains without an explicit orchestrator or state machine. |
| Concrete Dependency / Service Locator | Yes | Yes | No | No | Instantiation of concretes in policy modules; calls to locator/global context types; low constructor visibility of dependencies. |
| Cyclic Dependencies | No | Yes | Yes | No | Graph cycle detection over packages, modules, services, or architecture components. |
| Dead Code | Yes | No | No | Yes | Unused symbol analysis; zero runtime hits; stale feature flags; low coverage plus no call sites. |
| Dedicated DevOps Silo | No | No | Yes | No | Org-chart and ticket-flow analysis; deployment dependency on one team; low service ownership clarity. |
| Dependency Hell | No | Yes | Yes | No | Conflicting version constraints; high transitive depth; frequent lockfile conflicts; large exception allowlists. |
| Distributed Monolith | No | Yes | Yes | Yes | Trace depth, co-deployment/co-release analysis, cross-service change coupling, synchronous call chains. |
| Divergent Change | No | Yes | No | No | High change entropy by topic; disjoint collaborator clusters inside one class/module. |
| Duplicated Code | Yes | No | No | No | Token/AST clone detection; repeated call sequences; high co-change between similar functions. |
| EAV Abuse | No | No | Yes | No | Schema scan for attr/value tables; polymorphic value columns; repeated pivot/self-join reconstruction queries. |
| Extraneous Fetching | Yes | No | No | Yes | Projection analysis; unused response fields; payload-size telemetry; wide select statements. |
| Fat Interface | Yes | No | No | No | Large interface size; low method usage overlap across consumers; stubbed implementations. |
| Feature Envy | Yes | No | No | No | Foreign field/method access dominates local access; Law-of-Demeter violations plus data manipulation. |
| Flaky Tests | Yes | No | No | Yes | Historical intermittency; uncontrolled time/random/network usage; order-dependent suite failures. |
| Fragile Tests | Yes | No | No | Yes | Frequent VCS churn in tests after internal-only changes; reflection/private-state access; interaction-heavy assertions. |
| God Object / Blob | Yes | Yes | No | No | LOC and method count; LCOM/cohesion metrics; high fan-in/fan-out; centrality in change graph. |
| God Table | No | No | Yes | No | DDL metrics for width and sparsity; access logs from many modules/services; overloaded generic column names. |
| Golden Hammer | No | No | Yes | No | Architecture decision records show one repeated solution pattern despite very different problem shapes. |
| Hardcoded Environment / Configuration | Yes | No | Yes | No | Pattern matching for URLs/hosts/credentials; environment-name branching; secret scanning. |
| Hidden Temporal Coupling | Yes | No | No | No | Separate initialize/open/use methods on mutable types; precondition-sensitive call sequences. |
| Hub-like Dependency / God Library | No | Yes | Yes | No | Betweenness/centrality metrics; fan-in/fan-out outliers; many executables depending on one fat shared module. |
| Improper Caching | No | No | Yes | Yes | Repeated expensive calls; mismatched TTLs; missing invalidation events; cache-key analysis; load spikes on misses. |
| Inappropriate Intimacy / Deficient Encapsulation | Yes | Yes | No | No | Public mutable members; dense pairwise call graphs; getters returning mutable internals. |
| Layering Violations / Layer Skipping | No | Yes | Yes | No | Static dependency rules between layers; forbidden import checks; architecture tests. |
| Long Method / Deep Nesting | Yes | No | No | No | LOC, cyclomatic and NPath complexity, nesting depth, branch count, hotspot churn. |
| Long Parameter List / Data Clumps | Yes | No | No | No | Parameter-count thresholds; repeated parameter co-occurrence; many literal-heavy call sites. |
| Manual Deployments | No | No | Yes | No | Absence of automated pipeline evidence; manual approvals outside tooling; drift alerts; repeated runbook use. |
| Message Chains | Yes | No | No | No | Member-access chain length; Law-of-Demeter rules; repeated chained navigation patterns. |
| Monolithic Infrastructure as Code | No | No | Yes | No | Resource-count and blast-radius thresholds; graph analysis of one stack spanning multiple lifecycles/domains. |
| Mutable Artifacts | No | No | Yes | No | Registry policy checks; CI rules for floating tags; immutability flags and signature verification. |
| Mystery Guest | Yes | No | No | No | Data access without local setup; references to shared fixture files or seeded records outside the test. |
| N+1 Query | Yes | No | No | Yes | Static detection of DB/ORM calls inside loops; runtime clustering of repeated statements per trace. |
| Naive Trees | No | No | Yes | No | Adjacency-list plus repeated self-joins; level columns; depth assumptions in code. |
| Nanoservices | No | No | Yes | No | Service size metrics; service-per-transaction count; call graph role analysis. |
| Over-Mocking | Yes | No | No | No | High ratio of mocking API calls to assertions; interaction assertions outnumber state assertions. |
| Overloaded Column / Semantic Overloading | No | No | Yes | No | Column value diversity inconsistent with declared meaning; application-side switches over a column's interpretation. |
| Polymorphic Associations | No | No | Yes | No | Schema pattern matching for *_type + *_id; lack of real foreign keys; conditional association logic. |
| Premature Optimization | No | No | Yes | No | Complex performance code with no associated profiling or performance tests; optimization in low-volume paths. |
| Primitive Obsession | Yes | No | No | No | Recurrent primitive clusters around domain terms; repeated regex/substring logic; magic strings for state. |
| Refused Bequest | Yes | No | No | No | Subclass overrides that no-op or throw for inherited methods; base contract not honored. |
| Repeated Switches / Giant Conditional | Yes | No | No | No | Repeated discriminant expressions; branch count thresholds; co-change across switch sites. |
| SQL Injection | Yes | No | No | No | Taint analysis from input to query string; string concatenation near execute(); missing prepared statements. |
| Shared Database | No | No | Yes | Yes | Connection/config analysis; schema access logs by service identity; multiple services mutating same tables. |
| Shared Fixture / Inter-test Coupling | Yes | No | No | Yes | Shared globals/fixtures, uncleaned filesystem/DB state, order-dependent failures, suite-only breakage. |
| Shotgun Surgery | No | Yes | Yes | No | Co-change mining; duplicated behavior across modules; broad PR blast radius for small features. |
| Slow Test Suite | No | No | No | Yes | Per-test runtime telemetry; high proportion of tests needing DB/network/browser; low fast-test ratio. |
| Spaghetti Code | Yes | No | Yes | No | Complexity hotspot clustering; mixed concerns; heavy goto-like control flow or ad hoc branching. |
| Spaghetti Query | Yes | No | No | No | SQL parse-tree depth; statement length; join count; repeated nested subqueries. |
| Swallowed Exceptions / Error Hiding | Yes | No | No | Yes | Empty catch/except; broad handlers; default sentinel return after exception; missing rethrow or mapping. |
| Synchronous Dependency Chain | No | No | Yes | Yes | Distributed tracing for call depth and fan-out; synchronous HTTP/RPC usage inside request handlers. |
| Testing Implementation Details | Yes | No | No | No | Reflection/private-member access in test code; test-only access modifiers; internal-state assertions. |
| Toil Accumulation | No | No | Yes | Yes | Ticket taxonomy; repeated runbook steps; alert volume unrelated to incidents; automation gap analysis. |
| Unstable Dependency | No | Yes | Yes | No | Instability metrics, fan-in/fan-out, change frequency, Arcan-style architectural smell detection. |
| Wrong Bounded Context / Entity Service | No | No | Yes | No | Entity-centric service names; cross-team dependency concentration on generic services; cross-context field growth. |

## Source index

- **A**: Document A (Gemini) — gemini_anti_pattern_catalog.txt
- **B**: Document B (OpenAI) — openai_anti_pattern_catalog.md
- **C**: Document C (Perplexity) — perplexity_anti_pattern_catalog.md