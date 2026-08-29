"""Empacota o repositório num arquivo único, para auditoria por leitura.

Existe porque auditoria de contexto longo precisa do corpus **inteiro numa
janela só** — é isso que permite ler dois documentos um contra o outro, que é a
classe de defeito que nenhum portão deste repositório pega por construção.

O modo padrão `canonical` exclui o espelho e a referência congelada para revisar
a lógica sem duplicação. `security` acrescenta um manifesto SHA-256 de todos os
paths versionados, inclusive os omitidos do conteúdo. `full` inclui todas as
camadas textuais versionadas.

Uso:

    python tools/bundle_para_auditoria.py                 # bundle.txt na raiz
    python tools/bundle_para_auditoria.py --saida x.txt
    python tools/bundle_para_auditoria.py --mode security
    python tools/bundle_para_auditoria.py --mode full
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUIDOS_PADRAO = ("Novo_Ambiente_Simulado/", "Ajustes_Codex/")
BINARIOS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".dbc"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", default="bundle_auditoria.txt")
    parser.add_argument(
        "--mode",
        choices=("canonical", "security", "full"),
        default="canonical",
        help=("canonical: corpus editável; security: corpus + manifest de todos os "
              "paths/hashes; full: conteúdo de todas as camadas versionadas"),
    )
    parser.add_argument(
        "--incluir-espelho",
        action="store_true",
        help="compatibilidade: equivale a --mode full",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="permite bundle de revisão do worktree sujo e inclui untracked não ignorado",
    )
    args = parser.parse_args()

    mode = "full" if args.incluir_espelho else args.mode

    status = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if status.returncode != 0:
        print(f"FAIL git status retornou {status.returncode}: {status.stderr.strip()}")
        return 1
    dirty = bool(status.stdout.strip())
    if dirty and not args.allow_dirty:
        print("FAIL worktree sujo; commite as mudanças ou use --allow-dirty para revisão")
        return 1

    list_args = ["git", "ls-files"]
    if args.allow_dirty:
        list_args += ["--cached", "--others", "--exclude-standard"]
    git_files = subprocess.run(
        list_args, capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if git_files.returncode != 0:
        print(f"FAIL git ls-files retornou {git_files.returncode}: {git_files.stderr.strip()}")
        return 1
    versionados = [item.strip() for item in git_files.stdout.splitlines() if item.strip()]
    if not versionados:
        print("FAIL git ls-files não devolveu nenhum arquivo; bundle não foi criado")
        return 1

    git_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if git_commit.returncode != 0:
        print(f"FAIL git rev-parse retornou {git_commit.returncode}: {git_commit.stderr.strip()}")
        return 1
    commit = git_commit.stdout.strip()

    partes: list[str] = []
    manifest: list[str] = []
    incluidos = pulados = 0
    for rel in sorted(versionados):
        caminho = REPO_ROOT / rel
        if caminho.is_file():
            try:
                digest = hashlib.sha256(caminho.read_bytes()).hexdigest()
            except OSError as exc:
                print(f"FAIL não foi possível ler {rel}: {exc}")
                return 1
            manifest.append(f"{digest}  {rel}")
        if mode != "full" and rel.startswith(EXCLUIDOS_PADRAO):
            pulados += 1
            continue
        if caminho.suffix.lower() in BINARIOS or not caminho.is_file():
            pulados += 1
            continue
        try:
            conteudo = caminho.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            pulados += 1
            continue
        incluidos += 1
        partes.append(f"\n\n===== ARQUIVO: {rel} =====\n{conteudo}")

    if mode == "security":
        partes.append(
            "\n\n===== MANIFEST SHA256 DE TODOS OS PATHS VERSIONADOS =====\n"
            + "\n".join(manifest)
        )

    destino = REPO_ROOT / args.saida
    cabecalho = (
        f"BUNDLE DO REPOSITORIO Ambiente_Databricks\n"
        f"commit: {commit}\n"
        f"worktree_dirty: {str(dirty).lower()}\n"
        f"modo: {mode}\n"
        f"arquivos incluidos: {incluidos} (pulados: {pulados})\n"
        f"paths no manifest: {len(manifest)}\n"
        f"cada arquivo comeca com uma linha '===== ARQUIVO: <caminho> ====='\n"
    )
    destino.write_text(cabecalho + "".join(partes), encoding="utf-8")
    kb = destino.stat().st_size / 1024
    print(f"{destino.name}: {incluidos} arquivos, {kb:.0f} KB "
          f"(~{destino.stat().st_size / 4:.0f} tokens estimados)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
