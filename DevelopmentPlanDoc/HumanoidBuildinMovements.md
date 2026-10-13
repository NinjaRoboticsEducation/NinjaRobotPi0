# NinjaRobotPi0 Humanoid Built-in Movement Reference

Research and translation: 2026-10-12. **34 complete movement definitions, 1,203 keyframes. Host validated; physical validation pending.**

**Current installed defaults — 2026-10-13:** [humanoid_movements_updated.json](humanoid_movements_updated.json) is the owner-approved list: **37 movements / 1,278 steps**, comprising 36 `humanoid_*` definitions and exact `Poweroff`. The 34 original movement geometries are retained at M; two added run variants copy the corresponding walk geometry at F. The installed `ninja_core/data/humanoid_defaults.json` matches that file exactly apart from the package's `robot_type` envelope. Full Humanoid profiles receive exactly this list, using `humanoid_home` without an extra generic `home`. Partial profiles retain fallback `home`. `scripts/build_humanoid_defaults.py --check` validates source/resource parity, native schema and the reviewed fingerprint. See [replacement plan](../docs/HumanoidDefaultsReplacementPlan-2026-10-13.md) and [validation](../docs/validation/HumanoidDefaultsReplacement-2026-10-13.md).

The complete 34 Otto translations below and `data/humanoid_otto.json` remain the original research reference at S, not the current installed defaults. The original native integration had 34 translations plus generic home; the first Poweroff addition had 36 defaults / 1,205 steps. The owner replacement supersedes those installation counts and speeds. The original [implementation plan](../docs/HumanoidBuiltinMovementsImplementationPlan.md) and [validation report](../docs/validation/HumanoidBuiltinMovements-2026-10-12.md) remain historical evidence. Physical acceptance is still pending.

The request's references to “Spider hardware” are interpreted as reuse of its GPIO-addressed JSON format. The supplied hip/foot/arm table defines a **Humanoid** robot, requiring `robot_type: "humanoid"`; it is not a Spider geometry. This mapping must be physically checked before use. The 34 Otto trajectories keep GPIO24/25 at **nominal neutral 0°**, not a claimed measured neutral. The separate owner-supplied `Poweroff` below explicitly commands these shoulders to +30°/−30°; physical direction and clearance still require validation.

## 1. NinjaRobotPi0 movement system overview

### Storage, loading and execution

A movement is a named list of steps in the `movements` object of the existing core `config.json`. Each step commands one or more servos together; the next step starts after the driver finishes that step. Keys such as `"20"` are **BCM GPIO numbers**, not header-pin numbers or Otto array indices.

The verified path is [NinjaConfig and load/save](../ninja_core/src/ninja_core/config.py) → [catalog discovery and whole-sequence validation](../ninja_core/src/ninja_core/builtin_movements.py) → [MovementController](../ninja_core/src/ninja_core/movement_controller.py) → [ServoGroup.move_all_sync](../pi0servo/src/pi0servo/core/multi_servos.py) → [calibrated Servo pulse conversion](../pi0servo/src/pi0servo/core/servo.py).

`load_config(path)` parses an existing file with `NinjaConfig`; a missing path creates defaults. It does **not** itself seed the native catalog. Hardware configuration import and robot-type selection reconcile managed defaults. Full Humanoid defaults are the exact 37-entry owner list when GPIO20–27 are configured. Partial profiles receive only generic `home`. The controller does not scan Markdown or arbitrary JSON files. The hardware configuration import command is not a general movement-pack importer.

The core [HAL](../ninja_core/src/ninja_core/hal.py) chooses active servo channels from `config.servos.calibration` **keys**. Descriptive `servos.pins` labels alone do not activate channels. The actual servo driver obtains physical pulse calibration and speed limits through `ConfigManager("servo.json")` in the runtime working directory; core JSON pulse values are not sufficient evidence that the driver is calibrated. Verify both the active core configuration and the physical driver calibration.

### Humanoid Poweroff default — 2026-10-13

This additional default retains the exact name `Poweroff`, speed `M`, and owner-supplied angles. It is separate from the 34 Otto translations and their fingerprint. It is included unchanged in the current installed `data/humanoid_defaults.json` and seeded only for a Humanoid profile with all GPIO20–27 configured. Import/type selection creates managed scope and hashes; loading an existing configuration alone does not add it.

```json
{
  "movements": {
    "Poweroff": [
      {
        "speed": "M",
        "moves": {
          "20": 0,
          "21": 0,
          "22": 0,
          "23": 0,
          "24": 30,
          "25": -30,
          "26": 90,
          "27": -90
        },
        "per_servo_speeds": {}
      }
    ]
  }
}
```

After updating the installed code, run `.venv/bin/ninja_core config set-type humanoid` and `.venv/bin/ninja_core config import` from the calibrated runtime directory. These configuration commands do not initialize hardware. Restart a running tool/server deliberately to reload configuration. `Poweroff` is available through movement-tool, the web dropdown and Ninja Agent, and is attempted by deliberate movement-tool exit and the existing coordinated server shutdown. Runtime safety/cancellation checks still apply; shutdown releases PWM afterward.

Reimport preserves a custom or edited `Poweroff` instead of overwriting it. Unchanged managed entries are replaced with the correct pose when switching Spider/Humanoid type. A retained edited entry from the other profile remains scoped and blocked; after backing up config, remove that conflicting movement and reimport if the new default is desired. Known Humanoid Poweroff geometry is rejected on other profiles even after renaming or speed edits. Partial profiles cannot seed or execute its full eight-channel pose. Physical acceptance remains pending; see [validation report](../docs/validation/HumanoidPoweroff-2026-10-13.md).

### Exact supported step fields

| Field | Meaning |
|---|---|
| `moves` | Required nonempty object. Canonical decimal GPIO keys; finite numeric signed angles from −90 to +90. Booleans and unknown/unavailable channels are rejected. |
| `speed` | Required `"S"`, `"M"` or `"F"` global speed mode. |
| `per_servo_speeds` | Optional object of GPIO-to-mode overrides. `{}` uses global speed everywhere. An override for an omitted target has no motion effect. |

No step accepts `duration`, `delay`, `pause`, `repeat`, `loop`, oscillator amplitude/period/phase, custom easing, or detach/release commands. Repetition must be expanded into more steps or requested by a separate caller. These JSON sequences take no runtime height, direction, or period arguments.

A one-servo **example fragment** (merge the inner entry into the existing `movements` dictionary only after setup checks):

```json
{"movements":{"humanoid_example_left_hip":[{"moves":{"20":5},"speed":"S","per_servo_speeds":{}}]}}
```

`humanoid_example_left_hip` is a unique lookup name; `"20":5` requests signed +5° on the left hip. `S` selects the lowest mode factor. Other servos are omitted, so they keep their present commands. This is a small commissioning example, not part of the 34-entry library.

A coordinated **example fragment**:

```json
{"movements":{"humanoid_example_hip_pair":[{"moves":{"20":5,"21":-5},"speed":"S","per_servo_speeds":{"21":"M"}}]}}
```

Both hips begin in the same driver step. GPIO21 uses `M`; GPIO20 uses `S`. Opposite numerical signs do not prove opposite physical directions. This illustrates an override, not a calibrated gait recommendation. Omitted feet, arms and shoulders keep their current positions.

### What speed actually means

[MotionCalculator](../pi0servo/src/pi0servo/motion/calculator.py) calculates nominal velocity as `600 × speed_limit/100 × mode_factor` degrees/second, with `F=1`, `M=0.75`, `S=0.5`. Per-joint travel duration is `abs(target-current)/velocity`; the group uses a common clock and waits for the longest duration. Different joints can arrive earlier. The driver updates at a nominal 10 ms interval, applies easing and writes final targets explicitly. Actual mechanics can lag the commands.

For example, at an illustrative calibrated speed limit of 80%, `S` gives 240°/s nominal velocity: a 30° step takes about 0.125 s before scheduler/mechanical effects. Thus `S` is **not** an Otto millisecond duration or a guarantee of gentle physical motion. A zero/nonpositive velocity does not encode a pause; zero-distance duplicate steps also do not create a reliable dwell.

One-step movements use `ease_in_out_cubic`. Multi-step movements use `ease_in_cubic` for the first step, `linear` internally, and `ease_out_cubic` for the last. Intermediate points follow straight segments in joint coordinates, rather than a continuous time-controlled sine wave. Small integer steps can be dominated by scheduler resolution. Exact original period, rhythm, simultaneous arrival, balance and travel distance are not preserved.

### Registration and triggering

Section 3 blocks are merge fragments, not complete robot configurations. The installed native resource is reconciled automatically by `.venv/bin/ninja_core config set-type humanoid` and `.venv/bin/ninja_core config import` (or `import-all`) in the intended runtime directory. Select Humanoid explicitly: a newly generated default configuration is Tire until a type is selected. Module import reads calibration channels, then seeds the catalog without initializing hardware. Repeat import preserves edited movements and same-name custom collisions; only unchanged managed entries update/remove on profile changes. Keep existing credentials and hardware settings. Section 5's offline merge preview remains an optional research/inspection tool: on an already seeded config it deliberately refuses collisions. Prefer the native import flow for registration; do not manufacture managed hashes manually.

After installing the updated package, selecting the Humanoid profile and importing its calibrated module configuration, restart/reload the application so its in-memory config sees the entries. Complete physical commissioning before executing gaits. Native Movement Tool can list and execute valid movements; starting a hardware tool can center servos before its menu. The existing web Movement page uses `GET /api/servos/movements` and `POST /api/servos/movements/{name}/execute` in [web_server.py](../ninja_core/src/ninja_core/web_server.py). Use the active primary browser session and existing power/readiness flow. These routes are described, not called, by this task.

`humanoid_` names and managed scope metadata enforce the Humanoid profile. Known non-neutral Humanoid trajectories are also recognized after renaming/removing metadata, including speed changes and integer GPIO keys. Generic neutral centering is excluded from geometry inference so other profiles can still center. Arbitrary modified unscoped custom trajectories cannot be reliably classified by geometry alone. Discovery hides invalid/incompatible movements; direct execution validates **every step before any output**. Unknown names, wrong profile, unavailable pins, invalid angles, modes and fields fail validation. The web route reports unknown names as 404, validation failures as 422, unavailable hardware as 500 and aborted execution as 409, subject to session/shutdown middleware gates.

The controller serializes commands and checks its abort callback before and after each blocking driver step. A driver abort or boundary check stops progression with `EmergencyStop`; there is no unsolicited recovery pose. Browser cancellation is not checked inside every driver interpolation tick. The final commanded pose remains held unless later code moves or releases the servos.

## 2. Humanoid servo wiring and physical arrangement

The table records the **owner-supplied joint assignment**, verified software addressing, and standard 40-pin header positions. Mounting, actual neutral, forward direction, clearance and gait stability remain untested.

| BCM GPIO | Physical header pin | Source logical ID | Body location / function | JSON nominal neutral | Proposed range / status |
|---|---:|---|---|---:|---|
| 20 | 38 | S0 / YL | Left hip/leg | 0 | −90…+90 software range; physical range pending |
| 21 | 40 | S1 / YR | Right hip/leg | 0 | Same |
| 22 | 15 | S2 / RL | Left foot / ankle | 0 | Same |
| 23 | 16 | S3 / RR | Right foot / ankle | 0 | Same |
| 24 | 18 | None assigned | Additional left shoulder, fore/aft | 0 | Neutral only in this library; direction pending |
| 25 | 22 | None assigned | Additional right shoulder, fore/aft | 0 | Neutral only in this library; direction pending |
| 26 | 37 | S4 / LA | Left arm | 0 | −90…+90 software range; physical range pending |
| 27 | 13 | S5 / RA | Right arm | 0 | Same |

Front-view schematic below uses the **robot's** left/right (opposite the viewer's). It shows assignments, not measured dimensions or verified joint-axis orientations.

```text
                       HEAD
                +---------------+
Robot RIGHT     |     TORSO      |     Robot LEFT
shoulder GPIO25 o               o shoulder GPIO24
arm RA GPIO27  o               o arm LA GPIO26
                +-----+---+-----+
          hip YR GPIO21   GPIO20 hip YL
                  |       |
         foot RR GPIO23   GPIO22 foot RL
```

For the six Otto joints, the translation is `target_signed = source_logical − 90`: source 0/90/180° becomes −90/0/+90°. This is an **offline conversion**, not an extra controller feature. Pi0 receives the signed angle and clamps to each calibrated angle range, then maps it piecewise linearly through calibrated minimum, center and maximum pulse widths. No additional inversion is applied by this pack. Source Otto trims are not copied; physical alignment belongs to the actual robot's calibration.

Servo driver defaults are not a measurement: the calibration dataclass can have all three pulses at 1500 µs; partially populated saved records have different fallback values. Missing calibration can therefore produce no useful travel. The driver's cached requested angle is not an encoder reading and may differ from a clamped physical command. Validate actual pulses, center alignment and permitted travel; do not treat numerical acceptance as clearance validation.

The registered [current InstallationGuide](../ninjarobot_pi0_Wiki/raw/articles/ninjarobotpi0/2026-10-10-model-adapter/InstallationGuide.md) documents a Pi supply of 5 V / 2.5 A and a separate 5 V servo supply (3 A or greater as its example baseline), common ground, and servo signals on GPIO20–27. Supply sizing must cover the actual eight servos and simultaneous load; the example rating is not a stall-current guarantee. Do not power the servo bank from the Pi 5 V rail. Wire with power removed and confirm each connector's polarity against the actual servo.

**Wiring evidence conflict:** the older wiki [installation/wiring reference](../ninjarobot_pi0_Wiki/wiki/references/installation-and-wiring.md) assigns display signals to GPIO24/25, conflicting with this owner's shoulder assignment. Some manual display examples also use GPIO20 for backlight. Verify that display, buzzer and other live pin assignments do not occupy **any** GPIO20–27 before enabling this profile. Do not adopt incompatible example configurations or rewire automatically. Display and sensor testing is pending and requires the actual robot's pin inventory.

## 3. Complete built-in Humanoid movement library

### Coverage and reading the definitions

The library covers all **16 public servo motion methods** (24 explicit variants including directions) plus **10 servo-containing gestures**. Base four-joint Otto motions are generated in the source's **six-servo Humanoid mode** to retain its arm extensions. `handsup` and `handwave` are six-servo-only methods. GPIO24/25 are target-only additions held at nominal neutral in **every** step. All eight channels must exist even when some stay still.

Each movement below has complete JSON in a `movements` envelope. Merge inner named entries; do not concatenate standalone JSON objects. Every step uses `S` and an empty override object as an explicit porting choice. There are no hidden loops, omitted keyframes, expressions, timestamps or unsupported metadata inside the steps.

Oscillator sequences sample the source's amplitude/offset/phase at 36 intervals per cycle, including start and endpoint: 37 points for one cycle, 73 for two, 181 for five. This preserves a geometric approximation, not original wall-clock playback. New source `_execute` subcalls start at mathematical phase zero in this port. Details and source quirks are in Section 4.

Source files are in the separate workspace checkout `RoboticsRepoReference/OttoDIYPython-master/` (a sibling of `NinjaRobotPi0/`, not included in a standalone Pi0 clone). The source reference is `OttoHumanoidMovementIntro.md`, cross-checked against `otto9.py` and `oscillator.py`. Source call arguments and line ranges below identify the exact local source revision; hashes are recorded in Section 5.

| Movement name | Description / servo groups with changing targets | Source movement | Keyframes | Adaptation notes |
|---|---|---|---:|---|
| `humanoid_home` | home; all neutral | `home()` | 1 | Neutral pose; does not detach |
| `humanoid_jump` | jump; feet/arms | `jump(1, 1000)` | 2 | One up/down pair; source steps ignored; no airborne claim |
| `humanoid_walk_forward` | walk forward; hips/feet/arms | `walk(1, 1000, 1)` | 37 | Six-source-joint gait; arms retain source amplitude90 |
| `humanoid_walk_backward` | walk backward; hips/feet/arms | `walk(1, 1000, -1)` | 37 | Six-source-joint gait; arms retain source amplitude90 |
| `humanoid_turn_left` | turn left; hips/feet/arms | `turn(1, 1000, 1)` | 37 | Python LEFT branch; direction pending mounting verification |
| `humanoid_turn_right` | turn right; hips/feet/arms | `turn(1, 1000, -1)` | 37 | Python RIGHT branch; direction pending mounting verification |
| `humanoid_bend_left` | bend left; feet/arms | `bend(1, 1000, 1)` | 3 | Three poses; source800ms dwell omitted |
| `humanoid_bend_right` | bend right; feet/arms | `bend(1, 1000, -1)` | 3 | Three poses; source800ms dwell omitted |
| `humanoid_shake_leg_left` | shake leg left; feet/arms | `shakeLeg(1, 1500, 1)` | 8 | Eight poses incl. both neutral returns; final500ms hold omitted |
| `humanoid_shake_leg_right` | shake leg right; feet/arms | `shakeLeg(1, 1500, -1)` | 8 | Eight poses; foot endpoint75 signed; final500ms hold omitted |
| `humanoid_updown` | updown; feet/arms | `updown(1, 1000, 15)` | 37 | h15; legs neutral, feet and arms oppose |
| `humanoid_swing` | swing; feet/arms | `swing(1, 1000, 15)` | 37 | h15; half-height foot offsets, full-height arm offsets |
| `humanoid_tiptoe_swing` | tiptoe swing; feet/arms | `tiptoeSwing(1, 1000, 15)` | 37 | h15; feet and arms have full offsets |
| `humanoid_jitter` | jitter; hips | `jitter(1, 1000, 15)` | 37 | h15; hips vary, feet/arms neutral |
| `humanoid_ascending_turn` | ascending turn; hips/feet/arms | `ascendingTurn(1, 1000, 15)` | 37 | Source caps h to13; arms amplitude40 |
| `humanoid_moonwalker_left` | moonwalker left; feet/arms | `moonwalker(1, 1000, 15, 1)` | 37 | Python LEFT, not browser label; source phase offsets preserved |
| `humanoid_moonwalker_right` | moonwalker right; feet/arms | `moonwalker(1, 1000, 15, -1)` | 37 | Python RIGHT, not browser label; source phase offsets preserved |
| `humanoid_crusaito_left` | crusaito left; hips/feet | `crusaito(1, 1000, 15, 1)` | 37 | Literal90-radian hip phase retained |
| `humanoid_crusaito_right` | crusaito right; hips/feet | `crusaito(1, 1000, 15, -1)` | 37 | Literal90-radian hip phase retained |
| `humanoid_flapping_forward` | flapping forward; hips/feet | `flapping(1, 1000, 15, 1)` | 37 | Arms neutral; h15 |
| `humanoid_flapping_backward` | flapping backward; hips/feet | `flapping(1, 1000, 15, -1)` | 37 | Arms neutral; h15 |
| `humanoid_hands_up` | hands up; arms | `handsup()` | 1 | LA−70 RA+70; lower body neutral |
| `humanoid_wave_left_arm` | wave left arm; arms | `handwave(-1)` | 181 | Source RIGHT actually moves LA/GPIO26; five cycles |
| `humanoid_wave_right_arm` | wave right arm; arms | `handwave(1)` | 37 | Source LEFT actually moves RA/GPIO27; one cycle |
| `humanoid_gesture_happy` | gesture happy; feet/arms | `playGesture(OTTOHAPPY)` | 38 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_superhappy` | gesture superhappy; feet/arms | `playGesture(OTTOSUPERHAPPY)` | 75 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_sad` | gesture sad; hips/feet | `playGesture(OTTOSAD)` | 2 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_sleeping` | gesture sleeping; hips/feet | `playGesture(OTTOSLEEPING)` | 2 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_fart` | gesture fart; feet | `playGesture(OTTOFART)` | 4 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_confused` | gesture confused; hips | `playGesture(OTTOCONFUSED)` | 2 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_love` | gesture love; hips/feet | `playGesture(OTTOLOVE)` | 74 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_angry` | gesture angry; hips/feet | `playGesture(OTTOANGRY)` | 4 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_fretful` | gesture fretful; feet | `playGesture(OTTOFRETFUL)` | 8 | Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained |
| `humanoid_gesture_victory` | gesture victory; feet/arms | `playGesture(OTTOVICTORY)` | 195 | Servo-only: sound/display/holds and detach omitted; first-ramp YL9 corrected to90; two foot ramps retained |

Servo-group labels indicate channels commanded away from nominal neutral at least once. They do not imply that other joints are omitted: every sequence explicitly commands all eight joints. Sequence entry moves from the robot's current pose to its first keyframe; check that transition separately. Final poses are whatever the final JSON step specifies. Neutral recovery is included only where the source calls `home`; the native engine adds none.

<!-- HUMANOID_LIBRARY_START -->

### humanoid_home

Source: `home()`, `otto9.py` lines 208–213. Neutral pose; does not detach.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_home": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_jump

Source: `jump(1, 1000)`, `otto9.py` lines 219–223. One up/down pair; source steps ignored; no airborne claim.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [1000, 1000] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_jump": [
      {"moves": {"20": 0, "21": 0, "22": 60, "23": -60, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_walk_forward

Source: `walk(1, 1000, 1)`, `otto9.py` lines 230–243. Six-source-joint gait; arms retain source amplitude90.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_walk_forward": [
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 5, "22": -16, "23": -24, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": -15, "23": -23, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": -13, "23": -21, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 19, "21": 19, "22": -11, "23": -19, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": -9, "23": -17, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 26, "21": 26, "22": -6, "23": -14, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 28, "21": 28, "22": -3, "23": -11, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 30, "22": 1, "23": -7, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 30, "22": 4, "23": -4, "24": 0, "25": 0, "26": 90, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 30, "22": 7, "23": -1, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 28, "21": 28, "22": 11, "23": 3, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 26, "21": 26, "22": 14, "23": 6, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": 17, "23": 9, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 19, "21": 19, "22": 19, "23": 11, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": 21, "23": 13, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": 23, "23": 15, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 5, "22": 24, "23": 16, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -5, "22": 24, "23": 16, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": 23, "23": 15, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": 21, "23": 13, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -19, "21": -19, "22": 19, "23": 11, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": 17, "23": 9, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -26, "21": -26, "22": 14, "23": 6, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -28, "21": -28, "22": 11, "23": 3, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -30, "22": 7, "23": -1, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -30, "22": 4, "23": -4, "24": 0, "25": 0, "26": -90, "27": -90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -30, "22": 1, "23": -7, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -28, "21": -28, "22": -3, "23": -11, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -26, "21": -26, "22": -6, "23": -14, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": -9, "23": -17, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -19, "21": -19, "22": -11, "23": -19, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": -13, "23": -21, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": -15, "23": -23, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -5, "22": -16, "23": -24, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_walk_backward

Source: `walk(1, 1000, -1)`, `otto9.py` lines 230–243. Six-source-joint gait; arms retain source amplitude90.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_walk_backward": [
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 5, "22": 24, "23": 16, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": 23, "23": 15, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": 21, "23": 13, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 19, "21": 19, "22": 19, "23": 11, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": 17, "23": 9, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 26, "21": 26, "22": 14, "23": 6, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 28, "21": 28, "22": 11, "23": 3, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 30, "22": 7, "23": -1, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 30, "22": 4, "23": -4, "24": 0, "25": 0, "26": 90, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 30, "22": 1, "23": -7, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 28, "21": 28, "22": -3, "23": -11, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 26, "21": 26, "22": -6, "23": -14, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": -9, "23": -17, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 19, "21": 19, "22": -11, "23": -19, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": -13, "23": -21, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": -15, "23": -23, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 5, "22": -16, "23": -24, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -5, "22": -16, "23": -24, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": -15, "23": -23, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": -13, "23": -21, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -19, "21": -19, "22": -11, "23": -19, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": -9, "23": -17, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -26, "21": -26, "22": -6, "23": -14, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -28, "21": -28, "22": -3, "23": -11, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -30, "22": 1, "23": -7, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -30, "22": 4, "23": -4, "24": 0, "25": 0, "26": -90, "27": -90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -30, "22": 7, "23": -1, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -28, "21": -28, "22": 11, "23": 3, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -26, "21": -26, "22": 14, "23": 6, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": 17, "23": 9, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -19, "21": -19, "22": 19, "23": 11, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": 21, "23": 13, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": 23, "23": 15, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -5, "22": 24, "23": 16, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_turn_left

Source: `turn(1, 1000, 1)`, `otto9.py` lines 250–266. Python LEFT branch; direction pending mounting verification.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_turn_left": [
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 2, "22": -16, "23": -24, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 3, "22": -15, "23": -23, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 5, "22": -13, "23": -21, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 19, "21": 6, "22": -11, "23": -19, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 8, "22": -9, "23": -17, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 26, "21": 9, "22": -6, "23": -14, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 28, "21": 9, "22": -3, "23": -11, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 10, "22": 1, "23": -7, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 10, "22": 4, "23": -4, "24": 0, "25": 0, "26": 90, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 30, "21": 10, "22": 7, "23": -1, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 28, "21": 9, "22": 11, "23": 3, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 26, "21": 9, "22": 14, "23": 6, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 8, "22": 17, "23": 9, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 19, "21": 6, "22": 19, "23": 11, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 5, "22": 21, "23": 13, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 3, "22": 23, "23": 15, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 2, "22": 24, "23": 16, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -2, "22": 24, "23": 16, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -3, "22": 23, "23": 15, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -5, "22": 21, "23": 13, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -19, "21": -6, "22": 19, "23": 11, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -8, "22": 17, "23": 9, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -26, "21": -9, "22": 14, "23": 6, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -28, "21": -9, "22": 11, "23": 3, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -10, "22": 7, "23": -1, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -10, "22": 4, "23": -4, "24": 0, "25": 0, "26": -90, "27": -90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -30, "21": -10, "22": 1, "23": -7, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -28, "21": -9, "22": -3, "23": -11, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -26, "21": -9, "22": -6, "23": -14, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -8, "22": -9, "23": -17, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -19, "21": -6, "22": -11, "23": -19, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -5, "22": -13, "23": -21, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -3, "22": -15, "23": -23, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -2, "22": -16, "23": -24, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_turn_right

Source: `turn(1, 1000, -1)`, `otto9.py` lines 250–266. Python RIGHT branch; direction pending mounting verification.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_turn_right": [
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": 5, "22": -16, "23": -24, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": 10, "22": -15, "23": -23, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 15, "22": -13, "23": -21, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": 19, "22": -11, "23": -19, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": 23, "22": -9, "23": -17, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": 26, "22": -6, "23": -14, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": 28, "22": -3, "23": -11, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 30, "22": 1, "23": -7, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 30, "22": 4, "23": -4, "24": 0, "25": 0, "26": 90, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 30, "22": 7, "23": -1, "24": 0, "25": 0, "26": 89, "27": 89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": 28, "22": 11, "23": 3, "24": 0, "25": 0, "26": 85, "27": 85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": 26, "22": 14, "23": 6, "24": 0, "25": 0, "26": 78, "27": 78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": 23, "22": 17, "23": 9, "24": 0, "25": 0, "26": 69, "27": 69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": 19, "22": 19, "23": 11, "24": 0, "25": 0, "26": 58, "27": 58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": 15, "22": 21, "23": 13, "24": 0, "25": 0, "26": 45, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": 10, "22": 23, "23": 15, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": 5, "22": 24, "23": 16, "24": 0, "25": 0, "26": 16, "27": 16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": -5, "22": 24, "23": 16, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": -10, "22": 23, "23": 15, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -15, "22": 21, "23": 13, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": -19, "22": 19, "23": 11, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": -23, "22": 17, "23": 9, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": -26, "22": 14, "23": 6, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": -28, "22": 11, "23": 3, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -30, "22": 7, "23": -1, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -30, "22": 4, "23": -4, "24": 0, "25": 0, "26": -90, "27": -90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -30, "22": 1, "23": -7, "24": 0, "25": 0, "26": -89, "27": -89}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": -28, "22": -3, "23": -11, "24": 0, "25": 0, "26": -85, "27": -85}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": -26, "22": -6, "23": -14, "24": 0, "25": 0, "26": -78, "27": -78}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": -23, "22": -9, "23": -17, "24": 0, "25": 0, "26": -69, "27": -69}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": -19, "22": -11, "23": -19, "24": 0, "25": 0, "26": -58, "27": -58}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": -15, "22": -13, "23": -21, "24": 0, "25": 0, "26": -45, "27": -45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": -10, "22": -15, "23": -23, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": -5, "22": -16, "23": -24, "24": 0, "25": 0, "26": -16, "27": -16}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -16, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_bend_left

Source: `bend(1, 1000, 1)`, `otto9.py` lines 273–299. Three poses; source800ms dwell omitted.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [400.0, 400.0, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_bend_left": [
      {"moves": {"20": 0, "21": 0, "22": -50, "23": -55, "24": 0, "25": 0, "26": 30, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -50, "23": 15, "24": 0, "25": 0, "26": -30, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_bend_right

Source: `bend(1, 1000, -1)`, `otto9.py` lines 273–299. Three poses; source800ms dwell omitted.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [400.0, 400.0, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_bend_right": [
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 10, "24": 0, "25": 0, "26": 30, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -15, "23": 30, "24": 0, "25": 0, "26": -30, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_shake_leg_left

Source: `shakeLeg(1, 1500, 1)`, `otto9.py` lines 306–346. Eight poses incl. both neutral returns; final500ms hold omitted.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [500.0, 500.0, 125.0, 125.0, 500, 125.0, 125.0, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_shake_leg_left": [
      {"moves": {"20": 0, "21": 0, "22": -50, "23": -55, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -50, "23": 30, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -20, "23": -30, "24": 0, "25": 0, "26": -10, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -50, "23": 30, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -20, "23": -30, "24": 0, "25": 0, "26": -10, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -50, "23": 30, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_shake_leg_right

Source: `shakeLeg(1, 1500, -1)`, `otto9.py` lines 306–346. Eight poses; foot endpoint75 signed; final500ms hold omitted.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [500.0, 500.0, 125.0, 125.0, 500, 125.0, 125.0, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_shake_leg_right": [
      {"moves": {"20": 0, "21": 0, "22": 75, "23": 50, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -30, "23": 32, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 32, "24": 0, "25": 0, "26": -10, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -30, "23": 32, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 32, "24": 0, "25": 0, "26": -10, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -30, "23": 32, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_updown

Source: `updown(1, 1000, 15)`, `otto9.py` lines 354–364. h15; legs neutral, feet and arms oppose.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_updown": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -1, "24": 0, "25": 0, "26": 1, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -2, "24": 0, "25": 0, "26": 2, "27": -2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -4, "24": 0, "25": 0, "26": 4, "27": -4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -5, "24": 0, "25": 0, "26": 5, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -7, "24": 0, "25": 0, "26": 8, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -12, "24": 0, "25": 0, "26": 12, "27": -12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 18, "23": -18, "24": 0, "25": 0, "26": 18, "27": -18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": -22, "24": 0, "25": 0, "26": 22, "27": -22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": -25, "24": 0, "25": 0, "26": 25, "27": -25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 26, "23": -26, "24": 0, "25": 0, "26": 26, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 28, "23": -28, "24": 0, "25": 0, "26": 28, "27": -28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": -29, "24": 0, "25": 0, "26": 29, "27": -29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -30, "24": 0, "25": 0, "26": 30, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -30, "24": 0, "25": 0, "26": 30, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -30, "24": 0, "25": 0, "26": 30, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": -29, "24": 0, "25": 0, "26": 29, "27": -29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 28, "23": -28, "24": 0, "25": 0, "26": 28, "27": -28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 26, "23": -26, "24": 0, "25": 0, "26": 26, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": -25, "24": 0, "25": 0, "26": 25, "27": -25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -23, "24": 0, "25": 0, "26": 23, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 18, "23": -18, "24": 0, "25": 0, "26": 18, "27": -18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -12, "24": 0, "25": 0, "26": 12, "27": -12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 10, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -8, "24": 0, "25": 0, "26": 8, "27": -8}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -5, "24": 0, "25": 0, "26": 5, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -4, "24": 0, "25": 0, "26": 4, "27": -4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -2, "24": 0, "25": 0, "26": 2, "27": -2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -1, "24": 0, "25": 0, "26": 1, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_swing

Source: `swing(1, 1000, 15)`, `otto9.py` lines 371–379. h15; half-height foot offsets, full-height arm offsets.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_swing": [
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -8, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -5, "24": 0, "25": 0, "26": 18, "27": -12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -2, "24": 0, "25": 0, "26": 20, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": 0, "24": 0, "25": 0, "26": 22, "27": -8}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": 2, "24": 0, "25": 0, "26": 25, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": 4, "24": 0, "25": 0, "26": 26, "27": -4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": 5, "24": 0, "25": 0, "26": 28, "27": -2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 7, "24": 0, "25": 0, "26": 29, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 7, "24": 0, "25": 0, "26": 30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 8, "24": 0, "25": 0, "26": 30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 7, "24": 0, "25": 0, "26": 30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 7, "24": 0, "25": 0, "26": 29, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": 5, "24": 0, "25": 0, "26": 28, "27": -2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": 4, "24": 0, "25": 0, "26": 26, "27": -4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": 2, "24": 0, "25": 0, "26": 25, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": 0, "24": 0, "25": 0, "26": 23, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -2, "24": 0, "25": 0, "26": 20, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -5, "24": 0, "25": 0, "26": 18, "27": -12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -7, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -10, "24": 0, "25": 0, "26": 12, "27": -18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -13, "24": 0, "25": 0, "26": 10, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -15, "24": 0, "25": 0, "26": 7, "27": -22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -2, "23": -17, "24": 0, "25": 0, "26": 5, "27": -25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -4, "23": -19, "24": 0, "25": 0, "26": 4, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -20, "24": 0, "25": 0, "26": 2, "27": -28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -7, "23": -22, "24": 0, "25": 0, "26": 1, "27": -29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -7, "23": -22, "24": 0, "25": 0, "26": 0, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -8, "23": -22, "24": 0, "25": 0, "26": 0, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -7, "23": -22, "24": 0, "25": 0, "26": 0, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -7, "23": -22, "24": 0, "25": 0, "26": 1, "27": -29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -20, "24": 0, "25": 0, "26": 2, "27": -28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -4, "23": -19, "24": 0, "25": 0, "26": 4, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -2, "23": -17, "24": 0, "25": 0, "26": 5, "27": -25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -15, "24": 0, "25": 0, "26": 8, "27": -22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -13, "24": 0, "25": 0, "26": 10, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -10, "24": 0, "25": 0, "26": 12, "27": -18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -8, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_tiptoe_swing

Source: `tiptoeSwing(1, 1000, 15)`, `otto9.py` lines 386–394. h15; feet and arms have full offsets.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_tiptoe_swing": [
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 18, "23": -12, "24": 0, "25": 0, "26": 18, "27": -12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -10, "24": 0, "25": 0, "26": 20, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": -8, "24": 0, "25": 0, "26": 22, "27": -8}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": -5, "24": 0, "25": 0, "26": 25, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 26, "23": -4, "24": 0, "25": 0, "26": 26, "27": -4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 28, "23": -2, "24": 0, "25": 0, "26": 28, "27": -2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": -1, "24": 0, "25": 0, "26": 29, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 0, "24": 0, "25": 0, "26": 30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 0, "24": 0, "25": 0, "26": 30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 0, "24": 0, "25": 0, "26": 30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": -1, "24": 0, "25": 0, "26": 29, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 28, "23": -2, "24": 0, "25": 0, "26": 28, "27": -2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 26, "23": -4, "24": 0, "25": 0, "26": 26, "27": -4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": -5, "24": 0, "25": 0, "26": 25, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -7, "24": 0, "25": 0, "26": 23, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -10, "24": 0, "25": 0, "26": 20, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 18, "23": -12, "24": 0, "25": 0, "26": 18, "27": -12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -18, "24": 0, "25": 0, "26": 12, "27": -18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -20, "24": 0, "25": 0, "26": 10, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -22, "24": 0, "25": 0, "26": 7, "27": -22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -25, "24": 0, "25": 0, "26": 5, "27": -25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -26, "24": 0, "25": 0, "26": 4, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -28, "24": 0, "25": 0, "26": 2, "27": -28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -29, "24": 0, "25": 0, "26": 1, "27": -29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -30, "24": 0, "25": 0, "26": 0, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -30, "24": 0, "25": 0, "26": 0, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -30, "24": 0, "25": 0, "26": 0, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -29, "24": 0, "25": 0, "26": 1, "27": -29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -28, "24": 0, "25": 0, "26": 2, "27": -28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -26, "24": 0, "25": 0, "26": 4, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -25, "24": 0, "25": 0, "26": 5, "27": -25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -22, "24": 0, "25": 0, "26": 8, "27": -22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -20, "24": 0, "25": 0, "26": 10, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -18, "24": 0, "25": 0, "26": 12, "27": -18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 15, "27": -15}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_jitter

Source: `jitter(1, 1000, 15)`, `otto9.py` lines 401–413. h15; hips vary, feet/arms neutral.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_jitter": [
      {"moves": {"20": -15, "21": 15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": 15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -14, "21": 14, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -13, "21": 13, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": 5, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": 3, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": -3, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": -5, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 7, "21": -7, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 13, "21": -13, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 14, "21": -14, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": -15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": -15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": -15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 14, "21": -14, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 13, "21": -13, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 5, "21": -5, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": -3, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": 3, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -5, "21": 5, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -7, "21": 7, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -13, "21": 13, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -14, "21": 14, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": 15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": 15, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_ascending_turn

Source: `ascendingTurn(1, 1000, 15)`, `otto9.py` lines 420–431. Source caps h to13; arms amplitude40.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_ascending_turn": [
      {"moves": {"20": -13, "21": 13, "22": 4, "23": 4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -13, "21": 13, "22": 4, "23": 4, "24": 0, "25": 0, "26": 7, "27": 7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 5, "23": 3, "24": 0, "25": 0, "26": 14, "27": 14}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 6, "23": 2, "24": 0, "25": 0, "26": 20, "27": 20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": 7, "23": 1, "24": 0, "25": 0, "26": 26, "27": 26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": 9, "23": -1, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": 7, "22": 10, "23": -2, "24": 0, "25": 0, "26": 35, "27": 35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -4, "21": 4, "22": 13, "23": -5, "24": 0, "25": 0, "26": 38, "27": 38}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": 2, "22": 15, "23": -7, "24": 0, "25": 0, "26": 39, "27": 39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -9, "24": 0, "25": 0, "26": 40, "27": 40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": -2, "22": 19, "23": -11, "24": 0, "25": 0, "26": 39, "27": 39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 4, "21": -4, "22": 21, "23": -13, "24": 0, "25": 0, "26": 38, "27": 38}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": -6, "22": 24, "23": -15, "24": 0, "25": 0, "26": 35, "27": 35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": 25, "23": -17, "24": 0, "25": 0, "26": 31, "27": 31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": 27, "23": -19, "24": 0, "25": 0, "26": 26, "27": 26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 28, "23": -20, "24": 0, "25": 0, "26": 20, "27": 20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 29, "23": -21, "24": 0, "25": 0, "26": 14, "27": 14}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 13, "21": -13, "22": 30, "23": -22, "24": 0, "25": 0, "26": 7, "27": 7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 13, "21": -13, "22": 30, "23": -22, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 13, "21": -13, "22": 30, "23": -22, "24": 0, "25": 0, "26": -7, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 29, "23": -21, "24": 0, "25": 0, "26": -14, "27": -14}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 28, "23": -20, "24": 0, "25": 0, "26": -20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": 27, "23": -19, "24": 0, "25": 0, "26": -26, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": 25, "23": -17, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 7, "21": -7, "22": 24, "23": -16, "24": 0, "25": 0, "26": -35, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 4, "21": -4, "22": 21, "23": -13, "24": 0, "25": 0, "26": -38, "27": -38}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": -2, "22": 19, "23": -11, "24": 0, "25": 0, "26": -39, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -9, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": 2, "22": 15, "23": -7, "24": 0, "25": 0, "26": -39, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -4, "21": 4, "22": 13, "23": -5, "24": 0, "25": 0, "26": -38, "27": -38}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": 6, "22": 11, "23": -3, "24": 0, "25": 0, "26": -35, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": 9, "23": -1, "24": 0, "25": 0, "26": -31, "27": -31}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": 7, "23": 1, "24": 0, "25": 0, "26": -26, "27": -26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 6, "23": 2, "24": 0, "25": 0, "26": -20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 5, "23": 3, "24": 0, "25": 0, "26": -14, "27": -14}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -13, "21": 13, "22": 4, "23": 4, "24": 0, "25": 0, "26": -7, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -13, "21": 13, "22": 4, "23": 4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_moonwalker_left

Source: `moonwalker(1, 1000, 15, 1)`, `otto9.py` lines 439–455. Python LEFT, not browser label; source phase offsets preserved.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_moonwalker_left": [
      {"moves": {"20": 0, "21": 0, "22": -6, "23": -17, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -19, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -21, "24": 0, "25": 0, "26": -29, "27": 1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -3, "23": -22, "24": 0, "25": 0, "26": -28, "27": 2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -2, "23": -24, "24": 0, "25": 0, "26": -26, "27": 4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -24, "24": 0, "25": 0, "26": -25, "27": 5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -24, "24": 0, "25": 0, "26": -22, "27": 8}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -24, "24": 0, "25": 0, "26": -20, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -24, "24": 0, "25": 0, "26": -18, "27": 12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -22, "24": 0, "25": 0, "26": -15, "27": 15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -21, "24": 0, "25": 0, "26": -12, "27": 18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -19, "24": 0, "25": 0, "26": -10, "27": 20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -17, "24": 0, "25": 0, "26": -8, "27": 22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": -15, "24": 0, "25": 0, "26": -5, "27": 25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 21, "23": -12, "24": 0, "25": 0, "26": -4, "27": 26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": -10, "24": 0, "25": 0, "26": -2, "27": 28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -7, "24": 0, "25": 0, "26": -1, "27": 29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -4, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -2, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 0, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 2, "24": 0, "25": 0, "26": -1, "27": 29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 3, "24": 0, "25": 0, "26": -2, "27": 28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 21, "23": 5, "24": 0, "25": 0, "26": -4, "27": 26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": 5, "24": 0, "25": 0, "26": -5, "27": 25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": 6, "24": 0, "25": 0, "26": -7, "27": 23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": 5, "24": 0, "25": 0, "26": -10, "27": 20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": 5, "24": 0, "25": 0, "26": -12, "27": 18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": 3, "24": 0, "25": 0, "26": -15, "27": 15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": 2, "24": 0, "25": 0, "26": -18, "27": 12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": 0, "24": 0, "25": 0, "26": -20, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -2, "24": 0, "25": 0, "26": -22, "27": 8}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -4, "24": 0, "25": 0, "26": -25, "27": 5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -2, "23": -7, "24": 0, "25": 0, "26": -26, "27": 4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -3, "23": -10, "24": 0, "25": 0, "26": -28, "27": 2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -12, "24": 0, "25": 0, "26": -29, "27": 1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -15, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -6, "23": -17, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_moonwalker_right

Source: `moonwalker(1, 1000, 15, -1)`, `otto9.py` lines 439–455. Python RIGHT, not browser label; source phase offsets preserved.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_moonwalker_right": [
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -2, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -4, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -7, "24": 0, "25": 0, "26": -1, "27": 29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": -9, "24": 0, "25": 0, "26": -2, "27": 28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 21, "23": -12, "24": 0, "25": 0, "26": -4, "27": 26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": -15, "24": 0, "25": 0, "26": -5, "27": 25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -17, "24": 0, "25": 0, "26": -7, "27": 23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -19, "24": 0, "25": 0, "26": -10, "27": 20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -21, "24": 0, "25": 0, "26": -12, "27": 18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -22, "24": 0, "25": 0, "26": -15, "27": 15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -24, "24": 0, "25": 0, "26": -18, "27": 12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -24, "24": 0, "25": 0, "26": -20, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -24, "24": 0, "25": 0, "26": -22, "27": 8}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -24, "24": 0, "25": 0, "26": -25, "27": 5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -2, "23": -24, "24": 0, "25": 0, "26": -26, "27": 4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -3, "23": -22, "24": 0, "25": 0, "26": -28, "27": 2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -21, "24": 0, "25": 0, "26": -29, "27": 1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -19, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -6, "23": -17, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -15, "24": 0, "25": 0, "26": -30, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -12, "24": 0, "25": 0, "26": -29, "27": 1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -3, "23": -10, "24": 0, "25": 0, "26": -28, "27": 2}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -2, "23": -7, "24": 0, "25": 0, "26": -26, "27": 4}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -4, "24": 0, "25": 0, "26": -25, "27": 5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -2, "24": 0, "25": 0, "26": -23, "27": 7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": 0, "24": 0, "25": 0, "26": -20, "27": 10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": 2, "24": 0, "25": 0, "26": -18, "27": 12}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 9, "23": 3, "24": 0, "25": 0, "26": -15, "27": 15}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": 5, "24": 0, "25": 0, "26": -12, "27": 18}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": 5, "24": 0, "25": 0, "26": -10, "27": 20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": 6, "24": 0, "25": 0, "26": -8, "27": 22}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": 5, "24": 0, "25": 0, "26": -5, "27": 25}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 21, "23": 5, "24": 0, "25": 0, "26": -4, "27": 26}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": 3, "24": 0, "25": 0, "26": -2, "27": 28}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 2, "24": 0, "25": 0, "26": -1, "27": 29}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": 0, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -2, "24": 0, "25": 0, "26": 0, "27": 30}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_crusaito_left

Source: `crusaito(1, 1000, 15, 1)`, `otto9.py` lines 463–469. Literal90-radian hip phase retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_crusaito_left": [
      {"moves": {"20": 22, "21": 22, "22": 12, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 20, "21": 20, "22": 14, "23": -23, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 17, "21": 17, "22": 17, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 14, "21": 14, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": 21, "23": -17, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": 6, "22": 23, "23": -14, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 1, "21": 1, "22": 24, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": -3, "22": 26, "23": -9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -7, "21": -7, "22": 26, "23": -6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": -11, "22": 26, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": 26, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -18, "21": -18, "22": 26, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -21, "21": -21, "22": 24, "23": 1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": 23, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 21, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 19, "23": 4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 17, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 14, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -22, "21": -22, "22": 12, "23": 1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -20, "21": -20, "22": 9, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -17, "21": -17, "22": 6, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -14, "21": -14, "22": 4, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": 2, "23": -6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": -6, "22": 0, "23": -9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -1, "21": -1, "22": -1, "23": -11, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": 3, "22": -3, "23": -14, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 7, "21": 7, "22": -3, "23": -17, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": 11, "22": -4, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": -3, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 18, "21": 18, "22": -3, "23": -23, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 21, "21": 21, "22": -1, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": 0, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 2, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 4, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 6, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 9, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 22, "21": 22, "22": 11, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_crusaito_right

Source: `crusaito(1, 1000, 15, -1)`, `otto9.py` lines 463–469. Literal90-radian hip phase retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_crusaito_right": [
      {"moves": {"20": 22, "21": 22, "22": 12, "23": 1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 20, "21": 20, "22": 14, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 17, "21": 17, "22": 17, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 14, "21": 14, "22": 19, "23": 4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": 21, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": 6, "22": 23, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 1, "21": 1, "22": 24, "23": 1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": -3, "22": 26, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -7, "21": -7, "22": 26, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": -11, "22": 26, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": 26, "23": -6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -18, "21": -18, "22": 26, "23": -9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -21, "21": -21, "22": 24, "23": -11, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": 23, "23": -14, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 21, "23": -17, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 17, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 14, "23": -23, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -22, "21": -22, "22": 12, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -20, "21": -20, "22": 9, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -17, "21": -17, "22": 6, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -14, "21": -14, "22": 4, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": 2, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": -6, "22": 0, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -1, "21": -1, "22": -1, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": 3, "22": -3, "23": -23, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 7, "21": 7, "22": -3, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": 11, "22": -4, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": -3, "23": -17, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 18, "21": 18, "22": -3, "23": -14, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 21, "21": 21, "22": -1, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": 0, "23": -9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 2, "23": -6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 4, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 6, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 9, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 22, "21": 22, "22": 11, "23": 1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_flapping_forward

Source: `flapping(1, 1000, 15, 1)`, `otto9.py` lines 477–483. Arms neutral; h15.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_flapping_forward": [
      {"moves": {"20": 0, "21": 0, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": -2, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 4, "21": -4, "22": -9, "23": 9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": -6, "22": -8, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": -6, "23": 6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": -9, "22": -5, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": -2, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 2, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 5, "23": -5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 8, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 10, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": 12, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": -9, "22": 15, "23": -15, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": 16, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": -6, "22": 18, "23": -18, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 4, "21": -4, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": -2, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": 2, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -4, "21": 4, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": 6, "22": 18, "23": -18, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": 16, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": 9, "22": 15, "23": -15, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": 13, "23": -13, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 10, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 8, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 5, "23": -5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 2, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": -2, "23": 2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": 9, "22": -5, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": -6, "23": 6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": 6, "22": -8, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -4, "21": 4, "22": -9, "23": 9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": 2, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_flapping_backward

Source: `flapping(1, 1000, 15, -1)`, `otto9.py` lines 477–483. Arms neutral; h15.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_flapping_backward": [
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": -2, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 4, "21": -4, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": -6, "22": 18, "23": -18, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": 16, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": -9, "22": 15, "23": -15, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": 13, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 10, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 8, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 5, "23": -5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 12, "21": -12, "22": 2, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": -11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": -10, "22": -2, "23": 2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 9, "21": -9, "22": -5, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 8, "21": -8, "22": -6, "23": 6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": -6, "22": -8, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 4, "21": -4, "22": -9, "23": 9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 2, "21": -2, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": 2, "22": -10, "23": 10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -4, "21": 4, "22": -9, "23": 9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": 6, "22": -8, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": -6, "23": 6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": 9, "22": -5, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": -3, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 2, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 5, "23": -5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -12, "21": 12, "22": 8, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": 11, "22": 10, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": 10, "22": 12, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -9, "21": 9, "22": 15, "23": -15, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -8, "21": 8, "22": 16, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": 6, "22": 18, "23": -18, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -4, "21": 4, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -2, "21": 2, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_hands_up

Source: `handsup()`, `otto9.py` lines 486–489. LA−70 RA+70; lower body neutral.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [1000] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_hands_up": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -70, "27": 70}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_wave_left_arm

Source: `handwave(-1)`, `otto9.py` lines 492–505. Source RIGHT actually moves LA/GPIO26; five cycles.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_wave_left_arm": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -2, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -4, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -7, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -11, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -15, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -20, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -25, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -60, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -58, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -56, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -53, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -49, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -45, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -40, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -35, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": -30, "27": -40}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_wave_right_arm

Source: `handwave(1)`, `otto9.py` lines 492–505. Source LEFT actually moves RA/GPIO27; one cycle.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1000 ms; sampled geometry only. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_wave_right_arm": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 60}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 65}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 70}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 75}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 79}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 83}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 86}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 88}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 90}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 88}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 86}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 83}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 79}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 75}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 70}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 65}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 60}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 55}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 50}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 41}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 34}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 32}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 32}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 34}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 41}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 45}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 50}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 55}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 40, "27": 60}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_happy

Source: `playGesture(OTTOHAPPY)`, `otto9.py` lines 732–739. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 800 ms; sampled geometry only. Source fixed-pose duration arguments in order: [500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_happy": [
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -7, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -3, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": 0, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": 3, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": 5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": 7, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": 9, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 10, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 10, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": 10, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": 9, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": 7, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": 5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": 3, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": 0, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -3, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -7, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -13, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -17, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -20, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -3, "23": -23, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -25, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -7, "23": -27, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -9, "23": -29, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -10, "23": -30, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -10, "23": -30, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -10, "23": -30, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -9, "23": -29, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -7, "23": -27, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -5, "23": -25, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -3, "23": -23, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -20, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -17, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -13, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_superhappy

Source: `playGesture(OTTOSUPERHAPPY)`, `otto9.py` lines 740–749. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 500, 500 ms; sampled geometry only. Source fixed-pose duration arguments in order: [500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_superhappy": [
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_sad

Source: `playGesture(OTTOSAD)`, `otto9.py` lines 750–767. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [700, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_sad": [
      {"moves": {"20": 20, "21": -20, "22": -70, "23": 70, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_sleeping

Source: `playGesture(OTTOSLEEPING)`, `otto9.py` lines 768–788. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [700, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_sleeping": [
      {"moves": {"20": 10, "21": -10, "22": -30, "23": 30, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_fart

Source: `playGesture(OTTOFART)`, `otto9.py` lines 789–811. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [500, 500, 500, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_fart": [
      {"moves": {"20": 0, "21": 0, "22": 55, "23": 32, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": -10, "23": 32, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 55, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_confused

Source: `playGesture(OTTOCONFUSED)`, `otto9.py` lines 812–819. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [300, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_confused": [
      {"moves": {"20": 20, "21": -20, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_love

Source: `playGesture(OTTOLOVE)`, `otto9.py` lines 820–827. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 1500 ms; sampled geometry only. Source fixed-pose duration arguments in order: [500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_love": [
      {"moves": {"20": 22, "21": 22, "22": 16, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 20, "21": 20, "22": 21, "23": -36, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 17, "21": 17, "22": 25, "23": -33, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 14, "21": 14, "22": 29, "23": -29, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": 33, "23": -25, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": 6, "22": 36, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 1, "21": 1, "22": 38, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": -3, "22": 40, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -7, "21": -7, "22": 41, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": -11, "22": 42, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": 41, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -18, "21": -18, "22": 40, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -21, "21": -21, "22": 38, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": 36, "23": 7, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 33, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 29, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 25, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 21, "23": 7, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -22, "21": -22, "22": 17, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -20, "21": -20, "22": 12, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -17, "21": -17, "22": 8, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -14, "21": -14, "22": 4, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": 0, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": -6, "22": -3, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -1, "21": -1, "22": -5, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": 3, "22": -7, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 7, "21": 7, "22": -8, "23": -25, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": 11, "22": -8, "23": -29, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": -8, "23": -33, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 18, "21": 18, "22": -7, "23": -36, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 21, "21": 21, "22": -5, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": -3, "23": -40, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 0, "23": -41, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 4, "23": -42, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 8, "23": -41, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 12, "23": -40, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 22, "21": 22, "22": 16, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 20, "21": 20, "22": 21, "23": -36, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 17, "21": 17, "22": 25, "23": -33, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 14, "21": 14, "22": 29, "23": -29, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 10, "21": 10, "22": 33, "23": -25, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 6, "21": 6, "22": 36, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 1, "21": 1, "22": 38, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -3, "21": -3, "22": 40, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -7, "21": -7, "22": 41, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -11, "21": -11, "22": 42, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -15, "21": -15, "22": 41, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -18, "21": -18, "22": 40, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -21, "21": -21, "22": 38, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -23, "21": -23, "22": 36, "23": 7, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 33, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 29, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -25, "21": -25, "22": 25, "23": 8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -24, "21": -24, "22": 21, "23": 7, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -22, "21": -22, "22": 17, "23": 5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -20, "21": -20, "22": 12, "23": 3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -17, "21": -17, "22": 8, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -14, "21": -14, "22": 4, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -10, "21": -10, "22": 0, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -6, "21": -6, "22": -3, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -1, "21": -1, "22": -5, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 3, "21": 3, "22": -7, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 7, "21": 7, "22": -8, "23": -25, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 11, "21": 11, "22": -8, "23": -29, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 15, "21": 15, "22": -8, "23": -33, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 18, "21": 18, "22": -7, "23": -36, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 21, "21": 21, "22": -5, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 23, "21": 23, "22": -3, "23": -40, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 0, "23": -41, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 4, "23": -42, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 25, "21": 25, "22": 8, "23": -41, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 24, "21": 24, "22": 12, "23": -40, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 22, "21": 22, "22": 16, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_angry

Source: `playGesture(OTTOANGRY)`, `otto9.py` lines 828–845. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [300, 200, 200, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_angry": [
      {"moves": {"20": 0, "21": 0, "22": -20, "23": 20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 20, "21": 20, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": -20, "21": -20, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_fretful

Source: `playGesture(OTTOFRETFUL)`, `otto9.py` lines 846–861. Servo-only: sound/display/holds and detach omitted; source pose/submovement order retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source fixed-pose duration arguments in order: [100, 500, 100, 500, 100, 500, 100, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_fretful": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

### humanoid_gesture_victory

Source: `playGesture(OTTOVICTORY)`, `otto9.py` lines 906–926. Servo-only: sound/display/holds and detach omitted; first-ramp YL9 corrected to90; two foot ramps retained.

Mapping: YL→20, YR→21, RL→22, RR→23, LA→26, RA→27; each target is source angle minus 90°, without added inversion. Additional shoulders 24/25 stay at 0°. Physical reproduction requires the checks in Section 5. Source oscillator period(s): 500, 500 ms; sampled geometry only. Source fixed-pose duration arguments: 121 poses, unique values [10, 500] ms. No source duration or dwell is encoded by `S`.

```json
{
  "movements": {
    "humanoid_gesture_victory": [
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 6, "23": -6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -7, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 9, "23": -9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 11, "23": -11, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -13, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 14, "23": -14, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 16, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -17, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 18, "23": -18, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 21, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": -22, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -23, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": -25, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 26, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -27, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 28, "23": -28, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": -29, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -30, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 31, "23": -31, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 32, "23": -32, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -33, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 34, "23": -34, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -35, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 36, "23": -36, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -37, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 38, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -39, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": -40, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 41, "23": -41, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 42, "23": -42, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 43, "23": -43, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 44, "23": -44, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 45, "23": -45, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 46, "23": -46, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 47, "23": -47, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 48, "23": -48, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 49, "23": -49, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 50, "23": -50, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 51, "23": -51, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 52, "23": -52, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 53, "23": -53, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 54, "23": -54, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 55, "23": -55, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 56, "23": -56, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 57, "23": -57, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 58, "23": -58, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 59, "23": -59, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 60, "23": -60, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 59, "23": -59, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 58, "23": -58, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 57, "23": -57, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 56, "23": -56, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 55, "23": -55, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 54, "23": -54, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 53, "23": -53, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 52, "23": -52, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 51, "23": -51, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 50, "23": -50, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 49, "23": -49, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 48, "23": -48, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 47, "23": -47, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 46, "23": -46, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 45, "23": -45, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 44, "23": -44, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 43, "23": -43, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 42, "23": -42, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 41, "23": -41, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": -40, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -39, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 38, "23": -38, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -37, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 36, "23": -36, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -35, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 34, "23": -34, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -33, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 32, "23": -32, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 31, "23": -31, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -30, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 29, "23": -29, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 28, "23": -28, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -27, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 26, "23": -26, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 25, "23": -25, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 24, "23": -24, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -23, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 22, "23": -22, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 21, "23": -21, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 19, "23": -19, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 18, "23": -18, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -17, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 16, "23": -16, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 15, "23": -15, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 14, "23": -14, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -13, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 12, "23": -12, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 11, "23": -11, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -10, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 9, "23": -9, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 8, "23": -8, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -7, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 6, "23": -6, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -5, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 4, "23": -4, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -3, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 2, "23": -2, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -1, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 40, "23": 0, "24": 0, "25": 0, "26": 40, "27": 0}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 39, "23": -1, "24": 0, "25": 0, "26": 39, "27": -1}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 37, "23": -3, "24": 0, "25": 0, "26": 37, "27": -3}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 35, "23": -5, "24": 0, "25": 0, "26": 35, "27": -5}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 33, "23": -7, "24": 0, "25": 0, "26": 33, "27": -7}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 30, "23": -10, "24": 0, "25": 0, "26": 30, "27": -10}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 27, "23": -13, "24": 0, "25": 0, "26": 27, "27": -13}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 23, "23": -17, "24": 0, "25": 0, "26": 23, "27": -17}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": -40, "24": 0, "25": 0, "26": 0, "27": -40}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 1, "23": -39, "24": 0, "25": 0, "26": 1, "27": -39}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 3, "23": -37, "24": 0, "25": 0, "26": 3, "27": -37}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 5, "23": -35, "24": 0, "25": 0, "26": 5, "27": -35}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 7, "23": -33, "24": 0, "25": 0, "26": 7, "27": -33}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 10, "23": -30, "24": 0, "25": 0, "26": 10, "27": -30}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 13, "23": -27, "24": 0, "25": 0, "26": 13, "27": -27}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 17, "23": -23, "24": 0, "25": 0, "26": 17, "27": -23}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 20, "23": -20, "24": 0, "25": 0, "26": 20, "27": -20}, "speed": "S", "per_servo_speeds": {}},
      {"moves": {"20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0}, "speed": "S", "per_servo_speeds": {}}
    ]
  }
}
```

<!-- HUMANOID_LIBRARY_END -->

## 4. Movement mapping and adaptation notes

### Reproducible geometric conversion

The source vector order is `[YL, YR, RL, RR, LA, RA]`, mapped to `[20, 21, 22, 23, 26, 27]`. For each fixed source pose `q`, subtract 90 from each of these six values, insert shoulder targets 24/25 = 0, and emit one existing-format step. GPIO numbers are not a sequential relabeling of source slots: LA/RA must skip the two added shoulders.

For each source oscillator call with amplitude `A`, offset `O`, phase `ph` (radians), and cycle count `c`, this document uses:

```text
k = 0 … 36*c inclusive
source_q[i] = 90 + round(A[i] * sin(2*pi*k/36 + ph[i]) + O[i])
target[GPIO[i]] = source_q[i] - 90
```

The source formula rounds the **sum** of the sine and offset. Host floating-point values near half-degree ties can differ from MicroPython; the complete integer JSON here is the reproducible port output. Sampling at 36 intervals is a translation choice, not Otto's nominal 30 ms oscillator refresh schedule. Source `_execute` retains oscillator phase across calls; this library resets its mathematical sampling phase at each new `_execute` subcall, while continuing phase across cycles inside that call. It does not reproduce source wall-clock jitter, cached-position mismatch, stale phase or interpolation overshoot.

For fixed-pose `_moveServos(T,...)`, this pack preserves requested target poses, not the original 10 ms stepping implementation. That implementation can undershoot or overshoot intermediate writes and treats `T<=10` as immediate. Pi0 explicitly reaches the final target. Source `home()` detaches afterward; `humanoid_home` only requests nominal center and **keeps PWM holding**, because no release command exists in this JSON format.

### Source choices and adaptations

| Source behavior | Translation / consequence |
|---|---|
| Four-servo Otto motion methods have Humanoid arm extensions | Generate in six-servo mode and map LA/RA to 26/27. `jitter` and `flapping` keep arms neutral; other methods follow their source parameters. |
| Directional gait names | `LEFT=+1`, `RIGHT=−1`, `FORWARD=+1`, `BACKWARD=−1` identify Python source branches. Names do not prove physical travel direction on the target. Browser remote labels are not used to override the Python branch. |
| Walking and turning arm amplitudes | Retain source amplitude 90° (target ±90°). This is a travel-limit test item, not a safe-clearance claim. Do not run full gaits until endpoints and entry transitions have been checked. |
| Additional fore/aft shoulders | No verified mounting sign or phase is available. Keep 24/25 at nominal 0 in all steps. Natural contralateral shoulder swing is deferred; record direction and clearance first, then develop a separately reviewed adaptation. Existing LA/RA motion is not automatically reassigned to shoulders. |
| `jump(steps,T)` | Source ignores `steps`; the port has one up/down pair. No claim that this robot becomes airborne. |
| `bend` and `shakeLeg` | Preserve source pose order, including neutral returns inside shakeLeg. Source dwell (800 ms for selected bend; 500 ms final shake hold) cannot be retained. |
| `ascendingTurn(...,h=15)` | Source caps h at 13; retain capped parameters, including source foot offsets `h+4` and `−h+4`. |
| `crusaito` | Retain its literal `90` radians phase value for hips. Do not silently “correct” it to `pi/2`. LOVE inherits this source quirk. |
| `handwave(RIGHT)` | Actually oscillates LA/GPIO26 for five cycles. Named `humanoid_wave_left_arm` by physical mapping. The other arm stays at its source offset. |
| `handwave(LEFT)` | Actually oscillates RA/GPIO27 for one cycle. Named `humanoid_wave_right_arm`. The asymmetry is retained, not an omitted repeat. |
| Ten gesture ports | Preserve servo-pose/submovement order while omitting sounds, mouth animation, pauses and detach. Emotional expression and timing are therefore incomplete; SAD/SLEEPING may look like brief pose-and-return rather than sustained gestures. |
| `OTTOVICTORY` | Explicit target adaptation: change the first ramp's source YL **9°** to nominal **90°**, avoiding the unverified −81° hip excursion. Preserve two 60-pose foot ramps, two tiptoe waves and final home. This is not a verbatim source port. |
| Consecutive `home()` in FRETFUL | Source resting flag makes the final redundant home a no-op; four pose/home pairs yield eight keyframes. No extra hold or ninth step is invented. |

No sign inversion is supported by measured target evidence. If a joint's mounting reverses the intended direction, establish that on hardware before revising its numeric targets; do not add an unsupported `invert` step field. A narrower calibrated range may clamp this library and change gait shape. Full-range values are reference targets awaiting clearance checks, not mechanically qualified defaults.

### Explicit omissions and future requirements

| Source item | Why it has no JSON movement here |
|---|---|
| `OTTOMAGIC` | Sound and display only; no servo trajectory to port. Requires caller-level audio/display coordination. |
| `OTTOWAVE` gesture | Mouth animation and sound only. This is different from servo method `handwave`, whose two arm variants are included. |
| `OTTOFAIL` | Depends on release/unpowered collapse and recovery. A powered waypoint approximation would materially change behavior; omitted until release, timing and a supported physical recovery procedure exist. |
| Songs, mouths, animations and remote numeric IDs | Not servo movement definitions. They are not invented as JSON movement parameters or duplicate names. |
| Spider `Poweroff` | Spider geometry must not be copied into Humanoid shutdown. The separate owner-supplied Humanoid `Poweroff` below uses Humanoid geometry. Existing installed Spider definitions remain untouched; no `Wave_Left_Hand` entry is added. |

Exact Otto periods, pauses, phase continuity between independently invoked movements, synchronized arrival, and multimodal gestures would require a separate future timing/oscillator controller or caller orchestration. Such timing/oscillator changes remain outside the native catalog integration. Repeating identical zero-distance steps, using a zero speed limit, or adding unrecognized timing keys does not solve these limitations.

## 5. Validation and testing guide

### Initial research host validation (before native integration)

The completed JSON was parsed and checked against the **actual** `NinjaConfig`, `validate_movement`, `available_movements`, `save_config` and `load_config`. All 34 entries and 1,203 steps passed. An inert driver exercised the actual `MovementController` with reversed pin order, verifying target remapping, speed modes, first/middle/last easing and every emitted step. The HAL import was stubbed so no peripherals or pigpio were initialized.

All 34 definitions were rejected with each of eight required pins missing (272 cases) and with each incompatible profile, Spider/Tire (68 cases). A bad later step was rejected before any driver output for unavailable pin, out-of-range angle and unsupported duration. A false driver completion stopped after the first step with `EmergencyStop`. Temporary configuration save/load preserved the full pack. Names were disjoint from the installed Spider catalog. Every six-joint value matched its captured source target minus 90 and every shoulder value remained zero.

Source extraction ran the local Otto method bodies with inert peripherals and a fake clock. It captured pose and oscillator calls rather than operating hardware. The complete source branches, direction choices, gestures, sampling formula and VICTORY exception were cross-checked. The verification does **not** establish physical speed, neutral, balance, travel direction, actual PWM behavior, gait similarity on a floor or mechanical safety.

### Offline extraction and merge preview

Save the Python below as a temporary script and run it with the project's already configured Python environment from the NinjaRobotPi0 root. Arguments are the Markdown path, an **existing** calibrated Humanoid core configuration path, and a **new** preview output path. It performs no HAL imports, server startup, servo-tool launch, movement execution or live configuration replacement. The output may contain private configuration fields, so it is created with mode 0600 and must not be committed or shared. Use a private directory.

```python
import json
import os
import re
import sys
from pathlib import Path
from ninja_core.config import NinjaConfig
from ninja_core.builtin_movements import validate_movement

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result

def parse(text):
    return json.loads(text, object_pairs_hook=unique_object)

markdown, existing, output = map(Path, sys.argv[1:4])
content = markdown.read_text()
start_marker = "<!-- HUMANOID_LIBRARY_START -->"
end_marker = "<!-- HUMANOID_LIBRARY_END -->"
# Use standalone marker lines, excluding these string literals in this script.
start = re.search(r"^" + re.escape(start_marker) + r"$", content, re.M).end()
end = re.search(r"^" + re.escape(end_marker) + r"$", content, re.M).start()
blocks = re.findall(r"^```json\n(.*?)\n```", content[start:end], re.M | re.S)
pack = {}
for block in blocks:
    fragment = parse(block)
    if set(fragment) != {"movements"}:
        raise ValueError("Unexpected envelope")
    for name, steps in fragment["movements"].items():
        if not name.startswith("humanoid_") or name in pack:
            raise ValueError("Invalid or duplicate movement name")
        pack[name] = steps
if len(pack) != 34 or sum(map(len, pack.values())) != 1203:
    raise ValueError("Incomplete library; review document version")
# Read explicitly: load_config would create defaults if the file were absent.
data = parse(existing.read_text())
config = NinjaConfig.model_validate(data)
if config.robot_type != "humanoid":
    raise ValueError("Commission and select the Humanoid profile first")
pins = {int(p) for p in config.servos.calibration}
if not set(range(20, 28)) <= pins:
    raise ValueError("All BCM GPIO20–27 must already be configured")
collisions = set(pack) & (set(config.movements) |
                          set(config.movement_robot_types) |
                          set(config.builtin_movement_hashes))
if collisions:
    raise ValueError("Existing names require manual review: " + ", ".join(sorted(collisions)))
# Preserve the original raw configuration and unrelated fields.
data.setdefault("movements", {}).update(pack)
data.setdefault("movement_robot_types", {}).update({n: "humanoid" for n in pack})
merged = NinjaConfig.model_validate(data)
for name in pack:
    validate_movement(merged, name, pins)
# Exclusive create: refuses an existing path, including a symlink.
fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "w") as stream:
    json.dump(data, stream, indent=2, allow_nan=False)
    stream.write("\n")
print("Validated preview created; live configuration was not replaced.")
```

Inspect the preview locally before any installation. Mere presence of calibration keys does not prove calibrated pulses, hardware connectivity or clearance. After physical checks, back up the actual core config and `servo.json`, stop the controlling application, deliberately merge/reload the intended runtime file, and confirm the movement names appear for the Humanoid profile. Do not point a running robot at an unreviewed preview. To roll back, restore the backed-up configuration while the application is stopped; this document does not alter the calibration or installer.

### Physical commissioning checklist — all pending

1. **Environment and prerequisites:** identify the actual runtime working directory, core config, driver `servo.json`, selected Humanoid profile, eight channel keys and hardware model. Check display/buzzer/sensor pin conflicts and separate servo power/common ground with power removed. Keep a means of cutting servo power available and support the robot mechanically.
2. **No-motion checks:** extract/parse the 34 definitions, run real schema/profile validation, check name collisions and compare file hashes. Confirm GPIO-to-header wiring and source-to-target mapping, especially LA/RA on 26/27 rather than 24/25. Check application discovery with hardware deliberately controlled; launching a tool is not a no-motion operation.
3. **Neutral and calibration:** establish each joint's measured neutral, pulse range, speed limit and safe travel. The library assumes 0 signed equals source 90 logical; do not command all eight zeroes before confirming that assumption. Verify software clamps against actual mechanical stops without driving into them.
4. **Individual small-angle checks:** with the robot supported, deliberately energize one known joint and test small signed changes such as ±5° around its measured neutral using slow calibrated limits. Record the physical direction, clearance and current draw. Repeat for all eight channels. Confirm shoulders can hold neutral without collision; leave their coordination disabled until their fore/aft signs are recorded.
5. **Pose and interface checks:** use the established Movement Tool or active web session. Confirm the requested name, entry transition, profile filtering and observed final pose. Test abort with a small commissioned movement, accounting for callback checks at step boundaries. Loss of connection is not a substitute for a physical power cutoff.
6. **Progressive multi-joint tests:** begin with commissioned center and small pose changes, then hands/arm gestures with verified clearance, then supported foot/hip combinations. Check left/right correspondence and mirrored mounting. Before full walk/turn, separately verify the ±90° source arm endpoints; before shake and gestures, verify their larger foot tilts. Reduce numerical amplitudes in a separate reviewed test copy if required; do not mistake a clipped motion for source fidelity.
7. **Gait acceptance:** only after supported tests, try a short flat-floor cycle with stable support available. Observe slipping, tipping, binding, supply sag, jitter and unexpected direction. S mode alone does not guarantee balance or safety. Measure actual period/travel and document differences from Otto rather than claiming timing equivalence.
8. **Unsupported behavior:** confirm no MAGIC/WAVE-animation/FAIL entry is advertised from this pack and that adding unsupported step keys is rejected before output. Do not simulate collapse, detach, dwell or audio with fabricated fields. Confirm no Spider Poweroff was added or executed on the Humanoid.
9. **Record and rollback:** log robot geometry, calibration version, movement name, changed angles, observed direction, current/power issues, abort result and pass/fail for each movement. Stop on interference, unstable posture or mapping mismatch. Restore the configuration backup while stopped if acceptance fails; retain the findings for a corrected port.

### Evidence and provenance

The reference wiki pages [motion system and easing](../ninjarobot_pi0_Wiki/wiki/concepts/motion-system-and-easing.md), [pi0servo](../ninjarobot_pi0_Wiki/wiki/entities/pi0servo.md), [installation and wiring](../ninjarobot_pi0_Wiki/wiki/references/installation-and-wiring.md), and [hardware calibration/tools](../ninjarobot_pi0_Wiki/wiki/references/hardware-calibration-and-tools.md) were retrieved as draft/unverified pages with recorded AI semantic reviews. Such reviews do not constitute human or hardware verification. Older motion text concerning ignored unknown pins or cancellation is superseded by current whole-sequence preflight code; the wiring conflict is recorded in Section 2.

Current manual sources used: InstallationGuide `src-20261010-installationguide-3`; DevelopmentGuide `src-20261011-developmentguide-4`. Code determines actual load, preflight and execution behavior. No new calibration values or physical rotation signs were established by this work.

The hashes below record the initial research revision, preceding the catalog integration; they are historical provenance. Current integration paths and validation are recorded in the linked implementation report.

| Evidence file | Initial research SHA-256 |
|---|---|
| `RoboticsRepoReference/OttoDIYPython-master/otto9.py` | `1dacad402b2132017b2fbe2e87f5d66284fffb35230d8a3b85b97bc1372be5b8` |
| `RoboticsRepoReference/OttoDIYPython-master/oscillator.py` | `3fff5034c1c9d4d8bc8aae8394e552c0a50392a7bc86206a39637e2fd267bf6f` |
| `RoboticsRepoReference/OttoDIYPython-master/OttoHumanoidMovementIntro.md` | `d7e82ba6fb08f7e45cf3e6fa30f72d1aa1266a15d9e724fadc09a9176e2d4711` |
| `NinjaRobotPi0/ninja_core/src/ninja_core/movement_controller.py` | `d93035731b1c0292a8a9cc8d23e5d9ab3d8a9a327268699fcce6e93669ada623` |
| `NinjaRobotPi0/ninja_core/src/ninja_core/builtin_movements.py` | `bf02235bfc444ded71b6c4f3efea41a9d1e714bc1b2b14268c1b5d23609b30ab` |

Canonical library fingerprint (inner `movements` object, sorted JSON keys, compact separators): `49f6c4fe998b3c8500347f56eeeb7e165fb442c206ac373485310af7d280d2d6`.
