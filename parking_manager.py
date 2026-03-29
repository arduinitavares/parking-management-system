"""Parking Lot Manager Application."""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import TypeAlias

import ElectricVehicle
import Vehicle

RegularSlot: TypeAlias = Vehicle.Vehicle | int
ElectricSlot: TypeAlias = ElectricVehicle.ElectricVehicle | int

root = tk.Tk()
root.geometry("650x850")
root.resizable(False, False)
root.title("Parking Lot Manager")

# input values
command_value = tk.StringVar()
num_value = tk.StringVar()
ev_value = tk.StringVar()
make_value = tk.StringVar()
model_value = tk.StringVar()
color_value = tk.StringVar()
reg_value = tk.StringVar()
level_value = tk.StringVar()
ev_car_value = tk.IntVar()
ev_car2_value = tk.IntVar()
slot1_value = tk.StringVar()
slot2_value = tk.StringVar()
reg1_value = tk.StringVar()
slot_value = tk.StringVar()
ev_motor_value = tk.IntVar()
level_remove_value = tk.StringVar()

tfield = tk.Text(root, width=70, height=15)


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
            lot.slots[slotid] = Vehicle.Motorcycle(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )
        else:
            lot.slots[slotid] = Vehicle.Car(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )

        lot.num_of_occupied_slots += 1
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
            lot.ev_slots[slotid] = ElectricVehicle.ElectricBike(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )
        else:
            lot.ev_slots[slotid] = ElectricVehicle.ElectricCar(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )

        lot.num_of_occupied_ev_slots += 1
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

    def update(self, event_type: str, message: str) -> None:
        """Render the message to the global Tkinter text field."""
        tfield.insert(tk.INSERT, message)


# Parking Lot class
class ParkingLot:
    """Domain model that manages regular and EV parking slots."""

    def __init__(self) -> None:
        """Initialize the parking lot."""
        self.capacity: int = 0
        self.ev_capacity: int = 0
        self.level: int = 0
        self.slotid: int = 0
        self.slot_ev_id: int = 0
        self.num_of_occupied_slots: int = 0
        self.num_of_occupied_ev_slots: int = 0
        self.slots: list[RegularSlot] = []
        self.ev_slots: list[ElectricSlot] = []
        self._observers: list[ParkingObserver] = []

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
        """Initialize regular and EV slots for the configured level."""
        self.slots = [-1] * capacity
        self.ev_slots = [-1] * evcapacity
        self.level = level
        self.capacity = capacity
        self.ev_capacity = evcapacity
        return self.level

    def get_empty_slot(self) -> int | None:
        """Return the first available regular slot index."""
        for i, slot in enumerate(self.slots):
            if slot == -1:
                return i
        return None

    def get_empty_ev_slot(self) -> int | None:
        """Return the first available EV slot index."""
        for i, slot in enumerate(self.ev_slots):
            if slot == -1:
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
        """Free a slot by one-based slot id for EV or regular parking."""
        index = slotid - 1
        if ev == 1:
            if (
                index >= 0
                and index < len(self.ev_slots)
                and self.num_of_occupied_ev_slots > 0
                and self.ev_slots[index] != -1
            ):
                self.ev_slots[index] = -1
                self.num_of_occupied_ev_slots = self.num_of_occupied_ev_slots - 1
                return True
            return False

        if (
            index >= 0
            and index < len(self.slots)
            and self.num_of_occupied_slots > 0
            and self.slots[index] != -1
        ):
            self.slots[index] = -1
            self.num_of_occupied_slots = self.num_of_occupied_slots - 1
            return True
        return False

    def edit(
        self,
        slotid: int,
        regnum: str,
        make: str,
        model: str,
        color: str,
        ev: int,
    ) -> bool:
        """Replace a slot occupant with updated vehicle information."""
        if ev == 1:
            self.ev_slots[slotid] = ElectricVehicle.ElectricCar(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
            )
            return True

        self.slots[slotid] = Vehicle.Car(
            regnum=regnum,
            make=make,
            model=model,
            color=color,
        )
        return True

    def status(self) -> None:
        """Print regular and EV occupancy details to the output text field."""
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        self.notify("display_update", output)
        for i, slot in enumerate(self.slots):
            if not isinstance(slot, Vehicle.Vehicle):
                continue
            output = (
                str(i + 1)
                + "\t"
                + str(self.level)
                + "\t"
                + str(slot.regnum)
                + "\t\t"
                + str(slot.color)
                + "\t\t"
                + str(slot.make)
                + "\t\t"
                + str(slot.model)
                + "\n"
            )
            self.notify("display_update", output)

        output = "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        self.notify("display_update", output)
        for i, slot in enumerate(self.ev_slots):
            if not isinstance(slot, ElectricVehicle.ElectricVehicle):
                continue
            output = (
                str(i + 1)
                + "\t"
                + str(self.level)
                + "\t"
                + str(slot.regnum)
                + "\t\t"
                + str(slot.color)
                + "\t\t"
                + str(slot.make)
                + "\t\t"
                + str(slot.model)
                + "\n"
            )
            self.notify("display_update", output)

    def charge_status(self) -> None:
        """Print EV charge percentages to the output text field."""
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        self.notify("display_update", output)

        for i, slot in enumerate(self.ev_slots):
            if not isinstance(slot, ElectricVehicle.ElectricVehicle):
                continue
            output = (
                str(i + 1)
                + "\t"
                + str(self.level)
                + "\t"
                + str(slot.regnum)
                + "\t\t"
                + str(slot.charge)
                + "\n"
            )
            self.notify("display_update", output)

    def get_reg_num_from_color(self, color: str) -> list[str]:
        """Return registration numbers of regular vehicles with matching color."""
        regnums: list[str] = []
        for slot in self.slots:
            if not isinstance(slot, Vehicle.Vehicle):
                continue
            if slot.color == color:
                regnums.append(slot.regnum)
        return regnums

    def get_slot_num_from_reg_num(self, regnum: str) -> int:
        """Return one-based regular slot number for a registration."""
        for i, slot in enumerate(self.slots):
            if isinstance(slot, Vehicle.Vehicle) and slot.regnum == regnum:
                return i + 1
        return -1

    def get_slot_num_from_color(self, color: str) -> list[str]:
        """Return one-based regular slot numbers filtered by color."""
        slotnums: list[str] = []

        for i, slot in enumerate(self.slots):
            if isinstance(slot, Vehicle.Vehicle) and slot.color == color:
                slotnums.append(str(i + 1))
        return slotnums

    def get_slot_num_from_make(self, make: str) -> list[str]:
        """Return one-based regular slot numbers filtered by make."""
        slotnums: list[str] = []

        for i, slot in enumerate(self.slots):
            if isinstance(slot, Vehicle.Vehicle) and slot.make == make:
                slotnums.append(str(i + 1))
        return slotnums

    def get_slot_num_from_model(self, model: str) -> list[str]:
        """Return one-based regular slot numbers filtered by model."""
        slotnums: list[str] = []

        for i, slot in enumerate(self.slots):
            if isinstance(slot, Vehicle.Vehicle) and slot.model == model:
                slotnums.append(str(i + 1))
        return slotnums

    def get_reg_num_from_color_ev(self, color: str) -> list[str]:
        """Return registration numbers of EVs with matching color."""
        regnums: list[str] = []
        for slot in self.ev_slots:
            if not isinstance(slot, ElectricVehicle.ElectricVehicle):
                continue
            if slot.color == color:
                regnums.append(slot.regnum)
        return regnums

    def get_slot_num_from_reg_num_ev(self, regnum: str) -> int:
        """Return one-based EV slot number for a registration."""
        for i, slot in enumerate(self.ev_slots):
            if isinstance(slot, ElectricVehicle.ElectricVehicle) and str(slot.regnum) == str(
                regnum
            ):
                return i + 1
        return -1

    def get_slot_num_from_color_ev(self, color: str) -> list[str]:
        """Return one-based EV slot numbers filtered by color."""
        slotnums: list[str] = []

        for i, slot in enumerate(self.ev_slots):
            if isinstance(slot, ElectricVehicle.ElectricVehicle) and slot.color == color:
                slotnums.append(str(i + 1))
        return slotnums

    def get_slot_num_from_make_ev(self, make: str) -> list[str]:
        """Return one-based EV slot numbers filtered by make."""
        slotnums: list[str] = []

        for i, slot in enumerate(self.ev_slots):
            if isinstance(slot, ElectricVehicle.ElectricVehicle) and slot.make == make:
                slotnums.append(str(i + 1))
        return slotnums

    def get_slot_num_from_model_ev(self, model: str) -> list[str]:
        """Return one-based EV slot numbers filtered by model."""
        slotnums: list[str] = []

        for i, slot in enumerate(self.ev_slots):
            if isinstance(slot, ElectricVehicle.ElectricVehicle) and slot.model == model:
                slotnums.append(str(i + 1))
        return slotnums

    def slot_num_by_reg(self) -> None:
        """Display the slot number identified by registration value."""
        slot_val = slot1_value.get()
        slotnum = self.get_slot_num_from_reg_num(slot_val)
        slotnum2 = self.get_slot_num_from_reg_num_ev(slot_val)
        output = ""
        if slotnum >= 0:
            output = "Identified slot: " + str(slotnum) + "\n"
        elif slotnum2 >= 0:
            output = "Identified slot (EV): " + str(slotnum2) + "\n"
        else:
            output = "Not found\n"

        self.notify("display_update", output)

    def slot_num_by_color(self) -> None:
        """Display regular and EV slot numbers filtered by color value."""
        slotnums = self.get_slot_num_from_color(slot2_value.get())
        slotnums2 = self.get_slot_num_from_color_ev(slot2_value.get())
        output = "Identified slots: " + ", ".join(slotnums) + "\n"
        self.notify("display_update", output)
        output = "Identified slots (EV): " + ", ".join(slotnums2) + "\n"
        self.notify("display_update", output)

    def reg_num_by_color(self) -> None:
        """Display regular and EV registrations filtered by color value."""
        regnums = self.get_reg_num_from_color(reg1_value.get())
        regnums2 = self.get_reg_num_from_color_ev(reg1_value.get())
        output = "Registation Numbers: " + ", ".join(regnums) + "\n"
        self.notify("display_update", output)
        output = "Registation Numbers (EV): " + ", ".join(regnums2) + "\n"
        self.notify("display_update", output)

    def make_lot(self) -> None:
        """Create a parking lot from UI field values and display confirmation."""
        try:
            self.create_parking_lot(
                int(num_value.get()),
                int(ev_value.get()),
                int(level_value.get()),
            )
        except ValueError:
            self.notify(
                "display_update", "Error: Please enter valid numbers to construct the lot.\n"
            )
            return

        output = (
            "Created a parking lot with "
            + num_value.get()
            + " regular slots and "
            + ev_value.get()
            + " ev slots on level: "
            + level_value.get()
            + "\n"
        )
        self.notify("display_update", output)

    def park_car(self) -> None:
        """Park a vehicle from UI field values and display the result."""
        res = self.park(
            reg_value.get(),
            make_value.get(),
            model_value.get(),
            color_value.get(),
            ev_car_value.get(),
            ev_motor_value.get(),
        )
        if res == -1:
            self.notify("display_update", "Sorry, parking lot is full\n")
        else:
            output = "Allocated slot number: " + str(res) + "\n"
            self.notify("display_update", output)

    def remove_car(self) -> None:
        """Remove a vehicle by slot id from UI field values."""
        try:
            status = self.leave(int(slot_value.get()), int(ev_car2_value.get()))
        except ValueError:
            self.notify("display_update", "Error: Please enter a valid numerical slot ID.\n")
            return

        if status:
            output = "Slot number " + str(slot_value.get()) + " is free\n"
            self.notify("display_update", output)
        else:
            self.notify(
                "display_update",
                "Unable to remove a car from slot: " + str(slot_value.get()) + "\n",
            )


def main() -> None:  # noqa: PLR0915
    """Build and launch the Tkinter Parking Lot Manager interface."""
    parkinglot = ParkingLot()
    display_observer = TkinterDisplayObserver()
    parkinglot.attach(display_observer)

    # input boxes and GUI
    label_head = tk.Label(root, text="Parking Lot Manager", font="Arial 14 bold")
    label_head.grid(row=0, column=0, padx=10, columnspan=4)

    label_head = tk.Label(root, text="Lot Creation", font="Arial 12 bold")
    label_head.grid(row=1, column=0, padx=10, columnspan=4)

    lbl_num = tk.Label(root, text="Number of Regular Spaces", font="Arial 12")
    lbl_num.grid(row=2, column=0, padx=5)

    num_entry = tk.Entry(root, textvariable=num_value, width=6, font="Arial 12")
    num_entry.grid(row=2, column=1, padx=4, pady=2)

    lbl_ev = tk.Label(root, text="Number of EV Spaces", font="Arial 12")
    lbl_ev.grid(row=2, column=2, padx=5)

    num_entry = tk.Entry(root, textvariable=ev_value, width=6, font="Arial 12")
    num_entry.grid(row=2, column=3, padx=4, pady=4)

    lbl_level = tk.Label(root, text="Floor Level", font="Arial 12")
    lbl_level.grid(row=3, column=0, padx=5)

    level_entry = tk.Entry(root, textvariable=level_value, width=6, font="Arial 12")
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

    make_entry = tk.Entry(root, textvariable=make_value, width=12, font="Arial 12")
    make_entry.grid(row=6, column=1, padx=4, pady=4)

    lbl_model = tk.Label(root, text="Model", font="Arial 12")
    lbl_model.grid(row=6, column=2, padx=5)

    model_entry = tk.Entry(root, textvariable=model_value, width=12, font="Arial 12")
    model_entry.grid(row=6, column=3, padx=4, pady=4)

    lbl_color = tk.Label(root, text="Color", font="Arial 12")
    lbl_color.grid(row=7, column=0, padx=5)

    color_entry = tk.Entry(root, textvariable=color_value, width=12, font="Arial 12")
    color_entry.grid(row=7, column=1, padx=4, pady=4)

    lbl_reg = tk.Label(root, text="Registration #", font="Arial 12")
    lbl_reg.grid(row=7, column=2, padx=5)

    reg_entry = tk.Entry(root, textvariable=reg_value, width=12, font="Arial 12")
    reg_entry.grid(row=7, column=3, padx=4, pady=4)

    ev_toggle = tk.Checkbutton(
        root,
        text="Electric",
        variable=ev_car_value,
        onvalue=1,
        offvalue=0,
        font="Arial 12",
    )
    ev_toggle.grid(column=0, row=8, padx=4, pady=4)

    motor_toggle = tk.Checkbutton(
        root,
        text="Motorcycle",
        variable=ev_motor_value,
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

    slot_entry = tk.Entry(root, textvariable=slot_value, width=12, font="Arial 12")
    slot_entry.grid(row=10, column=1, padx=4, pady=4)

    ev_toggle = tk.Checkbutton(
        root,
        text="Remove EV?",
        variable=ev_car2_value,
        onvalue=1,
        offvalue=0,
        font="Arial 12",
    )
    ev_toggle.grid(column=2, row=10, padx=4, pady=4)

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

    slot1_entry = tk.Entry(root, textvariable=slot1_value, width=12, font="Arial 12")
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

    slot2_entry = tk.Entry(root, textvariable=slot2_value, width=12, font="Arial 12")
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

    reg1_entry = tk.Entry(root, textvariable=reg1_value, width=12, font="Arial 12")
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
