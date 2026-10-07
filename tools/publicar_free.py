"""Publica o ecossistema no Databricks Free e confere o resultado.

Três fases, no padrão do engine `databricks-genie` do Verg_Alchemy_Hub:

    python tools/publicar_free.py             # plano (dry-run), nada é escrito
    python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>
    python tools/publicar_free.py --verify    # confere o remoto (read-only)

O ADR-0005 registra por que a publicação é feita aqui em vez de pelo engine do
Hub: aquele engine importa `.py` como notebook, o que quebraria os imports de
`hub_snippets`, e injeta cabeçalho, o que invalidaria o frontmatter das skills.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# `import-dir` precisa preservar módulos `.py` como FILE, mas versões atuais da
# CLI também podem reconhecer notebooks SOURCE e materializá-los diretamente sem
# a extensão. O fallback individual abaixo só é usado quando o objeto remoto não
# tiver sido materializado como NOTEBOOK. A detecção local continua canônica em
# notebook_marker.py; ver o docstring de lá.
from notebook_marker import eh_notebook  # noqa: E402
from project_policy import (  # noqa: E402
    CORPORATE_RE,
    SIMULATED_ROOT,
    simulated_root,
    EXPECTED_HUB_DIRS,
    EXPECTED_SKILL_NAMES,
    normalize_host,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SIMULADO = simulated_root(REPO_ROOT)
FONTE = REPO_ROOT / "ambiente_databricks"
CLI_PROFILE: str | None = None

# O render copia exatamente estes dois itens da fonte. Mantê-los aqui permite
# conferir espelho contra fonte sem reimplementar a lógica do renderer.
ITENS_PUBLICAVEIS = (".assistant_instructions.md", ".assistant")
PADROES_IGNORADOS = ("__pycache__", ".pytest_cache", ".ruff_cache", ".DS_Store")
SUFIXOS_IGNORADOS = (".pyc", ".pyo")

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
    profile_args = ["--profile", CLI_PROFILE] if CLI_PROFILE else []
    proc = subprocess.run(
        ["databricks", *profile_args, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
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


def _configuration_value(payload: object, key: str) -> str | None:
    if not isinstance(payload, dict):
        return None
    details = payload.get("details")
    configuration = details.get("configuration") if isinstance(details, dict) else None
    item = configuration.get(key) if isinstance(configuration, dict) else None
    value = item.get("value") if isinstance(item, dict) else None
    return str(value) if value is not None else None


def resolve_home(
    *, expected_host: str | None = None, require_explicit_target: bool = False
) -> tuple[str, str, str, str]:
    """Resolve usuário, host e perfil e aplica o guardrail de destino de escrita."""
    identidade = databricks_json("current-user", "me", "-o", "json")
    if not isinstance(identidade, dict) or "userName" not in identidade:
        raise SystemExit("FAIL não foi possível resolver o usuário pela CLI.")
    user = str(identidade["userName"])
    if CORPORATE_RE.search(user):
        raise SystemExit(
            "FAIL usuário com aparência corporativa. Esta ferramenta publica no\n"
            "     laboratório Free; o workspace do trabalho usa o runbook manual\n"
            "     (docs/playbooks/replicacao-trabalho.md)."
        )
    auth = databricks_json("auth", "describe", "-o", "json")
    actual_host = _configuration_value(auth, "host")
    actual_profile = _configuration_value(auth, "profile") or CLI_PROFILE
    if not actual_host or not actual_profile:
        raise SystemExit("FAIL a CLI não informou host e profile ativos em `auth describe`.")
    try:
        actual_host = normalize_host(actual_host)
        normalized_expected = normalize_host(expected_host) if expected_host else None
    except ValueError as exc:
        raise SystemExit(f"FAIL host inválido: {exc}") from exc

    if require_explicit_target and (not CLI_PROFILE or not normalized_expected):
        raise SystemExit(
            "FAIL --execute exige --profile e --expected-host (ou as variáveis\n"
            "     DATABRICKS_FREE_PROFILE e DATABRICKS_FREE_HOST). O gate impede\n"
            "     escrita quando o destino não foi declarado explicitamente."
        )
    if normalized_expected and actual_host != normalized_expected:
        raise SystemExit(
            "FAIL host ativo diverge do laboratório Free declarado:\n"
            f"     ativo   : {actual_host}\n"
            f"     esperado: {normalized_expected}"
        )
    return f"/Users/{user}", user, actual_host, actual_profile


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


def _notebook_ja_materializado(destino: str) -> bool:
    """Confirma se `import-dir` já criou o notebook remoto corretamente."""
    status = databricks_json("workspace", "get-status", destino, "-o", "json")
    return isinstance(status, dict) and status.get("object_type") == "NOTEBOOK"


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

    divergencias = conferir_fonte_espelho(root)
    if divergencias:
        print(f"\n== ESPELHO x FONTE ==\n{len(divergencias)} divergência(s):")
        for problema in divergencias[:20]:
            print(f"  FAIL {problema}")
        if len(divergencias) > 20:
            print(f"  ... e mais {len(divergencias) - 20}")
        print("\nRode: python tools/render_simulado.py --write")
        return 1
    print("espelho: em dia com a fonte")

    if not executar:
        print("\nDRY-RUN: nada foi publicado. Use --execute para publicar.")
        return 0

    rc, out, err = databricks("workspace", "import-dir", str(root), home, "--overwrite")
    if rc != 0:
        print(f"\nFAIL publicação falhou:\n{out}{err}")
        return 1

    # Versões atuais da CLI podem materializar notebooks SOURCE diretamente no
    # import-dir. Evitamos uma segunda escrita redundante quando o tipo remoto já
    # está correto, preservando o reenvio individual apenas como fallback.
    cadernos = [a for a in arquivos if eh_notebook(a)]
    materializados = 0
    reenviados = 0
    for caderno in cadernos:
        relativo = str(caderno.relative_to(root)).replace("\\", "/")
        destino = f"{home}/{relativo[:-3]}"  # o workspace guarda notebook sem .py
        if _notebook_ja_materializado(destino):
            materializados += 1
            continue
        rc, _out, err = databricks(
            "workspace", "import", destino, "--file", str(caderno),
            "--format", "SOURCE", "--language", "PYTHON", "--overwrite",
        )
        if rc != 0:
            print(f"FAIL notebook {relativo}: {err.strip()[:160]}")
            return 1
        reenviados += 1
    if materializados:
        print(f"  {materializados} notebook(s) já materializado(s) pelo import-dir")
    if reenviados:
        print(f"  {reenviados} notebook(s) reenviado(s) como fallback SOURCE")

    print(f"\nPublicado. Confira com: python {Path(__file__).name} --verify")
    return 0


def _e_ignorado(caminho: Path) -> bool:
    """Artefato de execução local, que o render não copia e o remoto não tem."""
    if caminho.suffix in SUFIXOS_IGNORADOS:
        return True
    return any(parte in PADROES_IGNORADOS for parte in caminho.parts)


def _normalizar_para_comparacao(dados: bytes, *, notebook: bool) -> bytes:
    """Representação canônica mínima para comparar local com remoto.

    A normalização é deliberadamente pequena. Remover comentário, espaço ou
    linha em branco mascararia diferença real de conteúdo — que é justamente o
    que esta comparação existe para encontrar. Só duas transformações:

    1. fim de linha: o workspace devolve LF; a origem pode estar em CRLF
       conforme a máquina e o `.gitattributes`;
    2. fim de arquivo, apenas em notebook: a plataforma normaliza a quebra final
       ao materializar as células.
    """
    texto = dados.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if notebook:
        texto = texto.rstrip(b"\n") + b"\n"
    return texto


def _sha(dados: bytes) -> str:
    return hashlib.sha256(dados).hexdigest()


def _commit_atual() -> str:
    """Identifica a origem do pacote, sem sujeira alheia ao escopo publicado.

    Evidência de publicação descreve o produto e seu espelho. Alteração em docs,
    artefato ignorado ou metadado de fim de linha fora desses caminhos não torna
    o pacote ``dirty``. A fonte é rastreada; a saída ignorada é validada por
    paridade exata antes de qualquer CLI remota, nunca certificada por Git.
    """
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                              capture_output=True, text=True)
        status = subprocess.run(
            [
                "git", "status", "--porcelain", "--",
                str(FONTE.relative_to(REPO_ROOT)),
                str(SIMULADO.relative_to(REPO_ROOT) / "Users" / "usuario-free"),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ValueError("Git indisponível para certificar origem") from exc
    if proc.returncode or status.returncode or not proc.stdout.strip():
        raise ValueError("Git falhou ao certificar commit/estado da árvore")
    return proc.stdout.strip() + ("-dirty" if status.stdout.strip() else "")


def conferir_fonte_espelho(root: Path) -> list[str]:
    """Recusa espelho desatualizado ANTES de qualquer escrita no workspace.

    Publicar de um espelho velho grava conteúdo que não corresponde a nenhum
    commit, e o `--verify` seguinte aprova, porque ele compara o remoto com o
    mesmo espelho velho.
    """
    problemas: list[str] = []
    esperados: set[Path] = set()
    for item in ITENS_PUBLICAVEIS:
        origem = FONTE / item
        if origem.is_file():
            esperados.add(Path(item))
        elif origem.is_dir():
            esperados.update(
                p.relative_to(FONTE)
                for p in origem.rglob("*")
                if p.is_file() and not _e_ignorado(p)
            )
        else:
            problemas.append(f"fonte ausente: {origem}")

    # Ignorar cache na fonte não autoriza enviar cache presente no espelho.
    # import-dir recebe o diretório inteiro: qualquer extra ignorado deve barrar
    # a escrita, mesmo que não participe da comparação de conteúdo.
    for extra in root.rglob("*"):
        if extra.is_file() and _e_ignorado(extra):
            problemas.append(f"arquivo não publicável no espelho: {extra.relative_to(root)}")
        if extra.is_symlink():
            problemas.append(f"link simbólico não publicável: {extra.relative_to(root)}")
    no_espelho = {
        p.relative_to(root) for p in root.rglob("*") if p.is_file() and not _e_ignorado(p)
    }
    for faltando in sorted(esperados - no_espelho):
        problemas.append(f"espelho desatualizado — ausente no espelho: {faltando}")
    for sobrando in sorted(no_espelho - esperados):
        problemas.append(f"espelho desatualizado — não existe na fonte: {sobrando}")
    for comum in sorted(esperados & no_espelho):
        local = _normalizar_para_comparacao((FONTE / comum).read_bytes(), notebook=False)
        espelho = _normalizar_para_comparacao((root / comum).read_bytes(), notebook=False)
        if local != espelho:
            problemas.append(f"espelho desatualizado — conteúdo difere: {comum}")
    return problemas


def _exportar_remoto(caminho_remoto: str, notebook: bool) -> tuple[bytes | None, str]:
    """Exporta um objeto do workspace. Erro nunca vira conteúdo válido."""
    formato = "SOURCE" if notebook else "AUTO"
    rc, out, err = databricks(
        "workspace", "export", caminho_remoto, "--format", formato, "-o", "json"
    )
    if rc != 0:
        return None, (err.strip() or out.strip() or "erro sem mensagem")[:160]
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        return None, "resposta não-JSON da CLI"
    conteudo = payload.get("content") if isinstance(payload, dict) else None
    if not isinstance(conteudo, str):
        return None, "resposta sem campo 'content'"
    try:
        return base64.b64decode(conteudo, validate=True), ""
    except Exception:
        return None, "campo 'content' não é base64 válido"


def comparar_conteudo(root: Path, arquivos: list[Path], home: str) -> tuple[list[str], int]:
    """Compara byte a byte, na representação canônica, o local com o remoto."""
    problemas: list[str] = []
    conferidos = 0
    for arquivo in arquivos:
        relativo = str(arquivo.relative_to(root)).replace("\\", "/")
        notebook = eh_notebook(arquivo)
        remoto_path = f"{home}/{relativo[:-3]}" if notebook else f"{home}/{relativo}"
        dados, erro = _exportar_remoto(remoto_path, notebook)
        if dados is None:
            problemas.append(f"leitura remota incompleta: {relativo} — {erro}")
            continue
        local = _normalizar_para_comparacao(arquivo.read_bytes(), notebook=notebook)
        remoto = _normalizar_para_comparacao(dados, notebook=notebook)
        conferidos += 1
        if _sha(local) != _sha(remoto):
            problemas.append(
                f"conteúdo divergente: {relativo} "
                f"(local {_sha(local)[:12]} != remoto {_sha(remoto)[:12]})"
            )
    return problemas, conferidos


def _hashes_do_pacote(root: Path, arquivos: list[Path]) -> tuple[str, str]:
    """Hash bruto e hash da representação normalizada, registrados separados.

    O bruto identifica os bytes que saem daqui. O normalizado é o único que pode
    ser comparado com o remoto, porque a plataforma transforma o fim de arquivo
    do notebook. Confundir os dois faz um pacote correto parecer divergente.
    """
    bruto = hashlib.sha256()
    normalizado = hashlib.sha256()
    for arquivo in sorted(arquivos):
        relativo = str(arquivo.relative_to(root)).replace("\\", "/").encode("utf-8")
        dados = arquivo.read_bytes()
        bruto.update(relativo + b"\0" + _sha(dados).encode("ascii") + b"\n")
        canonico = _normalizar_para_comparacao(dados, notebook=eh_notebook(arquivo))
        normalizado.update(relativo + b"\0" + _sha(canonico).encode("ascii") + b"\n")
    return bruto.hexdigest(), normalizado.hexdigest()


def _ancestrais(caminho: str) -> set[str]:
    """Todos os diretórios intermediários de um caminho relativo."""
    partes = caminho.split("/")
    return {"/".join(partes[:i]) for i in range(1, len(partes))}


def cmd_verify(root: Path, arquivos: list[Path], home: str, conteudo: bool = False, relatorio: Path | None = None) -> int:
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

    skills = {
        str(item["path"]).rsplit("/", 1)[-1]
        for item in remote_list(f"{home}/.assistant/skills")
        if item.get("object_type") == "DIRECTORY" and item.get("path")
    }
    for nome in sorted(EXPECTED_SKILL_NAMES - skills):
        problemas.append(f"skill ausente: {nome}")
    for nome in sorted(skills - EXPECTED_SKILL_NAMES):
        problemas.append(f"skill inesperada: {nome}")

    hub_dirs = {
        item["path"].rsplit("/", 1)[-1]
        for item in remote_list(f"{home}/.assistant")
        if item.get("object_type") == "DIRECTORY"
    }
    for faltante in sorted(EXPECTED_HUB_DIRS - hub_dirs):
        problemas.append(f"diretório ausente: {faltante}")

    plataforma = sorted(set(remotos) & GERENCIADOS_PELA_PLATAFORMA)

    conferidos = 0
    if conteudo:
        # Espelho velho invalida a comparação: o remoto seria conferido contra a
        # mesma referência errada que o gerou.
        for divergencia in conferir_fonte_espelho(root):
            problemas.append(divergencia)
        problemas_conteudo, conferidos = comparar_conteudo(root, arquivos, home)
        problemas.extend(problemas_conteudo)

    bruto, normalizado = _hashes_do_pacote(root, arquivos)

    try:
        commit = _commit_atual()
    except ValueError as exc:
        commit = "não certificado"
        if conteudo:
            problemas.append(str(exc))
    print(f"commit    : {commit}")
    print(f"esperados : {len(esperados)} arquivos")
    print(f"remotos   : {len(remotos)} arquivos sob .assistant + instruções")
    print(f"ausentes  : {len(ausentes)} | obsoletos: {len(obsoletos)}")
    if plataforma:
        print(f"plataforma: {len(plataforma)} arquivo(s) gerenciado(s) — {', '.join(plataforma)}")
    print(f"skills    : {len(skills)}/{len(EXPECTED_SKILL_NAMES)}")
    print(f"extensões : {len(hub_dirs & EXPECTED_HUB_DIRS)}/{len(EXPECTED_HUB_DIRS)} diretórios hub_")
    print(f"hash bruto: {bruto} | hash normalizado: {normalizado}")
    if conteudo:
        print(f"conteúdo  : {conferidos}/{len(arquivos)} arquivo(s) exportado(s) e comparado(s)")
        print("alcance   : inventário, tipos E conteúdo")
    else:
        print("alcance   : inventário e tipos — NÃO prova igualdade de conteúdo; "
              "use --verify --conteudo")
    print()
    for problema in problemas:
        print(f"FAIL {problema}")
    print(f"\n{'APROVADO' if not problemas else 'REPROVADO'}: {len(problemas)} problema(s)")
    if relatorio is not None:
        from datetime import datetime, timezone
        evidencia = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_commit": commit,
            "scope": "inventory-types-content" if conteudo else "inventory-types",
            "status": "PASS" if not problemas else "FAIL",
            "files_compared": conferidos,
            "package_raw_sha256": bruto,
            "package_normalized_sha256": normalizado,
            "normalization": "CRLF/CR to LF; notebook terminal LF only",
            "errors": problemas,
            "files": [{
                "path": a.relative_to(root).as_posix(),
                "raw_sha256": _sha(a.read_bytes()),
                "normalized_sha256": _sha(_normalizar_para_comparacao(a.read_bytes(), notebook=eh_notebook(a))),
                "type": "NOTEBOOK" if eh_notebook(a) else "FILE",
            } for a in arquivos],
        }
        relatorio.parent.mkdir(parents=True, exist_ok=True)
        relatorio.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
    global SIMULADO
    global CLI_PROFILE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="publica de fato")
    parser.add_argument("--verify", action="store_true", help="apenas confere o remoto")
    parser.add_argument(
        "--conteudo",
        action="store_true",
        help="no --verify, exporta cada objeto remoto e compara o conteúdo com a fonte",
    )
    parser.add_argument(
        "--rapido", action="store_true",
        help="com --verify: só contagens, para uso durante a execução",
    )
    parser.add_argument(
        "--profile",
        default=os.getenv("DATABRICKS_FREE_PROFILE"),
        help="profile explícito da CLI do laboratório Free",
    )
    parser.add_argument(
        "--expected-host",
        default=os.getenv("DATABRICKS_FREE_HOST"),
        help="origem HTTPS exata do laboratório Free; obrigatória com --execute",
    )
    parser.add_argument("--relatorio", type=Path, help="com --verify: salva evidência JSON local")
    parser.add_argument("--output-root", type=Path, default=SIMULATED_ROOT)
    args = parser.parse_args()
    try:
        SIMULADO = simulated_root(REPO_ROOT, args.output_root)
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 1
    CLI_PROFILE = args.profile

    if args.relatorio and not args.verify:
        print("FAIL --relatorio exige --verify")
        return 1
    if args.relatorio and args.rapido:
        print("FAIL --relatorio não aceita --rapido")
        return 1
    if args.execute and args.verify:
        print("FAIL use --execute ou --verify, não os dois")
        return 1
    if args.rapido and not args.verify:
        print("FAIL --rapido só faz sentido com --verify")
        return 1
    if args.conteudo and not args.verify:
        print("FAIL --conteudo só faz sentido com --verify")
        return 1
    if args.conteudo and args.rapido:
        print("FAIL --conteudo e --rapido se excluem: um confere bytes, o outro pula")
        return 1

    root, arquivos = local_tree()
    from simulado import parity_errors
    errors = parity_errors(REPO_ROOT, args.output_root, root.name)
    if errors:
        print("FAIL fonte/espelho: " + "; ".join(errors))
        return 1
    home, user, host, profile = resolve_home(
        expected_host=args.expected_host,
        require_explicit_target=args.execute,
    )
    print(f"usuário: {user}")
    print(f"profile: {profile}")
    print(f"host   : {host}\n")

    if args.verify:
        if args.rapido:
            return cmd_verify_rapido(root, arquivos, home)
        return cmd_verify(root, arquivos, home, conteudo=args.conteudo, relatorio=args.relatorio)
    return cmd_plan(root, arquivos, home, args.execute)


if __name__ == "__main__":
    sys.exit(main())