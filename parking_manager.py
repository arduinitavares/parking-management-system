"""EasyParkPlus Parking Management System.

This module implements the core parking allocation and state management functionality.
It has been architecturally refactored to employ the Strategy Pattern (isolating
allocation constraints) and the Observer Pattern (decoupling the UI from core logic).
"""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import TypeAlias

import ElectricVehicle
import Vehicle
from utils.di_container import DIContainer
from utils.repository import InMemoryRepository, RecordNotFoundError

RegularSlot: TypeAlias = Vehicle.Vehicle | int
ElectricSlot: TypeAlias = ElectricVehicle.ElectricVehicle | int


class VehicleRepository(InMemoryRepository[Vehicle.Vehicle]):
    """Entity-specific repository mapping for regular active allocations."""


class EVRepository(InMemoryRepository[ElectricVehicle.ElectricVehicle]):
    """Entity-specific repository mapping for electric active allocations."""


class UIState:
    """Manages all Tkinter variable states, replacing global allocations."""

    def __init__(self) -> None:
        """Initialize all bounded GUI variables as managed state properties."""
        self.command_value = tk.StringVar()
        self.num_value = tk.StringVar()
        self.ev_value = tk.StringVar()
        self.make_value = tk.StringVar()
        self.model_value = tk.StringVar()
        self.color_value = tk.StringVar()
        self.reg_value = tk.StringVar()
        self.level_value = tk.StringVar()
        self.ev_car_value = tk.IntVar()
        self.ev_car2_value = tk.IntVar()
        self.slot1_value = tk.StringVar()
        self.slot2_value = tk.StringVar()
        self.reg1_value = tk.StringVar()
        self.slot_value = tk.StringVar()
        self.ev_motor_value = tk.IntVar()
        self.level_remove_value = tk.StringVar()


# Strategy Pattern Definitions
class ParkingStrategy(ABC):
    """Interface for parking slot allocation strategies."""

    @abstractmethod
    def allocate_slot(
        self,
        lot: "ParkingLot",
        regnum: str,
        make: str,
        model: str,
        color: str,
        motor: int,
    ) -> int:
        """Allocate a slot and return a slot number or -1 when full."""
        raise NotImplementedError


class RegularParkingStrategy(ParkingStrategy):
    """Allocates slots for non-electric vehicles."""

    def allocate_slot(
        self,
        lot: "ParkingLot",
        regnum: str,
        make: str,
        model: str,
        color: str,
        motor: int,
    ) -> int:
        """Allocate a regular slot for a car or motorcycle."""
        if lot.num_of_occupied_slots >= lot.capacity:
            return -1

        slotid = lot.get_empty_slot()
        if slotid is None:
            return -1

        if motor == 1:
            vehicle = Vehicle.Motorcycle(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )
        else:
            vehicle = Vehicle.Car(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )

        lot.vehicle_repo.add(str(slotid), vehicle)
        lot.slotid += 1
        return lot.slotid


class ElectricParkingStrategy(ParkingStrategy):
    """Allocates slots for electric vehicles."""

    def allocate_slot(
        self,
        lot: "ParkingLot",
        regnum: str,
        make: str,
        model: str,
        color: str,
        motor: int,
    ) -> int:
        """Allocate an EV slot for an electric car or bike."""
        if lot.num_of_occupied_ev_slots >= lot.ev_capacity:
            return -1

        slotid = lot.get_empty_ev_slot()
        if slotid is None:
            return -1

        if motor == 1:
            ev_vehicle = ElectricVehicle.ElectricBike(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )
        else:
            ev_vehicle = ElectricVehicle.ElectricCar(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )

        lot.ev_repo.add(str(slotid), ev_vehicle)
        lot.slot_ev_id += 1
        return lot.slot_ev_id


class ParkingObserver(ABC):
    """Interface for observing ParkingLot events."""

    @abstractmethod
    def update(self, event_type: str, message: str) -> None:
        """Update the observer with an event type and message."""
        raise NotImplementedError


class TkinterDisplayObserver(ParkingObserver):
    """Concrete observer that renders updates to the Tkinter text field."""

    def __init__(self, tfield: tk.Text) -> None:
        """Inject the target Tkinter text instance."""
        self.tfield = tfield

    def update(self, event_type: str, message: str) -> None:
        """Render the message to the injected Tkinter text field."""
        self.tfield.insert(tk.INSERT, message)


# Parking Lot class
class ParkingLot:
    """Domain model that manages regular and EV parking slots."""

    def __init__(
        self, ui_state: UIState, vehicle_repo: VehicleRepository, ev_repo: EVRepository
    ) -> None:
        """Initialize the parking lot and inject dependencies."""
        self.ui_state = ui_state
        self.vehicle_repo = vehicle_repo
        self.ev_repo = ev_repo
        self.capacity: int = 0
        self.ev_capacity: int = 0
        self.level: int = 0
        self.slotid: int = 0
        self.slot_ev_id: int = 0
        self._observers: list[ParkingObserver] = []

    @property
    def num_of_occupied_slots(self) -> int:
        """Count active regular allocations dynamically."""
        return len(self.vehicle_repo._store)

    @property
    def num_of_occupied_ev_slots(self) -> int:
        """Count active EV allocations dynamically."""
        return len(self.ev_repo._store)

    def attach(self, observer: ParkingObserver) -> None:
        """Attach an observer to receive parking lot updates."""
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, event_type: str, message: str) -> None:
        """Notify all observers of an event."""
        for observer in self._observers:
            observer.update(event_type, message)

    def create_parking_lot(
        self,
        capacity: int,
        evcapacity: int,
        level: int,
    ) -> int:
        """Initialize regular and EV constraints for the configured level."""
        self.vehicle_repo._store.clear()
        self.ev_repo._store.clear()
        self.level = level
        self.capacity = capacity
        self.ev_capacity = evcapacity
        return self.level

    def get_empty_slot(self) -> int | None:
        """Return the first available regular slot index."""
        # 1-based indexing lookup
        for i in range(1, self.capacity + 1):
            if str(i) not in self.vehicle_repo._store:
                return i
        return None

    def get_empty_ev_slot(self) -> int | None:
        """Return the first available EV slot index."""
        for i in range(1, self.ev_capacity + 1):
            if str(i) not in self.ev_repo._store:
                return i
        return None

    def get_empty_level(self) -> int | None:
        """Return the level when both regular and EV areas are empty."""
        if self.num_of_occupied_ev_slots == 0 and self.num_of_occupied_slots == 0:
            return self.level
        return None

    def park(
        self,
        regnum: str,
        make: str,
        model: str,
        color: str,
        ev: int,
        motor: int,
    ) -> int:
        """Route parking to EV or regular strategy and return slot number."""
        strategy: ParkingStrategy
        if ev == 1:
            strategy = ElectricParkingStrategy()
        else:
            strategy = RegularParkingStrategy()

        return strategy.allocate_slot(self, regnum, make, model, color, motor)

    def leave(self, slotid: int, ev: int) -> bool:
        """Free a slot by one-based slot id for EV or regular parking using Repo boundaries."""
        try:
            if ev == 1:
                if slotid <= 0 or slotid > self.ev_capacity:
                    return False
                self.ev_repo.remove(str(slotid))
                return True

            if slotid <= 0 or slotid > self.capacity:
                return False
            self.vehicle_repo.remove(str(slotid))
            return True
        except RecordNotFoundError:
            return False

    def status(self) -> None:
        """Print regular and EV occupancy details to the output text field."""
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        self.notify("display_update", output)
        items = sorted(self.vehicle_repo._store.items(), key=lambda x: int(x[0]))
        for slotid_str, vehicle in items:
            output = (
                slotid_str
                + "\t"
                + str(self.level)
                + "\t"
                + str(vehicle.regnum)
                + "\t\t"
                + str(vehicle.color)
                + "\t\t"
                + str(vehicle.make)
                + "\t\t"
                + str(vehicle.model)
                + "\n"
            )
            self.notify("display_update", output)

        output = "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        self.notify("display_update", output)
        items = sorted(self.ev_repo._store.items(), key=lambda x: int(x[0]))
        for slotid_str, vehicle in items:
            output = (
                slotid_str
                + "\t"
                + str(self.level)
                + "\t"
                + str(vehicle.regnum)
                + "\t\t"
                + str(vehicle.color)
                + "\t\t"
                + str(vehicle.make)
                + "\t\t"
                + str(vehicle.model)
                + "\n"
            )
            self.notify("display_update", output)

    def charge_status(self) -> None:
        """Print EV charge percentages to the output text field."""
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        self.notify("display_update", output)

        for slotid_str, vehicle in sorted(self.ev_repo._store.items(), key=lambda x: int(x[0])):
            output = (
                slotid_str
                + "\t"
                + str(self.level)
                + "\t"
                + str(vehicle.regnum)
                + "\t\t"
                + str(vehicle.charge)
                + "\n"
            )
            self.notify("display_update", output)

    def get_reg_nums_from_color(self, color: str) -> list[str]:
        """Return registration numbers of all vehicles (regular and EV) matching the color.

        Example:
            >>> lot.get_reg_nums_from_color("Red")
            ['REG123', 'EV456']
        """
        regnums: list[str] = []
        regular = self.vehicle_repo.find_by(color=color)
        evs = self.ev_repo.find_by(color=color)
        for v in regular + evs:
            regnums.append(v.regnum)
        return regnums

    def get_slot_num_from_reg_num(self, regnum: str) -> int | None:
        """Return the one-based integer slot number for a registration (regular or EV).

        Returns None if the vehicle is not found in either lot.

        Example:
            >>> lot.get_slot_num_from_reg_num("REG123")
            1
            >>> lot.get_slot_num_from_reg_num("MISSING")
            None
        """
        for slotid_str, vehicle in self.vehicle_repo._store.items():
            if str(vehicle.regnum) == str(regnum):
                return int(slotid_str)
        for slotid_str, ev_vehicle in self.ev_repo._store.items():
            if str(ev_vehicle.regnum) == str(regnum):
                return int(slotid_str)
        return None

    def get_slot_nums_from_color(self, color: str) -> dict[str, list[int]]:
        """Return one-based slot numbers filtered by color across both lots.

        Standardizes the output type to integers instead of string representations.

        Example:
            >>> lot.get_slot_nums_from_color("Blue")
            {'regular': [1, 3], 'ev': [2]}
        """
        results: dict[str, list[int]] = {"regular": [], "ev": []}

        for slotid_str, vehicle in self.vehicle_repo._store.items():
            if vehicle.color == color:
                results["regular"].append(int(slotid_str))

        for slotid_str, ev_vehicle in self.ev_repo._store.items():
            if ev_vehicle.color == color:
                results["ev"].append(int(slotid_str))

        # Sort sequentially explicitly protecting return typing contracts
        results["regular"].sort()
        results["ev"].sort()
        return results

    def slot_num_by_reg(self) -> None:
        """Display the slot number identified by registration value."""
        slot_val = self.ui_state.slot1_value.get()
        slotnum = self.get_slot_num_from_reg_num(slot_val)

        output = ""
        if slotnum is not None:
            output = "Identified slot: " + str(slotnum) + "\n"
        else:
            output = "Not found\n"

        self.notify("display_update", output)

    def slot_num_by_color(self) -> None:
        """Display regular and EV slot numbers filtered by color value."""
        slot_data = self.get_slot_nums_from_color(self.ui_state.slot2_value.get())

        regular_strs = [str(x) for x in slot_data["regular"]]
        ev_strs = [str(x) for x in slot_data["ev"]]

        output = "Identified slots: " + ", ".join(regular_strs) + "\n"
        self.notify("display_update", output)
        output = "Identified slots (EV): " + ", ".join(ev_strs) + "\n"
        self.notify("display_update", output)

    def reg_num_by_color(self) -> None:
        """Display regular and EV registrations filtered by color value."""
        regnums = self.get_reg_nums_from_color(self.ui_state.reg1_value.get())
        output = "Registation Numbers: " + ", ".join(regnums) + "\n"
        self.notify("display_update", output)

    def make_lot(self) -> None:
        """Create a parking lot from UI field values and display confirmation."""
        try:
            self.create_parking_lot(
                int(self.ui_state.num_value.get()),
                int(self.ui_state.ev_value.get()),
                int(self.ui_state.level_value.get()),
            )
        except ValueError:
            self.notify(
                "display_update", "Error: Please enter valid numbers to construct the lot.\n"
            )
            return

        output = (
            "Created a parking lot with "
            + self.ui_state.num_value.get()
            + " regular slots and "
            + self.ui_state.ev_value.get()
            + " ev slots on level: "
            + self.ui_state.level_value.get()
            + "\n"
        )
        self.notify("display_update", output)

    def park_car(self) -> None:
        """Park a vehicle from UI field values and display the result."""
        res = self.park(
            self.ui_state.reg_value.get(),
            self.ui_state.make_value.get(),
            self.ui_state.model_value.get(),
            self.ui_state.color_value.get(),
            self.ui_state.ev_car_value.get(),
            self.ui_state.ev_motor_value.get(),
        )
        if res == -1:
            self.notify("display_update", "Sorry, parking lot is full\n")
        else:
            output = "Allocated slot number: " + str(res) + "\n"
            self.notify("display_update", output)

    def remove_car(self) -> None:
        """Remove a vehicle by slot id from UI field values."""
        try:
            status = self.leave(
                int(self.ui_state.slot_value.get()), int(self.ui_state.ev_car2_value.get())
            )
        except ValueError:
            self.notify("display_update", "Error: Please enter a valid numerical slot ID.\n")
            return

        if status:
            output = "Slot number " + str(self.ui_state.slot_value.get()) + " is free\n"
            self.notify("display_update", output)
        else:
            self.notify(
                "display_update",
                "Unable to remove a car from slot: " + str(self.ui_state.slot_value.get()) + "\n",
            )


def main() -> None:  # noqa: PLR0915
    """Build and launch the Tkinter Parking Lot Manager interface via DI container."""
    # Scaffold DI Container and UI Context
    container = DIContainer()
    root = tk.Tk()
    root.geometry("650x850")
    root.resizable(False, False)
    root.title("Parking Lot Manager")

    tfield = tk.Text(root, width=70, height=15)

    # Register core singletons into the dependency injection framework
    container.register_instance(tk.Tk, root)
    container.register_instance(tk.Text, tfield)

    ui_state = UIState()
    container.register_instance(UIState, ui_state)

    display_observer = TkinterDisplayObserver(container.resolve(tk.Text))

    parkinglot = ParkingLot(container.resolve(UIState))
    parkinglot.attach(display_observer)

    # Store parking lot loosely so commands execute correctly
    container.register_instance(ParkingLot, parkinglot)

    # input boxes and GUI
    label_head = tk.Label(root, text="Parking Lot Manager", font="Arial 14 bold")
    label_head.grid(row=0, column=0, padx=10, columnspan=4)

    label_head = tk.Label(root, text="Lot Creation", font="Arial 12 bold")
    label_head.grid(row=1, column=0, padx=10, columnspan=4)

    lbl_num = tk.Label(root, text="Number of Regular Spaces", font="Arial 12")
    lbl_num.grid(row=2, column=0, padx=5)

    num_entry = tk.Entry(root, textvariable=ui_state.num_value, width=6, font="Arial 12")
    num_entry.grid(row=2, column=1, padx=4, pady=2)

    lbl_ev = tk.Label(root, text="Number of EV Spaces", font="Arial 12")
    lbl_ev.grid(row=2, column=2, padx=5)

    num_entry = tk.Entry(root, textvariable=ui_state.ev_value, width=6, font="Arial 12")
    num_entry.grid(row=2, column=3, padx=4, pady=4)

    lbl_level = tk.Label(root, text="Floor Level", font="Arial 12")
    lbl_level.grid(row=3, column=0, padx=5)

    level_entry = tk.Entry(root, textvariable=ui_state.level_value, width=6, font="Arial 12")
    level_entry.grid(row=3, column=1, padx=4, pady=4)
    level_entry.insert(tk.INSERT, "1")

    park_make_btn = tk.Button(
        root,
        command=parkinglot.make_lot,
        text="Create Parking Lot",
        font="Arial 12",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    park_make_btn.grid(row=4, column=0, padx=4, pady=4)

    label_car = tk.Label(root, text="Car Management", font="Arial 12 bold")
    label_car.grid(row=5, column=0, padx=10, columnspan=4)

    lbl_make = tk.Label(root, text="Make", font="Arial 12")
    lbl_make.grid(row=6, column=0, padx=5)

    make_entry = tk.Entry(root, textvariable=ui_state.make_value, width=12, font="Arial 12")
    make_entry.grid(row=6, column=1, padx=4, pady=4)

    lbl_model = tk.Label(root, text="Model", font="Arial 12")
    lbl_model.grid(row=6, column=2, padx=5)

    model_entry = tk.Entry(root, textvariable=ui_state.model_value, width=12, font="Arial 12")
    model_entry.grid(row=6, column=3, padx=4, pady=4)

    lbl_color = tk.Label(root, text="Color", font="Arial 12")
    lbl_color.grid(row=7, column=0, padx=5)

    color_entry = tk.Entry(root, textvariable=ui_state.color_value, width=12, font="Arial 12")
    color_entry.grid(row=7, column=1, padx=4, pady=4)

    lbl_reg = tk.Label(root, text="Registration #", font="Arial 12")
    lbl_reg.grid(row=7, column=2, padx=5)

    reg_entry = tk.Entry(root, textvariable=ui_state.reg_value, width=12, font="Arial 12")
    reg_entry.grid(row=7, column=3, padx=4, pady=4)

    ev_toggle = tk.Checkbutton(
        root,
        text="Electric",
        variable=ui_state.ev_car_value,
        onvalue=1,
        offvalue=0,
        font="Arial 12",
    )
    ev_toggle.grid(column=0, row=8, padx=4, pady=4)

    motor_toggle = tk.Checkbutton(
        root,
        text="Motorcycle",
        variable=ui_state.ev_motor_value,
        onvalue=1,
        offvalue=0,
        font="Arial 12",
    )
    motor_toggle.grid(column=1, row=8, padx=4, pady=4)

    park_btn = tk.Button(
        root,
        command=parkinglot.park_car,
        text="Park Car",
        font="Arial 11",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    park_btn.grid(column=0, row=9, padx=4, pady=4)

    lbl_slot = tk.Label(root, text="Slot #", font="Arial 12")
    lbl_slot.grid(row=10, column=0, padx=5)

    slot_entry = tk.Entry(root, textvariable=ui_state.slot_value, width=12, font="Arial 12")
    slot_entry.grid(row=10, column=1, padx=4, pady=4)

    ev_toggle2 = tk.Checkbutton(
        root,
        text="Remove EV?",
        variable=ui_state.ev_car2_value,
        onvalue=1,
        offvalue=0,
        font="Arial 12",
    )
    ev_toggle2.grid(column=2, row=10, padx=4, pady=4)

    remove_btn = tk.Button(
        root,
        command=parkinglot.remove_car,
        text="Remove Car",
        font="Arial 11",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    remove_btn.grid(column=0, row=11, padx=4, pady=4)

    spacer1 = tk.Label(root, text="")
    spacer1.grid(row=12, column=0)

    slot_reg_btn = tk.Button(
        root,
        command=parkinglot.slot_num_by_reg,
        text="Get Slot ID by Registration #",
        font="Arial 11",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    slot_reg_btn.grid(column=0, row=13, padx=4, pady=4)

    slot1_entry = tk.Entry(root, textvariable=ui_state.slot1_value, width=12, font="Arial 12")
    slot1_entry.grid(row=13, column=1, padx=4, pady=4)

    slot_color_btn = tk.Button(
        root,
        command=parkinglot.slot_num_by_color,
        text="Get Slot ID by Color",
        font="Arial 11",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    slot_color_btn.grid(column=2, row=13, padx=4, pady=4)

    slot2_entry = tk.Entry(root, textvariable=ui_state.slot2_value, width=12, font="Arial 12")
    slot2_entry.grid(row=13, column=3, padx=4, pady=4)

    reg_color_btn = tk.Button(
        root,
        command=parkinglot.reg_num_by_color,
        text="Get Registration # by Color",
        font="Arial 11",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    reg_color_btn.grid(column=0, row=14, padx=4, pady=4)

    reg1_entry = tk.Entry(root, textvariable=ui_state.reg1_value, width=12, font="Arial 12")
    reg1_entry.grid(row=14, column=1, padx=4, pady=4)

    charge_status_btn = tk.Button(
        root,
        command=parkinglot.charge_status,
        text="EV Charge Status",
        font="Arial 11",
        bg="lightblue",
        fg="black",
        activebackground="teal",
        padx=5,
        pady=5,
    )
    charge_status_btn.grid(column=2, row=14, padx=4, pady=4)

    status_btn = tk.Button(
        root,
        command=parkinglot.status,
        text="Current Lot Status",
        font="Arial 11",
        bg="PaleGreen1",
        fg="black",
        activebackground="PaleGreen3",
        padx=5,
        pady=5,
    )
    status_btn.grid(column=0, row=15, padx=4, pady=4)

    tfield.grid(column=0, row=16, padx=10, pady=10, columnspan=4)

    root.mainloop()


if __name__ == "__main__":
    main()
