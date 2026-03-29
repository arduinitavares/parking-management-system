"""Unit tests establishing baseline for Observer Pattern decouple refactoring."""

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
UI_STATE_CLASS = PARKING_MANAGER_MODULE.UIState
VEHICLE_REPO_CLASS = PARKING_MANAGER_MODULE.VehicleRepository
EV_REPO_CLASS = PARKING_MANAGER_MODULE.EVRepository


class TestObserverUIBaseline(unittest.TestCase):
    """Behavioral tests locking down the tight UI coupling before Observer implementation."""

    def setUp(self) -> None:
        """Prepare a ParkingLot instance and configure isolated DI mock."""
        # Create a mock UIState where StringVars/IntVars are also mocks
        self.ui_state = MagicMock()

        self.vehicle_repo = VEHICLE_REPO_CLASS()
        self.ev_repo = EV_REPO_CLASS()
        self.lot = PARKING_LOT_CLASS(self.ui_state, self.vehicle_repo, self.ev_repo)

        # Attach the concrete Observer with an injected mock text field
        self.mock_tfield = MagicMock()
        observer = PARKING_MANAGER_MODULE.TkinterDisplayObserver(self.mock_tfield)
        self.lot.attach(observer)

    def test_nominal_status_output(self) -> None:
        """Nominal Case: Verify domain status() dynamically dumps data to injected tfield."""
        self.lot.create_parking_lot(capacity=1, evcapacity=0, level=1)

        # Insert a known testing vehicle directly into the domain
        self.lot.park("REG999", "Ford", "Focus", "Blue", 0, 0)

        self.mock_tfield.insert.reset_mock()
        self.lot.status()

        # Verify the injected DI widget received the domain's state string
        calls = self.mock_tfield.insert.call_args_list
        is_rendered = any("REG999" in str(call_args) for call_args in calls)
        self.assertTrue(
            is_rendered, "The injected UI widget did not receive the parked vehicle data."
        )

    def test_edge_ui_rejection(self) -> None:
        """Edge Case: Verify park_car() directly mutates the UI upon capacity rejection."""
        # Create zero capacity to force a boundary rejection
        self.lot.create_parking_lot(capacity=0, evcapacity=0, level=1)

        # Mock the managed UI variables relied on by the controller
        self.ui_state.reg_value.get.return_value = "FULL123"
        self.ui_state.make_value.get.return_value = "MakeFull"
        self.ui_state.model_value.get.return_value = "ModelFull"
        self.ui_state.color_value.get.return_value = "ColorFull"
        self.ui_state.ev_car_value.get.return_value = 0
        self.ui_state.ev_motor_value.get.return_value = 0

        self.mock_tfield.insert.reset_mock()

        # Trigger the simulated CLI mapping wrapper
        self.lot.park_car()

        # The observer should insert the correct full lot rejection message mapped to the view
        self.mock_tfield.insert.assert_called_with(
            ANY, "[ACTION: Park Car] Sorry, parking lot is full\n"
        )


if __name__ == "__main__":
    unittest.main()
