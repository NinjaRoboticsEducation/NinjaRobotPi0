#!/usr/bin/env bash
# Definitions precede execution so an incomplete function definition cannot install.
set -euo pipefail

bootstrap() {
  local script="${BASH_SOURCE[0]:-}" root="" ref=HEAD destination="${HOME}/NinjaRobotPi0"
  local preview=0 check=0 yes=0 staged="" parent target branch tag
  local -a forwarded=()
  if [[ -n "$script" && -f "$script" ]]; then
    root="$(cd -- "$(dirname -- "$script")" && pwd)"
    if [[ -f "$root/uv.lock" && -f "$root/scripts/install-rpi.sh" ]]; then
      exec bash "$root/scripts/install-rpi.sh" "$@"
    fi
  fi
  while (($#)); do
    case "$1" in
      --ref|--install-dir)
        [[ $# -ge 2 && -n "$2" && "$2" != -* ]] || { echo "Missing value for $1" >&2; return 2; }
        if [[ "$1" == --ref ]]; then ref="$2"; else destination="$2"; fi
        shift 2 ;;
      --dry-run) preview=1; forwarded+=("$1"); shift ;;
      --check) check=1; forwarded+=("$1"); shift ;;
      --yes) yes=1; forwarded+=("$1"); shift ;;
      --with-wiki) forwarded+=("$1"); shift ;;
      --help|-h)
        cat <<'EOF'
NinjaRobotPi0: Raspberry Pi Zero 2 W / Raspberry Pi OS 64-bit.
Usage: install.sh [--ref REF] [--install-dir ABSOLUTE_PATH] [--yes]
                  [--with-wiki] [--dry-run | --check]
Default: remote default branch (HEAD), new $HOME/NinjaRobotPi0 checkout.
An existing checkout installs as-is; --ref/--install-dir are bootstrap-only.
Preview performs no network or writes. Check inspects an existing installation.
Installation never launches hardware, onboarding, robot services, or reboot.
EOF
        return ;;
      *) echo "Unknown option: $1" >&2; return 2 ;;
    esac
  done
  [[ "$destination" == /* ]] || { echo 'Destination must be absolute.' >&2; return 2; }
  (( !(preview && check) )) || { echo 'Choose --dry-run or --check.' >&2; return 2; }
  if ((preview)); then
    printf 'Preview: official Pi0 repository, ref %s, new checkout %s.\n' "$ref" "$destination"
    echo 'Install Git if missing, then verified uv/Node/pigpio/Ollama CLI, locked Python and frontend. Hardware remains off.'
    return
  fi
  if ((check)); then
    [[ -f "$destination/scripts/install-rpi.sh" && ! -L "$destination" ]] || { echo 'Installation not found.' >&2; return 1; }
    exec bash "$destination/scripts/install-rpi.sh" "${forwarded[@]}"
  fi
  [[ ! -e "$destination" && ! -L "$destination" ]] || { printf 'Existing destination retained. To install or retry there:\n  cd -- %q && ./install.sh\nThis does not update Git files; follow README recovery steps if this checkout is outdated.\n' "$destination" >&2; return 1; }
  parent="$(dirname -- "$destination")"
  [[ -d "$parent" && ! -L "$parent" ]] || { echo 'Destination parent must exist and be a real directory.' >&2; return 1; }
  [[ $EUID -ne 0 && "$(uname -s)" == Linux && "$(uname -m)" == aarch64 ]] || { echo 'Run as a normal user on Raspberry Pi OS 64-bit Zero 2 W.' >&2; return 3; }
  grep -aq 'Raspberry Pi Zero 2' /proc/device-tree/model || { echo 'Zero 2 W required.' >&2; return 3; }
  grep -Eq '^ID="?(debian|raspbian)"?$' /etc/os-release || { echo 'Raspberry Pi OS required.' >&2; return 3; }
  if ((!yes)); then
    local answer
    printf 'Download into %s; install Git if absent. Type INSTALL: ' "$destination" > /dev/tty
    read -r answer < /dev/tty || return 1
    [[ "$answer" == INSTALL ]] || return 1
  fi
  if ! command -v git >/dev/null; then sudo apt-get update; sudo apt-get install -y --no-install-recommends git; fi
  # Cooperative lock plus no-clobber publication protects simultaneous runs.
  local lock="${destination}.bootstrap-lock"
  mkdir -- "$lock" || { echo 'Another bootstrap is active.' >&2; return 1; }
  staged="$(mktemp -d "$parent/.ninjarobot-bootstrap.XXXXXX")"
  BOOT_STAGE="$staged"; BOOT_LOCK="$lock"
  trap 'rm -rf -- "${BOOT_STAGE:-}"; rmdir -- "$BOOT_LOCK" 2>/dev/null || true' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  git clone --quiet --no-checkout --filter=blob:none -- https://github.com/NinjaRoboticsEducation/NinjaRobotPi0.git "$staged/checkout"
  resolve() { git -C "$staged/checkout" rev-parse --verify --end-of-options "$1^{commit}" 2>/dev/null; }
  case "$ref" in
    HEAD) target="$(resolve refs/remotes/origin/HEAD)" ;;
    refs/heads/*) target="$(resolve "refs/remotes/origin/${ref#refs/heads/}")" ;;
    refs/tags/*) target="$(resolve "$ref")" ;;
    *)
      branch="$(resolve "refs/remotes/origin/$ref")" || branch=""
      tag="$(resolve "refs/tags/$ref")" || tag=""
      [[ -z "$branch" || -z "$tag" ]] || { echo 'Ambiguous branch/tag; use refs/heads/ or refs/tags/.' >&2; return 1; }
      target="${branch:-$tag}"
      if [[ -z "$target" && "$ref" =~ ^[a-fA-F0-9]{40}$ ]]; then target="$(resolve "$ref")"; fi
      [[ -n "$target" ]] || { echo 'Published ref not found.' >&2; return 1; } ;;
  esac
  git -C "$staged/checkout" checkout --quiet --detach "$target"
  local required
  for required in install.sh scripts/install-rpi.sh scripts/install-versions.env uv.lock; do
    [[ -f "$staged/checkout/$required" && ! -L "$staged/checkout/$required" ]] || { echo "Missing regular file: $required" >&2; return 1; }
  done
  [[ ! -e "$destination" && ! -L "$destination" ]] || return 1
  # GNU mv -T -n never nests inside or overwrites a newly created destination.
  mv -T -n -- "$staged/checkout" "$destination"
  [[ ! -d "$staged/checkout" ]] || { echo 'Destination changed during download.' >&2; return 1; }
  rm -rf -- "$staged"; staged=""
  rmdir -- "$lock"; trap - EXIT INT TERM
  printf 'Verified checkout %s.\n' "$target"
  bash "$destination/scripts/install-rpi.sh" "${forwarded[@]}"
}

bootstrap "$@"
