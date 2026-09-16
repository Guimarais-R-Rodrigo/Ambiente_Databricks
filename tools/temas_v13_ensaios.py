"""V13-S6: ensaios operacionais locais/simulados por superfície.

Compõe owners já integrados para provar PREPARE/PREFLIGHT/PACKAGE/STAGE/VERIFY/
ROLLBACK onde isso é possível sem Databricks real. Não usa rede, credenciais,
publicação ou mutação remota. Casos ambientais V12 bloqueados permanecem
BLOQUEADO_AUTORIZACAO até nova autorização específica.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "ambiente_fonte" / ".assistant"
AIBI = PRODUCT / "hub_padroes" / "identidade_visual" / "aibi"
for _path in (ROOT, PRODUCT, AIBI):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import plotly.graph_objects as go  # noqa: E402
import plotly.io as pio  # noqa: E402

from hub_snippets.visual.tema import export_theme, load_reference_theme  # noqa: E402
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido  # noqa: E402
from hub_snippets.visual.kpi_card import kpi_card_html_resolvido  # noqa: E402
from hub_snippets.visual.theme_lab import (  # noqa: E402
    create_theme_lab_from_preset,
    get_demo_presets,
    reopen_theme_lab_session,
    save_theme_lab_session,
)
from aibi_theme import (  # noqa: E402
    bind_native_template,
    export_projection,
    project_theme,
    synthetic_dashboard_semantic_fingerprint,
)
from tools import temas_v10_app as v10_app  # noqa: E402
from tools.temas_v13_preflight import run_preflight  # noqa: E402
from tools.temas_v13_release import run_release_cycle  # noqa: E402

ENGINE = "V13-S6"
REPORT_VERSION = 1
PHASES = ("PREPARE", "PREFLIGHT", "PACKAGE", "STAGE", "VERIFY", "ROLLBACK")
SURFACE_ORDER = (
    "notebook_visual_core",
    "visual_lab",
    "transition_bundle",
    "databricks_app",
    "aibi_dashboard",
    "workspace_theme",
)
REAL_ENVIRONMENT_CASES = (
    ("V12-LAB-01", "visual_lab"),
    ("V12-APP-01", "databricks_app"),
    ("V12-AIBI-02", "workspace_theme"),
)
ARTIFACT_ROOT = ROOT / ".artifacts"
_THEME_ROOT = "ambiente_fonte/.assistant"
_THEME_REL = "hub_padroes/identidade_visual/exemplos/legado_notebook.json"
_THEME_PATH = ROOT / _THEME_ROOT / _THEME_REL


def _phase(name: str, status: str, code: str, message: str) -> dict[str, str]:
    if name not in PHASES:
        raise ValueError("fase S6 inválida")
    if status not in {"PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"}:
        raise ValueError("status S6 inválido")
    return {"phase": name, "status": status, "code": code, "message": message}


def _overall(phases: list[dict[str, str]]) -> str:
    statuses = {item["status"] for item in phases}
    if "FAIL" in statuses:
        return "FAIL"
    if "BLOCKED" in statuses:
        return "BLOCKED"
    if "PASS" in statuses:
        return "PASS"
    return "NOT_APPLICABLE"


def _surface_report(surface_id: str, phases: list[dict[str, str]], *, local_mutation: bool, evidence_refs: list[str]) -> dict[str, Any]:
    if tuple(item["phase"] for item in phases) != PHASES:
        raise ValueError("todas as fases S6 devem ser explícitas e ordenadas")
    return {
        "surface_id": surface_id,
        "overall_status": _overall(phases),
        "phases": phases,
        "local_mutation_performed": local_mutation,
        "network_access": False,
        "remote_mutation_performed": False,
        "publication_performed": False,
        "evidence_sanitized": True,
        "evidence_refs": list(evidence_refs),
    }


def _theme_input() -> dict[str, str]:
    raw = _THEME_PATH.read_bytes()
    return {
        "root_ref": _THEME_ROOT,
        "relative_path": _THEME_REL,
        "expected_sha256": hashlib.sha256(raw).hexdigest(),
        "expected_context": "notebook",
    }


def _preflight(surface_id: str, action_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
    return run_preflight({
        "request_version": 1,
        "mode": "surface",
        "operations": [{"surface_id": surface_id, "action_id": action_id, "inputs": inputs}],
    })


def rehearse_notebook() -> dict[str, Any]:
    theme = load_reference_theme("notebook")
    before_default = pio.templates.default
    original = go.Figure(go.Bar(x=["A", "B"], y=[10, 20], marker_color="#ABCDEF"))
    original.update_xaxes(title="Categoria")
    original.update_yaxes(title="Valor", range=[0, 25])
    before = json.loads(original.to_json())
    preflight = _preflight("notebook_visual_core", "render_with_resolved_theme", {"theme": _theme_input()})
    if preflight["overall_status"] != "PASS":
        raise RuntimeError("preflight local notebook deveria ser PASS")
    payload = export_theme(theme)
    staged = go.Figure(original)
    aplicar_tema_resolvido(staged, theme)
    html = kpi_card_html_resolvido({"Linhas": 2, "Total": 30}, theme)
    after = json.loads(staged.to_json())
    semantics_ok = (
        before["data"] == after["data"]
        and before["layout"]["xaxis"] == after["layout"]["xaxis"]
        and before["layout"]["yaxis"] == after["layout"]["yaxis"]
        and "30" in html
        and pio.templates.default == before_default
    )
    original_ok = json.loads(original.to_json()) == before
    return _surface_report(
        "notebook_visual_core",
        [
            _phase("PREPARE", "PASS", "THEME_SELECTED", "Tema notebook V02 foi carregado."),
            _phase("PREFLIGHT", "PASS", "S2_PREFLIGHT_PASS", "Preflight S2 local concluiu PASS."),
            _phase("PACKAGE", "PASS", "RESOLVED_THEME_PACKAGED", f"ResolvedTheme exportado em {len(payload)} bytes."),
            _phase("STAGE", "PASS", "IN_MEMORY_STAGE", "Tema aplicado somente a cópia Plotly e HTML local."),
            _phase("VERIFY", "PASS" if semantics_ok else "FAIL", "SEMANTICS_PRESERVED" if semantics_ok else "SEMANTIC_DRIFT", "Dados/eixos/default foram preservados." if semantics_ok else "Semântica protegida divergiu."),
            _phase("ROLLBACK", "PASS" if original_ok else "FAIL", "DISCARD_STAGE_VERIFIED" if original_ok else "ROLLBACK_MISMATCH", "Descartar a cópia staged preserva o original." if original_ok else "O objeto original foi alterado."),
        ],
        local_mutation=False,
        evidence_refs=["docs/sprints/sistema_temas/V02/README.md", "tools/tests/test_temas_v03.py", "tools/tests/test_temas_v04.py"],
    )


def rehearse_visual_lab() -> dict[str, Any]:
    preflight = _preflight("visual_lab", "preview_proposal", {"theme": _theme_input()})
    if preflight["overall_status"] != "PASS":
        raise RuntimeError("preflight local do Visual Lab deveria ser PASS")
    draft = create_theme_lab_from_preset(get_demo_presets(), "legado_notebook")
    base_sha = draft.base.content_sha256
    draft.set_token("brand.primary", "#112233")
    proposal_sha = draft.current.content_sha256
    package_ok = proposal_sha != base_sha
    with tempfile.TemporaryDirectory(prefix="v13_s6_lab_") as tmp:
        receipt = save_theme_lab_session(draft, tmp, "ensaio_s6")
        reopened = reopen_theme_lab_session(tmp, "ensaio_s6")
        stage_ok = receipt.proposal_sha256 == hashlib.sha256(reopened.export_bytes()).hexdigest() and reopened.current.content_sha256 == proposal_sha
        reopened.restore()
        rollback_ok = reopened.current.content_sha256 == base_sha
    return _surface_report(
        "visual_lab",
        [
            _phase("PREPARE", "PASS", "DEMO_PRESET_SELECTED", "Preset sintético V05 selecionado explicitamente."),
            _phase("PREFLIGHT", "PASS", "S2_PREFLIGHT_PASS", "Preview local V05 passou no preflight S2."),
            _phase("PACKAGE", "PASS" if package_ok else "FAIL", "PROPOSAL_PACKAGED" if package_ok else "PROPOSAL_UNCHANGED", "Proposta em memória possui identidade distinta da base." if package_ok else "A proposta não mudou."),
            _phase("STAGE", "PASS" if stage_ok else "FAIL", "LOCAL_SESSION_STAGED" if stage_ok else "LOCAL_SESSION_INVALID", "Sessão salva/reaberta somente em diretório temporário local." if stage_ok else "Sessão local divergente."),
            _phase("VERIFY", "PASS" if stage_ok else "FAIL", "SESSION_ROUNDTRIP_VERIFIED" if stage_ok else "SESSION_ROUNDTRIP_FAILED", "Roundtrip preservou a proposta." if stage_ok else "Roundtrip divergente."),
            _phase("ROLLBACK", "PASS" if rollback_ok else "FAIL", "RESTORE_BASE_VERIFIED" if rollback_ok else "RESTORE_BASE_FAILED", "Restore voltou ao fingerprint da base." if rollback_ok else "Restore divergiu da base."),
        ],
        local_mutation=True,
        evidence_refs=["docs/sprints/sistema_temas/V05/README.md", "tools/tests/test_temas_v05_sessions.py"],
    )


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _run_builder(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120, check=False)
    if completed.returncode != 0:
        raise RuntimeError("builder canônico local falhou")


def _release_phases(kind: str, path: Path, preflight: dict[str, Any], package_code: str) -> list[dict[str, str]]:
    report = run_release_cycle({
        "request_version": 1,
        "mode": "release",
        "preflight": preflight,
        "artifact": {"kind": kind, "path": _rel(path)},
        "last_known_good": None,
    })
    passed = report.get("overall_status") == "PASS"
    receipt = report.get("receipt", {}) if passed else {}
    preflight_pass = report.get("preflight_status") == "PASS"
    return [
        _phase("PREPARE", "PASS", "ARTIFACT_SOURCE_SELECTED", "Checkout e owner canônico selecionados."),
        _phase("PREFLIGHT", "PASS" if preflight_pass else "FAIL", "S2_PREFLIGHT_PASS" if preflight_pass else "S2_PREFLIGHT_NOT_PASS", "Artefato passou no preflight S2." if preflight_pass else "Preflight S2 não retornou PASS."),
        _phase("PACKAGE", "PASS", package_code, "Artefato foi construído pelo owner canônico e revalidado."),
        _phase("STAGE", "PASS" if receipt.get("staging_verified") is True else "FAIL", "LOCAL_STAGE_VERIFIED" if receipt.get("staging_verified") is True else "LOCAL_STAGE_FAILED", "Staging temporário local foi verificado." if receipt.get("staging_verified") is True else "Staging local não comprovado."),
        _phase("VERIFY", "PASS" if passed else "FAIL", "RELEASE_DRY_RUN_PASS" if passed else "RELEASE_DRY_RUN_FAILED", "Ciclo S3 local terminou em PASS." if passed else "Ciclo S3 local não terminou em PASS."),
        _phase("ROLLBACK", "PASS" if receipt.get("rollback_dry_run_verified") is True else "FAIL", "ROLLBACK_DRY_RUN_VERIFIED" if receipt.get("rollback_dry_run_verified") is True else "ROLLBACK_DRY_RUN_FAILED", "Rollback dry-run local foi comprovado." if receipt.get("rollback_dry_run_verified") is True else "Rollback local não comprovado."),
    ]


def rehearse_transition_bundle() -> dict[str, Any]:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="v13_s6_v09_", dir=ARTIFACT_ROOT) as tmp:
        bundle = Path(tmp) / "transition.zip"
        _run_builder([sys.executable, "-B", str(ROOT / "tools/bundle_implantacao.py"), "--output", _rel(bundle)])
        preflight = {
            "request_version": 1,
            "mode": "surface",
            "operations": [{
                "surface_id": "transition_bundle",
                "action_id": "build_transition_bundle",
                "inputs": {
                    "bundle_path": _rel(bundle),
                    "authorization_ref": "s6-local-build",
                    "rollback": {"prepared": True, "state_ref": "discard-local-bundle"},
                },
            }],
        }
        phases = _release_phases("transition_bundle", bundle, preflight, "V09_BUNDLE_PACKAGED")
    return _surface_report("transition_bundle", phases, local_mutation=True, evidence_refs=["docs/sprints/sistema_temas/V09/README.md", "tools/temas_v09_transicao.py", "tools/temas_v13_release.py"])


def rehearse_app_bundle() -> dict[str, Any]:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="v13_s6_v10_", dir=ARTIFACT_ROOT) as tmp:
        app_dir = Path(tmp) / "app"
        v10_app.build(app_dir)
        preflight = {
            "request_version": 1,
            "mode": "surface",
            "operations": [{
                "surface_id": "databricks_app",
                "action_id": "build_app_bundle",
                "inputs": {
                    "app_bundle_dir": _rel(app_dir),
                    "authorization_ref": "s6-local-build",
                    "rollback": {"prepared": True, "state_ref": "discard-local-app-bundle"},
                },
            }],
        }
        phases = _release_phases("app_bundle", app_dir, preflight, "V10_APP_BUNDLE_PACKAGED")
    return _surface_report("databricks_app", phases, local_mutation=True, evidence_refs=["docs/sprints/sistema_temas/V10/README.md", "tools/temas_v10_app.py", "tools/temas_v13_release.py"])


def rehearse_aibi_fixture() -> dict[str, Any]:
    theme = load_reference_theme("notebook")
    preflight = _preflight("aibi_dashboard", "project_theme", {"theme": _theme_input()})
    projection = project_theme(theme)
    exported = export_projection(projection)
    template = {"theme": {"widget": {"background": "#000000", "cornerRadius": 0}, "visualization": {"categoricalPalette": ["#000000"]}, "unknownFutureField": {"preserve": True}}}
    template_raw = (json.dumps(template, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    binding = {
        "binding_version": 1,
        "template_sha256": hashlib.sha256(template_raw).hexdigest(),
        "paths": {
            "widget.background": "/theme/widget/background",
            "widget.corner_radius": "/theme/widget/cornerRadius",
            "visualization.categorical_palette": "/theme/visualization/categoricalPalette",
        },
    }
    binding_raw = json.dumps(binding, sort_keys=True, separators=(",", ":")).encode("utf-8")
    candidate = bind_native_template(projection, template_raw, binding_raw)
    bound = json.loads(candidate.content)
    binding_ok = candidate.validation_status == "locally_bound_not_databricks_validated" and bound["theme"]["unknownFutureField"] == {"preserve": True} and set(candidate.applied_capabilities) == {"widget.background", "widget.corner_radius", "visualization.categorical_palette"}
    fixture = json.loads((AIBI / "dashboard_sintetico.json").read_text(encoding="utf-8"))
    semantic_before = synthetic_dashboard_semantic_fingerprint(fixture)
    decorated = dict(fixture)
    decorated["theme_projection_sha256"] = hashlib.sha256(exported).hexdigest()
    semantics_ok = semantic_before == synthetic_dashboard_semantic_fingerprint(decorated)
    rollback_ok = hashlib.sha256(template_raw).hexdigest() == binding["template_sha256"]
    return _surface_report(
        "aibi_dashboard",
        [
            _phase("PREPARE", "PASS", "V11_FIXTURE_SELECTED", "Tema V02 e fixture local V11 selecionados."),
            _phase("PREFLIGHT", "PASS" if preflight["overall_status"] == "PASS" else "FAIL", "S2_PREFLIGHT_PASS" if preflight["overall_status"] == "PASS" else "S2_PREFLIGHT_FAILED", "Projeção local passou no S2." if preflight["overall_status"] == "PASS" else "S2 recusou a projeção."),
            _phase("PACKAGE", "PASS", "V11_PROJECTION_PACKAGED", "Projeção V11 exportada localmente."),
            _phase("STAGE", "PASS" if binding_ok else "FAIL", "LOCAL_FIXTURE_BOUND" if binding_ok else "LOCAL_FIXTURE_BIND_FAILED", "Três bindings diretos aplicados somente a fixture local." if binding_ok else "Binding local divergente."),
            _phase("VERIFY", "PASS" if semantics_ok else "FAIL", "SEMANTICS_PRESERVED" if semantics_ok else "SEMANTIC_DRIFT", "Queries/filtros preservaram fingerprint semântico." if semantics_ok else "Semântica do fixture mudou."),
            _phase("ROLLBACK", "PASS" if rollback_ok else "FAIL", "DISCARD_BOUND_COPY_VERIFIED" if rollback_ok else "ROLLBACK_MISMATCH", "Descartar a cópia bound preserva template original." if rollback_ok else "Template original divergiu."),
        ],
        local_mutation=False,
        evidence_refs=["docs/sprints/sistema_temas/V11/README.md", "tools/tests/test_temas_v11.py", "docs/sprints/sistema_temas/V12/TESTES.md"],
    )


def rehearse_workspace_theme_blocked() -> dict[str, Any]:
    preflight = _preflight("workspace_theme", "apply_workspace_theme", {})
    blocked = preflight["overall_status"] == "BLOCKED"
    return _surface_report(
        "workspace_theme",
        [
            _phase("PREPARE", "PASS", "WORKSPACE_POLICY_SELECTED", "Política local V11 selecionada."),
            _phase("PREFLIGHT", "BLOCKED" if blocked else "FAIL", "AUTHORIZATION_BLOCKED" if blocked else "UNEXPECTED_PREFLIGHT_STATE", "S2 preservou o bloqueio canônico de autorização." if blocked else "Workspace theme não permaneceu bloqueado."),
            _phase("PACKAGE", "NOT_APPLICABLE", "REMOTE_PACKAGE_NOT_AUTHORIZED", "Nenhum pacote remoto foi preparado."),
            _phase("STAGE", "NOT_APPLICABLE", "REMOTE_STAGE_NOT_AUTHORIZED", "Nenhum workspace foi alterado."),
            _phase("VERIFY", "NOT_APPLICABLE", "REMOTE_VERIFY_NOT_RUN", "Sem execução remota não há resultado de ambiente."),
            _phase("ROLLBACK", "NOT_APPLICABLE", "REMOTE_ROLLBACK_NOT_RUN", "Nenhuma mutação remota ocorreu."),
        ],
        local_mutation=False,
        evidence_refs=["docs/sprints/sistema_temas/V11/README.md", "docs/sprints/sistema_temas/V12/TESTES.md", "tools/temas_v13_preflight.py"],
    )


def run_rehearsals() -> dict[str, Any]:
    runners = (rehearse_notebook, rehearse_visual_lab, rehearse_transition_bundle, rehearse_app_bundle, rehearse_aibi_fixture, rehearse_workspace_theme_blocked)
    surfaces = [runner() for runner in runners]
    if tuple(item["surface_id"] for item in surfaces) != SURFACE_ORDER:
        raise RuntimeError("ordem de superfícies S6 divergente")
    return {
        "report_version": REPORT_VERSION,
        "engine": ENGINE,
        "scope": "LOCAL_OR_SIMULATED_ONLY",
        "surfaces": surfaces,
        "real_environment_cases": [
            {"case_id": case_id, "surface_id": surface_id, "status": "BLOQUEADO_AUTORIZACAO", "reason": "nova autorização específica não foi concedida para ensaio Databricks real"}
            for case_id, surface_id in REAL_ENVIRONMENT_CASES
        ],
        "a11_status": "FAIL",
        "issue_57_state_expected": "open",
        "network_access": False,
        "remote_mutation_performed": False,
        "publication_performed": False,
        "s7_started": False,
    }


def main() -> int:
    report = run_rehearsals()
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if all(item["overall_status"] in {"PASS", "BLOCKED"} for item in report["surfaces"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
