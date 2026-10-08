---
name: robot-wiki-query
description: Retrieves traceable NinjaRobotPi0 architecture, hardware, API, protocol, deployment, and troubleshooting evidence from the local NinjaRobotPi0 wiki before development decisions. Use for substantial NinjaRobotPi0 planning, diagnosis, implementation, or review; keep retrieval read-only.
---

# NinjaRobot Wiki Query

Resolve the robot root from the skill location. Read `AGENTS.md`, the wiki README,
`project-knowledge.json`, and relevant current pages/manual versions. Use
`python3 scripts/wiki.py search "topic"`, `source status`, and `check`.
From the wiki root use `python3 ../scripts/wiki.py`.
Queries never setup dependencies, normalize sources, write knowledge, or operate hardware.
If the environment is missing, read sources directly and report that CLI retrieval was unavailable.
Inspect lifecycle, trust, source hashes and semantic review; compare important behavior with
Serena/code/tests. Cite pages/source IDs and report stale, incomplete or conflicting evidence.
A passing semantic review is not human verification or physical-device acceptance.
