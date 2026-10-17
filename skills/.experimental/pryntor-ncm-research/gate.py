#!/usr/bin/env python3
"""NCM research evidence gate: structural checks, NOT execution or scientific verification."""
import argparse
import json
import math
import re
import statistics
import sys
from pathlib import Path

HEX = re.compile(r"^[0-9a-f]{40}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
TASKS = {"xsum", "wmt14-de-en", "sudoku-easy", "sudoku-medium", "sudoku-hard",
         "tinystories", "lm1b", "openwebtext"}
METRICS = {"rouge_l": "higher", "bleu": "higher", "solved_rate": "higher", "gen_ppl": "lower"}


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check(record):
    errors = []
    if not isinstance(record, dict):
        return {"status": "BLOCKED", "errors": ["input must be a JSON object"]}
    def required(key, predicate, message):
        if not predicate(record.get(key)):
            errors.append(f"{key}: {message}")
    required("schema", lambda v: v == "pryntor-ncm-r0-v1", "unsupported schema")
    for name in ("upstream_commit", "checkpoint_commit", "dataset_commit"):
        required(name, lambda v: isinstance(v, str) and bool(HEX.fullmatch(v)), "40-hex pinned revision required")
    required("preregistration_sha256", lambda v: isinstance(v, str) and bool(SHA.fullmatch(v)), "64-hex digest required")
    required("task", lambda v: isinstance(v, str) and v in TASKS, "unsupported research task")
    required("metric", lambda v: isinstance(v, str) and v in METRICS, "unsupported metric")
    required("quality_tolerance", lambda v: number(v) and 0 <= v <= 1, "0..1 tolerance required")
    required("min_speedup", lambda v: number(v) and 1 <= v <= 100, "predeclared 1..100 threshold required")
    required("expected_seeds", lambda v: type(v) is int and 3 <= v <= 50, "3..50 seeds required")
    required("new_spend_usd", lambda v: number(v) and v == 0, "zero-new-spend rule")
    required("data_classification", lambda v: v == "public_or_synthetic", "private data prohibited")
    required("deployment_enabled", lambda v: v is False, "deployment prohibited")
    required("independent_review_completed", lambda v: v is False, "cannot self-certify review")
    runs = record.get("runs")
    if not isinstance(runs, list) or not runs:
        errors.append("runs: paired evidence missing")
        runs = []
    if type(record.get("expected_seeds")) is int and len(runs) != record["expected_seeds"]:
        errors.append("runs: missing or extra preregistered seeds")
    if len(runs) > 50:
        errors.append("runs: maximum 50")
    seen, valid = set(), []
    for index, row in enumerate(runs[:50]):
        label = f"runs[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: object required")
            continue
        seed = row.get("seed")
        if type(seed) is not int or not 0 <= seed < 2**32 or seed in seen:
            errors.append(f"{label}.seed: unique uint32 required")
        if type(seed) is int:
            seen.add(seed)
        for key in ("baseline_ms", "candidate_ms"):
            if not number(row.get(key)) or row[key] <= 0:
                errors.append(f"{label}.{key}: positive finite number required")
        for key in ("baseline_quality", "candidate_quality"):
            if not number(row.get(key)) or row[key] < 0:
                errors.append(f"{label}.{key}: nonnegative finite number required")
        if record.get("metric") == "solved_rate" and any(
            number(row.get(k)) and not 0 <= row[k] <= 100
            for k in ("baseline_quality", "candidate_quality")
        ):
            errors.append(f"{label}: solved_rate outside 0..100%")
        for key in ("input_digest", "log_sha256"):
            if not isinstance(row.get(key), str) or not SHA.fullmatch(row[key]):
                errors.append(f"{label}.{key}: SHA256 digest required")
        if not isinstance(row.get("hardware"), str) or len(row["hardware"].strip()) < 3:
            errors.append(f"{label}.hardware: shared hardware required")
        for key in ("batch_size", "max_output_tokens"):
            if type(row.get(key)) is not int or row[key] <= 0:
                errors.append(f"{label}.{key}: positive integer required")
        if all(number(row.get(k)) and row[k] > 0 for k in ("baseline_ms", "candidate_ms")) and all(
            number(row.get(k)) for k in ("baseline_quality", "candidate_quality")
        ):
            valid.append(row)
    if runs and all(isinstance(r, dict) for r in runs) and all(
        type(r.get(k)) in (str, int)
        for r in runs for k in ("input_digest", "hardware", "batch_size", "max_output_tokens")
    ):
        for key in ("input_digest", "hardware", "batch_size", "max_output_tokens"):
            if len({r.get(key) for r in runs}) != 1:
                errors.append(f"runs: unmatched {key}")
    report = {"status": "BLOCKED", "errors": errors,
              "scope": "STRUCTURAL_AUDIT_ONLY_NOT_A_REAL_BENCHMARK"}
    if errors or not valid:
        return report
    b_ms = statistics.mean(r["baseline_ms"] for r in valid)
    c_ms = statistics.mean(r["candidate_ms"] for r in valid)
    b_q = statistics.mean(r["baseline_quality"] for r in valid)
    c_q = statistics.mean(r["candidate_quality"] for r in valid)
    speedup = b_ms / c_ms
    tolerance = record["quality_tolerance"]
    quality_ok = (c_q <= b_q + tolerance if METRICS[record["metric"]] == "lower"
                  else c_q >= b_q - tolerance)
    if not quality_ok:
        errors.append("quality: noninferiority threshold failed")
    if speedup < record["min_speedup"]:
        errors.append("latency: preregistered speed threshold failed")
    report.update({"status": "BLOCKED" if errors else "STRUCTURALLY_ELIGIBLE_FOR_HUMAN_REVIEW",
                   "paired_runs": len(valid), "speedup": round(speedup, 6),
                   "mean_baseline_ms": round(b_ms, 6), "mean_candidate_ms": round(c_ms, 6),
                   "mean_baseline_quality": round(b_q, 6),
                   "mean_candidate_quality": round(c_q, 6)})
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="local JSON file; never uploaded")
    path = Path(parser.parse_args(argv).manifest)
    try:
        if path.stat().st_size > 262144:
            raise ValueError("manifest exceeds 256 KiB")
        output = check(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, UnicodeError) as err:
        output = {"status": "BLOCKED", "errors": [f"unreadable manifest: {type(err).__name__}"],
                  "scope": "STRUCTURAL_AUDIT_ONLY"}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["status"] == "STRUCTURALLY_ELIGIBLE_FOR_HUMAN_REVIEW" else 2


if __name__ == "__main__":
    sys.exit(main())
