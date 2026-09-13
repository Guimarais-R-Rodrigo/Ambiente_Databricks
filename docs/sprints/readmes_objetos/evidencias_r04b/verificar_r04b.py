"""Casos datados da R04-B para seis Hub Scripts, com Spark opcional/obrigatório."""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT = ROOT / "ambiente_fonte" / ".assistant"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))

OBJECTS = [
    "data_quality_check",
    "doc_coverage",
    "drift_detector",
    "naming_checker",
    "rfv_calculator",
    "schema_to_yaml",
]

try:
    from pyspark.sql import SparkSession
except ImportError:
    SparkSession = None

REQUIRE_SPARK = False


def spark_case(fn):
    return unittest.skipIf(SparkSession is None and not REQUIRE_SPARK, "PySpark opcional nesta execução")(fn)


class StaticCases(unittest.TestCase):
    def test_six_readmes_have_contract_marker_and_sections(self):
        expected = [f"## {i}." for i in range(1, 16)]
        for obj in OBJECTS:
            path = ASSISTANT / "hub_scripts" / obj / "README.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text, obj)
            positions = [text.index(prefix) for prefix in expected]
            self.assertEqual(positions, sorted(positions), obj)
            self.assertIn(f"exemplo_{obj}.py", text, obj)
            self.assertIn(f"[{('implementação')}](", text, obj)

    def test_no_readme_claims_independent_audit_or_publication(self):
        for obj in OBJECTS:
            text = (ASSISTANT / "hub_scripts" / obj / "README.md").read_text(encoding="utf-8").lower()
            self.assertNotIn("auditoria independente aprovada", text)
            self.assertNotIn("publicado no databricks", text)


class DocCoverageCases(unittest.TestCase):
    def test_documented_and_dry_sources(self):
        from hub_scripts.doc_coverage import doc_coverage
        with tempfile.TemporaryDirectory() as d:
            good = Path(d) / "good.py"
            bad = Path(d) / "bad.py"
            good.write_text(
                "# Databricks notebook source\n# MAGIC %md\n# MAGIC explicação\n"
                "# COMMAND ----------\nx = 1\n",
                encoding="utf-8",
            )
            bad.write_text(
                "# Databricks notebook source\nx = 1\n# COMMAND ----------\ny = 2\n",
                encoding="utf-8",
            )
            self.assertEqual(doc_coverage(str(good))["coverage_pct"], 100.0)
            self.assertEqual(doc_coverage(str(bad))["coverage_pct"], 0.0)

    def test_empty_markdown_still_counts_by_design(self):
        from hub_scripts.doc_coverage import doc_coverage
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "empty.py"
            p.write_text("# MAGIC %md\n# MAGIC .\n# COMMAND ----------\nx=1\n", encoding="utf-8")
            self.assertEqual(doc_coverage(str(p))["coverage_pct"], 100.0)

    def test_zero_code_returns_hundred_by_convention(self):
        from hub_scripts.doc_coverage import doc_coverage
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "only_md.py"
            p.write_text("# MAGIC %md\n# MAGIC texto\n", encoding="utf-8")
            result = doc_coverage(str(p))
            self.assertEqual(result["total_code_cells"], 0)
            self.assertEqual(result["coverage_pct"], 100.0)

    def test_unsupported_extension_rejected(self):
        from hub_scripts.doc_coverage import doc_coverage
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.txt"; p.write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError):
                doc_coverage(str(p))


class SparkCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SparkSession is None:
            if REQUIRE_SPARK:
                raise RuntimeError("--require-spark foi solicitado, mas PySpark não está instalado")
            cls.spark = None
            return
        cls.spark = (
            SparkSession.builder.master("local[2]")
            .appName("readmes-r04b")
            .config("spark.ui.enabled", "false")
            .getOrCreate()
        )
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "spark", None) is not None:
            cls.spark.stop()

    @spark_case
    def test_data_quality_detects_duplicate_null_key_and_null_rate(self):
        from hub_scripts.data_quality_check import data_quality_check
        today = date.today()
        df = self.spark.createDataFrame(
            [(1, today, 1.0), (2, today, None), (2, today, 3.0), (None, today, 4.0)],
            "id int, dt date, valor double",
        )
        df.createOrReplaceTempView("r04b_dq")
        out = data_quality_check(
            "r04b_dq", ["id"], "dt",
            thresholds={"null_warn": 20.0, "null_fail": 50.0, "freshness_days": 0},
        )
        self.assertEqual(out["status"], "fail")
        self.assertEqual(out["checks"]["pk_uniqueness"]["duplicate_rows"], 1)
        self.assertEqual(out["checks"]["pk_uniqueness"]["null_key_rows"], 1)
        self.assertEqual(out["checks"]["nulls"]["valor"]["pct"], 25.0)
        self.assertEqual(out["checks"]["freshness"]["days_old"], 0)

    @spark_case
    def test_data_quality_threshold_validation(self):
        from hub_scripts.data_quality_check import data_quality_check
        with self.assertRaises(ValueError):
            data_quality_check("qualquer", ["id"], thresholds={"null_warn": 30, "null_fail": 20})
        with self.assertRaises(ValueError):
            data_quality_check("qualquer", [])

    @spark_case
    def test_naming_checker_separates_policy_origins(self):
        from hub_scripts.naming_checker import naming_checker
        self.spark.createDataFrame([(1, 2)], "id_ok int, ValorTotal int").createOrReplaceTempView("vw_r04b_nome")
        out = naming_checker("vw_r04b_nome", max_col_length=40)
        policies = [x["policy"] for x in out]
        self.assertIn("databricks-recommended-context", policies)
        self.assertIn("project-custom", policies)
        self.assertTrue(all(x["severity"] == "warning" for x in out))
        with self.assertRaises(ValueError):
            naming_checker("vw_r04b_nome", enforce_prefix=True)

    @spark_case
    def test_rfv_cutoff_windows_and_future_exclusion(self):
        from hub_scripts.rfv_calculator import rfv_calculator
        rows = [
            ("a", "2026-06-01", 10.0),
            ("a", "2026-05-03", 20.0),
            ("a", "2026-04-01", 30.0),
            ("a", "2026-06-02", 999.0),
            ("b", "2026-05-01", 5.0),
        ]
        self.spark.createDataFrame(rows, "id string, dt string, valor double").createOrReplaceTempView("r04b_rfv")
        out = rfv_calculator("r04b_rfv", "id", "dt", "valor", "2026-06-01", periodos=(30, 60))
        a = out.filter("id='a'").first().asDict()
        self.assertEqual(a["frequencia_total"], 3)
        self.assertEqual(a["valor_total"], 60.0)
        self.assertEqual(a["frequencia_30d"], 2)
        self.assertEqual(a["frequencia_60d"], 2)
        self.assertEqual(a["recencia"], 0)

    @spark_case
    def test_rfv_invalid_periods_rejected(self):
        from hub_scripts.rfv_calculator import rfv_calculator
        with self.assertRaises(ValueError):
            rfv_calculator("qualquer", "id", "dt", "valor", "2026-01-01", periodos=())
        with self.assertRaises(ValueError):
            rfv_calculator("qualquer", "id", "dt", "valor", "2026-01-01", periodos=(0, 30))

    @spark_case
    def test_drift_detector_shift_and_classification(self):
        from hub_scripts.drift_detector import drift_detector
        rows = []
        for i in range(100):
            rows.append(("ref", float(i % 10)))
            rows.append(("comp", float(20 + (i % 10))))
        self.spark.createDataFrame(rows, "safra string, x double").createOrReplaceTempView("r04b_drift")
        plain = drift_detector("r04b_drift", "safra", "ref", "comp", cols=["x"], num_bins=5)
        self.assertEqual(plain["x"]["classification"], "not_classified")
        self.assertGreater(plain["x"]["psi"], 0)
        classified = drift_detector(
            "r04b_drift", "safra", "ref", "comp", cols=["x"], num_bins=5,
            warning_threshold=0.01, critical_threshold=0.02,
        )
        self.assertEqual(classified["x"]["classification"], "critical")

    @spark_case
    def test_drift_rejects_method_and_empty_cohort(self):
        from hub_scripts.drift_detector import drift_detector
        self.spark.createDataFrame([("ref", 1.0)], "safra string, x double").createOrReplaceTempView("r04b_drift_small")
        with self.assertRaises(ValueError):
            drift_detector("r04b_drift_small", "safra", "ref", "ref", cols=["x"], method="ks")
        with self.assertRaises(ValueError):
            drift_detector("r04b_drift_small", "safra", "ref", "missing", cols=["x"])

    @spark_case
    def test_schema_dict_stats_and_yaml_roundtrip(self):
        from hub_scripts.schema_to_yaml import schema_to_dict, schema_to_yaml
        self.spark.createDataFrame([(1, "a"), (2, None), (2, "b")], "id int, nome string").createOrReplaceTempView("r04b_schema")
        payload = schema_to_dict("r04b_schema", include_stats=True)
        self.assertEqual(payload["row_count"], 3)
        by_name = {x["name"]: x for x in payload["columns"]}
        self.assertEqual(by_name["nome"]["stats"]["null_count"], 1)
        text = schema_to_yaml("r04b_schema")
        try:
            import yaml
            parsed = yaml.safe_load(text)
        except ImportError:
            parsed = json.loads(text)
        self.assertEqual(parsed["table"], "r04b_schema")
        self.assertEqual([c["name"] for c in parsed["columns"]], ["id", "nome"])


def main() -> int:
    global REQUIRE_SPARK
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-spark", action="store_true")
    args = parser.parse_args()
    REQUIRE_SPARK = args.require_spark
    if REQUIRE_SPARK and SparkSession is None:
        print("ERRO: --require-spark exige PySpark instalado", file=sys.stderr)
        return 2
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if REQUIRE_SPARK and result.skipped:
        print(f"ERRO: {len(result.skipped)} caso(s) pulado(s) com --require-spark", file=sys.stderr)
        return 3
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
