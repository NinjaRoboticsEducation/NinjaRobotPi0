"""Install only the verified ARM64 CLI; no daemon, libraries or model downloads."""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

VERSION = "0.40.2"
SHA256 = "92b3ef3d5e10f5849273bfa1345000f2a8ce8bc834e95061ff5b9df5d08e3c3f"
URL = f"https://github.com/ollama/ollama/releases/download/v{VERSION}/ollama-linux-arm64.tar.zst"


def version_of(binary, run=subprocess.run):
    try:
        result = run(
            [str(binary), "--version"], capture_output=True, text=True, timeout=20
        )
        # --version may warn about the absent daemon. No daemon is needed by this CLI install.
        match = re.search(
            r"(?:version is|version)\s+(\d+)\.(\d+)\.(\d+)",
            result.stdout + result.stderr,
        )
        if result.returncode == 0 and match:
            return tuple(map(int, match.groups()))
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def check_path(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Refusing redirected Ollama installation")


def install(home=Path.home()):
    directory = home / ".local/share/ninjarobot_pi0/tools/ollama"
    binary = directory / "bin/ollama"
    check_path(directory)
    existing = shutil.which("ollama")
    if existing and (version_of(existing) or (0,)) >= (0, 12, 0):
        return Path(existing)
    if existing:
        raise ValueError(
            "Existing Ollama CLI is incompatible; preserve and repair it before retrying"
        )
    if binary.exists():
        if (version_of(binary) or (0,)) >= (0, 12, 0):
            ensure_launcher(binary)
            return binary
        raise ValueError(
            "Existing private Ollama CLI incompatible; preserve and repair it"
        )
    directory.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(directory.parent).free < 2_000_000_000:
        raise ValueError(
            "At least 2 GB free temporary disk space required for the official ARM64 archive"
        )
    if not shutil.which("zstd"):
        raise ValueError("zstd is required to extract the official Ollama archive")
    with tempfile.TemporaryDirectory(
        prefix=".ollama-", dir=directory.parent
    ) as temporary:
        stage = Path(temporary)
        archive = stage / "arm64.tar.zst"
        subprocess.run(
            [
                "curl",
                "--fail",
                "--location",
                "--proto",
                "=https",
                "--tlsv1.2",
                "--connect-timeout",
                "20",
                "--max-time",
                "1800",
                URL,
                "-o",
                str(archive),
            ],
            check=True,
        )
        with archive.open("rb") as stream:
            digest = (
                hashlib.file_digest(stream, "sha256").hexdigest()
                if hasattr(hashlib, "file_digest")
                else _digest(stream)
            )
        if digest != SHA256:
            raise ValueError("Ollama artifact checksum mismatch")
        (stage / "publish/bin").mkdir(parents=True)
        candidate = stage / "publish/bin/ollama"
        # Emit exactly one reviewed archive member to a regular file. Archive paths cannot escape.
        with candidate.open("wb") as output:
            subprocess.run(
                [
                    "tar",
                    "--use-compress-program=zstd",
                    "-xOf",
                    str(archive),
                    "bin/ollama",
                ],
                stdout=output,
                check=True,
            )
        candidate.chmod(0o755)
        with candidate.open("rb") as stream:
            header = stream.read(20)
        if header[:5] != b"\x7fELF\x02" or header[18:20] != b"\xb7\x00":
            raise ValueError("Ollama CLI is not Linux ARM64")
        if version_of(candidate) != tuple(map(int, VERSION.split("."))):
            raise ValueError("Pinned Ollama CLI did not report the expected version")
        # Cooperative installer lock is already held; preserve an independently created destination.
        if directory.exists():
            raise ValueError("Ollama installation destination changed")
        os.rename(stage / "publish", directory)
    ensure_launcher(binary)
    return binary


def ensure_launcher(binary):
    launcher = Path("/usr/local/bin/ollama")
    if launcher.is_symlink() and launcher.resolve() == binary.resolve():
        return
    if launcher.exists() or launcher.is_symlink():
        raise ValueError("Existing Ollama launcher retained; resolve PATH conflict")
    subprocess.run(["sudo", "ln", "-s", str(binary), str(launcher)], check=True)


def _digest(stream):
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        binary = shutil.which("ollama") or str(
            Path.home() / ".local/share/ninjarobot_pi0/tools/ollama/bin/ollama"
        )
        if (version_of(binary) or (0,)) < (0, 12, 0):
            raise SystemExit(
                "Compatible Ollama CLI missing (run ./install.sh to install)"
            )
        print(f"Ollama CLI available: {binary}; cloud inference needs no local service")
    else:
        print(install())
