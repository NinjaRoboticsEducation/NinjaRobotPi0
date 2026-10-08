# NinjaRobotPi0 knowledge workflow

Read [parent policy](../../AGENTS.md) and [current manual map](../project-knowledge.json).

From the robot root:

```bash
python3 scripts/wiki.py setup
python3 scripts/wiki.py prepare
python3 scripts/wiki.py search "installation"
python3 scripts/wiki.py check
python3 scripts/wiki.py lint --strict
python3 scripts/wiki.py link check
python3 scripts/wiki.py index check
python3 scripts/wiki.py stats
```

Only setup installs dependencies. Prepare verifies unchanged source hashes, takes the wiki
writer lock, stages normalization, and publishes ignored text evidence without refreshing
tracked catalog fingerprints. Queries/checks use the existing interpreter without uv sync.
From the wiki directory use `python3 ../scripts/wiki.py`; arbitrary CWD is supported too.

For a change: inspect code and current cited pages, record documentation impact, create a
new dated complete manual/evidence version, register and normalize it explicitly, and prepare
a schema-v2 semantic plan. Validate and display its exact diff before approved apply. Record
an honest new review for each changed sourced page. Preserve reviews on unchanged pages.
Update current pointers and implementation classifications after review, then run all gates.
Never overwrite raw originals or blindly refresh fingerprints. Legacy overwrite-sync is retired.

Root AGENT/CLAUDE/GEMINI, root `.agents/skills`, Claude wrappers and Cursor rules delegate to
shared policy. The nested wiki retains canonical wiki-* skills for wiki-only workspaces.
Static adapter validation is not a claim of editor activation. A wiki-only workspace without
parent access cannot verify current robot code; report that limitation.

Recover through the wiki transaction backup tools and Git review; preserve later user edits.
A source-hash mismatch requires investigation, not force-normalization or catalog rewriting.
Generated caches/environments are ignored and must be explicitly rebuilt in a fresh checkout.
