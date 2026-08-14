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

SIMULADO = Path("Novo_Ambiente_Simulado")
CORPORATE_RE = re.compile(r"c\d{6}|corp\.|\.gov\.br", re.IGNORECASE)

# Estrutura mínima que o Genie Code precisa encontrar para descobrir o ecossistema.
EXPECTED_SKILLS = 12
EXPECTED_X_DIRS = {"x_config", "x_docs", "x_projects", "x_prompts", "x_scripts", "x_snippets"}


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
    print(f"\nPublicado. Confira com: python {Path(__file__).name} --verify")
    return 0


def cmd_verify(root: Path, arquivos: list[Path], home: str) -> int:
    print("== VERIFY (read-only) ==")
    problemas: list[str] = []

    esperados = {str(a.relative_to(root)).replace("\\", "/") for a in arquivos}
    remotos = {
        item["path"][len(home) + 1 :]: item
        for item in remote_walk(f"{home}/.assistant")
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
    obsoletos = sorted(set(remotos) - esperados)
    for nome in obsoletos:
        problemas.append(f"obsoleto no remoto (remover à mão): {nome}")

    # `.py` precisa ser FILE: como NOTEBOOK, `from x_snippets...` deixa de funcionar.
    for nome, item in sorted(remotos.items()):
        if nome.endswith(".py") and item.get("object_type") != "FILE":
            problemas.append(f"{nome}: importado como {item.get('object_type')}, esperado FILE")

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

    print(f"esperados : {len(esperados)} arquivos")
    print(f"remotos   : {len(remotos)} arquivos sob .assistant + instruções")
    print(f"ausentes  : {len(ausentes)} | obsoletos: {len(obsoletos)}")
    print(f"skills    : {len(skills)}/{EXPECTED_SKILLS}")
    print(f"extensões : {len(x_dirs & EXPECTED_X_DIRS)}/{len(EXPECTED_X_DIRS)} diretórios x_")
    print()
    for problema in problemas:
        print(f"FAIL {problema}")
    print(f"\n{'APROVADO' if not problemas else 'REPROVADO'}: {len(problemas)} problema(s)")
    return 0 if not problemas else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="publica de fato")
    parser.add_argument("--verify", action="store_true", help="apenas confere o remoto")
    args = parser.parse_args()

    if args.execute and args.verify:
        print("FAIL use --execute ou --verify, não os dois")
        return 1

    root, arquivos = local_tree()
    home, user = resolve_home()
    print(f"usuário: {user}\n")

    if args.verify:
        return cmd_verify(root, arquivos, home)
    return cmd_plan(root, arquivos, home, args.execute)


if __name__ == "__main__":
    sys.exit(main())
