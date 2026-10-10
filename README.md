# NinjaRobotPi0

<div align="center">

**An Educational Raspberry Pi Zero 2 W Robot — Build It, Program It, Bring It to Life**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Raspberry Pi Zero 2 W](https://img.shields.io/badge/platform-Raspberry%20Pi%20Zero%202%20W-red.svg)](https://www.raspberrypi.com/)
[![AI: Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

**🌐 Language / 言語 / 語言 / 语言:**
[English](#english) ・ [日本語](#日本語) ・ [繁體中文](#繁體中文) ・ [简体中文](#简体中文)

---

<!-- ENGLISH -->

# English

## 1. What Is NinjaRobotPi0?

**NinjaRobotPi0** is an open-source, modular educational robot built on the **Raspberry Pi Zero 2 W** (a tiny, affordable computer about the size of a stick of gum). It brings together servo motors (for movement), an LCD display (the robot's face), a buzzer (for sounds and melodies), a distance sensor, cloud AI chat (Google, OpenAI, Anthropic or Ollama Cloud), Bluetooth Low Energy (BLE), and a browser-based control interface — all in one compact package.

Whether you want to build a tire-type car, a humanoid, or a spider robot, NinjaRobotPi0 gives you the foundation to learn how software, AI, and physical components work together.

### What can it do?

- **Move and express itself** — Use the built-in movement library to make your robot walk, wave, or dance. The LCD face shows animated expressions, and the buzzer plays emotion sounds.
- **Sense distance** — A VL53L0X laser sensor measures distances in millimetres, so your robot can detect obstacles.
- **Chat with AI** — Choose a cloud provider and connect its API key to chat with the AI. The AI can even trigger robot actions like movements and expressions.
- **Control from your phone** — Open a web browser on any device and you get a control panel with Home, Agent (AI chat), and Help pages — in English, Japanese, Traditional Chinese, and Simplified Chinese.
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

> **📎 Full hardware details:** See the [Installation Guide](ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-10-model-adapter/InstallationGuide.md)

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
3. Choose **Raspberry Pi OS (64-bit)** — Bookworm or Trixie. The Lite (no desktop) edition works fine.
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

### 2.4 Project Installation

#### Default installation (recommended)

Run this single command in your Pi's terminal. It clones the project into `~/NinjaRobotPi0`, installs system prerequisites and prepares the project environment:

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

When prompted, read the installation plan and type `INSTALL` to confirm. The installer will:

- Create the `$HOME/NinjaRobotPi0` directory
- Install system packages, locked Python dependencies and the web frontend; reuse compatible Node/uv or download verified fallback tools
- Set up the locked Python environment in `.venv`

> **Note:** `HEAD` follows the repository's default branch. Do **not** prefix the command with `sudo`. The installer will ask for your sudo password only when it needs to install system packages.

#### Custom folder installation (alternative)

If you want to install into a different location (e.g., `~/Projects/NinjaRobotPi0`):

```bash
mkdir -p "$HOME/Projects"
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash -s -- --install-dir "$HOME/Projects/NinjaRobotPi0"
```

The `--install-dir` path must be absolute (starting with `/`), must not already exist, and its parent folder must already exist.

#### After installation

Once the installer prints **Software installed**, verify the installation and start the pigpio daemon (a background service that controls GPIO pins):

```bash
cd "$HOME/NinjaRobotPi0" &&
./install.sh --check &&

# Start pigpio now:
sudo systemctl start pigpiod

# Optional: make pigpio start automatically on future boots:
sudo systemctl enable pigpiod
```

> **Important:** The installer leaves `pigpiod` inactive and does not enable autostart. Use your chosen installation path if it differs from the default. `pigpiod` is required for servo, buzzer, and other GPIO hardware to work. If you skip this step, hardware tools will fail to connect.

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
| **6. Identity** | Set a BLE name and choose your robot type: `tire`, `humanoid`, or `spider` | Name and type match your build |
| **7. Select model provider** | Choose Google, OpenAI, Anthropic or Ollama Cloud; enter a hidden API key and select a live model | Model validates successfully (internet required; small provider charge possible) |
| **8. ngrok** | Optionally enter your ngrok authtoken for remote access | Token is saved (no tunnel opens yet) |

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

`./install.sh` installs the Ollama CLI automatically; Pi0 uses Ollama Cloud, with no local models or daemon. The official ARM64 archive needs 2 GB free temporary disk space. New keys are stored under `~/.config/ninjarobot_pi0/credentials/` (or `$XDG_CONFIG_HOME`); protect that directory and `config.pre-provider.json`. Web microphone input uses browser speech recognition and works with every model provider; uploaded audio files require a supported Gemini model. Cloud calls may incur charges. Detailed behavior and manual validation are in the [model adapter wiki source](ninjarobot_pi0_Wiki/raw/notes/ninjarobotpi0/2026-10-10-model-adapter/ModelAdapterImplementation.md).

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
| **Home** | Robot entry page with a power-off slider control |
| **Agent** | AI chat with your selected provider, expressions, sounds, movements, and distance readings |
| **Help** | Usage guidance; the menu also lets you switch the interface language |

> **Note:** The BLE badge on screen means the robot is **advertising** (broadcasting its Bluetooth signal), not that a controller is connected. Browser speech input depends on browser support and permissions.

---

### 2.8. Automatic Startup (Optional)

If you want the robot to start automatically when you turn on the power, follow these steps.

> [!IMPORTANT]
> **Prerequisites:** Ensure you have completed all previous steps, including hardware calibration and API key setup. The robot must be fully functional before enabling autostart.
>
> **Ngrok requirement:** Autostart checks that a saved token exists and aborts if none is found. Token presence does not prove validity; verify manual server startup first.

#### Step1: Install the Startup Service

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

Spider receives 19 `spider_*` movements and the exact `Poweroff` pose from the Spider proposal when GPIO20–27 are configured. Wheel and Humanoid currently receive only `home`, which commands every configured servo to 0° at Slow speed. Their other default movements will be added later. No movements run during import. Restart an already running server/tool deliberately to load the updated configuration.

Once the robot is supported and ready to move, use movement-tool option 4, the web Agent page's movement dropdown, or ask Ninja agent for an available movement. Opening movement-tool or starting the server can initialize hardware; server shutdown can run `Poweroff`. Spider's sampled waypoints preserve targets, not OTTO's exact timing or physical walking distance. Validate direction, clearance, power and calibration before grouped motion, especially the ±90° shutdown pose.

Reimport preserves custom sequences and edited built-ins. Type changes remove only unchanged imported built-ins; edited movements retain their type scope and are hidden/rejected on incompatible profiles. Native playback validates the entire sequence before its first servo command. Invalid or incompatible web requests return an error and are recorded in the page's log. Missing active channels also block playback. Built-ins can be restored by removing an unwanted edited entry and importing again; back up your configuration first. Existing custom `home`/`Poweroff` name collisions are preserved rather than overwritten.

日本語: 校正後にロボット種類を設定し、`config import` を実行すると対応する動作が追加されます。Wheel と Humanoid は現在、全設定サーボを中心に戻す `home` のみです。インポートではサーボは動きません。実行前に機体を支え、配線・方向・可動範囲・電源を確認してください。Spider の `Poweroff` は終了処理でも動く場合があります。

繁體中文：完成校正後設定機器人類型，再執行 `config import`，即可加入適用動作。Wheel 與 Humanoid 目前只有將所有已設定伺服機回中的 `home`。匯入不會驅動硬體。執行前請支撐機體並確認接線、方向、活動範圍與電源；Spider 的 `Poweroff` 也可能在結束伺服器時執行。

The [implementation plan](docs/BuiltinMovementsImplementationPlan.md) and [validation report](docs/validation/BuiltinMovements-2026-10-09.md) record the built-in movement implementation and its original validation status.

### Exit, reconnect and environment prompt

Movement-tool **6. Exit** executes configured `Poweroff` before HAL shutdown, without a following center command. Wheel/Humanoid without `Poweroff` use their configured `home`. Invalid/incompatible poses are refused; shutdown and configuration save still run. Opening the tool centers servos, and exiting can move them; check clearance and support the robot first. Shutdown releases PWM, so the final pose is not held electrically afterward.

One browser identity controls the web interface at a time; tabs sharing its session cookie count as one controller. Home/Agent/Help navigation retains the connection. Closing its last tab restores the saved ngrok QR (or LAN QR if tunneling failed), stops active browser-owned work and permits another browser to connect. A lost network is released after 35 seconds without a heartbeat; browsers retry every 3 seconds. Missing/failing displays do not prevent reconnection. This ownership guard is not login authentication, and BLE remains a separate existing protocol. REST `/api/` calls and distance/events sockets require the active browser session; inactive API requests return 423.

The installer retains the `.venv` directory and now sets its prompt to `(ninjarobotpi0)` with `uv venv --allow-existing --prompt ninjarobotpi0`, then performs locked synchronization. It does not clear the environment. Re-activate your current shell after upgrading: `deactivate` (if active), then `source .venv/bin/activate`. The local environment's activation scripts have also been updated without reinstalling packages.

日本語：移動ツールの「6. Exit」は `Poweroff`（未設定の Wheel/Humanoid は `home`）を実行してから終了し、再センタリングしません。最後のタブを閉じると再接続 QR を表示します。同時操作は一つのブラウザー識別情報に限定され、通信断はハートビート未受信から 35 秒で解放します。`.venv` の表示名は `ninjarobotpi0` です。終了時にも動くため、機体を支えて可動範囲を確認してください。

繁體中文：移動工具選擇「6. Exit」會先執行 `Poweroff`（未設定 Poweroff 的 Wheel/Humanoid 使用 `home`），之後不再回中。關閉最後一個分頁後重新顯示連線 QR；同時僅允許一個瀏覽器身分控制，35 秒未收到心跳即釋放連線。`.venv` 顯示名稱改為 `ninjarobotpi0`。結束時仍可能移動，請先支撐機體並確認活動範圍。

简体中文：移动工具选择「6. Exit」会先执行 `Poweroff`（未配置 Poweroff 的 Wheel/Humanoid 使用 `home`），之后不再回中。关闭最后一个标签页后重新显示连接 QR；同时仅允许一个浏览器身份控制，35 秒未收到心跳即释放连接。`.venv` 显示名称改为 `ninjarobotpi0`。退出时仍可能移动，请先支撑机体并确认活动范围。

See the [lifecycle plan](docs/LifecycleRefinementsImplementationPlan.md) and [validation report](docs/validation/LifecycleRefinements-2026-10-10.md). New lifecycle raw manual versions await the owner's ingestion/review; existing wiki pointers remain unchanged.

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

Only after CLI help succeeds **and physical readiness is confirmed**, run `uv run --no-sync ninja_core server` (or `.venv/bin/ninja_core server`). Startup can energize/center servos, initialize display/buzzer and open ngrok; it is not a non-moving smoke test. See [repair plan](docs/CLIEntryPointRepairPlan.md) and [validation](docs/validation/CLIEntryPoints-2026-10-10.md).

### Installation stopped before Python setup

`Stop pigpiod ... first` or `Stop ninjarobot ... first` means installation stopped **before** dependencies were installed. `PASS: software prerequisites` at this stage is only platform/path preflight; success is **Software installed**. Missing `.venv/bin/ninja_core` or package metadata is an incomplete installation, not a version mismatch.

Support the robot and disconnect actuator power before stopping the foreground robot application. Stop any active robot service **before** pigpiod; then retry from the existing folder:

```bash
sudo systemctl stop ninjarobot   # Only if this service is installed/running
sudo systemctl stop pigpiod
cd "$HOME/NinjaRobotPi0" && ./install.sh && ./install.sh --check
```

Keep configuration/calibration files. If installation fails again, retain the **first error**; `--check` only inspects and does not repair. After successful installation, start pigpiod again before hardware use. To update an existing checkout first, use `git fetch origin HEAD && git merge --ff-only FETCH_HEAD`; stop if Git reports an error. The installer itself does not update existing Git files.


### Installation Issues

| Problem | Solution |
|---|---|
| `curl` returns 404 | The installer must be published to the official repository first. For pre-publication testing, use the local checkout: `cd /path/to/NinjaRobotPi0 && ./install.sh` |
| `Unsupported platform` error | Verify: Raspberry Pi Zero 2 W, `uname -m` shows `aarch64`, Debian-based Raspberry Pi OS 64-bit, Python 3.10+, and you are logged in as a normal user (not root). |
| `Destination already exists` | The installer will not overwrite an existing folder. Enter that folder and run: `cd "$HOME/NinjaRobotPi0" && ./install.sh` |
| Installation stops at OS packages | Check the error message — it is usually an `apt`, network, or `sudo` issue. Fix the underlying problem and re-run `./install.sh`. |
| `uv is not found` after install | Use `.venv/bin/ninja_core` for runtime commands. Compatible existing tools are reused; fallback tools are private. See the autostart section if that helper needs uv on PATH. |

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

Full references: [Installation Guide](ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-10-model-adapter/InstallationGuide.md), [Development Guide](ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-10-model-adapter/DevelopmentGuide.md), [Development Log](ninjarobot_pi0_Wiki/raw/notes/ninjarobotpi0/2026-10-10-model-adapter/DevelopmentLog.md).

## License

NinjaRobotPi0 source code is licensed under the [MIT License](LICENSE).

<div align="center">

Made with ❤️ for AI Robotics Education

</div>

---
---

<!-- 日本語 -->

# 日本語

モデルの変更: `uv run ninja_core config select-model` または `./onboard.sh --step ai_model` で Google、OpenAI、Anthropic、Ollama Cloud を選び、API キーを非公開で入力してモデルを検証します。変更後はエージェントを手動で再起動してください。Pi0 はクラウド推論のみを使用します。インストーラーは Ollama CLI を導入します（ローカルモデルやデーモンなし、展開用の空き容量 2 GB が必要）。Web のマイク入力はブラウザーの音声認識を使い、すべてのモデルプロバイダーで利用できます。音声ファイルの送信には対応する Gemini モデルが必要です。クラウド利用は課金される場合があります。

## 1. NinjaRobotPi0 とは？

**NinjaRobotPi0** は、**Raspberry Pi Zero 2 W**（ガム一個分ほどの小さくて手頃なコンピュータ）で動くオープンソースの教育用ロボットです。サーボモーター（動き）、LCD ディスプレイ（ロボットの顔）、ブザー（音やメロディ）、距離センサー、Google Gemini AI チャット、Bluetooth Low Energy（BLE）、ブラウザ操作をひとつにまとめたコンパクトなパッケージです。

タイヤ型の車、ヒューマノイド、クモ型ロボットなど、好きな形で組み立てられます。ソフトウェア・AI・ハードウェアがどう連携するかを楽しく学べます。

### 何ができる？

- **動いて表情を見せる** — 内蔵の動作ライブラリで歩行・ウェーブ・ダンスが可能。LCD にアニメ表情、ブザーで感情サウンドを再生。
- **距離を測る** — VL53L0X レーザーセンサーがミリメートル単位で障害物を検知。
- **AI とチャット** — Google Gemini API キーを接続すれば AI と会話でき、動作やアクションも起動可能。
- **スマホから操作** — ブラウザで Home・Agent（AI チャット）・Help の 3 ページを操作。英語・日本語・繁體中文・简体中文に対応。
- **段階的に学べる** — ガイド付きツールで各部品を校正し、Python パッケージや Web インターフェースを自分のペースで探索。

---

## 2. クイックスタートガイド

### 2.1 推奨ハードウェア

| 部品 | 仕様 | 備考 |
|---|---|---|
| **コンピュータ** | Raspberry Pi Zero 2 W（GPIO ヘッダー付き） | ロボットの頭脳 |
| **OS** | Raspberry Pi OS 64-bit（Bookworm / Trixie） | Debian 系、デスクトップ不要 |
| **ストレージ** | microSD カード 16 GB 以上 | 依存関係とフロントエンドのビルド用 |
| **Pi 電源** | 5 V micro-USB 電源 | Pi 用のみ |
| **サーボ** | 最大 8 個の SG90 / MG90S マイクロサーボ | 車輪・腕・脚など用途に合わせて |
| **サーボ電源** | 別系統の 5 V 3 A+ 電源 | Pi の電源ピンを通さないこと |
| **ディスプレイ** | ST7789V SPI LCD 240×320 | ロボットの顔 |
| **距離センサー** | VL53L0X（I2C） | レーザー測距 |
| **ブザー** | パッシブブザー（3–5 V） | 音やメロディ用 |

### 2.2 配線

電源を切ってから配線してください。サーボ電源は別系統で、Pi の電源ピンを通さないでください。サーボ電源と Pi の GND は共有してください。

| 部品 | 接続先 |
|---|---|
| サーボ信号線（最大 8 本） | GPIO 20–27 |
| ST7789V SPI データ | MOSI → GPIO 10、SCLK → GPIO 11、CE0 → GPIO 8 |
| ST7789V 制御 | DC → GPIO 14、RST → GPIO 15、バックライト → GPIO 16 |
| VL53L0X | SDA → GPIO 2、SCL → GPIO 3 |
| ブザー | 信号 → GPIO 17 |

> ⚠️ **安全:** 通電中に配線を変更しないでください。

GPIO 番号は **BCM 番号**です（物理ピン番号ではありません）。GPIO は **3.3 V ロジック**で、5 V を入力してはいけません。モジュールの電源・駆動回路を確認し、サーボ電源は合計ストール電流に合わせて選んでください。SG90/MG90S の位置制御サーボは車輪を連続回転させるものではありません。

### 2.3 OS インストール

1. [raspberrypi.com/software](https://www.raspberrypi.com/software/) から **Raspberry Pi Imager** をダウンロード。
2. **Raspberry Pi OS 64-bit** を microSD に書き込み。ホスト名・SSH・Wi-Fi・ユーザー名を設定。
3. Pi に挿して起動、SSH で接続：
   ```bash
   ssh YOUR_USERNAME@ninjarobotpi0.local
   ```
4. `sudo raspi-config` で **I2C** と **SPI** を有効化。GPIO 14/15 をディスプレイに使う場合は、そのピンのシリアルコンソールと UART を無効化し、必要に応じて再起動。

### 2.4 プロジェクトのインストール

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

通常ユーザーで実行し、`INSTALL` と入力して確認。**Software installed** が表示された後に確認し、pigpiod を起動します（インストーラーは起動・自動起動設定を行いません）：

```bash
cd "$HOME/NinjaRobotPi0" &&
./install.sh --check &&

# pigpio を起動（GPIO ハードウェア制御に必要）：
sudo systemctl start pigpiod

# 任意：今後の起動時に自動で開始：
sudo systemctl enable pigpiod
```

**別フォルダにインストール** したい場合：

```bash
mkdir -p "$HOME/Projects"
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash -s -- --install-dir "$HOME/Projects/NinjaRobotPi0"
```

> **重要:** 別フォルダを選んだ場合は、以降の `cd` をそのパスに置き換えてください。`pigpiod` はサーボ・ブザーなどの GPIO ハードウェア制御に必須です。

### 2.5 初期設定ウィザード

サーボの支えを確認してから実行：

```bash
./onboard.sh
```

| ステップ | 内容 |
|---|---|
| 1. ディスプレイ | GPIO ピン設定、向き・明るさテスト |
| 2. ブザー | ピン設定、テスト音再生 |
| 3. サーボ | `READY` 入力後、各サーボの範囲と中立点を校正 |
| 4. 距離 | センサー読み取り値を確認・校正 |
| 5. 取り込み | 設定を `config.json` にインポート |
| 6. 名前/型 | BLE 名とロボットタイプ（`tire`/`humanoid`/`spider`）を設定 |
| 7. モデルプロバイダー選択 | Google / OpenAI / Anthropic / Ollama Cloud の API キーとモデルを設定 |
| 8. ngrok | リモートアクセス用トークン設定（任意） |

> ⚠️ **注意:** サーボツールは開くと**即座に**校正済みサーボを動かす場合があります。必ずロボットを支えてから開いてください。

### 2.6 動作の作成

```bash
.venv/bin/ninja_core movement-tool
```

サーボを個別に動かし、ポーズを記録してシーケンスを作成できます。

**動作コマンドの形式：**

```
[スピード_]ピン:角度[スピード][/ピン:角度[スピード]...]
```

| 例 | 動作内容 |
|---|---|
| `20:45` | GPIO 20 を 45° に中速で移動 |
| `20:C` | GPIO 20 を中央（0°）に移動 |
| `S_20:45/21:-30` | 2 つのサーボを低速で同時移動 |

**スピード:** `F` = 高速、`M` = 中速（デフォルト）、`S` = 低速
**角度キーワード:** `C` = 中央（0°）、`M` = 最小（−90°）、`X` = 最大（90°）

### 2.7 サーバー起動と Web インターフェース

サーバーはハードウェアを初期化し、サーボを中央に動かす場合があります。ngrok の確認では Enter で保存済みトークンを保持します。トークンの入力・変更にはウィザードの非表示入力を使ってください。ngrok の設定を省略しても接続は試行されるため、ローカル専用モードにはなりません。

```bash
.venv/bin/ninja_core server
```

表示された **ローカル URL**（通常 `http://<Pi のアドレス>:8000`）をスマホで開いてください。

| ページ | 機能 |
|---|---|
| **Home** | ロボットのホーム画面、電源オフ制御 |
| **Agent** | AI チャット、表情・サウンド・動作 |
| **Help** | 使い方ガイド、言語切替 |

---

### 2.8 自動起動（オプション）

電源を入れたときにロボットを自動的に起動させたい場合は、次の手順に従ってください。

> [!IMPORTANT]
> **前提条件:** ハードウェアの校正やAPIキーの設定など、前のすべての手順を完了していることを確認してください。自動起動を有効にする前に、ロボットが完全に機能している必要があります。
>
> **ngrok の要件:** 自動起動は保存済みトークンの存在を確認し、なければ終了します。存在だけでは有効性を保証しないため、先に手動で起動を確認してください。

#### ステップ1: スタートアップサービスのインストール

プロジェクトのルートで通常ユーザーとして実行します。インストーラーの確認ツールで互換性のある uv を選び、サービス設定に使用します：

```bash
NINJAROBOT_UV="$(python3 -B scripts/install_check.py --find-tool uv)" &&
PATH="$(dirname -- "$NINJAROBOT_UV"):$PATH" .venv/bin/ninja_utils install-startup
```

これにより:

1. システムの準備ができているか確認します（configが存在するか、pigpiodが実行されているかなど）
2. systemdサービスファイルを作成します
3. 次回起動時に有効化します。この操作だけではロボットは起動しません。既存サービスは `uv run ninja_core server --autostart` を使うため、起動時に Python 依存関係を同期する場合があります。

#### ステップ2: 確認

サービスの状態を確認できます。手動起動または再起動までは、有効でも inactive（停止中）と表示されるのが通常です：

```bash
.venv/bin/ninja_utils status-startup
```

#### ステップ3: 再起動

Raspberry Piを再起動します:

```bash
sudo reboot
```

再起動後にサービスの状態を確認し、実際のホスト名または IP アドレス（例：`http://ninjarobotpi0.local:8000`）を使ってください。QR コードはディスプレイと公開トンネルが動作した場合だけ表示され、起動時間も環境に依存します。

> [!TIP]
> **シャットダウン:** Home の電源スライダーと確認操作で終了を要求します。表情・音・設定済みの `Poweroff` 動作を試みるため、ロボットを支えてください。OS 停止には `sudo shutdown` の権限が必要です。失敗時は SSH で `sudo shutdown -h now` を実行し、OS の停止を確認してから電源を抜いてください。LED の消灯だけでは停止を確認できません。

#### 自動起動の削除

ロボットの自動起動を停止したい場合:

```bash
.venv/bin/ninja_utils remove-startup
```

---

## 3. ファイル構成

```
NinjaRobotPi0/
├── ninja_core/               # サーバー本体: HAL・動作・AI・Web
├── ninja_ble/                # BLE GATT サービス
├── ninja_utils/              # 共有インターフェースとユーティリティ
├── ninja_webapp/             # React + Vite フロントエンド
├── pi0servo/                 # サーボドライバー
├── pi0disp/                  # LCD ディスプレイドライバー
├── pi0buzzer/                # ブザードライバー
├── pi0vl53l0x/               # 距離センサードライバー
├── ninjarobot_pi0_Wiki/      # プロジェクト Wiki
├── install.sh                # ワンコマンドインストーラー
├── onboard.sh                # 初期設定ウィザード
└── config.json               # ロボット設定ファイル
```

---

## 4. トラブルシューティング

### 更新後に `ninja_core` を起動できない場合

`Failed to spawn` / `No such file or directory` は CLI 起動ファイルがないことを示します。以前はルートと個別パッケージが同じ起動ファイルを所有していました。修正で重複を解消し、インストーラーが五つを再作成・確認します。稼働中のロボットを安全に停止してから（Poweroff が動く場合があります）、修正済みフォルダーで通常ユーザーとして実行してください：

```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev --reinstall-package ninja-core --reinstall-package pi0servo --reinstall-package pi0disp --reinstall-package pi0buzzer --reinstall-package pi0vl53l0x
uv run --no-sync ninja_core --help
./install.sh --check
```

校正・設定と既存の開発用パッケージは保持します。別のフォルダーでは修正の公開後に `git status`、`git pull --ff-only` の順に確認し、Git エラー時は停止してください。ヘルプ成功と実機準備の確認後のみ `uv run --no-sync ninja_core server` を実行します。起動はハードウェアを動かす場合があります。

### Python 導入前に停止する場合

`Stop pigpiod ... first` / `Stop ninjarobot ... first` は依存関係の導入**前**の停止です。この段階の `PASS: software prerequisites` は OS・パスの確認のみで、完了は **Software installed** です。`.venv/bin/ninja_core` やパッケージ情報がない場合は導入未完了です。

本体を支えてアクチュエータ電源を外してから、手動起動したロボットを停止します。ロボットサービスを先に停止し、既存フォルダで再実行してください：

```bash
sudo systemctl stop ninjarobot   # このサービスを導入・起動している場合のみ
sudo systemctl stop pigpiod
cd "$HOME/NinjaRobotPi0" && ./install.sh && ./install.sh --check
```

校正・設定を削除せず、再失敗時は最初のエラーを保存してください。`--check` は修復しません。完了後、ハードウェア使用前に pigpiod を再起動します。既存コードの更新は `git fetch origin HEAD && git merge --ff-only FETCH_HEAD` を使い、Git エラー時は停止してください。インストーラーは既存 Git ファイルを更新しません。


| 問題 | 解決方法 |
|---|---|
| `curl` が 404 を返す | リポジトリに公開後、再実行してください |
| 対応外プラットフォーム | Zero 2 W / aarch64 / Raspberry Pi OS 64-bit / Python 3.10+ / 通常ユーザーを確認 |
| ディスプレイが表示されない | SPI 有効化を確認：`sudo raspi-config` → SPI |
| サーボが動かない | `sudo systemctl status pigpiod` で起動確認。車輪を浮かせて再校正 |
| ポート 8000 が使用中 | 既存のサーバーインスタンスを停止してから再起動 |
| Gemini の設定失敗 | インターネット接続と API キーを確認。再試行: `./onboard.sh --step gemini` |

---

## 5. 付録

### 付録 A: Google Gemini API キー

1. [Google AI Studio](https://aistudio.google.com/) にアクセスしてログイン。
2. **Get API key** → **Create API key** をクリック。
3. プロジェクトを選択し、利用可能なモデル・割り当て・課金設定を確認。
4. 生成されたキーをコピーし、初期設定ウィザードの Gemini ステップで入力。

変更する場合：`./onboard.sh --step gemini`

> **注意:** 無料枠には使用制限があります。詳細は [Google AI の料金ページ](https://ai.google.dev/gemini-api/docs/pricing) をご確認ください。

### 付録 B: ngrok アカウント設定

1. [ngrok.com](https://ngrok.com/) で無料アカウントを作成。
2. ダッシュボードの **Your Authtoken** からトークンをコピー。
3. 初期設定ウィザードの ngrok ステップで入力。

変更する場合：`./onboard.sh --step ngrok`

> ⚠️ ngrok の公開 URL は他人に共有しないでください。URL を知っている人がロボットを操作できてしまいます。

---

### 付録 C: 互換性と確認用リファレンス

Bookworm/Trixie 64-bit は参照環境であり、OS コードネームの許可リストではありません。Zero 2 W、Linux `aarch64`、Debian 系 Raspberry Pi OS、通常ユーザー、Python 3.10+ が必要です。Node は 20.x の 20.19+ または 22.12.0 以降、uv は必要なコマンドに対応していれば完全一致の版は不要です。ソフトウェアの確認だけでは実機の動作を保証しません。

カスタムインストール先は未作成の絶対パスを指定し、親フォルダを先に作ってください。`sudo` を付けずにインストールします。`YOUR_USERNAME` とホスト名は Imager で設定した値に置き換えてください。

導入先で `./onboard.sh --status` は保存設定を確認し、`./onboard.sh --resume` は設定を再開します。実機確認とは別です。ハードウェアツールとサーバーを同時に実行しないでください。動作ツールは記録開始時にサーボを中央へ動かす場合があります。設定済みピンと安全な角度のみを使用し、個別速度は数値角度に付けます（`21:45F`、`21:XF` は不可）。

`config.json`（Gemini キーを含む場合があります）、ngrok 認証情報、校正ファイルを公開しないでください。料金・割り当て・利用可否はアカウントやモデルに依存します。Pi0 の操作画面にはログイン保護がなく、暗号化トンネルもアプリの認証を追加しません。信頼できるネットワークだけで使ってください。

詳細：[導入ガイド](InstallationGuide.md)、[開発ガイド](DevelopmentGuide.md)、[開発履歴](DevelopmentLog.md)。

<div align="center">

AI ロボティクス教育のために ❤️ を込めて作られました

</div>

---
---

<!-- 繁體中文 -->

# 繁體中文

更換模型：執行 `uv run ninja_core config select-model` 或 `./onboard.sh --step ai_model`，選擇 Google、OpenAI、Anthropic 或 Ollama Cloud，私下輸入 API 金鑰並驗證模型，然後手動重新啟動代理。Pi0 僅使用雲端推論；安裝程式會安裝 Ollama CLI，不下載本機模型或啟動守護程序，解壓暫存需 2 GB 可用空間。網頁麥克風輸入使用瀏覽器語音辨識，可搭配所有模型供應商；音訊檔上傳需要支援的 Gemini 模型。雲端呼叫可能產生費用。

## 1. 什麼是 NinjaRobotPi0？

**NinjaRobotPi0** 是一個以 **Raspberry Pi Zero 2 W**（一個口香糖大小的迷你電腦）為核心的開源教育機器人。它整合了伺服馬達（動作）、LCD 顯示螢幕（機器人的臉）、蜂鳴器（音效與旋律）、距離感測器、Google Gemini AI 對話、藍牙低功耗（BLE）以及瀏覽器控制介面——全部濃縮在一個小巧的套件中。

無論你想組裝輪型車、人形機器人或蜘蛛機器人，NinjaRobotPi0 都能幫助你學習軟體、AI 和硬體如何協同運作。

### 它能做什麼？

- **移動與表達** — 內建動作庫讓機器人行走、揮手、跳舞。LCD 顯示動畫表情，蜂鳴器播放情感音效。
- **感測距離** — VL53L0X 雷射感測器以毫米為單位量測距離，偵測障礙物。
- **AI 對話** — 連接 Google Gemini API 金鑰後即可和 AI 聊天，AI 還能觸發機器人動作。
- **手機操控** — 用任何裝置的瀏覽器開啟 Home、Agent（AI 聊天）和 Help 頁面，支援英文、日文、繁體中文、簡體中文。
- **循序漸進學習** — 用引導式工具校準每個元件，再依自己的節奏探索 Python 套件和 Web 介面。

---

## 2. 快速開始指南

### 2.1 推薦硬體

| 元件 | 規格 | 備註 |
|---|---|---|
| **電腦** | Raspberry Pi Zero 2 W（含 GPIO 排針） | 機器人的大腦 |
| **作業系統** | Raspberry Pi OS 64-bit（Bookworm / Trixie） | Debian 系，不需桌面 |
| **儲存** | microSD 卡 16 GB 以上 | 預留空間給依賴套件和前端建置 |
| **Pi 電源** | 5 V micro-USB 電源 | 僅供 Pi 使用 |
| **伺服馬達** | 最多 8 個 SG90 / MG90S 微型伺服 | 依車輪/手臂/腿的需求 |
| **伺服電源** | 獨立 5 V 3 A+ 電源 | 不可經由 Pi 電源引腳供電 |
| **顯示螢幕** | ST7789V SPI LCD 240×320 | 機器人的臉 |
| **距離感測器** | VL53L0X（I2C） | 雷射測距 |
| **蜂鳴器** | 被動式蜂鳴器（3–5 V） | 音效與旋律 |

### 2.2 接線

關閉電源後再接線。伺服馬達使用獨立電源，伺服電源的接地線與 Pi 的接地線共用（共地）。

| 元件 | 接線位置 |
|---|---|
| 伺服信號線（最多 8 條） | GPIO 20–27 |
| ST7789V SPI 資料 | MOSI → GPIO 10、SCLK → GPIO 11、CE0 → GPIO 8 |
| ST7789V 控制 | DC → GPIO 14、RST → GPIO 15、背光 → GPIO 16 |
| VL53L0X | SDA → GPIO 2、SCL → GPIO 3 |
| 蜂鳴器 | 信號 → GPIO 17 |

> ⚠️ **安全：** 通電時切勿更改接線。

GPIO 數字是 **BCM 編號**，不是實體排針序號。GPIO 使用 **3.3 V 邏輯**，不可輸入 5 V；請確認模組供電與驅動電路。伺服電源需依合計堵轉電流選擇；SG90/MG90S 定位伺服不提供車輪連續旋轉。

### 2.3 OS 安裝

1. 從 [raspberrypi.com/software](https://www.raspberrypi.com/software/) 下載 **Raspberry Pi Imager**。
2. 將 **Raspberry Pi OS 64-bit** 寫入 microSD 卡。設定主機名、SSH、Wi-Fi、使用者名稱。
3. 插入 Pi 並開機，用 SSH 連線：
   ```bash
   ssh YOUR_USERNAME@ninjarobotpi0.local
   ```
4. 執行 `sudo raspi-config` 啟用 **I2C** 和 **SPI**；若顯示器使用 GPIO 14/15，停用佔用這些腳位的序列主控台與 UART，需要時重新開機。

### 2.4 安裝專案

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

以一般使用者執行，輸入 `INSTALL` 確認。看到 **Software installed** 後才檢查並啟動 pigpiod（安裝程式不會啟動它或設定其自動啟動）：

```bash
cd "$HOME/NinjaRobotPi0" &&
./install.sh --check &&

# 啟動 pigpio（GPIO 硬體控制必需）：
sudo systemctl start pigpiod

# 選用：設定 pigpiod 開機自動啟動：
sudo systemctl enable pigpiod
```

**自訂安裝資料夾：**

```bash
mkdir -p "$HOME/Projects"
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash -s -- --install-dir "$HOME/Projects/NinjaRobotPi0"
```

> **重要：** 若使用自訂安裝資料夾，請將後續 `cd` 換成實際路徑。`pigpiod` 是伺服馬達、蜂鳴器等 GPIO 硬體控制的必要服務。

### 2.5 引導式初始設定

支撐好機器人後執行：

```bash
./onboard.sh
```

| 步驟 | 內容 |
|---|---|
| 1. 顯示螢幕 | GPIO 腳位設定、方向與亮度測試 |
| 2. 蜂鳴器 | 腳位設定、測試音播放 |
| 3. 伺服馬達 | 輸入 `READY` 後校準各伺服的範圍與中立點 |
| 4. 距離感測 | 確認與校準感測器讀數 |
| 5. 匯入設定 | 將設定匯入 `config.json` |
| 6. 名稱/類型 | 設定 BLE 名稱和機器人類型（`tire`/`humanoid`/`spider`） |
| 7. 選擇模型供應商 | 設定 Google / OpenAI / Anthropic / Ollama Cloud API 金鑰和模型 |
| 8. ngrok | 設定遠端存取權杖（選用） |

> ⚠️ **注意：** 伺服工具開啟時可能**立即移動**校準過的伺服馬達。請務必先支撐好機器人。

### 2.6 建立動作

```bash
.venv/bin/ninja_core movement-tool
```

個別移動伺服、記錄姿勢、播放動作序列。

**動作指令格式：**

```
[速度_]腳位:角度[速度][/腳位:角度[速度]...]
```

| 範例 | 動作內容 |
|---|---|
| `20:45` | 將 GPIO 20 以中速移動到 45° |
| `20:C` | 將 GPIO 20 移至中央（0°） |
| `S_20:45/21:-30` | 兩個伺服以慢速同步移動 |

**速度：** `F` = 快速、`M` = 中速（預設）、`S` = 慢速
**角度關鍵字：** `C` = 中央（0°）、`M` = 最小（−90°）、`X` = 最大（90°）

### 2.7 啟動伺服器與 Web 介面

伺服器會初始化硬體，可能將伺服移至中立位置。ngrok 提示可按 Enter 保留已儲存的權杖；輸入或更換權杖請使用精靈的隱藏輸入。略過 ngrok 設定仍會嘗試連線，並非僅限本機模式。

```bash
.venv/bin/ninja_core server
```

用瀏覽器開啟顯示的**本機 URL**（通常 `http://<Pi 位址>:8000`）。

| 頁面 | 功能 |
|---|---|
| **Home** | 機器人首頁、關機控制 |
| **Agent** | AI 聊天、表情、音效、動作 |
| **Help** | 使用指南、語言切換 |

---

### 2.8. 自動啟動（選用）

如果您希望機器人在開機時自動啟動，請按照以下步驟操作。

> [!IMPORTANT]
> **前提條件：** 確保您已完成所有先前步驟，包括硬體校準和 API 金鑰設定。在啟用自動啟動之前，機器人必須完全正常運作。
>
> **ngrok 要求：** 自動啟動會檢查是否已有權杖，若無則結束。權杖存在不代表有效，請先確認手動啟動成功。

#### 步驟1：安裝啟動服務

在專案根目錄以一般使用者執行。使用安裝程式的檢查工具選取相容的 uv，供服務設定使用：

```bash
NINJAROBOT_UV="$(python3 -B scripts/install_check.py --find-tool uv)" &&
PATH="$(dirname -- "$NINJAROBOT_UV"):$PATH" .venv/bin/ninja_utils install-startup
```

這將會：

1. 檢查您的系統是否準備就緒（config 存在、pigpiod 正在執行等）
2. 建立 systemd 服務檔案
3. 設定下次開機自動啟動，不會立即啟動機器人。既有服務使用 `uv run ninja_core server --autostart`，可能在啟動時同步 Python 依賴套件。

#### 步驟2：驗證

您可以檢查服務狀態；手動啟動或重新開機前，已啟用但顯示 inactive（未執行）是正常的：

```bash
.venv/bin/ninja_utils status-startup
```

#### 步驟3：重新啟動

重新啟動您的 Raspberry Pi：

```bash
sudo reboot
```

重新開機後再次檢查服務狀態，使用實際主機名稱或 IP 位址（例如 `http://ninjarobotpi0.local:8000`）。QR 碼只在顯示器和公開通道成功運作時顯示，啟動時間依環境而異。

> [!TIP]
> **關機：** 使用 Home 的電源滑桿並確認後，系統會嘗試播放表情、音效及設定的 `Poweroff` 動作，請支撐好機器人。OS 關機需要執行 `sudo shutdown` 的權限；失敗時可透過 SSH 執行 `sudo shutdown -h now`。確認 OS 已停止後再斷電，不能只以 LED 不閃爍判斷。

#### 移除自動啟動

如果您想停止機器人自動啟動：

```bash
.venv/bin/ninja_utils remove-startup
```

---

## 3. 檔案結構

```
NinjaRobotPi0/
├── ninja_core/               # 伺服器核心：HAL、動作、AI、Web
├── ninja_ble/                # BLE GATT 服務
├── ninja_utils/              # 共用介面與工具程式
├── ninja_webapp/             # React + Vite 前端
├── pi0servo/                 # 伺服馬達驅動程式
├── pi0disp/                  # LCD 顯示驅動程式
├── pi0buzzer/                # 蜂鳴器驅動程式
├── pi0vl53l0x/               # 距離感測器驅動程式
├── ninjarobot_pi0_Wiki/      # 專案 Wiki 知識庫
├── install.sh                # 一鍵安裝程式
├── onboard.sh                # 引導式設定精靈
└── config.json               # 機器人設定檔
```

---

## 4. 疑難排解

### 更新後無法啟動 `ninja_core`

`Failed to spawn` / `No such file or directory` 表示 CLI 啟動檔不存在，不是伺服器設定遭拒。舊版根專案與個別套件重複擁有相同啟動檔；此次修正移除重複，安裝程式會重建並檢查五個啟動檔。先安全停止正在執行的機器人（可能執行 Poweroff），再於含修正的資料夾以一般使用者執行：

```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev --reinstall-package ninja-core --reinstall-package pi0servo --reinstall-package pi0disp --reinstall-package pi0buzzer --reinstall-package pi0vl53l0x
uv run --no-sync ninja_core --help
./install.sh --check
```

保留設定、校準及現有開發套件。其他工作目錄須等修正發布後先查看 `git status`，再執行 `git pull --ff-only`；Git 出錯時停止並保留本機修改。僅在說明指令成功且硬體準備完成後才執行 `uv run --no-sync ninja_core server`；啟動可能驅動硬體。

### 在安裝 Python 套件前停止

`Stop pigpiod ... first` / `Stop ninjarobot ... first` 代表在安裝依賴套件**前**停止。此時的 `PASS: software prerequisites` 只表示平台與路徑預檢通過，**Software installed** 才代表完成。缺少 `.venv/bin/ninja_core` 或套件中繼資料表示尚未安裝完整。

支撐好本體並切斷致動器電源，再停止手動執行的機器人。先停止機器人服務，再從既有資料夾重試：

```bash
sudo systemctl stop ninjarobot   # 僅限已安裝／執行此服務時
sudo systemctl stop pigpiod
cd "$HOME/NinjaRobotPi0" && ./install.sh && ./install.sh --check
```

保留校準與設定；再次失敗時記錄第一個錯誤。`--check` 不會修復環境。完成後，操作硬體前需重新啟動 pigpiod。若需先更新程式，使用 `git fetch origin HEAD && git merge --ff-only FETCH_HEAD`，Git 報錯就停止。安裝程式不會更新既有 Git 檔案。


| 問題 | 解決方法 |
|---|---|
| `curl` 回傳 404 | 請確認已發佈至官方儲存庫 |
| 不支援的平台 | 確認 Zero 2 W / aarch64 / Raspberry Pi OS 64-bit / Python 3.10+ / 一般使用者 |
| 顯示螢幕不亮 | 確認 SPI 已啟用：`sudo raspi-config` → SPI |
| 伺服馬達不動 | 確認 `pigpiod` 正在執行：`sudo systemctl status pigpiod`。抬起輪子重新校準 |
| 連接埠 8000 被佔用 | 停止已執行的伺服器後再啟動 |
| Gemini 設定失敗 | 確認網路連線與 API 金鑰。重試：`./onboard.sh --step gemini` |

---

## 5. 附錄

### 附錄 A：Google Gemini API 金鑰

1. 前往 [Google AI Studio](https://aistudio.google.com/) 並登入。
2. 點選 **Get API key** → **Create API key**。
3. 選擇或建立專案，確認模型可用性、配額與計費設定。
4. 複製產生的金鑰，在初始設定精靈的 Gemini 步驟中貼上。

變更金鑰：`./onboard.sh --step gemini`

> **注意：** 免費方案有使用限制。詳情請參閱 [Google AI 定價頁面](https://ai.google.dev/gemini-api/docs/pricing)。

### 附錄 B：ngrok 帳號設定

1. 前往 [ngrok.com](https://ngrok.com/) 註冊免費帳號。
2. 在儀表板的 **Your Authtoken** 複製權杖。
3. 在初始設定精靈的 ngrok 步驟中貼上。

變更權杖：`./onboard.sh --step ngrok`

> ⚠️ 切勿與他人分享 ngrok 公開 URL。知道 URL 的人可以操控你的機器人。

---

### 附錄 C：相容性與檢查參考

Bookworm/Trixie 64-bit 是參考環境，不是 OS 代號白名單。需使用 Zero 2 W、Linux `aarch64`、Debian 系 Raspberry Pi OS、一般使用者及 Python 3.10+。Node 需為 20.x 的 20.19+ 或 >=22.12.0；uv 只檢查必要指令能力，不要求固定版本。軟體檢查通過不代表實機驗收完成。

自訂安裝路徑必須是尚不存在的絕對路徑，先建立其父資料夾。安裝時不要加 `sudo`。請將 `YOUR_USERNAME` 與主機名稱換成 Imager 中設定的值。

在安裝目錄執行 `./onboard.sh --status` 檢查已儲存的設定，`./onboard.sh --resume` 繼續設定；這不等於實機驗證。勿同時執行硬體工具與伺服器。動作工具開始錄製時可能將伺服移至中立位置；只使用已設定的腳位和安全角度。個別速度後綴需接在數字角度後（`21:45F`，不可用 `21:XF`）。

保護 `config.json`（可能含 Gemini 金鑰）、ngrok 憑證與校準檔案，切勿公開。費率、配額與可用性依帳號及模型而異。Pi0 控制介面沒有使用者登入保護；加密通道不會增加應用程式驗證，請只在可信任網路使用。

詳細資料：[安裝指南](InstallationGuide.md)、[開發指南](DevelopmentGuide.md)、[開發紀錄](DevelopmentLog.md)。

<div align="center">

以 ❤️ 為 AI 機器人教育而製作

</div>

---
---

<!-- 简体中文 -->

# 简体中文

更换模型：运行 `uv run ninja_core config select-model` 或 `./onboard.sh --step ai_model`，选择 Google、OpenAI、Anthropic 或 Ollama Cloud，私下输入 API 密钥并验证模型，然后手动重启代理。Pi0 仅使用云端推理；安装程序会安装 Ollama CLI，不下载本地模型或启动守护进程，解压临时文件需要 2 GB 可用空间。网页麦克风输入使用浏览器语音识别，可搭配所有模型提供商；音频文件上传需要受支持的 Gemini 模型。云端调用可能产生费用。

## 1. 什么是 NinjaRobotPi0？

**NinjaRobotPi0** 是一个以 **Raspberry Pi Zero 2 W**（一个口香糖大小的迷你电脑）为核心的开源教育机器人。它集成了舵机（动作）、LCD 显示屏（机器人的脸）、蜂鸣器（音效与旋律）、距离传感器、Google Gemini AI 对话、蓝牙低功耗（BLE）以及浏览器控制界面——全部浓缩在一个小巧的套件中。

无论你想组装轮式车、人形机器人还是蜘蛛机器人，NinjaRobotPi0 都能帮助你学习软件、AI 和硬件如何协同工作。

### 它能做什么？

- **移动与表达** — 内置动作库让机器人行走、挥手、跳舞。LCD 显示动画表情，蜂鸣器播放情感音效。
- **感测距离** — VL53L0X 激光传感器以毫米为单位测量距离，检测障碍物。
- **AI 对话** — 连接 Google Gemini API 密钥后即可和 AI 聊天，AI 还能触发机器人动作。
- **手机操控** — 用任何设备的浏览器打开 Home、Agent（AI 聊天）和 Help 页面，支持英文、日文、繁体中文、简体中文。
- **循序渐进学习** — 用引导式工具校准每个组件，再按自己的节奏探索 Python 包和 Web 界面。

---

## 2. 快速开始指南

### 2.1 推荐硬件

| 组件 | 规格 | 备注 |
|---|---|---|
| **计算机** | Raspberry Pi Zero 2 W（带 GPIO 排针） | 机器人的大脑 |
| **操作系统** | Raspberry Pi OS 64-bit（Bookworm / Trixie） | Debian 系，不需桌面 |
| **存储** | microSD 卡 16 GB 以上 | 预留空间给依赖包和前端构建 |
| **Pi 电源** | 5 V micro-USB 电源 | 仅供 Pi 使用 |
| **舵机** | 最多 8 个 SG90 / MG90S 微型舵机 | 按车轮/手臂/腿的需求选配 |
| **舵机电源** | 独立 5 V 3 A+ 电源 | 不可通过 Pi 电源引脚供电 |
| **显示屏** | ST7789V SPI LCD 240×320 | 机器人的脸 |
| **距离传感器** | VL53L0X（I2C） | 激光测距 |
| **蜂鸣器** | 无源蜂鸣器（3–5 V） | 音效与旋律 |

### 2.2 接线

断电后再接线。舵机使用独立电源，舵机电源的接地线与 Pi 的接地线共用（共地）。

| 组件 | 接线位置 |
|---|---|
| 舵机信号线（最多 8 条） | GPIO 20–27 |
| ST7789V SPI 数据 | MOSI → GPIO 10、SCLK → GPIO 11、CE0 → GPIO 8 |
| ST7789V 控制 | DC → GPIO 14、RST → GPIO 15、背光 → GPIO 16 |
| VL53L0X | SDA → GPIO 2、SCL → GPIO 3 |
| 蜂鸣器 | 信号 → GPIO 17 |

> ⚠️ **安全：** 通电时切勿更改接线。

GPIO 数字是 **BCM 编号**，不是物理排针序号。GPIO 使用 **3.3 V 逻辑**，不可输入 5 V；请确认模块供电与驱动电路。舵机电源应按总堵转电流选择；SG90/MG90S 位置舵机不提供车轮连续旋转。

### 2.3 OS 安装

1. 从 [raspberrypi.com/software](https://www.raspberrypi.com/software/) 下载 **Raspberry Pi Imager**。
2. 将 **Raspberry Pi OS 64-bit** 写入 microSD 卡。设置主机名、SSH、Wi-Fi、用户名。
3. 插入 Pi 并开机，用 SSH 连接：
   ```bash
   ssh YOUR_USERNAME@ninjarobotpi0.local
   ```
4. 运行 `sudo raspi-config` 启用 **I2C** 和 **SPI**；若显示屏使用 GPIO 14/15，禁用占用这些引脚的串口控制台和 UART，需要时重启。

### 2.4 安装项目

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

以普通用户运行，输入 `INSTALL` 确认。看到 **Software installed** 后再检查并启动 pigpiod（安装程序不会启动它或设置其自启动）：

```bash
cd "$HOME/NinjaRobotPi0" &&
./install.sh --check &&

# 启动 pigpio（GPIO 硬件控制必需）：
sudo systemctl start pigpiod

# 可选：设置 pigpiod 开机自启动：
sudo systemctl enable pigpiod
```

**自定义安装文件夹：**

```bash
mkdir -p "$HOME/Projects"
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash -s -- --install-dir "$HOME/Projects/NinjaRobotPi0"
```

> **重要：** 若选择自定义安装文件夹，请将后续 `cd` 换成实际路径。`pigpiod` 是舵机、蜂鸣器等 GPIO 硬件控制的必要服务。

### 2.5 引导式初始设置

支撑好机器人后运行：

```bash
./onboard.sh
```

| 步骤 | 内容 |
|---|---|
| 1. 显示屏 | GPIO 引脚设置、方向与亮度测试 |
| 2. 蜂鸣器 | 引脚设置、测试音播放 |
| 3. 舵机 | 输入 `READY` 后校准各舵机的范围与中立点 |
| 4. 距离传感 | 确认与校准传感器读数 |
| 5. 导入设置 | 将设置导入 `config.json` |
| 6. 名称/类型 | 设置 BLE 名称和机器人类型（`tire`/`humanoid`/`spider`） |
| 7. 选择模型提供商 | 设置 Google / OpenAI / Anthropic / Ollama Cloud API 密钥和模型 |
| 8. ngrok | 设置远程访问令牌（可选） |

> ⚠️ **注意：** 舵机工具打开时可能**立即移动**校准过的舵机。请务必先支撑好机器人。

### 2.6 创建动作

```bash
.venv/bin/ninja_core movement-tool
```

单独移动舵机、记录姿势、播放动作序列。

**动作命令格式：**

```
[速度_]引脚:角度[速度][/引脚:角度[速度]...]
```

| 示例 | 动作内容 |
|---|---|
| `20:45` | 将 GPIO 20 以中速移至 45° |
| `20:C` | 将 GPIO 20 移至中央（0°） |
| `S_20:45/21:-30` | 两个舵机以慢速同步移动 |

**速度：** `F` = 快速、`M` = 中速（默认）、`S` = 慢速
**角度关键字：** `C` = 中央（0°）、`M` = 最小（−90°）、`X` = 最大（90°）

### 2.7 启动服务器与 Web 界面

服务器会初始化硬件，可能将舵机移至中立位置。ngrok 提示可按 Enter 保留已保存的令牌；输入或更换令牌请使用向导的隐藏输入。跳过 ngrok 设置仍会尝试连接，并非仅限本地模式。

```bash
.venv/bin/ninja_core server
```

用浏览器打开显示的**本地 URL**（通常 `http://<Pi 地址>:8000`）。

| 页面 | 功能 |
|---|---|
| **Home** | 机器人首页、关机控制 |
| **Agent** | AI 聊天、表情、音效、动作 |
| **Help** | 使用指南、语言切换 |

---

### 2.8 自动启动（可选）

完成硬件校准、API 密钥设置并确认手动运行正常后，才启用自动启动。
自启动会检查 ngrok 令牌是否存在，若无则退出；存在不代表有效，请先手动验证。

#### 步骤 1：安装启动服务

在项目根目录以普通用户运行。使用安装程序的检查工具选择兼容的 uv，供服务配置使用：

```bash
NINJAROBOT_UV="$(python3 -B scripts/install_check.py --find-tool uv)" &&
PATH="$(dirname -- "$NINJAROBOT_UV"):$PATH" .venv/bin/ninja_utils install-startup
```

该工具检查 `config.json`、pigpiod、ninja_core 和 uv，创建并启用 `ninjarobot.service`，但不会立即启动机器人。
现有服务使用 `uv run ninja_core server --autostart`，可能在启动时同步 Python 依赖包。

#### 步骤 2：查看状态

手动启动或重启前，已启用但显示 inactive（未运行）是正常的。

```bash
.venv/bin/ninja_utils status-startup
```

#### 步骤 3：重启

```bash
sudo reboot
```

重启后再次检查状态，使用实际主机名或 IP 地址（例如 `http://ninjarobotpi0.local:8000`）。
二维码仅在显示屏和公开隧道成功工作时显示，启动时间因环境而异。

> **关机：** 使用 Home 的电源滑块并确认后，系统会尝试播放表情、音效及配置的 `Poweroff` 动作，请支撑好机器人。OS 关机需要执行 `sudo shutdown` 的权限；失败时可通过 SSH 执行 `sudo shutdown -h now`。确认 OS 已停止后再断电，不能只凭 LED 不闪烁判断。

#### 移除自启动

```bash
.venv/bin/ninja_utils remove-startup
```

---

## 3. 文件结构

```
NinjaRobotPi0/
├── ninja_core/               # 服务器核心：HAL、动作、AI、Web
├── ninja_ble/                # BLE GATT 服务
├── ninja_utils/              # 共享接口与工具程序
├── ninja_webapp/             # React + Vite 前端
├── pi0servo/                 # 舵机驱动程序
├── pi0disp/                  # LCD 显示驱动程序
├── pi0buzzer/                # 蜂鸣器驱动程序
├── pi0vl53l0x/               # 距离传感器驱动程序
├── ninjarobot_pi0_Wiki/      # 项目 Wiki 知识库
├── install.sh                # 一键安装程序
├── onboard.sh                # 引导式设置向导
└── config.json               # 机器人配置文件
```

---

## 4. 故障排除

### 更新后无法启动 `ninja_core`

`Failed to spawn` / `No such file or directory` 表示 CLI 启动文件不存在，不是服务器配置遭拒。旧版根项目与各个包重复拥有相同启动文件；此次修正移除重复，安装程序会重建并检查五个启动文件。先安全停止正在运行的机器人（可能执行 Poweroff），再在包含修正的目录中以普通用户执行：

```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev --reinstall-package ninja-core --reinstall-package pi0servo --reinstall-package pi0disp --reinstall-package pi0buzzer --reinstall-package pi0vl53l0x
uv run --no-sync ninja_core --help
./install.sh --check
```

保留配置、校准及现有开发包。其他工作目录须等修正发布后先查看 `git status`，再执行 `git pull --ff-only`；Git 出错时停止并保留本机修改。仅在帮助命令成功且硬件准备完成后才运行 `uv run --no-sync ninja_core server`；启动可能驱动硬件。

### 在安装 Python 包之前停止

`Stop pigpiod ... first` / `Stop ninjarobot ... first` 表示在安装依赖包**之前**停止。此时的 `PASS: software prerequisites` 只表示平台及路径预检通过，**Software installed** 才代表完成。缺少 `.venv/bin/ninja_core` 或包元数据表示安装不完整。

支撑好机体并断开执行器电源，再停止手动运行的机器人。先停止机器人服务，再从现有文件夹重试：

```bash
sudo systemctl stop ninjarobot   # 仅在已安装／运行此服务时
sudo systemctl stop pigpiod
cd "$HOME/NinjaRobotPi0" && ./install.sh && ./install.sh --check
```

保留校准与配置；再次失败时记录第一个错误。`--check` 不会修复环境。完成后，使用硬件前需重新启动 pigpiod。若需先更新代码，使用 `git fetch origin HEAD && git merge --ff-only FETCH_HEAD`，Git 报错就停止。安装程序不会更新现有 Git 文件。


| 问题 | 解决方法 |
|---|---|
| `curl` 返回 404 | 请确认已发布至官方仓库 |
| 不支持的平台 | 确认 Zero 2 W / aarch64 / Raspberry Pi OS 64-bit / Python 3.10+ / 普通用户 |
| 显示屏不亮 | 确认 SPI 已启用：`sudo raspi-config` → SPI |
| 舵机不动 | 确认 `pigpiod` 正在运行：`sudo systemctl status pigpiod`。抬起轮子重新校准 |
| 端口 8000 被占用 | 停止已运行的服务器后再启动 |
| Gemini 设置失败 | 确认网络连接与 API 密钥。重试：`./onboard.sh --step gemini` |

---

## 5. 附录

### 附录 A：Google Gemini API 密钥

1. 前往 [Google AI Studio](https://aistudio.google.com/) 并登录。
2. 点击 **Get API key** → **Create API key**。
3. 选择或创建项目，确认模型可用性、配额及计费设置。
4. 复制生成的密钥，在初始设置向导的 Gemini 步骤中粘贴。

变更密钥：`./onboard.sh --step gemini`

> **注意：** 免费套餐有使用限制。详情请参阅 [Google AI 定价页面](https://ai.google.dev/gemini-api/docs/pricing)。

### 附录 B：ngrok 账号设置

1. 前往 [ngrok.com](https://ngrok.com/) 注册免费账号。
2. 在仪表盘的 **Your Authtoken** 复制令牌。
3. 在初始设置向导的 ngrok 步骤中粘贴。

变更令牌：`./onboard.sh --step ngrok`

> ⚠️ 切勿与他人分享 ngrok 公开 URL。知道 URL 的人可以操控你的机器人。

---

### 附录 C：兼容性与检查参考

Bookworm/Trixie 64-bit 是参考环境，不是 OS 代号白名单。需要 Zero 2 W、Linux `aarch64`、Debian 系 Raspberry Pi OS、普通用户及 Python 3.10+。Node 需为 20.x 的 20.19+ 或 >=22.12.0；uv 只检查必要命令能力，不要求固定版本。软件检查通过不代表实机验收完成。

自定义安装路径必须是尚不存在的绝对路径，先创建其父文件夹。安装时不要加 `sudo`。请将 `YOUR_USERNAME` 和主机名换成 Imager 中配置的值。

在安装目录运行 `./onboard.sh --status` 检查已保存的配置，`./onboard.sh --resume` 继续设置；这不等于实机验证。不要同时运行硬件工具和服务器。动作工具开始录制时可能将舵机移至中立位置；只使用已配置的引脚及安全角度。单独速度后缀需接在数字角度后（`21:45F`，不能用 `21:XF`）。

保护 `config.json`（可能包含 Gemini 密钥）、ngrok 凭据和校准文件，不要公开。费用、配额与可用性依账号及模型而异。Pi0 控制界面没有用户登录保护；加密隧道不会添加应用身份验证，请仅在可信网络使用。

详细资料：[安装指南](InstallationGuide.md)、[开发指南](DevelopmentGuide.md)、[开发记录](DevelopmentLog.md)。

<div align="center">

以 ❤️ 为 AI 机器人教育而制作

</div>
