"""V12 — regressão da evidência real AI/BI, sem converter CI em ambiente."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "temas_v12_homologacao.py"
SPEC = importlib.util.spec_from_file_location("temas_v12_homologacao_evidence", MODULE_PATH)
assert SPEC and SPEC.loader
v12 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v12)

EVIDENCE = ROOT / "docs" / "sprints" / "sistema_temas" / "V12" / "evidencias" / "V12-AIBI-01"
ATTEMPT_1 = EVIDENCE / "V12-AIBI-01_attempt-01.json"
ATTEMPT_2 = EVIDENCE / "V12-AIBI-01_attempt-02.json"
SYNTHETIC_SQL = (
    EVIDENCE / "synthetic_trips.sql",
    EVIDENCE / "synthetic_route_revenue.sql",
)


class RealAibiEvidenceTests(unittest.TestCase):
    def test_real_records_remain_fail_closed_and_synthetic_pass_validates(self):
        matrix = v12.load_matrix()

        first = json.loads(ATTEMPT_1.read_text(encoding="utf-8"))
        second = json.loads(ATTEMPT_2.read_text(encoding="utf-8"))

        self.assertEqual(first["status"], "FAIL")
        self.assertFalse(first["facts"]["synthetic_data_only"])
        v12.validate_evidence(first, matrix)

        self.assertEqual(second["status"], "PASS")
        self.assertTrue(second["facts"]["synthetic_data_only"])
        self.assertFalse(second["facts"]["published"])
        v12.validate_evidence(second, matrix)

        for path in SYNTHETIC_SQL:
            sql = path.read_text(encoding="utf-8")
            upper = sql.upper()
            self.assertIn("FROM VALUES", upper)
            self.assertNotIn("SAMPLES.NYCTAXI", upper)
            for forbidden in ("CREATE TABLE", "CREATE SCHEMA", "CREATE VOLUME", "INSERT INTO", "MERGE INTO"):
                self.assertNotIn(forbidden, upper)


if __name__ == "__main__":
    unittest.main(verbosity=2)
