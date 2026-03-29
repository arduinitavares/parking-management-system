"""Electric vehicle models used by Parking Lot Manager."""

from pydantic import BaseModel, ConfigDict


class ElectricVehicle(BaseModel):
    """Represents an electric vehicle."""

    regnum: str
    make: str
    model: str
    color: str
    charge: int = 0

    model_config = ConfigDict(extra="forbid")

    def __init__(self, regnum: str, make: str, model: str, color: str) -> None:
        """Initialize an ElectricVehicle."""
        super().__init__(
            regnum=regnum,
            make=make,
            model=model,
            color=color,
        )

    def get_make(self) -> str:
        """Get the make of the electric vehicle."""
        return self.make

    def get_model(self) -> str:
        """Get the model of the electric vehicle."""
        return self.model

    def get_color(self) -> str:
        """Get the color of the electric vehicle."""
        return self.color

    def get_reg_num(self) -> str:
        """Get the registration number of the electric vehicle."""
        return self.regnum

    def set_charge(self, charge: int) -> None:
        """Set the charge of the electric vehicle."""
        self.charge = charge

    def get_charge(self) -> int:
        """Get the charge of the electric vehicle."""
        return self.charge


class ElectricCar(ElectricVehicle):
    """Represents an electric car."""

    def get_type(self) -> str:
        """Get the type of the electric vehicle."""
        return "Car"


class ElectricBike(ElectricVehicle):
    """Represents an electric motorcycle."""

    def get_type(self) -> str:
        """Get the type of the electric vehicle."""
        return "Motorcycle"
