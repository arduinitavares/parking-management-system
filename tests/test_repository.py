"""Unit tests for the Repository Pattern data access framework."""

import sys
import unittest
from pathlib import Path

from utils.repository import DuplicateRecordError, InMemoryRepository, RecordNotFoundError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if sys.path[0] != str(PROJECT_ROOT):
    sys.path.insert(0, str(PROJECT_ROOT))


class MockVehicleEntity:
    """Mock domain object to isolate repository testing."""

    def __init__(self, regnum: str, make: str, color: str) -> None:
        """Initialize mock properties."""
        self.regnum = regnum
        self.make = make
        self.color = color


class TestRepositoryPattern(unittest.TestCase):
    """Behavioral tests enforcing data access stability."""

    def setUp(self) -> None:
        """Initialize an isolated in-memory repository."""
        self.repo = InMemoryRepository[MockVehicleEntity]()
        self.v1 = MockVehicleEntity("REG1", "Toyota", "Blue")
        self.v2 = MockVehicleEntity("REG2", "Honda", "Red")
        self.v3 = MockVehicleEntity("REG3", "Toyota", "Silver")

    def test_crud_operations(self) -> None:
        """Requirement: Test CRUD operations through repository."""
        # CREATE (Add)
        self.repo.add(self.v1.regnum, self.v1)

        # READ (Get)
        retrieved = self.repo.get("REG1")
        self.assertIs(retrieved, self.v1)

        # UPDATE (Update)
        self.v1.color = "Green"
        self.repo.update("REG1", self.v1)
        self.assertEqual(self.repo.get("REG1").color, "Green")

        # DELETE (Remove)
        self.repo.remove("REG1")
        with self.assertRaises(RecordNotFoundError):
            self.repo.get("REG1")

    def test_query_methods_with_filters(self) -> None:
        """Requirement: Test query methods with filters."""
        self.repo.add(self.v1.regnum, self.v1)
        self.repo.add(self.v2.regnum, self.v2)
        self.repo.add(self.v3.regnum, self.v3)

        # Filter by single attribute (make)
        toyotas = self.repo.find_by(make="Toyota")
        self.assertEqual(len(toyotas), 2)
        self.assertIn(self.v1, toyotas)
        self.assertIn(self.v3, toyotas)

        # Filter by multi attributes (make + color)
        silver_toyotas = self.repo.find_by(make="Toyota", color="Silver")
        self.assertEqual(len(silver_toyotas), 1)
        self.assertIs(silver_toyotas[0], self.v3)

        # Filter yielding empty results
        none = self.repo.find_by(color="Purple")
        self.assertEqual(len(none), 0)

    def test_repository_exception_handling(self) -> None:
        """Requirement: Test repository exception handling."""
        # Missing elements should deterministically throw RecordNotFoundError
        with self.assertRaises(RecordNotFoundError) as ctx_get:
            self.repo.get("GHOST")
        self.assertIn("not found", str(ctx_get.exception))

        with self.assertRaises(RecordNotFoundError):
            self.repo.remove("GHOST")

        with self.assertRaises(RecordNotFoundError):
            self.repo.update("GHOST", self.v1)

        # Attempting to overwrite existing allocations without an explicit update should fail
        self.repo.add("COLLISION", self.v1)
        with self.assertRaises(DuplicateRecordError) as ctx_dup:
            self.repo.add("COLLISION", self.v2)
        self.assertIn("already exists", str(ctx_dup.exception))


if __name__ == "__main__":
    unittest.main()
