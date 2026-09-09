"""Gate local do repositório: roda sem credencial do Databricks.

    python tools/ci_local.py

Executa, em ordem, e sempre até o fim — um gate que para no primeiro erro
esconde os outros e obriga a rodar de novo para cada um:

1. `validate_assistant.py`  — forma, links, contratos, identidade e higiene;
2. `hub_snippets/tests/test_core.py`   — regressões da biblioteca;
3. `tools/tests/test_tool_guards.py`   — guardas das próprias ferramentas.

O que este gate **não** faz, por decisão do plano consolidado: nada que precise
de credencial, rede ou runtime Databricks. Publicação, verify remoto, smoke em
Spark e testes conversacionais do Genie Code são etapas próprias, com evidência
datada. Um gate que mistura os dois nunca roda em máquina nova nem em CI.

Dependências declaradas em `tools/requirements-dev.txt`:

    python -m pip install -r tools/requirements-dev.txt
"""

from __future__ import annotations

import argparse
import importlib.util
import locale
import os
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# (módulo importável, pacote em requirements-dev.txt). O nome importável nem
# sempre é o nome do pacote — checar o import evita um "instalado" que não
# importa.
DEPENDENCIAS = [
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("plotly", "plotly"),
]

ETAPAS = [
    (
        "validacao",
        "validação local do ambiente_fonte",
        [sys.executable, "tools/validate_assistant.py"],
    ),
    (
        "biblioteca",
        "regressões de hub_snippets",
        [sys.executable, "ambiente_fonte/.assistant/hub_snippets/tests/test_core.py"],
    ),
    (
        "ferramentas",
        "guardas de tools/",
        [sys.executable, "tools/tests/test_tool_guards.py"],
    ),
]


def conferir_dependencias() -> list[str]:
    """Devolve os pacotes ausentes, pelo nome com que se instala."""
    ausentes = []
    for modulo, pacote in DEPENDENCIAS:
        if importlib.util.find_spec(modulo) is None:
            ausentes.append(pacote)
    return ausentes


def _decodificar(dados: bytes) -> str:
    """Decodifica a saída do filho sem nunca levantar.

    No Windows o console usa cp1252 e o filho escreve nele; decodificar como
    UTF-8 estrito levanta `UnicodeDecodeError` **dentro da thread leitora** do
    subprocess. A exceção é impressa e engolida, a saída volta vazia, e a etapa
    reprova sem mostrar a causa. Um gate que esconde o motivo do erro é pior que
    gate nenhum.
    """
    for codificacao in ("utf-8", locale.getpreferredencoding(False)):
        try:
            return dados.decode(codificacao)
        except (UnicodeDecodeError, LookupError):
            continue
    return dados.decode("utf-8", errors="replace")


def rodar(comando: list[str], mostrar_saida: bool) -> tuple[int, str, float]:
    # As três etapas são Python: pedir UTF-8 ao filho resolve a origem do
    # problema. A decodificação tolerante acima é a rede de segurança para
    # qualquer saída que ainda escape disso.
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    inicio = time.monotonic()
    proc = subprocess.run(comando, cwd=RAIZ, capture_output=True, env=ambiente)
    duracao = time.monotonic() - inicio
    saida = _decodificar((proc.stdout or b"") + (proc.stderr or b""))
    if mostrar_saida:
        print(saida.rstrip())
    return proc.returncode, saida, duracao


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verbose", action="store_true", help="mostra a saída completa de cada etapa"
    )
    parser.add_argument(
        "--etapa",
        choices=[nome for nome, _, _ in ETAPAS],
        help="roda apenas uma etapa, pelo nome",
    )
    args = parser.parse_args()

    print("== GATE LOCAL ==")
    print(f"raiz    : {RAIZ}")
    print(f"python  : {sys.version.split()[0]}")

    ausentes = conferir_dependencias()
    if ausentes:
        print("\nFAIL dependências de teste ausentes: " + ", ".join(ausentes))
        print("     python -m pip install -r tools/requirements-dev.txt")
        return 2

    etapas = [e for e in ETAPAS if args.etapa is None or e[0] == args.etapa]
    resultados: list[tuple[str, int, float, str]] = []
    for nome, descricao, comando in etapas:
        print(f"\n-- {nome}: {descricao}")
        codigo, saida, duracao = rodar(comando, args.verbose)
        ultima = ""
        for linha in reversed(saida.strip().splitlines()):
            if linha.strip():
                ultima = linha.strip()[:100]
                break
        estado = "OK  " if codigo == 0 else "FAIL"
        print(f"   {estado} ({duracao:.1f}s) {ultima}")
        if codigo != 0 and not args.verbose:
            print("   --- saída da etapa que reprovou ---")
            print("   " + saida.strip().replace("\n", "\n   ")[:4000])
        resultados.append((nome, codigo, duracao, ultima))

    print("\n== RESUMO ==")
    for nome, codigo, duracao, _ in resultados:
        print(f"  {'OK  ' if codigo == 0 else 'FAIL'} {nome:<12} {duracao:6.1f}s")

    reprovadas = [nome for nome, codigo, _, _ in resultados if codigo != 0]
    print()
    print("alcance : gate local — não cobre Databricks, Spark nem Genie Code")
    if reprovadas:
        print(f"REPROVADO: {len(reprovadas)} etapa(s) — {', '.join(reprovadas)}")
        return 1
    print(f"APROVADO: {len(resultados)} etapa(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
