"""Empacota texto UTF-8 para leitura: canonical (padrão), security, full ou task.

canonical preserva o corpus amplo sem espelho/referência congelada; security
acrescenta hashes dos arquivos enumerados pelo Git, inclusive conteúdo omitido;
full inclui todas as camadas textuais enumeradas. --incluir-espelho continua
sobrescrevendo --mode com full. Nenhum modo recupera arquivos ignorados pelo Git.

task é um recorte explícito, NÃO auditoria integral. Exige --task; aceita
--include PATH repetido e produz também <saida>.manifest.json. Consulte
 docs/ai/task-context.md. --allow-dirty inclui untracked não ignorado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

if __package__:
    from . import project_policy
    from .task_context import CONFIG, load_routes, relative_path, safe_path, select_task
else:
    import project_policy
    from task_context import CONFIG, load_routes, relative_path, safe_path, select_task

REPO_ROOT = Path(__file__).resolve().parent.parent
# O caminho antigo continua reconhecido; o novo normalmente já é ignorado pelo Git.
EXCLUIDOS_PADRAO = tuple(dict.fromkeys((
    "Novo_Ambiente_Simulado/", "Ajustes_Codex/",
    getattr(project_policy, "SIMULATED_ROOT", Path("Novo_Ambiente_Simulado")).as_posix().rstrip("/") + "/",
)))
BINARIOS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".dbc"}


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", cwd=str(REPO_ROOT)
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(args)} retornou {result.returncode}: {result.stderr.strip()}")
    return result.stdout


def _changes(status: str) -> list[dict[str, str]]:
    entries = iter(status.split("\0"))
    result = []
    for entry in entries:
        if not entry:
            continue
        change = {"status": entry[:2], "path": entry[3:]}
        if "R" in change["status"] or "C" in change["status"]:
            change["original_path"] = next(entries)
        result.append(change)
    return result


def _destination(value: str, tracked: set[str]) -> Path:
    path = Path(value)
    if not path.is_absolute():
        relative_path(value)
        path = REPO_ROOT / path
    if ".git" in path.parts or ".." in path.parts:
        raise ValueError("destino não pode escapar por '..' nem escrever em .git")
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, "is_junction", lambda: False)():
            raise ValueError("destino não pode atravessar symlink/junction")
    if path.exists() and (not path.is_file() or path.stat().st_nlink > 1):
        raise ValueError("destino deve ser arquivo regular sem hardlink")
    resolved = path.resolve()
    if resolved.is_relative_to(REPO_ROOT.resolve()):
        if resolved.relative_to(REPO_ROOT.resolve()).as_posix() in tracked:
            raise ValueError("destino não pode sobrescrever arquivo rastreado")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", help="arquivo de saída; padrão antigo nos modos integrais")
    parser.add_argument("--mode", choices=("canonical", "security", "full", "task"), default="canonical")
    parser.add_argument("--incluir-espelho", action="store_true", help="compatibilidade: equivale a --mode full")
    parser.add_argument("--allow-dirty", action="store_true", help="permite revisão do worktree sujo e untracked não ignorado")
    parser.add_argument("--task", help="nome de rota em docs/ai/task-context.json; somente --mode task")
    parser.add_argument("--include", action="append", default=[], metavar="PATH", help="arquivo exato adicional, relativo ao repositório; repetível em task")
    args = parser.parse_args(argv)
    mode = "full" if args.incluir_espelho else args.mode
    if mode == "task" and not args.task:
        parser.error("--mode task exige --task")
    if mode != "task" and (args.task or args.include):
        parser.error("--task/--include exigem --mode task sem --incluir-espelho")

    try:
        status = _git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        dirty = bool(status)
        if dirty and not args.allow_dirty:
            raise ValueError("worktree sujo; commite as mudanças ou use --allow-dirty para revisão")
        tracked = set(filter(None, _git("ls-files", "-z").split("\0")))
        if not tracked:
            raise ValueError("git ls-files não devolveu nenhum arquivo; bundle não foi criado")
        paths = set(tracked)
        if args.allow_dirty:
            paths.update(filter(None, _git("ls-files", "-z", "--others", "--exclude-standard").split("\0")))
        commit = _git("rev-parse", "HEAD").strip()
        config = config_bytes = task = selected = None
        if mode == "task":
            config, config_bytes = load_routes(REPO_ROOT)
            selected, task = select_task(config, args.task, args.include)
        default = f".artifacts/contexto-{args.task}.txt" if mode == "task" else "bundle_auditoria.txt"
        destination = _destination(args.saida or default, tracked)
        sidecar = _destination(str(destination) + ".manifest.json", tracked) if mode == "task" else None
        outputs = {p.resolve() for p in (destination, sidecar) if p is not None}
        if selected is not None:
            for rel in selected:
                candidate = safe_path(REPO_ROOT, rel)
                if rel not in paths or not candidate.is_file():
                    raise ValueError(f"seleção ausente do inventário Git ou não é arquivo: {rel}")
                if candidate.resolve() in outputs:
                    raise ValueError(f"seleção inclui a própria saída: {rel}")
                if rel.startswith(EXCLUIDOS_PADRAO):
                    raise ValueError(f"camada derivada/congelada não permitida em task: {rel}; use --mode full")

        parts: list[str] = []
        hashes: list[str] = []
        included: list[dict] = []
        excluded: list[dict[str, str]] = []
        content_bytes = 0
        for rel in sorted(paths):
            candidate = safe_path(REPO_ROOT, rel)
            reason = None
            if candidate.resolve() in outputs:
                reason = "saída do próprio comando; não realimentar contexto"
            elif selected is not None and rel not in selected:
                reason = "fora da rota e das ampliações explícitas; use --include ou modo integral"
            if reason:
                excluded.append({"path": rel, "reason": reason})
                continue
            if not candidate.is_file():
                if selected is not None:
                    raise ValueError(f"arquivo selecionado ausente: {rel}")
                excluded.append({"path": rel, "reason": "ausente ou não é arquivo regular"})
                continue
            data = candidate.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            hashes.append(f"{digest}  {rel}")
            if mode != "full" and rel.startswith(EXCLUIDOS_PADRAO):
                reason = "espelho/referência congelada excluído neste modo; expanda com --mode full"
            elif candidate.suffix.lower() in BINARIOS:
                reason = "extensão binária excluída do corpo textual"
            else:
                try:
                    content = data.decode("utf-8")
                except UnicodeDecodeError:
                    reason = "conteúdo não UTF-8 excluído do corpo textual"
            if reason:
                if selected is not None:
                    raise ValueError(f"arquivo selecionado não pode compor contexto textual: {rel}: {reason}")
                excluded.append({"path": rel, "reason": reason})
                continue
            included.append({"path": rel, "sha256": digest, "bytes": len(data),
                             "reasons": selected[rel] if selected is not None else [f"corpus {mode}"],
                             "tracked": rel in tracked})
            # Os modos anteriores usavam read_text: conservar universal newlines.
            # task preserva os bytes UTF-8 que seus hashes identificam.
            if mode != "task":
                content = content.replace("\r\n", "\n").replace("\r", "\n")
            content_bytes += len(content.encode("utf-8"))
            parts.append(f"\n\n===== ARQUIVO: {rel} =====\n{content}")
        if not included:
            raise ValueError("seleção textual vazia; bundle não foi criado")
        if mode == "security":
            parts.append("\n\n===== MANIFEST SHA256 DE TODOS OS PATHS VERSIONADOS =====\n" + "\n".join(hashes))
        title = ("CONTEXTO DE TAREFA (RECORTE; NAO E AUDITORIA INTEGRAL)" if mode == "task"
                 else "BUNDLE DO REPOSITORIO Ambiente_Databricks")
        header = (f"{title}\ncommit: {commit}\nworktree_dirty: {str(dirty).lower()}\nmodo: {mode}\n"
                  f"arquivos incluidos: {len(included)} (pulados: {len(excluded)})\n"
                  f"bytes de conteudo incluidos: {content_bytes}\npaths no manifest: {len(hashes)}\n"
                  "cada arquivo comeca com uma linha '===== ARQUIVO: <caminho> ====='\n")
        if mode == "task":
            header += (f"tarefa: {args.task}\nmanifesto: {sidecar.name}\n"
                       + "\n".join(f"limite: {item}" for item in task["exclusions"]) + "\n"
                       + "\n".join(f"expandir: {item}" for item in task["expand"]) + "\n")
        payload = (header + "".join(parts)).encode("utf-8")
        if sidecar is not None:
            manifest = {
                "schema_version": 1, "kind": "task-context-not-full-audit", "task": args.task,
                "description": task["description"], "git_commit": commit,
                "worktree_dirty": dirty, "allow_dirty": args.allow_dirty,
                "content_source": "worktree", "atomic_git_snapshot": False,
                "dirty_entries": _changes(status),
                "inventory": "git ls-files -z; untracked não ignorado somente com --allow-dirty",
                "route_config": {"path": CONFIG, "sha256": hashlib.sha256(config_bytes).hexdigest()},
                "included": included, "excluded": excluded, "exclusion_notes": task["exclusions"],
                "expand": task["expand"],
                "metrics": {"included_files": len(included), "included_content_bytes": content_bytes,
                            "excluded_files": len(excluded)},
                "bundle": {"name": destination.name, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()},
            }
            sidecar_payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        if sidecar is not None:
            sidecar.write_bytes(sidecar_payload)
        print(f"{destination.name}: {len(included)} arquivos, {content_bytes} bytes de conteúdo, {len(payload)} bytes de bundle")
        if sidecar is not None:
            print(f"{sidecar.name}: {len(sidecar_payload)} bytes de manifesto SHA-256; recorte não é auditoria integral")
        return 0
    except (OSError, ValueError, StopIteration) as exc:
        print(f"FAIL {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
