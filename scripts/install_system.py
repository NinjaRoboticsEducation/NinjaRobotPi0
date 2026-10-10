"""Install fixed OS prerequisites while inhibiting Debian service activation."""

import os
import signal
import subprocess
from pathlib import Path

PACKAGES = (
    "build-essential",
    "ca-certificates",
    "curl",
    "git",
    "python3-dev",
    "python3-venv",
    "xz-utils",
    "zstd",
    "bluez",
    "dbus",
)


def install_packages(policy, run=subprocess.run):
    if os.geteuid() != 0:
        raise SystemExit("This narrow OS setup helper requires sudo.")
    # Never overwrite or reinterpret an administrator's service policy.
    descriptor = os.open(policy, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o755)
    owned = os.fstat(descriptor)
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write("#!/bin/sh\nexit 101\n")
        run(["apt-get", "update"], check=True)
        run(
            ["apt-get", "install", "-y", "--no-install-recommends", *PACKAGES],
            check=True,
        )
    finally:
        # Do not remove a policy replaced by an administrator during apt work.
        if policy.exists():
            current = policy.lstat()
            if (current.st_dev, current.st_ino) == (owned.st_dev, owned.st_ino):
                policy.unlink()


def main():
    def interrupted(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupted)
    install_packages(Path("/usr/sbin/policy-rc.d"))


if __name__ == "__main__":
    main()
