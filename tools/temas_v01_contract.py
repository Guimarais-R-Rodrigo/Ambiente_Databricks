"""Verificação LOCAL do contrato candidato V01, sem resolver ou aplicar temas.

Reutiliza o núcleo V02 do produto para validar; não consulta serviços nem concede papéis.
Os modelos de workflow são oráculos sintéticos da especificação, não controles
operacionais de autenticação. Relatos V01 permanecem históricos; o schema ativo foi promovido na V02.

Uso: python -B tools/temas_v01_contract.py
     python -B tools/temas_v01_contract.py --print-dictionary
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

from markdown_contract import anchors, markdown_links

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
    from referencing import Registry
except ImportError as exc:
    raise SystemExit('DEPENDENCIA_AUSENTE: instale tools/requirements-temas-dev.txt no ambiente de manutenção.') from exc

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / 'docs/sprints/sistema_temas/V01'


# API de manutenção preservada, com implementação única no núcleo V02.
sys.path.insert(0, str(ROOT / 'ambiente_fonte/.assistant'))
from hub_snippets.visual.tema.tema import (
    ThemeError as ContractError, _fail, _strict_json as strict_json,
    _MAX_BYTES as MAX_BYTES, _MAX_DEPTH as MAX_DEPTH, _ENGINE as CANDIDATE_ENGINE,
    _read_json as read_json, _schema_validator as schema_validator,
    _validate_theme as validate_theme, _safe_file as safe_file,
)
SCHEMA_PATH = ROOT / 'ambiente_fonte/.assistant/hub_padroes/identidade_visual/theme.schema.json'


def check_assets(theme: dict, registry: dict, root: Path = ROOT) -> int:
    """Verifica o baseline congelado. Não aprova nenhum ativo novo."""
    aset = theme['asset_set_id']
    if aset not in registry['sets']:
        _fail('ASSET_UNKNOWN', 'Conjunto de assets não registrado.')
    entries = registry['sets'][aset]
    seen = set()
    for entry in entries:
        if entry['path'] in seen:
            _fail('ASSET_DUPLICATE', 'Asset repetido no manifesto.')
        seen.add(entry['path'])
        path = safe_file(root, entry['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            _fail('ASSET_HASH', 'Os bytes do ativo diferem do baseline registrado.')
    if aset != 'sem-assets' and not entries:
        _fail('ASSET_EMPTY', 'Conjunto congelado não pode ficar vazio.')
    return len(entries)


def check_asset_registry(registry: dict, root: Path = ROOT) -> int:
    """Liga a amostra contratual aos registros de aprovação que já são canônicos.

    Hashes de bytes isolados não detectariam um item omitido do registro candidato
    nem um hash trocado junto com a imagem. O cadastro V01 deve refletir exatamente
    os dois manifestos existentes. Não aprova nem altera esses manifestos.
    """
    asset_root = 'ambiente_fonte/.assistant/hub_readmes_visual_assets/'
    headers = read_json(safe_file(root, asset_root + 'specs/approved_headers.json'))
    signatures = read_json(safe_file(root, asset_root + 'specs/approved_signatures.json'))
    expected: dict[str, str] = {}

    def register(path: str, digest: str) -> None:
        if path in expected or not re.fullmatch(r'[0-9a-f]{64}', digest):
            _fail('ASSET_REGISTRY', 'Registro oficial ambíguo ou hash inválido; revisar a origem.')
        expected[path] = digest

    for header in headers['headers']:
        register(asset_root + 'headers/png/' + header['id'] + '.png', header['sha256'])
    for asset in signatures['assets']:
        for variant in asset['variants']:
            for kind in ('svg', 'png'):
                register(asset_root + variant[kind], variant[kind + '_sha256'])
    if not expected:
        _fail('ASSET_REGISTRY', 'Não há referências oficiais para conferir o conjunto congelado.')
    sets = registry.get('sets', {})
    if set(sets) != {'sem-assets', 'editorial-v2-congelado'} or sets['sem-assets'] != []:
        _fail('ASSET_REGISTRY', 'Conjuntos divergentes da especificação candidata.')
    entries = sets['editorial-v2-congelado']
    declared = {entry['path']: entry['sha256'] for entry in entries}
    if len(entries) != len(declared) or declared != expected:
        _fail('ASSET_REGISTRY', 'Amostra de assets diverge dos manifestos oficiais; não aceitar automaticamente.')
    return len(expected)


GUARDED_ACTIONS = {
    'editar': ('rascunho', 'rascunho', {'proponente','mantenedor'}, {'owner','schema_valid'}),
    'submeter': ('rascunho', 'em_revisao', {'proponente','mantenedor'}, {'owner','schema_valid','revision_frozen'}),
    'rejeitar': ('em_revisao', 'rejeitado', {'aprovador'}, {'trusted_identity','revision_match','reason'}),
    'arquivar': ('rascunho', 'arquivado', {'proponente','mantenedor'}, {'owner'}),
    'aprovar': ('em_revisao', 'aprovado', {'aprovador'}, {'trusted_identity','not_author','revision_match','assets_verified','accessibility_review','independent_review','target_defined'}),
    'publicar': ('aprovado', 'publicado', {'publicador'}, {'trusted_identity','revision_match','approval_valid','target_permission','backup_verified','expected_previous_revision','dependency_manifest_match'}),
    'revogar': ('publicado', 'revogado', {'aprovador'}, {'trusted_identity','reason','target_defined'}),
}


def validate_policy(policy: dict) -> None:
    """Reprova enfraquecimento das guardas na especificação de governança."""
    if policy.get('default') != 'deny':
        _fail('POLICY_DEFAULT', 'O padrão precisa continuar sendo negar.')
    if policy.get('status') != 'ESPECIFICACAO_NAO_AUTORIZA_ACOES':
        _fail('POLICY_STATUS', 'A especificação não concede autorização operacional.')
    expected_components = {'theme_raw_sha256','schema_sha256','asset_manifest_sha256','renderer_version','requested_scope','target_id','expected_previous_revision'}
    if set(policy.get('trusted_revision_components', [])) != expected_components:
        _fail('POLICY_REVISION', 'A aprovação deve vincular conteúdo, dependências e destino.')
    if policy.get('permissions_source') != 'identidade_e_permissoes_validadas_no_processo_ou_servidor_nunca_no_json':
        _fail('POLICY_IDENTITY', 'Papéis não podem ser autodeclarados no tema.')
    expected_roles = {'leitor','proponente','aprovador','publicador','mantenedor'}
    expected_states = {'rascunho','em_revisao','aprovado','rejeitado','publicado','revogado','arquivado'}
    if set(policy.get('roles', [])) != expected_roles or set(policy.get('states', [])) != expected_states:
        _fail('POLICY_REFERENCE', 'O conjunto de papéis/estados foi alterado sem revisão.')
    if set(policy.get('scopes', [])) != {'pessoal','projeto','compartilhado'}:
        _fail('POLICY_SCOPE', 'O conjunto de escopos foi alterado sem revisão.')
    expected_read = {'ver_temas_aprovados': expected_roles, 'experimentar': expected_roles, 'exportar_proposta': {'proponente','mantenedor'}}
    reads = policy.get('read_actions', [])
    if len(reads) != len(expected_read) or {a.get('action') for a in reads} != set(expected_read):
        _fail('POLICY_READ', 'Ações de leitura/prévia/exportação divergentes.')
    if any(set(a.get('roles', [])) != expected_read[a['action']] for a in reads):
        _fail('POLICY_READ', 'Papéis de leitura/prévia/exportação divergentes.')
    if set(policy.get('new_revision_required_for', [])) != {'editar_em_revisao','editar_aprovado','editar_publicado','editar_rejeitado','editar_revogado'}:
        _fail('POLICY_IMMUTABLE', 'Revisões congeladas não podem ser editadas em lugar.')
    transitions = policy.get('transitions', [])
    actions = [t['action'] for t in transitions]
    if len(actions) != len(set(actions)):
        _fail('POLICY_DUPLICATE', 'Ação repetida torna a política ambígua.')
    if set(actions) != {'editar','submeter','aprovar','rejeitar','publicar','revogar','arquivar'}:
        _fail('POLICY_ACTIONS', 'Conjunto de ações divergente do contrato candidato.')
    for t in transitions:
        if t['from'] not in policy['states'] or t['to'] not in policy['states'] or not t['roles'] or not set(t['roles']) <= set(policy['roles']):
            _fail('POLICY_REFERENCE', 'Estado ou papel inexistente na transição.')
        if not t['scopes'] or not set(t['scopes']) <= set(policy['scopes']):
            _fail('POLICY_SCOPE', 'Escopo inválido na transição.')
        if t['action'] in GUARDED_ACTIONS:
            before, after, roles, guards = GUARDED_ACTIONS[t['action']]
            if t['from'] != before or t['to'] != after or set(t['roles']) != roles or set(t['guards']) != guards or set(t['scopes']) != ({'pessoal'} if t['action'] in {'editar','arquivar'} else {'projeto','compartilhado'}):
                _fail('POLICY_GUARD', 'Transição privilegiada foi enfraquecida ou alterada sem revisão.')


def model_transition(policy: dict, action: str, state: str, role: str, scope: str, guards: dict[str, bool]) -> str:
    """Oráculo de teste. Não autentica ninguém, não escreve e não publica."""
    validate_policy(policy)
    for transition in policy['transitions']:
        if transition['action'] == action and transition['from'] == state and role in transition['roles'] and scope in transition['scopes']:
            if all(guards.get(g) is True for g in transition['guards']):
                return transition['to']
    _fail('MODEL_DENY', 'A combinação não é autorizada pelo modelo de teste.')


def contrast(foreground: str, background: str) -> float:
    """Razão WCAG para cores sRGB opacas. Não certifica uma interface."""
    def luminance(color):
        linear = []
        for index in (1, 3, 5):
            x = int(color[index:index + 2], 16) / 255
            linear.append(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4)
        return sum(a*b for a,b in zip(linear,(.2126,.7152,.0722)))
    hi, lo = sorted((luminance(foreground),luminance(background)),reverse=True)
    return (hi + .05)/(lo + .05)


def dictionary(schema: dict) -> str:
    """Produz a referência derivada; o schema é o único dono dos campos."""
    lines = ['# Referência dos tokens — derivada do schema', '',
             '> GERADO por `tools/temas_v01_contract.py --print-dictionary`. Não editar esta tabela separadamente.',
             '', 'Os defaults são amostras declarativas, não valores injetados pelo validador. O produto legado permanece independente até os adaptadores serem integrados. Nenhum controle abaixo está instalado pela V01.', '']
    for group in ('notebookTokens','editorialTokens'):
        lines += ['## ' + ('Notebook' if group=='notebookTokens' else 'README e apresentação'), '']
        for key,spec in schema['$defs'][group]['properties'].items():
            meta=spec['x-hub']; limits={k:spec[k] for k in ('minimum','maximum','minItems','maxItems','enum','pattern') if k in spec}
            lines += [f'### `{key}`','',spec['description'],'',
              f"**Unidade:** {meta['unit']}. **Tipo:** {spec['type']}. **Default de referência:** `{json.dumps(spec['default'],ensure_ascii=False)}`.",
              f"**Limites:** `{json.dumps(limits,ensure_ascii=False)}`. **Edição de proposta:** {', '.join(meta['editable_by'])}.",
              f"**Controle projetado:** `{meta['control']}`. **Entrega:** `{meta['delivery']}`. **Contextos:** {', '.join(meta['contexts'])}.",
              '**Pontos de integração:** '+ '; '.join(f'`{p}`' for p in meta['consumers']) + '.',
              f"**Efeito previsto:** {meta['effect']}.",
              f"**Origem do default:** `{meta['default_origin']}`.", '']
    return '\n'.join(lines).rstrip()+'\n'



def check_links(package: Path = PACKAGE, root: Path = ROOT) -> int:
    """Reutiliza o parser do projeto e confere arquivo e âncora, não didática."""
    files = list(package.glob('*.md')) + [root/'docs/decisions/ADR-0013-sistema-de-temas.md']
    count = 0
    resolved_root = root.resolve()
    for path in files:
        text = path.read_text(encoding='utf-8')
        for link in markdown_links(text):
            target = urlsplit(link[1])
            if target.scheme in {'https', 'http', 'mailto'}:
                continue
            if target.scheme or target.netloc or target.query:
                _fail('DOC_LINK', 'Destino local inválido em ' + path.name)
            candidate = path.parent / unquote(target.path) if target.path else path
            destination = candidate.resolve()
            if not destination.is_relative_to(resolved_root) or not destination.is_file():
                _fail('DOC_LINK', 'Link local inexistente ou fora do checkout: ' + path.name)
            if target.fragment:
                if destination.suffix.lower() != '.md' or unquote(target.fragment) not in anchors(destination.read_text(encoding='utf-8')):
                    _fail('DOC_ANCHOR', 'Seção de destino não encontrada: ' + path.name)
            count += 1
    return count


def check_package(package: Path = PACKAGE, root: Path = ROOT) -> dict:
    schema = read_json(root/'ambiente_fonte/.assistant/hub_padroes/identidade_visual/theme.schema.json')
    schema_validator(schema)
    policy=read_json(package/'politica_workflow.json');validate_policy(policy)
    registry=read_json(package/'referencias_assets.json')
    official_assets = check_asset_registry(registry, root)
    counts={}
    for group in ('notebookTokens','editorialTokens'):
        specs=schema['$defs'][group]['properties'];counts[group]=len(specs)
        for key,spec in specs.items():
            meta=spec.get('x-hub',{})
            if not spec.get('description') or 'default' not in spec or not all(meta.get(k) for k in ('unit','consumers','default_origin','editable_by','effect','delivery','control','contexts')):
                _fail('TOKEN_DOCUMENTATION','Token sem contrato operacional completo.')
            for consumer in meta['consumers']: safe_file(root,consumer)
            if not Draft202012Validator(spec,registry=Registry()).is_valid(spec['default']):
                _fail('TOKEN_DEFAULT','Default declarado não atende ao próprio contrato.')
    fixtures=sorted((package/'fixtures').glob('*.json'))
    if {p.name for p in fixtures} != {'legado_notebook.json','executivo_claro_exemplo.json','legado_editorial.json','apresentacao_exemplo.json'}:
        _fail('FIXTURE_SET','Conjunto contratual vazio ou diferente do previsto.')
    names=set()
    for path in fixtures:
        theme=read_json(path);validate_theme(theme,schema);check_assets(theme,registry,root)
        if theme['theme_id'] in names:_fail('FIXTURE_DUPLICATE','Identidade de fixture duplicada.')
        names.add(theme['theme_id'])
    if (package/'TOKENS.md').read_text(encoding='utf-8') != dictionary(schema):
        _fail('TOKEN_DOC_DRIFT','A referência derivada difere do schema.')
    link_count = check_links(package,root)
    return {'status':'PASS_CONTRATO_LOCAL','local_document_links':link_count,'official_assets':official_assets,'tokens':counts,'fixtures':len(fixtures),'runtime':'NAO_IMPLEMENTADO_V01','autorizacao_real':'NAO_TESTADA','usabilidade_humana':'PENDENTE'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--print-dictionary',action='store_true',help='Imprime referência derivada no stdout; não altera arquivos.')
    args=parser.parse_args()
    try:
        if args.print_dictionary:
            print(dictionary(read_json(SCHEMA_PATH)),end='')
        else:
            print(json.dumps(check_package(),ensure_ascii=False,indent=2))
        return 0
    except (ContractError,OSError,KeyError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)},ensure_ascii=False))
        return 1

if __name__=='__main__':
    raise SystemExit(main())
