"""Electric vehicle models used by Parking Lot Manager."""

from pydantic import BaseModel, ConfigDict


class ElectricVehicle(BaseModel):
    regnum: str
    make: str
    model: str
    color: str
    charge: int = 0

    model_config = ConfigDict(extra="forbid")

    def __init__(self, regnum: str, make: str, model: str, color: str) -> None:
        super().__init__(
            regnum=regnum,
            make=make,
            model=model,
            color=color,
        )

    def getMake(self) -> str:
        return self.make

    def getModel(self) -> str:
        return self.model

    def getColor(self) -> str:
        return self.color

    def getRegNum(self) -> str:
        return self.regnum

    def setCharge(self, charge: int) -> None:
        self.charge = charge

    def getCharge(self) -> int:
        return self.charge


class ElectricCar(ElectricVehicle):
    def getType(self) -> str:
        return "Car"


class ElectricBike(ElectricVehicle):
    def getType(self) -> str:
        return "Motorcycle"
