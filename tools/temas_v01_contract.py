"""Verificação LOCAL do contrato candidato V01, sem resolver ou aplicar temas.

Reutiliza o núcleo V02 do produto para validar; não consulta serviços nem concede papéis.
Os modelos de workflow são oráculos sintéticos da especificação, não controles
operacionais de autenticação. Relatos V01 permanecem históricos; o schema ativo foi promovido na V02.

Uso: python -B tools/temas_v01_contract.py
     python -B tools/temas_v01_contract.py --print-dictionary
     python -B tools/temas_v01_contract.py --print-operational-dictionary
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
sys.path.insert(0, str(ROOT / 'ambiente_databricks/.assistant'))
from hub_snippets.visual.tema.tema import (
    ThemeError as ContractError, _fail, _strict_json as strict_json,
    _MAX_BYTES as MAX_BYTES, _MAX_DEPTH as MAX_DEPTH, _ENGINE as CANDIDATE_ENGINE,
    _read_json as read_json, _schema_validator as schema_validator,
    _validate_theme as validate_theme, _safe_file as safe_file,
)
SCHEMA_PATH = ROOT / 'ambiente_databricks/.assistant/hub_padroes/identidade_visual/theme.schema.json'


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
    asset_root = 'ambiente_databricks/.assistant/hub_readmes_visual_assets/'
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
    # V01 is a frozen historical projection. Its metadata uses the directory
    # name of that campaign; operational_dictionary emits the current namespace.
    return ('\n'.join(lines).rstrip()+'\n').replace('ambiente_databricks/', 'ambiente_fonte/')



# Projeção de uso independente do snapshot emitido por dictionary(). As listas
# descrevem leituras efetivas dos adaptadores, não x-hub.consumers planejados.
# test_temas_operational_tokens confronta estas listas com a AST dos consumidores.
_OPERATIONAL_READERS = {
    'constants/styles': (
        'styles.get_styles_resolvidos (CSS para componentes HTML)',
        ('font.family', 'surface.section', 'section.border_px', 'brand.primary',
         'section.padding_y_px', 'section.padding_x_px', 'section.radius_px',
         'section.title_px', 'text.secondary', 'section.description_px',
         'surface.card', 'card.padding_y_px', 'card.padding_x_px', 'card.radius_px',
         'card.font_px', 'text.primary', 'divider.light', 'divider.medium',
         'status.ok_bg', 'status.ok_text', 'badge.padding_y_px', 'badge.padding_x_px',
         'badge.radius_px', 'badge.font_px', 'status.warn_bg', 'status.warn_text',
         'status.fail_bg', 'status.fail_text', 'table.header_text', 'semantic.negative'),
    ),
    'visual/theme_plotly': (
        'theme_plotly (layout e rodapé nas APIs resolvidas)',
        ('font.family', 'chart.font_px', 'text.plot', 'chart.title_px',
         'brand.primary', 'palette.categorical', 'chart.height_px', 'chart.width_px',
         'chart.margin_left_px', 'chart.margin_right_px', 'chart.margin_top_px',
         'chart.margin_bottom_px', 'chart.footer_px', 'text.secondary'),
    ),
    'ml/curves_plotly': (
        'curves_plotly (com theme explícito)',
        ('palette.curves_legacy', 'text.plot', 'surface.card'),
    ),
    'ml/performance_monitor': (
        'PerformanceMonitor.plot_timeline_resolvido',
        ('brand.primary', 'text.secondary', 'semantic.warning', 'semantic.negative'),
    ),
    'ml/umap_viz': (
        'plot_umap_clusters_resolvido',
        ('palette.categorical', 'text.secondary', 'chart.footer_px'),
    ),
    'ml/vintage_analysis': (
        'vintage_analysis (curvas/heatmap resolvidos)',
        ('palette.categorical', 'palette.sequential', 'chart.height_px'),
    ),
    'display/correlation_matrix': (
        'plot_correlation_resolvido', ('palette.diverging',),
    ),
    'visual/theme_lab': (
        'theme_lab.build_preview (heatmap sintético)', ('palette.diverging',),
    ),
}
_OPERATIONAL_NO_NOTEBOOK_CONSUMER = frozenset({
    'brand.accent', 'semantic.positive', 'semantic.neutral',
})
_OPERATIONAL_NO_PREVIEW = frozenset({
    'brand.accent', 'semantic.positive', 'semantic.neutral', 'semantic.warning',
    'palette.curves_legacy', 'palette.sequential', 'divider.light', 'divider.medium',
    'status.ok_bg', 'status.ok_text', 'status.warn_bg', 'status.warn_text',
    'status.fail_bg', 'status.fail_text', 'badge.font_px', 'badge.radius_px',
    'badge.padding_y_px', 'badge.padding_x_px',
})
_OPERATIONAL_EDITORIAL_COLORS = frozenset({
    'editorial.' + key for key in (
        'background', 'background_elevated', 'panel', 'panel_high', 'line', 'text',
        'muted', 'quiet', 'hub_custom', 'gradient_end', 'atlas_core', 'dossier_back',
        'dossier_middle', 'dossier_fold', 'databricks_native', 'human_decision',
        'result_evidence', 'supporting_method', 'danger',
    )
})
_OPERATIONAL_EDITORIAL_INERT = frozenset({
    'typography.presentation_title_px', 'typography.readme_heading_px',
    'typography.module_title_px', 'typography.small_px',
    'geometry.connector_width', 'geometry.border_width',
    'geometry.safe_margin', 'geometry.glow_opacity',
})


def _operational_notebook_support(key: str) -> str:
    consumers = [f'[{label}](../../hub_snippets/{path}/README.md)'
                 for path, (label, keys) in _OPERATIONAL_READERS.items() if key in keys]
    if key in _OPERATIONAL_NO_NOTEBOOK_CONSUMER:
        support = 'Sem leitura visual direta nas APIs notebook atuais; valor validado e preservado, sem propagação automática.'
    elif consumers:
        support = '; '.join(consumers) + '.'
    else:
        raise ValueError('TOKEN_SUPPORT_MISSING: ' + key)
    if key == 'brand.accent':
        support += ' As curvas com tema usam a segunda cor de palette.curves_legacy, não brand.accent.'
    elif key == 'font.family':
        support += ' A tabela pandas mantém a família fixa Segoe UI; este token não altera table.font_family.'
    elif key == 'chart.footer_px':
        support += ' No adaptador geral, só há efeito quando a chamada cria uma nota/rodapé.'
    elif key == 'chart.height_px':
        support += ' O heatmap de safras usa o máximo entre este valor e 25 px por safra.'
    elif key == 'palette.categorical':
        support += ' Cores explícitas dos traces e a paleta própria das curvas podem prevalecer.'
    return support


def _operational_editorial_support(key: str) -> str:
    if key in {'canvas.width_px', 'canvas.height_px'}:
        return ('Metadado preservado no tema; não redimensiona figuras. O compositor de variantes '
                'usa as dimensões do preset de cada contrato visual.')
    if key == 'font.family':
        return ('O compositor de variantes aceita somente editorial_inter e recusa system_arial, '
                'embora ambos sejam válidos no schema. Não baixa fontes nem muda a fonte do Markdown.')
    if key in _OPERATIONAL_EDITORIAL_INERT:
        return ('Valor encaminhado à configuração do compositor de variantes, mas sem leitura '
                'nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam '
                'valores próprios das composições. Não há propagação visual garantida.')
    if key in {'editorial.atlas_core', 'editorial.dossier_fold'}:
        return ('Cor encaminhada ao compositor, usada na autoria de assinaturas. Na rota de '
                'variantes, essas assinaturas são congeladas e copiadas sem recoloração; '
                'alterar o token não modifica seus bytes.')
    if key == 'typography.body_px':
        return ('Default de tamanho dos helpers de texto/medição do compositor; chamadas com '
                'size explícito prevalecem. Não altera automaticamente todo texto das figuras.')
    if key == 'geometry.corner_radius':
        return ('Default de raio do helper de painéis do compositor; chamadas com radius '
                'explícito prevalecem. Não altera cantos de todos os elementos.')
    if key in _OPERATIONAL_EDITORIAL_COLORS:
        return ('Cor consumida pelo compositor nas figuras paramétricas que usam este papel. '
                'Assinaturas e assets congelados preservam os bytes; gerar uma variante '
                'não a aprova nem a publica.')
    raise ValueError('TOKEN_SUPPORT_MISSING: ' + key)


def operational_dictionary(schema: dict, *, root: Path = ROOT) -> str:
    """Emite somente a referência de uso; não modifica schema, temas ou snapshots."""
    mapping = read_json(root / 'ambiente_databricks/.assistant/hub_padroes/identidade_visual/aibi/aibi_mapping.json')
    aibi = {item['hub_token']: item for item in mapping['mappings']}
    notebook = schema['$defs']['notebookTokens']['properties']
    known = _OPERATIONAL_NO_NOTEBOOK_CONSUMER | {
        token for _label, keys in _OPERATIONAL_READERS.values() for token in keys
    }
    editorial = _OPERATIONAL_EDITORIAL_COLORS | _OPERATIONAL_EDITORIAL_INERT | {
        'font.family', 'typography.body_px', 'geometry.corner_radius',
        'canvas.width_px', 'canvas.height_px',
    }
    if (set(notebook) != known or set(aibi) != set(notebook)
            or len(mapping['mappings']) != len(aibi)
            or set(schema['$defs']['editorialTokens']['properties']) != editorial):
        raise ValueError('TOKEN_SUPPORT_COVERAGE: revisar cobertura de consumidores e AI/BI.')
    lines = [
        '# Referência de uso dos tokens', '',
        '> Referência gerada a partir do schema e da cobertura dos consumidores. Não editar separadamente.', '',
        'Consulte esta página para escolher um campo e verificar onde ele produz efeito. '
        'O [schema](theme.schema.json) define nomes, tipos, defaults declarativos e restrições; '
        'os adaptadores definem o suporte efetivo. Um campo válido não é um controle disponível em toda interface.', '',
        'Os defaults abaixo são referências, não valores injetados pelo validador. '
        'A configuração deve ser completa para seu contexto. Carregar/validar um tema não o aplica, '
        'não o aprova e não o publica. A edição de proposta indicada por papel é metadado de contrato, '
        'não autenticação nem concessão de permissão.', '',
        'Comece pelo [guia operacional](GUIA_OPERACIONAL.md). Passe um ResolvedTheme explicitamente '
        'às APIs resolvidas; as APIs legadas e constantes compartilhadas não são alteradas. '
        'O adaptador Plotly e a galeria completa aceitam notebook/light. '
        'SHAP/Matplotlib e Kaplan–Meier não recebem tema por essa rota.', '',
        'O campo de consumo identifica leituras diretas; componentes e wrappers podem herdar '
        'o layout/CSS desses adaptadores. O CSS de styles alimenta seção, cartões, badges, '
        'divisores, índice e tabela nas respectivas APIs resolvidas. Nem toda propriedade é usada '
        'por todo componente, e parâmetros explícitos de uma figura podem prevalecer.', '',
        'O [Visual Lab](../../hub_snippets/visual/theme_lab/README.md) e o '
        '[App de autoria](databricks_app/README.md) compartilham a disponibilidade de prévia '
        'indicada por token. O tipo de controle declarado no schema é uma intenção de edição; '
        'cada interface pode usar outro widget. Prévia sintética, validação e persistência '
        'não comprovam acessibilidade, ACL ou homologação do ambiente.', '',
        'Em AI/BI, a classificação vem da [matriz do Hub](aibi/aibi_mapping.json): '
        'translated indica correspondência conceitual, approximated exige decisão de mapeamento '
        'e unsupported não possui binding. Nenhuma classificação equivale a importação nativa pronta. '
        'É necessário export real, binding revisado e autorização específica para importar/publicar; '
        'consulte o [guia AI/BI](aibi/GUIA_PRIMEIRO_USO.md).', '',
        'Cores e status não criam regras analíticas. Conferir contraste de uma combinação '
        'não certifica toda a interface; o par de alerta de referência requer avaliação. '
        'A paleta divergente exige quantidade ímpar também na validação semântica do núcleo.', '',
    ]
    for group in ('notebookTokens', 'editorialTokens'):
        lines += ['## ' + ('Notebook' if group == 'notebookTokens' else 'README e apresentação'), '']
        if group == 'editorialTokens':
            lines += [
                'Estes campos pertencem aos contextos readme e presentation, não à galeria notebook '
                'nem ao App de autoria. A rota de variantes editoriais disponível seleciona readme; '
                'aceitar presentation no núcleo não garante um renderer de apresentações. '
                'O suporte abaixo descreve o compositor de variantes, que produz candidatos '
                'para revisão e preserva os assets congelados. O Markdown e as imagens já '
                'publicadas não são recoloridos ao carregar um tema. Consulte o '
                '[guia de recursos visuais](../../hub_readmes_visual_assets/README.md).', '',
            ]
        for key, spec in schema['$defs'][group]['properties'].items():
            meta = spec['x-hub']
            limits = {k: v for k, v in spec.items() if k not in {'type', 'description', 'default', 'x-hub'}}
            lines += [f'### `{key}`', '', spec['description'], '',
                      f"**Unidade:** {meta['unit']}. **Tipo:** {spec['type']}. **Default de referência:** `{json.dumps(spec['default'], ensure_ascii=False)}`.",
                      f"**Limites:** `{json.dumps(limits, ensure_ascii=False)}`. **Edição de proposta:** {', '.join(meta['editable_by'])}.",
                      f"**Controle declarado:** `{meta['control']}`. **Contextos:** {', '.join(meta['contexts'])}.",
                      f"**Efeito definido:** {meta['effect']}"]
            if group == 'notebookTokens':
                preview = ('Sem componente na galeria; controle desabilitado e valor preservado.'
                           if key in _OPERATIONAL_NO_PREVIEW else
                           'Controle habilitado na galeria sintética notebook/light; resultado depende do componente.')
                item = aibi[key]
                target = f" Destino conceitual: `{item['target_capability']}`." if item['target_capability'] else ''
                lines += ['**Consumo atual:** ' + _operational_notebook_support(key),
                          '**Visual Lab / App:** ' + preview,
                          f"**AI/BI (matriz do Hub):** `{item['classification']}`; binding `{item['binding_strategy']}`.{target} {item['note']}"]
            else:
                lines += ['**Consumo atual e limite:** ' + _operational_editorial_support(key),
                          '**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.']
            lines += ['']
    return '\n'.join(lines).rstrip() + '\n'


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
    schema = read_json(root/'ambiente_databricks/.assistant/hub_padroes/identidade_visual/theme.schema.json')
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
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--print-dictionary',action='store_true',help='Imprime referência histórica no stdout; não altera arquivos.')
    output.add_argument('--print-operational-dictionary', action='store_true',
                        help='Imprime referência de uso no stdout; não altera arquivos. Redirecionamento shell pode sobrescrever o destino.')
    args=parser.parse_args()
    try:
        if args.print_dictionary:
            print(dictionary(read_json(SCHEMA_PATH)),end='')
        elif args.print_operational_dictionary:
            print(operational_dictionary(read_json(SCHEMA_PATH)), end='')
        else:
            print(json.dumps(check_package(),ensure_ascii=False,indent=2))
        return 0
    except (ContractError,OSError,KeyError,ValueError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)},ensure_ascii=False))
        return 1

if __name__=='__main__':
    raise SystemExit(main())
