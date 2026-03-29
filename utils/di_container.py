"""Dependency Injection Container."""

from typing import Any, Callable, Type, TypeVar

T = TypeVar("T")


class DependencyNotFoundError(Exception):
    """Raised when a required dependency cannot be found."""


class CircularDependencyError(Exception):
    """Raised when a circular dependency chain is detected."""


class DIContainer:
    """A lightweight IoC container for managing global state dependencies."""

    def __init__(self) -> None:
        """Initialize empty dependency registries."""
        self._providers: dict[Type[Any], Callable[[], Any]] = {}
        self._instances: dict[Type[Any], Any] = {}
        self._resolution_stack: set[Type[Any]] = set()

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a pre-built singleton instance."""
        self._instances[interface] = instance

    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a factory method that builds the dependency."""
        self._providers[interface] = factory

    def resolve(self, interface: Type[T]) -> T:
        """Resolve an instance of the requested interface."""
        if interface in self._instances:
            return self._instances[interface]

        if interface in self._resolution_stack:
            raise CircularDependencyError(f"Circular dependency detected for {interface.__name__}")

        if interface not in self._providers:
            raise DependencyNotFoundError(f"No provider registered for {interface.__name__}")

        self._resolution_stack.add(interface)

        try:
            factory = self._providers[interface]
            instance = factory()

            # Simple simulation: auto-cache as singleton if desired, but for this DI container we
            # will assume singleton lifecycle by default for state modules
            self._instances[interface] = instance
            return instance
        finally:
            self._resolution_stack.remove(interface)
