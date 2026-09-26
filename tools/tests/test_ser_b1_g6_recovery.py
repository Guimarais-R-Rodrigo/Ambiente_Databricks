from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tools.skill_enforcement.real_campaigns.b1.g6_recovery import residual_probe_recovery as rec

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "tools/skill_enforcement/real_campaigns/b1/g6_recovery"


class G6ProbeRecoveryTests(unittest.TestCase):
    def manifest(self):
        return json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))

    def test_local_validation_passes(self):
        result = rec.validate_local()
        self.assertEqual("PASS", result["status"], result["issues"])
        self.assertEqual(2, result["object_count"])
        self.assertEqual(64, len(result["manifest_sha256"]))
        self.assertEqual(64, len(result["recovery_package_sha256"]))
        self.assertEqual(
            rec.EXPECTED_BASE_HTTP11_PACKAGE_SHA256,
            result["base_http11_publisher_package_sha256"],
        )
        self.assertFalse(result["remote_access_performed"])
        self.assertFalse(result["remote_write_performed"])

    def test_manifest_is_closed_to_ser05_write(self):
        manifest = self.manifest()
        rows = {row["object_id"]: row for row in manifest["objects"]}
        self.assertEqual({"ser03-free-probe", "ser05-free-probe"}, set(rows))
        self.assertFalse(rows["ser03-free-probe"]["write_allowed"])
        self.assertTrue(rows["ser05-free-probe"]["write_allowed"])
        contract = manifest["write_contract"]
        self.assertEqual(["ser05-free-probe"], contract["allowed_object_ids"])
        self.assertFalse(contract["overwrite"])
        self.assertTrue(contract["one_write_attempt"])
        self.assertFalse(contract["automatic_retry"])
        self.assertFalse(contract["mkdir_allowed"])
        self.assertFalse(contract["cleanup_allowed"])

    def test_source_blobs_are_bound(self):
        for row in self.manifest()["objects"]:
            path = ROOT / row["source_path"]
            self.assertEqual(row["expected_git_blob_sha1"], rec._git_blob_sha1(path.read_bytes()))

    def _remote_fixture(self, *, ser05_present=False, ser05_hash=None):
        manifest = self.manifest()
        entries = rec._entries(manifest)
        home = "/Users/u"
        root = home + "/" + manifest["remote_root_suffix"]
        ser03 = root + "/" + entries["ser03-free-probe"]["remote_name"]
        ser05 = root + "/" + entries["ser05-free-probe"]["remote_name"]
        rows = [
            {"path": ser03, "object_type": "NOTEBOOK", "language": "PYTHON"},
        ]
        if ser05_present:
            rows.append({"path": ser05, "object_type": "NOTEBOOK", "language": "PYTHON"})
        hashes = {
            ser03: rec._local_normalized_hash(entries["ser03-free-probe"]),
        }
        if ser05_present:
            hashes[ser05] = ser05_hash or rec._local_normalized_hash(entries["ser05-free-probe"])
        return home, root, ser03, ser05, rows, hashes

    def test_reconcile_requires_ser03_exact_and_allows_ser05_absent(self):
        home, root, ser03, ser05, rows, hashes = self._remote_fixture()
        with patch.object(rec.base, "_resolve_target", return_value=(home, {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True})),              patch.object(rec, "_list_exact_root", return_value=rows),              patch.object(rec, "_remote_notebook_hash", side_effect=lambda _p, path: hashes[path]):
            result = rec._reconcile_remote()
        self.assertEqual("EXACT", result["ser03"]["state"])
        self.assertEqual("ABSENT", result["ser05"]["state"])
        self.assertEqual("CREATE", result["ser05"]["action"])

    def test_reconcile_accepts_ser05_exact_without_write(self):
        home, root, ser03, ser05, rows, hashes = self._remote_fixture(ser05_present=True)
        with patch.object(rec.base, "_resolve_target", return_value=(home, {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True})),              patch.object(rec, "_list_exact_root", return_value=rows),              patch.object(rec, "_remote_notebook_hash", side_effect=lambda _p, path: hashes[path]):
            result = rec._reconcile_remote()
        self.assertEqual("ALREADY_CORRECT", result["ser05"]["action"])

    def test_reconcile_fails_if_ser03_missing(self):
        home, root, ser03, ser05, rows, hashes = self._remote_fixture()
        with patch.object(rec.base, "_resolve_target", return_value=(home, {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True})),              patch.object(rec, "_list_exact_root", return_value=[]):
            with self.assertRaisesRegex(RuntimeError, "SER03_REQUIRED_OBJECT_MISSING"):
                rec._reconcile_remote()

    def test_reconcile_fails_on_ser03_divergence(self):
        home, root, ser03, ser05, rows, hashes = self._remote_fixture()
        hashes[ser03] = "0" * 64
        with patch.object(rec.base, "_resolve_target", return_value=(home, {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True})),              patch.object(rec, "_list_exact_root", return_value=rows),              patch.object(rec, "_remote_notebook_hash", side_effect=lambda _p, path: hashes[path]):
            with self.assertRaisesRegex(RuntimeError, "SER03_REQUIRED_OBJECT_DIVERGENT"):
                rec._reconcile_remote()

    def test_reconcile_fails_on_ser05_divergence(self):
        home, root, ser03, ser05, rows, hashes = self._remote_fixture(
            ser05_present=True, ser05_hash="0" * 64
        )
        with patch.object(rec.base, "_resolve_target", return_value=(home, {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True})),              patch.object(rec, "_list_exact_root", return_value=rows),              patch.object(rec, "_remote_notebook_hash", side_effect=lambda _p, path: hashes[path]):
            with self.assertRaisesRegex(RuntimeError, "SER05_EXISTING_OBJECT_DIVERGENT"):
                rec._reconcile_remote()

    def test_reconcile_fails_on_unexpected_object(self):
        home, root, ser03, ser05, rows, hashes = self._remote_fixture()
        rows.append({"path": root + "/unexpected", "object_type": "NOTEBOOK"})
        with patch.object(rec.base, "_resolve_target", return_value=(home, {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True})),              patch.object(rec, "_list_exact_root", return_value=rows):
            with self.assertRaisesRegex(RuntimeError, "UNEXPECTED_ROOT_OBJECT"):
                rec._reconcile_remote()

    def _auth_payload(self, local):
        manifest = self.manifest()
        ser05 = rec._entries(manifest)["ser05-free-probe"]
        return {
            "schema_version": rec.AUTH_SCHEMA,
            "decision": "AUTHORIZED",
            "authorization_ref": "issue#114:comment#unit",
            "action": "G6_SER05_RESIDUAL_DIRECT_HTTP11_CREATE",
            "effect": "TEMPORARY_WORKSPACE_OBJECT_CREATE",
            "one_write_attempt": True,
            "manifest_sha256": local["manifest_sha256"],
            "recovery_package_sha256": local["recovery_package_sha256"],
            "base_http11_publisher_package_sha256": rec.EXPECTED_BASE_HTTP11_PACKAGE_SHA256,
            "ser05_source_git_blob_sha1": ser05["expected_git_blob_sha1"],
            "allowed_object_ids": ["ser05-free-probe"],
            "remote_root_suffix": "ser-b1-g6-tests/08c2a93c4c9d",
            "target": {"profile": "FREE", "host": rec.EXPECTED_HOST},
        }

    def test_authorization_binds_exact_residual(self):
        local = rec.validate_local()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "authorization.json"
            path.write_text(json.dumps(self._auth_payload(local)), encoding="utf-8")
            payload = rec._validate_authorization(
                path,
                manifest_sha256=local["manifest_sha256"],
                recovery_package_sha256=local["recovery_package_sha256"],
                ser05_source_blob=self.manifest()["objects"][1]["expected_git_blob_sha1"],
            )
        self.assertEqual(["ser05-free-probe"], payload["allowed_object_ids"])

    def test_authorization_rejects_package_drift(self):
        local = rec.validate_local()
        payload = self._auth_payload(local)
        payload["recovery_package_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "authorization.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "AUTH_RECOVERY_PACKAGE_BINDING"):
                rec._validate_authorization(
                    path,
                    manifest_sha256=local["manifest_sha256"],
                    recovery_package_sha256=local["recovery_package_sha256"],
                    ser05_source_blob=self.manifest()["objects"][1]["expected_git_blob_sha1"],
                )

    def test_execute_already_correct_does_not_acquire_token_or_consume(self):
        local = rec.validate_local()
        auth = self._auth_payload(local)
        reconciliation = {
            "status": "PASS",
            "target": {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True},
            "remote_root": "/Users/u/ser-b1-g6-tests/08c2a93c4c9d",
            "root_object_count": 2,
            "ser03": {"state": "EXACT"},
            "ser05": {"state": "EXACT", "action": "ALREADY_CORRECT"},
            "remote_write_performed": False,
        }
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            auth_path = td / "authorization.json"
            auth_path.write_text(json.dumps(auth), encoding="utf-8")
            evidence = td / "evidence"
            with patch.object(rec, "_reconcile_remote", return_value=reconciliation),                  patch.object(rec.base, "_acquire_u2m_access_token") as token,                  patch.object(rec, "_consume_authorization") as consume:
                result = rec.execute(auth_path, evidence)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("ALREADY_CORRECT", result["effect_status"])
        self.assertFalse(result["authorization_consumed"])
        token.assert_not_called()
        consume.assert_not_called()

    def test_token_failure_does_not_consume_or_write(self):
        local = rec.validate_local()
        auth = self._auth_payload(local)
        reconciliation = {
            "status": "PASS",
            "target": {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True},
            "remote_root": "/Users/u/ser-b1-g6-tests/08c2a93c4c9d",
            "root_object_count": 1,
            "ser03": {"state": "EXACT"},
            "ser05": {"state": "ABSENT", "action": "CREATE", "remote_path": "/Users/u/ser-b1-g6-tests/08c2a93c4c9d/ser05_l2_free_probe"},
            "remote_write_performed": False,
        }
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            auth_path = td / "authorization.json"
            auth_path.write_text(json.dumps(auth), encoding="utf-8")
            evidence = td / "evidence"
            with patch.object(rec, "_reconcile_remote", return_value=reconciliation),                  patch.object(rec.base, "_acquire_u2m_access_token", side_effect=RuntimeError("AUTH_TOKEN_FAILED")),                  patch.object(rec, "_consume_authorization") as consume,                  patch.object(rec.base, "_run_direct_http_import") as writer:
                result = rec.execute(auth_path, evidence)
        self.assertEqual("FAIL", result["status"])
        self.assertFalse(result["authorization_consumed"])
        self.assertFalse(result["write_started"])
        consume.assert_not_called()
        writer.assert_not_called()

    def test_execute_create_uses_one_http_call_and_readback(self):
        local = rec.validate_local()
        auth = self._auth_payload(local)
        remote_path = "/Users/u/ser-b1-g6-tests/08c2a93c4c9d/ser05_l2_free_probe"
        pre = {
            "status": "PASS",
            "target": {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True},
            "remote_root": "/Users/u/ser-b1-g6-tests/08c2a93c4c9d",
            "root_object_count": 1,
            "ser03": {"state": "EXACT"},
            "ser05": {"state": "ABSENT", "action": "CREATE", "remote_path": remote_path},
            "remote_write_performed": False,
        }
        final = {
            **pre,
            "root_object_count": 2,
            "ser05": {"state": "EXACT", "action": "ALREADY_CORRECT", "remote_path": remote_path},
        }
        ser05 = rec._entries(self.manifest())["ser05-free-probe"]
        local_hash = rec._local_normalized_hash(ser05)
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            auth_path = td / "authorization.json"
            auth_path.write_text(json.dumps(auth), encoding="utf-8")
            evidence = td / "evidence"
            with patch.object(rec, "_reconcile_remote", side_effect=[pre, pre, final]),                  patch.object(rec.base, "_acquire_u2m_access_token", return_value="unit-token"),                  patch.object(rec, "_consume_authorization", return_value="a" * 64) as consume,                  patch.object(rec.base, "_run_direct_http_import", return_value=(0, "", "")) as writer,                  patch.object(rec, "_remote_notebook_hash", return_value=local_hash):
                result = rec.execute(auth_path, evidence)
        self.assertEqual("PASS", result["status"])
        self.assertTrue(result["authorization_consumed"])
        self.assertTrue(result["write_started"])
        self.assertEqual("CREATED", result["effect_status"])
        self.assertEqual("PASS", result["verification"])
        consume.assert_called_once()
        writer.assert_called_once()

    def test_exception_after_write_start_is_unknown_and_no_retry(self):
        local = rec.validate_local()
        auth = self._auth_payload(local)
        remote_path = "/Users/u/ser-b1-g6-tests/08c2a93c4c9d/ser05_l2_free_probe"
        pre = {
            "status": "PASS",
            "target": {"profile": "FREE", "host": rec.EXPECTED_HOST, "current_user_resolved": True},
            "remote_root": "/Users/u/ser-b1-g6-tests/08c2a93c4c9d",
            "root_object_count": 1,
            "ser03": {"state": "EXACT"},
            "ser05": {"state": "ABSENT", "action": "CREATE", "remote_path": remote_path},
            "remote_write_performed": False,
        }
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            auth_path = td / "authorization.json"
            auth_path.write_text(json.dumps(auth), encoding="utf-8")
            evidence = td / "evidence"
            with patch.object(rec, "_reconcile_remote", side_effect=[pre, pre]),                  patch.object(rec.base, "_acquire_u2m_access_token", return_value="unit-token"),                  patch.object(rec, "_consume_authorization", return_value="a" * 64),                  patch.object(rec.base, "_run_direct_http_import", side_effect=RuntimeError("DIRECT_HTTP_REQUEST_FAILED:TimeoutError")) as writer:
                result = rec.execute(auth_path, evidence)
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(result["authorization_consumed"])
        self.assertTrue(result["write_started"])
        self.assertEqual("UNKNOWN", result["effect_status"])
        writer.assert_called_once()

    def test_source_has_no_cli_import_mkdir_or_delete_transport(self):
        source = (HERE / "residual_probe_recovery.py").read_text(encoding="utf-8")
        self.assertNotIn('"workspace", "import"', source)
        self.assertNotIn('"workspace", "mkdirs"', source)
        self.assertNotIn('"workspace", "delete"', source)
        self.assertIn("base._run_direct_http_import", source)

    def test_recovery_does_not_modify_frozen_g6_files(self):
        manifest = self.manifest()
        self.assertEqual(
            "c11c2dff07f0f7595ed545f32990e5d54f1fd583",
            manifest["g6_original_freeze_sha"],
        )


if __name__ == "__main__":
    unittest.main()
