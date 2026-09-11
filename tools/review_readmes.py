"""Confere rascunhos em sua localização real e no destino virtual de publicação.

Uso (sem rede, credencial ou escrita por padrão):
    python tools/review_readmes.py
    python tools/review_readmes.py --export .artifacts/readme-review/candidato

Exportação exige diretório novo dentro de .artifacts/readme-review. Copia apenas
arquivos Git versionados, aplica READMEs no snapshot e recalcula links. Nunca
substitui ambiente_fonte/, README.md ou Novo_Ambiente_Simulado/ no checkout.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from markdown_contract import anchors, markdown_links, mask_code, python_blocks

ROOT = Path(__file__).resolve().parents[1]
STAGING = Path('Template_READMEs/sprints_preenchidos')
ASSETS = Path('ambiente_fonte/.assistant/hub_readmes_visual_assets')


def confined(root: Path, value: str) -> Path:
    rel = PurePosixPath(value)
    if rel.is_absolute() or '..' in rel.parts or '\\' in value or not value:
        raise ValueError(f'Caminho não permitido: {value!r}')
    result = root.joinpath(*rel.parts)
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Caminho fora do repositório: {value!r}')
    return result


def load_mapping(root: Path = ROOT) -> list[dict[str, str]]:
    payload = json.loads((root / STAGING / 'mapping.json').read_text(encoding='utf-8'))
    if payload.get('version') != 1:
        raise ValueError('Versão de mapping não suportada')
    docs = payload['documents']
    if len(docs) != 10 or len({d['draft'] for d in docs}) != 10 or len({d['target'] for d in docs}) != 10:
        raise ValueError('O mapping deve conter dez pares únicos')
    for d in docs:
        draft = confined(root, d['draft'])
        target = confined(root, d['target'])
        if not draft.is_relative_to(root / STAGING) or draft.name != 'README.md':
            raise ValueError('Rascunho fora do staging de READMEs')
        if target.name != 'README.md' or not (target == root / 'README.md' or target.is_relative_to(root / 'ambiente_fonte')):
            raise ValueError('Destino fora do conjunto de READMEs do produto')
        if not draft.is_file() or not target.is_file():
            raise ValueError(f'Par ausente: {d}')
    return docs


def translated(text: str, source: Path, destination: Path, replacements: dict[Path, Path], root: Path) -> str:
    """Rebaseia links reais; preserva exemplos de Markdown dentro de código."""
    edits = []
    for m in markdown_links(text):
        u = urlsplit(m[1])
        if u.scheme or u.netloc or not u.path:
            continue
        old = (source.parent / unquote(u.path)).resolve()
        if not old.is_relative_to(root.resolve()):
            raise ValueError(f'Link escaparia do repositório: {m[1]}')
        new = replacements.get(old, old)
        rel = Path(os.path.relpath(new, destination.parent)).as_posix()
        value = rel + ('?' + u.query if u.query else '') + ('#' + u.fragment if u.fragment else '')
        edits.append((m.start(1), m.end(1), value))
    for a, b, value in reversed(edits):
        text = text[:a] + value + text[b:]
    return text


def canonical_text(root: Path, doc: dict[str, str], docs: list[dict[str, str]]) -> str:
    replacements = {(root / d['draft']).resolve(): (root / d['target']).resolve() for d in docs}
    text = (root / doc['draft']).read_text(encoding='utf-8')
    text = translated(text, root / doc['draft'], root / doc['target'], replacements, root)
    # Estado editorial reside no staging; só a cópia exportada remove o banner.
    return re.sub(r'(?m)^> \*\*Rascunho de sprint[^\n]*(?:\n>[^\n]*)*\n?', '', text)


def check_links(text: str, source: Path, root: Path, virtual: dict[Path, str]) -> tuple[list[str], int, list[Path]]:
    errors, count, images = [], 0, []
    for m in markdown_links(text):
        u = urlsplit(m[1])
        if u.scheme or u.netloc:
            continue
        count += 1
        target = (source.parent / unquote(u.path)).resolve() if u.path else source.resolve()
        if not target.is_relative_to(root.resolve()):
            errors.append(f'{source.relative_to(root)}: link sai do repositório: {m[1]}')
            continue
        if target not in virtual and not target.exists():
            errors.append(f'{source.relative_to(root)}: link ausente: {m[1]}')
            continue
        if u.fragment and target.suffix.lower() == '.md':
            body = virtual[target] if target in virtual else target.read_text(encoding='utf-8')
            if unquote(u.fragment) not in anchors(body):
                errors.append(f'{source.relative_to(root)}: âncora ausente: {m[1]}')
        if m[0].startswith('!'):
            if not re.match(r'!\[[^\]]+\]', m[0]):
                errors.append(f'{source.relative_to(root)}: imagem sem equivalente alt')
            images.append(target)
    return errors, count, images


def image_layout(text: str, source: Path) -> list[tuple[Path | str, str]]:
    """Localiza cada imagem real e seu título imediatamente anterior.

    Exclui exemplos de código e comentários HTML. Caminhos absolutos resolvidos
    permitem comparar o staging com o README de referência, sem comparar os
    diferentes prefixos relativos. A sequência também faz parte do contrato.
    """
    visible = mask_code(text)
    headings = list(re.finditer(r'^#{1,6}\s+(.+?)\s*$', visible, re.M))
    result = []
    for match in markdown_links(text):
        if not match[0].startswith('!'):
            continue
        url = urlsplit(match[1])
        if url.scheme or url.netloc:
            asset = match[1]
        else:
            asset = (source.parent / unquote(url.path)).resolve()
        preceding = [h for h in headings if h.start() < match.start()]
        heading = preceding[-1][1] if preceding else 'TOPO'
        result.append((asset, heading))
    return result


def check_image_layout(text: str, source: Path, reference_text: str,
                       reference: Path) -> list[str]:
    """Cobra as mesmas imagens, ordem e seções dos READMEs atuais do projeto."""
    actual = image_layout(text, source)
    expected = image_layout(reference_text, reference)
    if actual == expected:
        return []
    missing = [str(asset) + ' em ' + heading
               for asset, heading in expected if (asset, heading) not in actual]
    extra = [str(asset) + ' em ' + heading
             for asset, heading in actual if (asset, heading) not in expected]
    return [f'{source}: disposição de imagens diverge do README de referência; '
            f'ausentes/fora da seção: {missing}; extras/fora da seção: {extra}; '
            'a ordem e a multiplicidade também devem ser preservadas']


def png_contract(path: Path) -> tuple[int, int, str]:
    data = path.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n' or len(data) < 24 or data[12:16] != b'IHDR':
        raise ValueError(f'PNG inválido: {path.name}')
    width, height = struct.unpack('>II', data[16:24])
    return width, height, hashlib.sha256(data).hexdigest()


def approved_images(root: Path) -> dict[Path, tuple[int, int, str]]:
    folder = root / ASSETS
    manifest = (folder / 'manifest.yaml').read_text(encoding='utf-8')
    values = {}
    for block in manifest.split('\n  - id: ')[1:]:
        fields = dict(re.findall(r'^    (published|sha256|width|height):\s*(.+)$', block, re.M))
        if {'published', 'sha256', 'width', 'height'} <= fields.keys():
            values[(folder / fields['published']).resolve()] = (int(fields['width']), int(fields['height']), fields['sha256'])
    headers = json.loads((folder / 'headers/manifest.json').read_text(encoding='utf-8'))
    for h in headers['headers']:
        values[(folder / 'headers' / h['path']).resolve()] = (h['width'], h['height'], h['sha256'])
    return values


def import_contracts(text: str, root: Path) -> tuple[list[str], int]:
    """Verifica sintaxe e argumentos de chamadas diretas importadas do Hub por AST.

    Não certifica tipos de DataFrame, métodos, **kwargs dinâmico ou execução.
    """
    errors, count = [], 0
    for line, code in python_blocks(text):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            errors.append(f'Python linha {line}: {e.msg}')
            continue
        bindings = {}
        for n in ast.walk(tree):
            if not isinstance(n, ast.ImportFrom) or not n.module or not n.module.startswith(('hub_snippets.', 'hub_scripts.', 'hub_padroes.')):
                continue
            directory = root / 'ambiente_fonte/.assistant' / n.module.replace('.', '/')
            module = directory / (directory.name + '.py')
            if not module.exists():
                # Categorias reexportam subpacotes, por exemplo constants.colors.
                if not directory.is_dir():
                    errors.append(f'Import sem módulo: {n.module}')
                continue
            target = ast.parse(module.read_text(encoding='utf-8'))
            defs = {d.name: d for d in target.body if isinstance(d, (ast.FunctionDef, ast.ClassDef))}
            for alias in n.names:
                node = defs.get(alias.name)
                if isinstance(node, ast.ClassDef):
                    node = next((a for a in node.body if isinstance(a, ast.FunctionDef) and a.name == '__init__'), None)
                if isinstance(node, ast.FunctionDef):
                    bindings[alias.asname or alias.name] = node.args
        for c in ast.walk(tree):
            if not isinstance(c, ast.Call) or not isinstance(c.func, ast.Name) or c.func.id not in bindings:
                continue
            args = bindings[c.func.id]
            pos = [a.arg for a in (*args.posonlyargs, *args.args)]
            if pos and pos[0] in {'self', 'cls'}:
                pos = pos[1:]
            if any(isinstance(a, ast.Starred) for a in c.args) or any(k.arg is None for k in c.keywords):
                continue
            count += 1
            passed = {k.arg for k in c.keywords}
            accepted = set(pos) | {a.arg for a in args.kwonlyargs}
            if not args.kwarg and passed - accepted:
                errors.append(f'{c.func.id}: parâmetros inexistentes {sorted(passed - accepted)}')
            if not args.vararg and len(c.args) > len(pos):
                errors.append(f'{c.func.id}: excesso de posicionais')
            required = set(pos[:len(pos) - len(args.defaults)])
            required |= {a.arg for a, default in zip(args.kwonlyargs, args.kw_defaults) if default is None}
            missing = required - (set(pos[:len(c.args)]) | passed)
            if missing:
                errors.append(f'{c.func.id}: argumentos ausentes {sorted(missing)}')
    return errors, count


def audit(root: Path = ROOT) -> dict:
    docs = load_mapping(root)
    virtual = {(root / d['target']).resolve(): canonical_text(root, d, docs) for d in docs}
    errors, references, calls = [], 0, 0
    images = set()
    for d in docs:
        original = (root / d['draft']).read_text(encoding='utf-8')
        errors.extend(check_image_layout(original, root / d['draft'],
                                         (root / d['target']).read_text(encoding='utf-8'),
                                         root / d['target']))
        for source, text, overlay in [(root / d['draft'], original, {}), (root / d['target'], virtual[(root / d['target']).resolve()], virtual)]:
            e, n, pngs = check_links(text, source, root, overlay)
            errors.extend(e); references += n; images.update(pngs)
        e, n = import_contracts(original, root)
        errors.extend(f'{d["draft"]}: {x}' for x in e); calls += n
    approved = approved_images(root)
    image_results = []
    for path in sorted(images):
        if path not in approved:
            errors.append(f'Imagem fora dos manifestos aprovados: {path.relative_to(root)}')
            continue
        try:
            actual = png_contract(path)
            if actual != approved[path]:
                errors.append(f'Hash/dimensões divergentes: {path.relative_to(root)}')
            image_results.append({'path': path.relative_to(root).as_posix(), 'width': actual[0], 'height': actual[1], 'sha256': actual[2]})
        except (OSError, ValueError) as e:
            errors.append(str(e))
    return {'documents': len(docs), 'local_and_virtual_links': references, 'direct_calls_checked': calls, 'unique_images': len(image_results), 'images': image_results, 'errors': errors, 'scope': 'static; not Databricks runtime or conversation certification'}


def export(root: Path, output: Path) -> None:
    allowed = (root / '.artifacts/readme-review').resolve()
    output = output.resolve()
    if output == allowed or not output.is_relative_to(allowed) or output.exists():
        raise ValueError('Use diretório NOVO abaixo de .artifacts/readme-review; nenhum destino existente é sobrescrito')
    result = audit(root)
    if result['errors']:
        raise ValueError('Exportação bloqueada por falhas da revisão')
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode('utf-8').split('\0')
    for rel in filter(None, paths):
        source = confined(root, rel)
        if '.artifacts' in Path(rel).parts or source.is_symlink():
            continue
        dest = confined(output, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    docs = load_mapping(root)
    for doc in docs:
        target = confined(output, doc['target'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(canonical_text(root, doc, docs), encoding='utf-8')
    (output / 'REVIEW_SNAPSHOT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', type=Path)
    parser.add_argument('--json', type=Path, help='Registro JSON opcional; deve ficar em .artifacts/')
    args = parser.parse_args()
    try:
        result = audit()
        if args.json:
            path = args.json.resolve()
            if not path.is_relative_to((ROOT / '.artifacts').resolve()):
                raise ValueError('Registro JSON deve ficar em .artifacts/')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        for e in result['errors']:
            print('FAIL', e)
        print(f"READMEs: {result['documents']}; links staging/destino: {result['local_and_virtual_links']}; chamadas AST: {result['direct_calls_checked']}; PNGs: {result['unique_images']}; falhas: {len(result['errors'])}")
        if result['errors']:
            return 1
        if args.export:
            export(ROOT, args.export)
            print('Snapshot de revisão exportado; fonte oficial e workspace não alterados.')
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as e:
        print('FAIL', e)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
