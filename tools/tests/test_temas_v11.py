"""V11 — ponte AI/BI, matriz de correspondência e guardas fail-closed."""
from __future__ import annotations

import hashlib
import importlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "ambiente_fonte" / ".assistant"
AIBI = PRODUCT / "hub_padroes" / "identidade_visual" / "aibi"
MIRROR = ROOT / ".artifacts/simulado" / "Users" / "usuario-free" / ".assistant" / "hub_padroes" / "identidade_visual" / "aibi"
sys.path.insert(0, str(PRODUCT))
sys.path.insert(0, str(AIBI))

from hub_snippets.visual.tema import load_reference_theme
from aibi_theme import (
    AibiThemeError,
    authorize_local_operation,
    bind_native_template,
    dashboard_theme_policy,
    export_projection,
    project_theme,
    synthetic_dashboard_semantic_fingerprint,
    workspace_theme_policy,
)


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.mapping = json.loads((AIBI / "aibi_mapping.json").read_text(encoding="utf-8"))
        self.schema = json.loads(
            (PRODUCT / "hub_padroes/identidade_visual/theme.schema.json").read_text(encoding="utf-8")
        )

    def test_mapping_covers_exact_notebook_token_contract(self):
        expected = set(self.schema["$defs"]["notebookTokens"]["properties"])
        actual = {row["hub_token"] for row in self.mapping["mappings"]}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 48)

    def test_mapping_classifications_are_explicit_and_complete(self):
        counts = {}
        for row in self.mapping["mappings"]:
            counts[row["classification"]] = counts.get(row["classification"], 0) + 1
        self.assertEqual(counts, {"translated": 3, "approximated": 23, "unsupported": 22})
        for row in self.mapping["mappings"]:
            if row["classification"] == "unsupported":
                self.assertIsNone(row["target_capability"])
                self.assertEqual(row["binding_strategy"], "none")
            if row["binding_strategy"] == "direct":
                self.assertEqual(row["classification"], "translated")

    def test_aibi_context_remains_reserved_not_silently_enabled(self):
        self.assertNotIn("aibi", self.schema["properties"]["context"]["enum"])
        self.assertIn("aibi", self.schema["x-hub-policy"]["reserved_contexts"])
        self.assertIn("app", self.schema["x-hub-policy"]["reserved_contexts"])

    def test_mapping_sources_are_official_databricks_docs(self):
        urls = [item["url"] for item in self.mapping["official_sources"]]
        self.assertTrue(urls)
        self.assertTrue(all(url.startswith("https://docs.databricks.com/") for url in urls))


class ProjectionTests(unittest.TestCase):
    def test_projection_revalidates_v02_theme_and_is_not_native_import(self):
        theme = load_reference_theme("notebook")
        projection = project_theme(theme)
        data = projection.to_dict()
        self.assertEqual(data["source"]["fingerprint"], theme.fingerprint)
        self.assertEqual(data["source"]["context"], "notebook")
        self.assertFalse(data["target"]["native_import_ready"])
        self.assertEqual(data["target"]["native_schema_status"], "unverified")
        self.assertEqual(
            data["summary"],
            {"approximated": 23, "translated": 3, "unsupported": 22},
        )

    def test_projection_rejects_editorial_context(self):
        with self.assertRaises(AibiThemeError) as cm:
            project_theme(load_reference_theme("readme"))
        self.assertEqual(cm.exception.code, "AIBI_THEME_INTEGRITY")

    def test_projection_export_is_deterministic(self):
        projection = project_theme(load_reference_theme("notebook"))
        first = export_projection(projection)
        second = export_projection(project_theme(load_reference_theme("notebook")))
        self.assertEqual(first, second)
        parsed = json.loads(first)
        self.assertEqual(parsed["format"], "hub-aibi-theme-projection")
        self.assertIn("AIBI_NATIVE_JSON_SCHEMA_UNVERIFIED", parsed["warnings"])

    def test_direct_translations_are_only_three_capabilities(self):
        projection = project_theme(load_reference_theme("notebook")).to_dict()
        direct = {
            row["target_capability"]
            for row in projection["mappings"]
            if row["binding_strategy"] == "direct"
        }
        self.assertEqual(
            direct,
            {
                "widget.background",
                "widget.corner_radius",
                "visualization.categorical_palette",
            },
        )


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.projection = project_theme(load_reference_theme("notebook"))
        self.template = {
            "theme": {
                "widget": {"background": "#000000", "cornerRadius": 0},
                "visualization": {"categoricalPalette": ["#000000"]},
                "unknownFutureField": {"preserve": True},
            }
        }
        self.template_raw = (
            json.dumps(self.template, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

    def _binding(self, paths):
        return json.dumps(
            {
                "binding_version": 1,
                "template_sha256": hashlib.sha256(self.template_raw).hexdigest(),
                "paths": paths,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def test_binding_changes_only_explicit_existing_direct_fields(self):
        binding = self._binding(
            {
                "widget.background": "/theme/widget/background",
                "widget.corner_radius": "/theme/widget/cornerRadius",
                "visualization.categorical_palette": "/theme/visualization/categoricalPalette",
            }
        )
        candidate = bind_native_template(self.projection, self.template_raw, binding)
        data = json.loads(candidate.content)
        self.assertEqual(data["theme"]["widget"]["background"], "#E8F4FD")
        self.assertEqual(data["theme"]["widget"]["cornerRadius"], 12)
        self.assertEqual(data["theme"]["visualization"]["categoricalPalette"][0], "#005CA9")
        self.assertEqual(data["theme"]["unknownFutureField"], {"preserve": True})
        self.assertEqual(candidate.omitted_capabilities, ())
        self.assertEqual(candidate.validation_status, "locally_bound_not_databricks_validated")

    def test_binding_requires_exact_template_hash(self):
        bad = json.dumps(
            {
                "binding_version": 1,
                "template_sha256": "0" * 64,
                "paths": {"widget.background": "/theme/widget/background"},
            }
        ).encode()
        with self.assertRaises(AibiThemeError) as cm:
            bind_native_template(self.projection, self.template_raw, bad)
        self.assertEqual(cm.exception.code, "AIBI_BINDING_HASH")

    def test_binding_rejects_approximation_automation(self):
        binding = self._binding({"canvas.background": "/theme/widget/background"})
        with self.assertRaises(AibiThemeError) as cm:
            bind_native_template(self.projection, self.template_raw, binding)
        self.assertEqual(cm.exception.code, "AIBI_BINDING_CAPABILITY")

    def test_binding_rejects_missing_native_path(self):
        binding = self._binding({"widget.background": "/theme/widget/missing"})
        with self.assertRaises(AibiThemeError) as cm:
            bind_native_template(self.projection, self.template_raw, binding)
        self.assertEqual(cm.exception.code, "AIBI_BINDING_PATH")

    def test_binding_can_be_selective_and_reports_omissions(self):
        binding = self._binding({"widget.background": "/theme/widget/background"})
        candidate = bind_native_template(self.projection, self.template_raw, binding)
        self.assertEqual(candidate.applied_capabilities, ("widget.background",))
        self.assertEqual(
            set(candidate.omitted_capabilities),
            {"widget.corner_radius", "visualization.categorical_palette"},
        )


class PolicyTests(unittest.TestCase):
    def test_workspace_snapshot_policy_forbids_universal_propagation_claim(self):
        policy = workspace_theme_policy()
        self.assertTrue(policy["workspace_admin_required_for_manage"])
        self.assertTrue(policy["new_dashboards_inherit_workspace_theme"])
        self.assertTrue(policy["existing_dashboard_apply_is_snapshot"])
        self.assertFalse(policy["workspace_updates_auto_propagate_to_existing"])
        self.assertTrue(policy["manual_reapply_required_for_existing"])

    def test_dashboard_policy_separates_theme_from_publish(self):
        policy = dashboard_theme_policy()
        self.assertTrue(policy["draft_required_for_settings"])
        self.assertTrue(policy["theme_import_export_available"])
        self.assertEqual(policy["color_mappings_scope"], "dashboard_only")
        self.assertTrue(policy["publish_separate_from_theme_selection"])
        self.assertFalse(policy["publish_implemented_by_v11"])
        self.assertFalse(policy["workspace_api_write_implemented_by_v11"])

    def test_admin_and_draft_guards_fail_closed(self):
        with self.assertRaises(AibiThemeError) as cm:
            authorize_local_operation("manage_workspace_theme", workspace_admin=False, draft=True)
        self.assertEqual(cm.exception.code, "AIBI_ADMIN_REQUIRED")
        authorize_local_operation("manage_workspace_theme", workspace_admin=True, draft=True)
        with self.assertRaises(AibiThemeError) as cm:
            authorize_local_operation("edit_dashboard_theme", workspace_admin=False, draft=False)
        self.assertEqual(cm.exception.code, "AIBI_DRAFT_REQUIRED")
        authorize_local_operation("edit_dashboard_theme", workspace_admin=False, draft=True)
        with self.assertRaises(AibiThemeError) as cm:
            authorize_local_operation("publish_dashboard", workspace_admin=True, draft=True)
        self.assertEqual(cm.exception.code, "AIBI_OPERATION_NOT_IMPLEMENTED")


class FixtureAndPackagingTests(unittest.TestCase):
    def test_synthetic_dashboard_is_not_databricks_importable_and_has_stable_semantics(self):
        fixture = json.loads((AIBI / "dashboard_sintetico.json").read_text(encoding="utf-8"))
        self.assertFalse(fixture["databricks_importable"])
        self.assertEqual(fixture["data_classification"], "synthetic_only")
        self.assertEqual(len(fixture["queries"]), 2)
        self.assertEqual(len(fixture["filters"]), 2)
        first = synthetic_dashboard_semantic_fingerprint(fixture)
        decorated = dict(fixture)
        decorated["theme_projection_sha256"] = "a" * 64
        second = synthetic_dashboard_semantic_fingerprint(decorated)
        self.assertEqual(first, second)

    def test_source_and_simulated_aibi_surface_are_byte_identical(self):
        source_names = {
            path.relative_to(AIBI).as_posix()
            for path in AIBI.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}
        }
        mirror_names = {
            path.relative_to(MIRROR).as_posix()
            for path in MIRROR.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}
        }
        self.assertEqual(source_names, mirror_names)
        for name in source_names:
            self.assertEqual((AIBI / name).read_bytes(), (MIRROR / name).read_bytes(), name)

    def test_public_facade_imports_as_namespace_package(self):
        module = importlib.import_module("hub_padroes.identidade_visual.aibi.aibi_theme")
        projection = module.project_theme(load_reference_theme("notebook"))
        self.assertEqual(projection.source_theme_id, "hub-legado-notebook")
        with self.assertRaises(module.AibiThemeError) as cm:
            module.project_theme(load_reference_theme("readme"))
        self.assertEqual(cm.exception.code, "AIBI_THEME_INTEGRITY")

    def test_v11_workflow_is_read_only_and_has_no_remote_databricks_action(self):
        text = (ROOT / ".github/workflows/temas-v11-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", text)
        self.assertIn("persist-credentials: false", text)
        for forbidden in (
            "DATABRICKS_TOKEN",
            "databricks auth",
            "databricks workspace",
            "WorkspaceClient",
            "/api/2.0/",
        ):
            self.assertNotIn(forbidden, text)

    def test_v11_code_does_not_call_databricks_or_workspace_api(self):
        forbidden = (
            "databricks.sdk",
            "WorkspaceClient",
            "requests.",
            "urllib.request",
            "/api/2.0/",
        )
        python_files = sorted(AIBI.glob("*.py"))
        self.assertEqual({path.name for path in python_files}, {"aibi_theme.py", "_aibi_theme_impl.py"})
        for path in python_files:
            code = path.read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, code, f"{needle} encontrado em {path.name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
