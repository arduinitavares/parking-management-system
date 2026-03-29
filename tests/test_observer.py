"""Unit tests establishing baseline for Observer Pattern decouple refactoring in parking_manager.py."""

import importlib
import sys
import unittest
from pathlib import Path
from unittest.mock import ANY, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Mock tkinter before importing parking_manager to prevent GUI initialization during tests
sys.modules["tkinter"] = MagicMock()

PARKING_MANAGER_MODULE = importlib.import_module("parking_manager")
PARKING_LOT_CLASS = PARKING_MANAGER_MODULE.ParkingLot


class TestObserverUIBaseline(unittest.TestCase):
    """Behavioral tests locking down the tight UI coupling before Observer implementation."""

    def setUp(self) -> None:
        """Prepare a ParkingLot instance and reset the global UI mock before each test."""
        self.lot = PARKING_LOT_CLASS()

        # Attach the concrete Observer to properly route notifications back to the mocked tfield
        observer = PARKING_MANAGER_MODULE.TkinterDisplayObserver()
        self.lot.attach(observer)

        PARKING_MANAGER_MODULE.tfield.insert.reset_mock()

    def test_nominal_status_output(self) -> None:
        """Nominal Case: Verify domain status() dynamically dumps data to global tfield."""
        self.lot.create_parking_lot(capacity=1, evcapacity=0, level=1)

        # Insert a known testing vehicle directly into the domain
        self.lot.park("REG999", "Ford", "Focus", "Blue", 0, 0)

        PARKING_MANAGER_MODULE.tfield.insert.reset_mock()
        self.lot.status()

        # Verify the global tfield text widget received the domain's state string
        calls = PARKING_MANAGER_MODULE.tfield.insert.call_args_list
        is_rendered = any("REG999" in str(call_args) for call_args in calls)
        self.assertTrue(
            is_rendered, "The global UI widget did not receive the parked vehicle data."
        )

    def test_edge_ui_rejection(self) -> None:
        """Edge Case: Verify park_car() directly mutates the UI upon capacity rejection."""
        # Create zero capacity to force a boundary rejection
        self.lot.create_parking_lot(capacity=0, evcapacity=0, level=1)

        # Mock the global Tkinter StringVars/IntVars relied on by park_car()
        PARKING_MANAGER_MODULE.reg_value.get.return_value = "FULL123"
        PARKING_MANAGER_MODULE.make_value.get.return_value = "MakeFull"
        PARKING_MANAGER_MODULE.model_value.get.return_value = "ModelFull"
        PARKING_MANAGER_MODULE.color_value.get.return_value = "ColorFull"
        PARKING_MANAGER_MODULE.ev_car_value.get.return_value = 0
        PARKING_MANAGER_MODULE.ev_motor_value.get.return_value = 0

        PARKING_MANAGER_MODULE.tfield.insert.reset_mock()

        # Trigger the UI button simulation
        self.lot.park_car()

        # The baseline anti-pattern asserts the domain object directly warns the user via Tkinter
        PARKING_MANAGER_MODULE.tfield.insert.assert_called_with(ANY, "Sorry, parking lot is full\n")


if __name__ == "__main__":
    unittest.main()
