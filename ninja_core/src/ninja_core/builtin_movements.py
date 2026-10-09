"""Hardware-free native movement catalog, import reconciliation and preflight."""

from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .config import NinjaConfig

SPIDER_PINS = frozenset(range(20, 28))
SPIDER_POWEROFF = [{
    "speed": "S",
    "moves": {"20": -90, "21": 90, "22": 90, "23": -90,
              "24": 90, "25": -90, "26": -90, "27": 90},
    "per_servo_speeds": {},
}]
TYPE_PREFIXES = {"spider_": "spider", "humanoid_": "humanoid",
                 "wheel_": "tire", "tire_": "tire"}


class MovementValidationError(ValueError):
    """A native sequence cannot be executed on the selected robot."""


def movement_hash(sequence: list) -> str:
    """Fingerprint a managed value, independent of JSON dictionary ordering."""
    return hashlib.sha256(json.dumps(
        sequence, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()).hexdigest()


@lru_cache(maxsize=1)
def _spider_catalog() -> dict[str, list]:
    pack = json.loads(files("ninja_core").joinpath("data/spider_otto.json").read_text())
    movements = {
        name.replace("spider_otto_", "spider_", 1): steps
        for name, steps in pack["movements"].items()
    }
    movements["Poweroff"] = SPIDER_POWEROFF
    return movements


@lru_cache(maxsize=1)
def _spider_poses() -> list[list[dict]]:
    # Speed edits and omitted empty overrides do not change robot geometry.
    return [[step["moves"] for step in sequence]
            for sequence in _spider_catalog().values()]


def builtin_catalog(robot_type: str, pins: Iterable[int]) -> dict[str, list]:
    """Return independent definitions for a profile's configured channels."""
    pins = set(pins)
    if robot_type == "spider":
        return deepcopy(_spider_catalog()) if SPIDER_PINS <= pins else {}
    if robot_type in {"tire", "humanoid"} and pins:
        return {"home": [{
            "moves": {str(pin): 0 for pin in sorted(pins)}, "speed": "S",
        }]}
    return {}


def configured_pins(config: NinjaConfig) -> set[int]:
    """Match HAL channel selection (calibration keys, not descriptive names)."""
    return {int(pin) for pin in config.servos.calibration}


def validate_sequence(sequence: list, pins: Iterable[int]) -> None:
    """Validate every waypoint before allowing any actuator command."""
    known_pins = set(pins)
    if not isinstance(sequence, list) or not sequence:
        raise MovementValidationError("Movement must contain at least one step.")
    for index, step in enumerate(sequence):
        context = f"Movement step {index + 1}"
        if not isinstance(step, dict) or set(step) - {
            "moves", "speed", "per_servo_speeds"
        }:
            raise MovementValidationError(f"{context}: unsupported step fields.")
        moves = step.get("moves")
        if not isinstance(moves, dict) or not moves:
            raise MovementValidationError(f"{context}: moves must be a nonempty object.")
        if step.get("speed") not in ("F", "M", "S"):
            raise MovementValidationError(f"{context}: speed must be F, M or S.")
        normalized = set()
        for pin, angle in moves.items():
            if isinstance(pin, bool) or not isinstance(pin, (str, int)):
                raise MovementValidationError(f"{context}: invalid GPIO key.")
            try:
                number = int(pin)
            except (TypeError, ValueError) as exc:
                raise MovementValidationError(f"{context}: invalid GPIO key.") from exc
            if (str(number) != str(pin) or not 0 <= number <= 27
                    or number not in known_pins or number in normalized):
                raise MovementValidationError(f"{context}: GPIO {pin} is unavailable or invalid.")
            normalized.add(number)
            if (isinstance(angle, bool) or not isinstance(angle, (int, float))
                    or not -90 <= angle <= 90 or not math.isfinite(angle)):
                raise MovementValidationError(f"{context}: GPIO {pin} angle must be finite within ±90.")
        overrides = step.get("per_servo_speeds", {})
        if not isinstance(overrides, dict):
            raise MovementValidationError(f"{context}: invalid speed overrides.")
        for pin, speed in overrides.items():
            # Overrides for omitted targets historically have no effect; retain them.
            if str(pin) not in {str(p) for p in known_pins} or speed not in ("F", "M", "S"):
                raise MovementValidationError(f"{context}: invalid speed override for GPIO {pin}.")


def validate_movement(config: NinjaConfig, name: str, pins: Iterable[int]) -> None:
    """Enforce all known scopes, even for legacy data without metadata."""
    if name not in config.movements:
        raise MovementValidationError(f"Movement '{name}' not found.")
    scopes = {config.movement_robot_types[name]} if name in config.movement_robot_types else set()
    scopes.update(scope for prefix, scope in TYPE_PREFIXES.items()
                  if name.lower().startswith(prefix))
    sequence = config.movements[name]
    # Recognize copied/renamed Spider trajectories, especially legacy Poweroff.
    poses = [step.get("moves") if isinstance(step, dict) else None
             for step in sequence]
    if poses in _spider_poses():
        scopes.add("spider")
    if scopes and scopes != {config.robot_type}:
        raise MovementValidationError(
            f"Movement '{name}' requires {', '.join(sorted(scopes))}; robot type is {config.robot_type}."
        )
    validate_sequence(sequence, pins)


def available_movements(config: NinjaConfig, pins: Iterable[int] | None = None) -> list[str]:
    """Shared filtered discovery for native CLI, web and agent."""
    pins = configured_pins(config) if pins is None else set(pins)
    names = []
    for name in config.movements:
        try:
            validate_movement(config, name, pins)
        except MovementValidationError:
            continue
        names.append(name)
    return names


def seed_builtin_movements(config: NinjaConfig) -> bool:
    """Reconcile only unchanged managed entries; preserve user data and scope."""
    before = deepcopy((config.movements, config.movement_robot_types,
                       config.builtin_movement_hashes))
    catalog = builtin_catalog(config.robot_type, configured_pins(config))
    for name, fingerprint in list(config.builtin_movement_hashes.items()):
        current = config.movements.get(name)
        if current is None:
            config.builtin_movement_hashes.pop(name)
            config.movement_robot_types.pop(name, None)
            continue
        try:
            unchanged = movement_hash(current) == fingerprint
        except (ValueError, TypeError):
            unchanged = False
        if unchanged:
            # Removal/replacement is limited to our last exact imported value.
            del config.movements[name]
            config.builtin_movement_hashes.pop(name)
            config.movement_robot_types.pop(name, None)
            if name in catalog:
                config.movements[name] = deepcopy(catalog[name])
                config.movement_robot_types[name] = config.robot_type
                config.builtin_movement_hashes[name] = movement_hash(catalog[name])
    for name, sequence in catalog.items():
        if name not in config.movements:
            config.movements[name] = sequence
            config.movement_robot_types[name] = config.robot_type
            config.builtin_movement_hashes[name] = movement_hash(sequence)
        elif config.movements[name] == sequence:
            # Adopt identical pre-existing built-ins with explicit type scope.
            config.movement_robot_types[name] = config.robot_type
            config.builtin_movement_hashes[name] = movement_hash(sequence)
    return before != (config.movements, config.movement_robot_types,
                      config.builtin_movement_hashes)
