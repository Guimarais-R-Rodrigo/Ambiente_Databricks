"""Ciclo operacional local V13-S3 para release, update e rollback dry-run.

Compõe o preflight S2 e os validadores V09/V10. A ferramenta não usa rede,
credenciais Databricks nem executa mutação remota. Staging e rollback ocorrem
somente em diretório temporário local; recibo só existe após verificação completa.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.temas_v09_transicao import validate_theme_zip  # noqa: E402
from tools.temas_v10_app import MANIFEST as V10_MANIFEST  # noqa: E402
from tools.temas_v10_app import verify as verify_app_bundle  # noqa: E402
from tools.temas_v13_preflight import run_preflight  # noqa: E402

REQUEST_VERSION = 1
REPORT_VERSION = 1
RECEIPT_VERSION = 1
ENGINE = "V13-S3"
ARTIFACT_ROOT = ROOT / ".artifacts"
ARTIFACT_KINDS = {"transition_bundle", "app_bundle"}
MODES = {"release", "update", "rollback_dry_run"}
SHA256_HEX = set("0123456789abcdef")

STABLE_CODES = {
    "REQUEST_VALID",
    "REQUEST_TYPE",
    "REQUEST_FIELDS",
    "REQUEST_VERSION",
    "REQUEST_MODE",
    "ARTIFACT_DESCRIPTOR",
    "ARTIFACT_PATH_INVALID",
    "ARTIFACT_INVALID",
    "ARTIFACT_SOURCE_STALE",
    "ARTIFACT_READY",
    "TREE_CLEAN",
    "TREE_DIRTY",
    "GIT_UNAVAILABLE",
    "PREFLIGHT_PASS",
    "PREFLIGHT_BLOCKED",
    "PREFLIGHT_FAILED",
    "PREFLIGHT_BINDING_MISMATCH",
    "LKG_NOT_REQUIRED",
    "LKG_REQUIRED",
    "LKG_DESCRIPTOR_INVALID",
    "LKG_ARTIFACT_INVALID",
    "LKG_REFERENCE_VALID",
    "UPDATE_COMPATIBLE",
    "UPDATE_INCOMPATIBLE",
    "STAGING_VERIFIED",
    "ROLLBACK_DISCARD_VERIFIED",
    "ROLLBACK_RESTORE_VERIFIED",
    "LOCAL_OPERATION_FAILED",
}


class ReleaseRequestError(ValueError):
    """Entrada S3 inválida com código estável e mensagem sanitizada."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.safe_message = message
        super().__init__(f"{code}: {message}")


def _check(check_id: str, status: str, code: str, message: str) -> dict[str, str]:
    if status not in {"PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"}:
        raise ValueError("status interno inválido")
    if code not in STABLE_CODES:
        raise ValueError("código interno S3 não registrado")
    return {
        "check_id": check_id,
        "status": status,
        "code": code,
        "message": message,
    }


def _base_report(mode: str, status: str, checks: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_version": REPORT_VERSION,
        "engine": ENGINE,
        "mode": mode,
        "overall_status": status,
        "checks": checks,
        "network_access": False,
        "remote_mutation_performed": False,
        "publication_performed": False,
    }


def _is_hex(value: Any, size: int) -> bool:
    return (
        type(value) is str
        and len(value) == size
        and set(value) <= SHA256_HEX
    )


def _git_state() -> dict[str, Any]:
    """Resolve commit e exige worktree inteiro limpo; somente comandos Git read-only."""
    commands = (
        ["git", "rev-parse", "HEAD"],
        ["git", "status", "--porcelain", "--untracked-files=all"],
    )
    results = []
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        if completed.returncode != 0:
            raise ReleaseRequestError(
                "GIT_UNAVAILABLE",
                "Não foi possível resolver o estado Git local.",
            )
        results.append(completed.stdout.strip())
    return {"commit": results[0], "clean": not bool(results[1])}


def _safe_artifact_path(value: Any, *, kind: str) -> Path:
    if type(value) is not str or not value.strip():
        raise ReleaseRequestError("ARTIFACT_PATH_INVALID", "Artefato deve usar caminho relativo.")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or "\\" in value
        or ":" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise ReleaseRequestError(
            "ARTIFACT_PATH_INVALID",
            "O caminho do artefato deve ser relativo e normalizado.",
        )
    if not pure.parts or pure.parts[0] != ".artifacts":
        raise ReleaseRequestError(
            "ARTIFACT_PATH_INVALID",
            "Artefatos S3 devem permanecer sob .artifacts/ para não contaminar a árvore versionada.",
        )
    candidate = ROOT.joinpath(*pure.parts)
    current = ROOT
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ReleaseRequestError("ARTIFACT_PATH_INVALID", "Symlink não é aceito.")
    if kind == "transition_bundle" and not candidate.is_file():
        raise ReleaseRequestError("ARTIFACT_PATH_INVALID", "ZIP V09 não encontrado.")
    if kind == "app_bundle" and not candidate.is_dir():
        raise ReleaseRequestError("ARTIFACT_PATH_INVALID", "Diretório V10 não encontrado.")
    return candidate


def _file_entries_fingerprint(entries: Any) -> str:
    if type(entries) is not list:
        raise ValueError("manifesto sem files")
    normalized = []
    for entry in entries:
        if type(entry) is not dict:
            raise ValueError("entrada de manifesto inválida")
        path = entry.get("path")
        sha = entry.get("sha256")
        size = entry.get("bytes")
        if type(path) is not str or not path or not _is_hex(sha, 64) or type(size) is not int or size < 0:
            raise ValueError("entrada de manifesto inválida")
        normalized.append({"path": path, "sha256": sha, "bytes": size})
    normalized.sort(key=lambda item: item["path"])
    payload = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _snapshot_transition(path: Path) -> dict[str, Any]:
    validate_theme_zip(path)
    try:
        with zipfile.ZipFile(path) as archive:
            manifest = json.loads(archive.read("MANIFEST.json"))
    except (OSError, KeyError, zipfile.BadZipFile, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("manifesto V09 inválido") from exc
    if type(manifest) is not dict:
        raise ValueError("manifesto V09 inválido")
    schema_version = manifest.get("schema_version")
    source_commit = manifest.get("source_commit")
    dirty = manifest.get("worktree_dirty")
    theme_contract = manifest.get("theme_contract")
    if type(schema_version) is not int or schema_version < 1:
        raise ValueError("schema_version V09 inválida")
    if not _is_hex(source_commit, 40):
        raise ValueError("source_commit V09 inválido")
    if dirty is not False:
        raise ValueError("bundle V09 não pode ser release se worktree_dirty=true")
    if type(theme_contract) is not dict or type(theme_contract.get("contract_version")) is not int:
        raise ValueError("theme_contract V09 inválido")
    return {
        "kind": "transition_bundle",
        "schema_version": schema_version,
        "contract_version": theme_contract["contract_version"],
        "source_commit": source_commit,
        "content_fingerprint": _file_entries_fingerprint(manifest.get("files")),
        "container_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _snapshot_app(path: Path) -> dict[str, Any]:
    verify_app_bundle(path)
    try:
        manifest = json.loads((path / V10_MANIFEST).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("manifesto V10 inválido") from exc
    if type(manifest) is not dict:
        raise ValueError("manifesto V10 inválido")
    source_commit = manifest.get("source_commit")
    schema_version = manifest.get("schema_version")
    if not _is_hex(source_commit, 40) or type(schema_version) is not int:
        raise ValueError("identidade V10 inválida")
    return {
        "kind": "app_bundle",
        "schema_version": schema_version,
        "contract_version": schema_version,
        "source_commit": source_commit,
        "content_fingerprint": _file_entries_fingerprint(manifest.get("files")),
        "surface": manifest.get("surface"),
        "app_mode": manifest.get("app_mode"),
        "persistence": manifest.get("persistence"),
        "resource_key": manifest.get("resource_key"),
        "publication": manifest.get("publication"),
    }


def _snapshot(kind: str, path: Path) -> dict[str, Any]:
    if kind == "transition_bundle":
        return _snapshot_transition(path)
    if kind == "app_bundle":
        return _snapshot_app(path)
    raise ValueError("kind de artefato inválido")


def _validate_artifact_descriptor(value: Any) -> tuple[str, Path]:
    if type(value) is not dict or set(value) != {"kind", "path"}:
        raise ReleaseRequestError(
            "ARTIFACT_DESCRIPTOR",
            "artifact deve conter somente kind e path.",
        )
    kind = value["kind"]
    if kind not in ARTIFACT_KINDS:
        raise ReleaseRequestError(
            "ARTIFACT_DESCRIPTOR",
            "kind deve ser transition_bundle ou app_bundle.",
        )
    return kind, _safe_artifact_path(value["path"], kind=kind)


def _validate_request(request: Any) -> tuple[str, dict[str, Any], dict[str, Any], Any]:
    if type(request) is not dict:
        raise ReleaseRequestError("REQUEST_TYPE", "A entrada deve ser objeto JSON.")
    expected = {"request_version", "mode", "preflight", "artifact", "last_known_good"}
    if set(request) != expected:
        raise ReleaseRequestError("REQUEST_FIELDS", "Campos de topo S3 divergentes.")
    if request["request_version"] != REQUEST_VERSION:
        raise ReleaseRequestError("REQUEST_VERSION", "request_version deve ser 1.")
    mode = request["mode"]
    if mode not in MODES:
        raise ReleaseRequestError("REQUEST_MODE", "mode deve ser release, update ou rollback_dry_run.")
    if type(request["preflight"]) is not dict:
        raise ReleaseRequestError("REQUEST_TYPE", "preflight deve conter um request S2.")
    if request["last_known_good"] is not None and type(request["last_known_good"]) is not dict:
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "last_known_good inválido.")
    return mode, request["preflight"], request["artifact"], request["last_known_good"]


def _preflight_bound_to_artifact(preflight_request: dict[str, Any], kind: str, path: Path) -> bool:
    operations = preflight_request.get("operations")
    if type(operations) is not list or len(operations) != 1 or type(operations[0]) is not dict:
        return False
    operation = operations[0]
    inputs = operation.get("inputs")
    if type(inputs) is not dict:
        return False
    relative = path.relative_to(ROOT).as_posix()
    if kind == "transition_bundle":
        return (
            operation.get("surface_id") == "transition_bundle"
            and operation.get("action_id") == "build_transition_bundle"
            and inputs.get("bundle_path") == relative
        )
    return (
        operation.get("surface_id") == "databricks_app"
        and operation.get("action_id") == "build_app_bundle"
        and inputs.get("app_bundle_dir") == relative
    )


def _validate_lkg_descriptor(value: Any, expected_kind: str) -> tuple[Path, dict[str, Any]]:
    required = {"kind", "path", "source_commit", "artifact_fingerprint", "acceptance_ref"}
    if type(value) is not dict or set(value) != required:
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "Referência LKG incompleta.")
    if value["kind"] != expected_kind:
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "LKG pertence a outro tipo de artefato.")
    if not _is_hex(value["source_commit"], 40) or not _is_hex(value["artifact_fingerprint"], 64):
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "Identidade técnica do LKG inválida.")
    if type(value["acceptance_ref"]) is not str or not value["acceptance_ref"].strip():
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "LKG exige referência de aceite anterior.")
    path = _safe_artifact_path(value["path"], kind=expected_kind)
    try:
        snapshot = _snapshot(expected_kind, path)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise ReleaseRequestError("LKG_ARTIFACT_INVALID", "Artefato LKG não pôde ser validado.") from exc
    if (
        snapshot["source_commit"] != value["source_commit"]
        or snapshot["content_fingerprint"] != value["artifact_fingerprint"]
    ):
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "LKG não corresponde aos bytes referenciados.")
    return path, snapshot


def _compatible(lkg: dict[str, Any], candidate: dict[str, Any]) -> bool:
    if lkg["kind"] != candidate["kind"]:
        return False
    if lkg["schema_version"] != candidate["schema_version"]:
        return False
    if lkg["contract_version"] != candidate["contract_version"]:
        return False
    if candidate["kind"] == "app_bundle":
        keys = ("surface", "app_mode", "persistence", "resource_key", "publication")
        return all(lkg.get(key) == candidate.get(key) for key in keys)
    return True


def _copy_artifact(kind: str, source: Path, target: Path) -> None:
    if kind == "transition_bundle":
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return
    shutil.copytree(source, target, symlinks=False)


def _remove_artifact(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _stage_target(kind: str, directory: Path) -> Path:
    return directory / ("current.zip" if kind == "transition_bundle" else "current")


def _execute_local_dry_run(
    mode: str,
    kind: str,
    candidate_path: Path,
    candidate: dict[str, Any],
    lkg_path: Path | None,
    lkg: dict[str, Any] | None,
) -> tuple[dict[str, str], dict[str, str]]:
    with tempfile.TemporaryDirectory(prefix="v13_s3_stage_") as tmp:
        stage = Path(tmp)
        target = _stage_target(kind, stage)
        _copy_artifact(kind, candidate_path, target)
        staged = _snapshot(kind, target)
        if staged["content_fingerprint"] != candidate["content_fingerprint"]:
            raise ValueError("staging não reproduziu os bytes esperados")
        staging_check = _check(
            "staging.verify",
            "PASS",
            "STAGING_VERIFIED",
            "O artefato foi copiado para staging temporário e revalidado por conteúdo.",
        )

        if lkg_path is None or lkg is None:
            _remove_artifact(target)
            if target.exists():
                raise ValueError("rollback por descarte não removeu staging")
            rollback_check = _check(
                "rollback.dry_run",
                "PASS",
                "ROLLBACK_DISCARD_VERIFIED",
                "Rollback dry-run restaurou o estado inicial sem artefato staged.",
            )
            return staging_check, rollback_check

        _remove_artifact(target)
        _copy_artifact(kind, lkg_path, target)
        restored = _snapshot(kind, target)
        if restored["content_fingerprint"] != lkg["content_fingerprint"]:
            raise ValueError("rollback não restaurou o LKG")
        rollback_check = _check(
            "rollback.dry_run",
            "PASS",
            "ROLLBACK_RESTORE_VERIFIED",
            "Rollback dry-run restaurou e revalidou exatamente o conteúdo do LKG.",
        )
        return staging_check, rollback_check


def _receipt(
    mode: str,
    candidate: dict[str, Any],
    lkg: dict[str, Any] | None,
) -> dict[str, Any]:
    result = (
        "ROLLBACK_DRY_RUN_VERIFIED"
        if mode == "rollback_dry_run"
        else "READY_FOR_AUTHORIZED_APPLY"
    )
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "engine": ENGINE,
        "mode": mode,
        "result": result,
        "source_commit": candidate["source_commit"],
        "artifact_kind": candidate["kind"],
        "artifact_fingerprint": candidate["content_fingerprint"],
        "staging_verified": True,
        "rollback_dry_run_verified": True,
        "network_access": False,
        "remote_mutation_performed": False,
        "publication_performed": False,
    }
    if lkg is not None:
        receipt["last_known_good"] = {
            "source_commit": lkg["source_commit"],
            "artifact_fingerprint": lkg["content_fingerprint"],
        }
    return receipt


def run_release_cycle(request: Any) -> dict[str, Any]:
    """Valida release/update e prova staging/rollback somente em sandbox local."""
    mode_hint = request.get("mode") if type(request) is dict and type(request.get("mode")) is str else "invalid"
    checks: list[dict[str, str]] = []
    try:
        mode, preflight_request, artifact_descriptor, lkg_descriptor = _validate_request(request)
        kind, candidate_path = _validate_artifact_descriptor(artifact_descriptor)
        checks.append(_check("request.contract", "PASS", "REQUEST_VALID", "Request S3 válido."))

        git_state = _git_state()
        if not git_state["clean"]:
            checks.append(
                _check(
                    "git.clean_tree",
                    "FAIL",
                    "TREE_DIRTY",
                    "Release S3 exige worktree Git completamente limpo.",
                )
            )
            return _base_report(mode, "FAIL", checks)
        checks.append(
            _check(
                "git.clean_tree",
                "PASS",
                "TREE_CLEAN",
                "Worktree Git limpo antes do staging.",
            )
        )

        if not _preflight_bound_to_artifact(preflight_request, kind, candidate_path):
            checks.append(
                _check(
                    "preflight.binding",
                    "FAIL",
                    "PREFLIGHT_BINDING_MISMATCH",
                    "O preflight S2 não está fixado ao mesmo artefato/ação local.",
                )
            )
            return _base_report(mode, "FAIL", checks)

        preflight_report = run_preflight(preflight_request)
        if preflight_report["overall_status"] == "BLOCKED":
            checks.append(
                _check(
                    "preflight.result",
                    "BLOCKED",
                    "PREFLIGHT_BLOCKED",
                    "O preflight S2 manteve a operação bloqueada.",
                )
            )
            report = _base_report(mode, "BLOCKED", checks)
            report["preflight_status"] = "BLOCKED"
            return report
        if preflight_report["overall_status"] != "PASS":
            checks.append(
                _check(
                    "preflight.result",
                    "FAIL",
                    "PREFLIGHT_FAILED",
                    "O preflight S2 recusou a operação.",
                )
            )
            report = _base_report(mode, "FAIL", checks)
            report["preflight_status"] = preflight_report["overall_status"]
            return report
        checks.append(
            _check(
                "preflight.result",
                "PASS",
                "PREFLIGHT_PASS",
                "O mesmo artefato passou pelo preflight S2.",
            )
        )

        try:
            candidate = _snapshot(kind, candidate_path)
        except (OSError, ValueError, zipfile.BadZipFile):
            checks.append(
                _check(
                    "artifact.verify",
                    "FAIL",
                    "ARTIFACT_INVALID",
                    "O artefato candidato foi recusado pelo owner canônico.",
                )
            )
            return _base_report(mode, "FAIL", checks)
        if candidate["source_commit"] != git_state["commit"]:
            checks.append(
                _check(
                    "artifact.source_commit",
                    "FAIL",
                    "ARTIFACT_SOURCE_STALE",
                    "O artefato não foi gerado a partir do checkout atual.",
                )
            )
            return _base_report(mode, "FAIL", checks)
        checks.append(
            _check(
                "artifact.verify",
                "PASS",
                "ARTIFACT_READY",
                "Artefato canônico validado e fixado ao commit atual.",
            )
        )

        lkg_path: Path | None = None
        lkg: dict[str, Any] | None = None
        if mode == "release":
            if lkg_descriptor is not None:
                raise ReleaseRequestError(
                    "LKG_DESCRIPTOR_INVALID",
                    "release inicial não deve receber last_known_good.",
                )
            checks.append(
                _check(
                    "lkg.reference",
                    "NOT_APPLICABLE",
                    "LKG_NOT_REQUIRED",
                    "Release inicial usa rollback por descarte do novo staging.",
                )
            )
        else:
            if lkg_descriptor is None:
                checks.append(
                    _check(
                        "lkg.reference",
                        "FAIL",
                        "LKG_REQUIRED",
                        "Update/rollback exige last-known-good identificado.",
                    )
                )
                return _base_report(mode, "FAIL", checks)
            lkg_path, lkg = _validate_lkg_descriptor(lkg_descriptor, kind)
            checks.append(
                _check(
                    "lkg.reference",
                    "PASS",
                    "LKG_REFERENCE_VALID",
                    "LKG corresponde aos bytes e commit declarados; o aceite humano não é concedido por esta ferramenta.",
                )
            )
            if not _compatible(lkg, candidate):
                checks.append(
                    _check(
                        "update.compatibility",
                        "FAIL",
                        "UPDATE_INCOMPATIBLE",
                        "Candidate e LKG possuem versões/contratos incompatíveis para update automático.",
                    )
                )
                return _base_report(mode, "FAIL", checks)
            checks.append(
                _check(
                    "update.compatibility",
                    "PASS",
                    "UPDATE_COMPATIBLE",
                    "Candidate e LKG pertencem ao mesmo contrato de atualização.",
                )
            )

        try:
            staging_check, rollback_check = _execute_local_dry_run(
                mode, kind, candidate_path, candidate, lkg_path, lkg
            )
        except (OSError, ValueError, zipfile.BadZipFile, shutil.Error):
            checks.append(
                _check(
                    "local.operation",
                    "FAIL",
                    "LOCAL_OPERATION_FAILED",
                    "Staging/rollback local falhou; nenhum recibo de sucesso foi emitido.",
                )
            )
            return _base_report(mode, "FAIL", checks)

        checks.extend([staging_check, rollback_check])
        report = _base_report(mode, "PASS", checks)
        report["preflight_status"] = "PASS"
        report["receipt"] = _receipt(mode, candidate, lkg)
        return report

    except ReleaseRequestError as exc:
        checks.append(_check("request.contract", "FAIL", exc.code, exc.safe_message))
        return _base_report(mode_hint, "FAIL", checks)


def make_lkg_reference(
    kind: str,
    path: str,
    *,
    acceptance_ref: str,
) -> dict[str, str]:
    """Cria referência técnica verificável para um artefato já aceito externamente."""
    if kind not in ARTIFACT_KINDS:
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "kind de LKG inválido.")
    local = _safe_artifact_path(path, kind=kind)
    try:
        snapshot = _snapshot(kind, local)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise ReleaseRequestError("LKG_ARTIFACT_INVALID", "Artefato LKG inválido.") from exc
    if type(acceptance_ref) is not str or not acceptance_ref.strip():
        raise ReleaseRequestError("LKG_DESCRIPTOR_INVALID", "acceptance_ref é obrigatória.")
    return {
        "kind": kind,
        "path": path,
        "source_commit": snapshot["source_commit"],
        "artifact_fingerprint": snapshot["content_fingerprint"],
        "acceptance_ref": acceptance_ref,
    }


def _load_request(path: Path) -> Any:
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 262_144:
            raise OSError
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise ReleaseRequestError("REQUEST_TYPE", "Arquivo de request S3 inválido.") from None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa release/update/rollback V13-S3 somente como staging local dry-run."
    )
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    try:
        request = _load_request(args.request)
        report = run_release_cycle(request)
    except ReleaseRequestError as exc:
        report = _base_report(
            "invalid",
            "FAIL",
            [_check("request.contract", "FAIL", exc.code, exc.safe_message)],
        )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"PASS": 0, "NOT_APPLICABLE": 0, "BLOCKED": 2, "FAIL": 1}[report["overall_status"]]


if __name__ == "__main__":
    raise SystemExit(main())
