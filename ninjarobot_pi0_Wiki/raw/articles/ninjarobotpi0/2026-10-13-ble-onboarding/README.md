# English

## 1. What Is NinjaRobotPi0?

**NinjaRobotPi0** is an open-source, modular educational robot built on the **Raspberry Pi Zero 2 W** (a tiny, affordable computer about the size of a stick of gum). It brings together servo motors (for movement), an LCD display (the robot's face), a buzzer (for sounds and melodies), a distance sensor, cloud AI chat (Google, OpenAI, Anthropic or Ollama Cloud), Bluetooth Low Energy (BLE), and a browser-based control interface — all in one compact package.

Whether you want to build a tire-type car, a humanoid, or a spider robot, NinjaRobotPi0 gives you the foundation to learn how software, AI, and physical components work together.

### What can it do?

- **Move and express itself** — Use the built-in movement library to make your robot walk, wave, or dance. The LCD face shows animated expressions, and the buzzer plays emotion sounds.
- **Sense distance** — A VL53L0X laser sensor measures distances in millimetres, so your robot can detect obstacles.
- **Chat with AI** — Choose a cloud provider and connect its API key to chat with the AI. The AI can even trigger robot actions like movements and expressions.
- **Control from your phone** — Open a web browser on any device and you get a control panel with Home, Movement Tool, and Chat pages — in English, Japanese, Traditional Chinese, and Simplified Chinese.
- **Learn step by step** — Calibrate each component with guided tools, then explore the Python packages and web interface at your own pace.

### Who is this for?

Anyone who wants to build their own AI robot! Whether you are a student learning about robotics, a maker exploring hardware, or a developer who wants to extend the platform — NinjaRobotPi0 provides a starting point; each assembled robot still needs installation, wiring and calibration checks on the real device.

---

## 2. Quick Start Guide

Follow these steps to build and run your own NinjaRobotPi0 from scratch.

### 2.1 Recommended Hardware

| Component | Specification | Notes |
|---|---|---|
| **Computer** | Raspberry Pi Zero 2 W (with GPIO header) | The brain of the robot |
| **Operating System** | Raspberry Pi OS 64-bit (Bookworm or Trixie) | Debian-based, no desktop needed |
| **Storage** | microSD card, 16 GB or larger | Leave space for dependencies and frontend build |
| **Pi Power** | Regulated 5 V supply via micro-USB | Powers the Pi only |
| **Servos** | Up to 8× SG90 / MG90S micro servos | Choose servo types suitable for your mechanism; positional SG90/MG90S servos do not provide continuous wheel rotation |
| **Servo Power** | Separate 5 V 3 A+ supply for servos | Size for the servos’ combined stall current; **must not** go through the Pi’s power pins |
| **Display** | ST7789V SPI LCD, 240 × 320 pixels | The robot's face screen |
| **Distance Sensor** | VL53L0X Time-of-Flight (I2C) | Measures distance using a laser |
| **Buzzer** | Passive buzzer (3–5 V) | For sounds and melodies |
| **Setup Access** | Terminal or SSH, internet, normal user with sudo | For installation and configuration |

> **📎 Full hardware details:** See the [Installation Guide](../../../../../ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-13-humanoid-owner-defaults/InstallationGuide.md)

### 2.2 Hardware Wiring

Power off the Pi before connecting any wires. Keep servo power **disconnected** while installing software. The servo supply must **not** pass through the Pi's power pins — connect the servo power supply's ground and the Pi's ground together (common ground).

#### Pin Connections

| Component | Connection Type | Pin / Address |
|---|---|---|
| Servo signal wires (up to 8) | GPIO PWM | GPIO 20–27 (use the pins for your build) |
| ST7789V display — data | SPI0 | MOSI → GPIO 10 (Pin 19), SCLK → GPIO 11 (Pin 23), CE0 → GPIO 8 (Pin 24) |
| ST7789V display — control | GPIO (configurable) | DC → GPIO 14 (Pin 8), RST → GPIO 15 (Pin 10), Backlight → GPIO 16 (Pin 36) |
| VL53L0X distance sensor | I2C bus 1 | SDA → GPIO 2 (Pin 3), SCL → GPIO 3 (Pin 5) |
| Passive buzzer | GPIO | Signal → GPIO 17 (Pin 11), Ground → GND |

```
┌─────────────────────────────────────────┐
│         Raspberry Pi Zero 2 W           │
│                                         │
│  GPIO 20–27 ─────── Servo signals (×8)  │
│  GPIO 10,11,8 ────── ST7789V SPI data   │
│  GPIO 14,15,16 ───── ST7789V control    │
│  GPIO 2,3 ─────────── VL53L0X I2C      │
│  GPIO 17 ──────────── Buzzer signal     │
│  GND ──────────────── Common ground     │
└─────────────────────────────────────────┘
            │                    │
     Pi 5V micro-USB     Separate 5V supply
     (Pi power only)     (servo power only)
                    ↕ shared GND ↕
```

> ⚠️ **Safety:** Never change wiring while the Pi is powered on. Do not use the same GPIO pin for two components. GPIO numbers here are **BCM numbers**, not physical header positions. Pi GPIO uses **3.3 V logic**; never apply 5 V to a GPIO. Verify the module’s power/driver requirements. Display control pins are configurable — register your actual assignments during setup.

### 2.3 Raspberry Pi OS Installation

1. **Download Raspberry Pi Imager** from [raspberrypi.com/software](https://www.raspberrypi.com/software/) on your computer.
2. Insert your microSD card and open the Imager.
3. Choose **Raspberry Pi OS Lite (64-bit), Trixie (Debian 13)** for a new installation. The official image listed on 2026-10-12 is dated 2026-10-06; Bookworm is now the Legacy option. Zero 2 W supports this 64-bit image. See the [official OS downloads](https://www.raspberrypi.com/software/operating-systems/).
4. Open the Imager's **OS customisation** screen to configure:
   - Set your hostname (e.g., `ninjarobotpi0`)
   - Enable SSH (using an SSH key or password authentication)
   - Set your Wi-Fi network name and password
   - Set your username and password
5. Write the image to your microSD card and insert it into the Pi.
6. Power on the Pi and wait a few minutes for first-boot setup.
7. From your computer, connect via SSH:

   ```bash
   ssh YOUR_USERNAME@ninjarobotpi0.local
   ```

   Replace `YOUR_USERNAME` with the username you set in the Imager. If `.local` does not resolve, use the Pi's IP address instead.

8. Enable the hardware interfaces your components need:

   ```bash
   sudo raspi-config
   ```

   - Enable **I2C** (for the distance sensor)
   - Enable **SPI** (for the display)
   - If using GPIO 14/15 for the display, **disable the serial login console and the serial-port hardware assigned to those pins** so UART does not conflict with the display

   Reboot when prompted:

   ```bash
   sudo reboot
   ```

9. After reboot, verify your setup:

   ```bash
   uname -m                         # Should show: aarch64
   cat /etc/os-release              # Inspect OS identity; Bookworm/Trixie are reference releases
   ```

10. Update the fresh OS and install the small set of tools needed to download the installer. Run each command separately and stop if one fails:

    ```bash
    sudo apt update
    sudo apt full-upgrade -y
    sudo apt install -y ca-certificates curl git python3-pip python3-venv
    sudo reboot
    ```

    Reconnect over SSH after reboot. These are [official APT update steps](https://www.raspberrypi.com/documentation/computers/os.html#update-your-current-raspberry-pi-software) within your current OS release. The project installer also installs its OS prerequisites, so Git/pip do not need a separate repair afterward. Do not use `sudo pip install` or `--break-system-packages`; project Python dependencies belong in `.venv`.

    **Why not `sudo apt install -y git pigpio python3-pip`?** The current [Raspberry Pi Trixie ARM64 package index](https://archive.raspberrypi.com/debian/dists/trixie/main/binary-arm64/) does not provide `pigpio`/`pigpiod`. The installer builds the verified pigpio daemon and creates its systemd unit when absent. The Python `pigpio` package alone cannot create `pigpiod.service`.

### 2.4 Project Installation

#### Default installation (recommended)

Run these steps in your Pi's terminal as your normal user. The installer clones the project into `~/NinjaRobotPi0`, installs system prerequisites and prepares the project environment:

```bash
curl -fL --retry 2 --connect-timeout 20 https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh -o "$HOME/ninjarobot-install.sh" &&
  bash "$HOME/ninjarobot-install.sh"
```

The download must succeed before Bash runs; keeping a local copy also avoids feeding dependency commands from a live download pipe. To preview first, download the file and run `bash "$HOME/ninjarobot-install.sh" --dry-run`. When prompted, read each installation plan and type `INSTALL` to confirm (bootstrap and project setup each ask). The installer will:

- Create the `$HOME/NinjaRobotPi0` directory
- Install system packages, locked Python dependencies and the web frontend; reuse compatible Node/uv or download verified fallback tools
- Use a private temporary workspace under the checkout’s `.ninjarobot-install/` directory and reserve at least 2 GB free disk space before downloads; child installers also use that workspace
- Build/install `pigpiod` and its inactive systemd unit if absent; install the Ollama cloud CLI
- Set up the locked Python environment in `.venv`, including its activation script and all robot commands

Wait for **Software installed**. A cloned directory or **PASS: software prerequisites** during preflight is not completion. If installation stops, retain the first error and the reported stage, then use the existing-checkout recovery below.

> **Note:** `HEAD` follows the repository's default branch. Do **not** prefix the command with `sudo`. The installer will ask for your sudo password only when it needs to install system packages.

#### Custom folder installation (alternative)

If you want to install into a different location (e.g., `~/Projects/NinjaRobotPi0`):

```bash
mkdir -p "$HOME/Projects"
curl -fL --retry 2 --connect-timeout 20 https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh -o "$HOME/ninjarobot-install.sh" &&
  bash "$HOME/ninjarobot-install.sh" --install-dir "$HOME/Projects/NinjaRobotPi0"
```

The `--install-dir` path must be absolute (starting with `/`), must not already exist, and its parent folder must already exist.

#### After installation

After **Software installed**, enter the installation directory:

```bash
cd "$HOME/NinjaRobotPi0"
```

Then run the read-only check as a separate step:

```bash
./install.sh --check
```

**Continue only when it exits successfully with no FAIL messages.** It checks tools, the Python environment/launchers, frontend, Ollama CLI and a loaded `pigpiod.service`. It does not install or repair anything, and `pigpiod` is expected to be inactive at this point. If the unit or `.venv/bin/activate` is missing, go to the incomplete-installation recovery below rather than trying to start or activate it.

After a successful check, optionally activate the Python environment:

```bash
source .venv/bin/activate
```

You can also use `.venv/bin/ninja_core` directly without activation. If a compatible uv was not already on PATH, the installer puts it under `~/.local/share/ninjarobot_pi0/tools/uv/`; it does not change your shell profile. To use `uv` manually in this terminal:

```bash
NINJAROBOT_UV="$(python3 -B scripts/install_check.py --find-tool uv)" &&
  export PATH="$(dirname -- "$NINJAROBOT_UV"):$PATH"
uv --version
```

With the robot supported and actuator power still disconnected, start the GPIO daemon only after the software check passes:

```bash
sudo systemctl start pigpiod
systemctl is-active pigpiod
```

Expected result: `active`. Optional autostart on future boots:

```bash
sudo systemctl enable pigpiod
```

> **Important:** The installer creates a missing unit but leaves `pigpiod` inactive and does not enable autostart. Use your chosen installation path if it differs from the default. `pigpiod` is required for servo, buzzer, and other GPIO hardware to work. Installation checks do not establish physical compatibility with a new OS/kernel; complete the device checks during onboarding.

### 2.5 Onboarding — Set Up Your Robot

The onboarding wizard guides you through calibrating each hardware component and setting up your accounts. Before starting, make sure:

- All wiring is complete
- Servos are supported (wheels raised, limbs held) so they can move safely
- You are ready to remove servo power if anything goes wrong

Start the wizard:

```bash
./onboard.sh
```

The wizard walks you through these steps in order:

| Step | What you do | How you know it worked |
|---|---|---|
| **1. Display** | Enter your display's actual GPIO pins, set orientation and brightness | You see a test image on the LCD screen |
| **2. Buzzer** | Confirm the buzzer pin and play a test tone | You hear a short beep, then silence |
| **3. Servo** | Type `READY` only after supporting the robot; calibrate each servo's range and neutral point | Each servo moves to its expected position |
| **4. Distance** | Read sensor values, then calibrate at a known distance | Readings match the real distance |
| **5. Import** | Import display, buzzer, and servo settings into the main `config.json` | All settings pass validation |
| **6. Identity / Bluetooth** | Check and enable Bluetooth, then set the BLE name and robot type | Bluetooth service/controller and a temporary advertisement pass verification |
| **7. Select model provider** | Choose Google, OpenAI, Anthropic or Ollama Cloud; enter a hidden API key and select a live model | Model validates successfully (internet required; small provider charge possible) |
| **8. ngrok** | Optionally enter your ngrok authtoken for remote access | Token is saved (no tunnel opens yet) |

To repair Bluetooth separately, stop the robot server and run `./onboard.sh --step identity`, then choose **Configure this step**. Setup enables/starts Bluetooth when needed, unblocks its software radio switch, powers the controller and removes its temporary test advertisement. It may request your sudo password; press ENTER at the name/type prompts to keep existing settings. Masked services, hardware blocks, missing firmware/controllers or another active BLE application produce guidance rather than a false success. For a read-only check, use `.venv/bin/python -m ninja_ble.system_setup --check`. These checks do not start the robot or move servos.

> ⚠️ **Servo warning:** The servo tool can **immediately move** previously calibrated servos when it opens — even before its menu appears. Always support the robot before opening the servo tool.

**When valid settings already exist**, choose **2) Apply existing settings for all modules** to reuse them and only configure remaining modules.

**Useful onboarding commands:**

```bash
./onboard.sh --dry-run         # Preview without changing anything
./onboard.sh --status          # Check current progress and file validity
./onboard.sh --resume          # Resume from where you left off
./onboard.sh --step servo      # Jump to a specific step
./onboard.sh --step gemini     # Change your API key or model
./onboard.sh --step ngrok      # Configure remote access token
```

Press **Q** or **Ctrl+C** to save progress and exit. The wizard does not start the server on exit.

### Choose or change the agent model

Run `uv run ninja_core config select-model` (also available in `ninja_core init-tool`, option 1, or `./onboard.sh --step ai_model`). Choose **Google, OpenAI, Anthropic, or Ollama Cloud**, enter your API key privately, then select and validate an available model. Restart the running agent/server deliberately to apply a CLI change. Account login is a later feature; use provider API credentials rather than a ChatGPT/Claude subscription password.

`./install.sh` installs the Ollama CLI automatically; Pi0 uses Ollama Cloud, with no local models or daemon. The official ARM64 archive needs 2 GB free temporary disk space. New keys are stored under `~/.config/ninjarobot_pi0/credentials/` (or `$XDG_CONFIG_HOME`); protect that directory and `config.pre-provider.json`. Web microphone input uses browser speech recognition and works with every model provider; uploaded audio files require a supported Gemini model. Cloud calls may incur charges. Detailed behavior and manual validation are in the [model adapter wiki source](../../../../../ninjarobot_pi0_Wiki/raw/notes/ninjarobotpi0/2026-10-10-model-adapter/ModelAdapterImplementation.md).

### 2.6 Create Robot Movements

Use the `movement-tool` to create custom movement sequences (walking patterns, dance moves, gestures):

```bash
.venv/bin/ninja_core movement-tool
```

The movement tool lets you:

- **Move individual servos** to specific angles with speed control
- **Record multi-servo poses** as steps in a sequence
- **Play back sequences** with smooth, position-aware easing (acceleration at the start, constant speed in the middle, deceleration at the end)

**Movement command format:**

```
[SPEED_]PIN:ANGLE[SPEED][/PIN:ANGLE[SPEED]...]
```

| Example | What it does |
|---|---|
| `20:45` | Move GPIO 20 to 45° at medium speed |
| `20:C` | Move GPIO 20 to centre (0°) |
| `S_20:45/21:-30` | Move two servos at slow speed |
| `M_20:C/21:45F` | Global medium speed, but GPIO 21 targets 45° at fast speed |

**Speed letters:** `F` = Fast, `M` = Medium (default), `S` = Slow
**Angle keywords:** `C` = Centre (0°), `M` = Min (−90°), `X` = Max (90°)

### 2.7 Start the Server and Use the Web Interface

Keep the robot supported for the first start. From the project root:

```bash
.venv/bin/ninja_core server
```

The server initialises hardware and may centre servos. At the ngrok prompt, press Enter to retain the token saved during onboarding; enter or change tokens through onboarding’s hidden input. The current server attempts ngrok connections even if you skipped that step, so skipping it is **not a local-only mode**. A working token can expose the control interface publicly.

#### Open the web interface

Open the **Local Access** URL printed by the server (usually `http://<pi-address>:8000`) from any device on the same network.

The web interface has three pages:

| Page | What it does |
|---|---|
| **Home (`/`)** | Language selection, control interface selection and confirmed power-off slider |
| **Movement Tool (`/movement`)** | Distance telemetry and direct built-in movements, face expressions and sounds, without Ninja Agent |
| **Chat (`/agent`)** | AI prompts and browser voice input; expandable real-time System Activity |

The hamburger links on Movement Tool and Chat return to Home. Both control pages have a System Activity panel that starts folded at the bottom and expands over content. Clear Messages clears displayed history locally. Help has been removed; old `/help` bookmarks return to Home. The controller badge reports the active web session. Browser voice input depends on browser support, microphone permission and its speech service; it fills the prompt for review before Send.

---

### 2.8. Automatic Startup (Optional)

If you want the robot to start automatically when you turn on the power, follow these steps.

> [!IMPORTANT]
> **Prerequisites:** Ensure you have completed all previous steps, including hardware calibration and API key setup. The robot must be fully functional before enabling autostart.
>
> **Ngrok requirement:** Autostart checks that a saved token exists and aborts if none is found. Token presence does not prove validity; verify manual server startup first.

#### Step1: Install the Startup Service

> [!IMPORTANT]
> **Prerequisites:** To enable auto poweroff function, you need to disabel the sudo password confirmation by following steps:
> 1. run "sudo visudo" and scroll to the very bottom.
> 2. Add the follow line (replace "pi" with your actual username if it differs)
>```bash
>pi ALL=(ALL) NOPASSWD: ALL
>```
>3. Save and exit the editor (if it defaults to nano, press Ctrl+X, then Y, and hit Enter).

From the project root, as your normal user, select a compatible uv using the installer’s checker, then run the service helper:

```bash
NINJAROBOT_UV="$(python3 -B scripts/install_check.py --find-tool uv)" &&
PATH="$(dirname -- "$NINJAROBOT_UV"):$PATH" .venv/bin/ninja_utils install-startup
```

This will:

1. Check if your system is ready (config exists, pigpiod running, etc.)
2. Create a systemd service file
3. Enable the service for future boots; it does **not** start the robot immediately. The existing service runs `uv run ninja_core server --autostart`, which may sync Python dependencies at startup.

#### Step2: Verify

You can check the status of the service; enabled but inactive is expected until it is started or the Pi reboots:

```bash
.venv/bin/ninja_utils status-startup
```

#### Step3: Reboot

Reboot your Raspberry Pi:

```bash
sudo reboot
```

After reboot, check the service again. Use your actual hostname or Pi IP address (for example, `http://ninjarobotpi0.local:8000`). A QR code is shown only if the display and public tunnel succeed; startup time varies.

> [!TIP]
> **Shutdown:** The Home page’s power slider and confirmation request shutdown. The robot attempts a face/sound animation and the configured `Poweroff` movement, so keep it supported. OS shutdown requires permission to run `sudo shutdown`; if it fails, use `sudo shutdown -h now` from SSH. Confirm the OS has halted before removing power; an idle LED alone is not proof.

#### Removing Autostart

If you want to stop the robot from starting automatically:

```bash
.venv/bin/ninja_utils remove-startup
```

---


## 3. NinjaRobotPi0 File Structure

```
NinjaRobotPi0/
├── ninja_core/               # Central server: HAL, motion, AI agent, web server
├── ninja_ble/                # Bluetooth Low Energy GATT service
├── ninja_utils/              # Shared interfaces, logging, and system utilities
├── ninja_webapp/             # React + Vite frontend (browser control interface)
├── pi0servo/                 # Servo motor driver (velocity-based, up to 8 servos)
├── pi0disp/                  # ST7789V LCD display driver (face expressions)
├── pi0buzzer/                # Passive buzzer driver (sounds and melodies)
├── pi0vl53l0x/               # VL53L0X distance sensor driver
├── ninjarobot_pi0_Wiki/      # Built-in project knowledge base
├── scripts/                  # Installation and maintenance scripts
├── tests/                    # Automated test suite
├── docs/                     # Validation reports and documentation
├── 3Dmodels/                 # 3D-printable robot chassis models
├── assets/                   # Static resources (images, etc.)
├── config.json               # Robot configuration (identity, hardware, Gemini key)
├── servo.json                # Servo calibration data
├── install.sh                # One-command installer
├── onboard.sh                # Guided setup wizard entry point
├── pyproject.toml            # Python project metadata and dependencies
└── README.md                 # This file
```

---

### Built-in movements by robot type

After calibrating the servos for your build, select the robot type and import the module settings. These commands only update configuration data:

```bash
.venv/bin/ninja_core config set-type spider  # Or wheel / humanoid; wheel is saved as tire
.venv/bin/ninja_core config import
```

Spider receives 19 `spider_*` movements and the exact `Poweroff` pose from the Spider proposal when GPIO20–27 are configured. Wheel receives `home`, which commands every configured servo to 0° at Slow speed. Humanoid with GPIO20–27 configured receives the exact 37 movements from [the owner default list](../../../../../DevelopmentPlanDoc/humanoid_movements_updated.json): 36 `humanoid_*` movements (including forward/backward runs) and `Poweroff`. The ordinary movements use Medium speed; the runs use Fast speed. Full Humanoid defaults use `humanoid_home` instead of an extra generic `home`. Humanoid `Poweroff` uses Medium speed with GPIO20–23 at 0°, GPIO24/25 at +30°/−30°, and GPIO26/27 at +90°/−90°. Partial Humanoid profiles receive only `home`. No movements run during import. Restart an already running server/tool deliberately to load the updated configuration.

Once the robot is supported and ready to move, use movement-tool option 4, the web Movement Tool page's movement dropdown, or ask Ninja agent for an available movement. Opening movement-tool or starting the server can initialize hardware; server shutdown can run `Poweroff`. Spider's sampled waypoints preserve targets, not OTTO's exact timing or physical walking distance. Validate direction, clearance, power and calibration before grouped motion, especially the ±90° shutdown pose.

Reimport preserves custom sequences and edited built-ins. Type changes remove only unchanged imported built-ins; edited movements retain their type scope and are hidden/rejected on incompatible profiles. Native playback validates the entire sequence before its first servo command. Invalid or incompatible web requests return an error and are recorded in the page's log. Missing active channels also block playback. Built-ins can be restored by removing an unwanted edited entry and importing again; back up your configuration first. Existing custom `home`/`Poweroff` name collisions are preserved rather than overwritten.




The [implementation plan](../../../../../docs/BuiltinMovementsImplementationPlan.md) and [validation report](../../../../../docs/validation/BuiltinMovements-2026-10-09.md) record the built-in movement implementation and its original validation status.

### Exit, reconnect and environment prompt

Movement-tool **6. Exit** executes configured `Poweroff` before HAL shutdown, without a following center command. Wheel/Humanoid without `Poweroff` use their configured `home`. Invalid/incompatible poses are refused; shutdown and configuration save still run. Opening the tool centers servos, and exiting can move them; check clearance and support the robot first. Shutdown releases PWM, so the final pose is not held electrically afterward.

One browser identity controls the web interface at a time; tabs sharing its session cookie count as one controller. Home/Movement Tool/Chat navigation retains the connection. Closing its last tab restores the saved ngrok QR (or LAN QR if tunneling failed), stops active browser-owned work and permits another browser to connect. A lost network is released after 35 seconds without a heartbeat; browsers retry every 3 seconds. Missing/failing displays do not prevent reconnection. This ownership guard is not login authentication, and BLE remains a separate existing protocol. REST `/api/` calls and distance/events sockets require the active browser session; inactive API requests return 423.

The installer retains the `.venv` directory and now sets its prompt to `(ninjarobotpi0)` with `uv venv --allow-existing --prompt ninjarobotpi0`, then performs locked synchronization. It does not clear the environment. Re-activate your current shell after upgrading: `deactivate` (if active), then `source .venv/bin/activate`. The local environment's activation scripts have also been updated without reinstalling packages.




See the [lifecycle plan](../../../../../docs/LifecycleRefinementsImplementationPlan.md) and [validation report](../../../../../docs/validation/LifecycleRefinements-2026-10-10.md). New lifecycle raw manual versions await the owner's ingestion/review; existing wiki pointers remain unchanged.

## 4. Troubleshooting

### `uv run` cannot spawn `ninja_core` after upgrading

`Failed to spawn: ninja_core` / `No such file or directory` means the CLI launcher is missing, not that the server rejected your configuration. The former root project duplicated five package-owned console scripts; an upgrade could remove those shared files even though provider packages stayed installed. The root now delegates commands to their packages, and the installer reinstalls/checks all five providers. A normal sync can leave already-missing launchers untouched.

From your existing checkout containing this fix, stop any running robot in a controlled maintenance session first (shutdown may execute Poweroff), then repair Python as your normal user:

```bash
cd /home/rogerchang/NinjaRobotPi0  # Use your actual checkout path
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev \
  --reinstall-package ninja-core --reinstall-package pi0servo \
  --reinstall-package pi0disp --reinstall-package pi0buzzer \
  --reinstall-package pi0vl53l0x
uv run --no-sync ninja_core --help
./install.sh --check
```

`--inexact` preserves unrelated/dev packages; configuration/calibration is retained. This does not perform apt installation or start hardware/services. If dependencies/interpreter are absent, use the full installer after `./install.sh --dry-run`. For another checkout, first publish this fix, check `git status`, then `git pull --ff-only` on the intended tracking branch; stop on Git errors and preserve local changes. Do not delete `.venv` or your configuration as a first recovery step.

Only after CLI help succeeds **and physical readiness is confirmed**, run `uv run --no-sync ninja_core server` (or `.venv/bin/ninja_core server`). Startup can energize/center servos, initialize display/buzzer and open ngrok; it is not a non-moving smoke test. See [repair plan](../../../../../docs/CLIEntryPointRepairPlan.md) and [validation](../../../../../docs/validation/CLIEntryPoints-2026-10-10.md).

### Installation stopped before Python setup

**Missing uv, `.venv/bin/activate`, all robot commands, or `pigpiod.service` means the installation is incomplete.** Do not create an empty environment by hand or repeatedly run `--check`; retry the full installer from the existing directory. A missing service cannot be started.

`Stop pigpiod ... first` or `Stop ninjarobot ... first` means installation stopped **before** dependencies were installed. `PASS: software prerequisites` at this stage is only platform/path preflight; success is **Software installed**. Missing `.venv/bin/ninja_core` or package metadata is an incomplete installation, not a version mismatch.

Support the robot and disconnect actuator power before stopping the foreground robot application. Stop any active robot service **before** pigpiod; then retry from the existing folder:

```bash
sudo systemctl stop ninjarobot   # Only if this service is installed/running
sudo systemctl stop pigpiod   # Only if this service exists and is running
cd "$HOME/NinjaRobotPi0"
./install.sh --dry-run
./install.sh
# Continue only after Software installed:
./install.sh --check
```

Keep configuration/calibration files. If installation fails again, retain the **first error**; `--check` only inspects and does not repair. After successful installation, start pigpiod again before hardware use. To update an existing checkout first, use `git fetch origin HEAD && git merge --ff-only FETCH_HEAD`; stop if Git reports an error. The installer itself does not update existing Git files.


If Node extraction reports **`Cannot write: No space left on device`** or **`Wrote only ... bytes`**, the archive download reached extraction but its destination ran out of space. The earlier installer used the default temporary directory. [Trixie stores `/tmp` in RAM](https://www.debian.org/releases/trixie/release-notes/issues.en.html#the-temporary-files-directory-tmp-is-now-stored-in-a-tmpfs); on a Zero 2 W, Node's archive plus extracted files can exhaust that space even when the SD card has free space. The corrected installer uses `.ninjarobot-install/work.*` on the checkout's filesystem, exports that location to child tools, and checks for at least 2 GB free. Ensure the checkout is on the SD card or another disk with sufficient free space.

You can retry the **currently published earlier installer** with a disk-backed temporary directory, without deleting or downloading the checkout again:

```bash
cd "$HOME/NinjaRobotPi0"
df -h "$HOME" /tmp
mkdir -p -m 700 "$HOME/.cache/ninjarobot-install-tmp"
TMPDIR="$HOME/.cache/ninjarobot-install-tmp" ./install.sh
```

Check that `$HOME` has at least 2 GB free; free space there first if necessary. After **Software installed**, run `./install.sh --check` separately. To capture another failure completely, use Bash's pipeline status so `tee` does not hide installer failure:

```bash
set -o pipefail
TMPDIR="$HOME/.cache/ninjarobot-install-tmp" ./install.sh 2>&1 | tee "$HOME/ninjarobot-install.log"
```

Deleting `~/NinjaRobotPi0` does **not** remove reused/private tools under `~/.local/share/ninjarobot_pi0/tools/`; compatible tools are intentionally reused. Do not delete those tools or your configuration as the first recovery step. The corrected failure summary names the exact Node operation (download, checksum, extraction, capability check or publication).

### Installation Issues

| Problem | Solution |
|---|---|
| `curl` returns 404 | The installer must be published to the official repository first. For pre-publication testing, use the local checkout: `cd /path/to/NinjaRobotPi0 && ./install.sh` |
| `Unsupported platform` error | Verify: Raspberry Pi Zero 2 W, `uname -m` shows `aarch64`, Debian-based Raspberry Pi OS 64-bit, Python 3.10+, and you are logged in as a normal user (not root). |
| `Destination already exists` | The installer will not overwrite an existing folder. Enter that folder and run: `cd "$HOME/NinjaRobotPi0" && ./install.sh` |
| uv download reports `SSL_read` / `unexpected eof` / `Could not resolve host: github.com` | The download connection or DNS failed before uv installation. The installer retries the verified uv installation up to three times. Check Wi-Fi/internet and DNS resolution for `releases.astral.sh` and `github.com`; restore connectivity, then rerun `./install.sh` in the existing checkout. Keep TLS verification enabled. |
| Node stage ends with exit 2 and `tar: No space left on device` | Temporary extraction storage is full. Use the disk-backed TMPDIR recovery above or the published corrected installer; inspect free space on the actual checkout filesystem. |
| Installation stops at OS packages | Check the error message — it is usually an `apt`, network, or `sudo` issue. Fix the underlying problem and re-run `./install.sh`. |
| `uv is not found` after install | Run `./install.sh --check`. If it passes, uv is private: locate it with `python3 -B scripts/install_check.py --find-tool uv` and use the PATH step above. If it fails, retry the installer and retain its first error. |
| `Unit pigpiod.service not found` / missing `.venv/bin/activate` | Installation is incomplete. Enter the existing checkout, run `./install.sh`, wait for **Software installed**, then run `./install.sh --check`. Do not start the daemon or activate the environment until checks pass. |
| Existing `/usr/sbin/policy-rc.d` | The installer retains administrator service policy and stops before apt. Ask the system administrator to review the policy; do not blindly delete it. |

### Hardware Issues

| Problem | Solution |
|---|---|
| Display stays blank | Check that SPI is enabled: `sudo raspi-config` → Interface Options → SPI → Enable. Verify wiring matches your configured pins. |
| Buzzer makes no sound | Make sure it is a **passive** buzzer (not active). Confirm it is connected to GPIO 17. |
| Servos do not move | Raise wheels/limbs first. Check `sudo systemctl status pigpiod` — it must be running. Verify wiring and re-run calibration. |
| Distance sensor not detected | Check that I2C is enabled. With robot/sensor tools stopped, use `i2cdetect -y 1` (from the optional `i2c-tools` package); the usual sensor address is `29` (0x29). |
| Hardware tool will not open | Stop the server first (`Ctrl+C`). Then check: is `pigpiod` running? Are I2C/SPI enabled? Are pin assignments correct? |
| Import blocked in onboarding | Complete valid display, buzzer, and servo calibration first. Factory-default files are not accepted. |
| Port 8000 is busy | Identify the listener first. Stop a foreground robot with `Ctrl+C`, or its managed service with `sudo systemctl stop ninjarobot`; stopping can execute the configured shutdown movement. |

### Server / AI Issues

| Problem | Solution |
|---|---|
| Model setup fails | Check your internet connection and API key. Retry with: `./onboard.sh --step gemini` |
| ngrok setup fails | Check your internet connection and authtoken. Retry with: `./onboard.sh --step ngrok` |
| Server starts but web page is unreachable | Make sure your phone/computer is on the same Wi-Fi network as the Pi. Try using the Pi's IP address directly. |

---

## 5. Appendix

### Appendix A: Google Gemini API Key

To use the AI chat feature, you need a Google Gemini API key. Free-tier availability and quotas depend on the model, project and region. Here is how to get one:

#### Step 1 — Open Google AI Studio

1. Go to [Google AI Studio](https://aistudio.google.com/) in your browser.
2. Sign in with your Google account.

#### Step 2 — Create an API key

1. Click **Get API key** in the left sidebar (or top navigation).
2. Click **Create API key**.
3. Choose an existing Google Cloud project or create one, then check its quota and billing settings.
4. Copy the generated API key privately; do not include it in screenshots, logs or Git commits.

#### Step 3 — Save the key on your Pi

Choose Google in onboarding step 7, **Select model provider**, to enter your Gemini API key. Paste it in — the input is hidden for security. The wizard then lets you choose from the available AI models associated with your key.

If you already completed onboarding and want to change the key:

```bash
./onboard.sh --step gemini
```

> **Note:** The free tier of the Gemini API has usage limits. Check [Google AI pricing](https://ai.google.dev/gemini-api/docs/pricing) for current details.

### Appendix B: ngrok Account Setup

[ngrok](https://ngrok.com/) lets you access your robot from outside your home network (for example, from your office or while travelling). It creates a secure tunnel from the internet to your Pi.

#### Step 1 — Create an ngrok account

1. Go to [ngrok.com](https://ngrok.com/) and click **Sign up** for a free account.
2. After logging in, go to **Your Authtoken** in the left sidebar of the ngrok dashboard.
3. Copy your authtoken (a long string that identifies your account).

> **Note:** The ngrok free plan has connection limits. See [ngrok pricing](https://ngrok.com/docs/pricing-limits/free-plan-limits) for details.

#### Step 2 — Save the token on your Pi

During onboarding, the wizard asks for your ngrok authtoken at the **ngrok** step. Paste it in — the input is hidden for security.

If you already completed onboarding and want to add or change the token:

```bash
./onboard.sh --step ngrok
```

The token is saved privately. No tunnel opens during onboarding — the tunnel starts only when you launch the server.

> ⚠️ **Security:** Never share your ngrok public URL or screenshot it. Anyone with the URL can control your robot until you stop the tunnel.

---

### Appendix C: Compatibility and reference checks

Bookworm/Trixie 64-bit are reference releases, not an OS-codename allowlist. The installer requires Zero 2 W, Linux `aarch64`, Debian-family Raspberry Pi OS, a normal user and Python 3.10+. Node must satisfy the locked Vite build range (20.19+ in 20.x, or >=22.12.0); uv is checked for required commands, not an exact version. Passing software checks does not certify an assembled robot.

From the installation folder, `./onboard.sh --status` checks saved configuration; `./onboard.sh --resume` resumes setup. These do not certify physical operation. Only run one hardware tool/server at a time. The movement tool can centre servos when recording starts; use only configured pins and mechanically safe angles. Per-servo speed suffixes in the core movement tool require numeric angles (for example `21:45F`, not `21:XF`).

Protect `config.json` (which may contain your Gemini key), ngrok credentials and calibration files; do not publish them. Gemini pricing/quota and ngrok availability depend on your account. The Pi0 control interface has no user-login protection; an encrypted ngrok tunnel does not add application authentication. Use trusted networks and keep control URLs private.

Full references: [Installation Guide](../../../../../ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-13-humanoid-owner-defaults/InstallationGuide.md), [Development Guide](../../../../../ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-13-web-gamepad/DevelopmentGuide.md), [Development Log](../../../../../ninjarobot_pi0_Wiki/raw/notes/ninjarobotpi0/2026-10-13-web-gamepad/DevelopmentLog.md).

## License

NinjaRobotPi0 source code is licensed under the [MIT License](../../../../../LICENSE).

<div align="center">

Made with ❤️ for AI Robotics Education

</div>

---
---
