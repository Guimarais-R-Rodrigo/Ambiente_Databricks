# V07 — demais consumidores e formatos de saída

> **Nota administrativa — 06/10/2026.** Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência. [Jornadas posteriores](../V12/README.md) têm escopos próprios; PASS local não se converte em PASS ambiental.

## Registro histórico preservado

> **Estado atual:** aceita por Rodrigo e integrada no Git em 14/09/2026 pelo PR #40. O head final validado foi `6b50151738a311eff8530c3191e24693af3fb036` e o merge efetivo na `main` é `67114605c7345a01c1144e5d6c6d24e9c24e2491`. A árvore do merge (`5438288bda2326e96372c7464b3aef0cb8375102`) é a mesma árvore da candidata validada. Nenhuma publicação Databricks foi realizada.

## Objetivo

A V07 fecha a dispersão visual nos consumidores runtime que ficaram fora das integrações V03/V04 e da pipeline de assets V06. O princípio é estrito: **cálculo, agregação, amostragem, domínio dos dados e decisões analíticas não pertencem ao tema**. A V07 só cria rotas visuais opt-in sobre consumidores reais identificados no inventário V00.

A fonte de verdade continua sendo `ResolvedTheme`. Nenhum consumidor lê JSON de tema diretamente, inventa fallback ou altera tema de sessão por simples import.

## O que mudou

A V07 acrescenta rotas explícitas com sufixo `_resolvido` para:

- matriz de correlação (`display/correlation_matrix`), usando `palette.diverging` no domínio simétrico de -1 a +1;
- grade de distribuições (`display/distribution_grid`);
- curvas ROC, Precision–Recall, Lift e KS (`ml/curves_plotly`);
- timeline de monitoramento (`PerformanceMonitor.plot_timeline_resolvido`);
- UMAP (`ml/umap_viz`);
- curvas e heatmap de safras (`ml/vintage_analysis`).

`theme_plotly` passa a expor `get_tokens_plotly(theme)`, que devolve uma cópia dos tokens já revalidados pelas guardas V02/V03. Isso permite que consumidores com semântica própria usem, por exemplo, `palette.curves_legacy`, `palette.diverging`, `semantic.warning` ou `palette.sequential` sem reconstruir o tema.

## O que não mudou

As APIs legadas permanecem disponíveis e com suas assinaturas atuais. Em especial:

- correlação continua sendo calculada pelo mesmo caminho Spark;
- `smart_sample` continua responsável pela amostragem da grade de distribuições;
- AUC, AP, Lift e KS não são recalculados por uma implementação alternativa;
- `PerformanceMonitor` mantém política, thresholds, histórico e decisão de governança;
- `compute_umap` continua sendo a única rotina que calcula o embedding;
- `build_vintage_table` e `compare_safras` não recebem lógica visual nova;
- `display_styled_resolvido` permanece a integração já concluída na V04.

## Exceções deliberadas

### Kaplan–Meier

`ml/kaplan_meier` usa uma ordem histórica própria de oito cores. O contrato atual não representa essa ordem sem remapear grupos de modo silencioso. A V07, portanto, **não finge suporte**: o consumidor continua legado até existir decisão explícita de contrato.

### SHAP / Matplotlib

`ml/shap_explainer` delega aparência relevante à SHAP/Matplotlib e também possui `save_path` para PNG. O contrato V01 não define colormap/estilo SHAP nem uma superfície de exportação estática tematizada. A V07 mantém esses plots inalterados e registra a limitação de forma visível.

## Formatos de saída

Suporte exercitado na V07:

- `plotly_figure_memory`: figura Plotly em memória/notebook;
- `plotly_html_file`: serialização HTML local da mesma figura, preservando os atributos visuais já presentes nela.

Já existia e continua fora da implementação V07:

- HTML de `pandas.Styler`, coberto pela V04.

Permanecem legados e não theme-aware:

- tela Matplotlib/SHAP;
- PNG salvo pelo helper SHAP.

Não foram homologados pela V07:

- PNG estático de Plotly/Kaleido;
- PDF;
- PowerPoint/PPTX;
- aparência real no navegador Databricks;
- acessibilidade do render final.

## Como usar

O fluxo é sempre explícito. Exemplo conceitual:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.ml.curves_plotly import plot_roc_curve_resolvido

theme = load_reference_theme("notebook")
fig = plot_roc_curve_resolvido(y_true, y_prob, theme)
fig.show()
```

Se o tema não for um `ResolvedTheme` íntegro, não for contexto `notebook` ou estiver em modo ainda não suportado pelo adaptador Plotly, a operação falha fechado antes de produzir uma variante temática.

## Inventário e rastreabilidade

O arquivo [`CONSUMIDORES.json`](CONSUMIDORES.json) é o registro estruturado da sprint. Ele classifica todos os consumidores runtime de `display` e `ml` apontados pelo inventário V00 em:

- `supported_v07`;
- `already_supported_v04`;
- `exception_deferred`.

Cada exceção possui motivo, responsável e efeito visível para o usuário. Templates de autoria e assets editoriais são declarados separadamente como fora do runtime desta sprint.

## Evidência de integração

No head final `6b50151738a311eff8530c3191e24693af3fb036`, o run permanente `34862446870` passou com 19/19 testes V07, 383/383 regressões V01–V07, 12/12 V00, validação documental com 0 falhas/0 avisos e workflow somente leitura. Os sete checks disparados pela PR #40 também concluíram com `success` no mesmo SHA.

Depois do merge, a `main` em `67114605c7345a01c1144e5d6c6d24e9c24e2491` disparou nove checks — CI geral e V00–V07 — e todos concluíram com `success`. Os IDs e failures históricos preservados estão em [TESTES.md](TESTES.md) e o fechamento em [CHECKPOINT_V07.md](CHECKPOINT_V07.md).

## Limites de aceite

PASS local/GitHub Actions prova contratos Python/Plotly exercitados naquele checkout. Não prova aparência real no Databricks, acessibilidade, permissões de workspace, renderização por browser, Kaleido/PDF/PPTX ou UAT humano.

A V08 é uma sprint separada de integração transversal com skills, padrões e Manual. A documentação dos objetos alterados na V07 foi atualizada na própria V07; não foi acumulada como dívida para a V08.
