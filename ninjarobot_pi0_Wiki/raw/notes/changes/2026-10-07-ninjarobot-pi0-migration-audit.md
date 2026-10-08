# Migration audit corrections — 2026-10-07

The user requested an audit of the completed repository migration and authorized correction of errors. This follow-up evidence supplements the original migration record; it does not overwrite that record.

## Confirmed migration behavior

GitHub advertises main as default branch and only published branch. The new repository has fresh history; the legacy HEAD object is absent. The original tracked file set is present and robot runtime code, package names, versions, metadata, and lockfiles match the legacy snapshot. The private legacy Git backup has owner-only directory permissions and is ignored by the umbrella repository. Local pre-existing Serena edits remain unstaged.

## Findings and corrections

1. Current Markdown had missed spaced product names such as NinjaRobot V5 and some V4 folder references. Corrected current README/manual/package README names and paths, without renaming Python packages or changing literal historical version milestones/runtime identifiers. Corrected current workspace policy, skill examples, Cursor/agent descriptions, and Serena orientation notes. The retained mem:v5/core identifier is a historical key for the current Pi0 map.
2. The migration had relabeled the September audit's original findings and evidence paths as Pi0. Restored the historical audit body from the preserved pre-migration baseline and placed an explicit present-day repository mapping above it. A credential finding about a legacy revision must not be presented as a finding about the new history.
3. Clean-clone wiki lint failed with 13 missing-derived-manifest errors because raw/_derived is intentionally ignored. Added an explicit existing-wiki bootstrap before the generic template instructions in NinjaRobotPi0/Wiki/NinjaRobotPi0_Wiki/README.md. The procedure uses the existing source-list and source-normalize CLI commands; it does not reinitialize the wiki or create a nested Git repository. Tested the exact Python block on an isolated clone: all registered sources normalized and normal lint returned zero errors. Existing dependencies were reused for the test; no installation was performed. New clones must run the documented locked-tooling setup in their own environment.
4. Strengthened the existing website regression check to compare complete official manual URLs and the branch-free clone command. Browser inspection of /ninja-robots/pi0, /ide, and /ide/help confirmed official repository links, blob/HEAD manuals, and no old project name in rendered page text. Links can follow a later GitHub default-branch change as long as the files exist there.

## Boundaries

No robot function, Python runtime source, dependency version, package name, hardware configuration, or protocol was changed. Cursor/agent descriptors are development metadata. Historical V5 version names, package metadata identities, and literal runtime messages are deliberately retained. The website was tested locally; no deployment or hardware operation occurred. Wiki normal lint checks structure/provenance; this audit does not add human verification or certify unrelated technical claims. The original zero-error wiki result was for a prepared checkout, not an uninitialized clean clone.
