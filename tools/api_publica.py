"""Extrai a API pública de um módulo por AST, sem importá-lo.

Por que existe: com uma pasta por snippet, cada pasta precisa de um
``__init__.py`` que reexporta o que o módulo oferece. Decidir isso 51 vezes, à
mão, produz 51 critérios diferentes — e a auditoria do plano mostrou o custo:
``constants/colors`` tem 22 nomes públicos, e dois outros módulos importam nomes
específicos dele. Um ``__all__`` curado quebra o import de quem depende, e o
sintoma aparece sprints depois de a causa ser escrita.

**Regra: exaustiva, não curada.** Entra tudo que é definido no topo do módulo e
não começa com ``_``. Fica de fora o que foi apenas importado — reexportar import
alheio criaria um segundo caminho para o mesmo nome.

Uso:

    python tools/api_publica.py <caminho.py>          # um módulo
    python tools/api_publica.py --inventario <pasta>  # tabela de tudo
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_marker import eh_notebook  # noqa: E402


def api_publica(caminho: Path) -> list[str]:
    """Nomes públicos definidos no topo do módulo, na ordem em que aparecem.

    Recusa notebook. Numa pasta de objeto convivem o módulo e o notebook de
    exemplo, e apontar a ferramenta para o segundo produz um ``__init__.py`` que
    reexporta as variáveis de trabalho do notebook — e que **executa o notebook
    inteiro no import**. O erro é fácil de cometer e silencioso de diagnosticar.
    """
    if eh_notebook(caminho):
        raise SystemExit(
            f"FAIL {caminho.name} é um notebook, não um módulo.\n"
            "     Aponte para o arquivo de implementação da pasta —\n"
            "     o notebook de exemplo não tem API pública a declarar."
        )
    arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    nomes: list[str] = []

    def registrar(nome: str) -> None:
        if not nome.startswith("_") and nome not in nomes:
            nomes.append(nome)

    for no in arvore.body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            registrar(no.name)
        elif isinstance(no, ast.Assign):
            for alvo in no.targets:
                if isinstance(alvo, ast.Name):
                    registrar(alvo.id)
        elif isinstance(no, ast.AnnAssign) and isinstance(no.target, ast.Name):
            registrar(no.target.id)
    return nomes


def conteudo_init(modulo: str, nomes: list[str]) -> str:
    """Texto do ``__init__.py`` que reexporta a API pública da pasta."""
    if not nomes:
        raise ValueError(f"{modulo}: nenhum nome público — pasta de snippet precisa expor algo")
    importados = ", ".join(nomes)
    listados = ",\n    ".join(f'"{n}"' for n in nomes)
    return (
        f"from .{modulo} import {importados}\n"
        f"\n"
        f"__all__ = [\n    {listados},\n]\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("caminho", type=Path)
    parser.add_argument(
        "--inventario", action="store_true",
        help="trata o caminho como pasta e imprime a API de cada módulo",
    )
    args = parser.parse_args()

    if not args.inventario:
        nomes = api_publica(args.caminho)
        print(conteudo_init(args.caminho.stem, nomes))
        return 0

    modulos = [
        p for p in sorted(args.caminho.rglob("*.py"))
        if p.name != "__init__.py"
        and "__pycache__" not in p.parts
        and "tests" not in p.parts
        and not eh_notebook(p)  # notebook de exemplo não tem API pública
    ]
    total_nomes = 0
    multiplos = 0
    print(f"{'módulo':44} {'n':>3}  nomes públicos")
    for p in modulos:
        nomes = api_publica(p)
        total_nomes += len(nomes)
        multiplos += len(nomes) > 1
        rel = p.relative_to(args.caminho)
        amostra = ", ".join(nomes[:4]) + (" …" if len(nomes) > 4 else "")
        print(f"{str(rel):44} {len(nomes):>3}  {amostra}")
    print(
        f"\n{len(modulos)} módulos | {total_nomes} nomes públicos | "
        f"{multiplos} com mais de um nome"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
