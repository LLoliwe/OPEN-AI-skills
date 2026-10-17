#!/usr/bin/env python3
"""Pryntor R0 offline discovery tool for public ICLR-submission metadata.

NOT a paper evaluator, live API harvester, citation ranker, or production agent.
Only consumes an explicitly provided LOCAL copy of upstream tabular data.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ALLOWED_STATUSES = ("active", "withdrawn", "desk_rejected")
VEN = {
    "agents": ("agent", "reasoning", "retrieval", "tool use", "planning", "llm", "evaluation"),
    "education": ("math", "reasoning", "education", "grading", "feedback", "proof", "assessment"),
    "robotics": ("robot", "locomotion", "control", "sim-to-real", "sim2real", "reinforcement learning", "world model"),
    "studios": ("video", "audio", "motion", "diffusion", "3d", "image generation", "temporal consistency"),
    "security": ("prompt injection", "adversarial", "privacy", "jailbreak", "safety", "trustworthy"),
    "revenue": ("inference", "efficiency", "cost", "quantization", "compression", "benchmark", "optimization"),
}
ID = re.compile(r"^[A-Za-z0-9_-]{4,80}$")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate(meta, rows):
    """Fail closed on malformed third-party data, IDs, status totals or tag indices."""
    if not isinstance(meta, dict) or not isinstance(rows, list):
        raise ValueError("meta object and rows array required")
    statuses, areas, tags = meta.get("statuses"), meta.get("areas"), meta.get("tags")
    if statuses != list(ALLOWED_STATUSES) or not isinstance(areas, list) or not areas or not isinstance(tags, list):
        raise ValueError("unrecognized status/area/tag schema")
    if any(not isinstance(x, str) for x in areas):
        raise ValueError("invalid area")
    declared = meta.get("total")
    if type(declared) is not int or declared != len(rows):
        raise ValueError("declared total mismatch")
    counts, ids = Counter(), set()
    for idx, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 7:
            raise ValueError(f"row {idx}: expected seven fields")
        rid, number, title, keywords, area, status, tag_indices = row
        if not isinstance(rid, str) or not ID.fullmatch(rid) or rid in ids:
            raise ValueError(f"row {idx}: unsafe or duplicate note ID")
        ids.add(rid)
        if type(number) is not int or number < 0 or not isinstance(title, str) or not title.strip():
            raise ValueError(f"row {idx}: invalid paper metadata")
        if not isinstance(keywords, str) or type(area) is not int or not 0 <= area < len(areas):
            raise ValueError(f"row {idx}: invalid keywords or area")
        if type(status) is not int or not 0 <= status < len(statuses):
            raise ValueError(f"row {idx}: invalid status")
        if not isinstance(tag_indices, list) or any(type(t) is not int or not 0 <= t < len(tags) for t in tag_indices):
            raise ValueError(f"row {idx}: invalid tag index")
        counts[statuses[status]] += 1
    reported = meta.get("statusCounts")
    if not isinstance(reported, dict) or any(type(reported.get(s)) is not int or reported[s] != counts[s] for s in statuses):
        raise ValueError("status partition mismatch")
    return dict(total=len(rows), statusCounts=dict(counts), uniqueIds=len(ids))


def select(meta, rows, venture, limit=5):
    if venture not in VEN or type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("venture or limit invalid")
    terms = VEN[venture]
    scored = []
    for row in rows:
        rid, number, title, keywords, area, status, tag_indices = row
        if meta["statuses"][status] != "active":
            continue
        tag_text = " ".join(str(meta["tags"][t].get("en", "")) for t in tag_indices)
        title_l, keys_l, tag_l = title.lower(), keywords.lower(), tag_text.lower()
        # Mechanical heuristics for discovery ONLY, never paper quality or fit validation.
        def matches(term, body):
            return bool(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", body))

        score = sum(4 * matches(term, title_l) + 2 * matches(term, keys_l) + matches(term, tag_l) for term in terms)
        if score:
            scored.append((score, number, rid, title))
    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [{"note_id": rid, "title": title, "score": score,
             "openreview": "https://openreview.net/forum?id=" + rid,
             "status": "active", "screening_only": True}
            for score, _, rid, title in scored[:limit]]


def build(meta, rows, meta_path, rows_path, venture="all", limit=5):
    validation = validate(meta, rows)
    names = list(VEN) if venture == "all" else [venture]
    if any(v not in VEN for v in names):
        raise ValueError("unknown venture")
    return {"gate": "R0_DISCOVERY_ONLY_NOT_RESEARCH_VALIDATION",
            "provenance": {"origin": "yzc-666/iclr2027-explorer third-party OpenReview-derived snapshot",
                           "snapshot_built": meta.get("built"), "upstream_version_claim": meta.get("version"),
                           "meta_sha256": sha256_file(meta_path), "rows_sha256": sha256_file(rows_path)},
            "validation": validation, "shortlists": {name: select(meta, rows, name, limit) for name in names},
            "limitations": ["Offline structural validation of third-party metadata only",
                            "No official API sample reconciliation or paper reading",
                            "No citation extraction, independent grading or licence determination",
                            "No production agent installation, claims of acceptance or model inference"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meta", type=Path, required=True, help="local docs/data/meta.json")
    parser.add_argument("--papers", type=Path, required=True, help="local docs/data/papers.json")
    parser.add_argument("--venture", choices=["all", *VEN], default="all")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--out", type=Path, help="optional JSON report; never writes full paper text")
    args = parser.parse_args()
    meta = json.loads(args.meta.read_text(encoding="utf-8"))
    rows = json.loads(args.papers.read_text(encoding="utf-8"))
    result = build(meta, rows, args.meta, args.papers, args.venture, args.limit)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
