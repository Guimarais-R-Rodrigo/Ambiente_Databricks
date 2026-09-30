from __future__ import annotations
import copy, importlib.util, os, sys, unittest
from pathlib import Path
import jdk4py
os.environ["JAVA_HOME"]=str(jdk4py.JAVA_HOME)
os.environ["PYSPARK_PYTHON"]=sys.executable
os.environ["SPARK_LOCAL_IP"]="127.0.0.1"
root=Path(__file__).resolve().parents[2]
assistant=Path(os.environ.get("SER06_ASSISTANT_ROOT", str(root/"ambiente_fonte/.assistant")))
sys.path.insert(0,str(assistant))
from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.receipt import build_execution_receipt
from pyspark.sql import SparkSession
def load(name):
    path=assistant/"skills/hub-ml-cross-eda-ml/scripts"/name
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
r=load("run_pit.py");v=load("verify_pit.py")
facts=[{"decision_id":"d1","entity_id":"a","decision_at":"2026-01-10T00:00:00Z"},
       {"decision_id":"d2","entity_id":"b","decision_at":"2026-01-10T00:00:00Z"},
       {"decision_id":"d3","entity_id":"c","decision_at":"2026-01-10T00:00:00Z"}]
features=[{"entity_id":"a","reference_at":"2026-01-08T00:00:00Z","available_at":"2026-01-09T00:00:00Z","feature_value":1},
          {"entity_id":"a","reference_at":"2026-01-09T00:00:00Z","available_at":"2026-01-10T00:00:00Z","feature_value":2},
          {"entity_id":"a","reference_at":"2026-01-10T00:00:00Z","available_at":"2026-01-11T00:00:00Z","feature_value":3},
          {"entity_id":"b","reference_at":"2026-01-01T00:00:00Z","available_at":"2026-01-02T00:00:00Z","feature_value":9}]
datasets={"facts":facts,"history":features}
context={"schema_version":"SER05-CONTEXT-1","profile":"CONTEXT_ONLY_PILOT_V1",
         "synthetic":True,"sources":[
         {"id":"facts","snapshot_id":"synthetic-facts-v1","content_sha256":digest(facts),
          "grain":"ONE_ROW_PER_ENTITY_DECISION","columns":list(facts[0])},
         {"id":"history","snapshot_id":"synthetic-history-v1","content_sha256":digest(features),
          "grain":"FEATURE_HISTORY","columns":list(features[0])}],
         "anchor":"facts","entity_keys":["entity_id"],"anchor_grain":"ONE_ROW_PER_ENTITY_DECISION",
         "cardinality":"N:1","decision_at":"2026-01-10T00:00:00Z","pit":"APPLICABLE",
         "temporal":{"reference_column":"reference_at","availability_column":"available_at",
                     "lag_kind":"CONSTANT","lag_days":1,"boundary":"LE","timezone":"UTC",
                     "tie_break":"REJECT","bitemporal":False},
         "null_key_policy":"REJECT","requested_effect":"NONE"}
def test_synthetic_pit_and_adversarial():
    spark=SparkSession.builder.master("local[1]").appName("ser06-pit-overlay").config("spark.sql.session.timeZone","UTC").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    try:
        p=r.run(context,datasets,spark,window_days=5,run_id="SER06-SYNTH-1")
        print("RUN",p["status"],p["trace"]["blocking_issues"])
        assert p["status"]=="PASS",p["trace"]["blocking_issues"]
        assert [x["feature_value"] for x in p["result"]["records"]]==[2,None,None]
        final=v.finalize(p,expected_context=context,expected_datasets=datasets,expected_window_days=5,expected_run_id="SER06-SYNTH-1")
        check=v.verify_finalized(final,expected_context=context,expected_datasets=datasets,expected_window_days=5,expected_run_id="SER06-SYNTH-1")
        print("FINAL",final["postflight"]["status"],check)
        assert check["valid"],check
        forged=copy.deepcopy(final)
        forged["result"]["records"][0]["feature_value"]=3
        forged["artifacts"]["point_in_time_join"]=forged["result"]
        forged["trace"]["output_digest"]=digest(forged["result"])
        forged["receipt"]=build_execution_receipt(forged["trace"],forged["result"],expected_skill=r.SKILL,expected_entrypoint=r.ENTRYPOINT,protected_primitive=r.PRIMITIVE_ID)
        assert not v.verify_finalized(forged,expected_context=context,expected_datasets=datasets,expected_window_days=5,expected_run_id="SER06-SYNTH-1")["valid"]
        for mode in ("future","tie","availability","lt","duplicate_instant"):
            dc=copy.deepcopy(datasets);cc=copy.deepcopy(context)
            if mode=="future":
                dc["history"][1]["available_at"]="2026-01-11T00:00:00Z"
            elif mode=="tie":
                dc["history"].append(copy.deepcopy(dc["history"][1]))
            elif mode=="availability":
                dc["history"][0]["available_at"]="2026-01-10T00:00:00Z"
            elif mode=="duplicate_instant":
                dc["facts"].append({"decision_id":"d4","entity_id":"a",
                                    "decision_at":"2026-01-10T00:00:00+00:00"})
            else:
                cc["temporal"]["boundary"]="LT"
            for source in cc["sources"]:
                source["content_sha256"]=digest(dc[source["id"]])
            blocked=r.run(cc,dc,spark,window_days=5,run_id="SER06-"+mode)
            print(mode,blocked["status"],blocked["trace"]["blocking_issues"])
            assert blocked["status"]=="BLOCKED"
            if mode=="duplicate_instant":
                assert "FACT_DUPLICATE_ID_OR_GRAIN" in str(blocked["trace"]["blocking_issues"])
    finally:
        spark.stop()

def load_tests(loader, tests, pattern):
    suite=unittest.TestSuite()
    suite.addTest(unittest.FunctionTestCase(test_synthetic_pit_and_adversarial))
    return suite
