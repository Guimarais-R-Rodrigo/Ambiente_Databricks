from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

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
        self.assertEqual(
            "b68d378b4552f0f2800e82a47faf48961af68c0c95f416bb580582fc48f47be9",
            overwrite[0]["precondition"]["sha256"],
        )

    def test_import_argv_overwrite_semantics(self):
        entries = self.manifest()["entries"]
        missing = next(e for e in entries if e["object_id"] == "ser03-run")
        policy = next(e for e in entries if e["object_id"] == "policy")
        notebook = next(e for e in entries if e["object_kind"] == "NOTEBOOK")
        missing_argv = pub.build_import_argv("FREE", "/Users/u/" + missing["remote_relative_path"], ROOT / missing["rendered_path"], missing)
        policy_argv = pub.build_import_argv("FREE", "/Users/u/" + policy["remote_relative_path"], ROOT / policy["rendered_path"], policy)
        notebook_argv = pub.build_import_argv("FREE", "/Users/u/" + notebook["remote_relative_path"], ROOT / notebook["rendered_path"], notebook)
        self.assertNotIn("--overwrite", missing_argv)
        self.assertIn("--overwrite", policy_argv)
        self.assertEqual(["--format", "SOURCE", "--language", "PYTHON"], notebook_argv[-4:])
        self.assertNotIn("--overwrite", notebook_argv)

    def test_authorization_is_bound_to_manifest_and_object_set(self):
        manifest = self.manifest()
        object_ids = [e["object_id"] for e in manifest["entries"]]
        good = {
            "schema_version": pub.AUTH_SCHEMA,
            "decision": "AUTHORIZED",
            "manifest_sha256": pub._manifest_sha256(),
            "effect": "REMOTE_PACKAGE_WRITE",
            "target": {"profile": "FREE", "host": pub.EXPECTED_HOST},
            "allowed_object_ids": object_ids,
            "one_attempt": True,
            "authorization_ref": "issue#114:comment#future",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auth.json"
            path.write_text(json.dumps(good), encoding="utf-8")
            loaded = pub._validate_authorization(path, pub._manifest_sha256(), object_ids)
            self.assertEqual("AUTHORIZED", loaded["decision"])
            bad = dict(good)
            bad["manifest_sha256"] = "0" * 64
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "AUTH_MANIFEST_BINDING"):
                pub._validate_authorization(path, pub._manifest_sha256(), object_ids)

    def test_evidence_must_be_outside_repo_and_new(self):
        with self.assertRaisesRegex(RuntimeError, "EVIDENCE_MUST_BE_EXTERNAL"):
            pub._evidence_dir(ROOT / "tmp-evidence-forbidden")


if __name__ == "__main__":
    unittest.main()
