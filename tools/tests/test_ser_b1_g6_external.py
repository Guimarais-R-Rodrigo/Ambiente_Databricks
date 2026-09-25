from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.skill_enforcement.real_campaigns.b1.g6.validate_package import validate

ROOT = Path(__file__).resolve().parents[2]
G6 = ROOT / "tools/skill_enforcement/real_campaigns/b1/g6"


class G6PackageTests(unittest.TestCase):
    def test_package_validator_passes(self):
        report = validate()
        self.assertEqual("PASS", report["status"], report["issues"])
        self.assertEqual(16, report["genie_case_count"])
        self.assertEqual(20, report["genie_variant_count"])
        self.assertEqual(2, report["free_probe_count"])
        self.assertFalse(report["execution_authorized"])

    def test_external_manifest_is_fail_closed_before_human_gate(self):
        payload = json.loads((G6 / "external_manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["execution_authorized"])
        self.assertFalse(payload["promotion_authorized"])
        self.assertFalse(payload["policy_change_authorized"])
        self.assertTrue(all(row["authorized"] is False for row in payload["external_phases"]))

    def test_cleanup_is_separate_effect_and_not_pre_authorized(self):
        payload = json.loads((G6 / "external_manifest.json").read_text(encoding="utf-8"))
        phases = {row["phase_id"]: row for row in payload["external_phases"]}
        cleanup = phases["G6.PROBE_CLEANUP_AFTER_AUDIT"]
        self.assertEqual("TEMPORARY_WORKSPACE_OBJECT_DELETE", cleanup["effect"])
        self.assertFalse(cleanup["authorized"])
        self.assertIn("after evidence", cleanup["prerequisite"])

    def test_genie_manifest_starts_without_observed_results(self):
        payload = json.loads((G6 / "genie_manifest.json").read_text(encoding="utf-8"))
        variants = [v for skill in payload["skills"] for v in skill["variants"]]
        self.assertEqual(20, len(variants))
        self.assertTrue(all(v["execution_status"] == "NOT_RUN" for v in variants))
        self.assertTrue(all(v["evidence"]["response_literal"] is None for v in variants))
        self.assertTrue(all(v["evidence"]["evidence_grade"] == "NOT_OBSERVABLE" for v in variants))

    def test_each_skill_has_two_extra_neighbor_negatives(self):
        payload = json.loads((G6 / "genie_manifest.json").read_text(encoding="utf-8"))
        for skill in payload["skills"]:
            g03 = [v for v in skill["variants"] if v["case_id"].endswith("-G03")]
            self.assertEqual(3, len(g03))
            self.assertEqual(2, sum("-N" in v["variant_id"] for v in g03))

    def test_free_probe_sources_do_not_contain_known_write_entrypoints(self):
        for name in ("ser03_free_probe.py", "ser05_l2_free_probe.py"):
            text = (G6 / name).read_text(encoding="utf-8")
            for token in ("workspace import", "saveAsTable", ".write.format(", "dbutils.fs.rm", "dbutils.fs.put"):
                self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
