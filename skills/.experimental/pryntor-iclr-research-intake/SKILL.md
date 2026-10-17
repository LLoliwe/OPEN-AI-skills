---
name: pryntor-iclr-research-intake
description: Reproducible, offline ICLR 2027 public-submission metadata validation and venture-specific discovery with hard R0 evidence gates.
---

# Pryntor ICLR Research Intake (R0, experimental)

Use this skill only for public, non-sensitive research discovery across Pryntor's relevant ventures. It is NOT an accepted-paper recommender, an AI scientist, a citation ranking reproducer, a PDF ingestion tool or a deployed agent. Prefer reference links, not copied abstracts.

## Sources
- Primary authority: https://openreview.net/group?id=ICLR.cc/2027/Conference
- First public snapshot indexed by this R0 tool: https://github.com/yzc-666/iclr2027-explorer
- Expected upstream format: `docs/data/meta.json` plus `docs/data/papers.json` on upstream branch `cursor/openreview-fetch-scripts`.
- Upstream metadata dated 2026-10-07 reports 43,013 rows: 42,378 active, 216 withdrawn, 419 desk rejected, 17 topic groups and 171 tags. Verify a local copy, timestamps and digests before claiming your own snapshot. Original repository did not expose a licence file in the root at intake; do NOT assume it licenses wholesale republication of code or full articles.
- OpenReview's CC0 metadata declaration does not mean the text of every submitted paper is CC0: https://openreview.net/legal/terms
- Separate Leon (@iamleonli) citation rankings screenshot is an UNREPLICATED claim. Never blend it into this metadata-derived output.

## Local usage
No dependencies beyond Python 3.9+ standard library. No network calls and no inference.

```bash
python3 -m unittest discover -s skills/.experimental/pryntor-iclr-research-intake -p 'test_*.py' -v
python3 skills/.experimental/pryntor-iclr-research-intake/research_index.py \
  --meta /approved/local/snapshot/meta.json \
  --papers /approved/local/snapshot/papers.json \
  --venture all --limit 5 --out /approved/reports/iclr2027-r0.json
```

Only metadata fields are processed: OpenReview note ID, number, title, keywords, area and status indices, tag indices. `validate()` fails on malformed rows, duplicate IDs, mismatched total/status partition, invalid link IDs and tag indices. `select()` applies deterministic lexical rules. Its score is a heuristic **search signal**, not scientific novelty, quality, relevance or deployability. All results are labelled `screening_only`. The output includes local SHA256 digests, declared snapshot version and a banner that prohibits product claims.

## Venture application
- agents / R&D: reasoning, retrieval, agent-tool orchestration, evaluation. Keep PRY-199 experiment-integrity controls.
- education / LVL7 / Show Your Working: teacher-reviewed method marks, first consequential error, mathematical proof and holdouts.
- robotics: latency, control, world models and sim-to-real; no physical safety assertions.
- studios / BTWW / AFTERLIGHT: multimodal video/audio/3D, real-render quality and human review.
- security / fleet agents: prompt injection, privacy and adversarial evaluation.
- revenue / paid-social QA / Tirisano pilots: inference efficiency, credible measured process improvements only. Nontechnical ventures receive curated notes, not unnecessary deployed code.

## Mandatory acceptance gates
1. Record source URL, snapshot extraction date, commit/ref, SHA256 and rights assessment; confirm every external snapshot. No student/client data, private reviews, reviewer identities or restricted PDFs.
2. Reconcile all records against the official API; verify at least 30 sampled OpenReview note pages, status changes and exact field/licence rules. This tool does NOT perform that official reconciliation.
3. Subject shortlisted source papers to independent full-text/methods review, code licence check, available compute-cost check and domain-specific expert approval.
4. Use PRY-199 to preregister baselines and frozen holdout, report every run and real costs, disclose failure modes and get an independent reviewer. No auto-rollout.
5. Enable any company agent or public-facing feature only in a separate reviewed rollout with access, security, rollback and customer data protection confirmed.

## Operating rules
Zero new spend; no automatic public crawling, downloading 43k PDFs, training on anonymous authors, silently uploading research or making novelty/revenue claims. Keep Leseli production gates intact. Include source URLs and uncertain-status notes in every shared output.

## Company records
- https://linear.app/pryntor/issue/PRY-202/randd-002-intake-iclr-2027-public-research-index-and-validate
- https://docs.google.com/document/d/1803QvVqEe1sbAmIqxKtkm53vHYd0sJZ3Y5t8xGZrl4A/edit
- https://app.undermind.ai/projects/5c29e381-c306-4d70-8ff9-624fa5884fd4?path=/ICLR_2027_Pryntor_R0_Research_Intake.md
