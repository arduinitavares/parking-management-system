"""Vehicle models used by Parking Lot Manager."""

from pydantic import BaseModel, ConfigDict


class Vehicle(BaseModel):
    regnum: str
    make: str
    model: str
    color: str

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


class Car(Vehicle):
    def getType(self) -> str:
        return "Car"


class Truck(Vehicle):
    def getType(self) -> str:
        return "Truck"


class Motorcycle(Vehicle):
    def getType(self) -> str:
        return "Motorcycle"


class Bus(Vehicle):
    def getType(self) -> str:
        return "Bus"
