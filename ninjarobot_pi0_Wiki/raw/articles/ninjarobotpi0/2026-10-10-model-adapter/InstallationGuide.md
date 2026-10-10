# NinjaRobotPi0 installation and onboarding

## CLI launcher recovery — 2026-10-10

Current packaging delegates the five existing robot console commands exclusively to ninja_core/pi0servo/pi0disp/pi0buzzer/pi0vl53l0x. The root distribution remains ninjarobotpi0 but no longer duplicates those entry points. Installed root/provider RECORD files previously claimed the same launcher paths. Following the root rename, all five launchers were missing although their packages remained installed; normal sync did not repair them. The collision is confirmed. No prior transaction log establishes the exact deletion timing, so the rename-triggered removal is a grounded inference.

For an existing checkout containing this fix, use the normal user in a controlled maintenance session. Do not delete config/calibration or .venv. If another checkout is in use, publish the fix first, inspect git status and fast-forward its intended tracking branch; stop on errors and preserve local edits. Actual Python repair requires owner authorization and is distinct from diagnosis:

```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev \
  --reinstall-package ninja-core --reinstall-package pi0servo \
  --reinstall-package pi0disp --reinstall-package pi0buzzer \
  --reinstall-package pi0vl53l0x
uv run --no-sync ninja_core --help
./install.sh --check
```

This rebuilds changed root metadata plus the five local providers, preserving locked dependency versions and extra/development packages via --inexact. It does not start hardware or change system packages/services. Missing interpreter/dependencies instead require completing the full installer after its dry-run. The full installer now forces locked provider reinstallation and checks all five executable paths; uv must support --reinstall-package. Normal uv run may sync packages, while --no-sync uses an already repaired environment without synchronization.

Only after CLI help and software checks succeed AND physical readiness is confirmed may the owner start uv run --no-sync ninja_core server or .venv/bin/ninja_core server. This can initialize/center hardware and open ngrok; shutdown may execute Poweroff. No server/device tool was started for this repair. Direct module help passed without the launcher. 105 focused tests passed; full root regression passed 331 tests (exit 0)/1 intentionally excluded protected-baseline test with 31 existing dbus_next deprecation warnings. Ruff, shell syntax, offline lock check and installer/repair dry-runs passed. Real environment repair/repaired-launcher help remain pending owner approval; no package installation in the actual environment is claimed.

This is a complete English-only candidate derived from the preceding full 2026-10-10 lifecycle manual. Prior translated sections are not copied into this new version, and all original versions remain untouched. Historical sections below retain their dated status; this recovery section governs the current CLI behavior. Wiki registration/ingestion/review and current-pointer updates remain owner-deferred.

See [repair plan](../../../../../docs/CLIEntryPointRepairPlan.md) and [validation](../../../../../docs/validation/CLIEntryPoints-2026-10-10.md).


## Lifecycle refinements — 2026-10-10

This complete new version is raw evidence for owner manual validation and later ingestion/review. The owner reports the preceding built-in feature was ingested and semantically reviewed. This version does not change registered sources, curated pages, current pointers or review records. Earlier dated sections retain their historical validation status; the current lifecycle behavior below supersedes their exit/reconnect/prompt descriptions.

Movement-tool option 6 deliberately executes configured Poweroff before HAL shutdown and configuration save, without subsequent centering. If Poweroff is absent, configured home is attempted (the Wheel/Humanoid default). Invalid/incompatible/missing poses are logged and refused; cleanup/save still run. Keyboard interrupts and initialization failures do not request extra recovery motion. Startup still centers servos. Poweroff can command extreme Spider targets; physical clearance and power readiness are required. HAL shutdown releases PWM rather than electrically holding the final pose.

The shared Home/Agent/Help layout maintains /ws/session with a server-issued HttpOnly ninja_web_session cookie. One browser identity owns web controls; same-cookie tabs share ownership. A second browser gets busy/4409 and cannot access APIs or auxiliary sockets. Existing API paths/payloads and distance/events messages remain, but every /api/ request and /ws/distance or /ws/events socket now requires the live primary session. Inactive API requests return 423; requests during shutdown return 503. Scripted REST clients must get the cookie from HTML and keep /ws/session open. This is ownership, not login authentication; BLE is unchanged and remains a separate protocol.

Clients ping every 10 seconds, server timeout is 35 seconds without input, and browser retry is every 3 seconds. Final disconnect cancels pending browser requests/greetings, aborts ongoing native/Blockly work, stops output and restores the saved ngrok URL QR, falling back to reachable LAN URL if tunneling failed. No reachable URL means no QR. RuntimePipeline suppresses automatic idle painting while waiting. Startup QR and session cleanup/handoff are serialized; blocking ngrok/QR/display work runs off the asyncio thread. The QR remains square on rectangular displays. Missing/failing displays cannot retain ownership. Shutdown skips QR cleanup to preserve Poweroff. Cookie plus connection-generation context prevents old threads from regaining access after the same browser reconnects; centering receives an optional lifecycle abort callback checked inside the controller motion lock. Abort is cooperative, not an instantaneous hardware safety guarantee.

Root distribution/lock identity and the default virtual environment prompt are ninjarobotpi0. The directory remains .venv. Installer runs uv venv --allow-existing --prompt ninjarobotpi0 --python /usr/bin/python3 .venv before locked production sync, without --clear. uv compatibility now includes venv --allow-existing/--prompt/--python. Dependency versions are unchanged. Existing local activation scripts/pyvenv.cfg were mechanically updated without installation; re-activate an existing shell to see the new prompt.

Executed software checks: 72 inert movement/session/runtime tests and 93 installer/upgrade tests passed. Full root regression passed 319 tests, with one intentionally changed protected-baseline test excluded and 31 existing dbus_next deprecation warnings (exit 0). Focused Ruff, frontend lint/production build, shell syntax, offline lock check, install dry-run, prompt activation, Node hook harness and documentation links passed. Initial installer fixture failures were corrected by preventing host Node selection from bypassing mocked systemctl; no running service was stopped. Generated frontend assets were rebuilt. Protected-core and wiki-mapping gates intentionally remain drifted; no hashes are refreshed. No actual servo/display/network service acceptance or new semantic review is claimed.




See [implementation plan](../../../../../docs/LifecycleRefinementsImplementationPlan.md) and [validation report](../../../../../docs/validation/LifecycleRefinements-2026-10-10.md).


## Automatic built-in movements — 2026-10-09

This complete new manual version is staged raw evidence for the owner's later manual validation and wiki ingestion/review. Current registered originals, curated pages, pointers and source maps remain unchanged.

After physical calibration, use `.venv/bin/ninja_core config set-type spider` (or wheel/humanoid) and `.venv/bin/ninja_core config import`. These commands modify configuration only. Wheel is an alias for the existing stored type tire. Spider with all GPIO20–27 configured receives 19 spider_* waypoint movements plus the proposal's exact Poweroff. Wheel and Humanoid receive only home, returning every configured servo to zero at Slow speed as confirmed by the owner; other default movements are deferred.

Reimport preserves custom collisions and edits. Type/channel changes remove only unchanged managed entries; incompatible edits remain stored and are hidden/rejected at execution. Generated default calibration is not physical calibration. HAL selects configured channel identities but reads physical calibration from servo.json. Restart a running runtime deliberately after config changes. Do not publish private config contents.

After readiness, choose movement-tool option 4, the web Agent movement dropdown, or an exact advertised movement name through Ninja agent. Opening tools/starting the server can energize hardware. Support the robot and verify GPIO/joint identity, direction, calibrated pulse/angle limits, clearance and external servo power/common ground before motion. Poweroff can execute extreme ±90° targets during Spider server shutdown/SIGINT. Sampled waypoints do not preserve OTTO timing, pauses, balance or measured travel. Host tests do not establish physical acceptance; all Pi movement tests remain pending.




## Current supported setup

Raspberry Pi Zero 2 W, Debian-based Raspberry Pi OS 64-bit only. Real-device acceptance is
pending the owner's manual check. Keep the robot disconnected from actuator power during
software installation. Installer software checks do not certify wiring or calibration.



## Software compatibility policy

The installer checks capabilities, not exact OS/Node/uv release equality:

- Raspberry Pi Zero 2 W, Linux `aarch64`, Debian-based Raspberry Pi OS (`ID=debian`
  or `raspbian`), and a normal user are required. No release-codename allowlist remains.
  Bookworm and Trixie are the reference targets; other releases are not automatically
  hardware-qualified merely because they pass preflight.
- Python 3.10+ is needed by existing runtime annotations (for example `ninja_core/config.py`
  and `pi0servo/core/servo.py`). Optional wiki development requires Python 3.11+.
  Existing metadata still says >=3.9; this installer check reflects the stricter runtime
  requirement without changing the robot packages. Locked dependencies remain authoritative.
- Node 20.19+ within 20.x, or Node >=22.12.0, matches the committed Vite 7/plugin engines.
  Node 24.21.0 qualifies. npm must be executable; `npm ci` and the build still have to succeed.
- uv has no exact-version gate. Its `sync --help` must expose `--locked`, `--no-dev`,
  `--python`, `--directory`, and `--all-extras`; its `venv --help` must expose `--allow-existing`, `--prompt`, and `--python`. uv 0.9.26 satisfies this and passed an
  offline host `sync --locked --no-dev --dry-run` against the existing lockfile.
  The capability probe alone does not certify every future uv version; real locked sync
  must succeed, with its original error preserved if it fails.
- Compatible tools on PATH are reused before compatible private tools. Missing/incompatible
  tools use checksum-verified fallback downloads. Download pins are not installed-version
  requirements. System tools and calibration files are retained. The existing pigpio daemon
  qualification remains separate and unchanged.

`./install.sh --check` stays read-only. Missing `.venv/bin/python` or `.venv/bin/ninja_core`
still means installation is incomplete: run `./install.sh`, wait for **Software installed**,
then run `./install.sh --check`. Publish/fetch this change before retrying on the Pi.
No physical Pi, hardware, account, or network-service acceptance is implied by host checks.



## Install software

From a clone of the approved revision:

```bash
./install.sh --dry-run
./install.sh
./install.sh --check
```

Run as the normal user, not `sudo ./install.sh`. The installer displays its privileged operations;
apt installs prerequisites; compatible Node/uv are reused, with hash-checked fallbacks if needed.
The existing pinned pigpio build remains unchanged.
Python uses the existing lockfile in `.venv`; frontend uses `npm ci` and build. It does not
start pigpiod, Bluetooth robot services, calibration, server, boot startup, or reboot.
Existing custom system policy/services are preserved or installation stops for review.
Use `--with-wiki` only to explicitly install the independent developer wiki environment.

After this revision has been published to the official repository, the default-branch command is:

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

The raw endpoint is not ready until the implementation is pushed. A branch-following command
is mutable; to select an immutable published commit, use the same full SHA in the raw URL and
`--ref FULL_SHA`. For inspection, download to a file first with curl, inspect it, then run Bash
only if the download succeeded. `--install-dir` requires a new absolute destination. Existing
checkouts are installed as-is; retry locally after fixing a failed stage. Preview itself performs
no network or writes, although downloading the script necessarily uses the network.



## Recover an incomplete installation

`--check` is a read-only inspection, not installation. Missing `.venv/bin/python` or
`.venv/bin/ninja_core` means the project environment is incomplete or broken. A Node/uv
compatibility failure identifies an actual build requirement or missing uv command capability.
Compatible system/user tools are reused; do not uninstall them. Exact Node/uv version equality
is no longer required. Missing project Python/CLI still requires completing installation.

If the project folder already exists on your Pi, open its terminal and follow these steps.
Replace `$HOME/NinjaRobotPi0` if you chose a different installation directory.

1. After the maintainer publishes the corrected files, download them into the existing Git
   checkout using a fast-forward update. This also works with the detached checkout created
   by the curl bootstrap and follows the remote default branch rather than assuming `main`:

   ```bash
   cd "$HOME/NinjaRobotPi0" &&
     git fetch origin HEAD &&
     git merge --ff-only FETCH_HEAD
   ```

   If Git reports an error, conflict or that a fast-forward is impossible, stop and retain
   the message. Do not use `git reset --hard`, delete calibration, or replace the folder.

2. Run the actual software installer from that folder as your normal user:

   ```bash
   ./install.sh
   ```

   Read the plan and type `INSTALL` when prompted. Enter your sudo password only when asked.
   Wait until it prints **Software installed**. This reuses compatible tools or installs fallback tools and the locked
   Python environment, then builds the web interface. Running `--check` alone does none of this.
   An already-current checkout can run this step immediately without another Git update.

3. Verify completion:

   ```bash
   ./install.sh --check
   ```

   Expect PASS. On failure, the updated checker prints required/detected versions, executable
   paths, missing components and the exact local install command. If installation itself
   stops, retain the first error and the **Installation stopped during** line; resolve that
   failure and rerun `./install.sh`. No server or hardware tool starts as part of this process.

4. Preview initialization before performing the separately documented hardware preparation:

   ```bash
   ./onboard.sh --dry-run
   ```

If no project folder exists, use the curl command in the install section instead. Do not
rerun bootstrap into an existing directory to overwrite it; the installer prints a local
retry command and preserves the directory. Neither a local install nor a check updates Git
files automatically. These diagnostic improvements require publication before a Pi fetch can get them.





```bash
./onboard.sh
./onboard.sh --resume
./onboard.sh --step servo
./onboard.sh --status
./onboard.sh --dry-run
```

A real terminal is required. Steps offer open tool, reuse valid saved settings, or save and exit.
Before calibration, stop the robot server deliberately and check I2C/SPI/pigpiod prerequisites.
Activate pigpiod only when ready for GPIO initialization: `sudo systemctl start pigpiod`.
The wizard does not enable boot startup or restart the robot for you.

| Step | Existing tool/settings | Operator check |
| --- | --- | --- |
| Display | `pi0disp display-tool`; saves `pi0disp/display.json` | Verify wiring, rotation, brightness, readable text |
| Buzzer | `pi0buzzer buzzer-tool`; saves root `buzzer.json` | Initialization can sound; confirm pin and silence afterward |
| Servos | `pi0servo servo-tool`; saves root `servo.json` | Opening the tool can center saved servos immediately. Support all limbs/wheels, clear travel and be ready to remove power before READY |
| Distance | `pi0vl53l0x sensor-tool`; retains package-local config file | Use a measured flat target and inspect readings; save the offset through the tool |
| Import | Existing core hardware import | Requires validated display/buzzer/servo files; default-created calibration is not successful calibration. Sensor settings remain separate |
| Identity | Existing name/type setters | Retain or select tire/humanoid/spider and an appropriate robot name |
| Google Gemini | Existing key/model discovery and validation | Hidden key entry; model check uses network. Failure/cancel retains prior robot settings |
| ngrok | Existing pyngrok token storage | Hidden token entry; binary download may be needed. No tunnel is opened and token presence is not account verification |

Progress is private under `~/.local/state/ninjarobot_pi0/` (or XDG_STATE_HOME). It stores no keys,
tokens or full robot configs. Status reads existing files without creating default robot settings.
Reusing a valid file is software validation, not a claim that the hardware was physically checked.
A tool exiting with code zero is insufficient without valid saved settings. Cancel normally to
allow the existing device tool to clean up; if cleanup is uncertain, remove actuator power.



## 2026-10-08 — reviewed onboarding and first-operation clarification

Onboarding follows Pi5's branded welcome, numbered steps, What/Why/What-to-do guidance,
bulk reuse of valid saved hardware settings, per-module reuse, retry, Enter-to-continue and
readable summary. Q saves and exits. `--resume` skips only unchanged valid completed hardware;
changed or missing files clear prior operator observations. Accounts remain available on resume
and are not automatically revalidated. Invalid saved progress is rejected without overwriting it.
Credential helpers run with a private umask from the first write; failures retain prior settings.
Conflicting legacy servo pulse aliases and noncanonical numeric GPIO keys block import/reuse.
The saved-file hash describes the same bytes that passed validation.

The installer reuses compatible uv/Node or downloads private fallback tools; run `.venv/bin/ninja_core server` from the project root
rather than assuming uv is on the login PATH. This is a separate deliberate action: the existing
server initializes hardware, may center servos and attempts ngrok connections. With an existing
token, press Enter at its prompt to keep the token already entered privately through onboarding.
Skipping ngrok in onboarding is not a network-isolation mode. The Pi0 runtime does not implement
Pi5 pairing/authentication; use trusted networks and keep public control URLs private.

Follow the root README for the full beginner walkthrough and physical acceptance checklist.
Its English manual is comprehensive; Japanese, Traditional and Simplified Chinese sections are
explicitly labelled summaries. Root InstallationGuide/DevelopmentGuide/DevelopmentLog remain
compatibility links to full immutable wiki versions. Public curl use awaits repository publication.




The Pi0 Home, Agent and Help pages use the Pi5 dark navy/cyan visual family. Existing chat,
browser speech input, distance in millimetres, expressions, sounds, movements and log events
keep their Pi0 contracts. The badge means BLE advertising, not controller connection.
The shutdown slider still requires its gesture and confirmation. No Pi5 camera/Game Pad or
USB voice hardware feature is added. Four existing interface languages remain supported.


## First operation and recovery

After checking wiring and calibration, start the existing server deliberately from the robot root:
`.venv/bin/ninja_core server`. This initializes devices and can center servos.
Use the existing startup tool only if you intentionally want startup on later boots; it is not
part of installation or onboarding completion. Configure interfaces/reboot manually as required
by the OS; do not add Pi5 hardware-PWM overlays to a Pi0.

Keep existing config, calibration and custom system units. On installer failure, read the failed
stage, repair prerequisites and rerun `./install.sh`; do not reset the checkout or replace user data.
An existing `/usr/sbin/policy-rc.d` causes OS installation to stop rather than overwrite admin policy.
A stale installer/onboarding lock requires confirming that no writer is running before removing it.
No automated OS-wide uninstall/rollback is provided. Preserve backups before manual system recovery.

## Detailed earlier wiring/calibration reference

The complete preceding manual is retained below as historical reference. Its software installation
commands (floating downloads, global pip and older mirror paths) are superseded by the current
installer/workflow above and must not be used as the current installation procedure.

<a id="7-hardware-calibration"></a>

<a id="8-function-testing"></a>

<a id="10-troubleshooting"></a>





<details>
<summary>Previous complete manual — historical wiring/calibration context</summary>

# NinjaRobotPi0 Complete Installation Guide

This guide will walk you through every step needed to build and run your NinjaRobotPi0 on a Raspberry Pi Zero 2W. No programming experience is required—just follow each step carefully.

> [!NOTE]
> V5 introduces a modular architecture with non-blocking drivers. All hardware now uses standardized interfaces.

---

## Table of Contents

1. [Hardware Requirements](#1-hardware-requirements)
2. [Hardware Wiring Guide](#2-hardware-wiring-guide)
3. [Raspberry Pi OS Installation](#3-raspberry-pi-os-installation)
4. [Software Installation](#4-software-installation)
5. [Service Setup (Gemini AI & ngrok)](#5-service-setup-gemini-ai--ngrok)
6. [Project Installation](#6-project-installation)
7. [Hardware Calibration](#7-hardware-calibration)
8. [Function Testing](#8-function-testing)
9. [Running the Robot](#9-running-the-robot)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Hardware Requirements

### Required Components

- **Raspberry Pi Zero 2W** (with headers soldered)
- **MicroSD Card** (16GB or larger, Class 10 recommended)
- **Power Supply** (5V 2.5A USB-C or Micro-USB)
- **8x Servo Motors** (SG90 or similar, 5V)
- **External 5V Power Supply** for servos (recommended: 5V 3A or higher)
- **ST7789V LCD Display** (240x320 pixels, SPI interface)
- **VL53L0X Distance Sensor** (Time-of-Flight, I2C interface)
- **Passive Buzzer** (3-5V)
- **Jumper Wires** (Male-to-Female and Male-to-Male)
- **Breadboard** (optional, for prototyping)
- **Keyboard, Mouse, and Monitor** (for initial setup)

### Optional but Recommended

- **Raspberry Pi Case**
- **Heatsinks** for the Raspberry Pi
- **USB Hub** (if you need multiple USB devices during setup)

---

## 2. Hardware Wiring Guide

### Important Safety Notes

> [!CAUTION]
> - **Always power off** the Raspberry Pi before connecting or disconnecting components.
> - **Never connect servo power** directly to the Raspberry Pi's 5V pin—use an external power supply.
> - **Double-check all connections** before powering on to avoid damage.

### GPIO Pin Layout

Here's the complete wiring diagram for all components:

```
Raspberry Pi Zero 2W GPIO Pinout (40-pin header)
┌─────────────────────────────────────┐
│  3.3V  [1] [2]  5V                  │
│  SDA   [3] [4]  5V                  │
│  SCL   [5] [6]  GND                 │
│  GPIO4 [7] [8]  GPIO14 (DC)         │
│  GND   [9] [10] GPIO15 (RST)        │
│  GPIO17[11] [12] GPIO18             │  ← Buzzer (17)
│  GPIO27[13] [14] GND                │
│  GPIO22[15] [16] GPIO23             │
│  3.3V [17] [18] GPIO24              │
│  SPI0 MOSI [19] [20] GND            │
│  GPIO9[21] [22] GPIO25              │
│  SPI0 SCLK [23] [24] SPI0 CE0       │
│  GND  [25] [26] SPI0 CE1            │
│  ID_SD[27] [28] ID_SC               │
│  GPIO5[29] [30] GND                 │
│  GPIO6[31] [32] GPIO12              │
│  GPIO13[33] [34] GND                │
│  GPIO19[35] [36] GPIO16 (BLK)       │
│  GPIO26[37] [38] GPIO20             │
│  GND  [39] [40] GPIO21              │
└─────────────────────────────────────┘
```

### Component Connection Table

#### Servo Motors (8 servos)

| Servo # | GPIO Pin | Signal Wire | Power (5V) | Ground |
|---------|----------|-------------|------------|--------|
| 1       | GPIO 20  | Orange/Yellow | External 5V | Common GND |
| 2       | GPIO 21  | Orange/Yellow | External 5V | Common GND |
| 3       | GPIO 22  | Orange/Yellow | External 5V | Common GND |
| 4       | GPIO 23  | Orange/Yellow | External 5V | Common GND |
| 5       | GPIO 24  | Orange/Yellow | External 5V | Common GND |
| 6       | GPIO 25  | Orange/Yellow | External 5V | Common GND |
| 7       | GPIO 26  | Orange/Yellow | External 5V | Common GND |
| 8       | GPIO 27  | Orange/Yellow | External 5V | Common GND |

> [!IMPORTANT]
> **Servo Power:** Connect all servo power wires (red) to your external 5V power supply (NOT the Raspberry Pi). Connect all servo ground wires (brown/black) to a common ground that is also connected to one of the Raspberry Pi's GND pins.

#### ST7789V LCD Display (SPI)

> [!IMPORTANT]
> The GPIO pins for DC, RST, and BLK are **configurable**. The table below shows the default wiring. After connecting, run `uv run pi0disp init` to register your pin assignments.

| Display Pin | Raspberry Pi Pin | Description |
|-------------|------------------|-------------|
| VCC         | 3.3V             | Power       |
| GND         | GND              | Ground      |
| DIN (MOSI)  | SPI0 MOSI        | SPI Data    |
| CLK (SCL)   | SPI0 SCLK        | SPI Clock   |
| CS          | SPI0 CE0         | Chip Select |
| DC          | GPIO (configurable, e.g. 14 or 18) | Data/Command |
| RST         | GPIO (configurable, e.g. 15 or 19) | Reset       |
| BLK         | GPIO (configurable, e.g. 16 or 20) | Backlight   |

#### VL53L0X Distance Sensor (I2C)

| Sensor Pin | Raspberry Pi Pin | Description |
|------------|------------------|-------------|
| VCC        | Pin 1 (3.3V)     | Power       |
| GND        | Pin 6 (GND)      | Ground      |
| SCL        | Pin 5 (GPIO 3 - I2C SCL) | I2C Clock |
| SDA        | Pin 3 (GPIO 2 - I2C SDA) | I2C Data  |

#### Passive Buzzer

| Buzzer Pin | Raspberry Pi Pin | Description |
|------------|------------------|-------------|
| Positive (+) | Pin 11 (GPIO 17) | Signal    |
| Negative (-) | GND              | Ground    |

### Wiring Checklist

Before proceeding, verify:
- [ ] All servo signal wires are connected to the correct GPIO pins (20-27)
- [ ] Servo power comes from an external 5V supply (NOT the Pi)
- [ ] Common ground is shared between Pi and external servo power supply
- [ ] Display is connected via SPI (SCLK, MOSI, CE0) and your chosen GPIO pins for DC, RST, BLK
- [ ] Distance sensor is connected via I2C (SCL, SDA)
- [ ] Buzzer is connected to GPIO 17
- [ ] No loose wires or short circuits

---

## 3. Raspberry Pi OS Installation

### Step 3.1: Download Raspberry Pi Imager

1. On your computer, go to: https://www.raspberrypi.com/software/
2. Download **Raspberry Pi Imager** for your operating system (Windows, macOS, or Linux)
3. Install and open the Raspberry Pi Imager

### Step 3.2: Flash the OS to MicroSD Card

1. Insert your MicroSD card into your computer (use an adapter if needed)
2. In Raspberry Pi Imager:
   - Click **"Choose Device"** → Select **"Raspberry Pi Zero 2W"**
   - Click **"Choose OS"** → Select **"Raspberry Pi OS (64-bit)"** (recommended) or **"Raspberry Pi OS (32-bit)"**
   - Click **"Choose Storage"** → Select your MicroSD card

3. Click the **Settings (gear icon)** button to configure:
   - **Hostname**: `ninjarobot` (or your preferred name)
   - **Enable SSH**: Check this box and select "Use password authentication"
   - **Set username and password**: 
     - Username: `pi` (or your choice)
     - Password: (create a secure password)
   - **Configure WiFi** (if you want wireless):
     - SSID: Your WiFi network name
     - Password: Your WiFi password
     - Wireless LAN country: Select your country
   - **Set locale settings**: Choose your timezone and keyboard layout

4. Click **"SAVE"** to save settings
5. Click **"WRITE"** to flash the OS to the card
6. Wait for the process to complete (this may take 5-10 minutes)
7. When done, safely eject the MicroSD card

### Step 3.3: Boot the Raspberry Pi

1. Insert the MicroSD card into your Raspberry Pi Zero 2W
2. Connect your keyboard, mouse, and monitor (via HDMI adapter)
3. Connect the power supply
4. Wait for the Pi to boot (first boot may take 2-3 minutes)
5. Log in with the username and password you set earlier

---

## 4. Software Installation

### Step 4.1: Update System

Open a terminal and run:

```bash
sudo apt update && sudo apt upgrade -y
```

This may take 10-20 minutes depending on your internet speed.

### Step 4.2: Enable Required Interfaces

1. Open the Raspberry Pi configuration tool:
   ```bash
   sudo raspi-config
   ```

2. Navigate to **"3 Interface Options"**

3. Enable the following:
   - **I2C**: Select **"I5 I2C"** → **"Yes"**
   - **SPI**: Select **"I4 SPI"** → **"Yes"**

4. Select **"Finish"** and reboot when prompted:
   ```bash
   sudo reboot
   ```

### Step 4.3: Install System Dependencies

After reboot, open a terminal and install required packages:

```bash
sudo apt install -y git pigpio python3-pip
```

*For the lastest Raspberry Pi Bookworm 64-bit OS your will encounter "Package 'pigpio' has no installation candidate" error.
You can only install pigpio from the sorce, here is the step-by-step solution:

Here is the complete, step-by-step guide to installing `pigpio` on a Raspberry Pi Zero 2 W running the latest Raspberry Pi OS (Bookworm 64-bit).

This guide is designed to navigate the specific security changes in the new OS (PEP 668) and fix the common installation errors (missing candidates, `distutils` removal, and shared library linking issues).

---

## 🛠️ Complete pigpio Installation Guide (Raspberry Pi OS Bookworm 64-bit)

**Target Hardware:** Raspberry Pi Zero 2 W 
**Target OS:** Raspberry Pi OS "Bookworm" (64-bit)

## Phase 1: System Preparation

Before starting, ensure your system package list is up-to-date and you have the necessary tools to compile software from source.

1. **Install build tools:**
We need `make` and `gcc` (included in `build-essential`) to compile the C library, and `unzip` to handle the download.
```bash
sudo apt install -y build-essential unzip wget

```



---

## Phase 2: Compile and Install the C Library

Since the `pigpio` package was removed from the standard repository in Bookworm, we must install it from the source code.

1. **Download the source code:**
```bash
wget https://github.com/joan2937/pigpio/archive/master.zip

```


2. **Unzip and enter the directory:**
```bash
unzip master.zip
cd pigpio-master

```


3. **Compile the code:**
```bash
make

```


4. **Install the library:**
```bash
sudo make install

```


> **⚠️ IMPORTANT EXPECTED ERROR:**
> You will likely see an error at the end saying:
> `ModuleNotFoundError: No module named 'distutils'`
> `make: *** [Makefile:107: install] Error 1`


> **Ignore this error.** It happens because the installer tries to install the Python bindings using an outdated method. The core C library (which is what we really need from this step) has installed successfully. We will fix the Python part in Phase 4.



---

## Phase 3: Fix Shared Library Linking

This step fixes the error: `pigpiod: error while loading shared libraries: libpigpio.so.1: cannot open shared object file`.

1. **Update the system library cache:**
The installer placed `libpigpio.so` in `/usr/local/lib`, but the OS doesn't know it's there yet. Run this command to register it:
```bash
sudo ldconfig

```



---

## Phase 4: Install the Python Library

Since the automatic Python installation failed in Phase 2, we will install the Python interface manually using a method compatible with Bookworm.

**Option A: The Recommended Method (APT)**
Try this first. It installs the pre-compiled Python wrapper provided by the OS maintainers.

```bash
sudo apt install python3-pigpio

```

**Option B: The Fallback Method (PIP)**
If Option A fails (unable to locate package), use `pip`. Note the `--break-system-packages` flag, which is required on Bookworm to allow installation outside a virtual environment.

```bash
sudo pip3 install pigpio --break-system-packages

```

---

## Phase 5: Create the System Service (Auto-start)

This step fixes the error: `Failed to enable unit: Unit pigpiod.service does not exist`.
We must manually create the configuration file to tell the system how to run the daemon in the background.

1. **Create the service file:**
```bash
sudo nano /etc/systemd/system/pigpiod.service

```


2. **Paste the following configuration:**
(Copy and paste the text below into the editor)
```ini
[Unit]
Description=Pigpio daemon
Documentation=https://github.com/joan2937/pigpio
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/pigpiod
# ExecStart=/usr/local/bin/pigpiod -l
# (Uncomment the line above with -l if you want to restrict access to localhost only)

[Install]
WantedBy=multi-user.target

```


3. **Save and Exit:**
* Press `Ctrl + O` then `Enter` to save.
* Press `Ctrl + X` to exit.


4. **Enable and Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

```



---

## Phase 6: Verification

Let's verify everything is working correctly on your Raspberry Pi Zero 2 W.

1. **Check the Daemon:**
Run the `pigs` command (pigpio command-line tool).
```bash
pigs t

```


**Success:** You should see a large number (the current microsecond timestamp).
**Failure:** If it says "socket connect failed", ensure you ran `sudo systemctl start pigpiod`.
2. **Check Python:**
Create a quick test script:
```bash
python3 -c "import pigpio; pi=pigpio.pi(); print('Connected:', pi.connected)"

```


**Success:** It should print `Connected: True`.

---

## 🧹 Cleanup (Optional)

You can now remove the source code files to save space on your SD card.

```bash
cd ~
rm -rf pigpio-master master.zip

```

**Troubleshooting Tips for Zero 2 W:**

* 
**Performance:** The Zero 2 W is powerful (Quad-core), but if you are running heavy compiles, it may get warm. Ensure it's not enclosed in a case without ventilation during the `make` process.


* **Remote Access:** If you plan to control the GPIOs remotely from a PC, remember to remove the `-l` flag in the service file created in Phase 5 to allow network connections.

Reload systemd setting
```bash
sudo systemctl daemon-reload
```


### Step 4.4: Install Python Package Manager (uv)

We use `uv` for faster and more reliable Python package management:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, close and reopen your terminal, or run:

```bash
source $HOME/.local/bin/env
```

Verify installation:

```bash
uv --version
```

You should see a version number like `uv 0.x.x`.

### Step 4.5: Start pigpio Daemon

The `pigpio` daemon must run in the background for hardware control:

```bash
sudo pigpiod
```

> [!TIP]
> To make `pigpiod` start automatically on boot, run:
> ```bash
> sudo systemctl enable pigpiod
> sudo systemctl start pigpiod
> ```

### Step 4.6: Install Node.js

The web interface (`ninja_webapp`) requires Node.js to be built. Install it using NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

Verify installation:

```bash
node -v && npm -v
```

You should see version numbers like `v20.x.x` and `10.x.x`.

---

## 5. Service Setup (Gemini AI & ngrok)

### Step 5.1: Create Google Gemini API Key

The robot uses Google's Gemini AI for natural language understanding.

1. **Go to Google AI Studio**: https://aistudio.google.com/
2. **Sign in** with your Google account
3. Click **"Get API Key"** in the left sidebar
4. Click **"Create API Key"**
5. Select **"Create API key in new project"** or choose an existing project
6. **Copy the API key** that appears (it looks like: `AIzaSy...`)
7. **Save this key** somewhere safe—you'll need it later

> [!WARNING]
> Keep your API key private! Do not share it publicly or commit it to version control.

### Step 5.2: Create ngrok Account

`ngrok` creates a public URL so you can control your robot from anywhere.

1. **Go to ngrok**: https://ngrok.com/
2. Click **"Sign up"** and create a free account
3. After signing in, go to: https://dashboard.ngrok.com/get-started/your-authtoken
4. **Copy your Authtoken** (it looks like: `2a...`)
5. **Save this token**—you'll enter it when you first start the robot's web server

---

## 6. Project Installation

### Step 6.1: Clone the Repository

Navigate to your home directory and clone the project:

```bash
cd ~
git clone https://github.com/NinjaRoboticsEducation/NinjaRobotPi0.git
cd NinjaRobotPi0
```

> [!NOTE]
> If the repository is private or you're using a different source, adjust the URL accordingly.

### Step 6.2: Create a Virtual Environment

It is best practice to install Python packages in a virtual environment to avoid conflicts.

```bash
uv venv --allow-existing --prompt ninjarobotpi0
source .venv/bin/activate
```

You should see `(ninjarobotpi0)` at the start of your terminal line. Re-activate the shell after an installer upgrade; the environment directory is still `.venv`.

### Step 6.3: Install All Dependencies

Install the project dependencies into the virtual environment using one of these methods:

**Method A: `uv sync` (Recommended)**

```bash
uv sync
```

`uv sync` automatically reads `pyproject.toml`, resolves all dependencies, and installs them into the `.venv`. This is the simplest and most reliable method.

**Method B: `uv pip install -e .` (Alternative)**

```bash
uv pip install -e .
```

This installs the project in editable (development) mode. Use this if you need more control over the installation process.

> **Difference:** `uv sync` creates/manages the `.venv` automatically and uses a lockfile for reproducible installs. `uv pip install -e .` installs into an existing virtual environment without a lockfile.

Both methods will:
- Install all Python dependencies (including `pigpio`)
- Set up all the robot's libraries in editable mode
- Make all CLI commands available (`pi0vl53l0x`, `pi0servo`, etc.)

The installation may take 5-10 minutes.

### Step 6.4: Build the Web Interface

The robot's web interface is built with React. Build it with:

```bash
cd ninja_webapp
npm install
npm run build
cd ..
```

This creates the `ninja_webapp/dist/` folder that the server will use.

> [!NOTE]
> If you see errors during `npm install`, ensure Node.js was installed correctly (Step 4.6).

### Step 6.5: Verify Installation

Check that the main command is available:

```bash
ninja_core --help
```

You should see a list of available commands like `chat`, `server`, `config`, etc.

---

## 7. Hardware Calibration & Testing

Before running the robot, you need to initialize, calibrate, and test each hardware component individually. This ensures that every component's configuration file (`display.json`, `buzzer.json`, `servo.json`) is created and verified **before** importing them all into the main `config.json`.

> [!IMPORTANT]
> Follow the steps in order. Each step creates or updates a configuration file that will be imported in Step 7.6.

### Step 7.1: Display Setup

Initialize the display by running the interactive setup wizard:

```bash
uv run pi0disp init
```

Follow the prompts to select your display profile and configure GPIO pins (DC, RST, BLK). This creates `pi0disp/display.json`.

Test the display with an image:

```bash
uv run pi0disp image assets/images/sample_face.jpg
```

You should see the image on the display. Test additional features:

```bash
# Text rendering
uv run pi0disp text "Hello NinjaRobot"

# Brightness control
uv run pi0disp brightness 50
uv run pi0disp brightness 100

# Animation demo (Ctrl+C to stop)
uv run pi0disp demo --num-balls 3

# Health check
uv run pi0disp info --health-check
```

### Step 7.2: Buzzer Setup

Tell the system which GPIO pin the buzzer is connected to. This creates `buzzer.json`:

```bash
uv run pi0buzzer init 17
```

Test the buzzer:

```bash
uv run pi0buzzer beep
uv run pi0buzzer play happy
```

You should hear a short beep, then a happy emotion sound.

### Step 7.3: Distance Sensor Test

Run the built-in self-test to verify the VL53L0X sensor is connected:

```bash
uv run pi0vl53l0x test
```

Take a few live readings:

```bash
uv run pi0vl53l0x get --count 5 --interval 1.0
```

You should see 5 distance readings in millimeters.

Check the sensor status (firmware, offset, health):

```bash
uv run pi0vl53l0x status
```

Optionally, calibrate by placing an object at a known distance (e.g., 100 mm):

```bash
uv run pi0vl53l0x calibrate --distance 100 --count 10
```

### Step 7.4: Servo Calibration

Each servo needs to be calibrated to define its minimum, center, and maximum positions. This creates `servo.json`.

For each servo (example for GPIO 20):

```bash
uv run pi0servo calib 20
```

Follow the on-screen instructions:
1. Press `v` to select **Min** position
2. Use **Up/Down** arrow keys for large adjustments, **w/s** for fine-tuning
3. When the servo is at its minimum position, press **Enter** to save
4. Press `c` to select **Center** position, adjust, and press **Enter**
5. Press `x` to select **Max** position, adjust, and press **Enter**
6. Press `q` to quit

**Repeat this for all 8 servos** (GPIO pins: 20 through 27)

Test a servo after calibration:

```bash
uv run pi0servo move 20 0
uv run pi0servo move 20 45
uv run pi0servo move 20 -- -45
```

### Step 7.5: Set Gemini API Key and Model

Configure the AI agent with your API key (replace `YOUR_API_KEY` with the actual key from Step 5.1):

```bash
uv run ninja_core config set-key gemini YOUR_API_KEY
```

NinjaRobot then retrieves the models available to this key from Google. Select one of the numbered Gemini models shown. Only models that support agent content generation are listed. NinjaRobot runs a bounded minimal generation request and saves the key/model pair only if the selected model responds. Validation can take up to 60 seconds for a thinking model. A network error, rejected key, non-responsive model, or cancelled prompt leaves the previous configuration unchanged. Gemini 3 models may take several seconds because they use thinking; NinjaRobot requests the supported low thinking level and reports a visible timeout instead of waiting indefinitely.

### Step 7.5A: Guided NinjaRobot Initialization Tool

For classroom setup, you can use the guided initializer instead of running each configuration command separately:

```bash
uv run ninja_core init-tool
```

The menu provides these actions:

1. Set Gemini API Key and Model
2. Set ngrok Token
3. Rename the Ninja Robot
4. Select NinjaRobot Type (`Tire`, `Humanoid`, or `Spider`)
5. Import All Hardware Configuration
6. Show Existing Hardware Configuration
7. Start NinjaRobot Server
8. Exit

The "Show Existing Hardware Configuration" option prints the same sanitized robot profile sent to the Code IDE over Bluetooth. It includes `robot_type` and `hardware_configuration.servos.gpio_pins`, but never prints Gemini API keys or ngrok tokens.

### Step 7.6: Import All Hardware Configurations

Now that all components are initialized and tested, import their configurations into the main `config.json`:

> [!IMPORTANT]
> This step reads from `servo.json`, `buzzer.json`, and `pi0disp/display.json`. Make sure Steps 7.1–7.4 are completed first.

```bash
uv run ninja_core config import
```

You should see:
```
Found servo config at 'servo.json'. Importing...
...imported calibration for 8 servos.
Found buzzer config at 'buzzer.json'. Importing...
...buzzer import complete.
Found display config at 'pi0disp/display.json'. Importing...
...imported display pins: DC=18, RST=19, BLK=20, rotation=90
Configuration updated and saved to config.json!
```

> [!TIP]
> If you change any hardware wiring or recalibrate a component later, run `uv run ninja_core config import` again to sync the changes.

### Step 7.7: Name Your Robot

To make Bluetooth discovery easier when you have multiple NinjaRobots nearby, save a custom BLE name:

```bash
uv run ninja_core config set-name "Classroom Ninja 1"
```

Guidelines:
- Keep the name under 29 UTF-8 bytes so it fits in BLE advertising packets.
- Use quotes if the name contains spaces.
- Restart `uv run ninja_core server` (or reboot the Raspberry Pi) after changing the name so the new Bluetooth name is advertised.

When you scan from the NinjaRoboticPlatform Code IDE or nRF Connect, look for the new name instead of the default `NinjaRobot`.

### Step 7.8: Select NinjaRobot Type

Select the robot type so the Code IDE can tailor Blockly synchronization after Bluetooth connection:

```bash
uv run ninja_core config set-type tire
uv run ninja_core config set-type humanoid
uv run ninja_core config set-type spider
```

Only one type is active at a time. The guided initializer's "Select NinjaRobot Type" option calls the same setting. Restart `uv run ninja_core server` after changing the type so the next `robot_info` profile contains the updated value.

#### Troubleshooting Bluetooth Rename and Discovery

On the Raspberry Pi, update dependencies and restart cleanly:

```bash
cd ~/NinjaRobotPi0
uv sync
sudo rfkill unblock bluetooth
sudo systemctl restart bluetooth
uv run ninja_core server
```

If it still fails, run this Pi-side diagnosis:

```bash
systemctl status bluetooth hciuart --no-pager
rfkill list bluetooth
bluetoothctl show
journalctl -u bluetooth -b --no-pager | tail -100
```

If `bluetoothctl show` has no controller or says not powered, fix the Pi Bluetooth stack first:

```bash
sudo apt update
sudo apt install -y pi-bluetooth bluez
sudo systemctl enable --now bluetooth hciuart
sudo rfkill unblock bluetooth
sudo reboot
```

---

## 8. System Integration Testing

With all components individually verified and configurations imported, test the full system.

### Test 8.1: AI Agent Test (Text Chat)

Test the AI chat in terminal mode:

```bash
uv run ninja_core chat
```

Try these commands:
- `Hello` (the robot should greet you)
- `Show me a happy face` (displays happy expression and sound)
- Type `quit` or press **Ctrl+C** to exit

> [!NOTE]
> The robot will monitor distance continuously and react if you get too close (<50mm).

---

## 9. Running the Robot

### Start the Web Server

This is the main way to interact with your robot:

```bash
uv run ninja_core server
```

On **first run**, you'll be prompted to enter your **ngrok authtoken** (from Step 5.2). Paste it and press Enter.

The robot will:
1. Initialize all hardware
2. Start the web server
3. Create a public URL via ngrok
4. Display a QR code on its screen

### Access the Web Interface

You have two options:

#### Option A: Scan the QR Code (Recommended)

Use your smartphone to scan the QR code displayed on the robot's screen. This will open the web interface in your phone's browser.

#### Option B: Local Network

On any device on the same WiFi network, open a browser and go to:
```
http://ninjarobot.local:8000
```
(Replace `ninjarobot` with your hostname if different)

### Web Interface Features

Once connected, you can:

1. **Chat with the Robot**:
   - Type messages in the text box
   - Or click the **microphone icon** and speak (select language first)
   - The robot will respond in the same language

2. **Control Servos**:
   - Select a movement from the dropdown
   - Click **Execute**

3. **Show Facial Expressions**:
   - Select an expression (happy, sad, etc.)
   - Click **Show**

4. **Play Sounds**:
   - Select an emotion sound
   - Click **Play**

5. **Monitor Distance**:
   - Real-time distance readings appear at the top

### Supported Languages

- **English** (en-US)

### Stopping the Server

Press **Ctrl+C** in the terminal to stop the server. The robot will perform a **graceful shutdown animation**:
1. Display a "sleepy" face on the LCD
2. Play a "sleepy" sound melody
3. Move servos to the "Poweroff" rest position
4. Safely shut down all hardware

---

## 10. Automatic Startup (Optional)

If you want the robot to start automatically when you turn on the power, follow these steps.

> [!IMPORTANT]
> **Prerequisites:** Ensure you have completed all previous steps, including hardware calibration and API key setup. The robot must be fully functional before enabling autostart.
>
> **Ngrok Requirement:** For autostart to work, you **must** have a valid ngrok authtoken configured. If the token is missing, the service will fail to start to avoid hanging in the background.

### Step 10.1: Install the Startup Service

Run the following command:

```bash
uv run ninja_utils install-startup
```

This will:
1. Check if your system is ready (config exists, pigpiod running, etc.)
2. Create a systemd service file
3. Enable the service to start on boot

### Step 10.2: Verify

You can check the status of the service:

```bash
uv run ninja_utils status-startup
```

### Step 10.3: Reboot

Reboot your Raspberry Pi:

```bash
sudo reboot
```

The robot should start automatically. You can access the web interface via the QR code or `http://ninjarobot.local:8000` after a minute or two.

> [!TIP]
> **Safe Shutdown:** You can safely shut down the robot using the "Power Off Robot" button at the bottom of the web interface. The robot will display a "sleepy" face, play a sound, and move to its rest position before powering off. Wait for the green light on the Raspberry Pi to stop flashing before unplugging the power.

### Removing Autostart

If you want to stop the robot from starting automatically:

```bash
uv run ninja_utils remove-startup
```

---

## 11. Troubleshooting

### Problem: "Could not connect to pigpiod daemon"

**Solution**:
```bash
sudo pigpiod
```

Then try running your command again.

### Problem: Display not working

**Checks**:
1. Verify SPI is enabled: `sudo raspi-config` → Interface Options → SPI
2. Check wiring matches the pin table in Section 2
3. Run the display health check: `uv run pi0disp info --health-check`
4. **Verify GPIO pin configuration**: Run `uv run pi0disp init` to register your display pins, then `uv run ninja_core config import` to sync them to `config.json`. A common cause of blank displays is mismatched GPIO pins between `display.json` and `config.json`.
5. Reboot: `sudo reboot`

### Problem: Distance sensor not responding

**Checks**:
1. Verify I2C is enabled: `sudo raspi-config` → Interface Options → I2C
2. Check if sensor is detected:
   ```bash
   sudo i2cdetect -y 1
   ```
   You should see `29` or `52` in the output
3. Check wiring (VCC to 3.3V, not 5V)
4. Run the built-in diagnostic:
   ```bash
   uv run pi0vl53l0x test
   uv run pi0vl53l0x status
   ```
5. If status shows errors, try power-cycling the sensor and re-running `uv run pi0vl53l0x test`

### Problem: Servos not moving

**Checks**:
1. Ensure external 5V power supply is connected and turned on
2. Verify common ground between Pi and servo power supply
3. Check servo signal wire connections
4. Recalibrate servo: `uv run pi0servo calib <PIN>`

### Problem: "ImportError" or "ModuleNotFoundError"

**Solution**:
Reinstall the project:
```bash
cd ~/NinjaRobotPi0
uv pip install -e . --force-reinstall
```

### Problem: "Component Initialization Failed" Warning

**Cause**: One hardware component (like the sensor or display) is disconnected or faulty.
**Solution**: The robot is designed to be **fault-tolerant**. It will log a warning and continue starting up with the working components. You can check connections later.

### Problem: Web server won't start

**Checks**:
1. Ensure port 8000 is not already in use
2. Check if ngrok authtoken is set correctly
3. Restart the server with verbose output:
   ```bash
   uv run ninja_core server --log-level debug
   ```

### Problem: AI agent not responding

**Checks**:
1. Verify Gemini API key is set:
   ```bash
   cat config.json | grep gemini
   ```
2. Check internet connection
3. Re-set API key:
   ```bash
   uv run ninja_core config set-key gemini YOUR_KEY
   ```

### Getting More Help

If you encounter issues not covered here:

1. Check the project's GitHub Issues page
2. Review the `DevelopmentLog.md` for known issues and fixes
3. Ensure all wiring matches the diagrams exactly
4. Try running individual component tests (Section 8) to isolate the problem

---

## Next Steps

- **Record Custom Movements**: Use `uv run ninja_core movement-tool` to create and save servo choreography
- **Customize Behavior**: Edit `config.json` to adjust settings
- **Build an Enclosure**: Design a robot body and mount all components
- **Explore the Code**: Check `ninja_core/README.md` for developer documentation

**Congratulations!** Your NinjaRobotPi0 is now ready to use. Enjoy exploring and experimenting with your AI-powered robot! 🤖

---
---




## Cloud model provider adapter (2026-10-10)

The API-key release adds Google, OpenAI, Anthropic and Ollama Cloud selection through `ninja_core config select-model`, init-tool option 1 and onboarding step 7. Read the complete [implementation source](../../../../raw/notes/ninjarobotpi0/2026-10-10-model-adapter/ModelAdapterImplementation.md) for current behavior, credentials/migration, installer resource requirements and rollback. This section supersedes earlier Google-only setup descriptions for the new release.

The updated files are prepared for owner manual validation and ingestion; canonical wiki registration/reviews and target-Pi/hardware acceptance are pending. Do not treat the previous source-grounded semantic reviews as reviews of this new version.
