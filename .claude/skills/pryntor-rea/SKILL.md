---
name: pryntor-rea
description: Optional lawful reverse-engineering and read-only software structure analysis for Pryntor-owned or expressly authorised targets, using Pryntor's evidence-gated REA protocol.
---

# Pryntor REA — opt-in shared company skill (Codex and Claude)

Use this only when software source alone is insufficient and the exact target is owned by Pryntor or has explicit documented permission. Prefer normal source inspection for ordinary complete repositories.

**Authoritative policy:** https://github.com/LLoliwe/Anthropic-skills/blob/main/skills/pryntor-rea-company/SKILL.md

**Free working lab:** https://pryntor-rea-sandbox.onrender.com/readyz — this is a public READ-ONLY STATUS endpoint for internal fixture analysis. The 207 REA MCP tools are NOT available over public HTTP. Never send arbitrary inputs or customer files to this endpoint. The lab can sleep; HTTP 503 while warming up is normal.

**Source:** morluto/rea (MIT for REA code; inspect each target/provider licence). Node >=22.19 or >=24.11. Use `rea-agents@6.5.0` pinned with audited lock/integrity hashes where actually installed.

## Evidence and permission gate

1. Record target owner, licence, permission, issue identifier, target hash and isolated scope.
2. Never ingest customer secrets, traveller/learner information, private firmware or protected third-party artifacts without explicit authorisation, retention policy and necessary permissions.
3. Prefer offline static analysis of disposable owned software. Do not perform device actuation, interception, authentication circumvention, DRM bypass or production changes.
4. For agent-host installation, inspect the intended host and MCP config, run `npx -y rea-agents@6.5.0 doctor --client codex --json` and `setup --client codex --dry-run --json`; require authorised reviewer before actual persistent config changes. Do not mutate company hosts merely because this skill is present.
5. After any host install, restart the real agent client, verify `initialize`, `tools/list`, a lawful `tools/call` fixture analysis, rollback and audit trail.
6. Keep observations, interpretations and unknowns distinct. Never claim independent security signoff or real physical-control proof from these installation checks.

**Status:** This checked-in skill is an *agent skill registration*, not a demonstrated permanent installation on every machine. Hosted CI proves real MCP on an ephemeral independent GitHub runner only. The public product https://pryntor-inspect.onrender.com is a browser-local heuristic quick scan, **not** full REA deep analysis or certified security review.

**AC control:** NOT APPLICABLE: founder does not own an AC. Do not buy one for the skill.

**Issues:** https://linear.app/pryntor/issue/PRY-232 ; https://linear.app/pryntor/issue/PRY-229 (optional Home R&D).

## Invocation

Use the official REA operating overlay and vetted binaries, not remote snippets copied blindly into trusted shells. Verify the pin, source and permissions for each host. Use project-local disposable fixtures for proof. Reject privilege escalation and any paid integration not separately approved.
