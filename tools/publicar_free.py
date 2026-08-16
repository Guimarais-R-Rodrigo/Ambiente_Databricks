"""Publica o ecossistema no Databricks Free e confere o resultado.

Três fases, no padrão do engine `databricks-genie` do Verg_Alchemy_Hub:

    python tools/publicar_free.py             # plano (dry-run), nada é escrito
    python tools/publicar_free.py --execute   # publica
    python tools/publicar_free.py --verify    # confere o remoto (read-only)

O ADR-0005 registra por que a publicação é feita aqui em vez de pelo engine do
Hub: aquele engine importa `.py` como notebook, o que quebraria os imports de
`x_snippets`, e injeta cabeçalho, o que invalidaria o frontmatter das skills.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# `import-dir` não honra o marcador de notebook: envia tudo como arquivo. Os
# módulos da biblioteca precisam mesmo ser arquivo, senão o import quebra — mas o
# material didático precisa ser notebook, ou não há células para executar.
# A detecção é canônica em notebook_marker.py; ver o docstring de lá.
from notebook_marker import eh_notebook  # noqa: E402

SIMULADO = Path("Novo_Ambiente_Simulado")
CORPORATE_RE = re.compile(r"c\d{6}|corp\.|\.gov\.br", re.IGNORECASE)

# Estrutura mínima que o Genie Code precisa encontrar para descobrir o ecossistema.
EXPECTED_SKILLS = 12
EXPECTED_X_DIRS = {"x_config", "x_docs", "x_projects", "x_prompts", "x_scripts", "x_snippets"}

# Arquivos que a **plataforma** cria dentro de `.assistant/` e que não vêm da
# fonte. Observado em 2026-08-15: abrir o painel de MCP em Genie Code → Settings
# materializa `.assistant/.mcp_servers.json` com os conectores internos. Sem esta
# lista, a conferência os classificaria como obsoletos e mandaria removê-los.
GERENCIADOS_PELA_PLATAFORMA = {".assistant/.mcp_servers.json"}


def databricks(*args: str) -> tuple[int, str, str]:
    """Retorna (returncode, stdout, stderr) separados.

    stdout e stderr nunca são concatenados: a CLI emite avisos em stderr que,
    misturados à saída, corrompem o parse de JSON.
    """
    proc = subprocess.run(
        ["databricks", *args], capture_output=True, text=True, encoding="utf-8"
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def databricks_json(*args: str) -> object | None:
    """Executa a CLI e devolve o JSON de stdout, ou None se não houver."""
    rc, out, _err = databricks(*args)
    if rc != 0 or not out.strip():
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def resolve_home() -> tuple[str, str]:
    identidade = databricks_json("current-user", "me", "-o", "json")
    if not isinstance(identidade, dict) or "userName" not in identidade:
        raise SystemExit("FAIL não foi possível resolver o usuário pela CLI.")
    user = identidade["userName"]
    if CORPORATE_RE.search(user):
        raise SystemExit(
            "FAIL usuário com aparência corporativa. Esta ferramenta publica no\n"
            "     laboratório Free; o workspace do trabalho usa o runbook manual\n"
            "     (docs/playbooks/replicacao-trabalho.md)."
        )
    return f"/Users/{user}", user


def local_tree() -> tuple[Path, list[Path]]:
    """Retorna a raiz do usuário renderizada e os arquivos que serão publicados."""
    users_dir = SIMULADO / "Users"
    if not users_dir.exists():
        raise SystemExit(
            "FAIL simulado ausente. Rode antes:\n"
            "     python tools/validate_assistant.py\n"
            "     python tools/render_simulado.py --write"
        )
    roots = [p for p in users_dir.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise SystemExit(f"FAIL esperado exatamente um diretório de usuário, achei {len(roots)}")
    root = roots[0]
    return root, sorted(p for p in root.rglob("*") if p.is_file())


def remote_list(path: str) -> list[dict]:
    itens = databricks_json("workspace", "list", path, "-o", "json")
    return itens if isinstance(itens, list) else []


def remote_walk(path: str) -> list[dict]:
    """Percorre recursivamente a árvore remota."""
    encontrados: list[dict] = []
    for item in remote_list(path):
        encontrados.append(item)
        if item.get("object_type") == "DIRECTORY":
            encontrados.extend(remote_walk(item["path"]))
    return encontrados


def cmd_plan(root: Path, arquivos: list[Path], home: str, executar: bool) -> int:
    modo = "EXECUTE" if executar else "DRY-RUN"
    print(f"== PUBLICAR NO FREE ({modo}) ==")
    print(f"fonte  : {root}")
    print(f"destino: {home}")
    print(f"arquivos: {len(arquivos)}")

    por_area: dict[str, int] = {}
    for arquivo in arquivos:
        relativo = arquivo.relative_to(root)
        area = relativo.parts[1] if len(relativo.parts) > 1 else relativo.parts[0]
        por_area[area] = por_area.get(area, 0) + 1
    for area, total in sorted(por_area.items()):
        print(f"  {area:24} {total:4d}")

    if not executar:
        print("\nDRY-RUN: nada foi publicado. Use --execute para publicar.")
        return 0

    rc, out, err = databricks("workspace", "import-dir", str(root), home, "--overwrite")
    if rc != 0:
        print(f"\nFAIL publicação falhou:\n{out}{err}")
        return 1

    # Reenviar como notebook o material didático, que o import-dir mandou como
    # arquivo. Sem isto não há células para executar.
    cadernos = [a for a in arquivos if eh_notebook(a)]
    for caderno in cadernos:
        relativo = str(caderno.relative_to(root)).replace("\\", "/")
        destino = f"{home}/{relativo[:-3]}"  # o workspace guarda notebook sem .py
        rc, _out, err = databricks(
            "workspace", "import", destino, "--file", str(caderno),
            "--format", "SOURCE", "--language", "PYTHON", "--overwrite",
        )
        if rc != 0:
            print(f"FAIL notebook {relativo}: {err.strip()[:160]}")
            return 1
    if cadernos:
        print(f"  {len(cadernos)} arquivo(s) reenviado(s) como notebook")

    print(f"\nPublicado. Confira com: python {Path(__file__).name} --verify")
    return 0


def _ancestrais(caminho: str) -> set[str]:
    """Todos os diretórios intermediários de um caminho relativo."""
    partes = caminho.split("/")
    return {"/".join(partes[:i]) for i in range(1, len(partes))}


def cmd_verify(root: Path, arquivos: list[Path], home: str) -> int:
    print("== VERIFY (read-only) ==")
    problemas: list[str] = []

    # O workspace guarda notebook sem a extensão: o nome esperado muda.
    esperados = set()
    esperado_notebook = set()
    for arquivo in arquivos:
        relativo = str(arquivo.relative_to(root)).replace("\\", "/")
        if eh_notebook(arquivo):
            esperados.add(relativo[:-3])
            esperado_notebook.add(relativo[:-3])
        else:
            esperados.add(relativo)
    arvore_remota = remote_walk(f"{home}/.assistant")
    remotos = {
        item["path"][len(home) + 1 :]: item
        for item in arvore_remota
        if item.get("object_type") != "DIRECTORY"
    }
    instrucoes = databricks_json(
        "workspace", "get-status", f"{home}/.assistant_instructions.md", "-o", "json"
    )
    if isinstance(instrucoes, dict):
        remotos[".assistant_instructions.md"] = instrucoes

    ausentes = sorted(esperados - set(remotos))
    for nome in ausentes:
        problemas.append(f"ausente no remoto: {nome}")

    # `import-dir --overwrite` sobrescreve, mas nunca apaga: arquivo removido da
    # fonte sobrevive no workspace e continua sendo lido pelo Genie Code.
    obsoletos = sorted(set(remotos) - esperados - GERENCIADOS_PELA_PLATAFORMA)

    # Diretório sofre do mesmo problema e não aparece na conta de arquivos: uma
    # pasta esvaziada na fonte sobrevive no workspace sem nenhum arquivo dentro,
    # invisível para a comparação acima.
    esperado_dirs = {
        str(Path(nome).parent).replace("\\", "/")
        for nome in esperados
        if "/" in nome
    }
    esperado_dirs |= {
        pai for nome in esperado_dirs for pai in _ancestrais(nome)
    }
    remoto_dirs = {
        item["path"][len(home) + 1 :]
        for item in arvore_remota
        if item.get("object_type") == "DIRECTORY"
    }
    obsoletos += sorted(remoto_dirs - esperado_dirs)
    for nome in obsoletos:
        problemas.append(f"obsoleto no remoto (remover à mão): {nome}")

    # `.py` de biblioteca precisa ser FILE: como NOTEBOOK, o import quebra.
    # Material didático é o oposto: como FILE, não há células para executar.
    for nome, item in sorted(remotos.items()):
        tipo = item.get("object_type")
        if nome.endswith(".py") and tipo != "FILE":
            problemas.append(f"{nome}: importado como {tipo}, esperado FILE")
        if nome in esperado_notebook and tipo != "NOTEBOOK":
            problemas.append(f"{nome}: importado como {tipo}, esperado NOTEBOOK")

    skills = [
        item for item in remote_list(f"{home}/.assistant/skills")
        if item.get("object_type") == "DIRECTORY"
    ]
    if len(skills) != EXPECTED_SKILLS:
        problemas.append(f"skills: {len(skills)} pastas, esperado {EXPECTED_SKILLS}")

    x_dirs = {
        item["path"].rsplit("/", 1)[-1]
        for item in remote_list(f"{home}/.assistant")
        if item.get("object_type") == "DIRECTORY"
    }
    for faltante in sorted(EXPECTED_X_DIRS - x_dirs):
        problemas.append(f"diretório ausente: {faltante}")

    plataforma = sorted(set(remotos) & GERENCIADOS_PELA_PLATAFORMA)

    print(f"esperados : {len(esperados)} arquivos")
    print(f"remotos   : {len(remotos)} arquivos sob .assistant + instruções")
    print(f"ausentes  : {len(ausentes)} | obsoletos: {len(obsoletos)}")
    if plataforma:
        print(f"plataforma: {len(plataforma)} arquivo(s) gerenciado(s) — {', '.join(plataforma)}")
    print(f"skills    : {len(skills)}/{EXPECTED_SKILLS}")
    print(f"extensões : {len(x_dirs & EXPECTED_X_DIRS)}/{len(EXPECTED_X_DIRS)} diretórios x_")
    print()
    for problema in problemas:
        print(f"FAIL {problema}")
    print(f"\n{'APROVADO' if not problemas else 'REPROVADO'}: {len(problemas)} problema(s)")
    return 0 if not problemas else 1


PROFUNDIDADE_RAPIDA = 3  # .assistant → seção → pasta do objeto


def remote_dirs(path: str, profundidade: int) -> set[str]:
    """Lista só diretórios, até `profundidade` níveis. Uma chamada por diretório."""
    encontrados: set[str] = set()
    if profundidade <= 0:
        return encontrados
    for item in remote_list(path):
        if item.get("object_type") != "DIRECTORY":
            continue
        encontrados.add(item["path"])
        encontrados |= remote_dirs(item["path"], profundidade - 1)
    return encontrados


def cmd_verify_rapido(root: Path, arquivos: list[Path], home: str) -> int:
    """Compara a árvore de **diretórios**, não a de arquivos.

    A conferência completa faz um `workspace list` por diretório da árvore
    inteira. Com uma pasta por objeto isso passa de dezenas para mais de cem
    chamadas — e gate que demora é gate que se pula durante a execução.

    O que muda numa sprint de reestruturação é a árvore de pastas: pasta de
    objeto que não foi criada, seção que não subiu, pasta antiga que sobreviveu.
    Comparar só diretórios até a profundidade do objeto responde a isso com uma
    fração das chamadas.

    **Não substitui a completa.** Não vê tipo de objeto, arquivo faltando dentro
    de uma pasta que existe, nem obsoleto abaixo da profundidade varrida.
    """
    print(f"== VERIFY RÁPIDO (read-only, árvore de diretórios até {PROFUNDIDADE_RAPIDA} níveis) ==")

    esperados = set()
    for arquivo in arquivos:
        partes = arquivo.relative_to(root).parts[:-1]
        for i in range(1, min(len(partes), PROFUNDIDADE_RAPIDA) + 1):
            esperados.add("/".join(partes[:i]))

    remotos = {
        caminho[len(home) + 1:]
        for caminho in remote_dirs(f"{home}/.assistant", PROFUNDIDADE_RAPIDA - 1)
    }
    remotos.add(".assistant")

    ausentes = sorted(esperados - remotos)
    obsoletos = sorted(remotos - esperados)

    print(f"diretórios: {len(esperados)} esperados | {len(remotos)} remotos")
    for nome in ausentes:
        print(f"FAIL ausente no remoto: {nome}/")
    for nome in obsoletos:
        print(f"FAIL obsoleto no remoto: {nome}/")

    total = len(ausentes) + len(obsoletos)
    print(f"\n{'APROVADO' if not total else 'DIVERGENTE'}: {total} diferença(s)")
    print("Rode --verify (completo) antes de fechar a sprint.")
    return 0 if not total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="publica de fato")
    parser.add_argument("--verify", action="store_true", help="apenas confere o remoto")
    parser.add_argument(
        "--rapido", action="store_true",
        help="com --verify: só contagens, para uso durante a execução",
    )
    args = parser.parse_args()

    if args.execute and args.verify:
        print("FAIL use --execute ou --verify, não os dois")
        return 1
    if args.rapido and not args.verify:
        print("FAIL --rapido só faz sentido com --verify")
        return 1

    root, arquivos = local_tree()
    home, user = resolve_home()
    print(f"usuário: {user}\n")

    if args.verify:
        if args.rapido:
            return cmd_verify_rapido(root, arquivos, home)
        return cmd_verify(root, arquivos, home)
    return cmd_plan(root, arquivos, home, args.execute)


if __name__ == "__main__":
    sys.exit(main())
