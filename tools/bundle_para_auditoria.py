"""Empacota o repositório num arquivo único, para auditoria por leitura.

Existe porque auditoria de contexto longo precisa do corpus **inteiro numa
janela só** — é isso que permite ler dois documentos um contra o outro, que é a
classe de defeito que nenhum portão deste repositório pega por construção.

Exclui por padrão o que não acrescenta informação e dobraria o tamanho:

- `Novo_Ambiente_Simulado/` é cópia byte a byte de `ambiente_fonte/`;
- `Ajustes_Codex/` é referência congelada, com a nomenclatura anterior.

Uso:

    python tools/bundle_para_auditoria.py                 # bundle.txt na raiz
    python tools/bundle_para_auditoria.py --saida x.txt
    python tools/bundle_para_auditoria.py --incluir-espelho
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUIDOS_PADRAO = ("Novo_Ambiente_Simulado/", "Ajustes_Codex/")
BINARIOS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".dbc"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", default="bundle_auditoria.txt")
    parser.add_argument("--incluir-espelho", action="store_true",
                        help="inclui a camada derivada e a congelada")
    args = parser.parse_args()

    versionados = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, cwd=str(REPO_ROOT)
    ).stdout.split("\n")

    partes: list[str] = []
    incluidos = pulados = 0
    for rel in sorted(v.strip() for v in versionados if v.strip()):
        if not args.incluir_espelho and rel.startswith(EXCLUIDOS_PADRAO):
            pulados += 1
            continue
        caminho = REPO_ROOT / rel
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

    destino = REPO_ROOT / args.saida
    cabecalho = (
        f"BUNDLE DO REPOSITORIO Ambiente_Databricks\n"
        f"arquivos incluidos: {incluidos} (pulados: {pulados})\n"
        f"cada arquivo comeca com uma linha '===== ARQUIVO: <caminho> ====='\n"
    )
    destino.write_text(cabecalho + "".join(partes), encoding="utf-8")
    kb = destino.stat().st_size / 1024
    print(f"{destino.name}: {incluidos} arquivos, {kb:.0f} KB "
          f"(~{destino.stat().st_size / 4:.0f} tokens estimados)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
