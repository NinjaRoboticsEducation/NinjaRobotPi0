# Ninja Core

This package contains the main application logic for NinjaRobotPi0. It integrates all the individual hardware libraries (`pi0servo`, `pi0buzzer`, etc.) into a cohesive system managed by a central configuration and a Hardware Abstraction Layer (HAL).

## Key Components

- **`hal.py` (Hardware Abstraction Layer):** Initializes and provides a single access point for all hardware drivers.
- **`config.py` (Configuration Manager):** Manages all robot settings from a central `config.json` file.
- **`dispatcher.py` (Command Dispatcher):** Central router for BLE and Web commands. Bridges all input sources.
- **`safe_executor.py` (Safe Execution - Phase 4):** Sandboxed environment for running user/AI-generated Python code safely. Blocks dangerous imports.
- **`ninja_coder.py` (AI Code Agent - Phase 4):** Gemini-powered agent for code generation, translation, and debugging.
- **`api_wrappers.py` (Robot API - Phase 4):** High-level wrappers (`RobotWrapper`, `BuzzerWrapper`, `DisplayWrapper`, `DistanceWrapper`) exposed as `robot` in the executor.
- **`movement_controller.py` (Motion System):** Executes complex, multi-servo movement sequences.
- **`facial_expressions.py`, `robot_sound.py`, `perception.py`:** High-level controllers for expressions, sounds, and sensing.
- **`web_server.py` (FastAPI Server):** Web interface with WebSocket support for real-time events (Phase 4: `/ws/events` added).

---

## V5 Changes

> [!IMPORTANT]
> As of V5, the HAL uses **dynamic driver loading** via `importlib` and validates drivers against ABCs.

### Key Changes:
- **Dynamic Loading**: Drivers are loaded from a registry, not hardcoded imports.
- **ABC Validation**: All drivers implement `Sensor` or `Actuator` interfaces.
- **Config Import**: Run `uv run ninja_core config import` to merge `servo.json` and `buzzer.json` into `config.json`.

### Driver Registry:
```python
DRIVER_REGISTRY = {
    "servos": {"module": "pi0servo.core.servo_group", "class": "ServoGroup"},  # V5.2.1
    "buzzer": {"module": "pi0buzzer.driver", "class": "MusicBuzzer"},
    "display": {"module": "pi0disp.disp.st7789v", "class": "ST7789V"},
    "distance_sensor": {"module": "pi0vl53l0x.driver", "class": "VL53L0X"},
}
```

---

## Built-in movement import and robot compatibility

Set `robot_type` with `ninja_core config set-type spider`, `humanoid`, or `wheel` (`wheel` normalizes to the existing `tire` value), then run `ninja_core config import`/`import-all`. Import seeds 19 `spider_*` waypoint movements plus `Poweroff` for Spider with GPIO20–27, or one all-configured-servo center movement named `home` for Wheel/Humanoid. Additional Wheel/Humanoid movements are deferred. Import never initializes hardware; default calibration created when `servo.json` is missing is not proof of physical calibration.

The installed `ninja_core/data/spider_otto.json` resource retains the original trajectory values, with runtime names adapted to the proposal. `movements` still maps names to step lists. Additive `movement_robot_types` scopes names and `builtin_movement_hashes` records last imported definitions so reimport/type changes preserve edits and custom collisions. Removed built-ins return on the next import. Type switching removes only unchanged managed sequences; incompatible edits remain stored but cannot run on the new type.

`MovementController.available_movement_names()` filters by robot type, valid waypoints and active driver channels. `execute_movement()` revalidates every waypoint before actuator writes and raises `MovementValidationError` for unknown/incompatible/malformed sequences. Known robot prefixes and copied legacy Spider trajectories (including the document's unprefixed `Poweroff`) remain guarded without metadata. Custom unscoped sequences require owner review of mechanical roles. Driver abort stops sequence advancement without a controller-issued recovery pose. Callback checks occur before/after blocking driver calls; immediate in-step callback interruption is not guaranteed. The controller lock serializes its own operations; independent Blockly/direct driver writers still use the existing runtime ownership mechanisms.

The CLI's execute menu, `GET /api/servos/movements` (`{"movements": [...]}`), and Ninja agent use filtered discovery. `POST /api/servos/movements/{name}/execute` returns 404 for unknown names, 422 for invalid/incompatible data before reclaiming runtime, and 409 on abort. Existing frontend routes/payloads remain compatible, and failed requests appear in the log. Text/audio agent plans use exact permitted names; an invalid native chain is rejected as a whole, retaining the response and logging the reason. Bounds are 32 native chain entries and 1–20 repetitions per entry. Saved Blockly actions remain a separate existing execution path.

Physical direction, clearance, load, timing and power still require manual Pi validation. `Poweroff` holds eight extreme targets and can execute during web/server shutdown. Opening a device tool can energize servos. See [validation](../../../../../ninja_core/../docs/validation/BuiltinMovements-2026-10-09.md) before operation.

日本語: インポートで種類に合う動作を追加します。Wheel/Humanoid は `home` のみです。実行時にも種類と全ステップを検証します。物理的な校正・可動範囲・電源の確認は別途必要です。

繁體中文：匯入時加入對應類型的動作，Wheel/Humanoid 目前只有 `home`。執行時會再次驗證類型與所有步驟；仍須另外確認實際校正、活動範圍與電源。

## The Motion System (`movement_controller.py`)

The Motion System is responsible for all servo-based movements. It is composed of two main parts: the runtime `MovementController` class and the interactive `movement-tool` CLI.

### `MovementController` Class

This class is the runtime engine for executing pre-defined motion sequences.
- It is initialized with the HAL and `NinjaConfig` objects, removing the need for direct hardware or file system access.
- Its primary method, `execute_movement(movement_name)`, plays back a named sequence from the configuration.
- It uses **position-aware easing** for fluid multi-step motions:
  - **First step:** `ease_in_cubic` (accelerate only)
  - **Middle steps:** `linear` (constant velocity through waypoints)
  - **Last step:** `ease_out_cubic` (decelerate to stop)
- Arrival times depend on each servo's distance and calibration. Easing does not guarantee continuous physical momentum, balance, or source oscillator timing.

### `movement-tool` CLI

This is an interactive, command-line tool for developers to **calibrate, create, edit, and test** all servo-related functions. You can launch it by running `uv run ninja_core movement-tool` from the project root.

The tool presents a main menu with the following options:

- **1. Calibrate a Servo:** Launches the `pi0servo` calibration tool for a selected servo. This allows you to define the min, center, and max pulse widths. The new calibration is automatically imported into the application's main configuration when the tool is running.
- **2. Record new movement:** Starts the interactive recorder to create a new, named motion sequence step-by-step.
- **3. Modify existing movement:** Provides a menu to interactively edit, insert, or delete steps within a saved movement.
- **4. Execute a movement:** Plays back a saved movement, with options for looping.
- **5. Clear movement:** Deletes a saved movement from the configuration.
- **6. Exit:** Executes configured `Poweroff` (or configured `home` when Poweroff is absent), then shuts down HAL and saves `config.json`. No center command follows the exit pose. Type/waypoint validation remains enforced; a failed pose is logged and cleanup still runs. Keyboard interruption does not request an extra recovery movement. Shutdown releases PWM rather than holding the pose electrically.

### Browser session and reconnect lifecycle

The shared Home/Agent/Help layout opens `/ws/session` using the server-issued HttpOnly `ninja_web_session` cookie. Only one browser identity owns controls; same-cookie tabs share ownership. Another browser receives busy/4409. Every `/api/` request and `/ws/distance` or `/ws/events` socket requires that live primary session; inactive HTTP clients receive 423 and shutdown requests receive 503. Existing routes, payloads and auxiliary event messages are retained. Direct scripts using REST must obtain the cookie from HTML and keep `/ws/session` open; this is a connection-ownership contract, not authentication. BLE is unchanged and separately controlled.

Clients ping every 10 seconds; the server releases a dead connection after 35 seconds without input. The browser retries every 3 seconds. Final-tab disconnect cancels pending browser requests/greetings, stops Blockly/native output and restores an undistorted QR for the cached ngrok URL, or LAN URL if tunneling failed. RuntimePipeline suppresses automatic idle redraw while waiting for reconnect. Display failures cannot retain browser ownership; shutdown does not redraw QR over Poweroff. Request generations prevent work from a prior visit becoming authorized when the same browser reconnects. `center_all_servos(abort_check=None)` preserves existing default behavior while allowing web centering to check ownership inside the controller motion lock. Driver abort is still cooperative; no immediate physical stopping guarantee is made.

日本語：一つのブラウザー識別情報のみが操作できます。同じ Cookie のタブは共有し、最後の接続終了で再接続 QR を表示します。実機での停止タイミング・QR 読み取り確認は別途必要です。

繁體中文：僅允許一個瀏覽器身分操作；同 Cookie 分頁共用連線，最後一個連線結束後重新顯示 QR。仍須在實機驗證停止時機與 QR 可讀性。

See [lifecycle acceptance](../../../../../ninja_core/../docs/validation/LifecycleRefinements-2026-10-10.md). The environment path stays `.venv`; its installer prompt is now `ninjarobotpi0`.

#### In-Depth Guide: Recording a New Movement

This feature allows you to define a sequence of positions for your servos, which are then saved as a single, named movement (e.g., "wave", "nod").

##### Command Input Rules

When recording, you define each step using a special command syntax:

| Rule                | Description                                                                                                                            | Example                |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **Basic Format**    | A GPIO pin number and an angle, separated by a colon. Angles range from -90 to 90.                                                     | `17:45`                |
| **Angle Keywords**  | Use keywords for common angles: `C` for Center (0°), `M` for Minimum (-90°), and `X` for Maximum (90°).                                  | `17:C`                 |
| **Chaining**        | Multiple servo movements in the same step are chained together with a `/`.                                                              | `17:45/22:-30`         |
| **Speed Prefix**    | Set the speed for a step with a prefix: `S_` (Slow), `M_` (Medium), or `F_` (Fast). Medium is the default.                               | `S_17:90/22:90`        |
| **Auto-Completion** | **(Crucial Rule)** If a servo isn't specified in a command, it automatically holds its position from the *previous* step. This is the key to creating smooth, continuous motions. | If step 1 is `17:45` and step 2 is `22:30`, servo 17 remains at 45° during step 2. |

---

## Testing the Core Components

This guide assumes you are in the root directory of the `NinjaRobotPi0` project and have already installed all dependencies.

### Prerequisites

1.  **pigpio Daemon:** Before running any test, ensure the `pigpio` service is running.
    ```bash
    sudo pigpiod
    ```
2.  **Initial Configuration:** If you have not yet created the master `config.json`, run the import command at least once.
    ```bash
    uv run ninja_core config import-all
    ```

### Step 1: Calibrate and Test the Motion System

This workflow demonstrates the seamless integration of the calibration and movement tools.

1.  **Launch the Movement Tool:**
    ```bash
    uv run ninja_core movement-tool
    ```

2.  **Calibrate a Servo:**
    - Select option **1** to "Calibrate a Servo."
    - Choose the servo pin you wish to calibrate from the list.
    - The `pi0servo` calibration interface will launch. Follow the on-screen instructions (`h` for help) to set the Min, Center, and Max positions.
    - Press `q` to quit the calibration tool.
    - The `movement-tool` will automatically import the new settings and re-initialize the hardware.

3.  **Record a Movement:**
    - Select option **2** to "Record new movement."
    - Create a simple movement (e.g., `17:45`, confirm, then `17:C`, finish) and name it `test_wave`.

4.  **Execute the Movement:**
    - Select option **4** to "Execute a movement."
    - Choose the `test_wave` movement and loop it once.
    - **Expected Result:** The servo will smoothly move to its 45-degree position and back, respecting the calibration you just set.

5.  **Exit:** Select option **6** to exit. All your new calibration and movement data will be saved to `config.json`.

### Step 2: Test Other Core Components

You can test other hardware functionalities using the pre-made test scripts in the project root:

- **Test HAL (Servos and Buzzer):**
  ```bash
  uv run python test_hal.py
  ```
- **Test Display System:**
  ```bash
  uv run python test_facial_expressions.py
  ```
- **Test Sound System:**
  ```bash
  uv run python test_robot_sound.py
  ```
- **Test Perception System:**
  ```bash
-   **Test HAL (Servos and Buzzer):**
    ```bash
    uv run python test_hal.py
    ```
-   **Test Display System:**
    ```bash
    uv run python test_facial_expressions.py
    ```
-   **Test Sound System:**
    ```bash
    uv run python test_robot_sound.py
    ```
-   **Test Perception System:**
    ```bash
    uv run python test_perception.py
    ```

This confirms that all `ninja_core` systems are successfully communicating with and controlling the hardware.

### Step 3: Test the AI Agent

The AI Agent allows you to control the robot using natural language.

#### 3.1. Setup Google Gemini API Key and Model

1.  **Create an API Key:**
    -   Go to [Google AI Studio](https://aistudio.google.com/).
    -   Click on "Get API key" -> "Create API key".
    -   Copy the generated key.

2.  **Set the Key in NinjaRobot:**
    ```bash
    uv run ninja_core config set-key gemini YOUR_ACTUAL_API_KEY_HERE
    ```

    NinjaRobot queries Google's model catalog with the supplied key and lists Gemini models that support agent content generation. After you select a numbered model, NinjaRobot runs a bounded minimal generation request and saves the API key/model only if that request succeeds. Validation can take up to 60 seconds for a thinking model. A failed lookup, non-responsive model, or cancelled prompt leaves the existing Gemini configuration unchanged.

    The guided `uv run ninja_core init-tool` option performs the same model-selection flow while hiding the entered API key.

    Gemini 3 models use a bounded REST compatibility path with low thinking because the installed legacy Python SDK cannot configure their current thinking controls. A normal agent request may still take several seconds. The chat and server consoles show the configured model and return a visible error if the model exceeds the request timeout.

#### 3.2. Setup ngrok (For Remote Access)

To access the web server from outside your local network, you need an ngrok account.

1.  **Create an Account:**
    -   Go to [ngrok.com](https://ngrok.com/) and sign up for a free account.

2.  **Get Your Authtoken:**
    -   Go to your [ngrok Dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).
    -   Copy your Authtoken.

3.  **Configure NinjaRobot:**
    -   When you run `uv run ninja_core server` for the first time, you will be prompted to enter this token.
    -   `uv run ninja_core server` - Start the web interface (interactive mode)
    -   `uv run ninja_core server --autostart` - Start in non-interactive mode (for systemd)
    -   Alternatively, you can set it manually via the ngrok CLI if installed, but the server prompt is the easiest method.

#### 3.3. Run the Interactive Chat
    This command initializes the robot and the AI agent, allowing you to type commands.
    ```bash
    uv run ninja_core chat
    ```

#### 3.4. Test Capabilities
    -   **Nuance:** Type "I am feeling joyful." -> Robot should show a happy face.
    -   **Multilingual:** Type "こんにちは" (Konnichiwa). -> Robot should reply in Japanese.
    -   **Search:** Type "What is the weather in Tokyo?" -> Robot should search and answer.
    -   **Auto-Emotion:** Type "Tell me a joke." -> Robot should speak (show speaking face) while answering.
    -   **Movement:** Type "Do a wave." (if you recorded a 'wave' movement). -> Robot should execute the movement.

### Step 4: Test Web Server & Remote Access

The Web Server provides a user-friendly interface for controlling the robot from any device on the network or over the internet.

1.  **Start the Server:**
    ```bash
    uv run ninja_core server
    ```
    - The robot will initialize all hardware.
    - It will attempt to start an `ngrok` tunnel automatically.
    - **Check the Display:** The robot's LCD screen should display a **QR Code**.

2.  **Connect to the Interface:**
    - **Option A (Mobile/Remote):** Scan the QR code on the robot's screen with your phone.
    - **Option B (Local Network):** Open a browser on your computer and go to `http://<robot-ip>:8000` (The IP is printed in the terminal).

3.  **Test Web Features:**
    - **AI Chat & Voice Input:**
        - **Text Chat:** Type a message in the input box and click **Send**.
        - **Voice Input:** Select your language (English, 日本語, 繁體中文, 简体中文), click the  **`ninja_agent.py`** - AI Agent
  - Google Gemini integration for NLP
  - Semantic understanding and intent mapping
  - Auto-emotion generation
  - Action chaining (Movement, Faces, Sounds)
  - Multilingual support (EN/JP/ZH-TW/ZH-CN)he robot will detect the selected language and respond in the same language (including distinguishing between Traditional and Simplified Chinese).
    - **Servo Movements:** Select a movement from the dropdown and click **Execute**.
    - **Facial Expressions:** Select an expression and click **Show**.
    - **Sounds:** Select an emotion sound and click **Play**.
    - **Distance Sensor**: Verify that the distance reading updates in real-time (every ~200ms).
    - **System Controls**: Use the **Power Off Robot** button to safely shut down the Raspberry Pi.

4.  **Test Obstacle Avoidance (Safety):**
    - While a movement is executing (e.g., a long sequence), place your hand in front of the sensor (< 50mm).
    - **Expected Result:** The robot should **immediately stop**, display a "scary" face, play a warning sound, and the web interface should show an error or stop notification.


## Cloud model selection

Use `uv run ninja_core config select-model`, init-tool option 1, or onboarding step 7 to select Google, OpenAI, Anthropic or Ollama Cloud using a hidden API key and a validated live model. Restart an already-running agent deliberately to apply a CLI selection. Pi0 uses cloud inference only. Web microphone input uses browser speech recognition to fill the text box and works with every provider; direct audio-file input requires a supported Google model. Read the [detailed implementation source](../../../../../ninja_core/../ninjarobot_pi0_Wiki/raw/notes/ninjarobotpi0/2026-10-10-model-adapter/ModelAdapterImplementation.md) for private credentials, migration and manual validation.
