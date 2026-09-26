from __future__ import annotations

import ast
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import temas_v09_transicao as v09  # noqa: E402
from tools import temas_v13_preflight as preflight  # noqa: E402

THEME_ROOT = "ambiente_fonte/.assistant"
THEME_REL = "hub_padroes/identidade_visual/exemplos/legado_notebook.json"
THEME_PATH = ROOT / THEME_ROOT / THEME_REL


class V13S2PreflightTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix=".v13_s2_", dir=ROOT)
        self.tmp = Path(self._tmp.name)
        self.tmp_rel = self.tmp.relative_to(ROOT).as_posix()

    def tearDown(self):
        self._tmp.cleanup()

    @staticmethod
    def _codes(report):
        return {
            check["code"]
            for operation in report["operations"]
            for check in operation["checks"]
        } | {check["code"] for check in report["request_checks"]}

    def theme(self, *, sha: str | None = None, context: str = "notebook"):
        return {
            "root_ref": THEME_ROOT,
            "relative_path": THEME_REL,
            "expected_sha256": sha or hashlib.sha256(THEME_PATH.read_bytes()).hexdigest(),
            "expected_context": context,
        }

    def request(self, surface_id, action_id, inputs=None, *, mode="surface"):
        return {
            "request_version": 1,
            "mode": mode,
            "operations": [
                {
                    "surface_id": surface_id,
                    "action_id": action_id,
                    "inputs": inputs or {},
                }
            ],
        }

    def write_json(self, name: str, value) -> str:
        path = self.tmp / name
        path.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        return path.relative_to(ROOT).as_posix()

    def write_bytes(self, name: str, raw: bytes) -> str:
        path = self.tmp / name
        path.write_bytes(raw)
        return path.relative_to(ROOT).as_posix()

    def native_pair(self, *, pointer="/theme/widget/background", template_sha=None):
        template = {
            "theme": {
                "widget": {"background": "#000000", "cornerRadius": 0},
                "visualization": {"categoricalPalette": ["#000000"]},
            }
        }
        raw = (
            json.dumps(template, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        template_path = self.write_bytes("native_template.json", raw)
        binding = {
            "binding_version": 1,
            "template_sha256": template_sha or hashlib.sha256(raw).hexdigest(),
            "paths": {"widget.background": pointer},
        }
        binding_path = self.write_json("binding.json", binding)
        return template_path, binding_path

    def valid_bundle(self) -> str:
        package = self.tmp / "bundle.zip"
        payloads = {
            path: (f"fixture:{index}\n").encode("utf-8")
            for index, path in enumerate(v09.THEME_REQUIRED_PATHS)
        }
        entries = [
            {
                "path": path,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
            for path, raw in payloads.items()
        ]
        manifest = {
            "files": entries,
            "theme_contract": v09.validate_theme_inventory(entries),
        }
        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("MANIFEST.json", json.dumps(manifest))
            for path, raw in payloads.items():
                archive.writestr(path, raw)
        return package.relative_to(ROOT).as_posix()

    def test_valid_notebook_preflight_passes(self):
        report = preflight.run_preflight(
            self.request(
                "notebook_visual_core",
                "render_with_resolved_theme",
                {"theme": self.theme()},
            )
        )
        self.assertEqual(report["overall_status"], "PASS")
        self.assertIn("THEME_VALID", self._codes(report))
        self.assertFalse(report["network_access"])
        self.assertFalse(report["remote_mutation_performed"])

    def test_same_request_produces_identical_report(self):
        request = self.request(
            "notebook_visual_core",
            "render_with_resolved_theme",
            {"theme": self.theme()},
        )
        self.assertEqual(
            preflight.run_preflight(request),
            preflight.run_preflight(request),
        )

    def test_aggregate_mode_sorts_and_propagates_blocked(self):
        request = {
            "request_version": 1,
            "mode": "aggregate",
            "operations": [
                {
                    "surface_id": "workspace_theme",
                    "action_id": "apply_workspace_theme",
                    "inputs": {},
                },
                {
                    "surface_id": "notebook_visual_core",
                    "action_id": "render_with_resolved_theme",
                    "inputs": {"theme": self.theme()},
                },
            ],
        }
        report = preflight.run_preflight(request)
        self.assertEqual(report["overall_status"], "BLOCKED")
        self.assertEqual(
            [item["surface_id"] for item in report["operations"]],
            ["notebook_visual_core", "workspace_theme"],
        )
        self.assertIn("AUTHORIZATION_CANONICALLY_BLOCKED", self._codes(report))

    def test_invalid_request_shape_is_structured_fail(self):
        report = preflight.run_preflight({"mode": "surface"})
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertEqual(report["operations"], [])
        self.assertIn("REQUEST_FIELDS", self._codes(report))

    def test_surface_mode_requires_one_operation(self):
        request = {
            "request_version": 1,
            "mode": "surface",
            "operations": [
                {"surface_id": "a", "action_id": "b", "inputs": {}},
                {"surface_id": "c", "action_id": "d", "inputs": {}},
            ],
        }
        report = preflight.run_preflight(request)
        self.assertIn("REQUEST_OPERATION_COUNT", self._codes(report))

    def test_aggregate_rejects_duplicate_operation(self):
        operation = {
            "surface_id": "notebook_visual_core",
            "action_id": "render_with_resolved_theme",
            "inputs": {"theme": self.theme()},
        }
        request = {
            "request_version": 1,
            "mode": "aggregate",
            "operations": [operation, operation],
        }
        self.assertIn(
            "REQUEST_OPERATION_DUPLICATE",
            self._codes(preflight.run_preflight(request)),
        )

    def test_unknown_surface_fails_closed(self):
        report = preflight.run_preflight(
            self.request("unknown_surface", "anything", {})
        )
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("SURFACE_UNKNOWN", self._codes(report))

    def test_unknown_action_fails_closed(self):
        report = preflight.run_preflight(
            self.request("notebook_visual_core", "unknown_action", {})
        )
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertIn("ACTION_UNKNOWN", self._codes(report))

    def test_invalid_theme_fails_closed(self):
        bad = self.tmp / "bad.json"
        bad.write_text("{", encoding="utf-8")
        theme = {
            "root_ref": self.tmp_rel,
            "relative_path": "bad.json",
            "expected_sha256": hashlib.sha256(bad.read_bytes()).hexdigest(),
            "expected_context": "notebook",
        }
        report = preflight.run_preflight(
            self.request(
                "notebook_visual_core",
                "render_with_resolved_theme",
                {"theme": theme},
            )
        )
        self.assertIn("THEME_INVALID", self._codes(report))
        self.assertEqual(report["overall_status"], "FAIL")

    def test_stale_theme_hash_has_stable_code(self):
        report = preflight.run_preflight(
            self.request(
                "notebook_visual_core",
                "render_with_resolved_theme",
                {"theme": self.theme(sha="0" * 64)},
            )
        )
        self.assertIn("THEME_HASH_STALE", self._codes(report))

    def test_context_incompatible_has_stable_code(self):
        report = preflight.run_preflight(
            self.request(
                "notebook_visual_core",
                "render_with_resolved_theme",
                {"theme": self.theme(context="readme")},
            )
        )
        self.assertIn("CONTEXT_INCOMPATIBLE", self._codes(report))

    def test_incomplete_transition_bundle_fails(self):
        package = self.tmp / "bad_bundle.zip"
        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("MANIFEST.json", '{"files":[],"theme_contract":{}}')
        report = preflight.run_preflight(
            self.request(
                "transition_bundle",
                "build_transition_bundle",
                {"bundle_path": package.relative_to(ROOT).as_posix()},
            )
        )
        self.assertIn("BUNDLE_INCOMPLETE", self._codes(report))
        self.assertEqual(report["overall_status"], "FAIL")

    def test_missing_authorization_blocks_local_bundle(self):
        report = preflight.run_preflight(
            self.request(
                "transition_bundle",
                "build_transition_bundle",
                {
                    "bundle_path": self.valid_bundle(),
                    "rollback": {"prepared": True, "state_ref": "discard-new-bundle"},
                },
            )
        )
        self.assertEqual(report["overall_status"], "BLOCKED")
        self.assertIn("AUTHORIZATION_REQUIRED", self._codes(report))

    def test_missing_rollback_blocks_local_bundle(self):
        report = preflight.run_preflight(
            self.request(
                "transition_bundle",
                "build_transition_bundle",
                {
                    "bundle_path": self.valid_bundle(),
                    "authorization_ref": "operator-explicit",
                },
            )
        )
        self.assertEqual(report["overall_status"], "BLOCKED")
        self.assertIn("ROLLBACK_NOT_PREPARED", self._codes(report))

    def test_valid_local_bundle_preflight_passes(self):
        report = preflight.run_preflight(
            self.request(
                "transition_bundle",
                "build_transition_bundle",
                {
                    "bundle_path": self.valid_bundle(),
                    "authorization_ref": "operator-explicit",
                    "rollback": {"prepared": True, "state_ref": "discard-new-bundle"},
                },
            )
        )
        self.assertEqual(report["overall_status"], "PASS")
        self.assertIn("BUNDLE_VALID", self._codes(report))
        self.assertIn("ROLLBACK_PREPARED", self._codes(report))

    def test_invalid_app_bundle_and_storage_are_reported(self):
        report = preflight.run_preflight(
            self.request(
                "databricks_app",
                "deploy_app",
                {
                    "app_bundle_dir": self.tmp_rel,
                    "storage_path": "/tmp/not-volume",
                },
            )
        )
        codes = self._codes(report)
        self.assertIn("APP_BUNDLE_INVALID", codes)
        self.assertIn("APP_STORAGE_PRECONDITION", codes)
        self.assertIn("IDENTITY_REQUIRED", codes)
        self.assertEqual(report["overall_status"], "FAIL")

    def test_json_pointer_missing_fails_aibi_binding(self):
        template, binding = self.native_pair(pointer="/theme/widget/missing")
        report = preflight.run_preflight(
            self.request(
                "aibi_dashboard",
                "import_theme_draft",
                {
                    "theme": self.theme(),
                    "native_template_path": template,
                    "binding_path": binding,
                },
            )
        )
        self.assertIn("JSON_POINTER_MISSING", self._codes(report))
        self.assertEqual(report["overall_status"], "FAIL")

    def test_stale_native_template_hash_fails_aibi_binding(self):
        template, binding = self.native_pair(template_sha="0" * 64)
        report = preflight.run_preflight(
            self.request(
                "aibi_dashboard",
                "import_theme_draft",
                {
                    "theme": self.theme(),
                    "native_template_path": template,
                    "binding_path": binding,
                },
            )
        )
        self.assertIn("NATIVE_TEMPLATE_HASH_STALE", self._codes(report))

    def test_synthetic_dashboard_cannot_be_native_template(self):
        synthetic = {
            "kind": "hub_v11_synthetic_dashboard_draft",
            "databricks_importable": False,
        }
        raw = (
            json.dumps(synthetic, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        template = self.write_bytes("synthetic.json", raw)
        binding = self.write_json(
            "binding_synthetic.json",
            {
                "binding_version": 1,
                "template_sha256": hashlib.sha256(raw).hexdigest(),
                "paths": {"widget.background": "/theme/widget/background"},
            },
        )
        report = preflight.run_preflight(
            self.request(
                "aibi_dashboard",
                "import_theme_draft",
                {
                    "theme": self.theme(),
                    "native_template_path": template,
                    "binding_path": binding,
                },
            )
        )
        self.assertIn("NATIVE_TEMPLATE_SYNTHETIC", self._codes(report))

    def test_remote_import_with_valid_local_binding_stays_blocked_on_identity(self):
        template, binding = self.native_pair()
        report = preflight.run_preflight(
            self.request(
                "aibi_dashboard",
                "import_theme_draft",
                {
                    "theme": self.theme(),
                    "native_template_path": template,
                    "binding_path": binding,
                    "authorization_ref": "specific-draft-import",
                    "rollback": {"prepared": True, "state_ref": "original-theme-sha"},
                },
            )
        )
        codes = self._codes(report)
        self.assertIn("AIBI_BINDING_VALID", codes)
        self.assertIn("IDENTITY_REQUIRED", codes)
        self.assertEqual(report["overall_status"], "BLOCKED")

    def test_identity_reference_is_not_promoted_to_live_verification(self):
        template, binding = self.native_pair()
        report = preflight.run_preflight(
            self.request(
                "aibi_dashboard",
                "import_theme_draft",
                {
                    "theme": self.theme(),
                    "native_template_path": template,
                    "binding_path": binding,
                    "authorization_ref": "specific-draft-import",
                    "identity_ref": "sanitized-environment-evidence",
                    "rollback": {"prepared": True, "state_ref": "original-theme-sha"},
                },
            )
        )
        self.assertIn("IDENTITY_LIVE_UNVERIFIED", self._codes(report))
        self.assertEqual(report["overall_status"], "BLOCKED")

    def test_publish_remains_canonically_blocked(self):
        report = preflight.run_preflight(
            self.request(
                "aibi_dashboard",
                "publish_dashboard",
                {
                    "authorization_ref": "caller-cannot-override-owner",
                    "identity_ref": "some-reference",
                    "rollback": {"prepared": True, "state_ref": "some-state"},
                },
            )
        )
        self.assertIn("AUTHORIZATION_CANONICALLY_BLOCKED", self._codes(report))
        self.assertIn("ROLLBACK_CANONICALLY_BLOCKED", self._codes(report))
        self.assertEqual(report["overall_status"], "BLOCKED")

    def test_workspace_theme_remains_canonically_blocked(self):
        report = preflight.run_preflight(
            self.request(
                "workspace_theme",
                "apply_workspace_theme",
                {
                    "authorization_ref": "caller-cannot-override-owner",
                    "identity_ref": "some-reference",
                },
            )
        )
        codes = self._codes(report)
        self.assertIn("WORKSPACE_POLICY_VALID", codes)
        self.assertIn("AUTHORIZATION_CANONICALLY_BLOCKED", codes)
        self.assertIn("ROLLBACK_CANONICALLY_BLOCKED", codes)
        self.assertEqual(report["overall_status"], "BLOCKED")

    def test_report_never_echoes_authorization_identity_or_rollback_reference(self):
        secret = "sk-proj-THIS-MUST-NOT-APPEAR"
        report = preflight.run_preflight(
            self.request(
                "transition_bundle",
                "build_transition_bundle",
                {
                    "bundle_path": self.valid_bundle(),
                    "authorization_ref": secret,
                    "rollback": {"prepared": True, "state_ref": secret},
                },
            )
        )
        rendered = json.dumps(report, ensure_ascii=False)
        self.assertNotIn(secret, rendered)

    def test_every_emitted_code_is_registered(self):
        reports = [
            preflight.run_preflight(
                self.request(
                    "notebook_visual_core",
                    "render_with_resolved_theme",
                    {"theme": self.theme()},
                )
            ),
            preflight.run_preflight(self.request("unknown_surface", "x", {})),
        ]
        for report in reports:
            self.assertTrue(self._codes(report) <= preflight.STABLE_CODES)

    def test_s2_tool_has_no_network_databricks_or_mutation_client_import(self):
        source = (ROOT / "tools/temas_v13_preflight.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertTrue(
            imports.isdisjoint(
                {"requests", "socket", "urllib", "httpx", "databricks", "subprocess", "shutil"}
            )
        )

    def test_workflow_runs_s1_and_s2_read_only(self):
        workflow = (ROOT / ".github/workflows/temas-v13-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("test_temas_v13_s1.py", workflow)
        self.assertIn("test_temas_v13_s2.py", workflow)
        self.assertIn("V13_S2_NETWORK=0", workflow)
        self.assertIn("V13_S2_REMOTE_MUTATION=0", workflow)
        self.assertNotIn("DATABRICKS_TOKEN", workflow)
        self.assertNotIn("secrets.", workflow)


if __name__ == "__main__":
    unittest.main()
