# NinjaRobotPi0 local knowledge

Read [the parent policy](../AGENTS.md) and [project workflow](docs/PROJECT_WORKFLOW.md).
Current full manuals:

- [InstallationGuide.md](raw/articles/ninjarobotpi0/2026-10-10-model-adapter/InstallationGuide.md)
- [DevelopmentGuide.md](raw/articles/ninjarobotpi0/2026-10-10-model-adapter/DevelopmentGuide.md)
- [DevelopmentLog.md](raw/notes/ninjarobotpi0/2026-10-10-model-adapter/DevelopmentLog.md)

The [knowledge map](project-knowledge.json) resolves active source versions and reviewed code.
Curated pages begin at [overview](wiki/overview.md). Registered raw originals are immutable.
This folder remains embedded in the robot Git repository; do not initialize another Git repository.

```bash
python3 ../scripts/wiki.py setup
python3 ../scripts/wiki.py prepare
python3 ../scripts/wiki.py search "installation"
python3 ../scripts/wiki.py check
python3 ../scripts/wiki.py lint --strict
```

Setup explicitly installs the independent locked wiki environment. Preparation reconstructs
ignored text evidence without changing tracked fingerprints. Queries/checks are read-only.
Semantic review, lifecycle, trust and physical verification are separate. Report limitations.

## Intake and quality gates

Keep this embedded directory in the robot Git repository before the first ingestion.
Put immutable articles in `raw/articles/`, papers in `raw/papers/`, evidence notes in
`raw/notes/`, and media in `raw/media/`. Discover files that are not registered yet with
`python3 ../scripts/wiki.py lint` (look for `unregistered-source`); explicitly register and normalize selected
sources using the `wiki-ingest` skill. Do not replace registered originals.

Images (`.png`, `.jpg`, `.jpeg`) require a sanitized rendition before publication;
Tesseract OCR is optional evidence, not visual verification. Review text and image
claims against their actual source rather than trusting extraction alone.

Canonical skills are `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-review`, and
`wiki-maintain`. Use `llmwiki review prepare` through the launcher for source-grounded
page review, and `llmwiki lint --strict` for the release quality gate. Inspect the
exact plan diff before application. Batch ingestion must preserve every source's
identity, hash, provenance, review state and limitations.
