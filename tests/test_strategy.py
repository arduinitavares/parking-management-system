"""Unit test suite for the ParkingStrategy implementations."""

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

PARKING_MANAGER_MODULE = importlib.import_module("parking_manager")
PARKING_LOT_CLASS = PARKING_MANAGER_MODULE.ParkingLot
REGULAR_STRATEGY = PARKING_MANAGER_MODULE.RegularParkingStrategy
ELECTRIC_STRATEGY = PARKING_MANAGER_MODULE.ElectricParkingStrategy
UI_STATE_CLASS = PARKING_MANAGER_MODULE.UIState
VEHICLE_REPO_CLASS = PARKING_MANAGER_MODULE.VehicleRepository
EV_REPO_CLASS = PARKING_MANAGER_MODULE.EVRepository


class TestParkingStrategy(unittest.TestCase):
    """Directly test the concrete strategy allocation behaviors."""

    def setUp(self) -> None:
        """Prepare a clean ParkingLot instance and strategy objects."""
        self.ui_state = UI_STATE_CLASS()
        self.vehicle_repo = VEHICLE_REPO_CLASS()
        self.ev_repo = EV_REPO_CLASS()
        self.lot = PARKING_LOT_CLASS(self.ui_state, self.vehicle_repo, self.ev_repo)
        # 1 regular slot, 1 EV slot on level 1
        self.lot.create_parking_lot(capacity=1, evcapacity=1, level=1)
        self.reg_strategy = REGULAR_STRATEGY()
        self.ev_strategy = ELECTRIC_STRATEGY()

    def test_regular_strategy_allocation(self) -> None:
        """Test the concrete RegularParkingStrategy for car allocation."""
        slot_id = self.reg_strategy.allocate_slot(self.lot, "REG001", "Ford", "Fiesta", "Blue", 0)
        self.assertEqual(slot_id, 1)
        self.assertEqual(self.lot.num_of_occupied_slots, 1)

    def test_electric_strategy_allocation(self) -> None:
        """Test the concrete ElectricParkingStrategy for EV allocation."""
        slot_id = self.ev_strategy.allocate_slot(self.lot, "EV002", "Tesla", "Model S", "Black", 0)
        self.assertEqual(slot_id, 1)
        self.assertEqual(self.lot.num_of_occupied_ev_slots, 1)

    def test_strategy_switching_runtime(self) -> None:
        """Test runtime switching between both strategies successfully."""
        # Use lot.park() which dynamically switches strategies internally based on EV flag
        # Park an EV
        res1 = self.lot.park("EV99", "Lucid", "Air", "White", 1, 0)
        self.assertEqual(res1, 1)
        self.assertEqual(self.lot.num_of_occupied_ev_slots, 1)

        # Switch to Regular immediately after
        res2 = self.lot.park("REG99", "Honda", "Civic", "Red", 0, 0)
        self.assertEqual(res2, 1)
        self.assertEqual(self.lot.num_of_occupied_slots, 1)

    def test_strategy_boundary_conditions_and_errors(self) -> None:
        """Test boundary bounds checking directly inside the strategies."""
        # Fill the lot using the strategies directly
        res1 = self.reg_strategy.allocate_slot(self.lot, "BOUND1", "Toyota", "Corolla", "Grey", 0)
        self.assertEqual(res1, 1)

        # Confirm capacity blocking immediately returns -1
        res2 = self.reg_strategy.allocate_slot(self.lot, "BOUND2", "Honda", "Accord", "White", 0)
        self.assertEqual(res2, -1)
        self.assertEqual(self.lot.num_of_occupied_slots, 1)

        # Manual desync of count to trigger get_empty_slot internal failure
        class Dummy:
            pass

        # Manually fill the single available EV slot natively
        self.lot.ev_repo._store["1"] = Dummy()

        # When get_empty_ev_slot() returns None because "1" is already artificially mapped:
        res3 = self.ev_strategy.allocate_slot(self.lot, "ERR1", "Hyundai", "Ioniq", "Blue", 0)
        self.assertEqual(res3, -1)

        # Same bypass test for RegularParkingStrategy
        self.lot.vehicle_repo._store["1"] = Dummy()
        res4 = self.reg_strategy.allocate_slot(self.lot, "ERR2", "Ford", "Mustang", "Red", 0)
        self.assertEqual(res4, -1)

    def test_two_wheeler_allocation(self) -> None:
        """Test the motor=1 branch mapping to Motorcycle and EBike."""
        self.lot.create_parking_lot(capacity=1, evcapacity=1, level=1)

        # Test Regular Motorcycle
        slot_id = self.reg_strategy.allocate_slot(self.lot, "MOTO1", "Yamaha", "R1", "Blue", 1)
        self.assertEqual(slot_id, 1)

        # Test Electric Bike
        slot_id2 = self.ev_strategy.allocate_slot(self.lot, "EBIKE1", "Zero", "SR", "Black", 1)
        self.assertEqual(slot_id2, 1)

    def test_abc_interfaces(self) -> None:
        """Test coverage for the ABC stubs."""
        with self.assertRaises(NotImplementedError):
            PARKING_MANAGER_MODULE.ParkingStrategy.allocate_slot(
                self=None, lot=None, regnum="", make="", model="", color="", motor=0
            )
        with self.assertRaises(NotImplementedError):
            PARKING_MANAGER_MODULE.ParkingObserver.update(self=None, event_type="", message="")


if __name__ == "__main__":
    unittest.main()
