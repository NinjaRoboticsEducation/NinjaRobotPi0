"""Compatibility gate. Registered sources are now immutable versions."""
import subprocess
import sys
from pathlib import Path

if "--sync" in sys.argv:
    print("Overwrite sync retired. Create/register a NEW manual version and review its semantic plan.", file=sys.stderr)
    raise SystemExit(2)
root = Path(__file__).resolve().parents[4]
raise SystemExit(subprocess.call([sys.executable, "-B", str(root / "scripts/wiki.py"), "check"]))
