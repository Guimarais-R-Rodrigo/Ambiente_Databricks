"""Guarda R09: diff nominal, código/magics, saídas históricas e espelho.

Somente leitura. Erro, arquivo extra ou conjunto inesperado reprovam.
"""
from __future__ import annotations
import ast
import json
from pathlib import Path
import re
import subprocess
from aplicar_r09 import BASE, OBJECTS, ROOT, SPRINT, expected_paths


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def old(path):
    return git('show',f'{BASE}:{path}')


def md_cell(cell):
    first=[x for x in cell.splitlines() if x.strip() and x!='# Databricks notebook source']
    return bool(first) and first[0]=='# MAGIC %md'


def fences(cell):
    """Preserva todos os blocos cercados, inclusive erros e saídas históricas."""
    blocks=[];current=[];active=False
    for line in cell.splitlines(keepends=True):
        if re.match(r'^# MAGIC\s+```',line):
            if active:
                current.append(line);blocks.append(''.join(current));current=[];active=False
            else:current=[line];active=True
        elif active:current.append(line)
    if active:raise AssertionError('fence sem fechamento')
    return blocks


def notebook(old_bytes,new_bytes):
    a=old_bytes.decode('utf-8');b=new_bytes.decode('utf-8')
    ca=a.split('# COMMAND ----------');cb=b.split('# COMMAND ----------')
    assert len(ca)==len(cb),'quantidade de células'
    for left,right in zip(ca,cb):
        assert md_cell(left)==md_cell(right),'tipo de célula'
        if md_cell(left):assert fences(left)==fences(right),'saída histórica alterada'
        else:assert left==right,'código ou magic executável alterado'
    assert ast.dump(ast.parse(a))==ast.dump(ast.parse(b)),'AST alterada'


def main():
    paths=expected_paths()
    changed=git('diff','--name-only',BASE,'--').decode().splitlines()
    assert set(changed)==set(paths),(set(changed)-set(paths),set(paths)-set(changed))
    assert not git('ls-files','--others','--exclude-standard').strip(),'arquivos não versionados'
    base_paths=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
    protected=set(base_paths)-set(paths)
    assert not protected.intersection(changed)
    modes=git('ls-files','--stage').decode().splitlines()
    assert all(line.split()[0]!='120000' for line in modes if line.split('\t',1)[-1] in paths),'symlink novo'
    for obj in OBJECTS:
        prefix=f'ambiente_fonte/.assistant/hub_snippets/ml/{obj}'
        for name in (obj+'.py','__init__.py'):
            path=f'{prefix}/{name}';assert (ROOT/path).read_bytes()==old(path),path
        path=f'{prefix}/exemplo_{obj}.py';notebook(old(path),(ROOT/path).read_bytes())
        assert '[README deste objeto](README.md)' in (ROOT/path).read_text(encoding='utf-8')
    prior_readmes=[p for p in base_paths if p.startswith('ambiente_fonte/.assistant/') and p.endswith('/README.md') and p not in paths]
    for path in prior_readmes:assert (ROOT/path).read_bytes()==old(path),path
    op=json.loads(old(f'{SPRINT}/CONTROLE_MIGRACAO.json'));np=json.loads((ROOT/f'{SPRINT}/CONTROLE_MIGRACAO.json').read_text(encoding='utf-8'))
    removed={f'hub_snippets/ml/{o}' for o in OBJECTS}
    assert set(op['pending'])-set(np['pending'])==removed
    assert not set(np['pending'])-set(op['pending'])
    assert all(np['pending'][k]==op['pending'][k] for k in np['pending'])
    assert {k:v for k,v in op.items() if k!='pending'}=={k:v for k,v in np.items() if k!='pending'}
    previous=old('CHANGELOG.md').decode('utf-8');current=(ROOT/'CHANGELOG.md').read_text(encoding='utf-8')
    prefix,rest=previous.split('\n## ',1)
    assert current.startswith(prefix+'\n## 2026-09-13 — R09:')
    assert current.endswith('\n## '+rest),'histórico de changelog reescrito'
    source=ROOT/'ambiente_fonte';mirror=ROOT/'Novo_Ambiente_Simulado/Users/usuario-free'
    eligible={p.relative_to(source) for p in (source/'.assistant').rglob('*') if p.is_file()}
    eligible.add(Path('.assistant_instructions.md'))
    assert all('__pycache__' not in p.parts and p.suffix not in ('.pyc','.pyo') for p in eligible),'artefato local no produto'
    rendered={p.relative_to(mirror) for p in mirror.rglob('*') if p.is_file()}
    assert eligible==rendered,(eligible-rendered,rendered-eligible)
    for rel in eligible:assert (source/rel).read_bytes()==(mirror/rel).read_bytes(),str(rel)
    manual=(source/'.assistant/MANUAL_TECNICO.md').read_bytes()
    assert manual==(ROOT/'MANUAL_TECNICO.md').read_bytes()==(mirror/'.assistant/MANUAL_TECNICO.md').read_bytes()
    template=(source/'.assistant/hub_padroes/readme/template_objeto.md').read_text(encoding='utf-8')
    headings=re.findall(r'^## \d+\. .+$',template,re.M)
    assert len(headings)==15
    for obj in OBJECTS:
        text=(source/f'.assistant/hub_snippets/ml/{obj}/README.md').read_text(encoding='utf-8')
        assert re.findall(r'^## \d+\. .+$',text,re.M)==headings,obj
        assert '<!-- readme-objeto: 1.0.0 -->' in text and '## Visão rápida' in text,obj
    result={'state':'PASS','base':BASE,'paths':len(paths),'derived':sum(p.startswith('Novo_Ambiente_Simulado/') for p in paths),'unchanged_existing_paths':len(protected),'prior_readmes_preserved':len(prior_readmes),'implementations_facades':10,'notebooks_code_magics_outputs':5,'pending_removed':5,'published_files_mirrored':len(eligible),'manual_copies':3}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
