Plan web-refinement-navigation-20261011: Cite immutable link-corrected full log and final README navigation; no feature or validation-claim change.
Risk: low

## write wiki/entities/ninja-webapp.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md
@@ -64,11 +64,15 @@
   resource: urn:llmwiki:source:src-20261011-webrefinementevidence
   title: Web refinement code, design and local validation evidence
   content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
+- id: src-20261011-readme-final
+  resource: urn:llmwiki:source:src-20261011-readme-final
+  title: Web refinement final English README navigation
+  content_hash: sha256:149b9d5500e321b8e8b4bfd8eee4e056ef7eef77e5bca6107a9086860f8d1a8b
 semantic_review:
   version: 1
   performed_by: agent:codex
-  performed_at: '2026-10-11T06:55:00.439279+00:00'
-  target_hash: sha256:d3f86130f3dcaa4d3493a9c76e2ae6d64521465362b3ea2fbd915cea5177e400
+  performed_at: '2026-10-11T07:05:12.227497+00:00'
+  target_hash: sha256:128f5dd795543a2e7078c2dc4d931546a23ac2413b0cd55b9ebe553bbe68eec4
   result: passed
   checks:
     source_support: passed
@@ -83,13 +87,15 @@
     availability and owner-waived browser validation remain limitations.
   - Source fingerprints were checked; unchanged historical evidence retains its prior
     source-grounded review context. AI review is not human verification.
+  - Checked the new complete link-corrected log/README navigation source; feature
+    claims and validation limits are unchanged and earlier raw versions remain immutable.
 ---
 
 # ninja_webapp Package
 
 ## Current interface and contracts
 
-`ninja_webapp` is the existing React 19.2/Vite SPA with four locale bundles (`en`, `ja`, `zh-TW`, `zh-CN`). The owner-requested refinement changes frontend presentation only; backend/driver APIs, robot configuration, session ownership and shutdown confirmation remain unchanged. BLE advertising is distinct from web controller ownership.[^src-20261011-developmentguide] [^src-20261011-readme-current]
+`ninja_webapp` is the existing React 19.2/Vite SPA with four locale bundles (`en`, `ja`, `zh-TW`, `zh-CN`). The owner-requested refinement changes frontend presentation only; backend/driver APIs, robot configuration, session ownership and shutdown confirmation remain unchanged. BLE advertising is distinct from web controller ownership.[^src-20261011-developmentguide] [^src-20261011-readme-current] [^src-20261011-readme-final]
 
 ## Application pages
 
@@ -145,3 +151,5 @@
 [^src-20261011-readme-current]: Web refinement corrected English README (2026-10-11 web refinement).
 
 [^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).
+
+[^src-20261011-readme-final]: Web refinement final English README navigation; current complete source corrects navigation links while preserving earlier versions.

## write wiki/analyses/development-history-and-evolution.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/analyses/development-history-and-evolution.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/analyses/development-history-and-evolution.md
@@ -116,11 +116,15 @@
   resource: urn:llmwiki:source:src-20261011-webrefinementevidence
   title: Web refinement code, design and local validation evidence
   content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
+- id: src-20261011-developmentlog-2
+  resource: urn:llmwiki:source:src-20261011-developmentlog-2
+  title: Web refinement link-corrected current development log
+  content_hash: sha256:4efb54443f0dac7c48f1b8e722574e4e486ed5dd6db6f0074ea7aafe52478061
 semantic_review:
   version: 1
   performed_by: agent:codex
-  performed_at: '2026-10-11T06:55:43.837539+00:00'
-  target_hash: sha256:5195ceb11d6d885bbf2002dd758dab98dcbcd51937ae60eb32893e743c6b3b46
+  performed_at: '2026-10-11T07:05:12.227497+00:00'
+  target_hash: sha256:5a98c223e72e6be6e8bcf382e26431d9f1f3f8fa14a6352755cac5a02d45ae6d
   result: passed
   checks:
     source_support: passed
@@ -135,6 +139,8 @@
     corrected README versioning are explicitly recorded.
   - Source fingerprints were checked; unchanged historical evidence retains its prior
     source-grounded review context. AI review is not human verification.
+  - Checked the new complete link-corrected log/README navigation source; feature
+    claims and validation limits are unchanged and earlier raw versions remain immutable.
 ---
 
 # Development History and Evolution
@@ -274,10 +280,12 @@
 
 ## Home, Movement and Chat presentation refinement — 2026-10-11
 
-The owner-requested frontend refinement combined Home with the menu, split direct native controls into Movement Tool, retained Chat at `/agent`, added the shared floating folded activity drawer and removed Help with a legacy redirect. It adopted the inspected voice active/idle references and added four-language labels/document language without changing robot/runtime/driver behavior or API/power contracts.[^src-20261011-developmentlog] [^src-20261011-webrefinementevidence]
-
-Frontend lint/build, locale/session/stream checks and protected-core verification passed. Browser startup attempts were stopped when the owner waived testing on Pi Lite; no completed browser assertions, implemented-page screenshot review, real microphone or hardware acceptance is claimed. New complete English manual/log versions, corrected English README evidence and current pointers preserve earlier sources.[^src-20261011-developmentlog] [^src-20261011-webrefinementevidence]
+The owner-requested frontend refinement combined Home with the menu, split direct native controls into Movement Tool, retained Chat at `/agent`, added the shared floating folded activity drawer and removed Help with a legacy redirect. It adopted the inspected voice active/idle references and added four-language labels/document language without changing robot/runtime/driver behavior or API/power contracts.[^src-20261011-developmentlog] [^src-20261011-webrefinementevidence] [^src-20261011-developmentlog-2]
+
+Frontend lint/build, locale/session/stream checks and protected-core verification passed. Browser startup attempts were stopped when the owner waived testing on Pi Lite; no completed browser assertions, implemented-page screenshot review, real microphone or hardware acceptance is claimed. New complete English manual/log versions, corrected English README evidence and current pointers preserve earlier sources.[^src-20261011-developmentlog] [^src-20261011-webrefinementevidence] [^src-20261011-developmentlog-2]
 
 [^src-20261011-developmentlog]: Web refinement current development log (2026-10-11 web refinement).
 
 [^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).
+
+[^src-20261011-developmentlog-2]: Web refinement link-corrected current development log; current complete source corrects navigation links while preserving earlier versions.

