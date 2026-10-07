"""Núcleo V02: configurações completas, offline, sem aplicar aparência.

O import usa somente a biblioteca padrão. A validação exige jsonschema e
referencing, importados na chamada. Não há instalação, cache global, Spark,
rede, publicação, autenticação ou alteração de bibliotecas gráficas.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

_MAX_BYTES = 131072
_MAX_DEPTH = 12
_MAX_NODES = 8192
_ENGINE = (1, 0, 0)
_SCHEMA_SHA = 'a0d6bd1780611acae671910d3a4dbc76aa91b678673eaca17fc6de868508955c'
_ASSETS_SHA = '8a57ddea7a2bc5407726d02d75786d4611e464c99f8ab3a6ecfe89c10bff4905'
_MAX_ASSET_BYTES = 16 * 1024 * 1024


class ThemeError(ValueError):
    """Erro seguro: código, campo conhecido e ação; não repete o valor recebido."""
    def __init__(self, code: str, message: str, *, field: str = '$',
                 action: str = 'Confira o contrato e o guia de erros antes de tentar novamente.'):
        self.code, self.field, self.action = code, field, action
        super().__init__(f'{code} [{field}]: {message} {action}')


def _fail(code: str, message: str, **kwargs: Any) -> None:
    raise ThemeError(code, message, **kwargs) from None


def _strict_json(raw: bytes) -> Any:
    if type(raw) is not bytes:
        _fail('JSON_INPUT_TYPE', 'Forneça bytes UTF-8, não código nem um caminho.')
    if len(raw) > _MAX_BYTES:
        _fail('JSON_SIZE', 'O limite é 131.072 bytes por configuração.')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        _fail('JSON_ENCODING', 'Use UTF-8 sem BOM.')
    if text.startswith('\ufeff'):
        _fail('JSON_ENCODING', 'Use UTF-8 sem BOM.')
    depth = 0
    quoted = escaped = False
    for ch in text:
        if quoted:
            if escaped: escaped = False
            elif ch == '\\': escaped = True
            elif ch == '"': quoted = False
        elif ch == '"': quoted = True
        elif ch in '[{':
            depth += 1
            if depth > _MAX_DEPTH:
                _fail('JSON_DEPTH', 'O limite é 12 níveis de objetos/listas.')
        elif ch in ']}': depth -= 1
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                _fail('JSON_DUPLICATE', 'Uma propriedade foi declarada mais de uma vez.')
            result[key] = value
        return result
    def constant(_):
        _fail('JSON_NONFINITE', 'NaN e infinito não são admitidos.')
    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, RecursionError) as exc:
        if isinstance(exc, ThemeError): raise
        _fail('JSON_SYNTAX', 'Revise aspas, pontuação e tamanho dos números.')
    return _copy_json(value)


def _copy_json(value: Any) -> Any:
    """Copia apenas tipos JSON exatos; limita ciclos, profundidade e volume."""
    active: set[int] = set()
    nodes = 0
    def visit(item, depth):
        nonlocal nodes
        nodes += 1
        if nodes > _MAX_NODES: _fail('JSON_NODES', 'A configuração tem elementos em excesso.')
        if type(item) in (dict, list):
            if id(item) in active: _fail('JSON_CYCLE', 'A configuração contém referência circular.')
            if depth >= _MAX_DEPTH: _fail('JSON_DEPTH', 'O limite é 12 níveis de objetos/listas.')
            active.add(id(item))
            if type(item) is dict:
                result = {}
                for key, val in item.items():
                    if type(key) is not str: _fail('JSON_VALUE_TYPE', 'As chaves precisam ser texto.')
                    visit(key, depth + 1)
                    result[key] = visit(val, depth + 1)
            else: result = [visit(val, depth + 1) for val in item]
            active.remove(id(item))
            return result
        if type(item) is str:
            if len(item) > _MAX_BYTES: _fail('JSON_SIZE', 'O texto excede o limite da configuração.')
            if any(0xD800 <= ord(ch) <= 0xDFFF for ch in item):
                _fail('JSON_UNICODE', 'Sequência Unicode isolada não é válida.')
            return item
        if type(item) is float:
            if not math.isfinite(item): _fail('JSON_NONFINITE', 'O número precisa ser finito.')
            return item
        if type(item) is int:
            if item.bit_length() > 4096: _fail('JSON_SIZE', 'Número inteiro excessivamente grande.')
            return item
        if item is None or type(item) is bool: return item
        _fail('JSON_VALUE_TYPE', 'Use somente objetos, listas, texto e valores JSON simples.')
    return visit(value, 0)


def _safe_file(root: Path, relative: str) -> Path:
    if type(relative) is not str or '\x00' in relative:
        _fail('PATH_SCOPE', 'Use um nome relativo normalizado.')
    p = PurePosixPath(relative)
    if (not relative or p.is_absolute() or any(x in ('', '.', '..') for x in relative.split('/'))
            or '\\' in relative or ':' in relative):
        _fail('PATH_SCOPE', 'A referência precisa ficar dentro da pasta explicitamente escolhida.')
    try:
        root = Path(root).absolute()
        current = root
        if root.is_symlink() or any(parent.is_symlink() for parent in root.parents):
            _fail('PATH_SYMLINK', 'Não são aceitos atalhos simbólicos na raiz.')
        for part in p.parts:
            current /= part
            if current.is_symlink(): _fail('PATH_SYMLINK', 'Não são aceitos atalhos simbólicos.')
        if not current.is_file(): _fail('PATH_MISSING', 'Arquivo regular não encontrado no escopo.')
        return current
    except (OSError, ValueError, TypeError) as exc:
        if isinstance(exc, ThemeError): raise
        _fail('PATH_SCOPE', 'Raiz ou referência inválida.')


def _read_bytes(path: Path, limit: int = _MAX_BYTES) -> bytes:
    """Leitura limitada, sem seguir symlink e com conferência antes/depois.

    A raiz deve ter permissões controladas. Não é sandbox contra um processo
    hostil que substitui diretórios pais durante a leitura.
    """
    fd = None
    try:
        path = Path(path)
        if path.is_symlink() or any(p.is_symlink() for p in path.parents):
            _fail('PATH_SYMLINK', 'Arquivo ou pasta simbólica não é aceito.')
        before = path.stat()
        if not stat.S_ISREG(before.st_mode): _fail('PATH_REGULAR', 'Escolha um arquivo regular.')
        if before.st_size > limit: _fail('JSON_SIZE', 'O arquivo excede o limite permitido.')
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
        fd = os.open(path, flags)
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode): _fail('PATH_REGULAR', 'Escolha um arquivo regular.')
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            _fail('PATH_CHANGED', 'O arquivo foi substituído durante a leitura.')
        with os.fdopen(fd, 'rb') as stream:
            fd = None
            raw = stream.read(limit + 1)
            after = os.fstat(stream.fileno())
        if len(raw) > limit: _fail('JSON_SIZE', 'O arquivo excede o limite permitido.')
        if (opened.st_size, opened.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            _fail('PATH_CHANGED', 'O arquivo mudou durante a leitura.')
        return raw
    except (OSError, ValueError, TypeError) as exc:
        if isinstance(exc, ThemeError): raise
        raise ThemeError('PATH_READ', 'Não foi possível ler o arquivo regular.',
                         action='Confira existência, permissão de leitura e pasta escolhida.') from None
    finally:
        if fd is not None: os.close(fd)


def _read_json(path: Path) -> Any:
    return _strict_json(_read_bytes(path))


def _schema_validator(schema: dict[str, Any]):
    if type(schema) is not dict: _fail('SCHEMA_INVALID', 'O schema precisa ser um objeto.')
    if schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
        _fail('SCHEMA_DIALECT', 'O contrato exige o dialeto 2020-12.')
    # Falha fechada antes de chamar bibliotecas. O runtime só lê o schema fixado.
    schema = _copy_json(schema)
    def inspect(item, trail):
        if isinstance(item, dict):
            if '$id' in item and trail: _fail('SCHEMA_NESTED_ID', 'Subschema não redefine a base.')
            if '$dynamicRef' in item: _fail('SCHEMA_DYNAMIC_REF', 'Referências dinâmicas não são aceitas.')
            if '$ref' in item:
                ref = item['$ref']
                if type(ref) is not str or not ref.startswith('#/'):
                    _fail('SCHEMA_REMOTE_REF', 'Somente referências internas são aceitas.')
                if ref in trail: _fail('SCHEMA_CYCLE', 'Referência circular de schema não é aceita.')
                target = schema
                try:
                    for part in ref[2:].split('/'):
                        key = part.replace('~1', '/').replace('~0', '~')
                        target = target[int(key)] if isinstance(target, list) else target[key]
                except (KeyError, IndexError, ValueError, TypeError):
                    _fail('SCHEMA_LOCAL_REF', 'A referência interna não existe.')
                inspect(target, trail + (ref,))
            for key, sub in item.items():
                if key != '$ref': inspect(sub, trail or ('root-child',))
        elif isinstance(item, list):
            for sub in item: inspect(sub, trail)
    inspect(schema, ())
    try:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
        from referencing import Registry
    except ImportError:
        raise ThemeError('DEPENDENCY_MISSING', 'A biblioteca de validação não está disponível.',
                         action='Peça ao mantenedor o ambiente de requirements-temas.txt; não há instalação automática.') from None
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        _fail('SCHEMA_INVALID', 'O próprio schema não atende ao contrato.')
    return Draft202012Validator(schema, registry=Registry())


def _validate_theme(theme: Any, schema: dict[str, Any]) -> None:
    validator = _schema_validator(schema)
    error = next(validator.iter_errors(theme), None)
    if error:
        # Não repetir message, instance ou chaves arbitrárias da entrada.
        field_name = '$'
        known = set(schema['properties']) | set(schema['$defs']['notebookTokens']['properties']) | set(schema['$defs']['editorialTokens']['properties'])
        safe_parts = [str(p) for p in error.absolute_path if isinstance(p, int) or p in known]
        if safe_parts: field_name += '.' + '.'.join(safe_parts)
        if error.validator == 'required' and isinstance(error.instance, dict):
            missing = [p for p in error.validator_value if p not in error.instance and p in known]
            if missing: field_name += '.' + missing[0]
        hint = {'required': 'Preencha todos os campos; não há preenchimento automático.',
                'additionalProperties': 'Remova campos fora do contrato; papéis e aprovação não pertencem ao tema.',
                'pattern': 'Use o formato indicado na referência; cores exigem #RRGGBB em maiúsculas.',
                'minimum': 'Use um valor dentro dos limites da referência.',
                'maximum': 'Use um valor dentro dos limites da referência.',
                'type': 'Use o tipo JSON declarado na referência.'}.get(error.validator, 'Confira as opções e limites na referência do contrato.')
        _fail(f'SCHEMA_{str(error.validator).upper()}', 'O valor não atende ao contrato.',
              field=field_name, action=hint)
    compat = theme['engine_compatibility']
    minimum = tuple(int(v) for v in compat['minimum_version'].split('.'))
    if (minimum > _ENGINE or minimum[0] != compat['api_major']
            or not compat['api_major'] <= _ENGINE[0] < compat['maximum_major_exclusive']):
        _fail('ENGINE_VERSION', 'Exigência incompatível com a API 1.0.0.',
              field='$.engine_compatibility', action='Use uma versão compatível; não force fallback.')
    if theme['context'] == 'notebook' and len(theme['tokens']['palette.diverging']) % 2 == 0:
        _fail('PALETTE_CENTER', 'A paleta divergente exige quantidade ímpar de cores.',
              field='$.tokens.palette.diverging')


def _package_root() -> Path:
    return Path(__file__).absolute().parents[3]


def _resource(relative: str, expected: str) -> bytes:
    raw = _read_bytes(_safe_file(_package_root(), 'hub_padroes/identidade_visual/' + relative))
    if hashlib.sha256(raw).hexdigest() != expected:
        _fail('RESOURCE_HASH', 'O recurso do pacote difere da versão declarada.',
              action='Restaure o pacote compatível; não altere o hash para esconder a divergência.')
    return raw


def _asset_manifest(theme: dict) -> str:
    raw = _resource('assets.json', _ASSETS_SHA)
    entries = _strict_json(raw)['sets'].get(theme['asset_set_id'])
    if entries is None: _fail('ASSET_UNKNOWN', 'Conjunto de recursos não encontrado.')
    for entry in entries:
        path = _safe_file(_package_root(), entry['path'])
        actual = hashlib.sha256(_read_bytes(path, _MAX_ASSET_BYTES)).hexdigest()
        if actual != entry['sha256']:
            _fail('ASSET_HASH', 'Um recurso gráfico difere do manifesto.', action='Restaure o recurso aprovado com o mantenedor.')
    return hashlib.sha256(raw).hexdigest()


def _canonical(value: Any) -> bytes:
    def normalize(item):
        if type(item) is dict: return {k: normalize(v) for k, v in item.items()}
        if type(item) is list: return [normalize(v) for v in item]
        if type(item) is float and item.is_integer(): return int(item)
        return item
    return (json.dumps(normalize(value), sort_keys=True, ensure_ascii=False,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def _freeze(value: Any) -> Any:
    if type(value) is dict: return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if type(value) is list: return tuple(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class ResolvedTheme:
    """Retrato isolado de uma configuração válida; nunca uma autorização."""
    _canonical: bytes = field(repr=False)
    _values: Mapping[str, Any] = field(repr=False)
    raw_sha256: str
    content_sha256: str
    schema_sha256: str
    asset_manifest_sha256: str
    fingerprint: str
    source: str
    origins: Mapping[str, str] = field(repr=False)
    warnings: tuple[str, ...] = ('CONTRATO_VALIDADO_NAO_APROVADO', 'APLICACAO_VISUAL_NAO_EXECUTADA')

    @property
    def context(self) -> str:
        return self._values['context']

    @property
    def tokens(self) -> Mapping[str, Any]:
        return self._values['tokens']

    def to_dict(self) -> dict[str, Any]:
        """Retorna uma cópia editável; alterar a cópia não altera este resultado."""
        return json.loads(self._canonical)


def normalize_color(value: str) -> str:
    """Ajuda de autoria explícita: #RRGGBB, seis dígitos, sem espaço/alpha.

    A importação não chama esta função para corrigir silenciosamente propostas.
    """
    if type(value) is not str or re.fullmatch(r'#[0-9a-fA-F]{6}', value) is None:
        _fail('COLOR_FORMAT', 'Informe # seguido de seis dígitos hexadecimais.')
    return value.upper()


def resolve_theme(value: bytes | dict[str, Any], *, expected_context: str | None = None) -> ResolvedTheme:
    """Valida dados não confiáveis completos e devolve retrato imutável.

    Não herda perfis, não preenche defaults, não lê aprovação do JSON e não
    aplica estilos. O schema e o manifesto vêm do pacote, nunca da proposta.
    """
    if expected_context is not None and (type(expected_context) is not str or expected_context not in ('notebook', 'readme', 'presentation')):
        _fail('CONTEXT_EXPECTED', 'O contexto esperado deve ser notebook, readme ou presentation.')
    if type(value) is bytes:
        raw = value
        data = _strict_json(raw)
    elif type(value) is dict:
        data = _copy_json(value)
        raw = _canonical(data)
        if len(raw) > _MAX_BYTES: _fail('JSON_SIZE', 'O limite é 131.072 bytes por configuração.')
    else:
        _fail('JSON_INPUT_TYPE', 'Forneça bytes UTF-8 ou um dicionário JSON completo.')
    schema_raw = _resource('theme.schema.json', _SCHEMA_SHA)
    schema = _strict_json(schema_raw)
    _validate_theme(data, schema)
    if expected_context is not None and data['context'] != expected_context:
        _fail('CONTEXT_MISMATCH', 'O tema pertence a outro contexto.', field='$.context',
              action='Escolha uma configuração completa do contexto solicitado.')
    asset_sha = _asset_manifest(data)
    canonical = _canonical(data)
    if len(canonical) > _MAX_BYTES: _fail('JSON_SIZE', 'A representação canônica excede o limite.')
    content_sha = hashlib.sha256(canonical).hexdigest()
    identity = {'serialization': 'hub-json-v1', 'api_version': '1.0.0',
                'content_sha256': content_sha, 'schema_sha256': _SCHEMA_SHA,
                'asset_manifest_sha256': asset_sha}
    fingerprint = hashlib.sha256(_canonical(identity)).hexdigest()
    normalized = json.loads(canonical)
    return ResolvedTheme(canonical, _freeze(normalized), hashlib.sha256(raw).hexdigest(),
                         content_sha, _SCHEMA_SHA, asset_sha, fingerprint, 'memory',
                         MappingProxyType({key: 'document' for key in normalized['tokens']}))


def load_theme(root: str | Path, relative_path: str, *, expected_sha256: str | None = None,
               expected_context: str | None = None) -> ResolvedTheme:
    """Lê JSON dentro de raiz explícita. expected_sha256 compara bytes, não autoriza."""
    if expected_sha256 is not None and (type(expected_sha256) is not str or re.fullmatch(r'[0-9a-f]{64}', expected_sha256) is None):
        _fail('HASH_FORMAT', 'O hash esperado precisa conter 64 dígitos hexadecimais minúsculos.')
    path = _safe_file(root, relative_path)
    if path.suffix != '.json': _fail('PATH_EXTENSION', 'Escolha um arquivo com extensão .json.')
    raw = _read_bytes(path)
    if expected_sha256 is not None and hashlib.sha256(raw).hexdigest() != expected_sha256:
        _fail('HASH_MISMATCH', 'Os bytes diferem da revisão solicitada.', action='Confirme a revisão; não substitua por latest nem pelo legado.')
    result = resolve_theme(raw, expected_context=expected_context)
    from dataclasses import replace
    return replace(result, source=relative_path,
                   origins=MappingProxyType({key: relative_path for key in result.tokens}))


def load_reference_theme(context: str = 'notebook') -> ResolvedTheme:
    """Carrega somente referência sintética empacotada; não é tema aprovado."""
    names = {'notebook': 'legado_notebook.json', 'readme': 'legado_editorial.json',
             'presentation': 'apresentacao_exemplo.json'}
    if type(context) is not str or context not in names:
        _fail('CONTEXT_EXPECTED', 'Escolha notebook, readme ou presentation.')
    return load_theme(_package_root(), 'hub_padroes/identidade_visual/exemplos/' + names[context], expected_context=context)


def export_theme(theme: ResolvedTheme) -> bytes:
    """Devolve JSON canônico em memória; não cria arquivo nem inclui aprovação."""
    if type(theme) is not ResolvedTheme: _fail('RESULT_TYPE', 'Forneça um resultado de resolve_theme ou load_theme.')
    # Revalidar protege contra construção manual e pacote alterado após resolução.
    verified = resolve_theme(theme._canonical)
    if verified.fingerprint != theme.fingerprint or verified.content_sha256 != theme.content_sha256:
        _fail('RESULT_INTEGRITY', 'O resultado e seus identificadores não correspondem.')
    return verified._canonical
