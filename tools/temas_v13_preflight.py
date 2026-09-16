"""Preflight operacional unificado V13-S2.

Ferramenta local, determinística e read-only. Compõe contratos já integrados
(V02, V09, V10, V11 e a matriz S1) para dizer se uma operação está preparada.
Não usa rede, credenciais Databricks nem executa mutação local/remota.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "ambiente_fonte" / ".assistant"
AIBI = PRODUCT / "hub_padroes" / "identidade_visual" / "aibi"
for _path in (ROOT, PRODUCT, AIBI):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from tools import temas_v13_operacional as s1_contract  # noqa: E402
from tools.temas_v09_transicao import validate_theme_zip  # noqa: E402
from tools.temas_v10_app import verify as verify_app_bundle  # noqa: E402
from hub_snippets.visual.tema import ThemeError, load_theme  # noqa: E402
from aibi_theme import (  # noqa: E402
    AibiThemeError,
    bind_native_template,
    project_theme,
    workspace_theme_policy,
)

REPORT_VERSION = 1
REQUEST_VERSION = 1
ENGINE = "V13-S2"
MAX_INPUT_BYTES = 262_144

STATUSES = {"PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"}
STATUS_PRIORITY = {"NOT_APPLICABLE": 0, "PASS": 1, "BLOCKED": 2, "FAIL": 3}
HARD_AUTH_STATES = {"BLOQUEADO_AUTORIZACAO", "NOT_AUTHORIZED"}

STABLE_CODES = {
    "REQUEST_VALID",
    "REQUEST_TYPE",
    "REQUEST_FIELDS",
    "REQUEST_VERSION",
    "REQUEST_MODE",
    "REQUEST_OPERATIONS",
    "REQUEST_OPERATION_COUNT",
    "REQUEST_OPERATION_DUPLICATE",
    "OPERATION_FIELDS",
    "OPERATION_INPUTS",
    "S1_CONTRACT_VALID",
    "S1_CONTRACT_INVALID",
    "SURFACE_ACTION_VALID",
    "SURFACE_UNKNOWN",
    "ACTION_UNKNOWN",
    "PATH_INVALID",
    "PATH_MISSING",
    "THEME_VALID",
    "THEME_INPUT_REQUIRED",
    "THEME_INVALID",
    "THEME_HASH_STALE",
    "CONTEXT_INCOMPATIBLE",
    "BUNDLE_VALID",
    "BUNDLE_INPUT_REQUIRED",
    "BUNDLE_INCOMPLETE",
    "APP_BUNDLE_VALID",
    "APP_BUNDLE_INPUT_REQUIRED",
    "APP_BUNDLE_INVALID",
    "APP_STORAGE_VALID",
    "APP_STORAGE_NOT_APPLICABLE",
    "APP_STORAGE_PRECONDITION",
    "AIBI_PROJECTION_VALID",
    "AIBI_BINDING_VALID",
    "AIBI_BINDING_NOT_APPLICABLE",
    "AIBI_BINDING_INPUT_REQUIRED",
    "AIBI_BINDING_INVALID",
    "AIBI_CAPABILITY_FORBIDDEN",
    "NATIVE_TEMPLATE_HASH_STALE",
    "NATIVE_TEMPLATE_SYNTHETIC",
    "JSON_POINTER_MISSING",
    "WORKSPACE_POLICY_VALID",
    "AUTHORIZATION_NOT_REQUIRED",
    "AUTHORIZATION_REQUIRED",
    "AUTHORIZATION_DECLARED",
    "AUTHORIZATION_CANONICALLY_BLOCKED",
    "IDENTITY_NOT_REQUIRED",
    "IDENTITY_REQUIRED",
    "IDENTITY_LIVE_UNVERIFIED",
    "ROLLBACK_NOT_REQUIRED",
    "ROLLBACK_NOT_PREPARED",
    "ROLLBACK_PREPARED",
    "ROLLBACK_CANONICALLY_BLOCKED",
}


class PreflightRequestError(ValueError):
    """Entrada de preflight inválida, com código estável."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.safe_message = message
        super().__init__(f"{code}: {message}")


def _check(check_id: str, status: str, code: str, message: str) -> dict[str, str]:
    if status not in STATUSES:
        raise ValueError("status interno inválido")
    if code not in STABLE_CODES:
        raise ValueError("código interno não registrado")
    return {
        "check_id": check_id,
        "status": status,
        "code": code,
        "message": message,
    }


def _status(checks: list[dict[str, str]]) -> str:
    if not checks:
        return "NOT_APPLICABLE"
    return max((item["status"] for item in checks), key=STATUS_PRIORITY.__getitem__)


def _request_failure(mode: str, code: str, message: str) -> dict[str, Any]:
    return {
        "report_version": REPORT_VERSION,
        "engine": ENGINE,
        "mode": mode,
        "overall_status": "FAIL",
        "request_checks": [_check("request.contract", "FAIL", code, message)],
        "operations": [],
        "network_access": False,
        "remote_mutation_performed": False,
    }


def _validate_request(request: Any) -> tuple[str, list[dict[str, Any]]]:
    if type(request) is not dict:
        raise PreflightRequestError("REQUEST_TYPE", "A entrada deve ser um objeto JSON.")
    if set(request) != {"request_version", "mode", "operations"}:
        raise PreflightRequestError(
            "REQUEST_FIELDS",
            "Use somente request_version, mode e operations no topo.",
        )
    if request["request_version"] != REQUEST_VERSION:
        raise PreflightRequestError("REQUEST_VERSION", "request_version deve ser 1.")
    mode = request["mode"]
    if mode not in {"surface", "aggregate"}:
        raise PreflightRequestError("REQUEST_MODE", "mode deve ser surface ou aggregate.")
    operations = request["operations"]
    if type(operations) is not list or not operations:
        raise PreflightRequestError("REQUEST_OPERATIONS", "operations deve ser lista não vazia.")
    if mode == "surface" and len(operations) != 1:
        raise PreflightRequestError(
            "REQUEST_OPERATION_COUNT",
            "O modo surface exige exatamente uma operação.",
        )

    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in operations:
        if type(item) is not dict or set(item) != {"surface_id", "action_id", "inputs"}:
            raise PreflightRequestError(
                "OPERATION_FIELDS",
                "Cada operação deve conter somente surface_id, action_id e inputs.",
            )
        surface_id = item["surface_id"]
        action_id = item["action_id"]
        inputs = item["inputs"]
        if type(surface_id) is not str or not surface_id:
            raise PreflightRequestError("OPERATION_FIELDS", "surface_id deve ser texto não vazio.")
        if type(action_id) is not str or not action_id:
            raise PreflightRequestError("OPERATION_FIELDS", "action_id deve ser texto não vazio.")
        if type(inputs) is not dict:
            raise PreflightRequestError("OPERATION_INPUTS", "inputs deve ser um objeto JSON.")
        key = (surface_id, action_id)
        if key in seen:
            raise PreflightRequestError(
                "REQUEST_OPERATION_DUPLICATE",
                "A mesma superfície/ação não pode aparecer duas vezes.",
            )
        seen.add(key)
        normalized.append(
            {"surface_id": surface_id, "action_id": action_id, "inputs": inputs}
        )

    if mode == "aggregate":
        normalized.sort(key=lambda item: (item["surface_id"], item["action_id"]))
    return mode, normalized


def _safe_repo_path(value: Any, *, kind: str) -> Path:
    if type(value) is not str or not value.strip():
        raise PreflightRequestError("PATH_INVALID", "Informe um caminho relativo do repositório.")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or "\\" in value
        or ":" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise PreflightRequestError("PATH_INVALID", "O caminho deve permanecer dentro do repositório.")
    candidate = ROOT.joinpath(*pure.parts)
    try:
        relative = candidate.relative_to(ROOT)
    except ValueError:
        raise PreflightRequestError("PATH_INVALID", "O caminho deve permanecer dentro do repositório.") from None

    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise PreflightRequestError("PATH_INVALID", "Symlink não é aceito no preflight.")
    if kind == "file" and not candidate.is_file():
        raise PreflightRequestError("PATH_MISSING", "Arquivo local requerido não foi encontrado.")
    if kind == "dir" and not candidate.is_dir():
        raise PreflightRequestError("PATH_MISSING", "Diretório local requerido não foi encontrado.")
    return candidate


def _surface_and_action(
    matrix: dict[str, Any], surface_id: str, action_id: str
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, str]]]:
    surface = next(
        (item for item in matrix["surfaces"] if item["surface_id"] == surface_id),
        None,
    )
    if surface is None:
        return None, None, [
            _check(
                "operation.selection",
                "FAIL",
                "SURFACE_UNKNOWN",
                "A superfície não pertence ao inventário operacional S1.",
            )
        ]
    action = next(
        (item for item in surface["actions"] if item["action_id"] == action_id),
        None,
    )
    if action is None:
        return surface, None, [
            _check(
                "operation.selection",
                "FAIL",
                "ACTION_UNKNOWN",
                "A ação não pertence à superfície selecionada.",
            )
        ]
    return surface, action, [
        _check(
            "operation.selection",
            "PASS",
            "SURFACE_ACTION_VALID",
            "Superfície e ação existem na matriz operacional S1.",
        )
    ]


def _theme_preflight(inputs: dict[str, Any]) -> tuple[Any | None, dict[str, str]]:
    theme = inputs.get("theme")
    if type(theme) is not dict:
        return None, _check(
            "theme.contract",
            "FAIL",
            "THEME_INPUT_REQUIRED",
            "A operação exige um tema explicitamente fixado.",
        )
    required = {"root_ref", "relative_path", "expected_sha256", "expected_context"}
    if set(theme) != required:
        return None, _check(
            "theme.contract",
            "FAIL",
            "THEME_INPUT_REQUIRED",
            "O tema deve declarar raiz, caminho, SHA-256 esperado e contexto.",
        )
    try:
        root = _safe_repo_path(theme["root_ref"], kind="dir")
        resolved = load_theme(
            root,
            theme["relative_path"],
            expected_sha256=theme["expected_sha256"],
            expected_context=theme["expected_context"],
        )
    except PreflightRequestError:
        return None, _check(
            "theme.contract",
            "FAIL",
            "THEME_INVALID",
            "O caminho local do tema não atende ao contrato do preflight.",
        )
    except ThemeError as exc:
        if exc.code == "HASH_MISMATCH":
            code = "THEME_HASH_STALE"
            message = "Os bytes do tema divergem do SHA-256 fixado."
        elif exc.code in {"CONTEXT_MISMATCH", "CONTEXT_EXPECTED"}:
            code = "CONTEXT_INCOMPATIBLE"
            message = "O contexto do tema é incompatível com a operação."
        else:
            code = "THEME_INVALID"
            message = "O núcleo V02 recusou o tema."
        return None, _check("theme.contract", "FAIL", code, message)
    return resolved, _check(
        "theme.contract",
        "PASS",
        "THEME_VALID",
        "O tema foi validado pelo núcleo V02 com hash e contexto explícitos.",
    )


def _bundle_preflight(inputs: dict[str, Any]) -> dict[str, str]:
    value = inputs.get("bundle_path")
    if value is None:
        return _check(
            "artifact.transition_bundle",
            "FAIL",
            "BUNDLE_INPUT_REQUIRED",
            "Informe o ZIP candidato do bundle V09.",
        )
    try:
        path = _safe_repo_path(value, kind="file")
        validate_theme_zip(path)
    except (PreflightRequestError, OSError, ValueError):
        return _check(
            "artifact.transition_bundle",
            "FAIL",
            "BUNDLE_INCOMPLETE",
            "O bundle V09 não atende ao contrato de presença e hashes.",
        )
    return _check(
        "artifact.transition_bundle",
        "PASS",
        "BUNDLE_VALID",
        "O bundle V09 atende ao contrato local de transporte e hashes.",
    )


def _app_bundle_preflight(inputs: dict[str, Any]) -> dict[str, str]:
    value = inputs.get("app_bundle_dir")
    if value is None:
        return _check(
            "artifact.app_bundle",
            "FAIL",
            "APP_BUNDLE_INPUT_REQUIRED",
            "Informe o diretório candidato do bundle V10.",
        )
    try:
        path = _safe_repo_path(value, kind="dir")
        verify_app_bundle(path)
    except (PreflightRequestError, OSError, ValueError):
        return _check(
            "artifact.app_bundle",
            "FAIL",
            "APP_BUNDLE_INVALID",
            "O bundle V10 foi recusado pelo verificador canônico.",
        )
    return _check(
        "artifact.app_bundle",
        "PASS",
        "APP_BUNDLE_VALID",
        "O bundle V10 foi aceito pelo verificador canônico.",
    )


def _storage_preflight(action_id: str, inputs: dict[str, Any]) -> dict[str, str]:
    if action_id != "deploy_app":
        return _check(
            "environment.app_storage",
            "NOT_APPLICABLE",
            "APP_STORAGE_NOT_APPLICABLE",
            "Storage remoto não é requisito desta ação.",
        )
    value = inputs.get("storage_path")
    valid = (
        type(value) is str
        and value.startswith("/Volumes/")
        and "\\" not in value
        and ".." not in PurePosixPath(value).parts
    )
    if not valid:
        return _check(
            "environment.app_storage",
            "FAIL",
            "APP_STORAGE_PRECONDITION",
            "Deploy do App exige destino /Volumes/ explícito e normalizado.",
        )
    return _check(
        "environment.app_storage",
        "PASS",
        "APP_STORAGE_VALID",
        "O destino declarado atende ao formato de UC Volume exigido pelo contrato V10.",
    )


def _read_repo_bytes(inputs: dict[str, Any], key: str) -> bytes:
    path = _safe_repo_path(inputs.get(key), kind="file")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise PreflightRequestError("PATH_INVALID", "O arquivo local excede o limite do preflight.")
    return path.read_bytes()


def _aibi_binding_preflight(
    action_id: str,
    inputs: dict[str, Any],
    resolved_theme: Any | None,
) -> list[dict[str, str]]:
    if action_id == "publish_dashboard":
        return [
            _check(
                "aibi.binding",
                "NOT_APPLICABLE",
                "AIBI_BINDING_NOT_APPLICABLE",
                "Publish é gate separado e não cria binding nativo nesta etapa.",
            )
        ]
    if resolved_theme is None:
        return []
    try:
        projection = project_theme(resolved_theme)
    except AibiThemeError:
        return [
            _check(
                "aibi.projection",
                "FAIL",
                "AIBI_BINDING_INVALID",
                "A ponte V11 recusou a projeção do tema.",
            )
        ]
    checks = [
        _check(
            "aibi.projection",
            "PASS",
            "AIBI_PROJECTION_VALID",
            "A projeção V11 foi calculada sem ampliar os três bindings diretos.",
        )
    ]
    if action_id == "project_theme":
        checks.append(
            _check(
                "aibi.binding",
                "NOT_APPLICABLE",
                "AIBI_BINDING_NOT_APPLICABLE",
                "A projeção local não exige template nativo nem binding.",
            )
        )
        return checks
    if action_id != "import_theme_draft":
        return checks
    if "native_template_path" not in inputs or "binding_path" not in inputs:
        checks.append(
            _check(
                "aibi.binding",
                "FAIL",
                "AIBI_BINDING_INPUT_REQUIRED",
                "Import em draft exige template nativo e binding explicitamente fixados.",
            )
        )
        return checks
    try:
        template_raw = _read_repo_bytes(inputs, "native_template_path")
        binding_raw = _read_repo_bytes(inputs, "binding_path")
        try:
            template_obj = json.loads(template_raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            template_obj = None
        if (
            type(template_obj) is dict
            and template_obj.get("kind") == "hub_v11_synthetic_dashboard_draft"
        ):
            checks.append(
                _check(
                    "aibi.binding",
                    "FAIL",
                    "NATIVE_TEMPLATE_SYNTHETIC",
                    "O fixture sintético V11 não pode ser usado como export nativo.",
                )
            )
            return checks
        bind_native_template(projection, template_raw, binding_raw)
    except PreflightRequestError:
        checks.append(
            _check(
                "aibi.binding",
                "FAIL",
                "AIBI_BINDING_INVALID",
                "Template ou binding local não atende ao contrato de entrada.",
            )
        )
    except AibiThemeError as exc:
        mapping = {
            "AIBI_BINDING_HASH": (
                "NATIVE_TEMPLATE_HASH_STALE",
                "O binding não está fixado aos bytes atuais do template.",
            ),
            "AIBI_BINDING_PATH": (
                "JSON_POINTER_MISSING",
                "Um JSON Pointer do binding não existe no template.",
            ),
            "AIBI_BINDING_CAPABILITY": (
                "AIBI_CAPABILITY_FORBIDDEN",
                "O binding tentou automatizar capacidade fora do conjunto direto V11.",
            ),
        }
        code, message = mapping.get(
            exc.code,
            ("AIBI_BINDING_INVALID", "A ponte V11 recusou template ou binding."),
        )
        checks.append(_check("aibi.binding", "FAIL", code, message))
    else:
        checks.append(
            _check(
                "aibi.binding",
                "PASS",
                "AIBI_BINDING_VALID",
                "O binding foi aplicado localmente aos campos já existentes do template.",
            )
        )
    return checks


def _workspace_policy_preflight() -> dict[str, str]:
    try:
        policy = workspace_theme_policy()
        valid = policy.get("workspace_admin_required_for_manage") is True
    except Exception:
        valid = False
    if not valid:
        return _check(
            "workspace.policy",
            "FAIL",
            "AIBI_BINDING_INVALID",
            "A política local V11 de workspace theme está inconsistente.",
        )
    return _check(
        "workspace.policy",
        "PASS",
        "WORKSPACE_POLICY_VALID",
        "A política V11 confirma que workspace theme é superfície administrativa separada.",
    )


def _authorization_preflight(action: dict[str, Any], inputs: dict[str, Any]) -> dict[str, str]:
    auth = action["authorization"]
    if not auth["required"]:
        return _check(
            "governance.authorization",
            "NOT_APPLICABLE",
            "AUTHORIZATION_NOT_REQUIRED",
            "A ação é read-only e não exige autorização de mutação.",
        )
    if auth["state"] in HARD_AUTH_STATES:
        return _check(
            "governance.authorization",
            "BLOCKED",
            "AUTHORIZATION_CANONICALLY_BLOCKED",
            "O owner canônico mantém esta ação sem autorização operacional.",
        )
    ref = inputs.get("authorization_ref")
    if type(ref) is not str or not ref.strip():
        return _check(
            "governance.authorization",
            "BLOCKED",
            "AUTHORIZATION_REQUIRED",
            "A ação mutável exige referência explícita de autorização.",
        )
    return _check(
        "governance.authorization",
        "PASS",
        "AUTHORIZATION_DECLARED",
        "Há referência explícita de autorização; o preflight não concede nem autentica essa autorização.",
    )


def _identity_preflight(action: dict[str, Any], inputs: dict[str, Any]) -> dict[str, str]:
    if action["mode"] not in {"persistent_mutation", "remote_mutation"}:
        return _check(
            "environment.identity",
            "NOT_APPLICABLE",
            "IDENTITY_NOT_REQUIRED",
            "A ação não depende de identidade efetiva de ambiente.",
        )
    ref = inputs.get("identity_ref")
    if type(ref) is not str or not ref.strip():
        return _check(
            "environment.identity",
            "BLOCKED",
            "IDENTITY_REQUIRED",
            "A operação depende de identidade efetiva e nenhuma evidência foi referenciada.",
        )
    return _check(
        "environment.identity",
        "BLOCKED",
        "IDENTITY_LIVE_UNVERIFIED",
        "Uma referência foi fornecida, mas o núcleo local S2 não autentica identidade efetiva no Databricks.",
    )


def _rollback_preflight(action: dict[str, Any], inputs: dict[str, Any]) -> dict[str, str]:
    rollback = action["rollback"]
    if not rollback["required"]:
        return _check(
            "recovery.rollback",
            "NOT_APPLICABLE",
            "ROLLBACK_NOT_REQUIRED",
            "A ação não produz mutação persistente e não exige rollback.",
        )
    if rollback["strategy"].startswith("blocked_until_"):
        return _check(
            "recovery.rollback",
            "BLOCKED",
            "ROLLBACK_CANONICALLY_BLOCKED",
            "O owner canônico ainda não declara rollback operacional executável para esta ação.",
        )
    value = inputs.get("rollback")
    valid = (
        type(value) is dict
        and set(value) == {"prepared", "state_ref"}
        and value["prepared"] is True
        and type(value["state_ref"]) is str
        and bool(value["state_ref"].strip())
    )
    if not valid:
        return _check(
            "recovery.rollback",
            "BLOCKED",
            "ROLLBACK_NOT_PREPARED",
            "A ação mutável exige rollback preparado e referência do estado anterior.",
        )
    return _check(
        "recovery.rollback",
        "PASS",
        "ROLLBACK_PREPARED",
        "O pedido declara rollback preparado e estado anterior identificável.",
    )


def _surface_checks(
    surface_id: str,
    action_id: str,
    inputs: dict[str, Any],
) -> list[dict[str, str]]:
    if surface_id == "notebook_visual_core":
        _, check = _theme_preflight(inputs)
        return [check]

    if surface_id == "visual_lab":
        _, check = _theme_preflight(inputs)
        return [check]

    if surface_id == "transition_bundle":
        return [_bundle_preflight(inputs)]

    if surface_id == "databricks_app":
        return [_app_bundle_preflight(inputs), _storage_preflight(action_id, inputs)]

    if surface_id == "aibi_dashboard":
        if action_id == "publish_dashboard":
            return _aibi_binding_preflight(action_id, inputs, None)
        resolved, theme_check = _theme_preflight(inputs)
        return [theme_check, *_aibi_binding_preflight(action_id, inputs, resolved)]

    if surface_id == "workspace_theme":
        return [_workspace_policy_preflight()]

    return []


def _preflight_operation(matrix: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    surface_id = item["surface_id"]
    action_id = item["action_id"]
    inputs = item["inputs"]

    surface, action, selection_checks = _surface_and_action(matrix, surface_id, action_id)
    checks = list(selection_checks)
    if surface is None or action is None:
        return {
            "surface_id": surface_id,
            "action_id": action_id,
            "status": _status(checks),
            "checks": checks,
        }

    checks.extend(_surface_checks(surface_id, action_id, inputs))
    checks.append(_authorization_preflight(action, inputs))
    checks.append(_identity_preflight(action, inputs))
    checks.append(_rollback_preflight(action, inputs))
    return {
        "surface_id": surface_id,
        "action_id": action_id,
        "status": _status(checks),
        "checks": checks,
    }


def run_preflight(request: Any) -> dict[str, Any]:
    """Executa preflight local sem rede ou mutação e retorna relatório determinístico."""
    mode_hint = request.get("mode") if type(request) is dict and type(request.get("mode")) is str else "invalid"
    try:
        mode, operations = _validate_request(request)
    except PreflightRequestError as exc:
        return _request_failure(mode_hint, exc.code, exc.safe_message)

    try:
        matrix = s1_contract.validate_file()
    except (OSError, ValueError, s1_contract.OperationalContractError):
        return {
            "report_version": REPORT_VERSION,
            "engine": ENGINE,
            "mode": mode,
            "overall_status": "FAIL",
            "request_checks": [
                _check(
                    "s1.contract",
                    "FAIL",
                    "S1_CONTRACT_INVALID",
                    "A matriz operacional S1 não pôde ser validada.",
                )
            ],
            "operations": [],
            "network_access": False,
            "remote_mutation_performed": False,
        }

    results = [_preflight_operation(matrix, item) for item in operations]
    overall = max(
        (item["status"] for item in results),
        key=STATUS_PRIORITY.__getitem__,
        default="NOT_APPLICABLE",
    )
    return {
        "report_version": REPORT_VERSION,
        "engine": ENGINE,
        "mode": mode,
        "overall_status": overall,
        "request_checks": [
            _check(
                "request.contract",
                "PASS",
                "REQUEST_VALID",
                "A entrada atende ao contrato V13-S2.",
            ),
            _check(
                "s1.contract",
                "PASS",
                "S1_CONTRACT_VALID",
                "A matriz S1 foi validada e é consumida apenas por referência.",
            ),
        ],
        "operations": results,
        "network_access": False,
        "remote_mutation_performed": False,
    }


def _load_request(path: Path) -> Any:
    path = Path(path)
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_INPUT_BYTES:
            raise OSError
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise PreflightRequestError("REQUEST_TYPE", "O arquivo de request não pôde ser lido como JSON local.") from None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa o preflight operacional V13-S2 sem rede ou mutação Databricks."
    )
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()

    try:
        request = _load_request(args.request)
        report = run_preflight(request)
    except PreflightRequestError as exc:
        report = _request_failure("invalid", exc.code, exc.safe_message)

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"PASS": 0, "NOT_APPLICABLE": 0, "BLOCKED": 2, "FAIL": 1}[report["overall_status"]]


if __name__ == "__main__":
    raise SystemExit(main())
