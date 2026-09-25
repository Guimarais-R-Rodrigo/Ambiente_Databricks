from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.skill_enforcement.real_campaigns.b1.g6_publication import minimal_publish as pub

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "tools/skill_enforcement/real_campaigns/b1/g6_publication"

REQUIRED_ADVERSARIAL_TEST_METHODS = {
    "WORKSPACE_LIST_INVALID_JSON": "test_workspace_listing_rejects_invalid_json",
    "WORKSPACE_LIST_ROW_NOT_OBJECT": "test_workspace_listing_rejects_non_object_row",
    "AUTHORIZATION_RECORD_SYMLINK": "test_authorization_record_symlink_is_rejected",
    "AUTHORIZATION_MANIFEST_DIGEST_DRIFT": "test_authorization_rejects_manifest_digest_drift",
    "AUTHORIZATION_PUBLISHER_DIGEST_DRIFT": "test_authorization_rejects_package_digest_drift",
    "AUTHORIZATION_EXACT_OBJECT_ORDER": "test_authorization_v2_binds_manifest_package_order_and_target",
    "AUTHORIZATION_ATOMIC_SINGLE_USE": "test_write_authorization_consumption_is_atomic",
    "MISSING_PARENT_RECURSION": "test_missing_proof_handles_missing_parent_via_existing_ancestor",
    "MISSING_PARENT_LIST_FAILURE": "test_missing_proof_fails_closed_if_parent_exists_but_listing_fails",
    "MISSING_LISTED_TARGET": "test_missing_proof_rejects_listed_target",
    "API_PUT_JSON_IMPORT": "test_import_uses_api_put_json_base64",
    "FILE_AUTO_EXPORT_AFTER_TYPE_PROOF": "test_file_export_uses_auto_after_type_contract",
    "CONVERGENT_POLICY_CLASSIFIER": "test_policy_classifier_accepts_stale_or_exact_local",
    "READBACK_OBJECT_TYPE": "test_readback_type_contract",
    "PREFLIGHT_DOES_NOT_CONSUME": "test_execute_preflight_failure_does_not_consume_write_authorization",
    "UNKNOWN_AFTER_WRITE_START": "test_execute_exception_after_write_start_marks_unknown_and_stops",
    "MOCKED_FULL_SUCCESS": "test_execute_mocked_full_success_covers_manifest_records",
    "RESIDUAL_MANIFEST_BINDING": "test_manifest_matches_reconciled_residual_exactly",
    "CONVERGENT_CREATE_SKIP": "test_create_classifier_skips_exact_existing_content",
    "CONVERGENT_CREATE_DIVERGENCE": "test_create_classifier_rejects_divergent_existing_content",
    "CONVERGENT_EXECUTION_SKIP": "test_execute_skips_already_correct_without_consuming_for_that_entry",
}


class G6MinimalPublicationTests(unittest.TestCase):
    def manifest(self):
        return json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))

    def test_local_validation_passes(self):
        result = pub.validate_local()
        self.assertEqual("PASS", result["status"], result["issues"])
        manifest = self.manifest()
        self.assertEqual(manifest["expected_object_count"], result["object_count"])
        self.assertEqual(manifest["missing_object_count"], result["missing_count"])
        self.assertEqual(manifest["overwrite_object_count"], result["overwrite_count"])
        self.assertEqual(64, len(result["publisher_package_sha256"]))
        self.assertFalse(result["remote_access_performed"])
        self.assertFalse(result["remote_write_performed"])

    def test_manifest_is_closed_and_declared_counts_match(self):
        manifest = self.manifest()
        entries = manifest["entries"]
        self.assertEqual(manifest["expected_object_count"], len(entries))
        self.assertEqual(manifest["missing_object_count"], sum(e["precondition"]["kind"] in pub.CREATE_PRECONDITION_KINDS for e in entries))
        self.assertEqual(manifest["overwrite_object_count"], sum(e["precondition"]["kind"] in pub.OVERWRITE_PRECONDITION_KINDS for e in entries))
        self.assertEqual(len(entries), len({e["object_id"] for e in entries}))
        self.assertEqual(len(entries), len({e["remote_relative_path"] for e in entries}))
        self.assertFalse(manifest["full_republish"])
        self.assertEqual("REMOTE_PACKAGE_WRITE", manifest["effect"])
        self.assertEqual("NOT_AUTHORIZED", manifest["execution_status"])

    def test_manifest_matches_reconciled_residual_exactly(self):
        manifest = self.manifest()
        expected_ids = [
            "domain-context-init",
            "domain-context-example",
            "domain-context-release",
            "domain-context-schema",
            "ser03-contract",
            "ser03-input-schema",
            "ser03-release-manifest",
            "ser03-scripts-readme",
            "ser03-preflight",
            "ser03-run",
            "ser03-verify",
            "ser05-contract",
            "ser05-input-schema",
            "ser05-scripts-readme",
            "ser05-preflight",
            "policy",
        ]
        self.assertEqual("SER-B1-G6-CONVERGENT-PUBLISH-R7-1", manifest["package_id"])
        self.assertEqual("SER-B1-G6-CONVERGENT-PUBLISH-MANIFEST-2", manifest["schema_version"])
        self.assertEqual(expected_ids, [e["object_id"] for e in manifest["entries"]])
        self.assertEqual(16, manifest["expected_object_count"])
        self.assertEqual(15, manifest["missing_object_count"])
        self.assertEqual(1, manifest["overwrite_object_count"])
        residual = manifest["residual_source"]
        self.assertEqual(["domain-context-readme"], residual["already_correct_object_ids"])
        self.assertEqual("SIMPLE_RESIDUAL", residual["remote_residual_state"])
        self.assertEqual(
            "d255398df799f0262872db4b5b327cb4dc3b9be67178746923a009138f702435",
            residual["sanitized_evidence_sha256"],
        )
        self.assertNotIn("domain-context-readme", expected_ids)

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
        overwrite = [e for e in entries if e["precondition"]["kind"] in pub.OVERWRITE_PRECONDITION_KINDS]
        self.assertEqual(["policy"], [e["object_id"] for e in overwrite])

    def test_import_uses_api_put_json_base64(self):
        entries = self.manifest()["entries"]
        file_row = next(e for e in entries if e["object_id"] == "ser03-run")
        policy = next(e for e in entries if e["object_id"] == "policy")
        notebook = next(e for e in entries if e["object_kind"] == "NOTEBOOK")

        file_argv = pub.build_import_argv(
            "FREE", "/Users/u/" + file_row["remote_relative_path"],
            ROOT / file_row["rendered_path"], file_row, "CREATE"
        )
        policy_argv = pub.build_import_argv(
            "FREE", "/Users/u/" + policy["remote_relative_path"],
            ROOT / policy["rendered_path"], policy, "OVERWRITE"
        )
        notebook_argv = pub.build_import_argv(
            "FREE", "/Users/u/" + notebook["remote_relative_path"],
            ROOT / notebook["rendered_path"], notebook, "CREATE"
        )

        for argv in (file_argv, policy_argv, notebook_argv):
            self.assertIn("api", argv)
            self.assertIn("put", argv)
            self.assertIn("/api/2.0/workspace/import", argv)
            self.assertNotIn("workspace", argv)
            self.assertNotIn("--file", argv)

        file_payload = json.loads(file_argv[-1])
        policy_payload = json.loads(policy_argv[-1])
        notebook_payload = json.loads(notebook_argv[-1])
        self.assertEqual("RAW", file_payload["format"])
        self.assertFalse(file_payload["overwrite"])
        self.assertEqual((ROOT / file_row["rendered_path"]).read_bytes(), __import__("base64").b64decode(file_payload["content"]))
        self.assertTrue(policy_payload["overwrite"])
        self.assertEqual("SOURCE", notebook_payload["format"])
        self.assertEqual("PYTHON", notebook_payload["language"])

    def test_workspace_listing_accepts_cli_list_shape(self):
        rows = pub._parse_workspace_listing('[{"path":"/Users/u/a","object_type":"FILE"}]')
        self.assertEqual("/Users/u/a", rows[0]["path"])

    def test_workspace_listing_accepts_api_objects_shape(self):
        rows = pub._parse_workspace_listing('{"objects":[{"path":"/Users/u/a","object_type":"FILE"}]}')
        self.assertEqual("/Users/u/a", rows[0]["path"])

    def test_workspace_listing_accepts_empty_object(self):
        self.assertEqual([], pub._parse_workspace_listing("{}"))

    def test_workspace_listing_rejects_invalid_json(self):
        with self.assertRaisesRegex(RuntimeError, "WORKSPACE_LIST_INVALID_JSON"):
            pub._parse_workspace_listing("not-json")

    def test_workspace_listing_rejects_non_object_row(self):
        payload = json.dumps([{"path": "/Users/u/a", "object_type": "FILE"}, "bad-row"])
        with self.assertRaisesRegex(RuntimeError, "WORKSPACE_LIST_ROW_NOT_OBJECT"):
            pub._parse_workspace_listing(payload)

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

    def test_file_export_uses_auto_after_type_contract(self):
        calls = []
        with patch.object(pub, "_run_dbx", side_effect=lambda _profile,*args:(calls.append(args) or (0,json.dumps({"content":"YQ=="}),""))):
            self.assertEqual(b"a", pub._export("FREE", "/Users/u/a.py", "FILE"))
        self.assertIn("AUTO", calls[0])
        self.assertNotIn("RAW", calls[0])

    def test_policy_classifier_accepts_stale_or_exact_local(self):
        stale = pub._sha256_bytes(b"stale")
        local = pub._sha256_bytes(b"local")
        entry = {
            "object_kind": "FILE",
            "precondition": {"kind": "REMOTE_STALE_OR_EXACT_LOCAL", "sha256": stale},
            "expected_local_normalized_sha256": local,
        }
        with patch.object(pub, "_remote_normalized_hash", return_value=stale):
            self.assertEqual("OVERWRITE", pub._classify_overwrite_candidate("FREE", "/Users/u/policy.json", entry)["action"])
        with patch.object(pub, "_remote_normalized_hash", return_value=local):
            self.assertEqual("ALREADY_CORRECT", pub._classify_overwrite_candidate("FREE", "/Users/u/policy.json", entry)["action"])
        with patch.object(pub, "_remote_normalized_hash", return_value="0" * 64):
            with self.assertRaisesRegex(RuntimeError, "OVERWRITE_TARGET_UNEXPECTED_HASH"):
                pub._classify_overwrite_candidate("FREE", "/Users/u/policy.json", entry)

    def test_create_classifier_skips_exact_existing_content(self):
        entry = next(e for e in self.manifest()["entries"] if e["object_id"] == "domain-context-init")
        local_hash = pub._local_normalized_hash(entry)
        with patch.object(pub, "_status", return_value=(0, "{}", "")), patch.object(
            pub, "_remote_normalized_hash", return_value=local_hash
        ):
            result = pub._classify_create_candidate("FREE", "/Users/u/x.py", entry)
        self.assertEqual("ALREADY_CORRECT", result["action"])

    def test_create_classifier_rejects_divergent_existing_content(self):
        entry = next(e for e in self.manifest()["entries"] if e["object_id"] == "domain-context-init")
        with patch.object(pub, "_status", return_value=(0, "{}", "")), patch.object(
            pub, "_remote_normalized_hash", return_value="0" * 64
        ):
            with self.assertRaisesRegex(RuntimeError, "CREATE_TARGET_EXISTS_DIVERGENT"):
                pub._classify_create_candidate("FREE", "/Users/u/x.py", entry)

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

    def test_authorization_rejects_manifest_digest_drift(self):
        object_ids = [e["object_id"] for e in self.manifest()["entries"]]
        payload = {
            "schema_version": pub.AUTH_SCHEMA,
            "decision": "AUTHORIZED",
            "manifest_sha256": "0" * 64,
            "publisher_package_sha256": pub._publisher_package_sha256(),
            "effect": "REMOTE_PACKAGE_WRITE",
            "target": {"profile": "FREE", "host": pub.EXPECTED_HOST},
            "allowed_object_ids": object_ids,
            "one_write_attempt": True,
            "authorization_ref": "issue#114:comment#future",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "AUTH_MANIFEST_BINDING"):
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

    def test_authorization_record_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text("{}", encoding="utf-8")
            with patch.object(Path, "is_symlink", return_value=True):
                with self.assertRaisesRegex(RuntimeError, "AUTHORIZATION_SYMLINK_FORBIDDEN"):
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

    def test_execute_mocked_full_success_covers_manifest_records(self):
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
                 patch.object(pub, "_classify_entry", side_effect=lambda _p,_r,e: {"action":"CREATE"} if e["precondition"]["kind"] in pub.CREATE_PRECONDITION_KINDS else {"action":"OVERWRITE"}), \
                 patch.object(pub, "_consume_write_authorization", return_value="c" * 64) as consume, \
                 patch.object(pub, "_run_import", return_value=(0, "", "")), \
                 patch.object(pub, "_assert_remote_object_type"), \
                 patch.object(pub, "_export", side_effect=exported):
                result = pub.execute(auth, evidence)

            self.assertEqual("PASS", result["status"])
            self.assertTrue(result["authorization_consumed"])
            self.assertEqual(1, consume.call_count)
            expected_total = manifest["expected_object_count"]
            expected_created = manifest["missing_object_count"]
            expected_updated = manifest["overwrite_object_count"]
            self.assertEqual(expected_total, len(result["records"]))
            self.assertEqual(expected_total, sum(r["write_started"] is True for r in result["records"]))
            self.assertEqual(expected_total, sum(r["write_exit_code"] == 0 for r in result["records"]))
            self.assertEqual(expected_total, sum(r["verification"] == "PASS" for r in result["records"]))
            self.assertEqual(expected_created, sum(r["effect_status"] == "CREATED" for r in result["records"]))
            self.assertEqual(expected_updated, sum(r["effect_status"] == "UPDATED" for r in result["records"]))

    def test_execute_skips_already_correct_without_consuming_for_that_entry(self):
        manifest = self.manifest()
        first_id = manifest["entries"][0]["object_id"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            auth = self._write_auth_v2(root)
            evidence = root / "evidence"
            def classify(_p, _r, entry):
                if entry["object_id"] == first_id:
                    return {"action":"ALREADY_CORRECT","remote_normalized_sha256":"a"*64,"local_normalized_sha256":"a"*64}
                return {"action":"CREATE"} if entry["precondition"]["kind"] in pub.CREATE_PRECONDITION_KINDS else {"action":"OVERWRITE"}
            by_remote = {e["remote_relative_path"]: e for e in manifest["entries"]}
            def exported(_profile, remote, _kind):
                rel = remote.split("/.assistant/", 1)[1]
                entry = by_remote[".assistant/" + rel]
                return (ROOT / entry["rendered_path"]).read_bytes()
            with patch.object(pub, "_resolve_target", return_value=("/Users/u", {"profile":"FREE","host":pub.EXPECTED_HOST,"current_user_resolved":True})), \
                 patch.object(pub, "_assert_parent_directory_exists"), \
                 patch.object(pub, "_classify_entry", side_effect=classify), \
                 patch.object(pub, "_consume_write_authorization", return_value="c"*64) as consume, \
                 patch.object(pub, "_run_import", return_value=(0,"","")), \
                 patch.object(pub, "_assert_remote_object_type"), \
                 patch.object(pub, "_export", side_effect=exported):
                result = pub.execute(auth, evidence)
            self.assertEqual("PASS", result["status"])
            skipped = next(r for r in result["records"] if r["object_id"] == first_id)
            self.assertFalse(skipped["write_started"])
            self.assertEqual("ALREADY_CORRECT", skipped["effect_status"])
            self.assertEqual("PASS", skipped["verification"])
            self.assertEqual(1, consume.call_count)

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
                 patch.object(pub, "_classify_entry", return_value={"action":"CREATE"}), \
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

    def test_required_adversarial_case_methods_are_present(self):
        missing = [
            case_id
            for case_id, method_name in REQUIRED_ADVERSARIAL_TEST_METHODS.items()
            if not callable(getattr(type(self), method_name, None))
        ]
        self.assertEqual([], missing)

    def test_versioned_adversarial_coverage_matches_required_methods(self):
        coverage = json.loads((HERE / "adversarial_coverage.json").read_text(encoding="utf-8"))
        self.assertEqual("SER-B1-G6-PUBLISHER-ADVERSARIAL-COVERAGE-4", coverage["schema_version"])
        self.assertFalse(coverage["remote_access_required"])
        self.assertFalse(coverage["remote_execution_authorized"])
        observed = {case_id: method_name for case_id, method_name in coverage["required_cases"]}
        self.assertEqual(REQUIRED_ADVERSARIAL_TEST_METHODS, observed)

    def test_evidence_must_be_outside_repo_and_new(self):
        with self.assertRaisesRegex(RuntimeError, "EVIDENCE_MUST_BE_EXTERNAL"):
            pub._evidence_dir(ROOT / "tmp-evidence-forbidden")


if __name__ == "__main__":
    unittest.main()
