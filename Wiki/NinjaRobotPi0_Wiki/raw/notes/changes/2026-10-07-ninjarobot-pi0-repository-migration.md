# NinjaRobotPi0 repository migration — 2026-10-07

## Approved scope

Publish the existing NinjaRobotV5 tracked working snapshot with fresh Git history in https://github.com/NinjaRoboticsEducation/NinjaRobotPi0.git. Rename the local folder to NinjaRobotPi0, use main as the initial branch, and create no release tag. Preserve Python package names, package metadata, lockfiles, robot runtime files, and robot functions. Legacy Git history is retained only in an ignored private local backup. This migration does not resolve historical robot audit findings or certify hardware safety.

## Verified changes

- The original repository origin was Nilcreator/NinjaRobotV5 and its active branch was ninjav5_8_1 at b9d78e3. The destination advertised no branches or tags before migration.
- NinjaRobotPi0 is an independent Git repository; the umbrella .gitignore excludes it and the private rollback backup.
- Website Introduction, Help, and GitHubQuickStart repository links use NinjaRoboticsEducation/NinjaRobotPi0. Manual links use /blob/HEAD/InstallationGuide.md and /blob/HEAD/DevelopmentGuide.md so they follow GitHub's default branch. Clone commands have no branch option. The initial branch is main, but links are not pinned to main.
- All four website locale files use NinjaRobotPi0 for repository-facing copy. Runtime commands remain unchanged.
- Current onboarding and workflow documents use the new path. Development plans retain their audit/decision context with a migration note. Historical development log entries and immutable raw sources retain legacy provenance.
- The embedded robot wiki's project-owned mirrors were originally identical to the legacy HEAD project documents. Reviewed migration edits were synchronized using wiki_source_sync.py and normalized with llmwiki.

## Validation and limitations

- A credential-pattern check of the original 606 tracked snapshot files found no matches. This is a pattern check, not a comprehensive security audit. Legacy commit history is excluded from the new repository.
- Compared 423 non-document robot files against legacy HEAD bytes: no differences. This includes robot code, package metadata, and lockfiles outside the embedded wiki.
- Website npm run lint passed; npm run build passed with the existing large-chunk advisory. The Pi0 page test suite passed all 18 tests after updating default-branch link expectations.
- No Firebase deployment, production-data access, Raspberry Pi execution, or hardware operation occurred. No robot runtime test suite is needed to validate unchanged file bytes.
- Wiki source-version and link validation are performed through schema-v2 plans. Semantic/human review is not claimed; affected pages remain draft/unverified where appropriate.
- Publication and remote-default-branch verification are subsequent gates; this evidence record does not claim they already succeeded.
