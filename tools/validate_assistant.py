"""Bateria de validação local do ambiente_fonte/.

Recria os checks estruturais da auditoria do Codex (2026-08-13) como ferramenta
permanente do projeto. Uso:

    python tools/validate_assistant.py [--root ambiente_fonte]

Exit code 0 = aprovado (FAILs ausentes); 1 = pelo menos um FAIL.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_marker import eh_notebook  # noqa: E402

INSTRUCTION_LIMIT = 20_000
SKILL_LINE_WARN = 500

# Raiz do repositório, derivada do arquivo e não do diretório atual: os checks de
# repositório inteiro precisam varrer sempre o mesmo lugar, independentemente de
# onde o comando foi chamado.
REPO_ROOT = Path(__file__).resolve().parents[1]

# Diretórios fora do alcance dos checks de repositório inteiro.
REPO_IGNORE = {".git", "Ambiente_Antigo", "Ajustes_Codex", "__pycache__", ".venv"}

# Padrões que caracterizam identificador corporativo. Não são exaustivos — são os
# formatos conhecidos deste contexto. Ao levar o repositório para outra
# organização, acrescente aqui o formato de matrícula e o domínio de lá antes de
# confiar no check.
CORPORATE_RE = re.compile(
    r"\b[a-z]\d{6,8}\b"                      # matrícula: letra + 6 a 8 dígitos
    r"|corp(?:orativ)?[.@]"                  # domínio/e-mail corporativo
    r"|\.gov\.br"
    r"|@[a-z0-9-]*(?:banco|caixa|bank)[a-z0-9-]*\.",
    re.IGNORECASE,
)

# Sequências típicas de mojibake (UTF-8 lido como latin-1/cp1252).
MOJIBAKE_RE = re.compile(r"Ã[£¡©ªµ§¢³º]|â€[œ\x9d™“”]|Ã‚|Ã©|Ã§Ã")

# Identificadores que jamais podem aparecer em conteúdo versionado.
PERSONAL_RE = re.compile(
    r"c\d{6}|corp\.caixa|caixa\.gov\.br|guimarais[._-]?r?[._-]?rodrigo@|"
    r"C:\\Users\\Rodrigo|/Users/rodri\b",
    re.IGNORECASE,
)

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#?\s]+)(?:[#?][^)]*)?\)")


def iter_files(root: Path, suffix: str) -> list[Path]:
    return sorted(p for p in root.rglob(f"*{suffix}") if p.is_file())


def check_skill_frontmatter(root: Path, problems: list[str]) -> int:
    skills_dir = root / ".assistant" / "skills"
    count = 0
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        count += 1
        folder = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            problems.append(f"{skill_md}: sem frontmatter YAML")
            continue
        try:
            frontmatter = text.split("---", 2)[1]
        except IndexError:
            problems.append(f"{skill_md}: frontmatter malformado")
            continue
        name_match = re.search(r"^name:\s*(\S+)", frontmatter, re.MULTILINE)
        has_description = re.search(r"^description:", frontmatter, re.MULTILINE)
        if not name_match:
            problems.append(f"{skill_md}: frontmatter sem 'name'")
        elif name_match.group(1) != folder:
            problems.append(
                f"{skill_md}: name '{name_match.group(1)}' != pasta '{folder}'"
            )
        if not has_description:
            problems.append(f"{skill_md}: frontmatter sem 'description'")
    return count


def check_pycache(root: Path, warnings: list[str]) -> None:
    """Bytecode no fonte não quebra nada, mas viaja.

    O `.gitignore` impede o commit e o render o filtra na cópia, então ele nunca
    chega ao workspace pelo caminho normal. O que sobra é sujeira local que
    aparece em busca e em listagem de pasta — e que já chegou ao workspace uma
    vez, por publicação feita direto da pasta em vez de pelo simulado. Aviso, não
    falha: apagar é trivial e não bloqueia ninguém.
    """
    caches = [p for p in root.rglob("__pycache__") if p.is_dir()]
    if caches:
        warnings.append(
            f"{len(caches)} pasta(s) __pycache__ em {root.name}/ — "
            "remova com: find <raiz> -name __pycache__ -type d -exec rm -rf {} +"
        )


def check_skill_sizes(root: Path, warnings: list[str]) -> None:
    for skill_md in sorted((root / ".assistant" / "skills").glob("*/SKILL.md")):
        n_lines = len(skill_md.read_text(encoding="utf-8").splitlines())
        if n_lines > SKILL_LINE_WARN:
            warnings.append(
                f"{skill_md}: {n_lines} linhas (> {SKILL_LINE_WARN}; "
                "considere progressive disclosure)"
            )


def check_markdown(root: Path, problems: list[str]) -> tuple[int, int]:
    md_files = iter_files(root, ".md")
    links_checked = 0
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        if text.count("```") % 2 != 0:
            problems.append(f"{md}: cercas ``` desbalanceadas")
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            links_checked += 1
            if not (md.parent / target).resolve().exists():
                problems.append(f"{md}: link relativo quebrado -> {target}")
    return len(md_files), links_checked


def check_notebook_links(root: Path, problems: list[str]) -> tuple[int, int]:
    """Confere links markdown escritos dentro de células `%md` de notebook.

    Notebook é `.py`, e por isso escapava inteiro do check de markdown. Com uma
    pasta por objeto, cada snippet passa a ter um notebook cheio de links para o
    catálogo, o glossário e os módulos vizinhos — a classe de arquivo que mais
    vai crescer é justamente a que ninguém verificava.

    O caminho é resolvido a partir da pasta do notebook, como no Markdown.
    """
    notebooks = [p for p in iter_files(root, ".py") if eh_notebook(p)]
    links_checked = 0
    for nb in notebooks:
        for linha in nb.read_text(encoding="utf-8").splitlines():
            if not linha.lstrip().startswith("#"):
                continue  # link só conta dentro de comentário/`# MAGIC %md`
            for match in MD_LINK_RE.finditer(linha):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                links_checked += 1
                if not (nb.parent / target).resolve().exists():
                    problems.append(f"{nb}: link relativo quebrado -> {target}")
    return len(notebooks), links_checked


def check_smoke_test_sincronizado(problems: list[str]) -> None:
    """O smoke test roda no workspace, onde `tools/` não existe.

    Por isso ele carrega uma cópia da regra de detecção de notebook. Cópia sem
    guarda diverge: a canônica passa a tolerar um prefixo novo, a do smoke test
    não, e notebooks voltam a ser importados sem que nada acuse.
    """
    smoke = REPO_ROOT / "tools" / "spark_smoke_test.py"
    canonico = REPO_ROOT / "tools" / "notebook_marker.py"
    if not smoke.exists() or not canonico.exists():
        problems.append("tools: smoke test ou notebook_marker ausente")
        return
    texto_smoke = smoke.read_text(encoding="utf-8")
    for constante in ("MARCADOR_NOTEBOOK", "_PREFIXOS_TOLERADOS"):
        linha_canonica = next(
            (l for l in canonico.read_text(encoding="utf-8").splitlines()
             if l.startswith(f"{constante} =")),
            None,
        )
        if linha_canonica is None:
            problems.append(f"notebook_marker.py: constante {constante} não encontrada")
        elif linha_canonica not in texto_smoke:
            problems.append(
                f"spark_smoke_test.py: {constante} divergiu de notebook_marker.py "
                f"(esperado: {linha_canonica.strip()})"
            )


def check_python_ast(root: Path, problems: list[str]) -> int:
    py_files = iter_files(root, ".py")
    for py in py_files:
        try:
            ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        except SyntaxError as exc:
            problems.append(f"{py}: erro de sintaxe -> {exc}")
    return len(py_files)


def check_instructions_size(root: Path, problems: list[str]) -> int:
    instructions = root / ".assistant_instructions.md"
    if not instructions.exists():
        problems.append(f"{instructions}: arquivo ausente")
        return 0
    size = len(instructions.read_text(encoding="utf-8"))
    if size > INSTRUCTION_LIMIT:
        problems.append(
            f"{instructions}: {size} caracteres (> {INSTRUCTION_LIMIT})"
        )
    return size


def iter_repo_files() -> list[Path]:
    """Arquivos do repositório inteiro, exceto referências congeladas e caches."""
    return [
        p
        for p in REPO_ROOT.rglob("*")
        if not any(parte in REPO_IGNORE for parte in p.relative_to(REPO_ROOT).parts)
    ]


def check_repo_corporate(problems: list[str]) -> int:
    """Varre o repositório inteiro atrás de identificador **corporativo**.

    O check de caminho abaixo cobre apenas a raiz analisada, e o vetor descrito
    no ADR-0003 se materializa fora dela: em `Novo_Ambiente_Simulado/`, que é
    versionado e carrega o nome do usuário no caminho. Aqui a busca é só por
    padrão corporativo — o username pessoal do laboratório é estado aceito.

    A varredura parte de `REPO_ROOT`, não do diretório atual: antes disso, rodar
    o comando de outra pasta reduzia a varredura sem alterar o veredito.
    """
    verificados = 0
    for caminho in iter_repo_files():
        relativo = caminho.relative_to(REPO_ROOT)
        if CORPORATE_RE.search(str(relativo)):
            problems.append(f"{relativo}: identificador corporativo no caminho")
        if not caminho.is_file() or caminho.suffix not in {".md", ".py", ".txt", ".json"}:
            continue
        verificados += 1
        try:
            if CORPORATE_RE.search(caminho.read_text(encoding="utf-8")):
                problems.append(f"{relativo}: identificador corporativo no conteúdo")
        except (UnicodeDecodeError, OSError):
            continue
    if verificados == 0:
        problems.append(
            "check corporativo não varreu nenhum arquivo — a proteção do ADR-0003 "
            "não rodou; não trate este resultado como aprovação"
        )
    return verificados


def check_repo_links(root: Path, problems: list[str]) -> int:
    """Confere links relativos dos Markdown **fora** da raiz analisada.

    `check_markdown` cobre só `--root`. Sem isto, o README da raiz, `docs/` e
    `.claude/` — que é onde vive a maior parte da documentação de navegação —
    ficavam sem verificação de link algum.
    """
    verificados = 0
    for caminho in iter_repo_files():
        if caminho.suffix != ".md" or not caminho.is_file():
            continue
        if root in caminho.parents:
            continue  # já coberto por check_markdown
        relativo = caminho.relative_to(REPO_ROOT)
        try:
            texto = caminho.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in MD_LINK_RE.finditer(texto):
            alvo = match.group(1)
            if alvo.startswith(("http://", "https://", "mailto:")):
                continue
            verificados += 1
            if not (caminho.parent / alvo).resolve().exists():
                problems.append(f"{relativo}: link relativo quebrado -> {alvo}")
    return verificados


def check_path_hygiene(root: Path, problems: list[str]) -> None:
    """Identificador corporativo em nome de arquivo/pasta escapa ao check de conteúdo.

    Vetor real: renderizar o simulado com o username do trabalho cria
    `Users/<identificador>/` e um `git add` publicaria o identificador no nome do
    diretório, contra o ADR-0003.
    """
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if PERSONAL_RE.search(str(relative)):
            problems.append(f"{relative}: identificador pessoal/corporativo no caminho")


def check_text_hygiene(root: Path, problems: list[str]) -> None:
    for path in iter_files(root, ".md") + iter_files(root, ".py"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{path}: não decodifica como UTF-8")
            continue
        if MOJIBAKE_RE.search(text):
            problems.append(f"{path}: possível mojibake")
        if PERSONAL_RE.search(text):
            problems.append(f"{path}: identificador pessoal/corporativo")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="ambiente_fonte", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.exists():
        print(f"FAIL raiz não encontrada: {root}")
        return 1

    problems: list[str] = []
    warnings: list[str] = []

    n_skills = check_skill_frontmatter(root, problems)
    check_skill_sizes(root, warnings)
    check_pycache(root, warnings)
    n_md, n_links = check_markdown(root, problems)
    n_nb, n_nb_links = check_notebook_links(root, problems)
    n_py = check_python_ast(root, problems)
    n_chars = check_instructions_size(root, problems)
    check_text_hygiene(root, problems)
    check_path_hygiene(root, problems)
    check_smoke_test_sincronizado(problems)
    n_repo = check_repo_corporate(problems)
    n_repo_links = check_repo_links(root, problems)

    print(f"raiz analisada     : {root}")
    print(f"skills             : {n_skills}")
    print(f"markdown / links   : {n_md} arquivos / {n_links} links relativos")
    print(f"notebooks / links  : {n_nb} notebooks / {n_nb_links} links relativos")
    print(f"python (AST)       : {n_py} arquivos")
    print(f"instrucoes         : {n_chars}/{INSTRUCTION_LIMIT} caracteres")
    print(f"repo (corporativo) : {n_repo} arquivos varridos no repositório inteiro")
    print(f"repo (links)       : {n_repo_links} links fora da raiz analisada")
    print()
    for warning in warnings:
        print(f"WARN {warning}")
    for problem in problems:
        print(f"FAIL {problem}")
    status = "APROVADO" if not problems else "REPROVADO"
    print(f"\n{status}: {len(problems)} falha(s), {len(warnings)} aviso(s)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
