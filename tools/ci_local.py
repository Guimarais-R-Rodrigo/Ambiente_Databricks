"""Gate local do repositório: roda sem credencial do Databricks.

    python tools/ci_local.py

Executa, em ordem, e sempre até o fim — um gate que para no primeiro erro
esconde os outros e obriga a rodar de novo para cada um:

1. Temas — assets/geração V06 + Visual Lab V05 + HTML/tabelas V04 + Plotly V03 + núcleo V02 + contrato V01 (todas as `test_temas*.py`)
2. `validate_assistant.py`  — forma, links, contratos, identidade e higiene;
3. Skill Enforcement — perfil SE08 cumulativo em modo local read-only, sem renderer;
4. `hub_snippets/tests/test_core.py`   — regressões da biblioteca;
5. `tools/tests/test_tool_guards.py`   — guardas das próprias ferramentas.
6. `tools/tests/test_transicao_trabalho.py` — kit, notebook e guardas de aceite.
7. READMEs — contrato, migração e regressões de convivência com o Concierge;
8. Concierge — estrutura do pacote;
9. Concierge — regressões do verificador;
10. Concierge — integração canônica e espelho.
   Essas etapas não avaliam roteamento conversacional; esse gate continua no Genie Code.

O que este gate **não** faz, por decisão do plano consolidado: nada que precise
de credencial, rede ou runtime Databricks. Publicação, verify remoto, smoke em
Spark e testes conversacionais do Genie Code são etapas próprias, com evidência
datada. Um gate que mistura os dois nunca roda em máquina nova nem em CI.

A certificação SEF completa, incluindo renderer e evidence bundle, permanece em:

    python -B tools/skill_enforcement/certify_local.py --profile se08

Dependências Python declaradas em `tools/requirements-dev.txt`:

    python -m pip install -r tools/requirements-dev.txt

A V06 também exercita o compositor Node local. Prepare as dependências fixadas
antes de rodar o gate completo:

    npm install --global pnpm@10.34.5
    pnpm --dir tools/readme_visuals install --frozen-lockfile

O gate não instala dependências automaticamente nem faz chamadas ao Databricks.
"""

from __future__ import annotations

import argparse
import importlib.util
import locale
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# (módulo importável, pacote em requirements-dev.txt). O nome importável nem
# sempre é o nome do pacote — checar o import evita um "instalado" que não
# importa.
DEPENDENCIAS = [
    ("jsonschema", "jsonschema"),
    ("referencing", "referencing"),
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("plotly", "plotly"),
    ("jinja2", "jinja2"),
]

# A V06 chama o compositor Node pelos testes. Conferimos somente presença local
# das dependências declaradas; instalação automática continuaria sendo efeito de
# rede impróprio para um gate local/fail-closed.
DEPENDENCIAS_NODE = [
    "@fontsource/inter/package.json",
    "@svgdotjs/svg.js/package.json",
    "fontkit/package.json",
    "lucide-static/package.json",
    "sharp/package.json",
    "svgdom/package.json",
    "yaml/package.json",
]

ETAPAS = [
    (
        "temas", "Sistema de temas V06 + V05 + V04 + V03 + V02 + V01",
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_temas*.py", "-v"],
    ),
    (
        "validacao",
        "validação local do ambiente_fonte",
        [sys.executable, "tools/validate_assistant.py", "--conferir-readme"],
    ),
    (
        "sef",
        "Skill Enforcement SE08 — gate local cumulativo parcial sem renderer",
        [
            sys.executable,
            "-B",
            "tools/skill_enforcement/certify_local.py",
            "--profile",
            "se08",
            "--skip-render",
            "--no-evidence",
            "--allow-dirty",
        ],
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
    (
        "transicao",
        "guardas do kit e notebook de aceite (Spark opcional separado)",
        [sys.executable, "tools/tests/test_transicao_trabalho.py"],
    ),
    (
        "micromodelos",
        "contratos e aceite do módulo Micromodelos extraído",
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_micromodelo*.py", "-v"],
    ),
    (
        "micromodelos-pacote",
        "aceite sintético do produto Micromodelos isolado do checkout",
        [sys.executable, "-B", "tools/tests/test_aceite_micromodelos_trabalho.py", "-v"],
    ),
    (
        "readmes",
        "contrato dos READMEs, dispensas monotônicas e integração com Concierge",
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_readme*.py", "-v"],
    ),
    (
        "concierge-pacote",
        "estrutura do pacote Concierge",
        [sys.executable, "ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/validar_pacote.py"],
    ),
    (
        "concierge-regressoes",
        "regressões do verificador Concierge",
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "ambiente_fonte/.assistant/skills/hub-ml-concierge/tests", "-p", "test_*.py", "-v"],
    ),
    (
        "concierge-integracao",
        "integração canônica, contratos declarados e espelho",
        [sys.executable, "tools/tests/test_concierge_integracao.py", "-v"],
    ),
]


def conferir_dependencias() -> list[str]:
    """Devolve os pacotes Python ausentes, pelo nome com que se instala."""
    ausentes = []
    for modulo, pacote in DEPENDENCIAS:
        if importlib.util.find_spec(modulo) is None:
            ausentes.append(pacote)
    return ausentes


def conferir_dependencias_node() -> list[str]:
    """Devolve pré-requisitos locais ausentes para os testes V06 do compositor."""
    ausentes = []
    if shutil.which("node") is None:
        ausentes.append("node>=20")
    base = RAIZ / "tools" / "readme_visuals" / "node_modules"
    for relativo in DEPENDENCIAS_NODE:
        if not (base / relativo).is_file():
            ausentes.append(f"node_modules/{relativo}")
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
    # As etapas são Python: pedir UTF-8 ao filho resolve a origem do
    # problema. A decodificação tolerante acima é a rede de segurança para
    # qualquer saída que ainda escape disso.
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
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

    ausentes_node = conferir_dependencias_node()
    if ausentes_node:
        print("\nFAIL dependências do compositor V06 ausentes: " + ", ".join(ausentes_node))
        print("     npm install --global pnpm@10.34.5")
        print("     pnpm --dir tools/readme_visuals install --frozen-lockfile")
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
            print("   --- saída integral da etapa que reprovou ---")
            print("   " + saida.strip().replace("\n", "\n   "))
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
