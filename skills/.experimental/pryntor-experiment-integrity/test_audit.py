import hashlib
import tempfile
import unittest
from pathlib import Path
from audit import audit


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name)
        self.root.joinpath('run.log').write_text('synthetic run only')
        sha = hashlib.sha256(self.root.joinpath('run.log').read_bytes()).hexdigest()
        self.data = {'preregistration_id': 'PRY-RD-001-v1', 'hypothesis': 'A beats B',
            'baseline': 'manual baseline', 'metric': 'correct cases', 'direction': 'higher',
            'evaluation_split': 'held_out', 'data_leakage_review': 'passed',
            'scope_review': 'passed', 'cost_zar': 0, 'experimenter_id': 'agent-1',
            'reviewer_id': 'reviewer-2', 'preregistered_run_ids': ['seed-1'],
            'selection_rule': 'mean_all_runs', 'limitations': 'synthetic example',
            'baseline_score': 7, 'runs': [{'id':'seed-1','score':8,'log_path':'run.log','sha256':sha}]}

    def tearDown(self): self.t.cleanup()
    def test_valid_structural_manifest(self):
        r = audit(self.data, self.root)
        self.assertEqual(r['status'], 'AUDIT_READY_NOT_SCIENTIFICALLY_VERIFIED')
        self.assertEqual(r['delta_vs_baseline'], 1)
    def test_cherry_pick_blocked(self):
        self.data['selection_rule'] = 'best_of_10'
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_missing_run_blocked(self):
        self.data['preregistered_run_ids'].append('seed-2')
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_same_reviewer_blocked(self):
        self.data['reviewer_id'] = 'agent-1'
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_checksum_blocked(self):
        self.data['runs'][0]['sha256'] = 'bad'
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_path_traversal_blocked(self):
        self.data['runs'][0]['log_path'] = '../secret'
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_paid_run_blocked(self):
        self.data['cost_zar'] = 1
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_contamination_blocked(self):
        self.data['data_leakage_review'] = 'unknown'
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_nan_score_blocked(self):
        self.data['runs'][0]['score'] = float('nan')
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')
    def test_scope_violation_blocked(self):
        self.data['scope_review'] = 'failed'
        self.assertEqual(audit(self.data, self.root)['status'], 'BLOCKED')

if __name__ == '__main__': unittest.main()
