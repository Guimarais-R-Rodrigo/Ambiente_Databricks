"""Rotas explícitas e limitadas para o contexto de tarefa, sem busca recursiva."""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath

CONFIG = "docs/ai/task-context.json"
MAX_ROUTE_FILES = 32


def relative_path(value: str) -> str:
    """Aceita somente um path de arquivo relativo, portátil e sem glob."""
    if (not isinstance(value, str) or not value or "\\" in value
            or any(ord(char) < 32 for char in value) or ":" in value
            or any(char in value for char in "*?[]")
            or PurePosixPath(value).is_absolute()
            or any(part in ("", ".", "..", ".git") for part in value.split("/"))):
        raise ValueError(f"path relativo inválido: {value!r}")
    return value


def safe_path(root: Path, relative: str) -> Path:
    relative_path(relative)
    candidate = root
    for part in relative.split("/"):
        candidate /= part
        if candidate.is_symlink() or getattr(candidate, "is_junction", lambda: False)():
            raise ValueError(f"symlink/junction não permitido: {relative}")
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"path fora do repositório: {relative}")
    return candidate


def _files(value: object, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value or len(value) > MAX_ROUTE_FILES:
        raise ValueError(f"{label}: seleção deve conter 1–{MAX_ROUTE_FILES} arquivos exatos")
    result = []
    seen = set()
    for item in value:
        if not isinstance(item, dict) or set(item) != {"path", "reason"}:
            raise ValueError(f"{label}: cada arquivo exige path e reason")
        path = relative_path(item["path"])
        if path in seen or not isinstance(item["reason"], str) or not item["reason"].strip():
            raise ValueError(f"{label}: path duplicado ou motivo vazio: {path}")
        seen.add(path)
        result.append(item)
    return result


def load_routes(root: Path) -> tuple[dict, bytes]:
    data = safe_path(root, CONFIG).read_bytes()
    if len(data) > 131072:
        raise ValueError("configuração de rotas excede 128 KiB")
    config = json.loads(data.decode("utf-8"))
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError("schema_version de rotas deve ser 1")
    _files(config.get("common"), "common")
    tasks = config.get("tasks")
    if not isinstance(tasks, dict) or not tasks:
        raise ValueError("configuração sem tarefas")
    for name, task in tasks.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name) or not isinstance(task, dict):
            raise ValueError(f"tarefa inválida: {name!r}")
        if not isinstance(task.get("description"), str) or not task["description"].strip():
            raise ValueError(f"{name}: descrição ausente")
        _files(task.get("files"), name)
        for field in ("exclusions", "expand"):
            items = task.get(field)
            if (not isinstance(items, list) or not items
                    or any(not isinstance(item, str) or not item.strip() for item in items)):
                raise ValueError(f"{name}: {field} deve explicar os limites e a expansão")
    return config, data


def select_task(config: dict, name: str, extra: list[str]) -> tuple[dict[str, list[str]], dict]:
    if name not in config["tasks"]:
        raise ValueError(f"tarefa desconhecida: {name!r}; opções: {', '.join(config['tasks'])}")
    task = config["tasks"][name]
    selected: dict[str, list[str]] = {}
    for item in config["common"] + task["files"]:
        selected.setdefault(item["path"], []).append(item["reason"])
    for path in extra:
        relative_path(path)
        selected.setdefault(path, []).append("Ampliação explícita por --include")
    if not selected:
        raise ValueError("seleção de tarefa vazia")
    return selected, task
