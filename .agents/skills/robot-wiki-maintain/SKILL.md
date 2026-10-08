---
name: robot-wiki-maintain
description: Keeps the NinjaRobotPi0 local wiki aligned after features, APIs, setup, architecture, hardware guidance, or project documents change. Use to create immutable project-owned source versions, normalize new sources, prepare reviewed wiki plans, and run wiki quality gates; do not use for read-only questions.
---

# NinjaRobot Wiki Maintenance

Full manuals live as immutable dated versions under `ninjarobot_pi0_Wiki/raw/`.
Read the nested AGENTS and matching `wiki-*` skill. Resolve current versions using
`project-knowledge.json`; create a NEW complete dated source rather than overwriting one.
Rebase links, register/normalize new evidence explicitly, and preserve original hashes/history.
Create a schema-v2 plan with current source/target hashes, validate it and show its exact diff.
Apply only when the owner's approval covers that diff/scope; the approved implementation plan
already covers its named page updates. Expanded scope needs new approval.
Review changed sourced pages one by one and report actual checks; never invent human verification.
Update current README/root-pointer links and reviewed implementation mappings.
Run `python3 scripts/wiki.py check`, `lint --strict`, `link check`, `index check`, and `stats`.
Do not blindly refresh fingerprints or old review hashes. Queries have no setup/sync side effects.
Legacy `wiki_source_sync.py --sync` is retired; --check delegates to the new knowledge gate.
Robot functions and hardware are never modified/activated as a wiki-maintenance side effect.
