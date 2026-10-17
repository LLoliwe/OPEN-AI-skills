# AIE research R0 — dated technical acceptance (2026-10-17)

Issue: https://linear.app/pryntor/issue/PRY-224

## Independent live SOURCE validation
- Remote network-capable read-only session fetched `https://ai.engineer/api/data/talks?format=json`.
- HTTP 200, Content-Type `application/json; charset=utf-8`, response bytes **2,197,312**, SHA-256 `55399dc2200ffc7f921f7cd2f13520e550b1f5e9bae8df43487d754ac503436c`.
- Parsed JSON array of **1,338** talk records, all 1,338 URLs start with `https://ai.engineer/talks/`, 1,338 distinct slugs. Snapshot-specific; counts can change.
- No consumer credentials, personal data, restricted data or paid service used.

## Live MCP (NOT installed into Pryntor production agents)
- JSON-RPC `initialize` POST to `https://ai.engineer/mcp`: HTTP 200 `text/event-stream`; server `ai-engineer` v1.0.0 negotiated protocol 2025-06-18.
- `tools/list`: code_2026_get_application, code_2026_validate_application, code_2026_submit_application, search, fetch, list_conferences, get_schedule.
- `list_conferences` and `search` each returned live structured data. `fetch` with id `talk:youtube-54ffb168fa695befeaa3` and section transcript returned 2 of 11 timestamped transcript passages, proper source citations, automatic-transcription caveat, contentVersion.
- All operations strictly read-only. No applicant application requested, validated, submitted or paid ticket purchased.
- Search results can report transcript-wide search unavailable even when known-talk `fetch(section=transcript)` works; distinguish capabilities.
- Rate and availability status can change; user agents must use the official live schema.

## Offline preflight
- Python 3.13.5 local run from authored source: original `test_catalog.py` 12/12 passed, independent separately authored adversarial `test_independent.py` 12/12 passed; `python -m unittest discover -v -p 'test_*.py'` **24/24 passed**.
- Original source SHA-256: catalog `fe2f218a849b4016aa7a9dc289b5ed389fde285a04cffd2890e68e8f13dab492`, original tests `5bc80150c276211714a981b2a576990b31b3f0262e9841be37f69a9ceb22c92f`; independent suite `ebf78950e71aa7fb524b22400831712f681a432360de52e003542c82cfef1484` (compare committed byte content before asserting exact match).
- Hosted CI run for preceding head: https://github.com/LLoliwe/OPEN-AI-skills/actions/runs/39013364791 passed. **New head must independently pass CI**; do not borrow prior-head status.

## Acceptance scope and holds
- Research skill and public source triage only; NOT production agent/runtime installation, scientific validation, speaker admission, commercial dataset licence or venture production.
- Quality and licensing: third-party public talks remain attributed, automated transcripts may be imperfect. No copying restricted dataset.
- Commercial impact: prepare Recover billing sandbox failure-mode matrix; actual product source, external webhook/sandbox, human finance/security review and independent regression evidence needed before claiming first venture pilot or cash impact.
- Manual expert review and future permissioned agent deployment remain separate company gates.
