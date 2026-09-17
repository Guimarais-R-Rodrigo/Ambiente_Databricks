from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


_ALLOWED_ROOT_PACKAGES = {"hub_snippets", "hub_scripts"}


def canonical_module_parts(module: Any) -> tuple[str, ...] | None:
    """Valida e decompõe um caminho Python canônico de recurso do Hub."""
    if not isinstance(module, str):
        return None
    parts = tuple(module.split("."))
    if len(parts) < 2 or parts[0] not in _ALLOWED_ROOT_PACKAGES:
        return None
    if any(not part or not part.isidentifier() for part in parts):
        return None
    return parts


def public_exports(init_path: Path) -> set[str]:
    """Extrai exports realmente disponíveis na fachada sem executar código.

    Se ``__all__`` existir, ele funciona como filtro dos nomes que também foram
    importados ou definidos no próprio ``__init__.py``. Um nome apenas declarado
    em ``__all__`` não é considerado uma API pública resolvida.
    """
    try:
        tree = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    except (OSError, SyntaxError) as exc:
        raise ValueError(f"não foi possível analisar {init_path}: {exc}") from exc

    explicit_all: set[str] | None = None
    imported: set[str] = set()
    defined: set[str] = set()

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                defined.add(node.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                if not name.startswith("_"):
                    imported.add(name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".", 1)[0]
                if not name.startswith("_"):
                    imported.add(name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    try:
                        value = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        value = None
                    if isinstance(value, (list, tuple)) and all(
                        isinstance(item, str) for item in value
                    ):
                        explicit_all = set(value)

    available = imported | defined
    if explicit_all is None:
        return available
    return explicit_all & available


def resolve_public_symbol(
    assistant_root: Path | str,
    module: Any,
    symbol: Any,
) -> tuple[bool, str]:
    """Resolve uma API pública do Hub sem importar o módulo-alvo."""
    assistant_root = Path(assistant_root)
    module_parts = canonical_module_parts(module)
    if module_parts is None:
        return False, "module deve ser caminho Python canônico sob hub_snippets.* / hub_scripts.*"
    if not isinstance(symbol, str) or not symbol or not symbol.isidentifier():
        return False, "symbol público inválido"

    package_dir = assistant_root.joinpath(*module_parts)
    init_path = package_dir / "__init__.py"
    if not package_dir.is_dir() or not init_path.is_file():
        return False, f"fachada pública ausente para {module}"

    try:
        exports = public_exports(init_path)
    except ValueError as exc:
        return False, f"fachada pública ilegível: {exc}"

    if symbol not in exports:
        return False, f"{module}.{symbol} não exportado pela fachada pública"
    return True, "API pública resolvida estaticamente"
