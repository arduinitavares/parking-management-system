# Dependency Injection Framework Design: Global State Migration

This document outlines the architectural design for introducing a Dependency Injection (DI) framework into the EasyParkPlus Parking Management System. The objective is to eliminate hardcoded global variables, specifically mapping UI properties and core service objects into a managed Inversion of Control (IoC) container.

## 1. Global State Dependencies Identified

Currently, `parking_manager.py` defines the following components in the global module scope, causing testability and coupling issues:

- **UI Context (Tkinter Root):** `root = tk.Tk()`
- **UI Output Display:** `tfield = tk.Text(...)`
- **UI State Variables:** 16 distinct `tk.StringVar()` and `tk.IntVar()` objects instantiated globally.
- **Service State:** While `ParkingLot` is instantiated in `main()`, its tight binding to the global `tk.StringVar()` elements within its own class methods acts as a global dependency anti-pattern.

## 2. Provider and Injector Mechanisms

The DI framework operates centrally through the `DIContainer` established in `utils/di_container.py`. 

- **Provider Types:**
  - `register_instance(interface, instance)`: Directly registers an already-constructed object against an abstraction.
  - `register_factory(interface, Callable)`: Maps a deferred construction method requiring run-time resolution.

- **Injector Mechanism:**
  - Classes (like `TkinterDisplayObserver` and `ParkingLot`) will be modified to accept their dependencies (e.g., the output text field or state dependencies) directly via their `__init__` constructor arguments.
  - The bootstrap script (within `main()`) will construct the `DIContainer`, register the raw UI dependencies and logic controllers, and then `resolve()` the completed root application.

## 3. Service Lifecycle Definitions

To match the operational constraints of the application while making it resilient:

### Singleton Lifecycle
Components that represent unique application state or strict hardware bindings must persist as Singletons. Once resolved, the `DIContainer` retains the reference to ensure subsequent resolution attempts receive the identical memory address.
- `tk.Tk` (The main window loop)
- `TkinterDisplayObserver` (Singleton UI output router)
- `ParkingLot` ( The unitary business logic state container)
- All Tkinter `StringVar`/`IntVar` bindings acting as a shared state machine between the view and controller.

### Transient Lifecycle
Components created strictly per operation (such as `Vehicle` or `RegularParkingStrategy` inside the event loops) do not need container persistence and will remain actively instantiated at the invocation boundaries (Transient). The DI Container will primarily focus on substituting the Singleton structural elements.

## Impact
By finalizing this design space, `ParkingLot` will no longer query global `tk.StringVar.get()` directly. It will expect its runtime data to be resolved or explicitly passed, allowing testing environments to inject fully-mocked string structures without initializing standard Tkinter interfaces.
