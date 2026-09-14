"""Finaliza a documentação V05 sobre a base pós-D05, uma única vez.

Este helper temporário não usa rede nem credenciais. Ele só escreve fontes
versionadas após conferir os blobs esperados, executa o renderer canônico e
aborta se o diff sair da allowlist. O workflow chamador faz o commit/push.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANUAL = ROOT / "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
ROOT_MANUAL = ROOT / "MANUAL_TECNICO.md"
SIM_MANUAL = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md"
SOURCE_README = ROOT / "ambiente_fonte/.assistant/README.md"
SIM_README = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

EXPECTED_MANUAL = "389f7166cc54afacb20aa1498c39220eae00ae5d"
EXPECTED_SOURCE_README = "be3f5f4f8118489bb4d867595c95036324307361"
EXPECTED_CHANGELOG = "ff7453fb9c369a59decaeb90a7991c5107953939"

ALLOWED = {
    "ambiente_fonte/.assistant/MANUAL_TECNICO.md",
    "MANUAL_TECNICO.md",
    "ambiente_fonte/.assistant/README.md",
    "CHANGELOG.md",
    "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md",
    "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/README.md",
}


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1, encontrado {count}")


def patch_manual() -> str:
    for path in (SOURCE_MANUAL, ROOT_MANUAL, SIM_MANUAL):
        if path.is_symlink() or blob_sha(path) != EXPECTED_MANUAL:
            raise RuntimeError(f"Manual mudou ou não corresponde à base pós-D05: {path}")

    manual = SOURCE_MANUAL.read_text(encoding="utf-8")
    if "#### `hub_snippets.visual.theme_lab`" in manual:
        raise RuntimeError("theme_lab já está no Manual")

    anchor = "#### `hub_snippets.visual.theme_plotly`\n"
    require_once(manual, anchor, "âncora theme_plotly")
    entry = '''#### `hub_snippets.visual.theme_lab`

**Candidata V05 — Visual Lab de aparência, sem aprovação ou publicação.** Este
objeto oferece uma prévia pessoal para escolher uma base `notebook`, ajustar
tokens, comparar a aparência e preservar uma sessão de autoria. Ele recebe temas
revalidados pelo núcleo V02 e reutiliza os consumidores V03/V04; não consulta
rede, Spark, SQL ou MLflow e não altera `plotly.io.templates.default` ao importar.

**Primeiro acesso.** Na cópia autorizada de `.assistant`, leia
`hub_snippets/visual/theme_lab/README.md`, siga
`hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md` e use
`exemplo_theme_lab.py` como demonstração. O launcher é opt-in: abrir o Hub não
muda o padrão da equipe e escolher um preset não o torna aprovado.

**Escolher e ajustar.** `get_demo_presets()` expõe referências empacotadas
marcadas como demonstração; `prepare_theme_lab_presets()` aceita bases fornecidas
pelo mantenedor e as revalida; `create_theme_lab_from_preset()` recusa chave
inexistente e contexto diferente de `notebook`, sem fallback silencioso.
`get_control_specs()` deriva tipo, unidade, limites e controle do schema. As
alterações são aplicadas atomicamente: um valor inválido preserva o último estado
válido. Campos ainda sem consumidor na galeria ficam desabilitados e explicam o
motivo, em vez de simular efeito.

**Rascunho e comparação.** `ThemeLabDraft` preserva base, proposta corrente,
revisão e histórico local limitado; `undo()` e `restore()` não publicam nada.
`build_preview()` e `compare_preview()` usam os mesmos dados sintéticos em
cabeçalho, KPI, barras, série temporal, heatmap e tabela. A galeria completa
permanece `light`, porque a rota Plotly V03 recusa `dark` e `high_contrast` até
que exista suporte explícito.

<details>
<summary>Consultar a API deste objeto: nomes e contratos</summary>

```text
ThemeLabError(code, message, *, action)
ControlSpec
ProposalReceipt
ThemeLabPreview
ThemeLabComparison
ThemeLabPreset
ThemeLabSessionReceipt
ThemeLabSessionInfo
ThemeLabDraft(base: ResolvedTheme)
ThemeLabUI
ThemeLabLauncherUI
get_control_specs(theme: ResolvedTheme) -> tuple[ControlSpec, ...]
prepare_theme_lab_presets(presets) -> tuple[ThemeLabPreset, ...]
get_demo_presets() -> tuple[ThemeLabPreset, ...]
create_theme_lab_from_preset(preset_key, presets) -> ThemeLabDraft
save_theme_lab_session(draft, root, session_name) -> ThemeLabSessionReceipt
reopen_theme_lab_session(root, session_name) -> ThemeLabDraft
list_theme_lab_sessions(root) -> tuple[ThemeLabSessionInfo, ...]
create_theme_lab(theme: ResolvedTheme) -> ThemeLabDraft
build_preview(theme: ResolvedTheme) -> ThemeLabPreview
compare_preview(draft: ThemeLabDraft) -> ThemeLabComparison
install_dbutils_fallback(draft, dbutils, *, prefix="hub_tema_") -> dict[str, str]
apply_dbutils_fallback(draft, dbutils, *, prefix="hub_tema_") -> ResolvedTheme
build_ipywidgets_lab(draft, *, save_root=None, render_initial=True) -> ThemeLabUI
build_theme_lab_launcher(*, presets=None, save_root=None) -> ThemeLabLauncherUI
```

A fachada `__init__.py` é a referência exata dos nomes públicos; o README local
documenta assinaturas, opções e exemplos com mais detalhe.

</details>

**Persistência e linhagem local.** JSON avulso e sessão são produtos diferentes.
`save_proposal()` salva apenas a configuração atual. `save_theme_lab_session()`
cria um diretório novo com `base.json`, `proposal.json`, histórico e
`session.json`; o manifesto é escrito por último e registra hashes e revisão.
Sessão incompleta não aparece na listagem nem é reaberta. A reabertura revalida
os temas, confere os hashes e restaura base original, proposta, revisão e
histórico; adulteração é recusada em vez de ter o hash “corrigido”. O bundle não
autentica autor, não assina conteúdo e não registra aprovação de governança.

**Interface e dependências.** Importar o módulo não carrega `ipywidgets`.
Validação exige `jsonschema`/`referencing`; a galeria usa pandas, Plotly e Jinja2;
a interface completa usa ipywidgets/IPython quando construída. O fallback
`dbutils.widgets` recebe `dbutils` explicitamente e é funcionalmente menor: não
tem paridade com o launcher de presets/sessões. Nenhuma função instala pacotes.

**Segurança e limites de evidência.** Persistência exige pasta regular já
existente, não sobrescreve sessão/arquivo existente e não emite recibo de sucesso
quando a escrita falha. Essas guardas não substituem ACL do ambiente nem formam
uma sandbox. Os testes Python/GitHub Actions exercitam estado, callbacks no
kernel, presets, sessões, hashes e roundtrip; não homologam navegador/runtime
Databricks, teclado/leitor de tela, contraste percebido, zoom, p95, ACL real,
reinício de sessão ou UAT por iniciante. A V05 continua candidata: sem aceite,
merge, publicação Databricks ou início da V06.

'''
    manual = manual.replace(anchor, entry + anchor)

    old_count = "Este inventário cobre as 51 pastas de snippets e os sete scripts do snapshot examinado."
    require_once(manual, old_count, "contagem introdutória do inventário")
    manual = manual.replace(
        old_count,
        "Este inventário cobre as 52 pastas de snippets da candidata V05 e os sete scripts do snapshot examinado.",
    )

    old_heading = "## Sistema de Temas — V04 integrada no Git\n"
    require_once(manual, old_heading, "heading final V04")
    manual = manual.replace(
        old_heading,
        "## Sistema de Temas — V04 integrada no Git; V05 candidata em fechamento\n",
    )

    old_ending = '''Não migre chamadas existentes em massa nesta sprint. Não há publicação,
seletor, Visual Lab ou aprovação operacional de tema. Consulte
`hub_padroes/identidade_visual/GUIA_OPERACIONAL.md` e
`docs/sprints/sistema_temas/V04/README.md` no repositório de manutenção.
'''
    require_once(manual, old_ending, "encerramento V04")
    new_ending = '''Não migre chamadas existentes em massa. A V04 permanece integrada e opt-in. A
V05 acrescenta o Visual Lab descrito no inventário acima, também de forma opt-in,
mas continua candidata: não há aceite, merge da V05, publicação no workspace ou
aprovação operacional de identidade. Presets, comparação e sessão rastreável com
reabertura foram exercitados no contrato Python; navegador/runtime Databricks,
acessibilidade, p95, ACL real e UAT continuam gates separados. Consulte
`hub_padroes/identidade_visual/GUIA_OPERACIONAL.md` e
`docs/sprints/sistema_temas/V05/README.md` no repositório de manutenção. A V06
não foi iniciada.
'''
    return manual.replace(old_ending, new_ending)


def patch_hub_readme() -> str:
    if SOURCE_README.is_symlink() or blob_sha(SOURCE_README) != EXPECTED_SOURCE_README:
        raise RuntimeError("README .assistant mudou; reconciliar antes de escrever")
    hub = SOURCE_README.read_text(encoding="utf-8")
    if "Visual Lab do Sistema de Temas — V05 candidata" in hub:
        raise RuntimeError("bloco V05 já está no README do Hub")

    map_anchor = "| conferir runtime, dependências e segurança | [Compute e Segurança](#️-dependências-compute-e-segurança) |\n"
    require_once(hub, map_anchor, "âncora do mapa do Hub")
    hub = hub.replace(
        map_anchor,
        "| experimentar aparência de notebook sem publicar tema | [Visual Lab](hub_snippets/visual/theme_lab/README.md) |\n" + map_anchor,
    )

    scripts_anchor = "### ⚡ 3. Hub Scripts (`hub_scripts/`)\n"
    require_once(hub, scripts_anchor, "âncora Hub Scripts")
    lab_block = '''#### 🎨 Visual Lab do Sistema de Temas — V05 candidata

Dentro de `hub_snippets/visual/`, o objeto
[`theme_lab`](hub_snippets/visual/theme_lab/README.md) oferece uma experiência
opt-in para escolher uma base `notebook`, ajustar aparência, comparar a proposta
e salvar/reabrir uma sessão local. Comece pelo
[guia de primeiro uso](hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md).

O laboratório **não muda o padrão da equipe e não publica temas**. Presets de
demonstração continuam identificados como demonstração; uma sessão salva registra
linhagem local de base/proposta/histórico, não identidade ou aprovação. Os testes
automatizados exercitam o contrato Python e os callbacks no kernel, mas não
homologam navegador/runtime Databricks, acessibilidade, p95, ACL real ou UAT.
Enquanto a V05 estiver em candidata, seu uso deve ser tratado como laboratório,
não como configuração operacional aprovada.

'''
    return hub.replace(scripts_anchor, lab_block + scripts_anchor)


def patch_changelog() -> str:
    if CHANGELOG.is_symlink() or blob_sha(CHANGELOG) != EXPECTED_CHANGELOG:
        raise RuntimeError("CHANGELOG mudou; reconciliar antes de escrever")
    log = CHANGELOG.read_text(encoding="utf-8")
    anchor = "## 2026-09-13 — D05: reconciliação documental do Sistema de Temas (ChatGPT)\n"
    require_once(log, anchor, "âncora do CHANGELOG")
    entry = '''## 2026-09-14 — V05: fechamento técnico do Visual Lab em candidata (Codex)

### Adicionado

- (Codex) `hub_snippets.visual.theme_lab` entra no inventário do Manual com presets, edição atômica, comparação, sessão rastreável, reabertura e limites operacionais.
- (Codex) Entrada de primeiro uso no README do Hub para localizar o laboratório sem confundi-lo com publicação ou aprovação de tema.

### Atualizado

- (Codex) Candidata V05 reconciliada com a `main` pós-D05 `24ffce29`, preservando a documentação R13/D05 e mantendo a PR #26 como evidência histórica.
- (Codex) README do objeto migrado ao contrato `readme-objeto: 1.0.0`; checkpoint, testes e índices registram presets/linhagem/reabertura como contratos Python implementados, não homologação Databricks.
- (Codex) `CLAUDE.md` e Manual distinguem V04 integrada de V05 ainda candidata; a cobertura estrutural passa a incluir o novo 76º objeto fora do escopo histórico R00–R13.

### Notas

- (Codex) Runs reprovados continuam reprovados. `34797774791` falhou por contrato textual; `34798200237`, `34798497708` e `34798674298` mantiveram funções/regressões verdes e reprovaram o fechamento documental/métricas então desatualizadas.
- (Codex) Nas composições recentes foram observados 31/31 testes específicos V05, 14/14 de sessões, 359/359 regressões de temas e 12/12 V00; esses resultados são Python/GitHub Actions, não homologação de navegador/runtime Databricks.
- (Codex) Métricas finais do README, CI geral e PR final ainda dependem da árvore de fechamento; nenhum sucesso é antecipado nesta entrada.
- (Codex) Sem aceite V05, merge, publicação Databricks, homologação operacional ou início da V06.

'''
    return log.replace(anchor, entry + anchor)


def changed_paths() -> set[str]:
    output = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    result: set[str] = set()
    for line in output.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        result.add(path)
    return result


def main() -> int:
    SOURCE_MANUAL.write_text(patch_manual(), encoding="utf-8")
    ROOT_MANUAL.write_text(SOURCE_MANUAL.read_text(encoding="utf-8"), encoding="utf-8")
    SOURCE_README.write_text(patch_hub_readme(), encoding="utf-8")
    CHANGELOG.write_text(patch_changelog(), encoding="utf-8")

    subprocess.run(["python", "tools/render_simulado.py", "--write"], cwd=ROOT, check=True)

    changed = changed_paths()
    extra = changed - ALLOWED
    missing = ALLOWED - changed
    print("Arquivos alterados:")
    for path in sorted(changed):
        print(" -", path)
    if extra:
        raise RuntimeError("arquivo fora da allowlist: " + ", ".join(sorted(extra)))
    if missing:
        raise RuntimeError("alteração esperada ausente: " + ", ".join(sorted(missing)))

    if SOURCE_MANUAL.read_bytes() != ROOT_MANUAL.read_bytes() or SOURCE_MANUAL.read_bytes() != SIM_MANUAL.read_bytes():
        raise RuntimeError("as três cópias do Manual não ficaram idênticas")
    if SOURCE_README.read_bytes() != SIM_README.read_bytes():
        raise RuntimeError("README fonte e derivado não ficaram idênticos")

    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("OK: patch documental aplicado e escopo conferido; commit ainda não realizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
