#!/usr/bin/env bash
set -euo pipefail

finish_install() {
  local result=$?
  if ((result)); then
    printf '\nInstallation stopped during: %s (exit %s).\n' "${INSTALL_STAGE:-setup}" "$result" >&2
    printf 'Read the error above. After resolving it, retry from the same checkout:\n  cd -- %q && ./install.sh\n' "$INSTALL_ROOT" >&2
    echo 'Keep your configuration/calibration files. --check only inspects; it does not repair.' >&2
  fi
  [[ -z "${INSTALL_WORK:-}" ]] || rm -rf -- "$INSTALL_WORK"
  rmdir -- "$INSTALL_LOCK" 2>/dev/null || true
  return "$result"
}

install_stage() {
  INSTALL_STAGE="$1"
  printf '\n== %s ==\n' "$INSTALL_STAGE"
}

main() {
  local root tools work="" check=0 preview=0 yes=0 wiki=0 answer item
  root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
  # shellcheck source=install-versions.env
  source "$root/scripts/install-versions.env"
  tools="${HOME}/.local/share/ninjarobot_pi0/tools"
  while (($#)); do
    case "$1" in
      --check) check=1 ;; --dry-run) preview=1 ;; --yes) yes=1 ;; --with-wiki) wiki=1 ;;
      --help|-h)
        echo 'Usage: ./install.sh [--yes] [--with-wiki] [--dry-run | --check]'
        echo 'Bookworm/Trixie 64-bit Zero 2 W software only. Run ./onboard.sh afterward.'
        echo '--check reports status only; run ./install.sh without flags to install or retry.'; return ;;
      *) echo "Unknown/local-checkout-inapplicable option: $1" >&2; return 2 ;;
    esac
    shift
  done
  (( !(check && preview) )) || return 2
  # Always own the checkout environment; do not inherit a developer venv override.
  unset VIRTUAL_ENV UV_PROJECT_ENVIRONMENT UV_PROJECT
  export PATH="$tools/uv:$tools/node/bin:$PATH"
  if ((check)); then python3 -B "$root/scripts/install_check.py" --root "$root"; return; fi
  cat <<EOF
NinjaRobotPi0 software installation:
  checkout: $root (existing files and Git revision retained)
  uv $UV_VERSION, Node $NODE_VERSION, pigpio commit $PIGPIO_COMMIT
  apt: build-essential ca-certificates curl git python3-dev python3-venv xz-utils bluez dbus
  privileged files: pigpiod /usr/local/bin, library /usr/local/lib, optional inactive systemd unit
  Python: locked production .venv; frontend: npm ci and build
  wiki environment: $wiki (0=skip, 1=explicit setup)
No hardware/service activation, calibration, credentials, robot start, or reboot.
EOF
  ((preview)) && return
  python3 -B "$root/scripts/install_check.py" --platform
  for item in pigpiod ninjarobot; do
    if systemctl is-active --quiet "$item"; then echo "Stop $item in a controlled maintenance session first." >&2; return 1; fi
  done
  if ((!yes)); then
    printf 'Type INSTALL to accept these exact system/software changes: ' > /dev/tty
    read -r answer < /dev/tty || return 1
    [[ "$answer" == INSTALL ]] || return 1
  fi
  mkdir -- "$root/.ninjarobot-install.lock" || { echo 'Installation lock exists; review any interrupted run.' >&2; return 1; }
  work="$(mktemp -d)"
  INSTALL_WORK="$work"; INSTALL_LOCK="$root/.ninjarobot-install.lock"; INSTALL_ROOT="$root"
  trap finish_install EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  install_stage "OS prerequisites"
  sudo python3 -B "$root/scripts/install_system.py"
  [[ ! -L "$tools" && ! -L "$root/.venv" ]] || { echo "Refusing redirected tools/environment." >&2; return 1; }
  mkdir -p -- "$tools"
  download() { curl --fail --location --silent --show-error --retry 2 --connect-timeout 20 "$1" -o "$2"; }
  verify() { printf '%s  %s\n' "$2" "$1" | sha256sum --check --status || { echo 'Artifact checksum mismatch.' >&2; return 1; }; }
  install_stage "Pinned uv tooling"
  if [[ ! -x "$tools/uv/uv" ]] || [[ "$("$tools/uv/uv" --version)" != "uv $UV_VERSION"* ]]; then
    download "https://astral.sh/uv/$UV_VERSION/install.sh" "$work/uv.sh"
    verify "$work/uv.sh" "$UV_INSTALLER_SHA256"
    UV_INSTALL_DIR="$tools/uv" UV_NO_MODIFY_PATH=1 sh "$work/uv.sh"
  fi
  install_stage "Pinned Node tooling"
  if [[ ! -x "$tools/node/bin/node" ]] || [[ "$("$tools/node/bin/node" --version)" != "v$NODE_VERSION" ]]; then
    [[ ! -e "$tools/node" && ! -L "$tools/node" ]] || { echo 'Existing Node tool directory has a different version; preserve and review it.' >&2; return 1; }
    download "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-arm64.tar.xz" "$work/node.tar.xz"
    verify "$work/node.tar.xz" "$NODE_ARM64_SHA256"
    tar -xJf "$work/node.tar.xz" -C "$work"
    mv -- "$work/node-v$NODE_VERSION-linux-arm64" "$tools/node"
  fi
  install_stage "pigpio daemon and inactive service"
  if ! command -v pigpiod >/dev/null; then
    download "https://codeload.github.com/joan2937/pigpio/tar.gz/$PIGPIO_COMMIT" "$work/pigpio.tar.gz"
    verify "$work/pigpio.tar.gz" "$PIGPIO_SHA256"
    tar -xzf "$work/pigpio.tar.gz" -C "$work"
    (cd "$work/pigpio-$PIGPIO_COMMIT"; make -j1 pigpiod)
    sudo install -m 0755 "$work/pigpio-$PIGPIO_COMMIT/pigpiod" /usr/local/bin/pigpiod
    sudo install -m 0755 "$work/pigpio-$PIGPIO_COMMIT/libpigpio.so.1" /usr/local/lib/libpigpio.so.1
    sudo ldconfig
  fi
  [[ "$(pigpiod -v)" == 79 ]] || { echo 'Existing pigpiod version differs; preserve it and review.' >&2; return 1; }
  if ! systemctl cat pigpiod.service >/dev/null 2>&1; then
    cat > "$work/pigpiod.service" <<EOF
[Unit]
Description=Pi0 localhost pigpio daemon (manual activation)
After=network.target
[Service]
Type=simple
ExecStart=$(command -v pigpiod) -g -l
[Install]
WantedBy=multi-user.target
EOF
    sudo install -m 0644 "$work/pigpiod.service" /etc/systemd/system/pigpiod.service
    sudo systemctl daemon-reload
  fi
  install_stage "Locked Python environment (.venv)"
  (cd "$root"; uv sync --locked --no-dev --python /usr/bin/python3)
  install_stage "Frontend dependencies and build"
  (cd "$root/ninja_webapp"; npm ci --include=dev --no-audit --no-fund; npm run build)
  install_stage "Optional wiki setup"
  if ((wiki)); then python3 -B "$root/scripts/wiki.py" setup; python3 -B "$root/scripts/wiki.py" prepare; fi
  install_stage "Final software verification"
  python3 -B "$root/scripts/install_check.py" --root "$root"
  python3 -B "$root/scripts/install_record.py" "$root"
  rm -rf -- "$work"; work=""; rmdir -- "$root/.ninjarobot-install.lock"; trap - EXIT INT TERM
  echo 'Software installed. Hardware setup remains pending. Next: ./onboard.sh'
}

main "$@"
