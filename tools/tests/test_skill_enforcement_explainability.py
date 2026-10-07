from __future__ import annotations

import copy
import importlib.util
import json
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

ASSISTANT = Path(__file__).resolve().parents[2] / "ambiente_databricks/.assistant"
SKILL = ASSISTANT / "skills/hub-ml-explainability"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture():
    request = json.loads((SKILL / "tests/linear_fixture.json").read_text(encoding="utf-8"))
    model = LinearRegression().fit(np.array([[0, 0], [1, 0], [0, 1]], dtype=float),
                                   np.array([3, 5, 2], dtype=float))
    model.hub_model_id = request["model"]["model_id"]
    return request, model, np.array(request["X"], dtype=float), np.array(request["background"], dtype=float)


def test_positive_real_shap_and_oracle():
    runner = load(SKILL / "scripts/run.py", "explain_run_test")
    verifier = load(SKILL / "scripts/verify.py", "explain_verify_test")
    request, model, X, background = fixture()
    payload = runner.run(request, model=model, X=X, background=background, run_id="synthetic-run-1")
    assert payload["status"] == "PASS", payload["trace"]["blocking_issues"]
    assert np.allclose(payload["result"]["shap_values"], [[2, -2], [4, -1]])
    assert np.isclose(payload["result"]["base_value"], 3)
    checked = verifier.verify(payload, expected_request=request, expected_model=model,
                              expected_X=X, expected_background=background,
                              expected_run_id="synthetic-run-1")
    assert checked["valid"], checked["issues"]
    assert checked["completion_authorized"] is False
    assert payload["trace"]["context_provenance"]["numeric_columns"]["value"] == 2


def test_closed_request_and_bad_background_block_before_helper():
    runner = load(SKILL / "scripts/run.py", "explain_run_negative")
    request, model, X, background = fixture()
    malformed = copy.deepcopy(request)
    malformed["background"] = [[float("nan"), 0]]
    payload = runner.run(malformed, model=model, X=X, background=background, run_id="invalid")
    assert payload["status"] == "BLOCKED"
    assert payload["trace"]["resources_called"] == []
    malformed = copy.deepcopy(request)
    malformed["unknown"] = 1
    assert runner._preflight_module().validate_request(malformed)["status"] == "BLOCKED"


def test_replay_and_tamper_rejected():
    runner = load(SKILL / "scripts/run.py", "explain_run_tamper")
    verifier = load(SKILL / "scripts/verify.py", "explain_verify_tamper")
    request, model, X, background = fixture()
    payload = runner.run(request, model=model, X=X, background=background, run_id="run-a")
    assert payload["status"] == "PASS"
    args = dict(expected_request=request, expected_model=model, expected_X=X,
                expected_background=background, expected_run_id="run-b")
    assert not verifier.verify(payload, **args)["valid"]
    tampered = copy.deepcopy(payload)
    tampered["result"]["shap_values"][0][0] += 1
    args["expected_run_id"] = "run-a"
    result = verifier.verify(tampered, **args)
    assert not result["valid"]
    assert "ANALYTIC_ORACLE_MISMATCH" in result["issues"]


def test_model_and_array_binding():
    runner = load(SKILL / "scripts/run.py", "explain_run_binding")
    request, model, X, background = fixture()
    wrong = X.copy()
    wrong[0, 0] += 1
    payload = runner.run(request, model=model, X=wrong, background=background, run_id="binding")
    assert payload["status"] == "BLOCKED"
    assert payload["trace"]["resources_called"] == []


def test_helper_background_backward_compatible_and_restricted():
    from hub_snippets.ml.shap_explainer import compute_shap
    request, model, X, background = fixture()
    with redirect_stdout(io.StringIO()):
        values, base = compute_shap(model, X, request["feature_names"],
                                    model_type="linear", task="regression")
    assert np.isclose(base, 4.5)
    assert np.allclose(values, [[-1, -0.5], [1, 0.5]])
    try:
        compute_shap(model, X, request["feature_names"], model_type="tree",
                     task="regression", background=background)
    except ValueError as exc:
        assert "only for linear" in str(exc)
    else:
        raise AssertionError("nonlinear background should fail")


def test_mutation_during_helper_blocks_receipt():
    runner = load(SKILL / "scripts/run.py", "explain_run_mutation")
    request, model, X, background = fixture()

    def mutating_helper(model, array, names, **kwargs):
        array[0, 0] = 99
        return np.zeros_like(array), 3.0

    runner._canonical_primitive = lambda: mutating_helper
    payload = runner.run(request, model=model, X=X, background=background, run_id="mutation")
    assert payload["status"] == "BLOCKED"
    assert payload["receipt"] is None
    assert "INPUT_CHANGED_DURING_EXECUTION" in payload["trace"]["blocking_issues"][0]



def test_float32_inputs_use_float64_oracle():
    runner = load(SKILL / "scripts/run.py", "explain_run_float32")
    verifier = load(SKILL / "scripts/verify.py", "explain_verify_float32")
    request, model, _, _ = fixture()
    X = np.array([[0.1, 0.9], [0.9, 0.1]], dtype=np.float32)
    background = np.array([[0.2, 0.3]], dtype=np.float32)
    request["X"] = X.tolist()
    request["background"] = background.tolist()
    model.feature_names_in_ = np.array(request["feature_names"], dtype=object)
    payload = runner.run(request, model=model, X=X, background=background, run_id="float32")
    assert payload["status"] == "PASS", payload["trace"]["blocking_issues"]
    checked = verifier.verify(payload, expected_request=request, expected_model=model,
                              expected_X=X, expected_background=background,
                              expected_run_id="float32")
    assert checked["valid"], checked["issues"]


def test_inexact_integer_blocks_before_helper():
    runner = load(SKILL / "scripts/run.py", "explain_run_int64")
    request, model, X, background = fixture()
    unsafe = np.int64(2**53 + 1)
    X = X.astype(np.int64)
    X[0, 0] = unsafe
    request["X"] = X.tolist()
    payload = runner.run(request, model=model, X=X, background=background, run_id="int64")
    assert payload["status"] == "BLOCKED"
    assert payload["trace"]["resources_called"] == []


def test_model_feature_order_and_original_input_mutation():
    runner = load(SKILL / "scripts/run.py", "explain_run_names")
    request, model, X, background = fixture()
    model.feature_names_in_ = np.array(["x2", "x1"], dtype=object)
    payload = runner.run(request, model=model, X=X, background=background, run_id="names")
    assert payload["status"] == "BLOCKED"
    assert payload["trace"]["resources_called"] == []
    model.feature_names_in_ = np.array(request["feature_names"], dtype=object)

    def mutating_original(model, array, names, **kwargs):
        X[0, 0] = 99
        return np.zeros_like(array), 3.0

    runner._canonical_primitive = lambda: mutating_original
    payload = runner.run(request, model=model, X=X, background=background, run_id="source-mutation")
    assert payload["status"] == "BLOCKED"
    assert payload["receipt"] is None
    assert "INPUT_CHANGED_DURING_EXECUTION" in payload["trace"]["blocking_issues"][0]


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for name, value in sorted(globals().items()):
        if name.startswith("test_") and callable(value):
            suite.addTest(unittest.FunctionTestCase(value, description=name))
    return suite
