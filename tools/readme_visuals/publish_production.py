"""Publica somente a camada documental visual ativa no Databricks Free.

O publicador canônico ``tools/publicar_free.py`` continua sendo o caminho para
promover o produto inteiro. Este utilitário existe para a release visual v2,
cujo blast radius permitido é deliberadamente menor:

* os cinco READMEs sob ``.assistant``; e
* toda a pasta ``.assistant/hub_readmes_visual_assets``.

O modo padrão é um plano local. ``--execute`` faz inventário e backup do
escopo remoto, recusa divergências, revalida o snapshot imediatamente antes da
primeira escrita, envia arquivos como RAW, verifica bytes brutos e, somente com
``--retire-legacy``, remove os 12 arquivos visuais aposentados. ``--verify`` é
read-only no Databricks e produz um recibo local em ``.artifacts``.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time
from typing import Iterable, Mapping


TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import publicar_free as full_publisher  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
ASSISTANT_ROOT = REPO_ROOT / "ambiente_databricks" / ".assistant"
ASSET_REL = "hub_readmes_visual_assets"
ASSET_ROOT = ASSISTANT_ROOT / ASSET_REL
QA_ROOT = REPO_ROOT / "tools" / "readme_visuals" / "qa"
BASELINE_COMMIT = "f5461d8"
ARTIFACT_ROOT = REPO_ROOT / ".artifacts" / "visual-v2" / "publication"

ACTIVE_READMES = (
    "README.md",
    "hub_snippets/README.md",
    "hub_scripts/README.md",
    "skills/README.md",
    "hub_prompts/README.md",
)
ACTIVE_README_PARENT_DIRS = ("hub_snippets", "hub_scripts", "skills", "hub_prompts")

# Conjunto fechado obtido pela diferença entre o baseline congelado e os 21
# contratos v2. Nunca transformar esta lista em glob ou deleção recursiva.
LEGACY_ASSET_PATHS = (
    "hub_readmes_visual_assets/readmes/prompts/png/01_sinergia_contexto.png",
    "hub_readmes_visual_assets/readmes/prompts/png/03_anatomia_do_briefing.png",
    "hub_readmes_visual_assets/readmes/prompts/sources/01_sinergia_contexto.svg",
    "hub_readmes_visual_assets/readmes/prompts/sources/03_anatomia_do_briefing.svg",
    "hub_readmes_visual_assets/readmes/raiz/png/04_fluxo_de_contexto.png",
    "hub_readmes_visual_assets/readmes/raiz/sources/04_fluxo_de_contexto.svg",
    "hub_readmes_visual_assets/readmes/scripts/png/03_fluxo_execucao.png",
    "hub_readmes_visual_assets/readmes/scripts/png/05_leitura_do_veredito.png",
    "hub_readmes_visual_assets/readmes/scripts/sources/03_fluxo_execucao.svg",
    "hub_readmes_visual_assets/readmes/scripts/sources/05_leitura_do_veredito.svg",
    "hub_readmes_visual_assets/readmes/skills/png/03_camadas_de_uma_skill.png",
    "hub_readmes_visual_assets/readmes/skills/sources/03_camadas_de_uma_skill.svg",
)

TEXT_SUFFIXES = frozenset({".md", ".svg", ".json", ".yaml", ".yml", ".txt"})
REMOTE_TYPES = frozenset({"FILE", "NOTEBOOK"})


class PublicationError(RuntimeError):
    """Falha segura: nenhuma etapa seguinte deve continuar."""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_text(relative: str) -> bool:
    return PurePosixPath(relative).suffix.lower() in TEXT_SUFFIXES


def _comparison_bytes(data: bytes, relative: str) -> bytes:
    """Normaliza somente quebras de linha de formatos textuais UTF-8.

    Essa representação serve apenas ao preflight de preservação. A prova
    posterior ao upload compara bytes brutos, inclusive para texto.
    """

    if not _is_text(relative):
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PublicationError(f"texto não é UTF-8: {relative}") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _equivalent_for_preflight(left: bytes, right: bytes, relative: str) -> bool:
    return _comparison_bytes(left, relative) == _comparison_bytes(right, relative)


def _safe_relative(value: str) -> str:
    """Aceita somente um caminho POSIX relativo e canônico."""

    path = PurePosixPath(value)
    if (
        not value
        or not path.parts
        or path.is_absolute()
        or "\\" in value
        or ":" in value
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.as_posix() != value
    ):
        raise PublicationError(f"caminho relativo inseguro: {value!r}")
    return value


def _validate_record_scope(records: Mapping[str, LocalFile]) -> None:
    """Fecha também a entrada programática, não apenas a CLI."""

    for relative, record in records.items():
        _safe_relative(relative)
        if relative != record.relative or not (
            relative in ACTIVE_READMES or relative.startswith(f"{ASSET_REL}/")
        ):
            raise PublicationError(f"arquivo fora do escopo documental autorizado: {relative}")


def _is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


@dataclass(frozen=True)
class LocalFile:
    relative: str
    source: Path
    content: bytes

    @property
    def sha256(self) -> str:
        return _sha(self.content)


@dataclass(frozen=True)
class RemoteFile:
    relative: str
    object_type: str
    content: bytes

    @property
    def sha256(self) -> str:
        return _sha(self.content)


@dataclass(frozen=True)
class RemoteSnapshot:
    files: Mapping[str, RemoteFile]
    directories: frozenset[str]


@dataclass(frozen=True)
class Assessment:
    conflicts: tuple[str, ...]
    legacy_present: tuple[str, ...]
    uploads: tuple[str, ...]


def collect_local_files(assistant_root: Path = ASSISTANT_ROOT) -> dict[str, LocalFile]:
    """Monta a allowlist local e recusa uma release visual incompleta."""

    asset_root = assistant_root / ASSET_REL
    if not asset_root.is_dir():
        raise PublicationError(f"pasta visual ausente: {ASSET_REL}")
    if _is_link(assistant_root) or _is_link(asset_root):
        raise PublicationError("raiz local não pode ser link simbólico ou junction")

    validation = QA_ROOT / "validation.json"
    try:
        validation_payload = json.loads(validation.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PublicationError("QA visual completo ausente ou ilegível") from exc
    if validation_payload.get("status") != "passed" or validation_payload.get("scope") != "all":
        raise PublicationError("QA visual completo não está aprovado")

    manifest = asset_root / "manifest.yaml"
    try:
        manifest_text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PublicationError("manifesto visual ausente ou não UTF-8") from exc
    if not re.search(r"(?m)^version:\s*2\s*$", manifest_text):
        raise PublicationError("manifesto visual ativo não é v2")

    symlinks = sorted(
        path.relative_to(assistant_root).as_posix()
        for path in asset_root.rglob("*")
        if _is_link(path)
    )
    if symlinks:
        raise PublicationError(f"links simbólicos não publicáveis: {', '.join(symlinks)}")

    present_legacy = [rel for rel in LEGACY_ASSET_PATHS if (assistant_root / rel).exists()]
    if present_legacy:
        raise PublicationError(
            "ativos legados ainda existem na fonte; rode a aposentadoria local protegida: "
            + ", ".join(present_legacy)
        )

    paths: list[Path] = []
    for relative in ACTIVE_READMES:
        source = assistant_root / relative
        if not source.is_file():
            raise PublicationError(f"README ativo ausente: {relative}")
        paths.append(source)
    paths.extend(sorted(path for path in asset_root.rglob("*") if path.is_file()))

    records: dict[str, LocalFile] = {}
    resolved_root = assistant_root.resolve()
    for source in paths:
        for component in (source, *source.parents):
            if component == assistant_root:
                break
            if _is_link(component):
                raise PublicationError(f"link local não publicável: {source}")
        resolved = source.resolve()
        if not resolved.is_relative_to(resolved_root):
            raise PublicationError(f"fonte escapa de .assistant: {source}")
        relative = _safe_relative(source.relative_to(assistant_root).as_posix())
        if relative in records:
            raise PublicationError(f"arquivo duplicado na allowlist: {relative}")
        content = source.read_bytes()
        if _is_text(relative):
            _comparison_bytes(content, relative)  # valida UTF-8 sem alterar bytes
        records[relative] = LocalFile(relative, source, content)
    _validate_record_scope(records)
    return records


def assert_visual_qa_is_current() -> None:
    """Reexecuta o gate; um JSON 'passed' antigo não autoriza uma release nova.

    O validador só escreve sua evidência local determinística. Não faz chamadas
    de rede, não recria imagens e não modifica os READMEs.
    """

    try:
        process = subprocess.run(
            ["node", str(Path(__file__).with_name("validate_production.mjs"))],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublicationError("não foi possível revalidar o QA visual local") from exc
    if process.returncode:
        raise PublicationError(
            "QA visual local reprovado; rode node tools/readme_visuals/validate_production.mjs"
        )


def assert_mirror_is_current(records: Mapping[str, LocalFile]) -> None:
    """Reutiliza o gate canônico e exige bytes brutos para a camada visual."""

    mirror_root, _files = full_publisher.local_tree()
    divergences = full_publisher.conferir_fonte_espelho(mirror_root)
    if divergences:
        preview = "; ".join(divergences[:5])
        suffix = f"; e mais {len(divergences) - 5}" if len(divergences) > 5 else ""
        raise PublicationError(f"espelho desatualizado: {preview}{suffix}")
    for relative, record in records.items():
        target = mirror_root / ".assistant" / relative
        try:
            content = target.read_bytes()
        except OSError as exc:
            raise PublicationError(f"arquivo visual ausente no espelho: {relative}") from exc
        if content != record.content:
            raise PublicationError(f"bytes brutos divergentes no espelho visual: {relative}")


def _git(*args: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublicationError("Git indisponível para certificar o baseline") from exc


def load_baseline(
    relative_paths: Iterable[str], commit: str = BASELINE_COMMIT
) -> tuple[str, dict[str, bytes]]:
    """Lê do Git os bytes dos alvos que existiam no baseline conhecido."""

    resolved = _git("rev-parse", "--verify", f"{commit}^{{commit}}")
    if resolved.returncode or not resolved.stdout.strip():
        raise PublicationError(f"baseline Git indisponível: {commit}")
    full_commit = resolved.stdout.decode("ascii", errors="strict").strip()

    listing = _git(
        "ls-tree",
        "-r",
        "-z",
        "--name-only",
        full_commit,
        "--",
        "ambiente_databricks/.assistant",
    )
    if listing.returncode:
        raise PublicationError("Git falhou ao inventariar o baseline")
    names = {
        item.decode("utf-8")
        for item in listing.stdout.split(b"\0")
        if item
    }

    result: dict[str, bytes] = {}
    for relative in sorted(set(relative_paths)):
        relative = _safe_relative(relative)
        repo_relative = f"ambiente_databricks/.assistant/{relative}"
        if repo_relative not in names:
            continue
        shown = _git("show", f"{full_commit}:{repo_relative}")
        if shown.returncode:
            raise PublicationError(f"Git falhou ao ler baseline de {relative}")
        result[relative] = shown.stdout
    return full_commit, result


def source_provenance(records: Mapping[str, LocalFile]) -> dict[str, object]:
    head = _git("rev-parse", "HEAD")
    if head.returncode or not head.stdout.strip():
        raise PublicationError("Git não certificou o commit da fonte")
    # Diretórios cobrem inclusões, remoções e arquivos ainda não rastreados
    # sem estourar o limite de linha de comando no Windows.
    command = ["status", "--porcelain", "--"]
    command.extend(
        [
            *(f"ambiente_databricks/.assistant/{relative}" for relative in ACTIVE_READMES),
            f"ambiente_databricks/.assistant/{ASSET_REL}",
        ]
    )
    status = _git(*command)
    if status.returncode:
        raise PublicationError("Git não certificou o estado da fonte")
    package = hashlib.sha256()
    for relative, record in sorted(records.items()):
        package.update(relative.encode("utf-8") + b"\0" + record.sha256.encode("ascii") + b"\n")
    return {
        "source_commit": head.stdout.decode("ascii").strip(),
        "scope_dirty": bool(status.stdout.strip()),
        "package_raw_sha256": package.hexdigest(),
    }


def _redact(message: str) -> str:
    value = re.sub(r"[\w.+-]+@[\w.-]+", "<user>", message)
    value = re.sub(r"(?i)(?:bearer\s+|dapi)[A-Za-z0-9._-]+", "<redacted>", value)
    value = re.sub(r"/Users/[^/\s]+", "/Users/<user>", value)
    return value.replace(str(REPO_ROOT), "<repo>")


class DatabricksClient:
    """Wrapper pequeno, sem shell, com timeout e diagnóstico redigido."""

    def __init__(self, profile: str, *, timeout: int = 90) -> None:
        if not profile.strip():
            raise PublicationError("profile vazio")
        self.profile = profile
        self.timeout = timeout

    def raw_triplet(self, *command: str) -> tuple[int, str, str]:
        try:
            process = subprocess.run(
                ["databricks", "--profile", self.profile, *command],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=self.timeout,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return 1, "", f"CLI indisponível: {type(exc).__name__}"
        return process.returncode, process.stdout or "", process.stderr or ""

    def _raw(self, *command: str) -> tuple[int, str, str]:
        return self.raw_triplet(*command, "-o", "json")

    def json(self, *command: str) -> object:
        rc, stdout, stderr = self._raw(*command)
        if rc:
            diagnostic = _redact(stderr.strip())[:700]
            raise PublicationError(
                f"Databricks CLI falhou em {' '.join(command[:2])}: "
                f"{diagnostic or f'código {rc}'}"
            )
        if not stdout.strip():
            return {}
        try:
            return json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise PublicationError(
                f"Databricks CLI devolveu JSON inválido em {' '.join(command[:2])}"
            ) from exc

    def get_status_optional(self, remote: str) -> dict[str, object] | None:
        rc, stdout, stderr = self._raw("workspace", "get-status", remote)
        if rc:
            diagnostic = f"{stderr}\n{stdout}"
            if "RESOURCE_DOES_NOT_EXIST" in diagnostic:
                return None
            # CLI 1.12.1 omite o código da API neste caso. Aceitar apenas a
            # mensagem observada, com o MESMO alvo e sem payload em stdout;
            # erros de permissão ou de outro path continuam bloqueantes.
            if (
                not stdout.strip()
                and stderr.rstrip("\r\n") == f"Error: Path ({remote}) doesn't exist."
            ):
                return None
            raise PublicationError(
                "inventário remoto falhou em get-status: "
                + (_redact(stderr.strip())[:500] or f"código {rc}")
            )
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise PublicationError("get-status remoto não devolveu JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("object_type"), str):
            raise PublicationError("get-status remoto devolveu estrutura incompleta")
        return payload

    def list_directory(self, remote: str) -> list[dict[str, object]]:
        payload = self.json("workspace", "list", remote)
        if isinstance(payload, list):
            objects = payload
        elif isinstance(payload, dict) and isinstance(payload.get("objects"), list):
            if payload.get("next_page_token"):
                raise PublicationError("listagem remota parcial; paginação não suportada")
            objects = payload["objects"]
        else:
            raise PublicationError("listagem remota devolveu estrutura incompleta")
        if not all(isinstance(item, dict) for item in objects):
            raise PublicationError("listagem remota contém objeto inválido")
        return objects

    def export(self, remote: str, object_type: str) -> bytes:
        if object_type not in REMOTE_TYPES:
            raise PublicationError(f"tipo remoto não exportável: {object_type}")
        export_format = "SOURCE" if object_type == "NOTEBOOK" else "AUTO"
        payload = self.json("workspace", "export", remote, "--format", export_format)
        content = payload.get("content") if isinstance(payload, dict) else None
        if not isinstance(content, str):
            raise PublicationError("export remoto sem conteúdo")
        try:
            return base64.b64decode(content, validate=True)
        except ValueError as exc:
            raise PublicationError("export remoto não é base64 válido") from exc

    def mkdirs(self, remote: str) -> None:
        self.json("workspace", "mkdirs", remote)

    def import_raw(self, remote: str, local: Path) -> None:
        self.json(
            "workspace",
            "import",
            remote,
            "--file",
            str(local),
            "--format",
            "RAW",
            "--overwrite",
        )

    def delete_file(self, remote: str) -> None:
        # Deliberadamente não existe parâmetro recursive neste método.
        self.json("workspace", "delete", remote)


def resolve_destination(
    client: DatabricksClient, profile: str, expected_host: str
) -> tuple[str, str]:
    """Reutiliza os guardrails de identidade e host do publicador canônico."""

    previous_profile = full_publisher.CLI_PROFILE
    previous_databricks = full_publisher.databricks
    full_publisher.CLI_PROFILE = profile
    full_publisher.databricks = client.raw_triplet
    try:
        home, user, host, actual_profile = full_publisher.resolve_home(
            expected_host=expected_host,
            require_explicit_target=True,
        )
    finally:
        full_publisher.CLI_PROFILE = previous_profile
        full_publisher.databricks = previous_databricks
    if actual_profile != profile or client.profile != profile:
        raise PublicationError("profile remoto não coincide com o destino explícito")
    if (
        not user.strip()
        or user in {".", ".."}
        or any(separator in user for separator in ("/", "\\"))
        or home != f"/Users/{user}"
    ):
        raise PublicationError("username remoto não é componente de path seguro")
    return home, host


def _remote_path(home: str, relative: str) -> str:
    relative = _safe_relative(relative)
    return f"{home}/.assistant/{relative}"


def _relative_remote(home: str, remote: str) -> str:
    prefix = f"{home}/.assistant/"
    if not remote.startswith(prefix):
        raise PublicationError("inventário remoto escapou do escopo .assistant")
    return _safe_relative(remote[len(prefix) :])


def capture_remote_snapshot(client: DatabricksClient, home: str) -> RemoteSnapshot:
    """Inventaria e exporta todo objeto existente no escopo autorizado."""

    metadata: dict[str, tuple[str, str]] = {}
    directories: set[str] = set()
    asset_remote = _remote_path(home, ASSET_REL)
    asset_status = client.get_status_optional(asset_remote)
    if asset_status is not None:
        if asset_status.get("object_type") != "DIRECTORY":
            raise PublicationError("raiz visual remota existe, mas não é diretório")
        directories.add(ASSET_REL)
        pending = [asset_remote]
        seen: set[str] = set()
        while pending:
            directory = pending.pop()
            if directory in seen:
                raise PublicationError("ciclo ou diretório duplicado no inventário remoto")
            seen.add(directory)
            for item in client.list_directory(directory):
                remote = item.get("path")
                object_type = item.get("object_type")
                if not isinstance(remote, str) or not isinstance(object_type, str):
                    raise PublicationError("objeto remoto sem path ou tipo")
                if PurePosixPath(remote).parent.as_posix() != directory:
                    raise PublicationError("listagem remota retornou objeto fora do diretório solicitado")
                relative = _relative_remote(home, remote)
                if relative != ASSET_REL and not relative.startswith(f"{ASSET_REL}/"):
                    raise PublicationError("listagem da pasta visual escapou do escopo")
                if object_type == "DIRECTORY":
                    if relative in directories:
                        raise PublicationError(f"diretório remoto duplicado: {relative}")
                    directories.add(relative)
                    pending.append(remote)
                elif object_type in REMOTE_TYPES:
                    if relative in metadata:
                        raise PublicationError(f"arquivo remoto duplicado: {relative}")
                    metadata[relative] = (remote, object_type)
                else:
                    raise PublicationError(
                        f"tipo remoto não suportado em {relative}: {object_type}"
                    )

    # Esta ferramenta atualiza documentação de um produto já instalado. Não
    # deve reconstruir silenciosamente diretórios que também abrigam runtime.
    for relative in ACTIVE_README_PARENT_DIRS:
        status = client.get_status_optional(_remote_path(home, relative))
        if status is None or status.get("object_type") != "DIRECTORY":
            raise PublicationError(
                f"diretório do produto ausente ou inválido; use a publicação integral: {relative}"
            )

    for relative in ACTIVE_READMES:
        remote = _remote_path(home, relative)
        status = client.get_status_optional(remote)
        if status is None:
            continue
        object_type = status.get("object_type")
        if object_type not in REMOTE_TYPES:
            raise PublicationError(f"alvo README remoto tem tipo inseguro: {relative}")
        metadata[relative] = (remote, str(object_type))

    files: dict[str, RemoteFile] = {}
    for relative, (remote, object_type) in sorted(metadata.items()):
        files[relative] = RemoteFile(
            relative=relative,
            object_type=object_type,
            content=client.export(remote, object_type),
        )
    return RemoteSnapshot(files=files, directories=frozenset(directories))


def _expected_asset_directories(records: Mapping[str, LocalFile]) -> set[str]:
    expected = {ASSET_REL}
    for relative in records:
        if relative == ASSET_REL or not relative.startswith(f"{ASSET_REL}/"):
            continue
        parent = PurePosixPath(relative).parent
        while parent.as_posix().startswith(ASSET_REL):
            expected.add(parent.as_posix())
            if parent.as_posix() == ASSET_REL:
                break
            parent = parent.parent
    return expected


def assess_preflight(
    snapshot: RemoteSnapshot,
    records: Mapping[str, LocalFile],
    baseline: Mapping[str, bytes],
    *,
    allow_legacy_retirement: bool,
) -> Assessment:
    """Autoriza somente estado remoto conhecido: baseline ou fonte atual."""

    _validate_record_scope(records)
    conflicts: list[str] = []
    uploads: list[str] = []
    expected = set(records)
    remote = set(snapshot.files)

    for relative in sorted(expected & remote):
        remote_file = snapshot.files[relative]
        local_file = records[relative]
        if remote_file.object_type != "FILE":
            conflicts.append(f"tipo remoto divergente em {relative}: {remote_file.object_type}")
            continue
        same_local = _equivalent_for_preflight(
            remote_file.content, local_file.content, relative
        )
        old = baseline.get(relative)
        same_baseline = old is not None and _equivalent_for_preflight(
            remote_file.content, old, relative
        )
        if not (same_local or same_baseline):
            conflicts.append(f"alteração remota independente em {relative}")
        if remote_file.content != local_file.content:
            uploads.append(relative)

    uploads.extend(sorted(expected - remote))

    unexpected_files = sorted(remote - expected)
    legacy_present: list[str] = []
    for relative in unexpected_files:
        remote_file = snapshot.files[relative]
        if relative not in LEGACY_ASSET_PATHS:
            conflicts.append(f"arquivo remoto inesperado no escopo visual: {relative}")
            continue
        legacy_present.append(relative)
        old = baseline.get(relative)
        if (
            remote_file.object_type != "FILE"
            or old is None
            or remote_file.content != old
        ):
            conflicts.append(f"legado remoto não coincide byte a byte com baseline: {relative}")

    unexpected_dirs = sorted(
        set(snapshot.directories) - _expected_asset_directories(records)
    )
    conflicts.extend(
        f"diretório remoto inesperado no escopo visual: {relative}"
        for relative in unexpected_dirs
    )
    if legacy_present and not allow_legacy_retirement:
        conflicts.append(
            "12 legados só podem ser removidos com autorização explícita --retire-legacy"
        )
    return Assessment(
        conflicts=tuple(conflicts),
        legacy_present=tuple(sorted(legacy_present)),
        uploads=tuple(sorted(set(uploads))),
    )


def verify_snapshot(
    snapshot: RemoteSnapshot, records: Mapping[str, LocalFile]
) -> tuple[list[str], list[dict[str, object]]]:
    """Compara FILEs RAW sem qualquer normalização."""

    _validate_record_scope(records)
    problems: list[str] = []
    evidence: list[dict[str, object]] = []
    expected = set(records)
    remote = set(snapshot.files)
    for relative in sorted(expected - remote):
        problems.append(f"ausente no remoto: {relative}")
    for relative in sorted(remote - expected):
        problems.append(f"objeto remoto inesperado: {relative}")
    for relative in sorted(expected & remote):
        local_file = records[relative]
        remote_file = snapshot.files[relative]
        if remote_file.object_type != "FILE":
            problems.append(f"tipo remoto divergente em {relative}: {remote_file.object_type}")
        if remote_file.content != local_file.content:
            problems.append(f"bytes remotos divergentes: {relative}")
        elif remote_file.object_type == "FILE":
            evidence.append(
                {
                    "path": relative,
                    "type": "FILE",
                    "raw_sha256": local_file.sha256,
                    "bytes": len(local_file.content),
                }
            )
    unexpected_dirs = sorted(
        set(snapshot.directories) - _expected_asset_directories(records)
    )
    problems.extend(f"diretório remoto inesperado: {item}" for item in unexpected_dirs)
    return problems, evidence


def _snapshot_signature(snapshot: RemoteSnapshot) -> tuple[tuple[object, ...], ...]:
    file_rows = tuple(
        ("file", relative, item.object_type, item.sha256)
        for relative, item in sorted(snapshot.files.items())
    )
    dir_rows = tuple(("dir", relative) for relative in sorted(snapshot.directories))
    return file_rows + dir_rows


def _records_signature(records: Mapping[str, LocalFile]) -> tuple[tuple[str, str], ...]:
    return tuple((relative, item.sha256) for relative, item in sorted(records.items()))


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _new_run_directory(kind: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    path = ARTIFACT_ROOT / f"{stamp}_{kind}_{os.getpid()}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def stage_payload(records: Mapping[str, LocalFile], run_directory: Path) -> dict[str, Path]:
    """Congela os bytes locais que serão enviados e evita TOCTOU da fonte."""

    _validate_record_scope(records)
    payload_root = run_directory / "payload"
    staged: dict[str, Path] = {}
    for relative, record in sorted(records.items()):
        target = payload_root.joinpath(*PurePosixPath(relative).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(record.content)
        staged[relative] = target
    return staged


def backup_snapshot(snapshot: RemoteSnapshot, run_directory: Path) -> Path:
    """Salva todos os objetos remotos existentes como blobs endereçados por hash."""

    blob_root = run_directory / "remote-backup" / "blobs"
    entries: list[dict[str, object]] = []
    for relative, record in sorted(snapshot.files.items()):
        blob = blob_root / f"{record.sha256}.bin"
        if not blob.exists():
            blob.parent.mkdir(parents=True, exist_ok=True)
            blob.write_bytes(record.content)
        if blob.read_bytes() != record.content:
            raise PublicationError(f"backup remoto corrompido ou incompleto: {relative}")
        entries.append(
            {
                "path": f"$USER_ROOT/.assistant/{relative}",
                "type": record.object_type,
                "raw_sha256": record.sha256,
                "bytes": len(record.content),
                "blob": blob.relative_to(run_directory).as_posix(),
            }
        )
    manifest = run_directory / "remote-backup" / "manifest.json"
    _write_json(
        manifest,
        {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "scope": "$USER_ROOT/.assistant: five READMEs + hub_readmes_visual_assets",
            "files": entries,
            "directories": sorted(snapshot.directories),
        },
    )
    return manifest


def _verify_one_raw(
    client: DatabricksClient, home: str, relative: str, expected: bytes
) -> None:
    remote = _remote_path(home, relative)
    status = client.get_status_optional(remote)
    if status is None or status.get("object_type") != "FILE":
        raise PublicationError(f"upload não produziu FILE em {relative}")
    actual = client.export(remote, "FILE")
    if actual != expected:
        raise PublicationError(f"upload não preservou bytes brutos em {relative}")


def _assert_target_unchanged(
    client: DatabricksClient,
    home: str,
    relative: str,
    previous: RemoteFile | None,
) -> None:
    """Reduz a janela entre o snapshot global e cada overwrite/criação.

    A API de workspace não oferece compare-and-swap neste fluxo; não há
    garantia atômica contra uma edição concorrente depois desta leitura.
    """

    remote = _remote_path(home, relative)
    status = client.get_status_optional(remote)
    if previous is None:
        if status is not None:
            raise PublicationError(f"alvo remoto apareceu antes do envio: {relative}")
        return
    if status is None or status.get("object_type") != previous.object_type:
        raise PublicationError(f"alvo remoto mudou de tipo/estado antes do envio: {relative}")
    current = client.export(remote, previous.object_type)
    if current != previous.content:
        raise PublicationError(f"alvo remoto mudou antes do envio: {relative}")


def _upload_with_retry(
    client: DatabricksClient,
    remote: str,
    local: Path,
    *,
    previous: RemoteFile | None,
    attempts: int = 3,
) -> None:
    """Após erro ambíguo, reconcilia o alvo antes de qualquer novo overwrite."""

    if attempts < 1:
        raise PublicationError("número de tentativas de upload deve ser positivo")
    expected = local.read_bytes()
    last_error: PublicationError | None = None
    for attempt in range(attempts):
        try:
            client.import_raw(remote, local)
            return
        except PublicationError as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(attempt + 1)
            if local.read_bytes() != expected:
                raise PublicationError("payload local mudou entre tentativas de upload")
            status = client.get_status_optional(remote)
            if status is not None:
                if status.get("object_type") != "FILE":
                    raise PublicationError("alvo de upload mudou de tipo após falha; retry bloqueado") from exc
                current = client.export(remote, "FILE")
                if current == expected:
                    return  # A chamada concluiu, mas a resposta se perdeu.
                if previous is None or current != previous.content:
                    raise PublicationError("alvo de upload mudou após falha; retry bloqueado") from exc
            elif previous is not None:
                raise PublicationError("alvo de upload desapareceu após falha; retry bloqueado") from exc
    assert last_error is not None
    raise last_error


def execute_release(
    client: DatabricksClient,
    home: str,
    records: Mapping[str, LocalFile],
    baseline_commit: str,
    baseline: Mapping[str, bytes],
    provenance: Mapping[str, object],
    *,
    retire_legacy: bool,
    run_directory: Path | None = None,
    assistant_root: Path = ASSISTANT_ROOT,
) -> Path:
    """Executa a promoção alvo-fechado e devolve o caminho do recibo."""

    run_directory = run_directory or _new_run_directory("execute")
    staged = stage_payload(records, run_directory)
    receipt_path = run_directory / "receipt.json"
    changed: list[str] = []
    deleted: list[str] = []
    receipt: dict[str, object] = {
        "status": "started",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "destination": "$USER_ROOT/.assistant",
        "baseline_commit": baseline_commit,
        **provenance,
        "scope": {
            "active_readmes": list(ACTIVE_READMES),
            "asset_tree": ASSET_REL,
            "files": len(records),
        },
    }
    _write_json(receipt_path, receipt)
    try:
        print("preflight: inventariando e exportando o escopo remoto", file=sys.stderr, flush=True)
        first = capture_remote_snapshot(client, home)
        backup = backup_snapshot(first, run_directory)
        receipt["backup_manifest"] = backup.relative_to(run_directory).as_posix()
        assessment = assess_preflight(
            first,
            records,
            baseline,
            allow_legacy_retirement=retire_legacy,
        )
        receipt["preflight"] = {
            "remote_files": len(first.files),
            "uploads": list(assessment.uploads),
            "legacy_present": list(assessment.legacy_present),
            "conflicts": list(assessment.conflicts),
        }
        _write_json(receipt_path, receipt)
        if assessment.conflicts:
            raise PublicationError("preflight bloqueado: " + "; ".join(assessment.conflicts))
        print(f"preflight: backup validado; {len(assessment.uploads)} envios e {len(assessment.legacy_present)} legados", file=sys.stderr, flush=True)

        # Revalida fonte e remoto depois do backup, imediatamente antes da
        # primeira escrita. Qualquer diferença encerra sem mutação remota.
        fresh_records = collect_local_files(assistant_root)
        if _records_signature(fresh_records) != _records_signature(records):
            raise PublicationError("fonte local mudou durante o preflight")
        second = capture_remote_snapshot(client, home)
        if _snapshot_signature(second) != _snapshot_signature(first):
            raise PublicationError("escopo remoto mudou durante o preflight")
        second_assessment = assess_preflight(
            second,
            records,
            baseline,
            allow_legacy_retirement=retire_legacy,
        )
        if second_assessment.conflicts:
            raise PublicationError(
                "revalidação bloqueada: " + "; ".join(second_assessment.conflicts)
            )

        uploads = list(second_assessment.uploads)
        uploads.sort(key=lambda rel: (rel in ACTIVE_READMES, rel))
        directories = sorted(
            {
                PurePosixPath(relative).parent.as_posix()
                for relative in uploads
                if relative.startswith(f"{ASSET_REL}/")
            },
            key=lambda item: (item.count("/"), item),
        )
        for relative in directories:
            client.mkdirs(_remote_path(home, relative))

        for position, relative in enumerate(uploads, 1):
            record = records[relative]
            if staged[relative].read_bytes() != record.content:
                raise PublicationError(f"payload local mudou antes do envio: {relative}")
            _assert_target_unchanged(client, home, relative, second.files.get(relative))
            _upload_with_retry(
                client,
                _remote_path(home, relative),
                staged[relative],
                previous=second.files.get(relative),
            )
            _verify_one_raw(client, home, relative, record.content)
            changed.append(relative)
            if position % 10 == 0 or position == len(uploads):
                print(f"envio e verificação RAW: {position}/{len(uploads)}", file=sys.stderr, flush=True)

        if retire_legacy:
            print("aposentadoria: conferência individual dos legados com backup", file=sys.stderr, flush=True)
            for relative in second_assessment.legacy_present:
                status = client.get_status_optional(_remote_path(home, relative))
                if status is None:
                    raise PublicationError(f"legado desapareceu antes da remoção: {relative}")
                if status.get("object_type") != "FILE":
                    raise PublicationError(f"legado mudou de tipo antes da remoção: {relative}")
                current = client.export(_remote_path(home, relative), "FILE")
                old = baseline.get(relative)
                if old is None or current != old or current != second.files[relative].content:
                    raise PublicationError(f"legado mudou antes da remoção: {relative}")
                client.delete_file(_remote_path(home, relative))
                if client.get_status_optional(_remote_path(home, relative)) is not None:
                    raise PublicationError(f"legado permaneceu após remoção: {relative}")
                deleted.append(relative)

        print("verificação final: inventário e bytes do escopo completo", file=sys.stderr, flush=True)
        final = capture_remote_snapshot(client, home)
        problems, evidence = verify_snapshot(final, records)
        if problems:
            raise PublicationError("verificação final falhou: " + "; ".join(problems))
        receipt.update(
            {
                "status": "verified",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "uploaded": changed,
                "deleted_legacy": deleted,
                "files_verified_raw": len(evidence),
                "files": evidence,
            }
        )
        _write_json(receipt_path, receipt)
        return receipt_path
    except Exception as exc:
        receipt.update(
            {
                "status": "failed",
                "failed_at": datetime.now(timezone.utc).isoformat(),
                "error": _redact(str(exc)),
                "uploaded_before_failure": changed,
                "deleted_before_failure": deleted,
            }
        )
        _write_json(receipt_path, receipt)
        raise


def verify_release(
    client: DatabricksClient,
    home: str,
    records: Mapping[str, LocalFile],
    provenance: Mapping[str, object],
    *,
    run_directory: Path | None = None,
) -> Path:
    run_directory = run_directory or _new_run_directory("verify")
    snapshot = capture_remote_snapshot(client, home)
    problems, evidence = verify_snapshot(snapshot, records)
    receipt = {
        "status": "verified" if not problems else "failed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "destination": "$USER_ROOT/.assistant",
        **provenance,
        "scope": {
            "active_readmes": list(ACTIVE_READMES),
            "asset_tree": ASSET_REL,
            "files": len(records),
        },
        "files_verified_raw": len(evidence),
        "files": evidence,
        "errors": problems,
    }
    receipt_path = run_directory / "receipt.json"
    _write_json(receipt_path, receipt)
    if problems:
        raise PublicationError("verify reprovado: " + "; ".join(problems))
    return receipt_path


def build_plan(
    records: Mapping[str, LocalFile], baseline_commit: str, provenance: Mapping[str, object]
) -> dict[str, object]:
    asset_files = sum(relative.startswith(f"{ASSET_REL}/") for relative in records)
    return {
        "mode": "plan",
        "remote_calls": 0,
        "destination": "$USER_ROOT/.assistant",
        "baseline_commit": baseline_commit,
        **provenance,
        "scope": {
            "active_readmes": list(ACTIVE_READMES),
            "asset_tree": ASSET_REL,
            "asset_files": asset_files,
            "total_files": len(records),
        },
        "legacy_files": list(LEGACY_ASSET_PATHS),
        "next": "use --execute --retire-legacy with explicit --profile and --expected-host",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true", help="publica e verifica")
    mode.add_argument("--verify", action="store_true", help="somente verifica o remoto")
    parser.add_argument(
        "--retire-legacy",
        action="store_true",
        help="com --execute, autoriza remover somente os 12 arquivos legados conhecidos",
    )
    parser.add_argument(
        "--profile", default=os.getenv("DATABRICKS_FREE_PROFILE"), help="profile Free explícito"
    )
    parser.add_argument(
        "--expected-host",
        default=os.getenv("DATABRICKS_FREE_HOST"),
        help="origem HTTPS exata do Databricks Free",
    )
    args = parser.parse_args(argv)

    if args.retire_legacy and not args.execute:
        parser.error("--retire-legacy só pode ser usado com --execute")
    if (args.execute or args.verify) and (not args.profile or not args.expected_host):
        parser.error("--execute/--verify exigem --profile e --expected-host")

    try:
        assert_visual_qa_is_current()
        records = collect_local_files()
        assert_mirror_is_current(records)
        baseline_commit, baseline = load_baseline(
            [*records, *LEGACY_ASSET_PATHS]
        )
        provenance = source_provenance(records)
        if not args.execute and not args.verify:
            print(json.dumps(build_plan(records, baseline_commit, provenance), ensure_ascii=False, indent=2))
            return 0

        client = DatabricksClient(args.profile)
        home, host = resolve_destination(client, args.profile, args.expected_host)
        provenance["target_identity_sha256"] = _sha(
            f"{host}\0{args.profile}\0{home}".encode("utf-8")
        )
        if args.verify:
            receipt = verify_release(client, home, records, provenance)
        else:
            receipt = execute_release(
                client,
                home,
                records,
                baseline_commit,
                baseline,
                provenance,
                retire_legacy=args.retire_legacy,
            )
        print(
            json.dumps(
                {
                    "status": "verified",
                    "receipt": receipt.relative_to(REPO_ROOT).as_posix(),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (PublicationError, SystemExit) as exc:
        print(f"FAIL {_redact(str(exc))}")
        return 1


if __name__ == "__main__":
    # JSON e diagnósticos preservam o mesmo encoding sob PowerShell e pipes.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    raise SystemExit(main())
