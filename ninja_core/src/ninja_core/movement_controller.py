import time
import threading
from ninja_core.hal import HardwareAbstractionLayer
from ninja_core.config import NinjaConfig
from ninja_core.builtin_movements import available_movements, validate_movement

from typing import Callable, Optional

class EmergencyStop(Exception):
    """Raised when a movement is aborted due to safety checks."""
    pass


class MovementController:
    """A controller to manage and execute complex, multi-servo movement sequences."""

    def __init__(self, hal: HardwareAbstractionLayer, config: NinjaConfig):
        """
        Initializes the MovementController.

        Args:
            hal: The HardwareAbstractionLayer instance.
            config: The NinjaConfig instance for loading settings.
        """
        self.servos = hal.servos
        self.servo_definitions = config.servos.calibration
        self.movements = config.movements
        self.config = config
        self._motion_lock = threading.RLock()

    def available_movement_names(self) -> list[str]:
        """List only sequences executable on this profile and active channels."""
        pins = self.servos.pins if self.servos else ()
        return available_movements(self.config, pins)

    def validate_movement(self, name: str) -> None:
        pins = self.servos.pins if self.servos else ()
        validate_movement(self.config, name, pins)

    def move_servos(
        self,
        movements: dict[int, float],
        speed: str = "M",
        per_servo_speeds: dict[int, str] | None = None,
        abort_check: Optional[Callable[[], bool]] = None,
        easing: str = "ease_in_out_cubic",
    ):
        """
        Executes a set of servo movements with per-servo velocity control.

        Uses pi0servo's move_all_sync which handles:
        - Per-servo speed limits from calibration
        - Per-servo duration calculation
        - Easing curves for smooth motion

        Args:
            movements: A dictionary of {pin: angle}.
            speed: Global speed mode ('S'low, 'M'edium, 'F'ast).
            per_servo_speeds: Optional {pin: speed} for per-servo override.
            abort_check: Optional function that returns True to abort.
        """
        if not self.servos:
            return

        # Build ordered list of target angles and speed modes
        ordered_pins = self.servos.pins
        target_angles: list[float | None] = []
        speed_modes: list[str] = []

        per_servo_speeds = per_servo_speeds or {}

        for pin in ordered_pins:
            if pin in movements:
                target_angles.append(movements[pin])
                # Use per-servo speed if specified, otherwise global
                servo_speed = per_servo_speeds.get(pin, speed)
                speed_modes.append(servo_speed)
            else:
                # Hold current position (don't move this servo)
                target_angles.append(None)
                speed_modes.append(speed)

        # Use pi0servo's move_all_sync with per-servo speed modes
        # This handles velocity calculation, easing, and abort internally
        with self._motion_lock:
            if abort_check and abort_check():
                raise EmergencyStop("Movement aborted by safety check.")
            completed = self.servos.move_all_sync(
                target_angles,
                speed_mode=speed_modes,
                easing=easing,
                force=True,  # Prevent skipped PWM updates causing limpness
            )
            if not completed or (abort_check and abort_check()):
                # Stop without commanding an unsolicited recovery pose.
                raise EmergencyStop("Movement aborted by driver or safety check.")

    def get_current_angles(self) -> dict[int, float]:
        """
        Returns a dictionary of {pin: current_angle} by mapping the list
        from the driver to its corresponding pins.
        """
        if not self.servos:
            # Return 0 for all known pins if driver is missing
            return {int(pin): 0.0 for pin in self.servo_definitions.keys()}

        angle_list = self.servos.get_all_angles()
        pin_list = self.servos.pins
        return {pin_list[i]: angle_list[i] for i in range(len(pin_list))}

    def center_all_servos(self, abort_check: Optional[Callable[[], bool]] = None):
        """Center servos, optionally guarded by a browser/safety lifecycle."""
        print("Centering all servos...")
        center_angles = {int(pin): 0 for pin in self.servo_definitions.keys()}
        self.move_servos(center_angles, speed="F", abort_check=abort_check)
        time.sleep(0.5)

    def execute_movement(
        self, movement_name: str, abort_check: Optional[Callable[[], bool]] = None
    ):
        """
        Executes a pre-defined movement sequence by name.

        Args:
            movement_name: The name of the movement to execute.
            abort_check: An optional function that returns True if the movement should stop.
        """
        with self._motion_lock:
            self.validate_movement(movement_name)
            self._execute_validated_movement(movement_name, abort_check)

    def _execute_validated_movement(self, movement_name, abort_check):
        print(f"Executing movement: '{movement_name}'...")
        sequence = self.movements[movement_name]
        total_steps = len(sequence)
        
        for i, step in enumerate(sequence):
            # Position-aware easing for smooth transitions
            if total_steps == 1:
                easing = "ease_in_out_cubic"  # Single step: full curve
            elif i == 0:
                easing = "ease_in_cubic"  # First: accelerate only
            elif i == total_steps - 1:
                easing = "ease_out_cubic"  # Last: decelerate to stop
            else:
                easing = "linear"  # Middle: constant velocity
            
            # The keys in 'moves' from JSON will be strings, convert them to int
            moves = {int(k): v for k, v in step["moves"].items()}
            # Extract per-servo speeds if stored (int keys from JSON strings)
            per_servo = None
            if "per_servo_speeds" in step:
                per_servo = {int(k): v for k, v in step["per_servo_speeds"].items()}
            self.move_servos(moves, step["speed"], per_servo, abort_check, easing)
        print(f"Movement '{movement_name}' finished.")
