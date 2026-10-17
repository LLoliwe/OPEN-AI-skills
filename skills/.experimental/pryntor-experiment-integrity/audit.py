"""Offline, dependency-free manifest audit. It does not verify scientific truth."""
import hashlib
import json
import math
import sys
from pathlib import Path


def audit(data, root):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)

    require(bool(data.get('preregistration_id')), 'Missing preregistration ID')
    require(bool(data.get('hypothesis')), 'Missing frozen hypothesis')
    require(bool(data.get('baseline')), 'Missing baseline description')
    require(bool(data.get('metric')), 'Missing metric')
    require(data.get('direction') in ('higher', 'lower'), 'Invalid metric direction')
    require(data.get('evaluation_split') == 'held_out', 'Evaluation must use held-out data')
    require(data.get('data_leakage_review') == 'passed', 'Contamination review not passed')
    require(data.get('scope_review') == 'passed', 'Scope review not passed')
    require(data.get('cost_zar') == 0, 'Pilot must have R0 recorded cost')
    require(bool(data.get('experimenter_id')), 'Missing experimenter identity')
    require(bool(data.get('reviewer_id')) and data.get('reviewer_id') != data.get('experimenter_id'),
            'Independent reviewer missing or same as experimenter')
    expected = data.get('preregistered_run_ids', [])
    runs = data.get('runs', [])
    require(bool(expected) and len(expected) == len(set(expected)), 'Invalid preregistered run IDs')
    actual = [r.get('id') for r in runs]
    require(sorted(map(str, expected)) == sorted(map(str, actual)), 'Missing, extra or duplicate run IDs')
    require(data.get('selection_rule') == 'mean_all_runs', 'Cherry-picking or undeclared selection rule')
    require(bool(data.get('limitations')), 'Missing limitations disclosure')
    vals = []
    for r in runs:
        rid = str(r.get('id'))
        val = r.get('score')
        require(type(val) in (int, float) and math.isfinite(val), f'{rid}: invalid score')
        if type(val) in (int, float) and math.isfinite(val):
            vals.append(val)
        path = r.get('log_path', '')
        digest = r.get('sha256', '')
        p = root / path
        # Enforce relative, within-root files: no traversal and no credentials/remote paths.
        safe = bool(path) and not Path(path).is_absolute() and root.resolve() in p.resolve().parents
        require(safe, f'{rid}: unsafe log path')
        if safe and p.is_file():
            require(hashlib.sha256(p.read_bytes()).hexdigest() == digest, f'{rid}: log checksum mismatch')
        else:
            require(False, f'{rid}: log file absent')
    if vals:
        avg = sum(vals) / len(vals)
        base = data.get('baseline_score')
        if type(base) in (int, float) and math.isfinite(base):
            delta = avg - base if data.get('direction') == 'higher' else base - avg
        else:
            require(False, 'Baseline score missing or invalid')
            delta = None
    else:
        avg = delta = None
    return {'status': 'AUDIT_READY_NOT_SCIENTIFICALLY_VERIFIED' if not errors else 'BLOCKED',
            'issues': errors, 'run_count': len(runs), 'mean_all_runs': avg, 'delta_vs_baseline': delta,
            'note': 'Structural checks only; external replication, novelty, safety, utility and reviewer identity need independent verification.'}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python audit.py MANIFEST.json')
    manifest = Path(sys.argv[1]).resolve()
    print(json.dumps(audit(json.loads(manifest.read_text()), manifest.parent), indent=2))
