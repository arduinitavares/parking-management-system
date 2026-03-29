"""Generic Repository Pattern definition and in-memory implementation."""

from typing import Any, Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class RecordNotFoundError(Exception):
    """Raised when an attempt to look up a record by its identifier fails."""


class DuplicateRecordError(Exception):
    """Raised when an attempt to insert a record with an existing identifier occurs."""


class Repository(Generic[T, ID]):
    """Abstract generic repository interface."""

    def add(self, record_id: ID, entity: T) -> None:
        """Add a new entity to the repository under the given ID."""
        raise NotImplementedError

    def get(self, record_id: ID) -> T:
        """Fetch an entity by its ID, raising an error if absent."""
        raise NotImplementedError

    def update(self, record_id: ID, entity: T) -> None:
        """Update an existing entity by its ID."""
        raise NotImplementedError

    def remove(self, record_id: ID) -> None:
        """Remove an entity by its ID."""
        raise NotImplementedError

    def find_by(self, **kwargs: Any) -> list[T]:
        """Return entities that match exactly on the given attribute keyword parameters."""
        raise NotImplementedError


class InMemoryRepository(Repository[T, str]):
    """Concrete repository mapping string IDs to entities in memory."""

    def __init__(self) -> None:
        """Initialize empty storage dictionary."""
        self._store: dict[str, T] = {}

    def add(self, record_id: str, entity: T) -> None:
        """Add a new entity, enforcing uniqueness."""
        if record_id in self._store:
            raise DuplicateRecordError(f"Record with ID '{record_id}' already exists.")
        self._store[record_id] = entity

    def get(self, record_id: str) -> T:
        """Retrieve an entity or raise if invalid."""
        if record_id not in self._store:
            raise RecordNotFoundError(f"Record '{record_id}' not found.")
        return self._store[record_id]

    def update(self, record_id: str, entity: T) -> None:
        """Overwrite an existing entity."""
        if record_id not in self._store:
            raise RecordNotFoundError(f"Cannot update missing record '{record_id}'.")
        self._store[record_id] = entity

    def remove(self, record_id: str) -> None:
        """Delete an entity from the store."""
        if record_id not in self._store:
            raise RecordNotFoundError(f"Cannot delete missing record '{record_id}'.")
        del self._store[record_id]

    def find_by(self, **kwargs: Any) -> list[T]:
        """Simple property matching filter."""
        results: list[T] = []
        for item in self._store.values():
            match = True
            for k, expected_v in kwargs.items():
                if not hasattr(item, k) or getattr(item, k) != expected_v:
                    match = False
                    break
            if match:
                results.append(item)
        return results
