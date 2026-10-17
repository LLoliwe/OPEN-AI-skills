import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("gate", pathlib.Path(__file__).with_name("gate.py"))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def fixture():
    row = {"seed": 0, "baseline_ms": 200, "candidate_ms": 100, "baseline_quality": 30,
           "candidate_quality": 30, "hardware": "NVIDIA H100 80GB", "batch_size": 1,
           "max_output_tokens": 128, "input_digest": "a" * 64, "log_sha256": "b" * 64}
    return {"schema": "pryntor-ncm-r0-v1", "task": "xsum", "metric": "rouge_l",
            "upstream_commit": "a" * 40, "checkpoint_commit": "b" * 40,
            "dataset_commit": "c" * 40, "preregistration_sha256": "d" * 64,
            "quality_tolerance": 0.0, "min_speedup": 1.1, "expected_seeds": 3,
            "new_spend_usd": 0, "data_classification": "public_or_synthetic",
            "deployment_enabled": False, "independent_review_completed": False,
            "runs": [{**row, "seed": seed} for seed in range(3)]}


class NcmGateTests(unittest.TestCase):
    def blocked(self, f):
        self.assertEqual(gate.check(f)["status"], "BLOCKED")

    def test_structural_only(self):
        report = gate.check(fixture())
        self.assertEqual(report["status"], "STRUCTURALLY_ELIGIBLE_FOR_HUMAN_REVIEW")
        self.assertIn("NOT_A_REAL_BENCHMARK", report["scope"])
        self.assertEqual(report["speedup"], 2)

    def test_omitted_seeds(self):
        f = fixture(); f["runs"].pop(); self.blocked(f)

    def test_no_data(self):
        f = fixture(); f["runs"] = []; self.blocked(f)

    def test_duplicate_seed(self):
        f = fixture(); f["runs"][1]["seed"] = 0; self.blocked(f)

    def test_private_data(self):
        f = fixture(); f["data_classification"] = "student_private"; self.blocked(f)

    def test_paid_gpu(self):
        f = fixture(); f["new_spend_usd"] = 0.01; self.blocked(f)

    def test_bool_cost(self):
        f = fixture(); f["new_spend_usd"] = False; self.blocked(f)

    def test_deploy(self):
        f = fixture(); f["deployment_enabled"] = True; self.blocked(f)

    def test_self_review(self):
        f = fixture(); f["independent_review_completed"] = True; self.blocked(f)

    def test_unpinned(self):
        f = fixture(); f["checkpoint_commit"] = "main"; self.blocked(f)

    def test_hardware_mismatch(self):
        f = fixture(); f["runs"][0]["hardware"] = "CPU"; self.blocked(f)

    def test_batch_mismatch(self):
        f = fixture(); f["runs"][0]["batch_size"] = 2; self.blocked(f)

    def test_dataset_mismatch(self):
        f = fixture(); f["runs"][0]["input_digest"] = "f" * 64; self.blocked(f)

    def test_quality_regression(self):
        f = fixture(); f["runs"][0]["candidate_quality"] = 18; self.blocked(f)

    def test_speed_regression(self):
        f = fixture(); f["runs"][0]["candidate_ms"] = 500; self.blocked(f)

    def test_nan(self):
        f = fixture(); f["runs"][0]["candidate_ms"] = float("nan"); self.blocked(f)

    def test_hostile_types(self):
        f = fixture(); f["runs"][0]["seed"] = []; self.blocked(f)
        f = fixture(); f["runs"][0]["hardware"] = []; self.blocked(f)

    def test_sudoku_bounds(self):
        f = fixture(); f["task"] = "sudoku-hard"; f["metric"] = "solved_rate"
        f["runs"][0]["candidate_quality"] = 101; self.blocked(f)

    def test_lower_better(self):
        f = fixture(); f["metric"] = "gen_ppl"
        for row in f["runs"]:
            row["candidate_quality"] = 29
        self.assertEqual(gate.check(f)["status"], "STRUCTURALLY_ELIGIBLE_FOR_HUMAN_REVIEW")

    def test_non_object(self):
        self.blocked([])


if __name__ == "__main__":
    unittest.main()
