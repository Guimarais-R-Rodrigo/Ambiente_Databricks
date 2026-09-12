"""Conferência datada R02-I: compara bytes com árvores reais, sem importar helpers.

Execute no checkout da composição, com histórico completo:
    python docs/sprints/readmes_objetos/evidencias_integracao_r02/verificar_preservacao.py
Não é um gate universal: hashes fixos identificam as bases desta integração.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MAIN_TREE = '0062a9e82690b96a1cf0a650d4a3f362b78f6b38'
R02_TREE = '9daeb7c0de86a0c8655119b58d7e5e471b9c1f6c'
BASE = 'f748c144dbb6909c7437b53498b25dd4f4854ab7'
HUB = 'ambiente_fonte/.assistant/'


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def source(tree: str, path: str) -> bytes:
    return git('show', f'{tree}:{path}')


def paths(tree: str, prefix: str) -> list[str]:
    return [s.decode() for s in git('ls-tree', '-rz', '--name-only', tree, prefix).split(b'\0') if s]


def main() -> int:
    groups: dict[str, int] = {}
    failures: list[str] = []

    def exact(group: str, tree: str, selected: list[str]) -> None:
        if not selected:
            failures.append(group + ': conjunto vazio')
        groups[group] = len(selected)
        for path in selected:
            p = ROOT / path
            if not p.is_file() or p.read_bytes() != source(tree, path):
                failures.append(group + ': ' + path)

    exact('concierge_canonico', MAIN_TREE, paths(MAIN_TREE, HUB + 'skills/hub-ml-concierge'))
    exact('prototipo_experimental', MAIN_TREE, paths(MAIN_TREE, 'novas_funcionalidades/'))
    exact('adrs_aceitos', MAIN_TREE, [p for p in paths(MAIN_TREE, 'docs/decisions/') if Path(p).name.startswith('ADR-')])
    exact('templates_e_exemplares', R02_TREE, paths(R02_TREE, HUB + 'hub_padroes/'))
    exact('skill_criacao', R02_TREE, paths(R02_TREE, HUB + 'skills/hub-ml-criar-objeto/'))
    exact('especialistas_restantes', MAIN_TREE, [p for p in paths(MAIN_TREE, HUB + 'skills/')
          if '/hub-ml-' in p and '/hub-ml-criar-objeto/' not in p and '/hub-ml-concierge/' not in p])
    helper_paths = [p for prefix in ('hub_snippets/', 'hub_scripts/')
                    for p in paths(R02_TREE, HUB + prefix)
                    if p.endswith('.py') and not Path(p).name.startswith('exemplo_')]
    exact('helpers_fachadas_testes', R02_TREE, helper_paths)
    exact('notebooks_de_exemplo', R02_TREE, [p for p in paths(R02_TREE, 'ambiente_fonte/')
          if Path(p).name.startswith('exemplo_') and p.endswith('.py')])
    exact('imagens_e_assets', MAIN_TREE, paths(MAIN_TREE, HUB + 'hub_readmes_visual_assets/'))
    exact('readmes_pilotos', R02_TREE, [HUB + p + '/README.md' for p in (
        'hub_snippets/ml/train_xgboost', 'hub_snippets/ml/isolation_forest',
        'hub_snippets/spark/pit_join', 'hub_snippets/constants/format_br',
        'hub_scripts/quick_profile', 'hub_prompts/eda_rapida')])
    exact('controle_e_gates_herdados_readmes', R02_TREE, [
        'docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json',
        'tools/readme_objeto_contract.py', 'tools/tests/test_readme_objeto_contract.py',
        'tools/validate_assistant.py'])
    exact('politica_e_gates_herdados_concierge', MAIN_TREE, [
        'tools/project_policy.py', 'tools/tests/test_concierge_integracao.py',
        'tools/requirements-dev.txt'])
    exact('workflows_permanentes', R02_TREE, paths(R02_TREE, '.github/workflows/'))
    # Entire prompt files as authored in R02, stronger than checking only fenced blocks.
    exact('formularios_prompt', R02_TREE, [p for p in paths(R02_TREE, HUB + 'hub_prompts/')
          if p.endswith('.md') and Path(p).stem == Path(p).parent.name])

    # The shared history and both independent additions occur literally once.
    historical = source(BASE, 'CHANGELOG.md').decode()
    header, past = historical.split('## ', 1)
    past = '## ' + past
    current = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    if not current.endswith(past):
        failures.append('changelog: histórico compartilhado modificado')
    for label, tree in [('concierge', MAIN_TREE), ('readmes', R02_TREE)]:
        old = source(tree, 'CHANGELOG.md').decode()
        addition = old[len(header):-len(past)]
        if current.count(addition) != 1:
            failures.append('changelog: adição perdida/duplicada de ' + label)
    groups['historicos_changelog_preservados'] = 3

    old_adr = source(R02_TREE, 'docs/decisions/ADR-0011-readmes-de-objeto.md').decode()
    renamed = (ROOT / 'docs/decisions/ADR-0012-readmes-de-objeto.md').read_text(encoding='utf-8')
    if not renamed.startswith(old_adr.replace('# ADR-0011 — README', '# ADR-0012 — README', 1)):
        failures.append('ADR-0012: corpo original da proposta alterado')
    groups['corpo_adr_proposto_preservado'] = 1

    manual = (ROOT / HUB / 'MANUAL_TECNICO.md').read_bytes()
    for path in ('MANUAL_TECNICO.md', 'Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md'):
        if (ROOT / path).read_bytes() != manual:
            failures.append('manual divergente: ' + path)
    if b'28.5. Concierge:' not in manual or b'README local:' not in manual:
        failures.append('manual: uma das duas camadas perdeu sua seção')
    groups['copias_manual_identicas'] = 3

    for src in paths(R02_TREE, 'ambiente_fonte/.assistant') + paths(MAIN_TREE, HUB + 'skills/hub-ml-concierge'):
        p = ROOT / src
        relative = Path(src).relative_to('ambiente_fonte')
        dest = ROOT / 'Novo_Ambiente_Simulado/Users/usuario-free' / relative
        if p.is_file() and (not dest.is_file() or dest.read_bytes() != p.read_bytes()):
            failures.append('espelho divergente: ' + src)
    instructions = ROOT / 'ambiente_fonte/.assistant_instructions.md'
    if instructions.read_bytes() != (ROOT / 'Novo_Ambiente_Simulado/Users/usuario-free/.assistant_instructions.md').read_bytes():
        failures.append('espelho de instruções divergente')

    result = {'status': 'PASS' if not failures else 'FAIL', 'main_tree': MAIN_TREE,
              'r02_tree': R02_TREE, 'groups': groups, 'groups_may_overlap': True,
              'manual_sha256': hashlib.sha256(manual).hexdigest(), 'failures': failures,
              'databricks_executed': False, 'independent_audit': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
