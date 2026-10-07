"""SER07/08 fixed-lag candidate: real helper call, leakage boundaries and Receipt."""
from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "ambiente_databricks/.assistant"
sys.path.insert(0, str(ROOT))
SKILL = ROOT / "skills/hub-ml-feature-engineering"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _request():
    def row(rid, entity, day, value):
        return {"id": rid, "entity_id": entity,
                "event_at": f"2026-01-{day:02d}T00:00:00+00:00",
                "available_at": f"2026-01-{day+1:02d}T00:00:00+00:00", "value": value}
    return {"schema_version": "SER07-REQUEST-1", "profile": "FIXED_LAG_L1_V1",
            "synthetic": True, "population_id": "synthetic-panel-01",
            "decision_at": "2026-01-10T00:00:00+00:00", "window_days": 4,
            "requested_effect": "NONE", "temporal": {
                "reference_column": "event_at", "availability_column": "available_at",
                "lag_kind": "CONSTANT", "lag_days": 1, "boundary": "LE",
                "timezone": "UTC", "tie_break": "REJECT", "bitemporal": False},
            "rows": [row("a7", "A", 7, 1), row("a8", "A", 8, 2),
                     row("a10", "A", 10, 5), row("a11", "A", 11, 7),
                     row("b7", "B", 7, 10), row("b8", "B", 8, 20)]}


def test_fixed_lag_helper_receipt_and_adversaries():
    runner = _load("_ser07_test_runner", SKILL / "scripts/run.py")
    verifier = _load("_ser07_test_verifier", SKILL / "scripts/verify.py")
    request = _request()
    oracle = [{"id": "a8", "entity_id": "A", "event_at": "2026-01-08", "lag_1": 1.0},
              {"id": "b8", "entity_id": "B", "event_at": "2026-01-08", "lag_1": 10.0}]
    payload = runner.run(request, run_id="fe-local-001")
    assert payload["status"] == "PASS", payload
    assert payload["result"]["features"] == oracle
    assert payload["result"]["excluded_counts"] == {"future": 1, "unavailable": 1, "outside_window": 0}
    assert verifier.verify(payload, expected_request=request, expected_run_id="fe-local-001",
                           expected_features=oracle)["valid"]
    mutant = copy.deepcopy(payload)
    mutant["result"]["features"][0]["lag_1"] = 5.0
    assert not verifier.verify(mutant, expected_request=request, expected_run_id="fe-local-001",
                               expected_features=oracle)["valid"]
    bad = copy.deepcopy(request)
    bad["rows"][2]["available_at"] = "2026-01-10T00:00:00+00:00"
    assert runner.preflight(bad)["status"] == "BLOCKED"
    bad = copy.deepcopy(request)
    del bad["temporal"]
    assert runner.preflight(bad)["status"] == "BLOCKED"


def test_run_identity_cannot_be_omitted_or_coerced():
    runner = _load("_ser07_identity_runner", SKILL / "scripts/run.py")
    verifier = _load("_ser07_identity_verifier", SKILL / "scripts/verify.py")
    request = _request()
    good = runner.run(request, run_id="independent-id")
    assert good["status"] == "PASS", good
    oracle = [{"id": "a8", "entity_id": "A", "event_at": "2026-01-08", "lag_1": 1.0},
              {"id": "b8", "entity_id": "B", "event_at": "2026-01-08", "lag_1": 10.0}]
    for invalid in (None, "", " ", False, 0, "other-id"):
        assert not verifier.verify(good, expected_request=request, expected_run_id=invalid,
                                   expected_features=oracle)["valid"], invalid
    for invalid in ("", " ", False, 0):
        blocked = runner.run(request, run_id=invalid)
        assert blocked["status"] == "BLOCKED", invalid
        assert blocked["receipt"] is None


def test_dates_cutoff_window_and_out_of_order_history():
    runner = _load("_ser07_boundary_runner", SKILL / "scripts/run.py")
    request = _request()
    request["rows"] += [
        {"id": "a6", "entity_id": "A", "event_at": "20260106T00:00:00+00:00",
         "available_at": "20260107T00:00:00+00:00", "value": -2},
        {"id": "a9", "entity_id": "A", "event_at": "2026-01-09T00:00:00+00:00",
         "available_at": "2026-01-10T00:00:00+00:00", "value": 8}]
    request["rows"].reverse()
    out = runner.run(request, run_id="boundary-id")
    assert out["status"] == "PASS", out
    assert out["result"]["features"] == [
        {"id": "a7", "entity_id": "A", "event_at": "2026-01-07", "lag_1": -2.0},
        {"id": "a8", "entity_id": "A", "event_at": "2026-01-08", "lag_1": 1.0},
        {"id": "a9", "entity_id": "A", "event_at": "2026-01-09", "lag_1": 2.0},
        {"id": "b8", "entity_id": "B", "event_at": "2026-01-08", "lag_1": 10.0}]


def test_empty_warmup_is_explicit_empty_output_not_materialization():
    runner = _load("_ser07_empty_runner", SKILL / "scripts/run.py")
    request = _request()
    request["rows"] = [request["rows"][0], request["rows"][4]]
    out = runner.run(request, run_id="empty-warmup")
    assert out["status"] == "PASS", out
    assert out["result"]["features"] == []
    assert out["result"]["eligible_ids"] == ["a7", "b7"]
    assert not out["result"]["materialization_performed"]


def load_tests(loader, tests, pattern):
    import unittest
    return unittest.TestSuite(unittest.FunctionTestCase(fn) for name, fn in globals().items()
                              if name.startswith("test_") and callable(fn))
