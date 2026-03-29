"""Vehicle models used by Parking Lot Manager."""

from pydantic import BaseModel, ConfigDict


class Vehicle(BaseModel):
    """Base domain model representing a generic vehicle."""

    regnum: str
    make: str
    model: str
    color: str

    model_config = ConfigDict(extra="forbid")

    def __init__(self, regnum: str, make: str, model: str, color: str) -> None:
        """Initialize a standard vehicle with its core attributes."""
        super().__init__(
            regnum=regnum,
            make=make,
            model=model,
            color=color,
        )

    def get_make(self) -> str:
        """Return the manufacturer make of the vehicle."""
        return self.make

    def get_model(self) -> str:
        """Return the specific model name of the vehicle."""
        return self.model

    def get_color(self) -> str:
        """Return the exterior color of the vehicle."""
        return self.color

    def get_reg_num(self) -> str:
        """Return the unique registration number of the vehicle."""
        return self.regnum


class Car(Vehicle):
    """Domain model representing a standard passenger car."""

    def get_type(self) -> str:
        """Return the specific type string for this vehicle."""
        return "Car"


class Truck(Vehicle):
    """Domain model representing a transport truck."""

    def get_type(self) -> str:
        """Return the specific type string for this vehicle."""
        return "Truck"


class Motorcycle(Vehicle):
    """Domain model representing a motorcycle."""

    def get_type(self) -> str:
        """Return the specific type string for this vehicle."""
        return "Motorcycle"


class Bus(Vehicle):
    """Domain model representing a passenger bus."""

    def get_type(self) -> str:
        """Return the specific type string for this vehicle."""
        return "Bus"
