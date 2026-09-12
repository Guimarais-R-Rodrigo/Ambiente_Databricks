"""Conferência de preservação documental, sem executar exemplos ou modificar Git."""
import ast, hashlib, json, re, subprocess, sys
from pathlib import Path
R=Path(sys.argv[1]).resolve(); BASE='0c76bce9f3fa0f52b4312b60c3059e0fd27a2733'
def git(*args): return subprocess.check_output(['git','-C',str(R),*args])
def old(p): return git('show',f'{BASE}:{p}')
def now(p): return (R/p).read_bytes()
paths=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
H='ambiente_fonte/.assistant/'
modules=[p for p in paths if p.startswith((H+'hub_snippets/',H+'hub_scripts/')) and p.endswith('.py') and not Path(p).name.startswith('exemplo_')]
for p in modules: assert old(p)==now(p),p
six=['hub_snippets/ml/train_xgboost','hub_snippets/ml/isolation_forest','hub_snippets/spark/pit_join','hub_snippets/constants/format_br','hub_scripts/quick_profile','hub_prompts/eda_rapida']
notebooks=[H+o+'/exemplo_'+o.split('/')[-1]+'.py' for o in six]
def executable_magics(t):
    return [l for l in t.splitlines() if re.match(r'# MAGIC\s*[%!]',l) and not re.match(r'# MAGIC\s*%md(?:\s|$)',l)]
def outputs(t): return re.findall(r'```(?:text|plaintext)\s*\n.*?```',t,re.S)
for p in notebooks:
    a,b=old(p).decode(),now(p).decode()
    assert ast.dump(ast.parse(a),include_attributes=False)==ast.dump(ast.parse(b),include_attributes=False),p
    assert executable_magics(a)==executable_magics(b),p
    assert outputs(a)==outputs(b),p
prompts=[p for p in paths if p.endswith('.md') and (p.startswith(H+'hub_prompts/') or p.startswith(H+'hub_padroes/prompt/')) and '## Prompt pronto para colar' in old(p).decode()]
for p in prompts:
    for a,b in [(old(p).decode().split('## Prompt pronto para colar',1)[1],now(p).decode().split('## Prompt pronto para colar',1)[1])]:
        assert re.search(r'```.*?```',a,re.S).group()==re.search(r'```.*?```',b,re.S).group(),p
protected_prefixes=[H+'skills/',H+'hub_readmes_visual_assets/',H+'hub_padroes/','.claude/rules/','tools/','.github/workflows/','novas_funcionalidades/']
protected=[p for p in paths if any(p.startswith(x) for x in protected_prefixes)]
for p in protected: assert old(p)==now(p),p
control='docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json'
assert old(control)==now(control)
manuals=[H+'MANUAL_TECNICO.md','MANUAL_TECNICO.md','Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md']
assert len({hashlib.sha256(now(p)).hexdigest() for p in manuals})==1
assert all(old(p)==now(p) for p in manuals)
result={'base':BASE,'modulos_e_testes_de_helpers_intactos':len(modules),'notebooks_piloto_ast_magics_outputs_iguais':len(notebooks),'blocos_colaveis_iguais':len(prompts),'arquivos_em_prefixos_protegidos_iguais':len(protected),'controle_migracao_igual':True,'manual_tres_copias_identicas_e_intactas':True,'contrato_e_exemplares_intactos':True,'sucesso':True}
print(json.dumps(result,ensure_ascii=False,indent=2))
