import os
import subprocess
import sys
import getpass
import shutil
from pathlib import Path
from .my_logger import get_logger

logger = get_logger("service_manager")

class ServiceManager:
    SERVICE_NAME = "ninjarobot.service"
    SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"

    def __init__(self):
        self.user = getpass.getuser()
        # Assuming ninja_utils is installed in editable mode inside the project root,
        # or we can find the project root by looking for pyproject.toml
        self.project_root = self._find_project_root()
        self.uv_path = shutil.which("uv")

    def _find_project_root(self) -> Path:
        """Finds the project root by looking for config.json or pyproject.toml."""
        current_path = Path.cwd()
        # If we are running from the project root
        if (current_path / "config.json").exists() or (current_path / "pyproject.toml").exists():
            return current_path
        
        # If we are inside a subdirectory, look upwards
        for parent in current_path.parents:
            if (parent / "config.json").exists() or (parent / "pyproject.toml").exists():
                return parent
        
        # Fallback to current directory if not found (might fail validation later)
        return current_path

    def _run_command(self, command: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Runs a shell command."""
        try:
            return subprocess.run(command, check=check, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}\nError: {e.stderr}")
            raise

    def _check_prerequisites(self):
        """Validates that the system is ready for autostart installation."""
        logger.info("Checking prerequisites...")

        # 1. Check for config.json
        config_path = self.project_root / "config.json"
        if not config_path.exists():
            raise RuntimeError(
                f"Configuration file not found at {config_path}.\n"
                "Please run 'ninja_core config import-all' and 'ninja_core config set-key' first."
            )
        logger.info("✅ config.json found.")

        # 2. Check if pigpiod is running
        try:
            subprocess.run(["systemctl", "is-active", "--quiet", "pigpiod"], check=True)
            logger.info("✅ pigpiod is running.")
        except subprocess.CalledProcessError:
            raise RuntimeError(
                "pigpiod daemon is not running.\n"
                "Please enable it with: sudo systemctl enable --now pigpiod"
            )

        # 3. Check if ninja_core is installed
        try:
            import ninja_core  # noqa: F401
            logger.info("✅ ninja_core is installed.")
        except ImportError:
            raise RuntimeError(
                "ninja_core package is not installed.\n"
                "Please install the project with: uv pip install -e ."
            )

        # 4. Check if uv is found
        if not self.uv_path:
            raise RuntimeError("Could not find 'uv' executable. Please ensure uv is installed and in PATH.")
        logger.info(f"✅ uv found at {self.uv_path}")

    def generate_content(self) -> str:
        """Generates the systemd unit file content."""
        return f"""[Unit]
Description=NinjaRobotV4 Web Server
After=network.target pigpiod.service
Requires=pigpiod.service

[Service]
Type=simple
User={self.user}
WorkingDirectory={self.project_root}
ExecStart={self.uv_path} run ninja_core server --autostart
Restart=always
RestartSec=5
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
"""

    def install(self):
        """Installs the systemd service."""
        try:
            self._check_prerequisites()

            content = self.generate_content()
            logger.info(f"Generating service file for user '{self.user}' in '{self.project_root}'...")

            # Write to a temporary file first
            temp_path = Path("/tmp") / self.SERVICE_NAME
            with open(temp_path, "w") as f:
                f.write(content)

            # Move to /etc/systemd/system/ using sudo
            logger.info("Installing service file (requires sudo)...")
            self._run_command(["sudo", "mv", str(temp_path), self.SERVICE_PATH])
            self._run_command(["sudo", "chown", "root:root", self.SERVICE_PATH])
            self._run_command(["sudo", "chmod", "644", self.SERVICE_PATH])

            # Reload and enable
            logger.info("Reloading systemd daemon...")
            self._run_command(["sudo", "systemctl", "daemon-reload"])
            
            logger.info("Enabling service...")
            self._run_command(["sudo", "systemctl", "enable", self.SERVICE_NAME])

            logger.info(f"✅ Service {self.SERVICE_NAME} installed and enabled successfully!")
            logger.info("To start it now, run: sudo systemctl start ninjarobot")

        except Exception as e:
            logger.error(f"Installation failed: {e}")
            sys.exit(1)

    def remove(self):
        """Removes the systemd service."""
        try:
            if not os.path.exists(self.SERVICE_PATH):
                logger.warning(f"Service file {self.SERVICE_PATH} does not exist.")
                return

            logger.info("Stopping service (requires sudo)...")
            self._run_command(["sudo", "systemctl", "stop", self.SERVICE_NAME], check=False)

            logger.info("Disabling service...")
            self._run_command(["sudo", "systemctl", "disable", self.SERVICE_NAME], check=False)

            logger.info("Removing service file...")
            self._run_command(["sudo", "rm", self.SERVICE_PATH])

            logger.info("Reloading systemd daemon...")
            self._run_command(["sudo", "systemctl", "daemon-reload"])

            logger.info(f"✅ Service {self.SERVICE_NAME} removed successfully.")

        except Exception as e:
            logger.error(f"Removal failed: {e}")
            sys.exit(1)

    def status(self):
        """Checks the status of the service."""
        try:
            subprocess.run(["systemctl", "status", self.SERVICE_NAME], text=True)
            # systemctl status returns non-zero if service is not running, which is fine for status check
        except FileNotFoundError:
            logger.error("systemctl command not found.")
