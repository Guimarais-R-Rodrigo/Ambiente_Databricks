"""Synthetic Spark proof for the static SER05 diagnostic candidate."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = ROOT / "ambiente_databricks/.assistant"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))

from hub_scripts.skill_execution.domain_context import digest

SPEC = importlib.util.spec_from_file_location(
    "ser05_run_diagnostic",
    ASSISTANT / "skills/hub-ml-cross-eda-ml/scripts/run_diagnostic.py",
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
SPEC = importlib.util.spec_from_file_location(
    "ser05_verify_diagnostic",
    ASSISTANT / "skills/hub-ml-cross-eda-ml/scripts/verify_diagnostic.py",
)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class CrossDiagnosticSparkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.spark = SparkSession.builder.master("local[1]").appName("ser05-synthetic-diagnostic").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def setUp(self):
        fixture = ROOT / "tools/tests/fixtures/ser_b1/ce_l2_static.json"
        self.context = json.loads(fixture.read_text(encoding="utf-8"))["context"]
        self.datasets = {
            "anchor_snapshot": [
                {"entity_id": "a", "value": 1},
                {"entity_id": "b", "value": 2},
                {"entity_id": "c", "value": 3},
            ],
            "attributes_snapshot": [
                {"entity_id": "a", "flag": 1},
                {"entity_id": "b", "flag": 0},
            ],
        }
        self._bind()

    def _bind(self):
        for source in self.context["sources"]:
            rows = self.datasets[source["id"]]
            source["columns"] = list(rows[0])
            source["content_sha256"] = digest(rows)

    def test_static_diagnostic_receipt_and_independent_oracle(self):
        expected = {
            "linhas_esquerda": 3, "linhas_direita": 2,
            "chaves_nulas_esquerda": 0, "chaves_nulas_direita": 0,
            "linhas_descartadas_chave_nula": 0, "linhas_com_match": 2,
            "linhas_sem_match_chave_valida": 1, "cobertura_pct_chaves_validas": 66.67,
            "multiplicidade_max_direita": 1, "multiplicidade_media_direita": 1.0,
            "relacao": "1:1 ou N:1 — join preserva a cardinalidade",
            "linhas_apos_join_left": 3, "linhas_apos_join_inner": 2,
            "expansao_prevista_left": 1.0, "expansao_prevista_inner": 0.667,
            "exemplos_sem_match": [{"entity_id": "c"}], "exemplos_chave_nula": [],
        }
        payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-STATIC-001")
        self.assertEqual("PASS", payload["status"], payload["trace"]["blocking_issues"])
        self.assertEqual([runner.PRIMITIVE_ID], payload["trace"]["resources_completed"])
        verified = verifier.verify(payload, expected_context=self.context,
                                   expected_datasets=self.datasets,
                                   expected_run_id="CE-L3-STATIC-001",
                                   expected_diagnostic=expected)
        self.assertTrue(verified["valid"], verified)
        self.assertFalse(verified["completion_authorized"])
        tampered = copy.deepcopy(payload)
        tampered["result"]["diagnostic"]["linhas_com_match"] = 3
        self.assertFalse(verifier.verify(tampered, expected_context=self.context,
                                         expected_datasets=self.datasets,
                                         expected_run_id="CE-L3-STATIC-001",
                                         expected_diagnostic=expected)["valid"])

    def test_duplicate_right_blocks_after_real_diagnostic(self):
        self.datasets["attributes_snapshot"].append({"entity_id": "a", "flag": 2})
        self._bind()
        payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-DUP-001")
        self.assertEqual("BLOCKED", payload["status"])
        self.assertEqual([runner.PRIMITIVE_ID], payload["trace"]["resources_completed"])
        self.assertIsNone(payload["receipt"])

    def test_stale_source_hash_blocks_before_helper(self):
        self.datasets["attributes_snapshot"][0]["flag"] = 9
        payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-HASH-001")
        self.assertEqual("BLOCKED", payload["status"])
        self.assertEqual([], payload["trace"]["resources_called"])
        self.assertIsNone(payload["receipt"])

    def test_null_key_and_duplicate_anchor_block_before_helper(self):
        for value in (None, "a"):
            with self.subTest(value=value):
                self.setUp()
                self.datasets["anchor_snapshot"][2]["entity_id"] = value
                self._bind()
                payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-KEY-001")
                self.assertEqual("BLOCKED", payload["status"])
                self.assertEqual([], payload["trace"]["resources_called"])

    def test_key_type_mismatch_and_mixed_types_block(self):
        for right_key in (1, True):
            with self.subTest(right_key=right_key):
                self.setUp()
                self.datasets["attributes_snapshot"][0]["entity_id"] = right_key
                self._bind()
                payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-TYPE-001")
                self.assertEqual("BLOCKED", payload["status"])
                self.assertEqual([], payload["trace"]["resources_called"])

    def test_uniform_cross_source_key_type_mismatch_blocks(self):
        self.datasets["attributes_snapshot"][0]["entity_id"] = 1
        self.datasets["attributes_snapshot"][1]["entity_id"] = 2
        self._bind()
        payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-COERCE-001")
        self.assertEqual("BLOCKED", payload["status"])
        self.assertIn("KEY_TYPE_MISMATCH", " ".join(payload["trace"]["blocking_issues"]))
        self.assertEqual([], payload["trace"]["resources_called"])
    def test_receipt_replay_wrong_run_and_context_rejected(self):
        expected = {
            "linhas_esquerda": 3, "linhas_direita": 2,
            "chaves_nulas_esquerda": 0, "chaves_nulas_direita": 0,
            "linhas_descartadas_chave_nula": 0, "linhas_com_match": 2,
            "linhas_sem_match_chave_valida": 1, "cobertura_pct_chaves_validas": 66.67,
            "multiplicidade_max_direita": 1, "multiplicidade_media_direita": 1.0,
            "relacao": "1:1 ou N:1 — join preserva a cardinalidade",
            "linhas_apos_join_left": 3, "linhas_apos_join_inner": 2,
            "expansao_prevista_left": 1.0, "expansao_prevista_inner": 0.667,
            "exemplos_sem_match": [{"entity_id": "c"}], "exemplos_chave_nula": [],
        }
        payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-REPLAY-001")
        self.assertEqual("PASS", payload["status"])
        self.assertFalse(verifier.verify(payload, expected_context=self.context,
                                         expected_datasets=self.datasets,
                                         expected_run_id="CE-L3-OTHER",
                                         expected_diagnostic=expected)["valid"])
        other = copy.deepcopy(self.context)
        other["decision_at"] = "2026-01-11T00:00:00Z"
        self.assertFalse(verifier.verify(payload, expected_context=other,
                                         expected_datasets=self.datasets,
                                         expected_run_id="CE-L3-REPLAY-001",
                                         expected_diagnostic=expected)["valid"])
    def test_pit_applicable_blocks_before_spark_diagnostic(self):
        self.context["pit"] = "APPLICABLE"
        self.context.pop("not_applicable_reason")
        self.context["temporal"] = {
            "reference_column": "reference_at", "availability_column": "available_at",
            "lag_kind": "CONSTANT", "lag_days": 1, "timezone": "UTC",
            "boundary": "LE", "tie_break": "REJECT", "bitemporal": False,
        }
        for source in self.context["sources"]:
            source["columns"] += ["reference_at", "available_at"]
        payload = runner.run(self.context, self.datasets, self.spark, run_id="CE-L3-PIT-001")
        self.assertEqual("BLOCKED", payload["status"])
        self.assertEqual([], payload["trace"]["resources_called"])
        self.assertIsNone(payload["receipt"])


if __name__ == "__main__":
    unittest.main()
