"""Reconciliação temporária, restrita à candidata V00 autorizada."""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path.cwd()
logs = Path(os.environ['RUNNER_TEMP']) / 'v00-integracao'
logs.mkdir(exist_ok=False)


def git(*args, check=True):
    p = subprocess.run(['git', *args], text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError(p.stderr + p.stdout)
    return p.stdout


def text(ref, path):
    return git('show', f'{ref}:{path}')


def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')


main, old, common = (os.environ[k] for k in ('BASE_MAIN', 'BASE_V00', 'BASE_COMUM'))
source = git('rev-parse', 'HEAD').strip()
transport = {'.github/workflows/temas-v00-integrar-temporario.yml', '.github/temas_v00_integrar.py'}
assert git('rev-parse', 'origin/main').strip() == main, 'main mudou; exige nova revisão'
assert git('merge-base', main, old).strip() == common
assert set(git('diff', '--name-only', old, 'HEAD').splitlines()) == transport, 'mudança concorrente na candidata'
assert not git('status', '--porcelain')
git('config', 'user.name', 'Codex')
git('config', 'user.email', 'codex@users.noreply.github.com')
proc = subprocess.run(['git', 'merge', '--no-commit', '--no-ff', main], text=True, capture_output=True)
(logs / 'merge.log').write_text(proc.stdout + proc.stderr, encoding='utf-8')
conflicts = set(git('diff', '--name-only', '--diff-filter=U').splitlines())
allowed = {'CHANGELOG.md', 'README.md', 'docs/README.md', 'tools/README.md'}
assert conflicts <= allowed, f'conflito fora do escopo: {conflicts - allowed}'
assert proc.returncode == 0 or conflicts, 'merge falhou sem conflito reconhecido'
for path in sorted(conflicts):
    if path == 'README.md':
        delta = git('diff', common, old, '--', path)
        changed = [s for s in delta.splitlines() if s[:1] in '+-' and not s.startswith(('+++', '---'))]
        assert changed and all('repo (identidade)' in s or 'repo (links)' in s for s in changed), 'README contém mudança não numérica'
        write(path, text(main, path))
    elif path == 'CHANGELOG.md':
        original = text(common, path)
        header, tail = original.split('\n## ', 1)
        tails = []
        for ref in (main, old):
            h, t = text(ref, path).split('\n## ', 1)
            assert h == header and t.endswith(tail), 'changelog não é apenas acréscimo; revisar'
            tails.append(t[:-len(tail)])
        write(path, header + '\n## ' + ''.join(tails) + tail)
    else:
        for ref in (main, old):
            stats = git('diff', '--numstat', common, ref, '--', path).strip().split('\t')
            assert not stats[0] or stats[1] == '0', f'{path}: houve remoção; revisar'
        with tempfile.TemporaryDirectory() as d:
            names = []
            for i, ref in enumerate((main, common, old)):
                p = Path(d) / str(i)
                p.write_text(text(ref, path), encoding='utf-8')
                names.append(str(p))
            merged = subprocess.run(['git', 'merge-file', '-p', '--union', *names], text=True, capture_output=True, check=True)
            write(path, merged.stdout)
assert '<<<<<<<' not in '\n'.join(Path(p).read_text(encoding='utf-8') for p in allowed)
for path in transport:
    Path(path).unlink()
entry = '''## 2026-09-12 — V00: reconciliação e aceite de integração Git (Codex)

### Atualizado

- (Codex) Reconciliação da candidata V00 com a main que incorpora READMEs e Concierge, preservando histórico, produto, espelho, Manual e as oito etapas do gate.
- (Codex) Autorização explícita de Rodrigo para aprovar e integrar registrada em `docs/sprints/sistema_temas/INTEGRACAO_V00.md`; limites e pendências não convertidos em homologação.
- (Codex) Contagens locais do README recalculadas pelo validador existente. Automação transitória de conciliação removida da árvore final, sem mudança das permissões do workflow permanente.

### Notas

- (Codex) Evidências anteriores permanecem vinculadas aos commits executados. A nova rodada identifica sua própria base e comandos. Sem publicação Databricks, alteração visual, force-push ou desativação de gates.
- (Codex) A primeira tentativa de automação transitória foi rejeitada por sintaxe YAML antes de executar comandos; a correção separa o script da configuração. O run reprovado permanece no histórico.

'''
changelog = Path('CHANGELOG.md').read_text(encoding='utf-8')
pos = changelog.index('## ')
write('CHANGELOG.md', changelog[:pos] + entry + changelog[pos:])
notice = '''## Aceite de integração Git — 12/09/2026

Rodrigo autorizou explicitamente: “Pode aprovar e integrar”. A autorização cobre
integrar a instrumentação V00 no Git; não equivale a publicação no Databricks,
auditoria independente ou homologação dos ambientes. A reconciliação e os testes
novos estão em [Integração V00](INTEGRACAO_V00.md). O estado efetivo do merge é
registrado no PR #8; não se presume merge pela existência deste documento.

As notas anteriores abaixo são históricas. Classificação semântica completa,
leitura por usuário iniciante, auditoria independente, capturas Databricks e
correção do validador editorial global continuam pendentes. A V01 pode seguir
como desenho e contrato conforme a orientação anterior de Rodrigo; não há
homologação integral nem entrega de funcionalidades visuais nesta integração.

'''
for name in ('README.md', 'CHECKPOINT_V00.md'):
    path = 'docs/sprints/sistema_temas/' + name
    original = Path(path).read_text(encoding='utf-8')
    heading, body = original.split('\n', 1)
    write(path, heading + '\n\n' + notice + '## Registro anterior (histórico)\n' + body)
report = '''# Integração Git da V00

## Para quem nunca entrou no Hub

Esta entrega acrescenta ferramentas de diagnóstico e proteção, testes e
documentação. Não muda cores nem exige executar células no Databricks. O uso
atual do Hub permanece igual. O seletor de temas ainda não foi implementado.

Rodrigo autorizou aprovar e integrar esta candidata. Integração Git significa
incorporar os arquivos na branch principal; não significa publicar no ambiente
do trabalho ou certificar a experiência de usuários iniciantes.

## Referências da rodada

'''
report += f'- Main preservada: `{main}`.\n- Candidata anterior: `{old}`.\n- Ancestral comum: `{common}`.\n- GitHub Actions run: `{os.environ["GITHUB_RUN_ID"]}`.\n'
report += '''
## Escopo e limites

Os oito gates existentes permanecem inalterados. Produto, espelho e Manual são
comparados byte a byte com a main. As evidências históricas não são reescritas.
A falha editorial global anteriormente reproduzida por referência ao catálogo
removido permanece registrada; não foi reclassificada como PASS nem corrigida
nesta integração. Os testes Node globais não são reexecutados por este workflow.
Spark, Databricks, Apps, AI/BI, leitura por iniciante e auditoria independente
continuam pendentes. A autorização de integração não substitui essas evidências.

## Recuperação

Não publicar ou sobrescrever workspaces a partir deste registro. Em caso de
regressão atribuída a esta integração, o mantenedor deve criar um PR de reversão
do merge #8, preservar alterações posteriores e repetir os gates. Não usar reset
ou force-push da main. O histórico do PR preserva base, candidata e commit final.

## Execução

O relatório de comandos abaixo é preenchido somente após execução. Os logs
completos ficam no artefato deste run, separado dos resultados históricos.
'''
report_path = 'docs/sprints/sistema_temas/INTEGRACAO_V00.md'
write(report_path, report)
git('add', '-A')
sys.path.insert(0, str(root / 'tools'))
import validate_assistant as va


def counts():
    problems = []
    actual = {'repo (identidade)': va.check_repo_corporate(problems),
              'repo (links)': va.check_repo_links(root / 'ambiente_fonte', problems)}
    assert not problems, '\n'.join(problems)
    data = Path('README.md').read_text(encoding='utf-8')
    for key, value in actual.items():
        data, n = re.subn(r'(' + re.escape(key) + r'\s*:\s*)[\d.]+', lambda m: m[1] + str(value), data)
        assert n == 1, (key, n)
    write('README.md', data)
    git('add', 'README.md')


counts()
git('commit', '-m', 'merge(temas): reconciliar V00 com READMEs e Concierge sem alterar produto (Codex)')
tested = git('rev-parse', 'HEAD').strip()
protected = ['ambiente_fonte', 'Novo_Ambiente_Simulado', 'MANUAL_TECNICO.md', 'tools/ci_local.py']
assert not git('diff', '--name-only', main, 'HEAD', '--', *protected), 'conteúdo protegido alterado'
commands = [
    ['python', '-B', 'tools/ci_local.py', '--verbose'],
    ['python', '-B', 'tools/tests/test_inventario_visual.py'],
    ['python', '-B', 'tools/tests/test_visual_legado_v00.py'],
    ['python', '-B', 'tools/tests/test_baseline_visual_runner.py'],
    ['python', '-B', 'tools/tests/test_publicar_readmes_visuais.py'],
]
if not Path(commands[-1][-1]).is_file():
    matches = list(Path('tools/tests').glob('*publicar*visual*.py'))
    assert len(matches) == 1, f'teste do publicador visual ambíguo: {matches}'
    commands[-1][-1] = str(matches[0])
results = []
for i, cmd in enumerate(commands):
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (logs / f'teste-{i}.log').write_text(p.stdout, encoding='utf-8')
    summaries = [s for s in p.stdout.splitlines() if re.match(r'^(Ran \d+ tests?|OK\b|APROVADO:|alcance\s*:)', s)]
    results.append({'comando': ' '.join(cmd), 'codigo': p.returncode, 'resumos': summaries})
    print(' '.join(cmd), p.returncode, '\n'.join(summaries), flush=True)
    if p.returncode:
        print(p.stdout[-20000:], flush=True)
        raise SystemExit(p.returncode)
assert not git('status', '--porcelain'), 'teste alterou a árvore'
report += '\n### Primeira rodada da composição\n\nCommit executado: `' + tested + '`.\n\n'
for r in results:
    report += '- `' + r['comando'] + '`: PASS (código 0).\n'
    for line in r['resumos']:
        report += '  - ' + line + '\n'
report += '''
Após registrar os resultados, o mesmo conjunto é reexecutado sobre o commit
de documentação final antes do push. O resultado dessa verificação está no run
identificado acima. SKIPs não significam homologação Spark. Revisão própria não
é auditoria independente. O workflow temporário com permissão de escrita e seu
script foram removidos antes do commit; permanece apenas o CI V00 com permissão
de leitura.
'''
write(report_path, report)
git('add', report_path)
counts()
git('commit', '-m', 'docs(temas): registrar evidências da reconciliação autorizada V00 (Codex)')
final = git('rev-parse', 'HEAD').strip()
for i, cmd in enumerate(commands):
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (logs / f'final-{i}.log').write_text(p.stdout, encoding='utf-8')
    print('FINAL', ' '.join(cmd), p.returncode, flush=True)
    if p.returncode:
        print(p.stdout[-20000:], flush=True)
        raise SystemExit(p.returncode)
assert not git('status', '--porcelain')
assert not git('diff', '--name-only', main, 'HEAD', '--', *protected)
assert all(not Path(p).exists() for p in transport)
(logs / 'resultado.json').write_text(json.dumps({
    'main': main, 'origem': source, 'commit_executado': tested, 'commit_final': final,
    'comandos': results, 'reexecucao_final': 'PASS',
    'produto_espelho_manual_gate': 'PRESERVADOS',
    'node_global': 'NAO_REEXECUTADO_FALHA_PREEXISTENTE', 'merge_main': 'NAO_REALIZADO'
}, ensure_ascii=False, indent=2), encoding='utf-8')
with open(os.environ['GITHUB_ENV'], 'a') as f:
    f.write('INTEGRACAO_PRONTA=1\n')
