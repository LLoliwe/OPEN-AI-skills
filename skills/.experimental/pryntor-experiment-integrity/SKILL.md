---
name: pryntor-experiment-integrity
description: Offline, evidence-first protocol to audit AI research experiment manifests and prevent selective reporting before human verification.
---

# Pryntor experiment integrity, v0.1

Use when an agent proposes a research improvement for any Pryntor venture. The same experimenter MUST NOT award their own scientific, safety or release approval. This is an **original Pryntor skill** informed by David Owen's Epoch AI InnovationEval (2026-10-07): https://epoch.ai/publications/innovationeval. It is not Epoch's code or benchmark.

## Workflow
1. Freeze the actual hypothesis, prior-art search, experiment scope, selected metric and metric direction, comparison baseline, fixed holdout, run IDs/seeds, allowed budget and termination condition **before** experimentation. Timestamp and SHA256 the preregistration in company records. A declared ID alone does not prove immutability.
2. Separate exploratory tuning from sealed evaluation. Do not train/tune on a held-out set or reveal private learner/client data to external AI providers. Require POPIA/permission review.
3. Implement and execute with the smallest sanctioned R0 local/synthetic resources. No paid GPU/API and no automatic cloud billing.
4. Save **every** experiment attempt, including failures, with configuration, logs, model/tool versions, wall time, costs and SHA256 hashes. Do not claim the best of repeated seeds as the expected performance.
5. Supply a manifest JSON with the fields expected by `audit.py`. From this directory: `python audit.py path/to/manifest.json`; tests: `python -m unittest -v test_audit.py`.
6. Independent reviewer compares logs, source and frozen preregistration and replays on previously unseen cases. The script's AUDIT_READY output means structural consistency only, **not** proof that the data, reviewers, novelty or outcomes are genuine.
7. Preserve negative results. Escalate failure cases, estimated effect with uncertainty, scope violations, conflicts and safe rollback in the canonical Linear issue. Do not mark product GO until domain-specific gates pass.

## Initially selected pilot
Show Your Working: recovered historical Proof Studio, independently written and educator-adjudicated method-marking holdout. Compare baseline vs candidate at fixed seeds and cases. Critical false-credit defects are a veto. Existing R5 risks and missing evaluator approval are still blockers. Do not manufacture a new private student sample; use synthetic or expressly authorized data.

Then: Intelligence Engine 16/20 synthetic decision baseline with urgent/opt-out false negatives; Robotics 10ms latency holdouts in simulation; Studios shot-level continuity/provenance checks on real footage.

## Non-goals and constraints
No autonomous science or novelty claim. No real-time autonomous worker, production release, external outreach, wallet, billing or confidential-data transfer. Independent reviewer identity and logs cannot be authenticated by this static script; verify in a separate authorized record. Respect company PRY-98, PRY-156, PRY-86, PRY-199 and R0 policy.
