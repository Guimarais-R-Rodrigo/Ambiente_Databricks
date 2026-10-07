from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_databricks" / ".assistant"
SKILL = "hub-ml-eda-profissional"
SOURCE_SKILL = SOURCE_ASSISTANT / "skills" / SKILL
VALIDATOR_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "validate_contracts.py"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))

from hub_scripts.skill_execution import run_preflight

validator_spec = importlib.util.spec_from_file_location("sef_validate_contracts_se02", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(validator_spec)
assert validator_spec and validator_spec.loader
sys.modules[validator_spec.name] = validator
validator_spec.loader.exec_module(validator)


DEFAULT_CONTEXT = {
    "local_sample_required": True,
    "tabular_preview_required": True,
    "numeric_columns": 4,
    "numeric_distributions_requested": True,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": True,
    "pk_columns_available": True,
}


def _copy_fixture(root: Path) -> tuple[Path, Path]:
    assistant_root = root / ".assistant"
    skill_dir = assistant_root / "skills" / SKILL
    shutil.copytree(SOURCE_SKILL, skill_dir)

    contract = json.loads((SOURCE_SKILL / "execution_contract.json").read_text(encoding="utf-8"))
    for resource in contract["resources"]:
        module_parts = resource["module"].split(".")
        source_package = SOURCE_ASSISTANT.joinpath(*module_parts)
        target_package = assistant_root.joinpath(*module_parts)
        target_package.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_package, target_package)

    return assistant_root, skill_dir / "execution_contract.json"


def _hash_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class SkillEnforcementSE02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.assistant_root, self.contract = _copy_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_gate(self, context: dict | None = None):
        return run_preflight(
            self.contract,
            assistant_root=self.assistant_root,
            context=dict(DEFAULT_CONTEXT if context is None else context),
        )

    def validate_contract(self):
        return validator.validate_contract(
            self.contract,
            assistant_root=self.assistant_root,
        )

    def test_happy_path_passes_on_non_placeholder_assistant_root(self) -> None:
        result = self.run_gate()
        self.assertEqual("PASS", result.status)
        self.assertTrue(result.assistant_root_resolved)
        self.assertEqual([], [issue.to_dict() for issue in result.blocking_issues])
        self.assertFalse(result.writes_performed)
        self.assertNotEqual(SOURCE_ASSISTANT.resolve(), self.assistant_root.resolve())

    def test_required_resource_missing_blocks(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_scripts" / "quick_profile")
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        self.assertIn("quick_profile", {issue.item_id for issue in result.blocking_issues})

    def test_required_symbol_not_exported_blocks(self) -> None:
        init_path = self.assistant_root / "hub_scripts" / "data_quality_check" / "__init__.py"
        init_path.write_text("__all__ = []\n", encoding="utf-8")
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any(issue.item_id == "data_quality_check" for issue in result.blocking_issues))

    def test_declared_only_in_all_does_not_fake_public_export(self) -> None:
        init_path = self.assistant_root / "hub_scripts" / "data_quality_check" / "__init__.py"
        init_path.write_text('__all__ = ["data_quality_check"]\n', encoding="utf-8")
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        decision = next(item for item in result.resources if item.item_id == "data_quality_check")
        self.assertFalse(decision.resolved)
        self.assertIn("não exportado", decision.reason)

    def test_noncanonical_module_path_blocks(self) -> None:
        payload = _load(self.contract)
        payload["resources"][0]["module"] = "hub_scripts./tmp/fake"
        _write(self.contract, payload)
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        decision = next(item for item in result.resources if item.item_id == "quick_profile")
        self.assertFalse(decision.resolved)
        self.assertIn("caminho Python canônico", decision.reason)

    def test_contract_validator_rejects_declared_only_in_all(self) -> None:
        init_path = self.assistant_root / "hub_scripts" / "data_quality_check" / "__init__.py"
        init_path.write_text('__all__ = ["data_quality_check"]\n', encoding="utf-8")
        result = self.validate_contract()
        self.assertFalse(result.ok)
        issues = {issue.code for issue in result.issues}
        self.assertIn("RESOURCE_SYMBOL_NOT_EXPORTED", issues)

    def test_contract_validator_rejects_noncanonical_module_path(self) -> None:
        payload = _load(self.contract)
        payload["resources"][0]["module"] = "hub_scripts./tmp/fake"
        _write(self.contract, payload)
        result = self.validate_contract()
        self.assertFalse(result.ok)
        issues = {issue.code for issue in result.issues}
        self.assertIn("RESOURCE_MODULE_INVALID", issues)

    def test_required_template_missing_blocks(self) -> None:
        (self.contract.parent / "templates" / "roteiro_eda.md").unlink()
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any(issue.item_id == "roteiro_eda" for issue in result.blocking_issues))

    def test_pk_unavailable_does_not_require_data_quality_check(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_scripts" / "data_quality_check")
        context = dict(DEFAULT_CONTEXT, pk_columns_available=False)
        result = self.run_gate(context)
        self.assertEqual("PASS", result.status)
        decision = next(
            item for item in result.resources
            if item.item_id == "data_quality_check"
        )
        self.assertFalse(decision.applicable)
        self.assertIsNone(decision.resolved)

    def test_missing_pk_applicability_context_blocks_fail_closed(self) -> None:
        context = dict(DEFAULT_CONTEXT)
        context.pop("pk_columns_available")
        result = self.run_gate(context)
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(
            any(
                issue.code == "CONDITION_CONTEXT_INVALID"
                and issue.item_id == "data_quality_check"
                for issue in result.blocking_issues
            )
        )

    def test_conditional_false_does_not_require_resource(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_snippets" / "spark" / "smart_sample")
        context = dict(DEFAULT_CONTEXT, local_sample_required=False)
        result = self.run_gate(context)
        self.assertEqual("PASS", result.status)
        decision = next(item for item in result.resources if item.item_id == "smart_sample")
        self.assertFalse(decision.applicable)
        self.assertIsNone(decision.resolved)

    def test_conditional_true_missing_resource_blocks(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_snippets" / "spark" / "smart_sample")
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any(issue.item_id == "smart_sample" for issue in result.blocking_issues))

    def test_numeric_condition_false_skips_correlation(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_snippets" / "display" / "correlation_matrix")
        context = dict(DEFAULT_CONTEXT, numeric_columns=1)
        result = self.run_gate(context)
        self.assertEqual("PASS", result.status)
        decision = next(item for item in result.resources if item.item_id == "correlation_matrix")
        self.assertFalse(decision.applicable)

    def test_numeric_condition_true_missing_correlation_blocks(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_snippets" / "display" / "correlation_matrix")
        result = self.run_gate(dict(DEFAULT_CONTEXT, numeric_columns=2))
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any(issue.item_id == "correlation_matrix" for issue in result.blocking_issues))

    def test_theme_not_selected_does_not_require_theme_helper(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_snippets" / "visual" / "theme_plotly")
        result = self.run_gate(dict(DEFAULT_CONTEXT, resolved_theme_selected=False))
        self.assertEqual("PASS", result.status)

    def test_optional_resource_absence_does_not_block(self) -> None:
        shutil.rmtree(self.assistant_root / "hub_snippets" / "constants" / "format_br")
        result = self.run_gate()
        self.assertEqual("PASS", result.status)
        decision = next(item for item in result.resources if item.item_id == "format_br")
        self.assertFalse(decision.resolved)
        self.assertFalse(decision.applicable)

    def test_missing_condition_context_blocks_fail_closed(self) -> None:
        context = dict(DEFAULT_CONTEXT)
        context.pop("visual_diagnostics_requested")
        result = self.run_gate(context)
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any(issue.code == "CONDITION_CONTEXT_INVALID" for issue in result.blocking_issues))

    def test_invalid_condition_context_type_blocks(self) -> None:
        context = dict(DEFAULT_CONTEXT, local_sample_required="sim")
        result = self.run_gate(context)
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any("booleano" in issue.message for issue in result.blocking_issues))

    def test_unknown_condition_blocks(self) -> None:
        payload = _load(self.contract)
        payload["resources"][3]["condition"] = {"kind": "invented_condition"}
        _write(self.contract, payload)
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any("não suportado" in issue.message for issue in result.blocking_issues))

    def test_unsafe_required_template_path_blocks(self) -> None:
        payload = _load(self.contract)
        payload["templates"][0]["path"] = "../fora.md"
        _write(self.contract, payload)
        result = self.run_gate()
        self.assertEqual("BLOCKED", result.status)
        self.assertTrue(any(issue.item_id == "roteiro_eda" for issue in result.blocking_issues))

    def test_result_is_deterministic(self) -> None:
        first = self.run_gate().to_dict()
        second = self.run_gate().to_dict()
        self.assertEqual(first, second)

    def test_preflight_does_not_write_fixture(self) -> None:
        before = _hash_tree(self.assistant_root)
        result = self.run_gate()
        after = _hash_tree(self.assistant_root)
        self.assertEqual("PASS", result.status)
        self.assertEqual(before, after)
        self.assertFalse(result.writes_performed)

    def test_skill_thin_script_uses_canonical_preflight(self) -> None:
        script = SOURCE_SKILL / "scripts" / "preflight.py"
        text = script.read_text(encoding="utf-8")
        self.assertIn("from hub_scripts.skill_execution import run_preflight", text)
        self.assertNotIn("quick_profile(", text)
        self.assertNotIn("data_quality_check(", text)

    def test_later_sprint_boundaries_remain_explicit(self) -> None:
        self.assertFalse((SOURCE_SKILL / "scripts" / "run_core.py").exists())
        execution_dir = SOURCE_ASSISTANT / "hub_scripts" / "skill_execution"
        self.assertFalse((execution_dir / "postflight.py").exists())
        self.assertFalse((execution_dir / "runner.py").exists())


if __name__ == "__main__":
    unittest.main()
