import click
from .service_manager import ServiceManager

@click.group()
def main():
    """NinjaRobot Utility Tools"""
    pass

@main.command()
def install_startup():
    """Install the automatic startup service (systemd)."""
    manager = ServiceManager()
    manager.install()

@main.command()
def remove_startup():
    """Remove the automatic startup service."""
    manager = ServiceManager()
    manager.remove()

@main.command()
def status_startup():
    """Check the status of the startup service."""
    manager = ServiceManager()
    manager.status()

if __name__ == "__main__":
    main()
