"""Unit test suite for the Dependency Injection Container."""

import sys
import unittest
from pathlib import Path

# Import the lightweight DI framework created to eliminate global variables in ParkingLot
from utils.di_container import CircularDependencyError, DependencyNotFoundError, DIContainer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class DatabaseConnectionStub:
    """A mock dependency to inject."""

    def __init__(self) -> None:
        """Initialize mock connection status."""
        self.connected = True


class ServiceStub:
    """A mock service that requires the DatabaseConnectionStub."""

    def __init__(self, db: DatabaseConnectionStub) -> None:
        """Store the injected database stub."""
        self.db = db


class CircularA:
    """Mock edge case causing a resolution loop."""

    def __init__(self, container: "DIContainer") -> None:
        """Force a resolution of B during A's instantiation."""
        self.b = container.resolve(CircularB)


class CircularB:
    """Mock edge case causing a resolution loop."""

    def __init__(self, container: "DIContainer") -> None:
        """Force a resolution of A during B's instantiation."""
        self.a = container.resolve(CircularA)


class TestDIContainer(unittest.TestCase):
    """Behavior test suite specifically asserting IoC mapping and resolution."""

    def setUp(self) -> None:
        """Create a fresh container context per test."""
        self.container = DIContainer()

    def test_successful_dependency_resolution(self) -> None:
        """Requirement: Test successful dependency resolution."""
        # Setup: Register the pure DB singleton instance manually
        db_instance = DatabaseConnectionStub()
        self.container.register_instance(DatabaseConnectionStub, db_instance)

        # Register the Service factory which itself delegates resolution upward
        def _factory_service() -> ServiceStub:
            resolved_db = self.container.resolve(DatabaseConnectionStub)
            return ServiceStub(resolved_db)

        self.container.register_factory(ServiceStub, _factory_service)

        # Trigger resolution
        resolved_service = self.container.resolve(ServiceStub)

        # Asserts
        self.assertIsInstance(resolved_service, ServiceStub)
        self.assertIs(resolved_service.db, db_instance)
        self.assertTrue(resolved_service.db.connected)

    def test_failure_when_dependency_missing(self) -> None:
        """Requirement: Test failure when dependency missing."""
        # By attempting to resolve an unregistered interface, we expect deterministic error
        with self.assertRaises(DependencyNotFoundError) as context:
            self.container.resolve(DatabaseConnectionStub)

        self.assertIn("No provider registered", str(context.exception))

    def test_circular_dependency_detection(self) -> None:
        """Requirement: Test circular dependency detection."""

        # When Service A needs B, and B needs A, we MUST throw to prevent StackOverflow crashes
        def _factory_a() -> CircularA:
            return CircularA(self.container)

        def _factory_b() -> CircularB:
            return CircularB(self.container)

        self.container.register_factory(CircularA, _factory_a)
        self.container.register_factory(CircularB, _factory_b)

        with self.assertRaises(CircularDependencyError) as context:
            self.container.resolve(CircularA)

        self.assertIn("Circular dependency detected", str(context.exception))


if __name__ == "__main__":
    unittest.main()
