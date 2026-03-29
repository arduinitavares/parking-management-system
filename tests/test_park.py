"""Unit tests for the park method of the ParkingLot class in parking_manager.py."""

import importlib
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Mock tkinter before importing parking_manager to prevent GUI initialization during tests
sys.modules["tkinter"] = MagicMock()

ELECTRIC_VEHICLE_MODULE = importlib.import_module("ElectricVehicle")
VEHICLE_MODULE = importlib.import_module("Vehicle")
PARKING_MANAGER_MODULE = importlib.import_module("parking_manager")
PARKING_LOT_CLASS = PARKING_MANAGER_MODULE.ParkingLot
VEHICLE_CAR_CLASS = VEHICLE_MODULE.Car
ELECTRIC_CAR_CLASS = ELECTRIC_VEHICLE_MODULE.ElectricCar
UI_STATE_CLASS = PARKING_MANAGER_MODULE.UIState
VEHICLE_REPO_CLASS = PARKING_MANAGER_MODULE.VehicleRepository
EV_REPO_CLASS = PARKING_MANAGER_MODULE.EVRepository


class TestParkingLotPark(unittest.TestCase):
    """Behavioral tests for parking regular and electric vehicles."""

    def setUp(self) -> None:
        """Prepare a ParkingLot instance before each test."""
        self.ui_state = UI_STATE_CLASS()
        self.vehicle_repo = VEHICLE_REPO_CLASS()
        self.ev_repo = EV_REPO_CLASS()
        self.lot = PARKING_LOT_CLASS(self.ui_state, self.vehicle_repo, self.ev_repo)
        # Create a lot with 2 regular slots and 1 EV slot on floor 1
        self.lot.create_parking_lot(capacity=2, evcapacity=1, level=1)

    def test_nominal_park_regular_car(self) -> None:
        """Nominal Case: Successfully park a regular car."""
        # Park a regular car (ev=0, motor=0)
        slot_id = self.lot.park("REG123", "Toyota", "Camry", "Red", 0, 0)

        self.assertEqual(slot_id, 1)
        self.assertEqual(self.lot.num_of_occupied_slots, 1)
        self.assertIsInstance(self.lot.vehicle_repo.get("1"), VEHICLE_CAR_CLASS)
        self.assertEqual(getattr(self.lot.vehicle_repo.get("1"), "regnum", None), "REG123")

    def test_nominal_park_ev_car(self) -> None:
        """Nominal Case: Successfully park an electric car."""
        # Park an electric car (ev=1, motor=0)
        slot_id = self.lot.park("EV456", "Tesla", "Model 3", "White", 1, 0)

        self.assertEqual(slot_id, 1)
        self.assertEqual(self.lot.num_of_occupied_ev_slots, 1)
        self.assertIsInstance(self.lot.ev_repo.get("1"), ELECTRIC_CAR_CLASS)
        self.assertEqual(getattr(self.lot.ev_repo.get("1"), "regnum", None), "EV456")

    def test_edge_case_lot_full(self) -> None:
        """Edge Case: Attempt to park a regular car when all regular slots are full."""
        # Fill capacity (2 slots)
        self.lot.park("CAR1", "Honda", "Civic", "Blue", 0, 0)
        self.lot.park("CAR2", "Ford", "Focus", "Black", 0, 0)

        # Attempt to park a 3rd regular car in a capacity=2 lot
        slot_id = self.lot.park("CAR3", "Chevy", "Malibu", "Silver", 0, 0)

        # Verify rejection (-1) and that capacity didn't overfill
        self.assertEqual(slot_id, -1)
        self.assertEqual(self.lot.num_of_occupied_slots, 2)

    def test_edge_case_ev_lot_full(self) -> None:
        """Edge Case: Attempt to park an EV when EV slots are full, but regular slots exist."""
        # Fill EV capacity (1 slot)
        self.lot.park("EV1", "Nissan", "Leaf", "Green", 1, 0)

        # Attempt to park a 2nd EV
        slot_id = self.lot.park("EV2", "Polestar", "2", "Grey", 1, 0)

        # Verify rejection
        self.assertEqual(slot_id, -1)
        self.assertEqual(self.lot.num_of_occupied_ev_slots, 1)


if __name__ == "__main__":
    unittest.main()
