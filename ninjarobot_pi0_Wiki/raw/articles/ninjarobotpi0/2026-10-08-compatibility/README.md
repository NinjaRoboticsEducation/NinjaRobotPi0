# NinjaRobotPi0

<div align="center">

**An educational Raspberry Pi Zero 2 W robot — build it, program it, and bring it to life**

Raspberry Pi OS 64-bit · Python 3.10+ (host-tested: 3.11/3.13) · Google Gemini · Browser and BLE control

</div>

**Language / 言語 / 語言 / 语言:**
[English](#english) · [日本語](#日本語) · [繁體中文](#繁體中文) · [简体中文](#简体中文)

# English

## 1. What Is NinjaRobotPi0?

NinjaRobotPi0 is a modular educational robot for **Raspberry Pi Zero 2 W**. It brings together servo movement, an expressive LCD face, buzzer sounds, distance sensing, Google Gemini chat, Bluetooth Low Energy (BLE), and a browser interface. Students and makers can explore how software, AI and physical components work together; developers can extend the existing Python packages and web interface.

### What can it do?

- **Move and express itself:** use the existing movement library, display expressions and buzzer sounds.
- **Sense distance:** view readings from a VL53L0X sensor in millimetres.
- **Use cloud AI:** configure a Google Gemini API key and select a model through the guided setup. Chat can invoke robot actions; keep the robot supported during first tests.
- **Connect through a browser:** Home, Agent and Help share NinjaRobotPi5's navy/cyan design, with English, Japanese, Traditional Chinese and Simplified Chinese UI text.
- **Learn incrementally:** calibrate with the existing `pi0*` tools, then explore the core, BLE, utility and frontend packages.

Pi0 retains its own capabilities and control protocol. Pi5's local model providers, camera, game pad, MCP integrations and authenticated pairing are not included. The original Python package names and robot functions are preserved; some existing tools still display legacy V4/V5 labels.

**Release qualification:** host validation is recorded in the [compatibility report](../../../../../docs/validation/InstallerCompatibility-2026-10-08.md). Physical Pi installation, calibration and account testing remain pending. Publish this update before fetching it on your Pi.

## 2. Quick Start Guide

### 2.1 Hardware and supported operating system

| Component | Pi0 setup |
| --- | --- |
| Computer | Raspberry Pi Zero 2 W with GPIO header |
| OS | **Debian-based Raspberry Pi OS 64-bit**; Python 3.10+; no codename allowlist |
| Storage | microSD card, 16 GB or larger; allow free space for dependencies and the frontend build |
| Pi power | Suitable regulated 5 V supply through the Pi's micro-USB power input |
| Servos | Appropriate servos for your tire, humanoid or spider build; calibrate every connected servo |
| Servo power | Separate supply rated for the connected servos, with a common ground to the Pi |
| Display | ST7789V SPI LCD, 240 × 320 |
| Sensor | VL53L0X I2C distance sensor |
| Sound | Passive buzzer |
| Setup access | Terminal or SSH, internet, and a normal user with sudo access |

### 2.2 Wiring and preparation

Power off before wiring. Keep actuator power disconnected while installing software. Servo supply current must not pass through the Pi's power pins. Connect the external supply ground and Pi ground together.

| Component | Reference connections (BCM GPIO numbers) |
| --- | --- |
| Servo signal wires | Existing eight-servo reference uses GPIO20–27; use the pins actually wired for your build |
| Display SPI | MOSI GPIO10 / physical pin 19; SCLK GPIO11 / pin 23; CE0 GPIO8 / pin 24 |
| Display control | Configurable DC, RST and backlight; reference layout uses GPIO14, GPIO15 and GPIO16 |
| Distance sensor | SDA GPIO2 / pin 3; SCL GPIO3 / pin 5; compatible 3.3 V breakout and common ground |
| Buzzer | Reference signal GPIO17 / pin 11, with ground |

Use your module's wiring and voltage requirements. Do not allocate the same GPIO to two components. Display pins are configurable; register your actual assignments in the display tool. The [complete installation manual](InstallationGuide.md) retains the detailed wiring reference. Its older manual installation commands are explicitly historical.

### 2.3 Prepare Raspberry Pi OS

1. Write **Raspberry Pi OS Bookworm/Trixie 64-bit** to the microSD card using Raspberry Pi Imager. Bookworm (Debian 12) and Trixie (Debian 13) are reference targets; see compatibility requirements below.
2. Set your username/password, hostname and Wi-Fi; enable SSH if using a remote terminal. Boot and log in as your normal user.
3. Run `sudo raspi-config` and enable **I2C** and **SPI** for your components. If using GPIO14/15 for the display, disable the serial login console so it does not own those pins. Reboot manually if requested.
4. Verify the target before installation:

```bash
uname -m                         # aarch64
cat /etc/os-release              # VERSION_CODENAME=bookworm or trixie
tr -d '\0' < /proc/device-tree/model
```

### 2.4 Install the project

Run this in your Pi's normal-user terminal **after the upgrade is published**:

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

`HEAD` follows the repository's **default branch**, even if its name changes. Read the displayed operations and type `INSTALL` when prompted. The bootstrap creates `$HOME/NinjaRobotPi0`, records the resolved commit, and runs its local installer. It may ask for confirmation again before the system/package installation stage. Do not prefix the command with sudo.

For download-and-inspect installation, use a new temporary file; Bash runs only after a successful download and inspection:

```bash
installer=$(mktemp) &&
  curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh -o "$installer" &&
  less "$installer" && bash "$installer"
```

To select a published commit, replace `FULL_COMMIT_SHA` below with its full 40-character hash in both places:

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/FULL_COMMIT_SHA/install.sh |
  bash -s -- --ref FULL_COMMIT_SHA
```

The installer provisions prerequisites, compatible Node/uv (verified fallbacks if needed) and pinned pigpio tooling, locked Python dependencies in `.venv`, and the built web interface. It does **not** calibrate hardware, collect credentials, start the robot, enable boot startup or reboot. Keep hardware activation separate.

Once installation finishes:

```bash
cd "$HOME/NinjaRobotPi0"
./install.sh --check
./onboard.sh --dry-run
```

If you already have this revision locally, or are validating it before publication:

```bash
cd /path/to/NinjaRobotPi0
./install.sh --dry-run
./install.sh
./install.sh --check
```

Rerun the **local** installer after a failed installation. Bootstrap refuses to overwrite an existing destination. Local installation retains the checkout's current revision; it is not an automatic Git updater. `--install-dir /absolute/new/path` and `--ref` are bootstrap options. `--with-wiki` additionally installs the separate developer wiki environment. Compatible existing tools are reused, and fallback downloads are private to this installation; the runtime commands below use `.venv/bin` and do not depend on a globally installed `uv`.

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
  `--python`, `--directory`, and `--all-extras`. uv 0.9.26 satisfies this and passed an
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

日本語：OS のコードネームと Node/uv の完全一致チェックを廃止し、実際の必要条件を確認します。
互換性のある既存ツールを再利用します。`.venv` がない場合は `./install.sh` による導入が必要です。
繁體中文：取消 OS 代號及 Node/uv 的固定版本比對，改查實際需求並重用相容工具。
缺少 `.venv` 時仍須執行 `./install.sh` 完成安裝；實機驗收另行進行。
简体中文：取消 OS 代号及 Node/uv 的固定版本比对，改查实际需求并复用兼容工具。
缺少 `.venv` 时仍须运行 `./install.sh` 完成安装；实机验收单独进行。

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

日本語：`--check` は確認のみです。既存フォルダーで上記の Git 更新が成功した後、
`./install.sh` を実行し、Software installed の表示を待ってから `--check` を実行します。
Git 更新が失敗したら停止し、校正や設定を削除しないでください。導入失敗時は段階名と最初のエラーを確認します。

繁體中文：`--check` 只檢查、不安裝。既有專案請先以上述 Git 指令更新，成功後執行
`./install.sh`，看到 Software installed 再執行 `--check`。Git 更新失敗時請停止，不要刪除校準或設定。
安裝失敗會顯示階段與重試指令，請保留第一個錯誤訊息。

简体中文：`--check` 只检查、不安装。已有项目先按上述 Git 命令更新，成功后运行
`./install.sh`，看到 Software installed 再运行 `--check`。更新失败请停止并保留配置；安装失败请保留阶段和首个错误。

### 2.5 Guided initialization and calibration

Stop any existing robot server before standalone calibration. Prepare the wiring and interfaces, support every limb/wheel, and remain ready to remove actuator power. Deliberately activate pigpio when ready:

```bash
sudo systemctl start pigpiod
./onboard.sh
```

The terminal wizard follows Pi5's welcome screen, numbered steps, “What / Why / What to do” guidance, saved-setting reuse, retry, and summary flow. It calls the existing Pi0 tools. Opening the servo tool can immediately center previously configured servos, **before its own menu appears**.

| Step | What you do | Successful check |
| --- | --- | --- |
| 1. Display | Open the display tool, enter actual pins, set orientation/brightness and test output | Readable display and valid saved settings |
| 2. Buzzer | Configure the pin and play a short tone | Audible output followed by silence |
| 3. Servo | Type `READY` only after supporting the robot; calibrate each connected servo | Appropriate limits/neutral point and valid saved pulses |
| 4. Distance | Inspect readings, then calibrate against a target at a measured distance | Plausible readings and a saved offset |
| 5. Import | Import saved display, buzzer and servo settings into `config.json` | Import is blocked until these files validate; sensor settings remain separate |
| 6. Identity | Set a BLE name and choose `tire`, `humanoid` or `spider` | Name/type match your build |
| 7. Gemini | Enter your API key privately, choose a discovered model, allow validation | Existing helper saves the validated model/key; internet and account access required |
| 8. ngrok | Optionally enter your ngrok authtoken privately | Token saved using existing storage; no tunnel opens during onboarding |

When valid settings exist, select **2) Apply existing settings for all modules** to reuse them and configure remaining modules. Each hardware step offers **1) Open setup tool**, **2) Reuse validated settings** when valid, and **Q) Save and exit**. Failed tools can be retried immediately. Review the result and press Enter to continue. Settings/account steps can be skipped without replacing existing values.

Software validation and physical observation are separate. Reuse never invents a physical check. `--resume` skips previously validated hardware only while its file is unchanged and still valid. Changed files clear the recorded physical observation. Account steps remain available on resume; saved credentials are not revalidated automatically.

```bash
./onboard.sh --status          # Read-only progress and current saved-file validity
./onboard.sh --resume          # Resume; recheck saved hardware fingerprints
./onboard.sh --step servo      # Open one step deliberately
./onboard.sh --step import     # Re-import after changing hardware calibration
./onboard.sh --step gemini     # Change key or selected model
./onboard.sh --step ngrok      # Configure remote-access token
```

Q or Ctrl+C saves progress. Let an active hardware tool complete cleanup; if cleanup is uncertain, disconnect actuator power. Credentials are excluded from progress, which is stored privately under `~/.local/state/ninjarobot_pi0/` or `$XDG_STATE_HOME/ninjarobot_pi0/`. The wizard does not launch the server on exit.

### 2.6 Start the existing robot server deliberately

Keep the robot supported for the first start. From the project root:

```bash
.venv/bin/ninja_core server
```

The server initializes devices and can center servos. Its existing startup asks about ngrok; press Enter to keep the token already entered privately through onboarding. If no token was configured, Enter continues without saving a new one, but the existing runtime still attempts ngrok connections. **Skipping onboarding's ngrok step is not a network-isolation mode.** With a usable token, server startup can open a public tunnel and display its URL/QR code.

Pi0's existing control interface does not gain Pi5's pairing/authentication through this design update. Use a trusted network and treat a public control URL as sensitive. No boot service is enabled by this walkthrough.

### 2.7 Open the web interface

Open the server's printed **Local Access** URL, normally `http://<pi-address>:8000`, from a device on the same network. If the runtime reports **Public Access**, that is the ngrok URL. Use the URL actually printed by your Pi.

- **Home:** robot entry page and deliberate power-off control.
- **Agent:** Gemini chat, existing expressions/sounds/movements, distance and activity messages.
- **Help:** usage guidance; the menu also selects the interface language.

The BLE badge means **advertising**, not that a controller is connected. Browser speech input depends on browser support and permissions; local HTTP access may restrict it. Typed chat remains available. The shutdown slider asks for confirmation before sending the existing power-off request.

## 3. First Test Checklist

Perform these checks on the physical Pi in order. Host unit tests cannot substitute for them.

1. **Software:** `./install.sh --check` passes. Read `./onboard.sh --status`; resolve any pending/attention items.
2. **Calibration:** complete each existing device tool, record actual observations and run the import step after changes. Test one component at a time with the robot supported.
3. **Server start:** start manually and confirm expected startup behavior, readable display and no unexpected motion. Keep hands clear of travel.
4. **Web display:** open Home, Agent and Help on a phone; check all four UI languages and the menu. Confirm distance changes plausibly when a target moves.
5. **Single actions:** deliberately select one expression, one short sound, then one movement with the robot supported. Confirm expected physical results before progressing.
6. **Gemini:** send a simple greeting; then test one intended robot action with supervision. Confirm the selected model/account works and review activity messages.
7. **Remote access, if needed:** verify the printed ngrok URL using your own device. A saved token alone is not proof of a working tunnel.
8. **Exit/recovery:** stop the server with Ctrl+C, let cleanup finish, then test onboarding resume. Test power-off separately only when ready for the Pi to shut down.

Record your OS, installer commit, hardware configuration and results. The [host validation report](../../../../../docs/validation/UpgradeValidation-2026-10-07.md) and [audit report](../../../../../docs/validation/UpgradeAudit-2026-10-08.md) distinguish automated checks from pending physical acceptance.

## 4. Troubleshooting

| Symptom | Next step |
| --- | --- |
| curl returns 404 | The installer must first be published to the official default branch; use the local checkout for pre-publication validation |
| Unsupported platform | Check Zero 2 W, `aarch64`, Debian-based Raspberry Pi OS, Python 3.10+ and normal-user login; do not bypass the platform gate |
| Destination already exists | Enter that checkout and run `./install.sh`; do not remove calibration/configuration to retry |
| Installation stops at OS packages | Check the reported apt/network/sudo error. An existing administrator `policy-rc.d` is preserved; resolve it with the administrator |
| Hardware tool will not open | Stop the server, check pigpiod and I2C/SPI, permissions and saved pin assignments; retry from the wizard |
| Import blocked | Finish valid display, buzzer and servo configuration; file presence and factory defaults are insufficient |
| Saved progress rejected | Preserve the original file for inspection. Correct the reported schema/path issue before continuing; never replace it with guessed “complete” results |
| Lock exists after interruption | Confirm no installer/onboarding process is running before removing its corresponding stale lock; preserve all settings |
| Gemini/ngrok setup fails | Check internet/account access and retry the individual step. Previous settings are restored on helper failure/cancel |
| Port 8000 is busy | Stop the already running robot instance deliberately; do not run calibration and the server together |
| `uv` is not found | Use `.venv/bin/ninja_core` from the root for runtime commands; installation keeps its tools in a private directory |

## Appendix A — Useful Commands and Files

Run from the project root:

```bash
./install.sh --help
./onboard.sh --help
.venv/bin/ninja_core --help
python3 scripts/verify_core.py
python3 scripts/wiki.py setup       # Explicit developer dependency installation
python3 scripts/wiki.py prepare     # Explicit source preparation
python3 scripts/wiki.py search onboarding
python3 scripts/wiki.py check
```

| File/location | Purpose |
| --- | --- |
| `config.json` | Existing robot identity, imported hardware and Gemini settings; contains secrets |
| `servo.json`, `buzzer.json`, `pi0disp/display.json` | Existing device-tool configuration |
| `pi0vl53l0x/src/pi0vl53l0x/config/vl53l0x.json` | Existing distance offset |
| pyngrok-selected config path | Existing ngrok token storage; keep private |
| `.ninjarobot-install/record.json` | Resolved checkout revision and installer input fingerprints |
| `ninjarobot_pi0_Wiki/` | Independent wiki, immutable source versions and reviewed knowledge |

Keep credentials and calibration backups private. Root package identities remain unchanged; boot startup and legacy CLI actions should be reviewed separately before use.

## Appendix B — Documentation and Development

- [InstallationGuide.md](InstallationGuide.md)
- [DevelopmentGuide.md](DevelopmentGuide.md)
- [DevelopmentLog.md](../../../notes/ninjarobotpi0/2026-10-08-compatibility/DevelopmentLog.md)
- [Wiki entry point](../../../../README.md)
- [Development policy](../../../../../AGENTS.md)
- [Approved implementation plan](../../../../../DevelopmentPlanDoc/NinjaRobot_Install_wiki_upgrade_261007.md)
- [License](../../../../../LICENSE)

The three root manual files remain compatibility links. Full manuals are versioned inside the wiki; this README is the public introduction and practical quick-start manual. Current code and tests determine implemented behavior. Wiki pages remain draft/unverified until actual human verification is recorded.

# 日本語

NinjaRobotPi0 は Raspberry Pi Zero 2 W 向けの教育ロボットです。サーボ、液晶表情、ブザー、距離センサー、Gemini、BLE、Web 操作を備えています。対応 OS は **Raspberry Pi OS 64-bit（コードネーム制限なし）**です。詳しい配線・テスト手順は上の英語版と [導入マニュアル](../../../../../InstallationGuide.md) を参照してください。この節は要約です。

1. 電源を切って配線し、サーボ電源は別電源にします。GND を共有し、ソフト導入中はアクチュエータ電源を切ってください。
2. Bookworm/Trixie 64-bit、Wi-Fi/SSH、I2C/SPI を設定します。通常ユーザーで、公開後に下記 curl コマンドを実行します。
3. 導入後は `./install.sh --check`、準備完了後に `sudo systemctl start pigpiod` と `./onboard.sh` を実行します。
4. 表示、ブザー、サーボ、距離、設定の取り込み、名前/型、Gemini、ngrok の順に設定します。サーボツールはメニュー前に動く場合があります。手足・車輪を支持してから `READY` を入力してください。
5. Q で保存終了、`--resume` で再開します。既存設定の再利用は実機確認ではありません。変更された校正の実機確認記録は無効になります。失敗時は再試行できます。
6. 最後にプロジェクト直下で `.venv/bin/ninja_core server` を手動実行します。機器が初期化され、ngrok 接続も試行されます。表示されたローカル URL を開き、一つずつ動作確認してください。ngrok を省略しても通信遮断モードにはなりません。

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
cd "$HOME/NinjaRobotPi0"
./install.sh --check
./onboard.sh --dry-run
```

導入・初期設定はサーバー、自動起動、再起動を自動実行しません。キーとトークンは非表示入力です。公開 URL は秘密として扱ってください。実機での最終検証とリポジトリへの公開は別途必要です。

# 繁體中文

NinjaRobotPi0 是 Raspberry Pi Zero 2 W 教育機器人，整合伺服動作、螢幕表情、蜂鳴器、距離感測、Gemini、BLE 與網頁操作。需要 **Debian 系 Raspberry Pi OS 64-bit（不限制代號）**。完整接線及測試步驟請參閱上方英文版與[安裝手冊](../../../../../InstallationGuide.md)；此節為摘要。

1. 關閉電源後接線；伺服使用獨立電源並共地，安裝軟體時切斷致動器電源。
2. 設定 Bookworm/Trixie 64-bit、Wi-Fi/SSH、I2C/SPI。版本公開後，以一般使用者執行下方 curl 指令。
3. 安裝後執行 `./install.sh --check`。準備好校準時，執行 `sudo systemctl start pigpiod` 與 `./onboard.sh`。
4. 依序完成螢幕、蜂鳴器、伺服、距離、匯入設定、名稱/類型、Gemini 與 ngrok。伺服工具可能在顯示選單前立即置中；支撐四肢／輪子後才輸入 `READY`。
5. Q 保存退出，`--resume` 繼續。有效既有設定可重用，但不等於實體驗證；校準檔改變會清除舊實體觀察紀錄，失敗步驟可重試。
6. 在專案根目錄手動執行 `.venv/bin/ninja_core server`；它會初始化硬體並嘗試 ngrok 連線。開啟顯示的本機 URL，逐項測試。略過 ngrok 設定不代表禁止對外連線。

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
cd "$HOME/NinjaRobotPi0"
./install.sh --check
./onboard.sh --dry-run
```

安裝與初始設定不會自動啟動伺服器、開機服務或重新開機。金鑰及 token 使用隱藏輸入，公開控制 URL 請保密。實機最終驗證與 GitHub 發布仍需另外完成。

# 简体中文

NinjaRobotPi0 是 Raspberry Pi Zero 2 W 教育机器人，包含舵机动作、屏幕表情、蜂鸣器、距离传感、Gemini、BLE 和网页操作。需要 **Debian 系 Raspberry Pi OS 64-bit（不限制代号）**。完整接线及测试步骤请阅读上方英文版与[安装手册](../../../../../InstallationGuide.md)；本节为摘要。

1. 断电接线，舵机使用独立电源并共地；安装软件时切断执行器电源。
2. 配置 Bookworm/Trixie 64-bit、Wi-Fi/SSH、I2C/SPI。版本发布后，以普通用户执行下方 curl 命令。
3. 安装后运行 `./install.sh --check`。准备好校准后运行 `sudo systemctl start pigpiod` 和 `./onboard.sh`。
4. 依次完成屏幕、蜂鸣器、舵机、距离、导入配置、名称/类型、Gemini、ngrok。舵机工具可能在菜单出现前立即回中；支撑四肢／轮子后再输入 `READY`。
5. Q 保存退出，`--resume` 继续。复用有效配置不等于物理验证；校准文件改变会清除旧物理观察记录，失败步骤可以重试。
6. 在项目根目录手动运行 `.venv/bin/ninja_core server`，它会初始化硬件并尝试 ngrok 连接。打开显示的本地 URL，逐项测试。跳过 ngrok 配置不代表禁止外部连接。

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
cd "$HOME/NinjaRobotPi0"
./install.sh --check
./onboard.sh --dry-run
```

安装和初始化不会自动启动服务器、开机服务或重启。密钥与 token 隐藏输入，公开控制 URL 请保密。实机最终验证及 GitHub 发布仍需另行完成。
