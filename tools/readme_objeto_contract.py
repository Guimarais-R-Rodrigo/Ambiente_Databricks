"""Contrato estrutural dos READMEs e migração monotônica, sem importar helpers.

O template do produto é a fonte dos títulos e da versão. Este gate não certifica
teoria, clareza, veracidade de fontes externas nem resultados de execução.
"""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_contract import anchors, markdown_links, mask_fences

CONTROL = Path("docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json")
TEMPLATE = Path("hub_padroes/readme/template_objeto.md")
CATEGORIES = ("constants", "display", "ml", "spark", "testing", "visual")
MARKER = re.compile(r"<!--\s*readme-objeto:\s*([^\s]+)\s*-->")
HEADINGS = re.compile(r"(?m)^## (\d+)\. (.+?)\s*$")


@dataclass(frozen=True)
class ObjectSpec:
    """Um recurso documentável, separado de índices e arquivos de apoio."""
    path: Path  # relativo a .assistant
    kind: str
    exemplar: bool = False

    @property
    def main(self) -> str:
        return self.path.name + (".md" if self.kind == "prompt" else ".py")

    @property
    def example(self) -> str:
        return f"exemplo_{self.path.name}.py"


def discover(base: Path) -> list[ObjectSpec]:
    """Inclui pastas candidatas mesmo malformadas; não confunde ausência com zero."""
    result: list[ObjectSpec] = []
    snippets = base / "hub_snippets"
    if snippets.is_dir():
        for child in snippets.iterdir():
            if child.is_dir() and child.name not in {*CATEGORIES, "tests", "__pycache__"} and not child.name.startswith("."):
                raise ValueError(f"categoria de snippets não reconhecida: {child.name}")
    parents = [(base / "hub_snippets" / c, "snippet", False) for c in CATEGORIES]
    parents += [(base / "hub_scripts", "script", False),
                (base / "hub_prompts", "prompt", False)]
    parents += [(base / "hub_padroes" / t, t, True)
                for t in ("snippet", "script", "prompt")]
    for parent, kind, exemplar in parents:
        if parent.is_symlink():
            raise ValueError(f"coleção não pode ser link simbólico: {parent}")
        if not parent.is_dir():
            continue
        for folder in sorted(parent.iterdir()):
            if folder.name.startswith(".") or folder.name == "__pycache__":
                continue
            if folder.is_symlink():
                raise ValueError(f"pasta de objeto não pode ser link simbólico: {folder}")
            if folder.is_dir():
                result.append(ObjectSpec(folder.relative_to(base), kind, exemplar))
    return result


def template_contract(text: str) -> tuple[str, list[str]]:
    markers = MARKER.findall(text)
    headings = list(HEADINGS.finditer(mask_fences(text)))
    if len(markers) != 1 or [int(m[1]) for m in headings] != list(range(1, 16)):
        raise ValueError("template precisa de uma versão e quinze seções numeradas em ordem")
    return markers[0], [m[0].strip() for m in headings]


def read_control(text: str) -> dict:
    """Recusa erro de esquema em vez de dar dispensa automática a toda a árvore."""
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError(f"chave duplicada no controle: {key}")
            out[key] = value
        return out
    data = json.loads(text, object_pairs_hook=pairs)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("schema_version do controle precisa ser 1")
    if data.get("phase") not in {"migration", "complete"}:
        raise ValueError("phase precisa ser migration ou complete")
    if not isinstance(data.get("template_version"), str):
        raise ValueError("template_version ausente")
    if not re.fullmatch(r"[0-9a-f]{40}", str(data.get("base_commit", ""))):
        raise ValueError("base_commit precisa identificar a base remota de autoria")
    pending = data.get("pending")
    if not isinstance(pending, dict):
        raise ValueError("pending precisa ser objeto JSON com caminhos explícitos")
    for key, value in pending.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9_]+(?:/[a-z0-9_]+){1,2}", key):
            raise ValueError(f"caminho de dispensa inválido: {key!r}")
        if not isinstance(value, dict) or not re.fullmatch(r"R\d{2}", str(value.get("sprint", ""))):
            raise ValueError(f"sprint ausente/inválida em {key}")
        if value.get("lote") not in {"A", "B"}:
            raise ValueError(f"lote ausente/inválido em {key}")
    if data["phase"] == "complete" and pending:
        raise ValueError("migração completa não admite objetos pendentes")
    return data


def check_ratchet(current: set[str], previous: set[str]) -> list[str]:
    """O conjunto de dispensas só diminui; retirar dispensa exige README válido."""
    return [f"dispensa nova ou reintroduzida: {p}" for p in sorted(current - previous)]


def _git(repo: Path, *args: str, allow_missing: bool = False) -> str | None:
    run = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                         text=True, encoding="utf-8", timeout=15)
    if run.returncode:
        if allow_missing:
            return None
        raise ValueError(f"histórico Git indisponível: git {' '.join(args)}")
    return run.stdout


def _ids_at(repo: Path, rev: str) -> set[str]:
    paths = _git(repo, "ls-tree", "-r", "--name-only", rev,
                 "ambiente_fonte/.assistant") or ""
    ids = set()
    for name in paths.splitlines():
        path = Path(name).relative_to("ambiente_fonte/.assistant")
        parts = path.parts
        if ((len(parts) == 4 and parts[0] == "hub_snippets" and parts[1] in CATEGORIES)
            or (len(parts) == 3 and parts[0] in {"hub_scripts", "hub_prompts"})):
            suffix = ".md" if parts[0] == "hub_prompts" else ".py"
            if path.name == path.parent.name + suffix:
                ids.add(path.parent.as_posix())
    return ids


def prior_pending(repo: Path, current: str) -> set[str]:
    """Compara worktree/commit à última versão diferente pela história first-parent.

    Na primeira introdução do controle, só pastas existentes antes dela podem
    receber dispensa. Em checkout raso, reprova: ausência de história não é prova
    de ausência de regressão. Em CI, checkout precisa de fetch-depth: 0.
    """
    if (_git(repo, "rev-parse", "--is-shallow-repository") or "").strip() == "true":
        raise ValueError("histórico raso: use fetch-depth: 0 para conferir dispensas")
    rel = CONTROL.as_posix()
    revisions = (_git(repo, "log", "--first-parent", "--format=%H", "--", rel) or "").splitlines()
    for rev in revisions:
        old = _git(repo, "show", f"{rev}:{rel}", allow_missing=True)
        if old is not None and old != current:
            return set(read_control(old)["pending"])
    # Sem versão anterior diferente, estamos na introdução do controle, ou em
    # descendentes que nunca o alteraram. Não usamos o inventário atual para
    # dispensar automaticamente um objeto recém-criado.
    ancestor = (revisions[-1] + "^") if revisions else "HEAD"
    ids = _ids_at(repo, ancestor)
    if not ids:
        raise ValueError("baseline Git sem objetos; dispensas não foram certificadas")
    return ids


def validate_readme(base: Path, spec: ObjectSpec, version: str,
                    headings: list[str]) -> list[str]:
    errors: list[str] = []
    folder = base / spec.path
    path = folder / "README.md"
    label = spec.path.as_posix()
    if folder.is_symlink() or path.is_symlink():
        return [f"{label}: README/pasta não pode ser link simbólico"]
    if not path.is_file():
        return [f"{label}: README.md obrigatório ausente"]
    text = path.read_text(encoding="utf-8")
    visible = mask_fences(text)
    if MARKER.findall(text) != [version]:
        errors.append(f"{label}: marcador de versão diferente do template")
    if len(re.findall(r"(?m)^# [^\n]+", visible)) != 1:
        errors.append(f"{label}: precisa de um único título H1")
    if not re.search(r"(?m)^## Visão rápida\s*$", visible):
        errors.append(f"{label}: Visão rápida ausente")
    matches = list(HEADINGS.finditer(visible))
    if [m[0].strip() for m in matches] != headings:
        errors.append(f"{label}: quinze seções ausentes, repetidas ou fora de ordem")
    # O corpo precisa de prosa; títulos, comentários e código isolados não
    # explicam o conceito. Não há quota de palavras nem teste automático de estilo.
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(visible)
        body = visible[match.end():end]
        body = re.sub(r"(?m)^#{1,6} .*?$", "", body).strip()
        if not body or body.lower() in {"n/a", "não se aplica", "pendente", "todo"}:
            errors.append(f"{label}: seção {match[1]} sem explicação")
    if re.search(r"\b(?:TODO|PREENCHER_AQUI|INSERIR_EXPLICACAO)\b", visible):
        errors.append(f"{label}: instrução de preenchimento não removida")
    linked: set[Path] = set()
    for match in markdown_links(text):
        target = unquote(match[1])
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue
        if parsed.scheme or parsed.netloc:
            errors.append(f"{label}: esquema de link não suportado: {target}")
            continue
        dest = (folder / parsed.path).resolve() if parsed.path else path.resolve()
        if not dest.is_relative_to(base.resolve()):
            errors.append(f"{label}: link sai do produto publicado: {target}")
            continue
        if not dest.exists():
            errors.append(f"{label}: link quebrado: {target}")
            continue
        linked.add(dest)
        if parsed.fragment and dest.suffix == ".md" and parsed.fragment not in anchors(dest.read_text(encoding="utf-8")):
            errors.append(f"{label}: âncora inexistente: {target}")
    required = [spec.main, spec.example]
    if spec.kind != "prompt":
        required.append("__init__.py")
    for name in required:
        dest = folder / name
        if not dest.is_file() or dest.is_symlink():
            errors.append(f"{label}: artefato obrigatório ausente/inválido: {name}")
        elif dest.resolve() not in linked:
            errors.append(f"{label}: falta link para {name}")
    return errors


def check_readme_objects(root: Path, problems: list[str], *,
                         repo: Path | None = None,
                         previous: set[str] | None = None) -> dict[str, int]:
    """Retorna contagens estruturais, nunca uma aprovação editorial automática."""
    base = root / ".assistant"
    repo = repo or Path(__file__).resolve().parents[1]
    counts = dict(operational=0, present=0, exemplar=0, exemplar_present=0, pending=0)
    try:
        version, headings = template_contract((base / TEMPLATE).read_text(encoding="utf-8"))
        control_text = (repo / CONTROL).read_text(encoding="utf-8")
        control = read_control(control_text)
        if control["template_version"] != version:
            raise ValueError("template e controle de migração têm versões diferentes")
        pending = set(control["pending"])
        counts["pending"] = len(pending)
        allowed = previous if previous is not None else prior_pending(repo, control_text)
        problems.extend(check_ratchet(pending, allowed))
        specs = discover(base)
        current = {s.path.as_posix() for s in specs if not s.exemplar}
        if not current:
            raise ValueError("inventário operacional vazio; cobertura não certificada")
        for ghost in sorted(pending - current):
            problems.append(f"dispensa sem objeto correspondente: {ghost}")
        for spec in specs:
            exists = (base / spec.path / "README.md").is_file()
            counts["exemplar" if spec.exemplar else "operational"] += 1
            if exists:
                counts["exemplar_present" if spec.exemplar else "present"] += 1
            if not spec.exemplar and spec.path.as_posix() in pending:
                if exists:
                    problems.append(f"{spec.path}: README presente ainda está dispensado; retire do controle")
                else:
                    continue
            problems.extend(validate_readme(base, spec, version, headings))
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        problems.append(f"READMEs de objeto não certificados: {error}")
    return counts
