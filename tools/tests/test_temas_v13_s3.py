from __future__ import annotations

import ast
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import temas_v09_transicao as v09  # noqa: E402
from tools import temas_v10_app as v10  # noqa: E402
from tools import temas_v13_release as s3  # noqa: E402


class V13S3ReleaseTests(unittest.TestCase):
    def setUp(self):
        s3.ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
        self._tmp = tempfile.TemporaryDirectory(prefix="v13_s3_test_", dir=s3.ARTIFACT_ROOT)
        self.tmp = Path(self._tmp.name)
        self.commit = s3._git_state()["commit"]

    def tearDown(self):
        self._tmp.cleanup()
        try:
            if s3.ARTIFACT_ROOT.is_dir() and not any(s3.ARTIFACT_ROOT.iterdir()):
                s3.ARTIFACT_ROOT.rmdir()
        except OSError:
            pass

    def rel(self, path: Path) -> str:
        return path.relative_to(ROOT).as_posix()

    def transition_bundle(
        self,
        name: str,
        *,
        schema_version: int = 2,
        source_commit: str | None = None,
        tamper: bool = False,
    ) -> Path:
        path = self.tmp / name
        payloads = {
            item: (f"s3:{index}:{item}\n").encode("utf-8")
            for index, item in enumerate(v09.THEME_REQUIRED_PATHS)
        }
        entries = [
            {
                "path": item,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "object_type": "FILE",
            }
            for item, raw in payloads.items()
        ]
        manifest = {
            "schema_version": schema_version,
            "source_commit": source_commit or self.commit,
            "worktree_dirty": False,
            "generated_at_utc": "2000-01-01T00:00:00+00:00",
            "target": "/Users/<username-trabalho>/",
            "files": entries,
            "theme_contract": v09.validate_theme_inventory(entries),
        }
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("MANIFEST.json", json.dumps(manifest, ensure_ascii=False))
            for index, (item, raw) in enumerate(payloads.items()):
                if tamper and index == 0:
                    raw = b"tampered"
                archive.writestr(item, raw)
        return path

    def preflight_transition(self, bundle: Path, *, authorized: bool = True):
        inputs = {
            "bundle_path": self.rel(bundle),
            "rollback": {"prepared": True, "state_ref": "discard-local-bundle"},
        }
        if authorized:
            inputs["authorization_ref"] = "explicit-local-build"
        return {
            "request_version": 1,
            "mode": "surface",
            "operations": [
                {
                    "surface_id": "transition_bundle",
                    "action_id": "build_transition_bundle",
                    "inputs": inputs,
                }
            ],
        }

    def preflight_app(self, bundle: Path):
        return {
            "request_version": 1,
            "mode": "surface",
            "operations": [
                {
                    "surface_id": "databricks_app",
                    "action_id": "build_app_bundle",
                    "inputs": {
                        "app_bundle_dir": self.rel(bundle),
                        "authorization_ref": "explicit-local-build",
                        "rollback": {"prepared": True, "state_ref": "discard-local-app-bundle"},
                    },
                }
            ],
        }

    def request(self, bundle: Path, *, mode: str = "release", preflight=None, lkg=None):
        return {
            "request_version": 1,
            "mode": mode,
            "preflight": preflight or self.preflight_transition(bundle),
            "artifact": {"kind": "transition_bundle", "path": self.rel(bundle)},
            "last_known_good": lkg,
        }

    def test_release_requires_clean_tree_and_emits_verified_receipt(self):
        bundle = self.transition_bundle("release.zip")
        report = s3.run_release_cycle(self.request(bundle))
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["preflight_status"], "PASS")
        self.assertEqual(report["receipt"]["result"], "READY_FOR_AUTHORIZED_APPLY")
        self.assertTrue(report["receipt"]["staging_verified"])
        self.assertTrue(report["receipt"]["rollback_dry_run_verified"])
        self.assertFalse(report["network_access"])
        self.assertFalse(report["remote_mutation_performed"])

    def test_dirty_tree_fails_before_receipt(self):
        bundle = self.transition_bundle("dirty.zip")
        with mock.patch.object(
            s3,
            "_git_state",
            return_value={"commit": self.commit, "clean": False},
        ):
            report = s3.run_release_cycle(self.request(bundle))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("TREE_DIRTY", {item["code"] for item in report["checks"]})
        self.assertNotIn("receipt", report)

    def test_tampered_bundle_is_rejected_without_receipt(self):
        bundle = self.transition_bundle("tampered.zip", tamper=True)
        report = s3.run_release_cycle(self.request(bundle))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("PREFLIGHT_FAILED", {item["code"] for item in report["checks"]})
        self.assertNotIn("receipt", report)

    def test_stale_artifact_source_commit_is_rejected(self):
        bundle = self.transition_bundle("stale.zip", source_commit="1" * 40)
        report = s3.run_release_cycle(self.request(bundle))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("ARTIFACT_SOURCE_STALE", {item["code"] for item in report["checks"]})

    def test_blocked_s2_preflight_stays_blocked(self):
        bundle = self.transition_bundle("blocked.zip")
        report = s3.run_release_cycle(
            self.request(bundle, preflight=self.preflight_transition(bundle, authorized=False))
        )
        self.assertEqual(report["overall_status"], "BLOCKED")
        self.assertIn("PREFLIGHT_BLOCKED", {item["code"] for item in report["checks"]})
        self.assertNotIn("receipt", report)

    def test_preflight_must_be_bound_to_same_artifact(self):
        bundle = self.transition_bundle("bound.zip")
        other = self.transition_bundle("other.zip")
        report = s3.run_release_cycle(
            self.request(bundle, preflight=self.preflight_transition(other))
        )
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("PREFLIGHT_BINDING_MISMATCH", {item["code"] for item in report["checks"]})

    def test_update_requires_last_known_good(self):
        bundle = self.transition_bundle("candidate.zip")
        report = s3.run_release_cycle(self.request(bundle, mode="update"))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("LKG_REQUIRED", {item["code"] for item in report["checks"]})

    def test_incompatible_update_version_is_rejected(self):
        lkg_bundle = self.transition_bundle("lkg_v1.zip", schema_version=1, source_commit="2" * 40)
        candidate = self.transition_bundle("candidate_v2.zip", schema_version=2)
        lkg = s3.make_lkg_reference(
            "transition_bundle",
            self.rel(lkg_bundle),
            acceptance_ref="previous-human-acceptance",
        )
        report = s3.run_release_cycle(self.request(candidate, mode="update", lkg=lkg))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("UPDATE_INCOMPATIBLE", {item["code"] for item in report["checks"]})
        self.assertNotIn("receipt", report)

    def test_update_with_compatible_lkg_verifies_restore(self):
        lkg_bundle = self.transition_bundle("lkg.zip", source_commit="3" * 40)
        candidate = self.transition_bundle("candidate_ok.zip")
        lkg = s3.make_lkg_reference(
            "transition_bundle",
            self.rel(lkg_bundle),
            acceptance_ref="previous-human-acceptance",
        )
        report = s3.run_release_cycle(self.request(candidate, mode="update", lkg=lkg))
        self.assertEqual(report["overall_status"], "PASS")
        self.assertIn("UPDATE_COMPATIBLE", {item["code"] for item in report["checks"]})
        self.assertIn("ROLLBACK_RESTORE_VERIFIED", {item["code"] for item in report["checks"]})
        self.assertEqual(
            report["receipt"]["last_known_good"]["artifact_fingerprint"],
            lkg["artifact_fingerprint"],
        )

    def test_rollback_dry_run_restores_exact_lkg_content(self):
        lkg_bundle = self.transition_bundle("rollback_lkg.zip", source_commit="4" * 40)
        candidate = self.transition_bundle("rollback_candidate.zip")
        lkg = s3.make_lkg_reference(
            "transition_bundle",
            self.rel(lkg_bundle),
            acceptance_ref="accepted-release-previous",
        )
        report = s3.run_release_cycle(
            self.request(candidate, mode="rollback_dry_run", lkg=lkg)
        )
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["receipt"]["result"], "ROLLBACK_DRY_RUN_VERIFIED")
        self.assertTrue(report["receipt"]["rollback_dry_run_verified"])

    def test_mid_operation_failure_never_emits_success_receipt(self):
        bundle = self.transition_bundle("copy_fail.zip")
        with mock.patch.object(s3, "_copy_artifact", side_effect=OSError("fixture")):
            report = s3.run_release_cycle(self.request(bundle))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("LOCAL_OPERATION_FAILED", {item["code"] for item in report["checks"]})
        self.assertNotIn("receipt", report)

    def test_lkg_reference_must_match_real_bytes(self):
        lkg_bundle = self.transition_bundle("lkg_ref.zip", source_commit="5" * 40)
        candidate = self.transition_bundle("candidate_ref.zip")
        lkg = s3.make_lkg_reference(
            "transition_bundle",
            self.rel(lkg_bundle),
            acceptance_ref="accepted-release",
        )
        lkg["artifact_fingerprint"] = "0" * 64
        report = s3.run_release_cycle(self.request(candidate, mode="update", lkg=lkg))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("LKG_DESCRIPTOR_INVALID", {item["code"] for item in report["checks"]})

    def test_acceptance_reference_is_not_echoed(self):
        secret = "sk-proj-MUST-NOT-APPEAR"
        lkg_bundle = self.transition_bundle("lkg_secret.zip", source_commit="6" * 40)
        candidate = self.transition_bundle("candidate_secret.zip")
        lkg = s3.make_lkg_reference(
            "transition_bundle",
            self.rel(lkg_bundle),
            acceptance_ref=secret,
        )
        report = s3.run_release_cycle(self.request(candidate, mode="update", lkg=lkg))
        self.assertNotIn(secret, json.dumps(report, ensure_ascii=False))

    def test_same_release_request_is_deterministic(self):
        bundle = self.transition_bundle("deterministic.zip")
        request = self.request(bundle)
        self.assertEqual(
            s3.run_release_cycle(request),
            s3.run_release_cycle(request),
        )

    def test_app_bundle_content_is_reproducible_and_releaseable(self):
        first = self.tmp / "app_first"
        second = self.tmp / "app_second"
        v10.build(first)
        v10.build(second)
        first_snapshot = s3._snapshot("app_bundle", first)
        second_snapshot = s3._snapshot("app_bundle", second)
        self.assertEqual(
            first_snapshot["content_fingerprint"],
            second_snapshot["content_fingerprint"],
        )
        request = {
            "request_version": 1,
            "mode": "release",
            "preflight": self.preflight_app(first),
            "artifact": {"kind": "app_bundle", "path": self.rel(first)},
            "last_known_good": None,
        }
        report = s3.run_release_cycle(request)
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["receipt"]["artifact_kind"], "app_bundle")

    def test_release_initial_rejects_lkg_descriptor(self):
        lkg_bundle = self.transition_bundle("unexpected_lkg.zip", source_commit="7" * 40)
        candidate = self.transition_bundle("initial.zip")
        lkg = s3.make_lkg_reference(
            "transition_bundle",
            self.rel(lkg_bundle),
            acceptance_ref="old",
        )
        report = s3.run_release_cycle(self.request(candidate, mode="release", lkg=lkg))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("LKG_DESCRIPTOR_INVALID", {item["code"] for item in report["checks"]})

    def test_every_emitted_code_is_registered(self):
        bundle = self.transition_bundle("codes.zip")
        reports = [
            s3.run_release_cycle(self.request(bundle)),
            s3.run_release_cycle({"mode": "bad"}),
        ]
        for report in reports:
            self.assertTrue(
                {item["code"] for item in report["checks"]} <= s3.STABLE_CODES
            )

    def test_s3_tool_has_no_network_or_databricks_client(self):
        source = (ROOT / "tools/temas_v13_release.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertTrue(
            imports.isdisjoint({"requests", "socket", "urllib", "httpx", "databricks"})
        )
        self.assertNotIn("shell=True", source)
        self.assertNotIn("DATABRICKS_TOKEN", source)

    def test_git_subprocess_is_read_only(self):
        source = (ROOT / "tools/temas_v13_release.py").read_text(encoding="utf-8")
        self.assertIn('["git", "rev-parse", "HEAD"]', source)
        self.assertIn('["git", "status", "--porcelain", "--untracked-files=all"]', source)
        for forbidden in ("git push", "git reset", "git checkout", "git clean", "git add", "git commit"):
            self.assertNotIn(forbidden, source)

    def test_workflow_runs_s1_s2_s3_read_only(self):
        workflow = (ROOT / ".github/workflows/temas-v13-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        for name in ("test_temas_v13_s1.py", "test_temas_v13_s2.py", "test_temas_v13_s3.py"):
            self.assertIn(name, workflow)
        self.assertIn("V13_S3_NETWORK=0", workflow)
        self.assertIn("V13_S3_REMOTE_MUTATION=0", workflow)
        self.assertIn("V13_S3_LOCAL_DRY_RUN_ONLY=1", workflow)
        self.assertIn("V13_S4_NOT_STARTED=1", workflow)
        self.assertNotIn("DATABRICKS_TOKEN", workflow)
        self.assertNotIn("secrets.", workflow)

    def test_s3_documentation_contains_all_canonical_runbooks(self):
        text = (ROOT / "docs/sprints/sistema_temas/V13/S3_RELEASE_OPERACIONAL.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "Runbook de release",
            "Runbook de instalação e atualização",
            "Runbook de rollback",
            "Checklist de staging",
            "Last known good",
        ):
            self.assertIn(heading, text)
        self.assertIn("não autoriza", text.lower())
        self.assertIn("Publish", text)
        self.assertIn("A11-01", text)


if __name__ == "__main__":
    unittest.main()
