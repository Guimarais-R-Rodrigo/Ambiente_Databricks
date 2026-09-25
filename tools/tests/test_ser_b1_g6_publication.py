from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.skill_enforcement.real_campaigns.b1.g6_publication import minimal_publish as pub

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "tools/skill_enforcement/real_campaigns/b1/g6_publication"


class G6MinimalPublicationTests(unittest.TestCase):
    def manifest(self):
        return json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))

    def test_local_validation_passes(self):
        result = pub.validate_local()
        self.assertEqual("PASS", result["status"], result["issues"])
        self.assertEqual(17, result["object_count"])
        self.assertEqual(16, result["missing_count"])
        self.assertEqual(1, result["overwrite_count"])
        self.assertEqual(64, len(result["publisher_package_sha256"]))
        self.assertFalse(result["remote_access_performed"])
        self.assertFalse(result["remote_write_performed"])

    def test_manifest_is_closed_exactly_17_objects(self):
        manifest = self.manifest()
        entries = manifest["entries"]
        self.assertEqual(17, len(entries))
        self.assertEqual(17, len({e["object_id"] for e in entries}))
        self.assertEqual(17, len({e["remote_relative_path"] for e in entries}))
        self.assertFalse(manifest["full_republish"])
        self.assertEqual("REMOTE_PACKAGE_WRITE", manifest["effect"])
        self.assertEqual("NOT_AUTHORIZED", manifest["execution_status"])

    def test_notebook_mapping_is_explicit(self):
        entries = self.manifest()["entries"]
        notebooks = [e for e in entries if e["object_kind"] == "NOTEBOOK"]
        self.assertEqual(1, len(notebooks))
        row = notebooks[0]
        self.assertTrue(row["rendered_path"].endswith("exemplo_domain_context.py"))
        self.assertTrue(row["remote_relative_path"].endswith("exemplo_domain_context"))
        self.assertFalse(row["remote_relative_path"].endswith(".py"))

    def test_only_policy_can_overwrite(self):
        entries = self.manifest()["entries"]
        overwrite = [e for e in entries if e["precondition"]["kind"] == "REMOTE_NORMALIZED_SHA256_EQUALS"]
        self.assertEqual(["policy"], [e["object_id"] for e in overwrite])

    def test_file_import_uses_raw_and_notebook_uses_source(self):
        entries = self.manifest()["entries"]
        file_row = next(e for e in entries if e["object_id"] == "ser03-run")
        policy = next(e for e in entries if e["object_id"] == "policy")
        notebook = next(e for e in entries if e["object_kind"] == "NOTEBOOK")
        file_argv = pub.build_import_argv("FREE", "/Users/u/" + file_row["remote_relative_path"], ROOT / file_row["rendered_path"], file_row)
        policy_argv = pub.build_import_argv("FREE", "/Users/u/" + policy["remote_relative_path"], ROOT / policy["rendered_path"], policy)
        notebook_argv = pub.build_import_argv("FREE", "/Users/u/" + notebook["remote_relative_path"], ROOT / notebook["rendered_path"], notebook)
        self.assertIn("RAW", file_argv)
        self.assertNotIn("AUTO", file_argv)
        self.assertNotIn("--overwrite", file_argv)
        self.assertIn("--overwrite", policy_argv)
        self.assertEqual(["--format", "SOURCE", "--language", "PYTHON"], notebook_argv[-4:])

    def test_workspace_listing_accepts_cli_list_shape(self):
        rows = pub._parse_workspace_listing('[{"path":"/Users/u/a","object_type":"FILE"}]')
        self.assertEqual("/Users/u/a", rows[0]["path"])

    def test_workspace_listing_accepts_api_objects_shape(self):
        rows = pub._parse_workspace_listing('{"objects":[{"path":"/Users/u/a","object_type":"FILE"}]}')
        self.assertEqual("/Users/u/a", rows[0]["path"])

    def test_workspace_listing_accepts_empty_object(self):
        self.assertEqual([], pub._parse_workspace_listing("{}"))

    def test_workspace_listing_rejects_unsupported_shape(self):
        with self.assertRaisesRegex(RuntimeError, "WORKSPACE_LIST_UNSUPPORTED_SHAPE"):
            pub._parse_workspace_listing('{"unexpected":[]}')

    def test_missing_proof_accepts_exact_absence(self):
        target = "/Users/u/.assistant/skills/x/run.py"
        with patch.object(pub, "_status", return_value=(1, "", "not found")), patch.object(
            pub, "_run_dbx", return_value=(0, json.dumps([{"path":"/Users/u/.assistant/skills/x/other.py","object_type":"FILE"}]), "")
        ):
            pub._assert_missing("FREE", target)

    def test_missing_proof_rejects_listed_target(self):
        target = "/Users/u/.assistant/skills/x/run.py"
        with patch.object(pub, "_status", return_value=(1, "", "not found")), patch.object(
            pub, "_run_dbx", return_value=(0, json.dumps([{"path":target,"object_type":"FILE"}]), "")
        ):
            with self.assertRaisesRegex(RuntimeError, "EXPECTED_MISSING_BUT_LISTED"):
                pub._assert_missing("FREE", target)

    def test_missing_proof_handles_missing_parent_via_existing_ancestor(self):
        target = "/Users/u/.assistant/hub_scripts/domain_context/README.md"
        parent = "/Users/u/.assistant/hub_scripts/domain_context"
        grandparent = "/Users/u/.assistant/hub_scripts"
        def status_side(_profile, path):
            if path in {target, parent}:
                return (1, "", "not found")
            return (0, json.dumps({"path": path, "object_type": "DIRECTORY"}), "")
        def dbx_side(_profile, *args):
            path = args[2]
            if path == parent:
                return (1, "", "parent missing")
            if path == grandparent:
                return (0, json.dumps([{"path":grandparent + "/other","object_type":"DIRECTORY"}]), "")
            raise AssertionError(path)
        with patch.object(pub, "_status", side_effect=status_side), patch.object(pub, "_run_dbx", side_effect=dbx_side):
            pub._assert_missing("FREE", target)

    def test_missing_proof_fails_closed_if_parent_exists_but_listing_fails(self):
        target = "/Users/u/.assistant/skills/x/run.py"
        parent = "/Users/u/.assistant/skills/x"
        def status_side(_profile, path):
            if path == target:
                return (1, "", "not found")
            if path == parent:
                return (0, json.dumps({"path":parent,"object_type":"DIRECTORY"}), "")
            raise AssertionError(path)
        with patch.object(pub, "_status", side_effect=status_side), patch.object(
            pub, "_run_dbx", return_value=(1, "", "transport")
        ):
            with self.assertRaisesRegex(RuntimeError, "MISSING_PARENT_LIST_FAILED"):
                pub._assert_missing("FREE", target)

    def test_missing_proof_rejects_existing_target(self):
        with patch.object(pub, "_status", return_value=(0, "{}", "")):
            with self.assertRaisesRegex(RuntimeError, "EXPECTED_MISSING_BUT_EXISTS"):
                pub._assert_missing("FREE", "/Users/u/a")

    def test_parent_directory_requires_directory_status(self):
        target = "/Users/u/.assistant/skills/x/run.py"
        parent = "/Users/u/.assistant/skills/x"
        with patch.object(pub, "_status", return_value=(0, json.dumps({"path":parent,"object_type":"DIRECTORY"}), "")):
            pub._assert_parent_directory_exists("FREE", target)
        with patch.object(pub, "_status", return_value=(0, json.dumps({"path":parent,"object_type":"FILE"}), "")):
            with self.assertRaisesRegex(RuntimeError, "PARENT_NOT_DIRECTORY"):
                pub._assert_parent_directory_exists("FREE", target)

    def test_readback_type_contract(self):
        file_path = "/Users/u/a.py"
        nb_path = "/Users/u/nb"
        with patch.object(pub, "_status", return_value=(0, json.dumps({"path":file_path,"object_type":"FILE"}), "")):
            pub._assert_remote_object_type("FREE", file_path, "FILE")
        with patch.object(pub, "_status", return_value=(0, json.dumps({"path":nb_path,"object_type":"NOTEBOOK","language":"PYTHON"}), "")):
            pub._assert_remote_object_type("FREE", nb_path, "NOTEBOOK")
        with patch.object(pub, "_status", return_value=(0, json.dumps({"path":file_path,"object_type":"NOTEBOOK","language":"PYTHON"}), "")):
            with self.assertRaisesRegex(RuntimeError, "READBACK_OBJECT_TYPE_MISMATCH"):
                pub._assert_remote_object_type("FREE", file_path, "FILE")

    def test_file_export_uses_raw(self):
        calls = []
        with patch.object(pub, "_run_dbx", side_effect=lambda _profile,*args:(calls.append(args) or (0,json.dumps({"content":"YQ=="}),""))):
            self.assertEqual(b"a", pub._export("FREE", "/Users/u/a.py", "FILE"))
        self.assertIn("RAW", calls[0])

    def test_authorization_v2_binds_manifest_package_order_and_target(self):
        object_ids = [e["object_id"] for e in self.manifest()["entries"]]
        good = {
            "schema_version": pub.AUTH_SCHEMA,
            "decision": "AUTHORIZED",
            "manifest_sha256": pub._manifest_sha256(),
            "publisher_package_sha256": pub._publisher_package_sha256(),
            "effect": "REMOTE_PACKAGE_WRITE",
            "target": {"profile": "FREE", "host": pub.EXPECTED_HOST + "/"},
            "allowed_object_ids": object_ids,
            "one_write_attempt": True,
            "authorization_ref": "issue#114:comment#future",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text(json.dumps(good), encoding="utf-8")
            self.assertEqual("AUTHORIZED", pub._validate_authorization(path, pub._manifest_sha256(), pub._publisher_package_sha256(), object_ids)["decision"])
            bad = dict(good)
            bad["allowed_object_ids"] = list(reversed(object_ids))
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "AUTH_OBJECT_SEQUENCE"):
                pub._validate_authorization(path, pub._manifest_sha256(), pub._publisher_package_sha256(), object_ids)

    def test_authorization_rejects_package_digest_drift(self):
        object_ids = [e["object_id"] for e in self.manifest()["entries"]]
        payload = {
            "schema_version": pub.AUTH_SCHEMA,
            "decision": "AUTHORIZED",
            "manifest_sha256": pub._manifest_sha256(),
            "publisher_package_sha256": "0" * 64,
            "effect": "REMOTE_PACKAGE_WRITE",
            "target": {"profile": "FREE", "host": pub.EXPECTED_HOST},
            "allowed_object_ids": object_ids,
            "one_write_attempt": True,
            "authorization_ref": "issue#114:comment#future",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "AUTH_PUBLISHER_PACKAGE_BINDING"):
                pub._validate_authorization(path, pub._manifest_sha256(), pub._publisher_package_sha256(), object_ids)

    def test_authorization_record_must_be_external(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "AUTHORIZATION_MUST_BE_EXTERNAL"):
                pub._assert_external_file(path, "AUTHORIZATION")

    def test_write_authorization_consumption_is_atomic(self):
        payload = {"authorization_ref":"issue#114:comment#future","manifest_sha256":pub._manifest_sha256(),"effect":"REMOTE_PACKAGE_WRITE"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text("{}", encoding="utf-8")
            self.assertEqual(64, len(pub._consume_write_authorization(path, payload, pub._publisher_package_sha256())))
            with self.assertRaisesRegex(RuntimeError, "AUTHORIZATION_ALREADY_CONSUMED"):
                pub._consume_write_authorization(path, payload, pub._publisher_package_sha256())

    def test_target_resolution_rejects_corporate_identity(self):
        auth = {"status":"ok","details":{"configuration":{"profile":{"value":"FREE"},"host":{"value":pub.EXPECTED_HOST}}}}
        user = {"userName":"corp.caixa@example.com"}
        with patch.object(pub, "_run_dbx", side_effect=[(0,json.dumps(auth),""),(0,json.dumps(user),"")]):
            with self.assertRaisesRegex(RuntimeError, "CURRENT_USER_LOOKS_CORPORATE"):
                pub._resolve_target("FREE", pub.EXPECTED_HOST)


    def _write_auth_v2(self, directory: Path) -> Path:
        object_ids = [e["object_id"] for e in self.manifest()["entries"]]
        payload = {
            "schema_version": pub.AUTH_SCHEMA,
            "decision": "AUTHORIZED",
            "manifest_sha256": pub._manifest_sha256(),
            "publisher_package_sha256": pub._publisher_package_sha256(),
            "effect": "REMOTE_PACKAGE_WRITE",
            "target": {"profile": "FREE", "host": pub.EXPECTED_HOST},
            "allowed_object_ids": object_ids,
            "one_write_attempt": True,
            "authorization_ref": "issue#114:comment#future",
        }
        path = directory / "auth.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_execute_mocked_full_success_covers_17_records(self):
        manifest = self.manifest()
        by_remote = {e["remote_relative_path"]: e for e in manifest["entries"]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            auth = self._write_auth_v2(root)
            evidence = root / "evidence"

            def exported(_profile, remote, _kind):
                rel = remote.split("/.assistant/", 1)[1]
                key = ".assistant/" + rel
                entry = by_remote[key]
                return (ROOT / entry["rendered_path"]).read_bytes()

            with patch.object(pub, "_resolve_target", return_value=("/Users/u", {"profile":"FREE","host":pub.EXPECTED_HOST,"current_user_resolved":True})), \
                 patch.object(pub, "_assert_parent_directory_exists"), \
                 patch.object(pub, "_assert_missing"), \
                 patch.object(pub, "_assert_stale_hash", return_value="b68d"), \
                 patch.object(pub, "_consume_write_authorization", return_value="c" * 64) as consume, \
                 patch.object(pub, "_run_import", return_value=(0, "", "")), \
                 patch.object(pub, "_assert_remote_object_type"), \
                 patch.object(pub, "_export", side_effect=exported):
                result = pub.execute(auth, evidence)

            self.assertEqual("PASS", result["status"])
            self.assertTrue(result["authorization_consumed"])
            self.assertEqual(1, consume.call_count)
            self.assertEqual(17, len(result["records"]))
            self.assertEqual(17, sum(r["write_started"] is True for r in result["records"]))
            self.assertEqual(17, sum(r["write_exit_code"] == 0 for r in result["records"]))
            self.assertEqual(17, sum(r["verification"] == "PASS" for r in result["records"]))
            self.assertEqual(16, sum(r["effect_status"] == "CREATED" for r in result["records"]))
            self.assertEqual(1, sum(r["effect_status"] == "UPDATED" for r in result["records"]))

    def test_execute_preflight_failure_does_not_consume_write_authorization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            auth = self._write_auth_v2(root)
            evidence = root / "evidence"
            with patch.object(pub, "_resolve_target", return_value=("/Users/u", {"profile":"FREE","host":pub.EXPECTED_HOST,"current_user_resolved":True})), \
                 patch.object(pub, "_assert_parent_directory_exists", side_effect=RuntimeError("PARENT_NOT_DIRECTORY")), \
                 patch.object(pub, "_consume_write_authorization") as consume:
                result = pub.execute(auth, evidence)
            self.assertEqual("FAIL", result["status"])
            self.assertIn("REMOTE_PRECONDITION:PARENT_NOT_DIRECTORY", result["first_failure"])
            self.assertFalse(result["authorization_consumed"])
            self.assertEqual(0, consume.call_count)
            self.assertEqual([], result["records"])

    def test_execute_exception_after_write_start_marks_unknown_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            auth = self._write_auth_v2(root)
            evidence = root / "evidence"
            with patch.object(pub, "_resolve_target", return_value=("/Users/u", {"profile":"FREE","host":pub.EXPECTED_HOST,"current_user_resolved":True})), \
                 patch.object(pub, "_assert_parent_directory_exists"), \
                 patch.object(pub, "_assert_missing"), \
                 patch.object(pub, "_assert_stale_hash", return_value="b68d"), \
                 patch.object(pub, "_consume_write_authorization", return_value="c" * 64), \
                 patch.object(pub, "_run_import", side_effect=OSError("transport vanished")):
                result = pub.execute(auth, evidence)
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(result["authorization_consumed"])
            self.assertEqual(1, len(result["records"]))
            self.assertTrue(result["records"][0]["write_started"])
            self.assertEqual("UNKNOWN", result["records"][0]["effect_status"])
            self.assertIn("transport vanished", result["first_failure"])

    def test_target_resolution_rejects_auth_describe_error_status(self):
        auth = {"status":"error","details":{"configuration":{"profile":{"value":"FREE"},"host":{"value":pub.EXPECTED_HOST}}}}
        with patch.object(pub, "_run_dbx", return_value=(0, json.dumps(auth), "")):
            with self.assertRaisesRegex(RuntimeError, "AUTH_DESCRIBE_STATUS_ERROR"):
                pub._resolve_target("FREE", pub.EXPECTED_HOST)

    def test_evidence_must_be_outside_repo_and_new(self):
        with self.assertRaisesRegex(RuntimeError, "EVIDENCE_MUST_BE_EXTERNAL"):
            pub._evidence_dir(ROOT / "tmp-evidence-forbidden")


if __name__ == "__main__":
    unittest.main()
