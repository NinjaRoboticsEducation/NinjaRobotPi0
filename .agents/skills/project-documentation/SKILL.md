---
name: project-documentation
description: Use when implementation work changes behavior, setup, drivers, architecture, or developer workflow and the NinjaRobotPi0 documentation must be reviewed, fact-checked against the code, and updated before the task is considered complete.
---

# Project Documentation Maintainer

Use `robot-wiki-query` and verify claims against code, tests, CLI exports and actual checks.
Find current InstallationGuide, DevelopmentGuide and DevelopmentLog in the knowledge map.
Copy a complete manual into a NEW dated wiki raw version before editing; retain registered
originals unchanged. Root manual files are short compatibility links, not editing authorities.
README is onboarding/navigation. Package READMEs stay beside packages and require immutable
new evidence snapshots when their documented behavior changes. Historical plans remain history.
Update setup, architecture, API, onboarding, UI/locales and safety sections affected by the task.
Follow AGENTS.md's documentation language policy: future project-authored documentation is
English-only. Only the project-root README.md is multilingual, ordered English, Japanese,
Traditional Chinese, Simplified Chinese. Raw README snapshots retain only English content;
new manual versions retain complete English guidance without translated sections. Preserve
registered originals and historical documents; do not generate translations for wiki raw sources.
Append outcomes and actual validation to a new development-log version, separating host checks
from owner-manual Raspberry Pi checks. Follow robot-wiki-maintain for semantic plans and reviews.
Completion: current pointers/source hashes and implementation mappings agree; knowledge check,
normal/strict lint, links and indexes pass. Do not mark physical testing performed when pending.
