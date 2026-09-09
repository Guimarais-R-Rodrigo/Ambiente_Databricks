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

from repo_inventory import git_paths
from notebook_marker import eh_notebook, texto_e_notebook  # noqa: E402
from project_policy import CORPORATE_RE, EXPECTED_SKILL_NAMES, PERSONAL_RE  # noqa: E402

INSTRUCTION_LIMIT = 20_000
SKILL_LINE_WARN = 500

# Raiz do repositório, derivada do arquivo e não do diretório atual: os checks de
# repositório inteiro precisam varrer sempre o mesmo lugar, independentemente de
# onde o comando foi chamado.
REPO_ROOT = Path(__file__).resolve().parents[1]

# Diretórios fora do alcance dos checks de repositório inteiro.
REPO_IGNORE = {
    ".git",
    ".artifacts",
    "Ambiente_Antigo",
    "Ajustes_Codex",
    "__pycache__",
    ".venv",
}

# Não cobre o nome da instituição usado como constante de domínio na paleta
# visual (`AZUL_CAIXA` e afins), exceção registrada no PLANO_HUB.md §2.2. O
# ADR-0009, por outro lado, exige identidade pessoal neutra no conteúdo ativo e
# derivado; e-mail/username real não é mais exceção implícita.
#
# Sequências típicas de mojibake (UTF-8 lido como latin-1/cp1252).
MOJIBAKE_RE = re.compile(r"Ã[£¡©ªµ§¢³º]|â€[œ\x9d™“”]|Ã‚|Ã©|Ã§Ã")

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#?\s]+)(?:[#?][^)]*)?\)")


def iter_files(root: Path, suffix: str) -> list[Path]:
    return sorted(p for p in root.rglob(f"*{suffix}") if p.is_file())


def alvo_existe(origem: Path, alvo: str) -> bool:
    """Resolve link relativo **respeitando a caixa** do nome.

    `Path.exists()` no NTFS ignora maiúsculas: um link para `catalogo.md` passa
    quando o arquivo é `CATALOGO.md`. O workspace Databricks não ignora, e o
    link morre exatamente no ambiente onde alguém clica nele. Foi assim que um
    link do glossário para o catálogo passou por três validações e só apareceu
    quando um auditor consultou o workspace.
    """
    if not (origem / alvo).resolve().exists():
        return False
    # Desce componente a componente a partir da origem, conferindo cada nome
    # contra a listagem real. `resolve()` normaliza a caixa para a do disco, e
    # por isso não serve aqui: é justamente a diferença que se quer detectar.
    atual = origem
    for parte in alvo.replace("\\", "/").split("/"):
        if parte in ("", "."):
            continue
        if parte == "..":
            atual = atual.parent
            continue
        try:
            if parte not in {p.name for p in atual.iterdir()}:
                return False
        except OSError:
            return True  # sem permissão de listar: não invente reprovação
        atual = atual / parte
    return True


def _parse_frontmatter_subset(text: str, skill_md: Path) -> tuple[dict[str, str], str | None]:
    """Parseia o subconjunto conservador adotado pelo pacote: escalares simples.

    O projeto usa somente ``name`` e ``description``. Rejeitar sintaxe fora desse
    subconjunto é deliberado e evita que regex aceite YAML inválido ou valor vazio.
    """
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.DOTALL)
    if not match:
        return {}, "frontmatter ausente ou sem delimitador final"
    values: dict[str, str] = {}
    for number, raw in enumerate(match.group(1).splitlines(), 2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw != raw.lstrip() or ":" not in raw:
            return {}, f"YAML fora do subconjunto escalar na linha {number}"
        key, scalar = raw.split(":", 1)
        key, scalar = key.strip(), scalar.strip()
        if key in values:
            return {}, f"chave YAML duplicada: {key}"
        if key not in {"name", "description"}:
            return {}, f"campo {key!r} fora da política conservadora deste pacote"
        if not scalar:
            return {}, f"campo {key!r} vazio"
        if scalar[0] in "[{&*!|>":
            return {}, f"campo {key!r} usa sintaxe YAML fora do subconjunto escalar"
        if scalar[0] in {'"', "'"}:
            try:
                parsed = ast.literal_eval(scalar)
            except (SyntaxError, ValueError):
                return {}, f"string YAML inválida no campo {key!r}"
            if not isinstance(parsed, str):
                return {}, f"campo {key!r} precisa ser string"
            scalar = parsed.strip()
        if not scalar:
            return {}, f"campo {key!r} vazio"
        values[key] = scalar
    return values, None


def check_skill_frontmatter(root: Path, problems: list[str]) -> int:
    skills_dir = root / ".assistant" / "skills"
    folders = {path.name: path for path in skills_dir.iterdir() if path.is_dir()}
    for name in sorted(EXPECTED_SKILL_NAMES - set(folders)):
        problems.append(f"{skills_dir}: skill esperada ausente: {name}")
    for name in sorted(set(folders) - EXPECTED_SKILL_NAMES):
        problems.append(f"{skills_dir}: pasta inesperada em skills: {name}")

    for folder, directory in sorted(folders.items()):
        skill_md = directory / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"{directory}: pasta de skill sem SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        frontmatter, error = _parse_frontmatter_subset(text, skill_md)
        if error:
            problems.append(f"{skill_md}: {error}")
            continue
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if not name:
            problems.append(f"{skill_md}: frontmatter sem 'name'")
        elif name != folder:
            problems.append(
                f"{skill_md}: name '{name}' != pasta '{folder}'"
            )
        elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            problems.append(f"{skill_md}: name fora do formato Agent Skills")
        if not description:
            problems.append(f"{skill_md}: frontmatter sem 'description' não vazia")
    return len(folders)


def check_saida_colada(root: Path, problems: list[str]) -> tuple[int, int]:
    """Cobra do notebook um bloco com a saída real da execução.

    O template pede que a leitura cite o número obtido, não o pretendido — e uma
    auditoria mostrou que só 6 de 24 notebooks faziam isso. Prosa sem número é
    prosa que ninguém confere sem reexecutar, e foi sob essa cobertura que
    sobreviveu um notebook ensinando a contar nulos numa saída que tem zero
    nulos por construção.

    O sinal exigido é um bloco ```text com dígito dentro **ou** com pelo menos
    trinta caracteres. A segunda porta existe para saída que é mensagem de erro
    — `safe_display` cola um `RuntimeError` sem um dígito sequer —, e é por ela
    que passa prosa inventada de trinta caracteres. É o preço de não ter falso
    positivo; saiba que ela está aberta.

    O que ele **não** cobre, e é bom saber: a guarda é por notebook, não por
    bloco de leitura. Um notebook com quatro células que imprimem e um único
    bloco colado passa. E ele não distingue transcrição literal de transcrição
    curada — uma auditoria encontrou seis blocos editados, um deles omitindo
    justamente a linha que contradizia a prosa em volta.

    **Falha, não aviso**, desde 2026-08-18. A dívida das Sprints 1, 4 e 6 — os
    11 notebooks listados em `PLANO_HUB.md` §12.1 — foi fechada executando os
    onze como job no Free e colando a transcrição na célula que lê o resultado.
    A escada estava escrita aqui desde o começo: *promover a falha quando
    `sem_bloco` chegar a zero*. Chegou.
    """
    com = sem = 0
    for nb in sorted(root.rglob("exemplo_*.py")):
        markdown = "\n".join(
            linha for linha in nb.read_text(encoding="utf-8").splitlines()
            if linha.startswith("# MAGIC")
        )
        # Bloco vazio ou de meia dúzia de palavras é decorativo: não sustenta
        # leitura nenhuma. Um número resolve, e uma mensagem de erro capturada
        # também — `safe_display` cola um `RuntimeError` sem um dígito sequer, e
        # é evidência tão conferível quanto uma tabela.
        blocos = [
            re.sub(r"^# MAGIC ?", "", b, flags=re.MULTILINE).strip()
            for b in re.findall(r"```text(.*?)```", markdown, re.DOTALL)
        ]
        if any(re.search(r"\d", b) or len(b) >= 30 for b in blocos):
            com += 1
        else:
            sem += 1
            motivo = ("bloco ```text sem nenhum número" if blocos
                      else "nenhum bloco ```text com saída real")
            problems.append(
                f"{nb.relative_to(root)}: {motivo}; "
                "a leitura não pode ser conferida sem reexecutar"
            )
    return com, sem



def check_skill_helpers_resolvem(root: Path, problems: list[str]) -> int:
    """Todo helper citado numa skill precisa existir.

    As skills recomendam helper por caminho de import pontilhado —
    `hub_snippets.spark.pit_join` — porque essa forma é imune à conversão para
    pasta de objeto. Ela sobreviveu a cinco sprints de conversão sem uma edição.

    O que ela **não** sobrevive é a um objeto renomeado ou removido: o caminho
    continua escrito, e a skill passa a recomendar algo que não existe. Ninguém
    percebe, porque o Genie Code não resolve o caminho — quem resolve é a pessoa,
    no notebook, e o erro aparece longe daqui.

    Uma auditoria verificou à mão os caminhos existentes à época e achou zero quebrados. Esta
    guarda é para que a próxima não precise.
    """
    base = root / ".assistant"
    verificados = 0
    for skill_md in sorted((base / "skills").glob("*/SKILL.md")):
        texto = skill_md.read_text(encoding="utf-8")
        rel = skill_md.relative_to(root)
        for pacote, caminho in re.findall(
            r"\b(hub_snippets|hub_scripts)((?:\.[a-z_][a-z0-9_]*)+)", texto
        ):
            partes = [p for p in caminho.split(".") if p]
            verificados += 1
            destino = base / pacote / Path(*partes)

            # Pasta de objeto é a que tem `__init__.py`. Exigir isso, e não só
            # `is_dir()`, é o que separa esta guarda de uma que não serve: uma
            # auditoria mostrou que aceitar "o pai existe" deixava 59 dos 72
            # caminhos desprotegidos, porque o pai de <secao>/<objeto> é a
            # seção, e seção sempre existe.
            if (destino / "__init__.py").exists():
                continue

            # O caminho pode terminar na função em vez do módulo. Aí o pai
            # precisa ser pasta de objeto **e** o último componente precisa ser
            # um nome que o `__init__.py` de lá realmente exporta.
            if len(partes) > 1:
                pai = base / pacote / Path(*partes[:-1])
                init = pai / "__init__.py"
                if init.exists():
                    exportados = set(re.findall(
                        r'^\s*"([A-Za-z_][A-Za-z0-9_]*)",\s*$',
                        init.read_text(encoding="utf-8"), re.MULTILINE,
                    ))
                    if partes[-1] in exportados or partes[-1] == partes[-2]:
                        continue
                    problems.append(
                        f"{rel}: recomenda `{pacote}{caminho}`, mas "
                        f"`{partes[-1]}` não está na API pública de "
                        f"`{'.'.join(partes[:-1])}`"
                    )
                    continue

            problems.append(
                f"{rel}: recomenda `{pacote}{caminho}`, que não existe na "
                "biblioteca — a skill aponta para um objeto renomeado ou removido"
            )
    return verificados


# A seção que o template chama de "não opcional e não decorativa" (ADR-0004).
_CHAVES_DE_HELPER = ("helper", "recurso")

# As cinco que o template lista. Só a de helpers é cobrada; as outras entram na
# contagem informativa, porque as 12 skills originais são anteriores ao template
# e reescrevê-las é decisão de produto, não conserto.
_SECOES_DE_SKILL = {
    # "se aplica", e nao "aplica": `hub-ml-pipeline-builder` tem uma seção
    # chamada "Aplicar qualidade", e a chave curta a contava como se fosse a
    # seção de escopo. Falso positivo da guarda, achado ao instrumentá-la.
    "quando esta skill se aplica": ("se aplica", "quando usar"),
    "fluxo": ("fluxo", "executar", "selecionar", "basear", "escolher"),
    "helpers": _CHAVES_DE_HELPER,
    # `guardrail` entra porque é a **mesma seção com outro nome**: sete skills
    # anteriores ao template listam proibições sob esse título, com o mesmo
    # formato de lista imperativa. Cobrar o título em vez do conteúdo era falso
    # negativo da própria guarda -- exatamente a classe que ela existe para pegar.
    "o que nunca fazer": ("nunca fazer", "não fazer", "evitar", "guardrail", "cuidado"),
    "formato de saída": ("formato de saída", "verificar o resultado", "entregar"),
}


def check_skill_secoes(root: Path, problems: list[str]) -> tuple[int, int]:
    """Confere o corpo da skill contra as seções que o template exige.

    Uma auditoria encontrou a skill mais nova sem três das cinco — inclusive a de
    helpers, que o template chama de "não opcional e não decorativa". Os dois
    portões aprovaram: eles conferem frontmatter e tamanho, não conteúdo.

    **A seção de helpers reprova**, e desde 18/08/2026 as treze a têm. A
    consequência dela é concreta: o Genie Code não descobre `hub_snippets`
    sozinho, e uma skill que não a declara transfere para a pessoa a tarefa de
    adivinhar que o helper existe.

    As outras quatro entram na contagem informativa — hoje **13/13** —, e não
    reprovam por um motivo de método: o casamento é por título, e título é
    vocabulário. Instrumentar esta guarda expôs os dois erros que o casamento
    lexical produz, e os dois viraram correção:

    - **falso positivo:** a chave `"aplica"` contava a seção "Aplicar qualidade"
      de `hub-ml-pipeline-builder` como se fosse a de escopo. Virou `"se aplica"`.
    - **falso negativo:** sete skills listam proibições sob o título `Guardrails`,
      e três descrevem o fluxo como uma sequência de seções no infinitivo. A
      primeira virou palavra-chave; a segunda virou detecção **estrutural**,
      porque renomear seções boas para agradar a guarda é ajustar o mundo ao
      instrumento.
    """
    verificados = completas = 0
    for skill_md in sorted((root / ".assistant" / "skills").glob("*/SKILL.md")):
        verificados += 1
        titulos = [
            l[3:].strip().lower()
            for l in skill_md.read_text(encoding="utf-8").splitlines()
            if l.startswith("## ")
        ]
        faltando = [
            nome for nome, chaves in _SECOES_DE_SKILL.items()
            if not any(c in t for t in titulos for c in chaves)
        ]
        # "Fluxo" pode não se chamar fluxo. Três skills o escrevem como uma
        # sequência de seções no infinitivo -- "definir o contexto",
        # "inventariar e especificar", "prevenir leakage" --, que é a mesma coisa
        # com nomes melhores. Cobrar a palavra seria fazer a guarda medir
        # vocabulário em vez de estrutura, e renomear seções boas para agradar a
        # guarda é ajustar o mundo ao instrumento.
        passos = sum(1 for t in titulos if t.split(" ")[0].endswith(("ar", "er", "ir")))
        if "fluxo" in faltando and passos >= 3:
            faltando.remove("fluxo")
        if not faltando:
            completas += 1
        if not any(c in t for t in titulos for c in _CHAVES_DE_HELPER):
            problems.append(
                f"{skill_md.relative_to(root)}: sem seção de helpers — o Genie "
                "Code não descobre `hub_snippets` sozinho (ADR-0004/0007)"
            )
    return verificados, completas


def check_saida_de_comando_no_readme(problems: list[str], *, remoto: bool = False) -> int:
    """Reexecuta os comandos que o README documenta e compara com o colado.

    O `README.md` da raiz ensina o ciclo colando a saída real de cada comando.
    É a escolha certa e a que envelhece sozinha: uma auditoria encontrou os três
    blocos errados por exatamente 1 em quatro contagens, porque foram capturados
    **antes** de o commit apagar um arquivo.

    A ironia registrada: o validador imprimia a resposta certa na tela enquanto o
    README exibia a errada. Esta guarda fecha esse caso.

    Compara só as linhas de contagem — as que começam com um rótulo conhecido.
    Não tenta casar o bloco inteiro, porque caminho e usuário aparecem com
    placeholder de propósito.
    """
    import subprocess

    readme = REPO_ROOT / "README.md"
    if not readme.exists():
        return 0

    rotulos = (
        "skills             :", "prompts            :", "helpers citados    :", "markdown / links   :",
        "notebooks / links  :", "pastas de objeto   :", "forma da pasta     :",
        "contrato de dados  :", "contrato de entrada:", "saída colada       :",
        "idioma da docstring:", "normas do molde    :", "notebook exercita  :",
        "python (AST)       :", "instrucoes         :", "repo (identidade)  :",
        "repo (links)       :", "APROVADO: 0 falha(s)",
    )
    comandos = [
        [sys.executable, str(REPO_ROOT / "tools" / "validate_assistant.py")],
    ]
    if remoto:
        rotulos = (
            "esperados : ", "remotos   : ", "ausentes  : ", "skills    :",
            "extensões :", "APROVADO: 0 problema(s)",
        )
        comandos = [[sys.executable, str(REPO_ROOT / "tools" / "publicar_free.py"), "--verify"]]
    # O filho herda a codificação do console, que no Windows é cp1252 e devolve
    # caractere de substituição em acento — e aí a comparação falha por
    # codificação, não por divergência real. PYTHONIOENCODING resolve na origem.
    import os

    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
    real = ""
    for cmd in comandos:
        try:
            process = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300,
                cwd=str(REPO_ROOT), encoding="utf-8", errors="replace",
                env=ambiente,
            )
            real += process.stdout
            if process.returncode != 0:
                problems.append(
                    f"README: `{Path(cmd[1]).name}` retornou {process.returncode}; "
                    "não há saída aprovada para certificar"
                )
        except (OSError, subprocess.SubprocessError) as erro:
            # Antes daqui havia `return 0`: o comando não lançava e a guarda
            # aprovava em silêncio, com "0 linhas conferidas" no meio de um bloco
            # de contagens. Uma auditoria mediu o custo numa máquina sem CLI —
            # três contagens erradas por 685, 684 e 86 passaram em dois segundos.
            # Timeout entra por aqui também (`--verify` gasta ~100 s de rede).
            problems.append(
                f"README: o comando `{Path(cmd[1]).name}` não executou "
                f"({type(erro).__name__}) — as contagens coladas ficaram sem "
                "conferência. Não trate este resultado como aprovação: rode de "
                "novo com a CLI do Databricks autenticada."
            )
            return 0

    texto_readme = readme.read_text(encoding="utf-8")
    verificados = 0
    for rotulo in rotulos:
        linha_real = next(
            (l.strip() for l in real.splitlines() if l.strip().startswith(rotulo.strip())), None)
        linha_readme = next(
            (l.strip() for l in texto_readme.splitlines() if l.strip().startswith(rotulo.strip())), None)
        if linha_readme is None and linha_real is not None:
            problems.append(
                f"README.md: bloco de saída não documenta `{rotulo.strip()}`; "
                "toda contagem do gate precisa ter um único dono conferível"
            )
            continue
        if linha_real is None:
            # Degradação silenciosa é o modo de falha que este repositório já
            # corrigiu duas vezes em outros checks: varredura vazia que passa.
            problems.append(
                f"README.md: documenta a linha `{rotulo.strip()}` mas o comando "
                "não a produziu — ou o rótulo mudou, ou o comando não rodou "
                "(CLI do Databricks autenticada?)"
            )
            continue
        verificados += 1
        norm = lambda s: re.sub(r"\s+", " ", s)
        if norm(linha_real) != norm(linha_readme):
            problems.append(
                f"README.md: a saída colada diverge da execução\n"
                f"    colado : {linha_readme}\n"
                f"    real   : {linha_real}"
            )
    return verificados


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


def check_prompt_contract(root: Path, problems: list[str]) -> tuple[int, int]:
    """Confere se cada prompt ensina a pessoa, além de instruir o modelo.

    A guarda nasceu quando 161 placeholders tinham rótulos, mas não explicavam
    preenchimento, impacto ou exemplo, e as seções humanas de QA/limites haviam
    sido substituídas por follow-ups. Repetir o placeholder em prosa não basta:
    cada campo precisa da linha de quatro colunas antes do bloco colável.
    """
    prompts_root = root / ".assistant" / "hub_prompts"
    files = sorted(
        path for path in prompts_root.glob("*/*.md")
        if path.name == f"{path.parent.name}.md"
    )
    placeholders_total = 0
    required = (
        "## Como preencher cada campo",
        "## Prompt pronto para colar",
        "## O que conferir na resposta",
        "## Limites",
    )
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)
        for heading in required:
            if heading not in text:
                problems.append(f"{rel}: seção obrigatória ausente: {heading}")
        before_prompt, marker, _prompt = text.partition("## Prompt pronto para colar")
        if not marker:
            continue
        placeholders = set(re.findall(r"\{\{[A-Z0-9_]+\}\}", text))
        documented = set(re.findall(r"\{\{[A-Z0-9_]+\}\}", before_prompt))
        placeholders_total += len(placeholders)
        for field in sorted(placeholders - documented):
            problems.append(f"{rel}: {field} não tem guia antes do bloco colável")
        for field in sorted(placeholders):
            row = next(
                (
                    line for line in before_prompt.splitlines()
                    if field in line and line.startswith("|")
                ),
                "",
            )
            if not row.startswith("|") or row.count("|") < 5:
                problems.append(
                    f"{rel}: {field} não tem linha campo/como/por quê/exemplo"
                )
        notebook = path.with_name(f"exemplo_{path.parent.name}.py")
        if notebook.exists() and re.search(
            r"\| Escrita \| \*\*sim\*\*.*`nenhuma",
            notebook.read_text(encoding="utf-8"),
        ):
            problems.append(
                f"{notebook.relative_to(root)}: declara escrita em tabela inexistente"
            )
    return len(files), placeholders_total


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
            if not alvo_existe(md.parent, target):
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
                if not alvo_existe(nb.parent, target):
                    problems.append(f"{nb}: link relativo quebrado -> {target}")
    return len(notebooks), links_checked


def check_pastas_de_objeto(root: Path, problems: list[str]) -> int:
    """Confere a forma das pastas de objeto: nome, arquivos e `__init__.py`.

    O checklist dos templates manda rodar este validador logo abaixo de "a pasta
    tem exatamente os três arquivos" e "`__init__.py` saiu da ferramenta". A
    adjacência sugeria que ele conferia essas coisas. Não conferia — e com 74
    objetos a converter, era por aqui que a deriva ficaria invisível até a
    auditoria.

    Uma pasta é de objeto quando contém `<nome_da_pasta>.py` — a forma que a
    conversão produz. Pasta de seção (`spark/`, `ml/`) não tem `spark.py` dentro,
    e por isso não entra na contagem.

    **Mas "não entra na contagem" não pode significar "passa".** Uma auditoria
    mostrou que uma pasta com `__init__.py` e um módulo de nome divergente —
    `taxa_nulos/calcula.py` — era simplesmente pulada: o validador aprovava um
    objeto que nunca seria importável pelo caminho que a documentação promete.
    `check_pasta_de_objeto_malformada` fecha isso.
    """
    from api_publica import api_publica, conteudo_init

    verificadas = 0
    for init in sorted(root.rglob("__init__.py")):
        pasta = init.parent
        modulo = pasta / f"{pasta.name}.py"
        if not modulo.exists():
            continue  # raiz de pacote ou pasta de seção
        verificadas += 1
        rel = pasta.relative_to(root)

        if not pasta.name.isidentifier():
            problems.append(f"{rel}: nome de pasta não é identificador Python válido")
        extras = [
            p for p in pasta.glob("*.py")
            if p.name not in {"__init__.py", modulo.name} and not eh_notebook(p)
        ]
        if extras:
            nomes = ", ".join(p.name for p in extras)
            problems.append(f"{rel}: módulo extra na pasta do objeto ({nomes})")
        notebooks = [p for p in pasta.glob("*.py") if eh_notebook(p)]
        esperado = f"exemplo_{pasta.name}.py"
        if not any(p.name == esperado for p in notebooks):
            problems.append(f"{rel}: falta o notebook '{esperado}'")
        try:
            # Normaliza fim de linha: redirecionar a saída da ferramenta no
            # Windows grava CRLF, e a divergência seria só de bytes invisíveis.
            atual = init.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            esperado_init = conteudo_init(modulo.stem, api_publica(modulo)).strip()
            if atual != esperado_init:
                problems.append(
                    f"{rel}/__init__.py: divergiu da API pública do módulo. "
                    f"Regenere: python tools/api_publica.py {modulo} > {init}"
                )
        except (SystemExit, ValueError) as exc:
            problems.append(f"{rel}: não foi possível derivar a API pública -> {exc}")
    return verificadas


# Seções conhecidas: uma pasta diretamente sob elas é objeto, não sub-seção.
_SECOES_DE_BIBLIOTECA = {"constants", "display", "ml", "spark", "testing", "visual"}


def check_docstring_em_portugues(root: Path, problems: list[str]) -> tuple[int, int]:
    """Cobra do módulo a norma de idioma que o próprio Hub publica.

    `hub_padroes/snippet/template.md` não descreve: manda. *"Docstring,
    comentário e notebook são prosa e vão em português"*, e *"não traduza
    identificador"*. É especificação executável escrita em Markdown — e até esta
    guarda existir, nada media se o produto a cumpria.

    Uma auditoria mediu: 15 dos 58 módulos (26%) tinham docstring de módulo em
    inglês, e a divisão era limpa por pasta — **7 de 7** em `hub_scripts/`. A
    biblioteca ensinava duas convenções ao mesmo tempo, e o molde publicado
    perdia autoridade sobre a etapa que o criou.

    A detecção não pode ser só "tem acento": cinco docstrings legítimas em
    português não têm nenhum (*"Wrapper Prophet com MLflow e feriados BR."*).
    O sinal é a **razão** entre palavras funcionais das duas línguas, que separa
    as duas populações sem falso positivo — e cai fora quando há acento, porque
    aí a língua está decidida.

    Escopo: a docstring **de módulo**, que é o que o leitor vê ao abrir o arquivo
    e o que o Genie Code cita ao explicá-lo. Docstring de função fica de fora por
    ora — a dívida é maior e vale medir antes de cobrar.

    **Falha, não aviso** — e isso é deliberado. As 15 foram traduzidas na mesma
    sessão em que a guarda nasceu, então não há dívida a tolerar: a partir daqui,
    docstring de módulo em inglês reprova a validação. Aviso serve para dívida
    aberta com prazo; norma cumprida se cobra.
    """
    en = re.compile(r"\b(the|of|with|for|and|to|from|based|against|as|on|in|"
                    r"an|that|when|not|into|by)\b", re.IGNORECASE)
    pt = re.compile(r"\b(de|com|para|do|da|dos|das|em|no|na|nos|nas|que|ou|"
                    r"ao|aos|um|uma|sem|por|pelo|pela|como|entre|sobre)\b", re.IGNORECASE)
    acento = re.compile(r"[áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ]")
    conferidos = ingleses = 0
    for modulo in sorted(root.rglob("*.py")):
        if modulo.parent.name != modulo.stem or modulo.name.startswith("exemplo_"):
            continue
        try:
            doc = ast.get_docstring(ast.parse(modulo.read_text(encoding="utf-8")))
        except SyntaxError:
            continue
        if not doc:
            continue
        conferidos += 1
        primeira = doc.split("\n")[0]
        if acento.search(primeira):
            continue
        if len(en.findall(primeira)) > len(pt.findall(primeira)):
            ingleses += 1
            problems.append(
                f"{modulo.relative_to(root)}: docstring de módulo em inglês — "
                f"{primeira[:60]!r}. O molde de `hub_padroes/snippet/` manda "
                "prosa em português; identificadores ficam como estão."
            )
    return conferidos, ingleses


def check_normas_do_molde(root: Path, problems: list[str]) -> tuple[int, int]:
    """Cobra do módulo as normas que `hub_padroes/snippet/template.md` **manda**.

    A auditoria de 18/08/2026 nomeou a classe: *norma publicada sem instrumento*.
    O molde não descreve, ele ordena — e viaja com o produto, com autoridade
    declarada. Até `check_docstring_em_portugues` existir, nenhuma das ordens dele
    era medida, e uma delas estava violada em 26% da biblioteca.

    Esta guarda instrumenta as quatro ordens que são **mecanicamente decidíveis**.
    O resto do molde continua sendo julgamento humano, e isso está certo: *"docstring
    do módulo diz por que existe, não o que faz"* não é verificável por AST.

    | Norma, como o molde a escreve | Como é medida |
    |---|---|
    | *"`cache()` ou `persist()`: bloqueados em serverless"* | chamada fora de `try` |
    | *"`toPandas()` sem limite verificável"* | sem `limit`/`sample`/`head`/`take` nas 5 linhas anteriores |
    | *"O global `spark` **não existe** dentro de módulo importado"* | nome `spark` lido sem ligação local |
    | *"O `__init__.py` de **seção** não reexporta nada"* | `from .` num `__init__` que não é de objeto |

    **Falha, não aviso**, e as quatro nasceram assim porque as quatro já estavam
    em zero quando a guarda foi escrita. Duas delas exigiram calibragem, e as duas
    calibragens são a parte que interessa:

    - `cache()` **dentro de `try`** é o padrão sancionado, não a violação:
      `drift_detector` e `quick_profile` têm um `_cache_if_supported` que degrada
      no serverless e mantém o cache onde ele existe. A regra é a chamada
      **desprotegida**.
    - `toPandas()` depois de `smart_sample(...)` tem limite verificável, mesmo sem
      a palavra `limit`. Daí a lista de limitadores em vez de um só nome.

    Sem essas duas, a guarda nasceria com três falsos positivos — e guarda que
    acusa código correto é desativada na segunda semana.
    """
    LIMITADORES = ("limit", "sample", "head", "take", "first")
    modulos = [
        p for p in sorted(root.rglob("*.py"))
        if p.parent.name == p.stem and not p.name.startswith("exemplo_")
    ]
    violacoes = 0

    def dentro_do_corpo_de_try(arvore: ast.AST, alvo: ast.AST) -> bool:
        for no in ast.walk(arvore):
            if isinstance(no, ast.Try) and any(
                sub is alvo for statement in no.body for sub in ast.walk(statement)
            ):
                return True
        return False

    def receiver_name(node: ast.AST) -> str | None:
        while isinstance(node, ast.Attribute):
            node = node.value
        return node.id if isinstance(node, ast.Name) else None

    def dataframe_receiver(node: ast.AST, tree: ast.AST) -> bool:
        name = receiver_name(node)
        if not name:
            return False
        lowered = name.lower()
        if lowered in {"df", "dataframe", "frame"} or lowered.startswith("df_") or lowered.endswith("_df"):
            return True
        for function in (item for item in ast.walk(tree) if isinstance(item, ast.FunctionDef)):
            for argument in [*function.args.posonlyargs, *function.args.args, *function.args.kwonlyargs]:
                if argument.arg != name or argument.annotation is None:
                    continue
                try:
                    if "DataFrame" in ast.unparse(argument.annotation):
                        return True
                except Exception:
                    pass
        return False

    def expression_has_limiter(node: ast.AST) -> bool:
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute) and child.func.attr in LIMITADORES:
                    return True
                if isinstance(child.func, ast.Name) and child.func.id in {"smart_sample", *LIMITADORES}:
                    return True
        return False

    def assigned_from_limiter(tree: ast.AST, name: str, before_line: int) -> bool:
        for child in ast.walk(tree):
            if not isinstance(child, (ast.Assign, ast.AnnAssign)) or child.lineno >= before_line:
                continue
            targets = child.targets if isinstance(child, ast.Assign) else [child.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                value = child.value
                if value is not None and expression_has_limiter(value):
                    return True
        return False

    def direct_nodes(scope: ast.AST):
        stack = list(getattr(scope, "body", []))
        while stack:
            node = stack.pop()
            yield node
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            stack.extend(ast.iter_child_nodes(node))

    def scope_bindings(scope: ast.AST) -> set[str]:
        bound: set[str] = set()
        if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)):
            bound |= {
                argument.arg
                for argument in [
                    *scope.args.posonlyargs, *scope.args.args,
                    *scope.args.kwonlyargs,
                ]
            }
        for node in direct_nodes(scope):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                bound |= {target.id for target in targets if isinstance(target, ast.Name)}
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                bound |= {alias.asname or alias.name.split(".")[0] for alias in node.names}
        return bound

    for modulo in modulos:
        texto = modulo.read_text(encoding="utf-8")
        try:
            arvore = ast.parse(texto)
        except SyntaxError:
            continue
        linhas = texto.splitlines()
        rel = modulo.relative_to(root)

        for no in ast.walk(arvore):
            if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)):
                continue
            if (
                no.func.attr in ("cache", "persist")
                and dataframe_receiver(no.func.value, arvore)
                and not dentro_do_corpo_de_try(arvore, no)
            ):
                violacoes += 1
                problems.append(
                    f"{rel}:{no.lineno}: `{no.func.attr}()` fora de `try` — o molde "
                    "de `hub_padroes/snippet/` diz que são bloqueados em serverless. "
                    "O padrão da casa é degradar, como em `_cache_if_supported`"
                )
            if no.func.attr == "toPandas":
                name = receiver_name(no.func.value)
                limited = expression_has_limiter(no.func.value) or (
                    bool(name) and assigned_from_limiter(arvore, name, no.lineno)
                )
                if not limited:
                    violacoes += 1
                    problems.append(
                        f"{rel}:{no.lineno}: `toPandas()` sem limite verificável — o "
                        "molde proíbe. Passe por `smart_sample`, `limit` ou equivalente"
                    )

        scopes: list[ast.AST] = [arvore]
        scopes.extend(
            node for node in ast.walk(arvore)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        for scope in scopes:
            bindings = scope_bindings(scope)
            if "spark" in bindings:
                continue
            for no in direct_nodes(scope):
                if isinstance(no, ast.Name) and no.id == "spark" and isinstance(no.ctx, ast.Load):
                    violacoes += 1
                    problems.append(
                        f"{rel}:{no.lineno}: usa o global `spark`, que **não existe** "
                        "dentro de módulo importado. Use "
                        "`SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()`"
                    )
                    break

    secoes = 0
    for init in sorted(root.rglob("__init__.py")):
        if (init.parent / f"{init.parent.name}.py").exists():
            continue                      # pasta de objeto: reexportar é a regra
        secoes += 1
        for numero, linha in enumerate(init.read_text(encoding="utf-8").splitlines(), 1):
            if linha.strip().startswith("from ."):
                violacoes += 1
                problems.append(
                    f"{init.relative_to(root)}:{numero}: `__init__.py` de seção "
                    "reexporta — o molde proíbe. Uma seção que reexporta importa "
                    "todos os objetos de uma vez, e os sete de `ml/` com dependência "
                    "opcional derrubariam os irmãos junto"
                )
    return len(modulos) + secoes, violacoes


def check_notebook_exercita_o_objeto(root: Path, problems: list[str]) -> tuple[int, int]:
    """O notebook do objeto precisa **chamar** pelo menos uma função pública dele.

    O molde diz que o notebook "ensina" o objeto. Um notebook que importa o módulo
    e nunca o executa não ensina nada — e passa em tudo: importa, valida, e roda
    como job com `SUCCESS`, porque não há o que quebrar.

    Foi assim que `exemplo_vintage_analysis.py` viveu duas sprints. Ele importava
    `build_vintage_table` na última célula, convertia a base para pandas, e
    terminava. As quatro funções públicas do módulo nunca foram chamadas por
    ninguém, e o relatório da Sprint 7 registrou o notebook como `SUCCESS` — o que
    era verdade e não significava nada.

    A guarda nasceu de uma medição: **1 de 60**. Por isso já nasce como falha; se
    fossem trinta, seria aviso com prazo.

    O que ela **não** cobre: chamar não é exercitar bem. Um notebook que chama a
    função uma vez e ignora o resultado passa aqui. A leitura do resultado é
    cobrada por `check_saida_colada`, que é outra guarda e outro defeito.
    """
    conferidos = mudos = 0
    for modulo in sorted(root.rglob("*.py")):
        if modulo.parent.name != modulo.stem or modulo.name.startswith("exemplo_"):
            continue
        notebook = modulo.parent / f"exemplo_{modulo.stem}.py"
        if not notebook.exists():
            continue
        try:
            arvore_modulo = ast.parse(modulo.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        publicas = {
            no.name for no in arvore_modulo.body
            if isinstance(no, (ast.FunctionDef, ast.ClassDef)) and not no.name.startswith("_")
        }
        if not publicas:
            continue
        conferidos += 1
        codigo = "\n".join(
            linha for linha in notebook.read_text(encoding="utf-8").splitlines()
            if not linha.startswith("# MAGIC")
        )
        try:
            arvore_nb = ast.parse(codigo)
        except SyntaxError:
            continue
        chamadas = set()
        for no in ast.walk(arvore_nb):
            if isinstance(no, ast.Call):
                if isinstance(no.func, ast.Name):
                    chamadas.add(no.func.id)
                elif isinstance(no.func, ast.Attribute):
                    chamadas.add(no.func.attr)
        if not (chamadas & publicas):
            mudos += 1
            problems.append(
                f"{notebook.relative_to(root)}: não chama nenhuma função pública de "
                f"`{modulo.stem}` ({', '.join(sorted(publicas))}). O notebook existe "
                "para ensinar o objeto, e importar não é executar"
            )
    return conferidos, mudos


def check_pasta_de_objeto_malformada(root: Path, problems: list[str]) -> int:
    """Pega a pasta de objeto que `check_pastas_de_objeto` não alcança.

    Aquela função só enxerga a pasta quando o módulo se chama como ela. O caso
    em que o nome **diverge** — que é justamente o erro — passava despercebido,
    e o validador devolvia APROVADO sobre um objeto que nunca seria importável
    pelo caminho documentado.

    Aqui a regra é invertida: toda pasta dentro de `hub_snippets/<secao>/` ou de
    `hub_scripts/` que tenha `__init__.py` **precisa** ter `<nome>.py`. Se tiver
    outro módulo no lugar, é defeito, não estrutura desconhecida.
    """
    verificadas = 0
    raizes = [
        (root / ".assistant" / "hub_scripts", None),
        (root / ".assistant" / "hub_snippets", _SECOES_DE_BIBLIOTECA),
    ]
    for raiz, secoes in raizes:
        if not raiz.is_dir():
            continue
        candidatas = []
        if secoes is None:
            candidatas = [d for d in raiz.iterdir() if d.is_dir()]
        else:
            for secao in sorted(secoes):
                if (raiz / secao).is_dir():
                    candidatas += [d for d in (raiz / secao).iterdir() if d.is_dir()]
        for pasta in candidatas:
            if not (pasta / "__init__.py").exists():
                continue
            verificadas += 1
            if (pasta / f"{pasta.name}.py").exists():
                continue  # forma correta; o outro check cuida do resto
            outros = [
                p.name for p in pasta.glob("*.py")
                if p.name != "__init__.py" and not eh_notebook(p)
            ]
            rel = pasta.relative_to(root)
            achado = f" (encontrei {', '.join(sorted(outros))})" if outros else ""
            problems.append(
                f"{rel}: pasta de objeto sem '{pasta.name}.py'{achado} — o módulo "
                "precisa ter o nome da pasta, ou o import documentado não existe"
            )
    return verificadas


def check_contrato_de_dados(root: Path, problems: list[str]) -> int:
    """Confronta o que o módulo devolve com o que o notebook irmão consome.

    Duas vezes seguidas a mesma classe de defeito atravessou todos os portões:
    três notebooks publicados pedindo chaves que a biblioteca havia renomeado, e
    um filtro por `status != 'ok'` num módulo cujo status é emoji. Nenhum dos
    checks existentes vê isso — eles conferem sintaxe, link e **nome exportado**,
    nunca **valor devolvido**.

    O que esta guarda extrai do módulo, por AST:

    - chaves de dicionário literais (`{"cobertura_pct": ...}` e `d["x"] = ...`);
    - nomes criados por `alias("nome")`, que viram coluna de DataFrame;
    - literais de string atribuídos a variável, que cobrem domínios como o
      semáforo do `null_summary`.

    O que ela cobra do notebook: todo acesso literal por string — `d["k"]`,
    `d.get("k")`, `filter("col != 'v'")`, `select("col")` — cujo alvo não esteja
    no conjunto acima **nem** tenha sido criado pelo próprio notebook.

    Não pega tudo: chave montada por concatenação e acesso por variável passam.
    Pega a forma que já falhou duas vezes.
    """
    def literal_string(node: ast.AST | None) -> str | None:
        return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None

    def produced_names(tree: ast.AST, *, include_return_literals: bool = True) -> set[str]:
        produced: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                produced |= {value for key in node.keys if (value := literal_string(key))}
                if include_return_literals:
                    produced |= {value for item in node.values if (value := literal_string(item))}
            elif isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Store):
                value = literal_string(node.slice)
                if value:
                    produced.add(value)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"alias", "withColumn", "withColumnRenamed"} and node.args:
                    value = literal_string(node.args[-1] if node.func.attr == "withColumnRenamed" else node.args[0])
                    if value:
                        produced.add(value)
                if not include_return_literals and node.func.attr == "count":
                    produced.add("count")
                if not include_return_literals and node.func.attr == "lit" and node.args:
                    value = literal_string(node.args[0])
                    if value:
                        produced.add(value)
            elif not include_return_literals and isinstance(node, (ast.List, ast.Tuple, ast.Set)):
                produced |= {value for item in node.elts if (value := literal_string(item))}
            elif not include_return_literals and isinstance(node, ast.Compare):
                if any(
                    isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Attribute)
                    and child.func.attr == "col"
                    for child in ast.walk(node)
                ):
                    produced |= {
                        child.value for child in ast.walk(node)
                        if isinstance(child, ast.Constant) and isinstance(child.value, str)
                    }
            elif include_return_literals and isinstance(node, (ast.Assign, ast.AnnAssign)):
                value = literal_string(node.value)
                if value:
                    produced.add(value)
            elif include_return_literals and isinstance(node, ast.Return):
                produced |= {
                    child.value for child in ast.walk(node)
                    if isinstance(child, ast.Constant) and isinstance(child.value, str)
                }
        return produced

    def consumed_names(tree: ast.AST) -> set[str]:
        consumed: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):
                value = literal_string(node.slice)
                if value:
                    consumed.add(value)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "get" and node.args:
                    value = literal_string(node.args[0])
                    if value:
                        consumed.add(value)
                if node.func.attr in {"select", "drop", "groupBy", "orderBy"}:
                    consumed |= {value for arg in node.args if (value := literal_string(arg))}
            elif isinstance(node, ast.Compare) and any(
                isinstance(operator, (ast.Eq, ast.NotEq)) for operator in node.ops
            ):
                consumed |= {
                    child.value for child in ast.walk(node)
                    if isinstance(child, ast.Constant) and isinstance(child.value, str)
                }
        return consumed

    verificadas = 0
    for init in sorted(root.rglob("__init__.py")):
        pasta = init.parent
        modulo = pasta / f"{pasta.name}.py"
        notebook = pasta / f"exemplo_{pasta.name}.py"
        if not (modulo.exists() and notebook.exists()):
            continue
        verificadas += 1
        texto_modulo = modulo.read_text(encoding="utf-8")
        texto_nb = notebook.read_text(encoding="utf-8")
        rel = pasta.relative_to(root)
        try:
            tree_module = ast.parse(texto_modulo)
            tree_notebook = ast.parse(texto_nb)
        except SyntaxError:
            continue

        produzidos = produced_names(tree_module)
        dynamic_prefixes = {
            "".join(
                part.value for part in node.values
                if isinstance(part, ast.Constant) and isinstance(part.value, str)
            )
            for node in ast.walk(tree_module)
            if isinstance(node, ast.JoinedStr)
        }
        dynamic_prefixes.discard("")
        # O notebook também cria e recebe nomes: de `alias`/`withColumn`, do
        # esquema que ele declara, e de qualquer nome que ele **passe** ao helper
        # como argumento — `date_col="dt_referencia"` diz que aquela coluna vem
        # da base, não do retorno. Sem isso a guarda acusa a própria entrada.
        produzidos |= produced_names(tree_notebook, include_return_literals=False)
        produzidos |= set(re.findall(r"""alias\(\s*["']([^"']+)["']""", texto_nb))
        produzidos |= set(re.findall(r"""withColumn\(\s*["']([^"']+)["']""", texto_nb))
        produzidos |= set(re.findall(r"""f?["'][^"']*\b(\w+) (?:string|int|double|date|boolean)""", texto_nb))
        produzidos |= set(re.findall(r"""\w+\s*=\s*["']([a-z_]{3,})["']""", texto_nb))
        # Coluna criada por atribuição no próprio notebook: `df["nova"] = ...`
        produzidos |= set(re.findall(
            r"""\w+\[\s*["']([a-z_]{3,})["']\s*\]\s*=[^=]""", texto_nb
        ))
        # Colunas das fixtures: são a entrada de quase todo notebook do Hub.
        fixtures = root / ".assistant" / "hub_snippets" / "testing" / "fixtures"
        if fixtures.is_dir():
            for f in fixtures.glob("*.py"):
                produzidos |= set(re.findall(
                    r"""\b(\w+) (?:string|int|double|date|boolean)""",
                    f.read_text(encoding="utf-8"),
                ))

        # Valores de argumentos nomeados são contrato de entrada e não precisam
        # ser produzidos pelo módulo irmão.
        for call in (node for node in ast.walk(tree_notebook) if isinstance(node, ast.Call)):
            for keyword in call.keywords:
                value = literal_string(keyword.value)
                if value:
                    produzidos.add(value)

        for chave in sorted(consumed_names(tree_notebook) - produzidos):
            if chave.isdigit():
                continue
            if any(chave.startswith(prefix) for prefix in dynamic_prefixes):
                continue
            problems.append(
                f"{rel}/{notebook.name}: consome '{chave}', que não é entrada "
                f"declarada nem saída efetiva de {modulo.name}"
            )
    return verificadas


def _assinaturas_publicas(arvore: ast.Module) -> dict[str, ast.arguments]:
    """Mapeia nome chamável -> assinatura, para funções e classes de nível superior.

    Classe entra pelo próprio nome, apontando para o `__init__`: no notebook a
    chamada é `PerformanceMonitor(...)`, não `__init__(...)`.
    """
    assinaturas: dict[str, ast.arguments] = {}
    for no in arvore.body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not no.name.startswith("_"):
                assinaturas[no.name] = no.args
        elif isinstance(no, ast.ClassDef) and not no.name.startswith("_"):
            for filho in no.body:
                if isinstance(filho, ast.FunctionDef) and filho.name == "__init__":
                    assinaturas[no.name] = filho.args
    return assinaturas


def check_contrato_de_entrada(root: Path, problems: list[str]) -> int:
    """Confronta o que o notebook **passa** com o que o módulo **aceita**.

    `check_contrato_de_dados` cobre a direção de saída: nome que o notebook
    consome do retorno. A direção oposta — argumento que o notebook passa — não
    tinha portão nenhum, e é por onde entraram seis dos dezesseis defeitos da
    Sprint 7: `n_bandas` em vez de `n_bands`, `thresholds` num construtor que
    pede `baseline_metrics`, `feature_cols` omitido sendo obrigatório.

    Confere, por AST, toda chamada do notebook a função ou classe pública do
    módulo irmão:

    - argumento nomeado que a assinatura não tem (e não há `**kwargs`);
    - posicionais a mais (e não há `*args`);
    - parâmetro obrigatório sem valor.

    Não pega: chamada por variável (`fn = modulo.f; fn(...)`), desempacotamento
    (`f(**cfg)`), e incompatibilidade de **tipo** ou de coluna dentro de um
    DataFrame — que continuam custando execução real para aparecer.
    """
    verificadas = 0
    for init in sorted(root.rglob("__init__.py")):
        pasta = init.parent
        modulo = pasta / f"{pasta.name}.py"
        notebook = pasta / f"exemplo_{pasta.name}.py"
        if not (modulo.exists() and notebook.exists()):
            continue
        try:
            arv_mod = ast.parse(modulo.read_text(encoding="utf-8"))
            arv_nb = ast.parse(notebook.read_text(encoding="utf-8"))
        except SyntaxError:
            continue  # o check de sintaxe já reprovou este arquivo
        assinaturas = _assinaturas_publicas(arv_mod)
        if not assinaturas:
            continue
        verificadas += 1
        rel = pasta.relative_to(root)

        direct_aliases: dict[str, str] = {}
        module_aliases: set[str] = set()
        for node in ast.walk(arv_nb):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    local = alias.asname or alias.name
                    if alias.name in assinaturas:
                        direct_aliases[local] = alias.name
                    else:
                        module_aliases.add(local)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module_aliases.add(alias.asname or alias.name.split(".")[0])

        for chamada in ast.walk(arv_nb):
            if not isinstance(chamada, ast.Call):
                continue
            alvo: str | None = None
            if isinstance(chamada.func, ast.Name):
                alvo = direct_aliases.get(chamada.func.id, chamada.func.id)
            elif (
                isinstance(chamada.func, ast.Attribute)
                and isinstance(chamada.func.value, ast.Name)
                and chamada.func.value.id in module_aliases
            ):
                alvo = chamada.func.attr
            if alvo is None:
                continue
            args = assinaturas.get(alvo)
            if args is None:
                continue

            posicionais = [a.arg for a in args.posonlyargs] + [a.arg for a in args.args]
            if posicionais and posicionais[0] in ("self", "cls"):
                posicionais = posicionais[1:]
            somente_nome = [a.arg for a in args.kwonlyargs]
            aceitos = set(posicionais) | set(somente_nome)

            if any(isinstance(a, ast.Starred) for a in chamada.args):
                continue  # desempacotamento: a contagem deixa de ser confiável
            passados_nome = {k.arg for k in chamada.keywords if k.arg}
            tem_duplo_asterisco = any(k.arg is None for k in chamada.keywords)

            if not args.kwarg:
                for nome in sorted(passados_nome - aceitos):
                    problems.append(
                        f"{rel}/{notebook.name}: {alvo}(...) recebe '{nome}=', "
                        f"que não existe na assinatura de {modulo.name}"
                    )
            if not args.vararg and len(chamada.args) > len(posicionais):
                problems.append(
                    f"{rel}/{notebook.name}: {alvo}(...) recebe "
                    f"{len(chamada.args)} posicionais; a assinatura aceita "
                    f"{len(posicionais)}"
                )
            if not tem_duplo_asterisco:
                n_com_padrao = len(args.defaults)
                obrigatorios = posicionais[:len(posicionais) - n_com_padrao]
                cobertos = set(posicionais[:len(chamada.args)]) | passados_nome
                for nome in obrigatorios:
                    if nome not in cobertos:
                        problems.append(
                            f"{rel}/{notebook.name}: {alvo}(...) não passa "
                            f"'{nome}', que é obrigatório"
                        )
                for arg, padrao in zip(args.kwonlyargs, args.kw_defaults):
                    if padrao is None and arg.arg not in passados_nome:
                        problems.append(
                            f"{rel}/{notebook.name}: {alvo}(...) não passa "
                            f"'{arg.arg}', que é obrigatório e só por nome"
                        )
    return verificadas


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
    import tempfile
    from types import SimpleNamespace

    try:
        tree = ast.parse(smoke.read_text(encoding="utf-8"))
    except SyntaxError:
        return
    selected: list[ast.stmt] = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name)
            and target.id in {"MARCADOR_NOTEBOOK", "_PREFIXOS_TOLERADOS"}
            for target in node.targets
        ):
            selected.append(node)
        if isinstance(node, ast.FunctionDef) and node.name == "modulo_e_notebook":
            selected.append(node)
    namespace: dict[str, object] = {}
    try:
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(smoke), "exec"), namespace)
        detector = namespace["modulo_e_notebook"]
    except Exception as exc:
        problems.append(f"spark_smoke_test.py: detector não pôde ser carregado ({exc})")
        return

    cases = {
        "marker": "# Databricks notebook source\nprint('ok')\n",
        "bom_blank": "\ufeff\n# Databricks notebook source\n",
        "encoding": "# -*- coding: utf-8 -*-\n# Databricks notebook source\n",
        "code_before": "x = 1\n# Databricks notebook source\n",
        "empty": "",
    }
    with tempfile.TemporaryDirectory(prefix="hub-notebook-marker-") as directory:
        finder = SimpleNamespace(path=directory)
        for name, content in cases.items():
            Path(directory, f"{name}.py").write_text(content, encoding="utf-8")
            expected = texto_e_notebook(content)
            actual = bool(detector(finder, name, False))
            if actual != expected:
                problems.append(
                    f"spark_smoke_test.py: detector diverge no caso {name!r} "
                    f"(canônico={expected}, smoke={actual})"
                )
        if detector(finder, "marker", True):
            problems.append("spark_smoke_test.py: pacote foi classificado como notebook")


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
    """Inventário versionado, independente de arquivos locais ignorados."""
    return [p for p in git_paths(REPO_ROOT)
            if not any(parte in REPO_IGNORE for parte in p.relative_to(REPO_ROOT).parts)]


def check_worktree_hygiene(problems: list[str]) -> int:
    """Extras são examinados sem alterar a contagem certificada do versionado."""
    paths = [p for p in git_paths(REPO_ROOT, untracked=True)
             if not any(part in REPO_IGNORE or part in {".pytest_cache", ".ruff_cache"}
                        for part in p.relative_to(REPO_ROOT).parts)]
    count = 0
    for p in paths:
        rel = p.relative_to(REPO_ROOT)
        if CORPORATE_RE.search(str(rel)) or PERSONAL_RE.search(str(rel)):
            problems.append(f"worktree: identidade no caminho {rel}")
        if not p.is_file() or p.suffix not in {".md", ".py", ".json", ".txt"}:
            continue
        count += 1
        try:
            content = p.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            problems.append(f"worktree: arquivo ilegível/UTF-8 inválido: {rel}")
            continue
        if CORPORATE_RE.search(content) or PERSONAL_RE.search(content) or MOJIBAKE_RE.search(content):
            problems.append(f"worktree: higiene de conteúdo inválida: {rel}")
        if p.suffix == ".md":
            for match in MD_LINK_RE.finditer(content):
                target = match.group(1)
                if not target.startswith(("http://", "https://", "mailto:")) and not alvo_existe(p.parent, target):
                    problems.append(f"worktree: link quebrado em {rel}: {target}")
    return count


def check_repo_corporate(problems: list[str]) -> int:
    """Varre o repositório editável/derivado atrás de identidade pessoal/corporativa.

    O check de caminho abaixo cobre apenas a raiz analisada, e o vetor descrito
    nos ADRs 0003/0009 se materializa também fora dela: no simulado versionado e
    nos documentos ativos. A busca cobre padrões corporativos e pessoais.
    Referências congeladas continuam fora desta guarda e entram somente no modo
    ``security`` do bundle de auditoria.

    A varredura parte de `REPO_ROOT`, não do diretório atual: antes disso, rodar
    o comando de outra pasta reduzia a varredura sem alterar o veredito.
    """
    verificados = 0
    for caminho in iter_repo_files():
        relativo = caminho.relative_to(REPO_ROOT)
        if CORPORATE_RE.search(str(relativo)) or PERSONAL_RE.search(str(relativo)):
            problems.append(f"{relativo}: identificador pessoal/corporativo no caminho")
        if not caminho.exists():
            problems.append(f"arquivo versionado ausente na worktree: {relativo}")
            continue
        if not caminho.is_file() or caminho.suffix not in {".md", ".py", ".txt", ".json"}:
            continue
        verificados += 1
        try:
            content = caminho.read_text(encoding="utf-8")
            if CORPORATE_RE.search(content) or PERSONAL_RE.search(content):
                problems.append(f"{relativo}: identificador pessoal/corporativo no conteúdo")
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
            if not alvo_existe(caminho.parent, alvo):
                problems.append(f"{relativo}: link relativo quebrado -> {alvo}")
    # Mesma guarda do check corporativo, e pelo mesmo motivo: varredura vazia é
    # indistinguível de varredura limpa na saída, e o README prometia que ambas
    # reprovassem. Só uma reprovava — uma auditoria mostrou.
    if verificados == 0:
        problems.append(
            "check de links do repositório não conferiu nenhum link — a rede "
            "não rodou; não trate este resultado como aprovação"
        )
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
    parser.add_argument(
        "--conferir-readme",
        action="store_true",
        dest="conferir_readme",
        help="confere apenas contagens locais do README; não chama Databricks",

    )
    parser.add_argument("--conferir-readme-remoto", action="store_true",
                        help="confere somente o bloco remoto; exige CLI/autenticação Databricks")
    parser.add_argument("--root", default="ambiente_fonte", type=Path)
    args = parser.parse_args()

    root = (REPO_ROOT / args.root).resolve()
    if not root.exists():
        print(f"FAIL raiz não encontrada: {root}")
        return 1

    problems: list[str] = []
    warnings: list[str] = []

    n_skills = check_skill_frontmatter(root, problems)
    n_prompts, n_prompt_fields = check_prompt_contract(root, problems)
    check_skill_sizes(root, warnings)
    check_pycache(root, warnings)
    n_md, n_links = check_markdown(root, problems)
    n_nb, n_nb_links = check_notebook_links(root, problems)
    n_py = check_python_ast(root, problems)
    n_chars = check_instructions_size(root, problems)
    check_text_hygiene(root, problems)
    check_path_hygiene(root, problems)
    n_objetos = check_pastas_de_objeto(root, problems)
    n_malformadas = check_pasta_de_objeto_malformada(root, problems)
    n_contratos = check_contrato_de_dados(root, problems)
    n_entradas = check_contrato_de_entrada(root, problems)
    n_com_saida, n_sem_saida = check_saida_colada(root, problems)
    check_smoke_test_sincronizado(problems)
    n_helpers = check_skill_helpers_resolvem(root, problems)
    n_secoes, n_completas = check_skill_secoes(root, problems)
    n_doc, n_doc_en = check_docstring_em_portugues(root, problems)
    n_norma, n_norma_ruim = check_normas_do_molde(root, problems)
    n_nb_obj, n_nb_mudos = check_notebook_exercita_o_objeto(root, problems)
    n_readme = 0
    if args.conferir_readme:
        n_readme = check_saida_de_comando_no_readme(problems)
    if args.conferir_readme_remoto:
        n_readme += check_saida_de_comando_no_readme(problems, remoto=True)
    n_repo = n_repo_links = n_extras = 0
    try:
        n_repo = check_repo_corporate(problems)
        n_repo_links = check_repo_links(root, problems)
        n_extras = check_worktree_hygiene(problems)
    except (ValueError, UnicodeError) as exc:
        problems.append(f"inventário não certificado: {exc}")

    print(f"raiz analisada     : {root}")
    print(f"skills             : {n_skills} · {n_completas}/{n_secoes} com as 5 seções estruturais")
    print(f"prompts            : {n_prompts} · {n_prompt_fields} campos com guia e contrato humano")
    print(f"helpers citados    : {n_helpers} caminhos verificados")
    if args.conferir_readme:
        print(f"saída no README    : {n_readme} linhas conferidas contra execução real")
    print(f"markdown / links   : {n_md} arquivos / {n_links} links relativos")
    print(f"notebooks / links  : {n_nb} notebooks / {n_nb_links} links relativos")
    print(f"pastas de objeto   : {n_objetos} conferidas (nome, arquivos, __init__)")
    print(f"forma da pasta     : {n_malformadas} conferidas (o módulo tem o nome da pasta)")
    print(f"contrato de dados  : {n_contratos} pares (saída: o que o notebook consome)")
    print(f"contrato de entrada: {n_entradas} pares (entrada: o que o notebook passa)")
    print(f"saída colada       : {n_com_saida} notebooks com bloco real, {n_sem_saida} sem")
    print(f"idioma da docstring: {n_doc} módulos, {n_doc_en} com docstring em inglês")
    print(f"normas do molde    : {n_norma} arquivos, {n_norma_ruim} violação(ões)")
    print(f"notebook exercita  : {n_nb_obj} objetos, {n_nb_mudos} notebook(s) que só importam")
    print(f"python (AST)       : {n_py} arquivos")
    print(f"instrucoes         : {n_chars}/{INSTRUCTION_LIMIT} caracteres")
    print(f"repo (identidade)  : {n_repo} arquivos varridos no repositório editável/derivado")
    print(f"repo (links)       : {n_repo_links} links fora da raiz analisada")
    print(f"worktree (extras)  : {n_extras} arquivos locais examinados, fora da contagem versionada")
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
