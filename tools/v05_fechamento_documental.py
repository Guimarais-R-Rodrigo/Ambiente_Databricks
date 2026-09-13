"""Prepara somente Manual e CHANGELOG da candidata V05 em checkout local.

Sem rede, credenciais, publicacao, mudanca de branch ou execucao de workflows.
O modo padrao apenas confere a base. --write aplica duas insercoes aditivas.
Depois, o mantenedor deve sincronizar o Manual, renderizar e repetir os gates.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'ambiente_fonte/.assistant/MANUAL_TECNICO.md': 'd15952f1570604e31f6d6c7a01503423368c6f5b',
    'CHANGELOG.md': 'd59b510982d2e4d042414ebbf1e9c533a956037e',
}
MANUAL_ENTRY = '''#### `hub_snippets.visual.theme_lab`

**Candidata V05 — laboratorio de aparencia, nao publicador.** Este objeto cria
uma previa pessoal para experimentar cores, fontes, dimensoes e paletas. Recebe
um `ResolvedTheme` notebook revalidado pelo nucleo V02 e reutiliza Plotly V03 e
HTML/tabelas V04. Nao consulta tabelas, nao treina modelos e nao muda o padrao da
 equipe nem os notebooks ja exibidos.

**Primeiro acesso.** Na copia autorizada de `.assistant`, abra
`hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md` e depois
`exemplo_theme_lab.py`. O mantenedor entrega caminho, pacote e dependencias
preparados. O operador ajusta controles, nao o codigo de cores. Depois de abrir
o painel, nao use Executar tudo: a celula de criacao reinicia o rascunho.

**Contrato.** `create_theme_lab(theme)` devolve um `ThemeLabDraft` isolado.
`apply_updates` valida o conjunto antes de trocar o estado; `undo` desfaz e
`restore` volta a base. `dirty` compara proposta e base, nao confirma gravacao.
A galeria usa dados sinteticos fixos em cabecalho, KPI, barras, serie, mapa de
calor e tabela. A galeria completa suporta somente notebook/light. Campos sem
consumidor ficam desabilitados; imagens raster nao sao recoloridas.

<details>
<summary>Consultar a API deste objeto: nomes e contratos</summary>

```text
ThemeLabError(code, message, *, action)
ControlSpec: token, label, description, unit, control, minimum, maximum, enum, primary, preview_supported, unavailable_reason
ProposalReceipt: filename, sha256, bytes_written, revision, destination
ThemeLabPreview: header_html, kpi_html, table_html, bar_figure, series_figure, heatmap_figure
ThemeLabComparison: current (base), proposal
ThemeLabDraft(base: ResolvedTheme)
  apply_updates(updates) / set_token(token, value) -> ResolvedTheme
  undo() / restore() -> ResolvedTheme
  export_bytes() -> bytes
  save_proposal(root, filename) -> ProposalReceipt
ThemeLabUI: root, draft, controls, status, preview
get_control_specs(theme: ResolvedTheme) -> tuple[ControlSpec, ...]
create_theme_lab(theme: ResolvedTheme) -> ThemeLabDraft
build_preview(theme: ResolvedTheme) -> ThemeLabPreview
compare_preview(draft: ThemeLabDraft) -> ThemeLabComparison
install_dbutils_fallback(draft, dbutils, *, prefix="hub_tema_") -> dict[str, str]
apply_dbutils_fallback(draft, dbutils, *, prefix="hub_tema_") -> ResolvedTheme
build_ipywidgets_lab(draft, *, save_root=None, render_initial=True) -> ThemeLabUI
```

Os resumos das classes nao sao construtores alternativos. O modulo e sua fachada
sao a fonte das assinaturas. O notebook exibe a UI com `display(ui.root)`.

</details>

**Dependencias.** Validacao: jsonschema/referencing; galeria: pandas, Plotly e
Jinja2; painel: ipywidgets/IPython. Importar nao carrega ipywidgets nem instala
pacotes. O fallback recebe `dbutils` explicitamente, oferece sete campos e exige
reexecutar a celula de aplicacao. Nao possui paridade de interface.

**Efeitos separados.** Exportar devolve JSON em memoria, sem criar arquivo.
Salvar cria novo JSON em pasta existente explicitamente indicada, recusa
sobrescrita e so emite recibo apos conferir os bytes. Sem pasta, Salvar fica
desabilitado. Campos nao aplicados bloqueiam salvar/exportar pela UI. Salvar nao
e submeter, aprovar ou publicar; os tres ultimos servicos nao existem nesta V05.

**Falhas e reabertura.** Falha de escrita ou sincronizacao pode deixar arquivo
parcial, nunca recibo de sucesso. O mantenedor inspeciona o destino; nao apagar
arquivos para tentar corrigir. A pasta e seus pais devem ter acesso controlado.
A gravacao nao e transacao de filesystem nem sandbox contra outros processos.
Para reabrir, o mantenedor prepara `load_theme` com pasta, nome, hash e contexto.
Recupera-se o tema, nao o historico de Desfazer.

**Integridade nao e linhagem.** O JSON e o recibo nao registram automaticamente
o hash da base. `theme_id` e `theme_version` nao provam essa origem. Registrar
base e proposta separadamente na revisao nao substitui linhagem implementada.
Nao inserir campos extras no JSON canonico. Ao reabrir, a proposta vira nova
base; a base original nao e recuperada automaticamente.

**Limites.** Escolha visual de presets, linhagem automatica e reabertura autonoma
permanecem lacunas da candidata. Testes Python nao homologam navegador,
Databricks, acessibilidade, p95, permissoes ou uso por iniciante. Nenhum aceite,
merge, publicacao ou inicio da V06 e presumido por esta documentacao.

'''
CHANGELOG_ENTRY = '''## 2026-09-13 — V05: preparacao do fechamento documental (Codex)

### Adicionado

- (Codex) Registro de `hub_snippets.visual.theme_lab` no Manual canonico, com API,
  operacao, dependencias, efeitos e lacunas de linhagem, presets e reabertura.

### Notas

- (Codex) Insercoes aditivas sobre blobs conferidos; texto anterior preservado.
- (Codex) Sincronizacao do Manual, espelho, navegacao, contagens e bateria final
  continuam condicionadas a execucao e conferencia pelo mantenedor.
- (Codex) O CI 34754060402 reprovou a ausencia do objeto no Manual. Nao se
  reclassifica esse run nem se antecipa sucesso para a composicao nova.
- (Codex) Sem alteracao funcional, aceite V05, merge, publicacao ou V06.

'''


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    originals = {}
    for relative, expected in EXPECTED.items():
        path = ROOT / relative
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise RuntimeError('Caminho simbolico recusado.')
        data = path.read_bytes()
        if git_blob_sha(data) != expected:
            raise RuntimeError('A base documental mudou; reconciliar antes de escrever: ' + relative)
        originals[relative] = data
    manual_key = 'ambiente_fonte/.assistant/MANUAL_TECNICO.md'
    manual = originals[manual_key].decode('utf-8')
    anchor = '#### `hub_snippets.visual.theme_plotly`\n'
    if manual.count(anchor) != 1 or '#### `hub_snippets.visual.theme_lab`' in manual:
        raise RuntimeError('Ancora ausente, duplicada ou entrada ja aplicada.')
    log = originals['CHANGELOG.md'].decode('utf-8')
    log_anchor = '## 2026-09-12 — V04: componentes HTML e tabelas opt-in (Codex)\n'
    if log.count(log_anchor) != 1:
        raise RuntimeError('Ancora do changelog mudou.')
    proposed = {
        manual_key: manual.replace(anchor, MANUAL_ENTRY + anchor).encode('utf-8'),
        'CHANGELOG.md': log.replace(log_anchor, CHANGELOG_ENTRY + log_anchor).encode('utf-8'),
    }
    for relative, data in proposed.items():
        print(relative, 'antes=' + git_blob_sha(originals[relative]), 'depois=' + git_blob_sha(data))
    if not args.write:
        print('CONFERIDO; nenhum arquivo alterado. --write aplica somente as duas fontes.')
        return 0
    for relative, original in originals.items():
        if (ROOT / relative).read_bytes() != original:
            raise RuntimeError('Arquivo alterado durante a preparacao; escrita cancelada.')
    for relative, data in proposed.items():
        (ROOT / relative).write_bytes(data)
    print('Duas fontes atualizadas. Sincronizacao, renderer, contagens e testes ainda pendentes.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
