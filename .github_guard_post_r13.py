from pathlib import Path
import json, subprocess
R=Path('.')
B='99e01012c26621539b4379ca301e4782765f68c0'
changed=set(subprocess.check_output(['git','diff','--name-only',B],text=True).splitlines())
for p in changed:
    if p.startswith('docs/sprints/readmes_objetos/') and p!='docs/sprints/readmes_objetos/README.md':
        raise SystemExit(f'histórico R00-R13 alterado: {p}')
    if p.endswith('/README.md') and any(x in p for x in ('hub_snippets/','hub_scripts/','hub_prompts/')):
        parts=Path(p).parts
        if 'Novo_Ambiente_Simulado' not in parts and len(parts)>=5 and p not in {
            'ambiente_fonte/.assistant/hub_snippets/README.md',
            'ambiente_fonte/.assistant/hub_scripts/README.md',
            'ambiente_fonte/.assistant/hub_prompts/README.md'}:
            raise SystemExit(f'README de objeto alterado: {p}')
control=json.loads(Path('docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json').read_text(encoding='utf-8'))
assert control['phase']=='complete' and control['pending']=={}
scripts=Path('ambiente_fonte/.assistant/hub_scripts/README.md').read_text(encoding='utf-8')
script_dirs=[p.name for p in Path('ambiente_fonte/.assistant/hub_scripts').iterdir() if p.is_dir() and (p/'README.md').is_file()]
assert all(f'({n}/README.md)' in scripts for n in script_dirs), script_dirs
prompts=Path('ambiente_fonte/.assistant/hub_prompts/README.md').read_text(encoding='utf-8')
prompt_dirs=[p.name for p in Path('ambiente_fonte/.assistant/hub_prompts').iterdir() if p.is_dir() and (p/'README.md').is_file()]
assert all(f'[README local]({n}/README.md)' in prompts for n in prompt_dirs), prompt_dirs
snip=Path('ambiente_fonte/.assistant/hub_snippets/README.md').read_text(encoding='utf-8')
for stale in ('migração das pastas legadas é gradual','A migração dos legados é gradual'):
    assert stale not in snip
assert 'contrato candidato' not in Path('ambiente_fonte/.assistant/hub_padroes/README.md').read_text(encoding='utf-8')
assert 'legados têm dispensa' not in Path('.claude/rules/docs-e-readmes.md').read_text(encoding='utf-8')
assert 'Estado da migração de READMEs — R04-B' not in Path('CLAUDE.md').read_text(encoding='utf-8')
assert Path('MANUAL_TECNICO.md').read_bytes()==Path('ambiente_fonte/.assistant/MANUAL_TECNICO.md').read_bytes()
print(f'PASS pós-R13: {len(script_dirs)}/7 scripts e {len(prompt_dirs)}/16 prompts com guia; históricos preservados; pending=0.')
