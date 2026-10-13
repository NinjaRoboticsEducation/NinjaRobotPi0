"""Bluetooth-only readiness/repair; never constructs robot hardware or runtime."""

import argparse
import asyncio
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from dbus_next import BusType, Variant
from dbus_next.aio import MessageBus
from dbus_next.constants import PropertyAccess
from dbus_next.service import ServiceInterface, dbus_property, method

ADAPTER = "org.bluez.Adapter1"
ADVERTISING = "org.bluez.LEAdvertisingManager1"
GATT = "org.bluez.GattManager1"
TIMEOUT = 10


class BluetoothSetupError(RuntimeError):
    pass


class ReadinessAdvertisement(ServiceInterface):
    """Short-lived connectable advertisement; no robot command surface."""

    def __init__(self):
        super().__init__("org.bluez.LEAdvertisement1")

    @dbus_property(access=PropertyAccess.READ)
    def Type(self) -> "s":  # noqa: F821
        return "peripheral"

    @method()
    def Release(self):
        pass


def supported_host():
    path = Path("/proc/device-tree/model")
    return (
        platform.system() == "Linux"
        and path.is_file()
        and "Raspberry Pi Zero 2" in path.read_text()
    )


def radio_blocks(root=Path("/sys/class/rfkill")):
    """Read kernel attributes rather than locale-dependent rfkill output."""
    soft = hard = False
    for entry in root.glob("rfkill*"):
        if (entry / "type").read_text().strip() == "bluetooth":
            soft |= (entry / "soft").read_text().strip() == "1"
            hard |= (entry / "hard").read_text().strip() == "1"
    return soft, hard


def legacy_uart_available():
    pins = Path("/proc/device-tree/soc/gpio@7e200000/bt_pins/brcm,pins")
    # serial1 normally exists on the legacy userspace UART path. Do not force
    # that path on kernel-managed Bookworm/Trixie controllers.
    return Path("/dev/serial1").exists() and pins.is_file() and bool(pins.read_bytes())


async def command(args, *, privileged=False, allow_failure=False):
    try:
        if privileged and os.geteuid() != 0:
            # Let sudo display its password prompt directly in the terminal;
            # never capture or pass an authentication secret ourselves.
            print("Bluetooth setup needs administrator permission (sudo).")
            auth = await asyncio.to_thread(subprocess.run, ["sudo", "-v"], timeout=60)
            if auth.returncode:
                raise BluetoothSetupError(
                    "Administrator permission was not granted. Bluetooth repair did not complete."
                )
            args = ["sudo", "-n", *args]
        result = await asyncio.to_thread(
            subprocess.run,
            args,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BluetoothSetupError(
            f"Bluetooth command unavailable/timed out: {args[-1]}. Check installation and sudo permission."
        ) from exc
    if result.returncode and not allow_failure:
        raise BluetoothSetupError(
            f"Bluetooth command failed: {' '.join(args)}. Check sudo permission and journalctl -u bluetooth -b."
        )
    return result.stdout


async def unit_state(unit):
    text = await command(
        ["systemctl", "show", unit, "--property=LoadState,ActiveState,UnitFileState"],
        allow_failure=True,
    )
    state = dict(line.split("=", 1) for line in text.splitlines() if "=" in line)
    if "LoadState" not in state:
        raise BluetoothSetupError(
            "Could not inspect Bluetooth systemd service. Check that systemd is running."
        )
    return state


async def ensure_unit(unit, repair):
    state = await unit_state(unit)
    if state.get("LoadState") == "masked" or state.get("UnitFileState") in (
        "masked",
        "masked-runtime",
    ):
        raise BluetoothSetupError(
            f"{unit} is masked by system policy. Ask the administrator to review it; setup will not unmask it."
        )
    if state.get("LoadState") != "loaded":
        raise BluetoothSetupError(
            f"{unit} is missing. Install the Raspberry Pi OS Bluetooth prerequisites (bluez, rfkill); rerun install.sh if needed."
        )
    enabled = state.get("UnitFileState") in ("enabled", "static", "indirect")
    active = state.get("ActiveState") == "active"
    if not enabled or not active:
        if not repair:
            raise BluetoothSetupError(
                f"{unit} is not enabled/active. Run ./onboard.sh --step identity to repair Bluetooth."
            )
        if not enabled:
            print(f"Enabling {unit} for future boots...")
            await command(["systemctl", "enable", unit], privileged=True)
        if not active:
            print(f"Starting {unit}...")
            await command(["systemctl", "start", unit], privileged=True)
        state = await unit_state(unit)
        if state.get("ActiveState") != "active" or state.get("UnitFileState") not in (
            "enabled",
            "static",
            "indirect",
        ):
            raise BluetoothSetupError(
                f"{unit} did not become active. Check journalctl -u {unit} -b; a missing controller or firmware may prevent startup."
            )


async def bounded(awaitable):
    return await asyncio.wait_for(awaitable, TIMEOUT)


class BlueZSession:
    def __init__(self):
        self.bus = None

    async def connect(self):
        self.bus = MessageBus(bus_type=BusType.SYSTEM)
        await bounded(self.bus.connect())

    async def objects(self):
        tree = await bounded(self.bus.introspect("org.bluez", "/"))
        iface = self.bus.get_proxy_object("org.bluez", "/", tree).get_interface(
            "org.freedesktop.DBus.ObjectManager"
        )
        return await bounded(iface.call_get_managed_objects())

    async def interface(self, path, name):
        tree = await bounded(self.bus.introspect("org.bluez", path))
        return self.bus.get_proxy_object("org.bluez", path, tree).get_interface(name)

    async def power_on(self, path):
        iface = await self.interface(path, "org.freedesktop.DBus.Properties")
        await bounded(iface.call_set(ADAPTER, "Powered", Variant("b", True)))

    async def probe(self, path):
        manager = await self.interface(path, ADVERTISING)
        object_path = "/org/ninjarobot/readiness/" + "p" + uuid4().hex
        self.bus.export(object_path, ReadinessAdvertisement())
        registered = False
        try:
            await bounded(manager.call_register_advertisement(object_path, {}))
            registered = True
        finally:
            # A timed-out registration may have succeeded remotely. Unregister
            # only this process-owned path, then disconnect to release leftovers.
            try:
                await bounded(manager.call_unregister_advertisement(object_path))
            except Exception as exc:
                if registered:
                    raise BluetoothSetupError(
                        "Test advertisement cleanup failed; the setup connection will be closed. Retry readiness before starting the server."
                    ) from exc
            finally:
                self.bus.unexport(object_path)

    def close(self):
        if self.bus:
            self.bus.disconnect()


def value(properties, key, default=None):
    item = properties.get(key)
    return getattr(item, "value", default)


def adapter_objects(objects):
    return [
        (path, interfaces)
        for path, interfaces in sorted(objects.items())
        if re.fullmatch(r"/org/bluez/hci\d+", path) and ADAPTER in interfaces
    ]


async def prepare_bluetooth(*, repair=False, session_factory=BlueZSession):
    """Inspect or repair Bluetooth. True means readiness verified, not a robot test."""
    if not supported_host():
        raise BluetoothSetupError(
            "BLE setup requires Raspberry Pi Zero 2 W running Linux; no settings were changed."
        )
    soft, hard = radio_blocks()
    if hard:
        raise BluetoothSetupError(
            "Bluetooth is hardware-blocked. Check the controller/firmware; software cannot unblock it."
        )
    if soft:
        if not repair:
            raise BluetoothSetupError(
                "Bluetooth is soft-blocked. Run ./onboard.sh --step identity to unblock Bluetooth."
            )
        if not shutil.which("rfkill"):
            raise BluetoothSetupError(
                "rfkill is missing. Run sudo apt-get install --no-install-recommends rfkill, then retry BLE setup."
            )
        print("Unblocking the Bluetooth radio...")
        await command(["rfkill", "unblock", "bluetooth"], privileged=True)
        if any(radio_blocks()):
            raise BluetoothSetupError(
                "Bluetooth remains blocked after repair. Check rfkill and firmware."
            )
    # Start legacy UART only when its prerequisites exist and no kernel
    # controller has already appeared. No boot/UART settings are edited.
    if (
        repair
        and not list(Path("/sys/class/bluetooth").glob("hci*"))
        and legacy_uart_available()
    ):
        await ensure_unit("hciuart.service", repair)
    await ensure_unit("bluetooth.service", repair)
    session = session_factory()
    try:
        await session.connect()
        adapters = []
        for attempt in range(5 if repair else 1):
            adapters = adapter_objects(await session.objects())
            if adapters:
                break
            if repair and attempt < 4:
                await asyncio.sleep(1)
        if not adapters:
            raise BluetoothSetupError(
                "No Bluetooth controller found. Check firmware, rfkill and any disable-bt overlay in /boot/firmware/config.txt (or /boot/config.txt). Setup does not edit boot files or reboot."
            )
        path, interfaces = adapters[0]
        if ADVERTISING not in interfaces or GATT not in interfaces:
            raise BluetoothSetupError(
                f"{path} lacks BLE advertising/GATT support. Check BlueZ/controller firmware; setup does not enable experimental features."
            )
        if not value(interfaces[ADAPTER], "Powered", False):
            if not repair:
                raise BluetoothSetupError(
                    "Bluetooth controller is powered off. Run ./onboard.sh --step identity to power it on."
                )
            print("Powering on the Bluetooth controller...")
            try:
                await session.power_on(path)
            except Exception as exc:
                if getattr(exc, "type", "") not in (
                    "org.freedesktop.DBus.Error.AccessDenied",
                    "org.bluez.Error.NotAuthorized",
                ):
                    raise
                await command(
                    [
                        "busctl",
                        "set-property",
                        "org.bluez",
                        path,
                        ADAPTER,
                        "Powered",
                        "b",
                        "true",
                    ],
                    privileged=True,
                )
            for attempt in range(5):
                interfaces = (await session.objects()).get(path, {})
                if value(interfaces.get(ADAPTER, {}), "Powered", False):
                    break
                await asyncio.sleep(0.2)
            else:
                raise BluetoothSetupError(
                    "Bluetooth controller did not power on. Check rfkill and firmware."
                )
        advertisement = interfaces.get(ADVERTISING, {})
        available = value(advertisement, "SupportedInstances", 0)
        active = value(advertisement, "ActiveInstances", 0)
        if active:
            raise BluetoothSetupError(
                "Another BLE advertisement is active. Stop ninja_core server or the other BLE application, then retry onboarding. Existing advertisements were retained."
            )
        if available < 1:
            raise BluetoothSetupError(
                "No BLE advertising instance is available. Check controller firmware/BlueZ; setup will not restart or power-cycle a healthy controller."
            )
        if repair:
            print("Checking a temporary BLE advertisement (no robot commands)...")
            await session.probe(path)
            print(
                "Bluetooth ready: service active, controller powered, test advertisement cleaned up."
            )
        else:
            print(
                "Bluetooth readiness checks passed. Read-only mode did not test advertisement registration."
            )
        return True
    except BluetoothSetupError:
        raise
    except Exception as exc:
        name = (
            getattr(exc, "type", None)
            or getattr(exc, "dbus_error", None)
            or type(exc).__name__
        )
        raise BluetoothSetupError(
            f"Bluetooth verification failed ({name}): {exc}. Check journalctl -u bluetooth -b and journalctl -k -b; firmware or D-Bus permissions may need attention."
        ) from exc
    finally:
        session.close()


def run_setup(*, repair=False):
    try:
        return asyncio.run(prepare_bluetooth(repair=repair))
    except (BluetoothSetupError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Bluetooth-only readiness: no robot runtime or actuator initialization."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_true", help="Read-only readiness inspection (default)"
    )
    mode.add_argument(
        "--repair",
        action="store_true",
        help="Enable/start/unblock/power Bluetooth and verify a temporary advertisement",
    )
    args = parser.parse_args()
    return 0 if run_setup(repair=args.repair) else 1


if __name__ == "__main__":
    raise SystemExit(main())
