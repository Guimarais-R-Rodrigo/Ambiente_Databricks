"""Inventário V00: leitura de checkout Git limpo, sem importar o produto.

Reutiliza repo_inventory.git_paths, api_publica e notebook_marker. A descoberta
é conservadora: evidência automática NÃO equivale a classificação humana nem a
homologação visual. A saída é exclusiva de .artifacts/, nunca do produto.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_publica import api_publica
from notebook_marker import eh_notebook
from repo_inventory import git_paths
from project_policy import SIMULATED_ROOT

TEXTOS = {'.py', '.md', '.css', '.html', '.js', '.mjs', '.json', '.yaml', '.yml',
          '.toml', '.ipynb', '.txt', '.sql', '.svg'}
IMAGENS = {'.png', '.svg', '.jpg', '.jpeg', '.webp', '.gif'}
PADROES = {
    'biblioteca_visual': re.compile(r'\b(?:plotly|matplotlib|seaborn|altair|bokeh|ipywidgets|streamlit)\b', re.I),
    'helper_visual': re.compile(r'\b(?:aplicar_tema|registrar_template_plotly|theme_plotly|section_header_html|kpi_card_html)\b'),
    'cor_hex': re.compile(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{1}|[0-9a-fA-F]{3}|[0-9a-fA-F]{5})?\b'),
    'cor_funcional': re.compile(r'\b(?:rgba?|hsla?)\([^\n)]{1,120}\)', re.I),
    'aparencia': re.compile(r'\b(?:font(?:[-_]\w+)?|color(?:way|scale)?|colour|palette|paleta|colorscale|background|padding|margin|border(?:[-_]\w+)?|height|width|template|theme|tema|displayHTML|set_table_styles|style\.use|rcParams)\b', re.I),
    'cor_nomeada': re.compile(r'[\'\"](?:white|black|red|green|blue|orange|gray|grey|transparent|yellow|purple|pink|brown|cyan|magenta)[\'\"]', re.I),
    'config_referenciada': re.compile(r'[\w./-]+\.(?:json|yaml|yml|toml)\b', re.I),
    'recurso': re.compile(r'[\w./-]+\.(?:png|svg|jpg|jpeg|webp|woff2?|ttf|otf)\b', re.I),
}
IMAGEM_MD = re.compile(r'!\[([^\]]*)\]\(([^\n)]+)\)|<img\b[^>]*?src=[\'\"]([^\'\"]+)[\'\"][^>]*>', re.I)
CENTRAIS = ('/constants/colors/', '/constants/styles/', '/visual_system/tokens.')
RAIZES_PROTEGIDAS = ('ambiente_databricks/', SIMULATED_ROOT.as_posix() + '/', 'Novo_Ambiente_Simulado/')


def git(root: Path, *args: str) -> str:
    try:
        p = subprocess.run(['git', *args], cwd=root, capture_output=True, check=False)
    except OSError as exc:
        raise ValueError('Git indisponível') from exc
    if p.returncode:
        raise ValueError('Git falhou: ' + ' '.join(args[:2]))
    return p.stdout.decode('utf-8', errors='strict').strip()


def camada(path: str) -> str:
    if path.startswith((SIMULATED_ROOT.as_posix() + '/', 'Novo_Ambiente_Simulado/')):
        return 'derivado'
    if path.startswith('ambiente_databricks/'):
        return 'produto'
    if path.startswith('tools/'):
        return 'ferramenta'
    return 'governanca'


def classe(path: str, asset: bool = False) -> str:
    if '/sprint_0/' in path or path.startswith('docs/historico/'):
        return 'historico_candidato'
    if '/tests/' in path or Path(path).name.startswith('exemplo_'):
        return 'exemplo_ou_teste'
    if any(item in path for item in CENTRAIS):
        return 'configuracao_central'
    if '/specs/approved_' in path:
        return 'registro_de_aprovacao'
    if asset:
        return 'ativo_a_conferir_no_registro'
    if Path(path).suffix in {'.md', '.txt'}:
        return 'orientacao_documental'
    return 'literal_ou_consumidor_candidato'


def _seguro(root: Path, path: Path) -> None:
    rel = path.relative_to(root)
    if 'Ambiente_Antigo' in rel.parts:
        raise ValueError('Quarentena encontrada no índice Git; conteúdo não lido')
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError('Link simbólico versionado não aceito: ' + rel.as_posix())
    if not path.is_file():
        raise ValueError('Arquivo versionado ausente: ' + rel.as_posix())


def contratos(path: Path, text: str) -> dict[str, Any]:
    tree = ast.parse(text, filename=path.name)
    notebook = eh_notebook(path)
    imports, chamadas, funcoes, constantes, reexports = [], [], [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imports.append({'linha': node.lineno, 'origem': '.' * node.level + (node.module or ''),
                            'nomes': [a.name for a in node.names]})
        elif isinstance(node, ast.Import):
            imports.append({'linha': node.lineno, 'origem': '', 'nomes': [a.name for a in node.names]})
        elif isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if re.search(r'plot|chart|heatmap|display|theme|tema|style|header|badge|kpi|render|widget', name, re.I):
                chamadas.append({'linha': node.lineno, 'funcao': name})
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_'):
            funcoes.append({'nome': node.name, 'assinatura': ast.unparse(node.args),
                            'retorno': ast.unparse(node.returns) if node.returns else None,
                            'linha': node.lineno})
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and (target.id.isupper() or target.id == '__all__') and node.value is not None:
                    item = {'nome': target.id, 'linha': node.lineno, 'expressao': ast.unparse(node.value)}
                    try:
                        value = ast.literal_eval(node.value)
                        item['tipo_literal'] = type(value).__name__
                    except (ValueError, TypeError, SyntaxError):
                        item['tipo_literal'] = 'expressao_nao_avaliada'
                    constantes.append(item)
        if path.name == '__init__.py' and isinstance(node, ast.ImportFrom):
            reexports.append(ast.unparse(node))
    return {'tipo_objeto': 'NOTEBOOK_SOURCE' if notebook else 'FILE',
            'api': [] if notebook else api_publica(path), 'funcoes': funcoes,
            'constantes': constantes, 'imports': imports, 'chamadas_visuais': chamadas,
            'reexports': reexports, 'efeitos_sessao_revisao': [
                {'linha': i, 'sinal': line.strip()[:180]}
                for i, line in enumerate(text.splitlines(), 1)
                if re.search(r'pio\.templates|rcParams|set_option|register_template|sys\.path|dbutils\.widgets', line)]}


def referencias_imagens(text: str) -> list[dict[str, Any]]:
    out, section = [], ''
    for lineno, line in enumerate(text.splitlines(), 1):
        if re.match(r'^#{1,6}\s', line):
            section = line.lstrip('# ').strip()
        for match in IMAGEM_MD.finditer(line):
            out.append({'ordem': len(out) + 1, 'linha': lineno, 'secao': section,
                        'alternativo': match.group(1) or '', 'destino': match.group(2) or match.group(3)})
    return out


def inventariar(root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    paths = git_paths(root)
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise ValueError('Worktree suja: inventário não atribuível ao commit')
    commit = git(root, 'rev-parse', 'HEAD')
    arquivos, ocorrencias, modulos, imagens_md = [], [], {}, {}
    for path in paths:
        _seguro(root, path)
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        suffix = path.suffix.lower()
        row: dict[str, Any] = {'path': rel, 'camada': camada(rel), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'classe_inicial': classe(rel, suffix in IMAGENS)}
        if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24:
            row['dimensoes_png'] = [int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')]
        if suffix in TEXTOS:
            try:
                text = data.decode('utf-8-sig')
            except UnicodeDecodeError as exc:
                raise ValueError('UTF-8 inválido: ' + rel) from exc
            hits = []
            for number, line in enumerate(text.splitlines(), 1):
                for kind, pattern in PADROES.items():
                    for match in pattern.finditer(line):
                        hits.append({'path': rel, 'linha': number, 'coluna': match.start() + 1,
                                     'tipo': kind, 'valor': match.group(0),
                                     'classe_inicial': row['classe_inicial'], 'revisado': False})
            ocorrencias.extend(hits)
            row['ocorrencias'] = len(hits)
            if suffix == '.py':
                modulos[rel] = contratos(path, text)
            if suffix == '.md':
                refs = referencias_imagens(text)
                if refs:
                    imagens_md[rel] = refs
        arquivos.append(row)
    fonte = [a for a in arquivos if a['camada'] == 'produto']
    if not fonte or not any(o['path'].startswith('ambiente_databricks/') for o in ocorrencias):
        raise ValueError('Varredura vazia no produto; inventário não certificado')
    if git(root, 'status', '--porcelain', '--untracked-files=normal') or git(root, 'rev-parse', 'HEAD') != commit:
        raise ValueError('Checkout mudou durante o inventário')
    locais = {}
    for rel in modulos:
        prefix = 'ambiente_databricks/.assistant/'
        if rel.startswith(prefix):
            nome = rel[len(prefix):-3].replace('/', '.')
            if nome.endswith('.__init__'):
                nome = nome[:-9]
            locais[nome] = rel
    arestas = []
    for rel, info in modulos.items():
        if not rel.startswith('ambiente_databricks/.assistant/'):
            continue
        for imp in info['imports']:
            candidates = [imp['origem']] if imp['origem'] else imp['nomes']
            if imp['origem'] and not imp['origem'].startswith('.'):
                candidates += [imp['origem'] + '.' + n for n in imp['nomes']]
            for nome in candidates:
                if nome in locais:
                    arestas.append({'consumidor': rel, 'provedor': locais[nome], 'linha': imp['linha'], 'import': nome})
    return {'schema_version': 1, 'commit': commit, 'tree': git(root, 'rev-parse', 'HEAD^{tree}'),
        'branch': git(root, 'symbolic-ref', '--short', '-q', 'HEAD') if git(root, 'branch', '--show-current') else 'detached',
        'estado': 'INVENTARIO_AUTOMATICO_REQUER_REVISAO',
        'resumo': {'arquivos': len(arquivos), 'camadas': dict(Counter(a['camada'] for a in arquivos)),
            'ocorrencias': len(ocorrencias), 'modulos_python': len(modulos),
            'arquivos_com_ocorrencias': sum(bool(a.get('ocorrencias')) for a in arquivos),
            'imagens': sum(Path(a['path']).suffix.lower() in IMAGENS for a in arquivos),
            'readmes_com_imagens': len(imagens_md)},
        'limites': ['Descoberta por padrões é conservadora; inclui falsos positivos.',
            'Imports e chamadas são estáticos; referências dinâmicas exigem revisão.',
            'Classes iniciais não são parecer humano sobre semântica ou aprovação de asset.',
            'IPYNB é pesquisado como texto; não executa células nem certifica outputs.',
            'Hashes não comprovam aparência no navegador; não há captura Databricks.'],
        'arquivos': arquivos, 'ocorrencias': ocorrencias, 'modulos': modulos, 'grafo_imports_absolutos_resolvidos': arestas, 'imagens_markdown': imagens_md}


def comparar_protegidos(base: dict[str, Any], atual: dict[str, Any]) -> list[str]:
    def subset(doc: dict[str, Any]) -> dict[str, str]:
        return {r['path']: r['sha256'] for r in doc['arquivos']
                if r['path'].startswith(RAIZES_PROTEGIDAS) or r['path'] == 'MANUAL_TECNICO_V2.md'}
    antes, depois = subset(base), subset(atual)
    if not antes or not depois:
        raise ValueError('Conjunto protegido vazio')
    return sorted(p for p in antes.keys() | depois.keys() if antes.get(p) != depois.get(p))


def gravar(root: Path, output: Path, doc: dict[str, Any]) -> None:
    root = root.resolve(strict=True)
    artifact = root / '.artifacts'
    if artifact.is_symlink():
        raise ValueError('Diretório de artefatos simbólico não aceito')
    target = output.absolute()
    if not target.resolve().is_relative_to(artifact):
        raise ValueError('Saída deve estar em .artifacts/ do checkout')
    cursor = target.parent
    while cursor != root:
        if cursor.is_symlink():
            raise ValueError('Saída simbólica não aceita')
        cursor = cursor.parent
    if target.exists() or target.is_symlink():
        raise ValueError('Saída já existe; use outro nome, sem sobrescrever evidência')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        doc = inventariar(args.root)
        gravar(args.root, args.output, doc)
    except (ValueError, OSError, SyntaxError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(doc['resumo'], ensure_ascii=False))
    print('Inventário técnico gerado; classificação independente permanece pendente.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
