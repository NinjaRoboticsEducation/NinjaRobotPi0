"""Inert installer checks: never downloads or executes Ollama."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ollama_install", ROOT / "scripts/install_ollama.py"
)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def test_version_without_daemon():
    def run(args, **kwargs):
        assert args == ["/inert/ollama", "--version"]
        return SimpleNamespace(
            returncode=0,
            stdout="",
            stderr="Warning: could not connect to server\nWarning: client version is 0.40.2\n",
        )

    assert installer.version_of("/inert/ollama", run=run) == (0, 40, 2)


def test_reuse_compatible_cli(monkeypatch, tmp_path):
    monkeypatch.setattr(installer.shutil, "which", lambda command: "/inert/ollama")
    monkeypatch.setattr(installer, "version_of", lambda *a: (0, 40, 2))
    assert installer.install(tmp_path) == Path("/inert/ollama")
    assert not tmp_path.joinpath(".local").exists()


def test_low_disk_fails_before_download(monkeypatch, tmp_path):
    monkeypatch.setattr(installer.shutil, "which", lambda command: None)
    monkeypatch.setattr(
        installer.shutil, "disk_usage", lambda path: SimpleNamespace(free=100)
    )
    with pytest.raises(ValueError, match="2 GB"):
        installer.install(tmp_path)


def test_private_path_redirect_rejected(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    (tmp_path / ".local").symlink_to(target)
    with pytest.raises(ValueError, match="redirected"):
        installer.install(tmp_path)


def test_pin_matches_manifest():
    values = dict(
        line.split("=", 1)
        for line in (ROOT / "scripts/install-versions.env").read_text().splitlines()
        if line.startswith("OLLAMA_")
    )
    assert values["OLLAMA_VERSION"] == installer.VERSION
    assert values["OLLAMA_ARM64_SHA256"] == installer.SHA256
    assert len(installer.SHA256) == 64
    source = (ROOT / "scripts/install_ollama.py").read_text()
    for forbidden in ('"serve"', '"pull"', '"signin"', '"run"', '"systemctl"'):
        assert forbidden not in source
