# Humanoid movement reference evidence

## Humanoid Otto waypoint reference — 2026-10-12

Created `DevelopmentPlanDoc/HumanoidBuildinMovements.md` as a documentation-only port: 34 complete JSON movement definitions / 1,203 keyframes, covering all 16 public Otto servo-motion methods through 24 variants plus 10 servo-containing gestures. The current native Humanoid catalog remains only `home`; these proposed `humanoid_*` definitions are not installed automatically. Production engine, installed Spider catalog, configuration, calibration and original Otto sources are unchanged.

Source slots YL/YR/RL/RR/LA/RA map to BCM GPIO20/21/22/23/26/27, with signed target = source angle minus 90. Additional fore/aft shoulders GPIO24/25 stay at nominal zero because mounting signs and measured neutral remain unverified. The document records conflicting older display assignments on these GPIOs; the actual eight-channel pin inventory must be checked before enabling hardware.

Fixed poses retain source target order. Oscillators use 36 phase intervals per cycle with endpoints, resetting mathematical phase at each new source oscillator subcall. Every step uses existing moves/speed/per_servo_speeds fields and S mode; no duration, dwell, loop, sound/display or detach fields are invented. Source timing and physical gait equivalence are explicitly not guaranteed. VICTORY intentionally changes source YL9 to90 during its first ramp. MAGIC and WAVE gestures have no servo trajectory; FAIL requires release/collapse/recovery and is omitted.

Host validation: all 34 sequences passed actual NinjaConfig/load/save/preflight and MovementController with an inert driver and stubbed HAL import; 1,203 emitted steps verified mapping, speed and easing. Missing channels rejected in 272 cases and wrong profiles in 68; bad later steps rejected before output; false driver completion stopped advancement. All 36 JSON blocks parse (34 library + two examples), inline library matches the validated pack, local links resolve, and the extraction/merge preview script passed parsing, output parity, collision, missing-input, no-overwrite and 0600 checks. Independent reader review found no actionable issue. No real HAL, GPIO, pigpio, server, device tool or physical robot was started. Hardware acceptance remains pending.

The complete reference contains per-movement source calls/line ranges, source hashes, wiring table/front-view schematic, schema and load/trigger explanations, an offline merge preview, unsupported behavior and a progressive physical commissioning checklist. Source-code evidence and registered current manuals were inspected. Existing global knowledge-map/web fingerprints and missing historical spider_movement.json remain unrelated unresolved drift; they are not refreshed by this task.

## Artifact integrity

Document SHA-256: `0d3ce2bb57e06e832f0b70614e48b65e89902e79eb57b3e25a1f85380231bc9d`.
Canonical movement-object SHA-256: `49f6c4fe998b3c8500347f56eeeb7e165fb442c206ac373485310af7d280d2d6`.

No InstallationGuide or DevelopmentGuide behavior/setup changes are required: this is an opt-in research reference, not a installed feature. The new complete DevelopmentLog version records the deliverable; earlier immutable manuals remain unchanged.
