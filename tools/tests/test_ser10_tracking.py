"""Fake MLflow protocol tests; remote capability is verified separately on Free."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

_MISSING = object()

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = Path(os.environ.get("SER10_CANDIDATE_ASSISTANT_ROOT",
                                ROOT / "ambiente_databricks/.assistant"))
sys.path.insert(0, str(ASSISTANT))
from hub_scripts.skill_execution.domain_context import digest


def load(name):
    path = ASSISTANT / "skills/hub-ml-baseline-ml/scripts" / name
    spec = importlib.util.spec_from_file_location("ser10_test_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request():
    return {
        "schema_version": "SER09-REQUEST-1", "profile": "BINARY_TEMPORAL_LOCAL_V1",
        "synthetic": True, "requested_effect": "NONE", "population_id": "SYNTHETIC-P01",
        "target": "target", "positive_class": 1, "unit": "synthetic_entity",
        "date_column": "observed_at", "feature_order": ["feature"], "train_pct": 0.5,
        "val_pct": 0.25, "gap_periods": 0, "period_unit": "M", "threshold": 0.5, "seed": 17,
        "rows": [{"id": f"B{i:02d}", "observed_at": f"2024-{i:02d}-01T00:00:00Z",
                  "feature": float(i % 5), "target": i % 2} for i in range(1, 13)],
    }


def authority(q, rid="candidate-1"):
    return {
        "schema_version": "SER10-AUTH-1", "authorized": True,
        "effect": "CREATE_EXPERIMENT_RUN_LOG_MODEL_SOFTDELETE",
        "target_experiment": "/Users/test@example.com/hub_lab/skills_delivery_1234abcd",
        "request_sha256": digest(q), "run_id": rid, "current_user": "test@example.com",
        "retention": "SOFT_DELETE_AFTER_READBACK", "authorization_id": "human-auth-1",
    }


class FakeSpark:
    def sql(self, statement):
        assert statement == "SELECT current_user() AS user"
        return types.SimpleNamespace(first=lambda: {"user": "test@example.com"})


class FakeMlflow(types.ModuleType):
    def __init__(self):
        super().__init__("mlflow")
        self.experiments = {}
        self.runs = {}
        self.active = None
        self.created = 0
        self.logged_model = None
        self.fail_readback = False
        self.fail_cleanup = False
        self.model_load_calls = 0
        self.autolog_enabled = True
        self.sklearn_autolog_enabled = True
        self.tracking = types.SimpleNamespace(MlflowClient=lambda: self)
        self.models = types.SimpleNamespace(get_model_info=self.get_model_info)
        self.sklearn = types.ModuleType("mlflow.sklearn")
        self.sklearn.autolog = self.sklearn_autolog
        self.sklearn.log_model = self.log_model
        self.sklearn.load_model = self.load_model

    def get_tracking_uri(self): return "databricks"
    def autolog(self, **kwargs):
        if kwargs.get("disable") is True:
            self.autolog_enabled = False
    def sklearn_autolog(self, **kwargs):
        if kwargs.get("disable") is True:
            self.sklearn_autolog_enabled = False
    def active_run(self): return self.active
    def set_experiment(self, name): self.current_experiment = name
    def set_tags(self, values): self.active.data.tags.update(values)
    def log_params(self, values): self.active.data.params.update({k: str(v) for k, v in values.items()})
    def log_metrics(self, values): self.active.data.metrics.update(values)

    @contextlib.contextmanager
    def start_run(self, run_name):
        exp = self.experiments[self.current_experiment]
        obj = types.SimpleNamespace(
            info=types.SimpleNamespace(run_id="fake-run-1", experiment_id=exp.experiment_id,
                                       status="RUNNING", lifecycle_stage="active"),
            data=types.SimpleNamespace(params={}, metrics={}, tags={}))
        self.runs[obj.info.run_id] = obj
        self.active = obj
        try:
            yield obj
            obj.info.status = "FINISHED"
        finally:
            self.active = None

    def get_experiment_by_name(self, name): return self.experiments.get(name)
    def create_experiment(self, name):
        self.created += 1
        self.experiments[name] = types.SimpleNamespace(
            name=name, experiment_id="fake-exp-1", lifecycle_stage="active")
        return "fake-exp-1"
    def get_experiment(self, experiment_id):
        return next(x for x in self.experiments.values() if x.experiment_id == experiment_id)
    def get_run(self, run_id):
        obj = self.runs[run_id]
        if self.get_experiment(obj.info.experiment_id).lifecycle_stage == "deleted":
            raise RuntimeError("RESOURCE_DOES_NOT_EXIST_AFTER_EXPERIMENT_DELETE")
        if self.fail_readback and obj.info.lifecycle_stage == "active":
            obj.data.metrics["holdout_auc_roc"] = 999.0
        return obj
    def delete_run(self, run_id):
        if self.fail_cleanup: raise RuntimeError("injected delete failure")
        self.runs[run_id].info.lifecycle_stage = "deleted"
    def delete_experiment(self, experiment_id):
        experiment = self.get_experiment(experiment_id)
        experiment.lifecycle_stage = "deleted"
        experiment.name = "/Trash/" + experiment.name.rsplit("/", 1)[-1]
    def log_model(self, model, *, artifact_path=None, name=None, input_example=None):
        self.logged_model = model
        self.example = input_example
    def get_model_info(self, uri):
        if any(exp.lifecycle_stage == "deleted" for exp in self.experiments.values()):
            raise RuntimeError("MODEL_UNAVAILABLE_AFTER_EXPERIMENT_DELETE")
        return types.SimpleNamespace(signature="fake-signature",
                                     saved_input_example_info={"saved": True})
    def load_model(self, uri):
        if any(exp.lifecycle_stage == "deleted" for exp in self.experiments.values()):
            raise RuntimeError("MODEL_UNAVAILABLE_AFTER_EXPERIMENT_DELETE")
        self.model_load_calls += 1
        return self.logged_model


class TrackingTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeMlflow()
        self.previous_modules = {
            key: sys.modules.get(key, _MISSING)
            for key in ("mlflow", "mlflow.sklearn")
        }
        sys.modules["mlflow"] = self.fake
        sys.modules["mlflow.sklearn"] = self.fake.sklearn
        # The helper retains the MLflow module imported at module load.
        import hub_snippets.ml.mlflow_run.mlflow_run as helper
        self.original = helper.mlflow
        helper.mlflow = self.fake
        self.helper = helper
        self.runner = load("run_tracking.py")
        self.verifier = load("verify_tracking.py")

    def tearDown(self):
        self.helper.mlflow = self.original
        for key, previous in self.previous_modules.items():
            if previous is _MISSING:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = previous

    def test_success_exact_model_softdelete_and_external_verifier(self):
        q = request()
        out = self.runner.run_tracking(q, authority(q), FakeSpark(), run_id="candidate-1")
        self.assertEqual("PASS", out["status"], out["issues"])
        self.assertEqual("SOFT_DELETED", out["effect"]["cleanup"]["run"])
        self.assertEqual("SOFT_DELETED", out["effect"]["cleanup"]["experiment"])
        self.assertIsNotNone(self.fake.logged_model)
        self.assertIsNone(out["tracking_receipt"])
        check = self.verifier.verify_finalized(out, expected_request=q, expected_authorization=authority(q),
                                     expected_run_id="candidate-1",
                                     authenticated_user="test@example.com", client=self.fake)
        self.assertTrue(check["valid"], check)
        self.assertFalse(check["model_rechecked_after_cleanup"])
        self.assertEqual(2, self.fake.model_load_calls)
        changed = copy.deepcopy(q)
        changed["rows"][0]["feature"] += 1
        self.assertFalse(self.verifier.verify_finalized(out, expected_request=changed,
                                               expected_authorization=authority(changed),
                                               expected_run_id="candidate-1",
                                               authenticated_user="test@example.com",
                                               client=self.fake)["valid"])
        tamper = copy.deepcopy(out)
        tamper["effect"]["readback"]["positive_class_probabilities"][0] = 0.9
        self.assertFalse(self.verifier.verify_finalized(tamper, expected_request=q,
                                               expected_authorization=authority(q),
                                               expected_run_id="candidate-1",
                                               authenticated_user="test@example.com",
                                               client=self.fake)["valid"])
        self.assertEqual("deleted", self.fake.get_experiment("fake-exp-1").lifecycle_stage)

    def test_stale_authority_and_existing_active_run_block_before_create(self):
        q = request()
        stale = authority(q)
        stale["run_id"] = "other"
        out = self.runner.run_tracking(q, stale, FakeSpark(), run_id="candidate-1")
        self.assertEqual("BLOCKED", out["status"])
        self.assertEqual(0, self.fake.created)
        self.fake.active = object()
        out = self.runner.run_tracking(q, authority(q), FakeSpark(), run_id="candidate-1")
        self.assertEqual("BLOCKED", out["status"])
        self.assertEqual(0, self.fake.created)

    def test_readback_mismatch_and_cleanup_failure_never_pass(self):
        q = request()
        self.fake.fail_readback = True
        out = self.runner.run_tracking(q, authority(q), FakeSpark(), run_id="candidate-1")
        self.assertEqual("BLOCKED", out["status"])
        self.assertEqual("SOFT_DELETED", out["effect"]["cleanup"]["run"])
        self.assertEqual("SOFT_DELETED", out["effect"]["cleanup"]["experiment"])
        self.assertIsNotNone(out["effect"]["mlflow_run_id"])
        self.fake = FakeMlflow()
        self.helper.mlflow = self.fake
        sys.modules["mlflow"] = self.fake
        sys.modules["mlflow.sklearn"] = self.fake.sklearn
        self.fake.fail_cleanup = True
        out = self.runner.run_tracking(q, authority(q), FakeSpark(), run_id="candidate-1")
        self.assertEqual("BLOCKED", out["status"])
        self.assertEqual("UNKNOWN_RESIDUE", out["effect"]["residue"])
        self.assertEqual("UNKNOWN_RESIDUE", out["effect"]["cleanup"]["run"])
        self.assertTrue(out["effect"]["live_verification"]["valid"])

    def test_timeout_after_create_without_returned_id_is_unknown_residue(self):
        q = request()
        original_create = self.fake.create_experiment
        def lost_response(name):
            original_create(name)
            raise TimeoutError("response lost after create")
        self.fake.create_experiment = lost_response
        out = self.runner.run_tracking(q, authority(q), FakeSpark(), run_id="candidate-1")
        self.assertEqual("BLOCKED", out["status"])
        self.assertEqual("UNKNOWN_RESIDUE", out["effect"]["residue"])
        self.assertEqual("UNKNOWN_RESIDUE", out["effect"]["cleanup"]["experiment"])
        self.assertEqual(1, self.fake.created)

    def test_direct_compute_and_verifier_disable_ambient_autolog_before_each_fit(self):
        from sklearn.linear_model import LogisticRegression
        q = request()
        compute = load("run.py")
        verifier = load("verify.py")
        original_fit = LogisticRegression.fit
        seen = []
        def guarded_fit(model, *args, **kwargs):
            seen.append((self.fake.autolog_enabled, self.fake.sklearn_autolog_enabled))
            if any(seen[-1]):
                raise AssertionError("fit under ambient autolog")
            return original_fit(model, *args, **kwargs)
        with patch.object(LogisticRegression, "fit", guarded_fit):
            payload = compute.run(q, run_id="direct-ser09")
            self.assertEqual("PASS", payload["status"], payload["trace"]["blocking_issues"])
            self.fake.autolog_enabled = True
            self.fake.sklearn_autolog_enabled = True
            checked = verifier.verify(payload, expected_request=q, expected_run_id="direct-ser09")
        self.assertTrue(checked["valid"], checked)
        self.assertEqual([(False, False), (False, False)], seen)
        self.assertEqual(0, self.fake.created)

    def test_lookup_callback_cannot_mutate_authorized_input_or_target(self):
        q = request()
        auth = authority(q)
        trusted_q, trusted_auth = copy.deepcopy(q), copy.deepcopy(auth)
        def mutate_during_lookup(name):
            q["rows"][0]["feature"] = 999.0
            auth["target_experiment"] = "/Users/test@example.com/hub_lab/skills_delivery_deadbeef"
            return None
        self.fake.get_experiment_by_name = mutate_during_lookup
        out = self.runner.run_tracking(q, auth, FakeSpark(), run_id="candidate-1")
        self.assertEqual("PASS", out["status"], out["issues"])
        self.assertEqual(digest(trusted_q), out["effect"]["request_sha256"])
        self.assertEqual(digest(trusted_q), out["compute"]["trace"]["input_digest"])
        self.assertEqual(trusted_auth["target_experiment"], out["effect"]["target_experiment"])
        checked = self.verifier.verify_finalized(
            out, expected_request=trusted_q, expected_authorization=trusted_auth,
            expected_run_id="candidate-1", authenticated_user="test@example.com",
            client=self.fake)
        self.assertTrue(checked["valid"], checked)

    def test_independent_live_model_mismatch_blocks_and_still_cleans(self):
        import numpy as np
        q = request()
        original_load = self.fake.sklearn.load_model
        calls = [0]
        def divergent_on_second_read(uri):
            calls[0] += 1
            if calls[0] == 2:
                return types.SimpleNamespace(predict_proba=lambda X: np.zeros((len(X), 2)))
            return original_load(uri)
        self.fake.sklearn.load_model = divergent_on_second_read
        out = self.runner.run_tracking(q, authority(q), FakeSpark(), run_id="candidate-1")
        self.assertEqual("BLOCKED", out["status"])
        self.assertIn("INDEPENDENT_LIVE_VERIFICATION_FAILED", out["issues"][0])
        self.assertEqual("SOFT_DELETED", out["effect"]["cleanup"]["run"])
        self.assertEqual("SOFT_DELETED", out["effect"]["cleanup"]["experiment"])
        self.assertFalse(out["effect"]["live_verification"]["valid"])


if __name__ == "__main__":
    unittest.main()
