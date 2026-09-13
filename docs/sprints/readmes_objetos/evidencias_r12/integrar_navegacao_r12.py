from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSIST = ROOT / "ambiente_fonte/.assistant"
CATEGORIES = ("constants", "display", "ml", "spark", "testing", "visual")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = read(path)
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f"substituicao nao unica em {path}: {old[:100]!r}")
    write(path, text.replace(old, new, 1))


def update_catalog() -> None:
    path = ASSIST / "hub_snippets/README.md"
    text = read(path)
    for cat in CATEGORIES:
        old = f"| `{cat}` |"
        new = f"| [`{cat}`]({cat}/README.md) |"
        if new not in text:
            if text.count(old) != 1:
                raise RuntimeError(f"categoria ausente/duplicada: {cat}")
            text = text.replace(old, new, 1)
    anchor = "| [`testing`](testing/README.md) | dados sintéticos e fixtures |\n"
    if "Cada categoria possui agora um índice local" not in text:
        note = anchor + "\nCada categoria possui agora um índice local que lista todos os objetos diretamente nela e aponta para o README de cada recurso. `hub_snippets/tests/` permanece fora desse mapa porque é infraestrutura interna de regressão, não uma categoria de uso.\n"
        if anchor not in text:
            raise RuntimeError("ancora de categorias ausente")
        text = text.replace(anchor, note, 1)
    write(path, text)


def update_entry() -> None:
    path = ASSIST / "README.md"
    anchor = "[Explore o catálogo narrativo de snippets](hub_snippets/README.md)."
    replacement = anchor + "\n\nEntre diretamente pela natureza do problema: " + " · ".join(
        f"[{c}](hub_snippets/{c}/README.md)" for c in CATEGORIES
    ) + "."
    replace_once(path, anchor, replacement)


def update_manual() -> None:
    src = ASSIST / "MANUAL_TECNICO.md"
    text = read(src)
    old = (
        "Na migração em andamento, pastas ainda não convertidas podem não ter README.\n"
        "Nesse caso, consulte o inventário e o exemplo existente; ausência do guia não\n"
        "é evidência de teste nem de defeito. Novos objetos devem incluir o guia. O molde\n"
        "está no caminho lógico `hub_padroes/readme/template_objeto.md`, relativo à raiz\n"
        "`.assistant/`. Esta referência lógica permanece válida nas três cópias deste\n"
        "Manual, sem pressupor acesso ao GitHub no workspace."
    )
    new = (
        "A migração estrutural dos READMEs de objeto foi concluída na R11: os 75 objetos\n"
        "operacionais possuem guia local, e os três exemplares permanecem contabilizados\n"
        "separadamente. Para `hub_snippets`, seis índices de categoria — `constants`,\n"
        "`display`, `ml`, `spark`, `testing` e `visual` — oferecem uma rota intermediária\n"
        "entre este Manual, o catálogo geral e cada objeto. Novos objetos continuam\n"
        "devendo incluir o guia. O molde está no caminho lógico\n"
        "`hub_padroes/readme/template_objeto.md`, relativo à raiz `.assistant/`."
    )
    if new not in text:
        if old not in text:
            raise RuntimeError("paragrafo de migracao do Manual nao encontrado")
        text = text.replace(old, new, 1)

    anchor = "**Como usar:** procure a finalidade, leia o tipo de entrada e de retorno, abra o exemplo específico e só então adapte a chamada. A assinatura é uma referência de consulta; os capítulos 4 a 7 explicam sua notação. Ela não substitui a docstring, os testes ou a revisão de efeitos. As dependências citadas nas fichas destacam pontos de atenção, não constituem um lockfile completo. Nenhuma ficha significa “homologado hoje no seu workspace”."
    addition = anchor + "\n\nPara navegar pelos snippets antes de chegar à ficha técnica, use os índices locais: " + " · ".join(
        f"[`{c}`](hub_snippets/{c}/README.md)" for c in CATEGORIES
    ) + ". Eles agrupam os mesmos objetos por natureza do problema e não substituem este inventário."
    if "Para navegar pelos snippets antes de chegar à ficha técnica" not in text:
        if anchor not in text:
            raise RuntimeError("ancora do inventario do Manual nao encontrada")
        text = text.replace(anchor, addition, 1)
    write(src, text)
    shutil.copyfile(src, ROOT / "MANUAL_TECNICO.md")


if __name__ == "__main__":
    update_catalog()
    update_entry()
    update_manual()
