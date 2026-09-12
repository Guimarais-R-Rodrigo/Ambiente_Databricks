"""Executa V00 em dois checkouts limpos e salva evidências em .artifacts/.

Não instala dependências, publica, commita, renderiza nem modifica o produto.
Logs de gates são resultados técnicos; aceite da sprint continua independente.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import time
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventario_visual import inventariar, comparar_protegidos, gravar, RAIZES_PROTEGIDAS


def executar(cmd, cwd, out, nome, root, base):
    inicio = time.monotonic()
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, env=env, timeout=240)
        code = proc.returncode
        text = (proc.stdout + proc.stderr).decode('utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        code, text = 124, 'TIMEOUT: limite de execução excedido; não aprovado.'
    except OSError as exc:
        code, text = 127, 'BLOQUEADO: comando indisponível: ' + type(exc).__name__
    text = text.replace(str(root), '<CANDIDATA>').replace(str(base), '<BASE>')
    (out / (nome + '.log')).write_text(text, encoding='utf-8')
    counts = [int(x) for x in re.findall(r'Ran (\d+) tests?\b', text)]
    # O gate imprime novamente o resumo; contar somente a linha unittest original.
    skips = [int(x) for x in re.findall(r'^OK \(skipped=(\d+)\)\s*$', text, re.MULTILINE)]
    result = {'nome': nome, 'codigo': code, 'estado': 'PASS' if code == 0 else ('BLOQUEADO' if code in (124,127) else 'FAIL'),
              'duracao_s': round(time.monotonic() - inicio, 3), 'testes_unittest_reportados': sum(counts),
              'skips_reportados': sum(skips), 'log': nome + '.log',
              'comando': [str(x).replace(str(root), '<CANDIDATA>').replace(str(base), '<BASE>') for x in cmd],
              'log_sha256': hashlib.sha256(text.encode()).hexdigest()}
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result, text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    base = args.base_root.resolve(strict=True)
    out = args.output.absolute()
    gravar(root, out / 'inicio.json', {'inicio_utc': datetime.now(timezone.utc).isoformat()})
    before = inventariar(base)
    candidate = inventariar(root)
    for name, doc in [('inventario_base.json', before), ('inventario_candidata.json', candidate)]:
        gravar(root, out / name, doc)
    changes = comparar_protegidos(before, candidate)
    protected = [r for r in before['arquivos'] if r['path'].startswith(RAIZES_PROTEGIDAS) or r['path'] == 'MANUAL_TECNICO.md']
    gravar(root, out / 'manifesto_protecao.json', {'source_commit': before['commit'], 'arquivos': protected, 'diferencas': changes})
    resultados, captures, qa = [], {}, {}
    for label, checkout in [('base', base), ('candidata', root)]:
        commands = [
            ('ci_' + label, [sys.executable, '-B', 'tools/ci_local.py', '--verbose']),
            ('publicador_visual_' + label, [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tools/readme_visuals/tests', '-p', 'test_*.py', '-v']),
            ('legado_' + label, [sys.executable, '-B', str(root / 'tools/tests/test_visual_legado_v00.py'), '--root', str(checkout)]),
            ('captura_' + label, [sys.executable, '-B', str(root / 'tools/tests/test_visual_legado_v00.py'), '--root', str(checkout), '--capturar'])]
        for nome, comando in commands:
            result, text = executar(comando, checkout, out, nome, root, base)
            resultados.append(result)
            if nome.startswith('captura_') and result['codigo'] == 0:
                captures[label] = json.loads(text)
        # O validador existente escreve qa/validation.json e compara um commit
        # editorial histórico. Executá-lo fora da árvore inventariada é obrigatório.
        with tempfile.TemporaryDirectory(prefix='qa_' + label + '_', dir=out) as tmp:
            sandbox = Path(tmp) / 'checkout'
            sha = before['commit'] if label == 'base' else candidate['commit']
            subprocess.run(['git', 'worktree', 'add', '--detach', str(sandbox), sha], cwd=root, check=True, capture_output=True)
            try:
                modules = root / 'tools/readme_visuals/node_modules'
                if modules.is_dir():
                    (sandbox / 'tools/readme_visuals/node_modules').symlink_to(modules, target_is_directory=True)
                result, visual_text = executar(['node', 'tools/readme_visuals/validate_production.mjs'], sandbox, out, 'assets_v2_' + label, root, base)
                resultados.append(result)
                report = sandbox / 'ambiente_fonte/.assistant/hub_readmes_visual_assets/qa/validation.json'
                # Usar apenas relatório emitido agora; o arquivo já versionado não
                # comprova execução desta rodada. Um crash sem regravação não passa.
                diff = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=sandbox, text=True)
                result['alteracoes_na_copia_descartavel'] = diff.splitlines()
                if report.is_file() and result['codigo'] == 0:
                    qa[label] = json.loads(report.read_text(encoding='utf-8'))
                elif report.is_file() and 'qa/validation.json' in diff:
                    qa[label] = json.loads(report.read_text(encoding='utf-8'))
                else:
                    missing = re.search(r"Error: (ENOENT)[^\n]*open '([^']+)'", visual_text)
                    reason = 'Execução não produziu relatório de QA novo verificável.'
                    if missing:
                        path = missing.group(2)
                        path = 'ambiente_fonte/' + path.split('/ambiente_fonte/', 1)[1] if '/ambiente_fonte/' in path else Path(path).name
                        reason = missing.group(1) + ': arquivo esperado pelo validador global ausente: ' + path
                    qa[label] = {'status': 'nao_confirmado', 'failures': [reason]}
                (out / ('qa_visual_' + label + '.json')).write_text(json.dumps(qa[label], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                # Validar as famílias não contorna nem aprova o gate global falho.
                # Cada resultado é guardado com alcance próprio, sem renderização.
                for family in ('top', 'snippets', 'scripts', 'skills', 'prompts'):
                    family_result, _ = executar(['node', 'tools/readme_visuals/validate_production.mjs', '--family', family], sandbox, out, 'figuras_' + label + '_' + family, root, base)
                    resultados.append(family_result)
                    family_path = sandbox / ('ambiente_fonte/.assistant/hub_readmes_visual_assets/qa/sprint_' + family + '.json')
                    if family_result['codigo'] == 0 and family_path.is_file():
                        family_report = json.loads(family_path.read_text(encoding='utf-8'))
                        family_result['verificacoes_visuais'] = family_report.get('checks')
                        (out / ('qa_' + label + '_' + family + '.json')).write_text(json.dumps(family_report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            finally:
                subprocess.run(['git', 'worktree', 'remove', '--force', str(sandbox)], cwd=root, check=True, capture_output=True)
    result, _ = executar([sys.executable, '-B', str(root / 'tools/tests/test_inventario_visual.py')], root, out, 'guardas_inventario', root, base)
    resultados.append(result)
    result, _ = executar([sys.executable, '-B', str(root / 'tools/tests/test_baseline_visual_runner.py')], root, out, 'guardas_runner', root, base)
    resultados.append(result)
    after_base = inventariar(base)
    after_candidate = inventariar(root)
    byte_integrity = before == after_base and candidate == after_candidate
    captures_equal = len(captures) == 2 and captures['base'] == captures['candidata']
    consumers = [r for r in before['arquivos'] if r['camada'] in ('produto', 'ferramenta') and r.get('ocorrencias', 0)]
    matrix = ['# Matriz automática de candidatos visuais — V00', '',
              'Extração do baseline. Classificação inicial, não revisão semântica nem catálogo operacional.', '',
              '| Caminho | Camada | Classe inicial | Ocorrências |', '|---|---|---|---:|']
    matrix += [f"| `{r['path']}` | {r['camada']} | {r['classe_inicial']} | {r['ocorrencias']} |" for r in consumers]
    (out / 'MATRIZ_AUTOMATICA.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')
    versions = {}
    for pkg in ('numpy', 'pandas', 'scikit-learn', 'plotly', 'jinja2'):
        try:
            versions[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            versions[pkg] = 'AUSENTE'
    for exe in ('node', 'pnpm', 'git'):
        try:
            versions[exe] = subprocess.check_output([exe, '--version'], text=True).strip()
        except (OSError, subprocess.CalledProcessError):
            versions[exe] = 'AUSENTE'
    summary = {'sprint': 'V00', 'estado_sprint': 'CANDIDATA_PENDENTE_DE_AUDITORIA_E_ACEITE',
        'base_commit': before['commit'], 'base_tree': before['tree'], 'candidata_commit_testado': candidate['commit'],
        'candidata_tree_testada': candidate['tree'], 'utc': datetime.now(timezone.utc).isoformat(),
        'ambiente': {'python': platform.python_version(), 'os': platform.system(), 'versoes': versions},
        'inventario': before['resumo'], 'protegidos': len(protected), 'diferencas_protegidas': changes,
        'nenhuma_alteracao_durante_testes': byte_integrity, 'capturas_legadas_identicas': captures_equal,
        'resultados': resultados, 'qa_visual': qa, 'run_id': os.environ.get('GITHUB_RUN_ID'),
        'pendencias': ['Classificação semântica nominal por revisor independente.',
            'Capturas e teste de uso no Databricks; não há acesso de runtime nesta execução.',
            'Matriz de browsers, compute, ipywidgets, Apps e AI/BI autorizados.',
            'Leitura operacional por usuário novo e aceite de Rodrigo antes de V01.',
            'Reconciliar orientação do renderer geral em sprint documental pertinente.',
            'Resolver colisão da numeração ADR-0011 quando integrar R01; não mesclar automaticamente.'],
        'observacoes': ['Skips não equivalem a aprovação Spark.',
            'Arrays, HTML e JSON não são captura de navegador.',
            'Inventário automático inclui falsos positivos e referências dinâmicas não resolvidas.']}
    summary['falhas_visuais_preexistentes'] = qa.get('base', {}).get('failures', [])
    summary['novas_falhas_visuais'] = sorted(set(qa.get('candidata', {}).get('failures', [])) - set(qa.get('base', {}).get('failures', [])))
    summary['gate_tecnico'] = 'PASS' if (not changes and byte_integrity and captures_equal and all(r['codigo'] == 0 for r in resultados)) else 'FAIL_OU_BLOQUEADO'
    gravar(root, out / 'RESUMO.json', summary)
    lines = ['# Resultado técnico V00', '', f"Estado da sprint: **{summary['estado_sprint']}**.", '',
        f"Baseline: `{before['commit']}`. Candidata executada: `{candidate['commit']}`.", '',
        f"Gate técnico: **{summary['gate_tecnico']}**. Não é aceite humano, auditoria independente ou publicação.", '',
        '| Execução | Estado | Casos unittest reportados | Skips reportados |', '|---|---|---:|---:|']
    lines += [f"| {r['nome']} | {r['estado']} | {r['testes_unittest_reportados']} | {r['skips_reportados']} |" for r in resultados]
    lines += ['', 'Contagens não incluem verificações sem unittest; não somar base e candidata como testes distintos.', '',
              f"Arquivos protegidos: {len(protected)}. Diferenças: {len(changes)}.",
              f"Capturas sintéticas iguais: {captures_equal}. Checkouts preservados durante os testes: {byte_integrity}.", '',
              '## Inventário automático', '', '```json', json.dumps(before['resumo'], ensure_ascii=False, indent=2), '```', '',
              '## Pendências de saída', ''] + ['- ' + p for p in summary['pendencias']]
    (out / 'RELATORIO_TECNICO.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('RESUMO_V00=' + json.dumps(summary, ensure_ascii=False), flush=True)
    return 0 if summary['gate_tecnico'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
