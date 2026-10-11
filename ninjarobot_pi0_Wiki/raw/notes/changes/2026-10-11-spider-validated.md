# Owner-validated Spider catalog replacement

Actor: agent:codex. Date: 2026-10-11. User explicitly requested replacement from DevelopmentPlanDoc/spider_movement.json.


## 2026-10-11: owner-validated Spider movement replacement

The installed `ninja_core/src/ninja_core/data/spider_otto.json` now contains the exact 20 movements and 566 steps supplied in `DevelopmentPlanDoc/spider_movement.json`. The supplied file is a movements-key fragment; the installed resource adds only the surrounding JSON object and robot_type=spider. Six run/walk/turn definitions change, and spider_moonwalk_left becomes spider_moonwalk_right. Poweroff remains exact. No Wave_Left_Hand movement was added.

The native loader/reconciliation and movement controller are unchanged. Normal Spider config loading/import replaces unchanged managed definitions, removes the unchanged managed old moonwalk name and seeds the new name. User-edited/custom definitions are preserved, so a same-name local edit may retain its old value. No live config, calibration or hardware was modified by this task. The original repository OTTO research pack and generator remain unchanged as historical evidence; they do not regenerate the installed validated pack.

SpiderBuildinMovements.md now includes all current JSON sequences, corrected direction provenance and the current installed resource path. Host validation passed 146 targeted tests covering native movements, original research data, config and lifecycle refinements, including every current movement with inert output and managed-catalog upgrades. Ruff and protected-core checks passed. The owner reports movement validation; no new physical qualification or Pi execution was performed here. Runtime period/dwell semantics remain unchanged.

Rollback: revert the installed data and corresponding document/test changes, then reload the installed package through the normal workflow. Reconciliation updates only unchanged managed values; retain/restorе user changes from a reviewed backup when needed. No automatic rollback or robot action was performed.

The source fragment was parsed with duplicate-key rejection. Runtime catalog and all inline JSON blocks equal its movement object. Original OTTO source data remain historical; direction labels in the validated catalog reflect the owner's selected movement mapping. No unsupported duration/period fields were added. The existing resource loader still normalizes the older prefix when present and adds the same Poweroff constant; this supplied catalog already uses final names and the identical Poweroff.
