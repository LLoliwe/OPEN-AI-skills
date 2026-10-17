import copy
import json
import tempfile
import unittest
from pathlib import Path

from research_index import build, select, validate, VEN


def fixture():
    meta = {"total": 6, "statuses": ["active", "withdrawn", "desk_rejected"],
            "statusCounts": {"active": 4, "withdrawn": 1, "desk_rejected": 1},
            "areas": ["ML", "Robotics"],
            "tags": [{"en": "Agents"}, {"en": "Robotics"}], "built": "2026-10-07"}
    rows = [
        ["abcde001", 1, "Agent reasoning benchmark", "planning", 0, 0, [0]],
        ["abcde002", 2, "Mathematical proof feedback", "grading", 0, 0, []],
        ["abcde003", 3, "Robotics locomotion control", "sim2real", 1, 0, [1]],
        ["abcde004", 4, "Temporal video diffusion", "audio", 0, 0, []],
        ["abcde005", 5, "Video withdrawn", "video", 0, 1, []],
        ["abcde006", 6, "Robotics rejected", "robot", 1, 2, []],
    ]
    return meta, rows


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.m, self.r = fixture()

    def test_counts(self):
        self.assertEqual(validate(self.m, self.r)["total"], 6)

    def test_reject_total_mismatch(self):
        self.m["total"] = 7
        with self.assertRaisesRegex(ValueError, "total mismatch"):
            validate(self.m, self.r)

    def test_partition_mismatch(self):
        self.m["statusCounts"]["active"] = 6
        with self.assertRaisesRegex(ValueError, "partition mismatch"):
            validate(self.m, self.r)

    def test_duplicate(self):
        self.r[1][0] = self.r[0][0]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate(self.m, self.r)

    def test_unsafe_id(self):
        self.r[0][0] = "../../secret"
        with self.assertRaisesRegex(ValueError, "unsafe"):
            validate(self.m, self.r)

    def test_malformed_row(self):
        self.r[0].pop()
        with self.assertRaisesRegex(ValueError, "seven"):
            validate(self.m, self.r)

    def test_reject_bad_area(self):
        self.r[0][4] = 9
        with self.assertRaisesRegex(ValueError, "area"):
            validate(self.m, self.r)

    def test_reject_bad_status(self):
        self.r[0][5] = True
        with self.assertRaisesRegex(ValueError, "status"):
            validate(self.m, self.r)

    def test_reject_bad_tag(self):
        self.r[0][6] = [55]
        with self.assertRaisesRegex(ValueError, "tag"):
            validate(self.m, self.r)

    def test_education(self):
        self.assertEqual(select(self.m, self.r, "education", 2)[0]["note_id"], "abcde002")

    def test_robotics_excludes_inactive(self):
        v = select(self.m, self.r, "robotics", 20)
        self.assertEqual([p["note_id"] for p in v], ["abcde003"])

    def test_studios_excludes_withdrawn(self):
        self.assertEqual([p["note_id"] for p in select(self.m, self.r, "studios")], ["abcde004"])

    def test_unknown_venture(self):
        with self.assertRaisesRegex(ValueError, "venture"):
            select(self.m, self.r, "unknown")

    def test_determinism(self):
        self.assertEqual(select(self.m, self.r, "agents"), select(self.m, copy.deepcopy(self.r), "agents"))

    def test_bounded_limits(self):
        with self.assertRaisesRegex(ValueError, "limit"):
            select(self.m, self.r, "agents", 101)

    def test_sha_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            m, p = Path(t) / "meta.json", Path(t) / "papers.json"
            m.write_text(json.dumps(self.m), encoding="utf8")
            p.write_text(json.dumps(self.r), encoding="utf8")
            report = build(self.m, self.r, m, p)
            self.assertEqual(len(report["provenance"]["rows_sha256"]), 64)
            self.assertIn("education", report["shortlists"])
            self.assertEqual(report["gate"], "R0_DISCOVERY_ONLY_NOT_RESEARCH_VALIDATION")


if __name__ == "__main__":
    unittest.main()
