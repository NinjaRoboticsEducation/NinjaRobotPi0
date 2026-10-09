# Spider OTTO implementation and movement contract evidence

Date: 2026-10-09. Actor: agent:codex. Owner-approved Pi0-only additive implementation.


## 2026-10-09: opt-in Spider OTTO waypoint library

The repository now contains `ninja_core/movements/spider_otto.json`, generated offline by `scripts/build_spider_movements.py`. Nineteen named entries cover sixteen OTTO movement functions plus selected directional variants; 565 steps use only the existing `moves` and `speed` fields. Existing `per_servo_speeds` remains supported by the unchanged controller and is tested separately. Source-ID-to-BCM mapping is S0→25, S1→24, S2→27, S3→26, S4→21, S5→20, S6→23, S7→22. The owner-supplied nominal conversion is q−90; Pi0 mounting direction remains unverified. No source S2 reversal or EEPROM trim is inferred for Pi0.

See `DevelopmentPlanDoc/SpiderBuildinMovements.md` for current schema examples, all movements, import-preview instructions and fidelity limits. The pack is a repository asset, not automatically loaded or installed as package data. It does not replace the live config or supply calibration. Existing movement functions, driver code, APIs, calibration and OTTO reference sources are unchanged.

Current movement steps use velocity-derived independent durations, wait for the slowest servo and choose easing by step position. They do not implement explicit pauses, exact periods or shared-time oscillator phases. Source jump/scared waits are omitted; hello is a documented partial adaptation of buggy state-dependent helpers. Unknown GPIO targets are silently omitted by the existing controller, and abort_check is not polled/forwarded; the pack does not improve cancellation guarantees.

`DevelopmentPlanDoc/Pi0BuildinMovementsRefinement.md` is a future-design reference only. It proposes a separate versioned registry/controller with timed poses, cancellable dwells, analytic oscillators, strict limits, shared monotonic time and exclusive output ownership. It does not add current fields or endpoints.

Host validation: 71 targeted pytest cases passed (Spider pack, config and API wrappers); Ruff checks/formatting passed for the two new Python files; generator --check and protected-core verification passed. No installation, physical robot execution or dynamics simulation occurred. Measured mapping/orientation, clearance, power, timing, balance and stop behavior remain pending owner-controlled Pi validation.

日本語: 19 個の動作定義を任意で読み込む JSON として追加しました。既存の動作制御関数は変更していません。元の周期・待機時間は再現しません。別の時間制御器は将来の提案のみで、実機検証は未実施です。

繁體中文：新增 19 個可選用的 JSON 動作定義，未修改既有動作控制函式。現有執行器不保留原始週期與停頓。獨立時間控制器僅為未來提案，尚未進行實機驗證。

简体中文：新增 19 个可选用的 JSON 动作定义，未修改现有动作控制函数。现有执行器不保留原始周期与停顿。独立时间控制器仅为未来提案，尚未进行实机验证。

The detailed two design documents are English; these summaries preserve the implementation boundary but are not full translations.

### Exact movement field and timing evidence

`ninja_core/src/ninja_core/movement_controller.py`: execute_movement converts JSON GPIO keys to integers, reads required moves/speed and optional per_servo_speeds. move_servos orders by driver pins; missing target is None; unknown pins never enter the list. Per-pin mode overrides the global mode. Calls move_all_sync(force=True) with easing single=in/out cubic, first=in cubic, middle=linear, last=out cubic. abort_check is not polled or passed to driver. A false completion with callback present automatically centers and raises EmergencyStop; without callback execution can advance.

`pi0servo/src/pi0servo/core/multi_servos.py`: shared elapsed monotonic loop with individual durations; waits for the longest. STEP_INTERVAL=.01s; timing is not a hard real-time guarantee. Starting a move clears driver abort events. Last angle/pulse estimate/center are command-state fallbacks, not encoder feedback. `motion/calculator.py` uses 600*(speed_percent/100)*{F:1,M:.75,S:.5}; duration=distance/velocity or zero for nonpositive velocity. The constant is an assumed motor spec. Cubic easing can peak at 3 times average velocity; these settings do not guarantee torque, protection, or velocity continuity.

`config.py`: movements is Dict[str,list], without deep step validation. `hal.py`: pins from core config but driver calibration read separately from servo.json. Driver absent calibration may use flat 1500/1500/1500; validated data bounds are not physical clearance. Servo.set_angle clamps pulse conversion but records requested angle. runtime_pipeline coordinates native/Blockly mode but is not universal servo ownership. Proposed scheduler must own cancellation and integrate exclusive writers.

### Source translation audit

Original OTTOKame.cpp uses signed sine amplitudes, offsets and phases. All 14 oscillator variants were compared to source arrays: run 0/1, turnL/R, dance, frontBack, upDown, pushUp, waveHAND, moonwalkL, omniWalk true/false factor2 and walk forward/backward. Walk feet have T/2; pause(1) refreshes every oscillator, so no opposite-diagonal hold. Source execute ignores steps and returns with oscillators active. The finite pack samples one cycle using 36 phase intervals (37 endpoint-inclusive poses), rounds to .001 degree, clips source angle to 0..180 then subtracts90 and permutes GPIO. Native M is an explicit target default, not inferred source speed.

Home/hide are single poses. Jump/scared use source three-pose order with unavailable pauses omitted. Hello uses actual zero-trim small helper writes (150ms divisor15, 500ms divisor50), then one 350ms-pattern wave; history, refresh interleaving and timestamp pause bug are not reproduced. Its S1 negative excursion is clipped. Source mounting S2 reversal and trim are not applied without target evidence. Mechanical fidelity is not claimed.

### Proposed design boundary

A separate future schema may support pose duration_ms, dwell duration_ms and analytic joints amplitude_deg/offset_deg/phase_deg/period_ms. These are proposals, not current config fields. Shared monotonic time, skip-stale deadline policy, command-owner cancellation and prevalidation are required. Repeated move_all_sync calls cannot preserve oscillator timing and reset abort flags. Peak oscillator velocity is 2*pi*abs(A)/Tseconds: walk A20,T275ms requires456.96deg/s, exceeding hypothetical M80 ceiling360. Reject or commonly stretch coupled periods; do not slow legs independently. No new controller is implemented.

### Host checks and provenance

71 tests passed on the existing temporary host environment. Tests use actual load_config and MovementController with a shuffled inert servo group; all565 steps, mapping, modes, easing, omissions and special source landmarks checked. Generator --check and Ruff passed. Protected-core check passed. No dependency installation, hardware command, runtime config edit or publication occurred.

- `scripts/build_spider_movements.py`: sha256:77491a278f891742924d7d4bfc247c6f9b1a18ab4e1effbf87c5f594c4be0d4a
- `ninja_core/movements/spider_otto.json`: sha256:6dee31d21fe57df2bf54deb568c10da000bc5e48b9c1f46a4921cf2ecf6bc547
- `tests/test_spider_movements.py`: sha256:80854b7bf60abe60e24ab39bdc625364bed2622754ec88a312e930322b6a1fb3
- `DevelopmentPlanDoc/SpiderBuildinMovements.md`: sha256:f63579266899081141bd3adb91ed74e15a52d78b8a0e1ad5c44bb81ffa46bda9
- `DevelopmentPlanDoc/Pi0BuildinMovementsRefinement.md`: sha256:d7c4dbd924d58e32bbc189b7e7a15ca1ae756cc63d2203d32bd068360e5a0fe8
