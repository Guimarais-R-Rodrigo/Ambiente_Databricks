from pathlib import Path
ROOT=Path.cwd()

def text(rel): return (ROOT/rel).read_text(encoding="utf-8")
def need(rel,*needles):
    t=text(rel)
    for n in needles:
        if n not in t: raise SystemExit(f"FAIL D05 marcador ausente em {rel}: {n}")
def forbid(rel,*needles):
    t=text(rel)
    for n in needles:
        if n in t: raise SystemExit(f"FAIL D05 rotulo antigo em {rel}: {n}")

need("ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md","V02 INTEGRADA; CONSUMO OPT-IN ATÉ V04","V04 estendeu a mesma arquitetura")
need("ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md","O núcleo V02 está integrado no Git","V03 e V04 acrescentam consumidores opt-in")
need("ambiente_fonte/.assistant/hub_snippets/README.md","Núcleo de temas integrado no Git","V04 estende a rota explícita")
need("ambiente_fonte/.assistant/MANUAL_TECNICO.md","## Sistema de Temas — V04 integrada no Git","não confirma publicação no workspace")
need("docs/README.md","## Sistema de Temas — estado vigente no Git","D05 reconcilia somente documentação viva")
need("docs/decisions/README.md","V01–V04 integradas no Git")
need("docs/decisions/ADR-0013-sistema-de-temas.md","## Registro de implementação V02–V04 e reconciliação D05")
need("docs/sprints/sistema_temas/README.md","documentação viva reconciliada em D05","sprint funcional V05")
need("docs/sprints/sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md","D05 é uma etapa **documental de manutenção**","não é a sprint funcional V05")
forbid("ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md","V02 CANDIDATA")
forbid("ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md","A candidata precisa ser instalada")
forbid("ambiente_fonte/.assistant/hub_snippets/README.md","Novo núcleo candidato")
forbid("ambiente_fonte/.assistant/MANUAL_TECNICO.md","## Sistema de Temas — V04 (candidata)")
forbid("docs/README.md","## Sistema de Temas — execução candidata")
forbid("docs/decisions/README.md","aceito para V01; integração Git condicionada aos checks")

ch=text("CHANGELOG.md")
if "(Codex) V04 é candidata: sem aceite" not in ch: raise SystemExit("FAIL D05 nota historica V04 foi reescrita")
if "D05: reconciliação documental do Sistema de Temas" not in ch: raise SystemExit("FAIL D05 changelog novo ausente")

m=(ROOT/"ambiente_fonte/.assistant/MANUAL_TECNICO.md").read_bytes()
if m!=(ROOT/"MANUAL_TECNICO.md").read_bytes(): raise SystemExit("FAIL D05 Manual fonte != raiz")
if m!=(ROOT/"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md").read_bytes(): raise SystemExit("FAIL D05 Manual fonte != simulado")
for rel in ["hub_padroes/README.md","hub_padroes/identidade_visual/README.md","hub_padroes/identidade_visual/GUIA_OPERACIONAL.md","hub_snippets/README.md"]:
    a=(ROOT/"ambiente_fonte/.assistant"/rel).read_bytes(); b=(ROOT/"Novo_Ambiente_Simulado/Users/usuario-free/.assistant"/rel).read_bytes()
    if a!=b: raise SystemExit(f"FAIL D05 espelho divergente: {rel}")
print("PASS D05 estado: rotulos vivos coerentes; historia preservada; fonte/raiz/simulado sincronizados.")
