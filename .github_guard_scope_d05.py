from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
BASE="88106290a8c92b52ef2ec5294247064237dfc8c2"

def git(*a):
    return subprocess.check_output(["git","-C",str(ROOT),*a],text=True,encoding="utf-8")

allowed={
"README.md","CHANGELOG.md","MANUAL_TECNICO.md",
"ambiente_fonte/.assistant/MANUAL_TECNICO.md",
"ambiente_fonte/.assistant/hub_padroes/README.md",
"ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md",
"ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md",
"ambiente_fonte/.assistant/hub_snippets/README.md",
"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md",
"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/README.md",
"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/identidade_visual/README.md",
"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md",
"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/README.md",
"docs/README.md","docs/decisions/README.md","docs/decisions/ADR-0013-sistema-de-temas.md",
"docs/sprints/documentacao_pos_r13.md","docs/sprints/sistema_temas/README.md",
"docs/sprints/sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md"}
changed=set(git("diff","--name-only",BASE).splitlines())
unexpected=sorted(changed-allowed)
if unexpected: raise SystemExit(f"FAIL D05 caminhos fora do escopo: {unexpected}")

hist=git("diff","--name-only",BASE,"--","docs/sprints/sistema_temas").splitlines()
prefixes=("V00","V01/","V02/","V03/","V04/","CHECKPOINT_V00","ACHADOS_V00","INTEGRACAO_V00","RASTREABILIDADE_V00")
bad=[p for p in hist if any(p.startswith("docs/sprints/sistema_temas/"+x) for x in prefixes)]
if bad: raise SystemExit(f"FAIL D05 historico V00-V04 alterado: {bad}")

snip=git("diff","--name-only",BASE,"--","ambiente_fonte/.assistant/hub_snippets").splitlines()
if snip != ["ambiente_fonte/.assistant/hub_snippets/README.md"]:
    raise SystemExit(f"FAIL D05 objeto/implementacao alterado: {snip}")
subprocess.check_call(["git","-C",str(ROOT),"diff","--check"])
print(f"PASS D05 escopo: {len(changed)} caminhos; historicos V00-V04 e objetos preservados.")
