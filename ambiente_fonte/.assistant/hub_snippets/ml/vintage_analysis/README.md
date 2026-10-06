# `vintage_analysis` — maturação por safra sem preencher o que ainda não foi observado

<!-- readme-objeto: 1.0.0 -->
<!-- sistema-temas-v07: consumidores -->
build_vintage_table e compare_safras calculam os resultados sem configuração de aparência. Use plot_vintage_curves_resolvido ou plot_vintage_heatmap_resolvido com ResolvedTheme notebook/light para personalizar as figuras. As rotas preservam pontos, matrizes, maturidades, denominadores, taxas e células NaN; curvas usam paleta categórica e heatmap, sequencial.

Análise de vintage organiza contratos pela safra de originação e pelo tempo decorrido desde a originação, aqui expresso em MOB (*months on book*). Este helper constrói taxas acumuladas somente quando a célula safra×MOB está completamente observada e oferece curvas, heatmap e comparação de checkpoints. Ele ajuda a comparar maturação; **não extrapola safras imaturas nem corrige sozinho definição de evento, denominator ou censura operacional**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Construtor pandas de tabela safra×MOB + visualizações Plotly. |
| Para que serve? | Comparar incidência acumulada em maturidades equivalentes. |
| Use quando... | Originação, referência, contrato, MOB e evento estiverem semanticamente definidos. |
| Evite quando... | Snapshots faltantes forem confundidos com não-evento ou quando se pretende extrapolar uma safra ainda imatura. |
| Precisa de... | pandas, NumPy e Plotly já no import (via `theme_plotly`). |
| Entrega... | Tabela de vintage, figuras Plotly e comparação de checkpoints. |

Consulte a [implementação](vintage_analysis.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_vintage_analysis.py).

## 1. O que é?

Uma safra reúne contratos originados no mesmo mês ou trimestre. MOB mede diferença em meses entre originação e referência, ou usa uma coluna fornecida pelo consumidor.

`build_vintage_table` transforma snapshots por contrato em incidência acumulada por safra e MOB. `plot_vintage_curves`, `plot_vintage_heatmap` e `compare_safras` consomem essa tabela.

## 2. Que problema este recurso resolve?

Comparar carteiras no calendário mistura contratos com maturidades diferentes. O helper alinha pelo tempo de vida para que, por exemplo, MOB 6 de janeiro seja comparado a MOB 6 de março.

Também evita uma armadilha importante: ausência de snapshot não é automaticamente não-evento. Células parcialmente observadas ficam com `taxa_acumulada=NaN`.

## 3. Quando faz sentido usar?

Use em inadimplência, churn ou outro evento acumulável ao longo da vida de uma coorte quando existe identificador de contrato e snapshots longitudinais.

O helper suporta safra mensal ou trimestral e pode receber MOB já calculado.

## 4. Quando não usar?

Não use para comparar safras em idades diferentes como se fossem equivalentes. Não use a última taxa disponível de uma safra recente como estimativa automática da taxa final.

Não use se a estrutura dos dados não representa snapshots por contrato/MOB de forma coerente. Duplicidades são colapsadas por máximo do evento, o que é uma política específica e precisa fazer sentido no domínio.

## 5. Como funciona, intuitivamente?

Se `mob_col` não for informado, o MOB é diferença de ano/mês entre `dt_referencia` e `dt_originacao`. Snapshots com MOB negativo ou nulo são removidos. O target precisa ser binário.

Para cada contrato/MOB, duplicidades viram uma linha usando máximo do evento. Se `target_is_cumulative=False`, o helper aplica `cummax` por contrato para representar “evento já ocorreu até aqui”. Se `True`, exige que o target acumulado nunca diminua.

A taxa só é publicada quando `n_contratos_observados == n_contratos_safra` naquele MOB.

## 6. Exemplo de situação

Uma safra de janeiro tem 200 contratos e todos possuem snapshot até MOB 6. Se 46 já tiveram evento até esse ponto, `taxa_acumulada=46/200`.

Se uma safra de maio tem 200 contratos mas apenas 150 possuem snapshot de MOB 6, a implementação mantém `cobertura_observada=0,75` e a taxa acumulada fica `NaN`; não presume que os 50 ausentes sejam não-eventos.

## 7. O que você precisa antes de usar?

Valide identidades antes de construir a tabela; estas verificações não são impostas pelo wrapper:

```python
assert df["id_contrato"].notna().all()
assert df.groupby("id_contrato")["dt_orig"].nunique(dropna=False).eq(1).all()
assert df["dt_orig"].notna().all()
```

Normalize datas antes de comparar. IDs nulos podem ser descartados pelo agrupamento; um mesmo ID com origens diferentes pode entrar em safras distintas. Quando houver base-mestra de contratos, confronte IDs/safras e denominadores com ela, incluindo contratos sem nenhum snapshot válido. Não reescreva a origem para forçar consistência.

Devem existir `contract_id`, datas de originação e referência e target. Mesmo quando `mob_col` é fornecido, **as duas colunas de data continuam obrigatórias** pelo contrato atual.

Datas são convertidas com `pd.to_datetime`. MOB deve ser finito, não negativo e inteiro após filtragem. Target não pode ter nulos e deve conter apenas 0/1 nas observações remanescentes.

## 8. O que este recurso entrega?

A tabela contém `safra`, `mob`, `n_contratos_observados`, `n_eventos_acumulados`, `n_contratos_safra`, `taxa_acumulada`, `cobertura_observada` e o alias `taxa`.

`plot_vintage_curves` e `plot_vintage_heatmap` devolvem figuras Plotly. `compare_safras` produz uma linha por safra com taxa em checkpoints e diferença para a média entre safras disponíveis naquele checkpoint.

## 9. Como usar este recurso no Hub?

Com `theme` já obtido pela [resolução de tema](../../visual/tema/README.md) e compatível com notebook/light:

```python
from hub_snippets.ml.vintage_analysis import (
    plot_vintage_curves_resolvido, plot_vintage_heatmap_resolvido,
)
curvas = plot_vintage_curves_resolvido(tabela, theme, max_mob=12)
cobertura = plot_vintage_heatmap_resolvido(tabela, theme, metric="cobertura_observada")
```

Figuras são retornadas em memória; salvar/publicar exige uma ação separada.

```python
from hub_snippets.ml.vintage_analysis import build_vintage_table, compare_safras

tabela = build_vintage_table(
    df,
    contract_id="id_contrato",
    dt_originacao="dt_orig",
    dt_referencia="dt_ref",
    target="evento",
    mob_col="mob",
)
comparacao = compare_safras(tabela, mob_checkpoints=[3, 6, 12])
```

O módulo opera em pandas. Se a origem é Spark, reduza o volume deliberadamente antes de coletar.

## 10. Decisões e configurações que mais importam

`target_is_cumulative` define se o target recebido já é acumulado. Com `False`, qualquer evento observado em um MOB permanece como evento acumulado nos snapshots posteriores existentes. Com `True`, diminuições são rejeitadas.

`safra_grain` define mês ou trimestre. `max_mob` limita apenas a visualização. `top_n_safras` escolhe safras recentes segundo a ordenação textual das chaves produzidas pelo próprio helper.

## 11. Limitações, riscos e armadilhas

O heatmap multiplica `metric` por 100 e rotula `%`, sem verificar sua unidade. Use somente proporções 0–1, como `taxa_acumulada` ou `cobertura_observada`; passar contagens apresenta percentuais falsos. Célula parcial existente pode ter `NaN`, mas MOB totalmente ausente não produz sequer uma linha. As curvas podem ligar MOBs separados e o `pivot_table` do heatmap pode eliminar eixos inteiramente nulos. Reveja a grade e a cobertura antes de interpretar continuidade ou ausência de cor.

A definição de “coorte completa” usa contratos que sobreviveram ao filtro de MOB válido. O helper não possui base-mestra externa para recuperar contratos ausentes de todos os snapshots válidos.

Ele também não fabrica snapshots intermediários. Um contrato observado em MOB 5 e MOB 7, mas ausente no 6, reduz a cobertura da célula MOB 6; a implementação não carrega o último estado para preencher a lacuna.

`compare_safras` calcula `vs_media` com as safras que têm valor não nulo em cada checkpoint; isso não é benchmark causal nem ajuste de composição.

## 12. Quais são as alternativas?

[kaplan_meier](../kaplan_meier/README.md) trata tempo até evento e censura individual. O vintage é mais natural para leitura por coorte/MOB. [survival_cox](../survival_cox/README.md) adiciona covariáveis sob modelo de hazard.

Para projeção de safras imaturas, seria necessário um modelo de maturação explicitamente validado; este helper não o implementa.

## 13. Como saber se o resultado faz sentido?

Confirme que `taxa_acumulada` não diminui nas células completas de uma mesma safra, que `cobertura_observada` fica entre 0 e 1 e que taxa nula não está sendo confundida com zero.

Escolha contratos individuais e reconstrua manualmente MOB/evento acumulado. Compare safras apenas no mesmo checkpoint de maturidade.

## 14. Arquivos relacionados e próximos passos

A [implementação](vintage_analysis.py) constrói tabela, curvas, heatmap e comparações; a [fachada](__init__.py) também reexporta constantes visuais por compatibilidade; o [notebook](exemplo_vintage_analysis.py) demonstra a diferença entre somar taxas e contar contratos afetados.

Depois da tabela, documente política para safras incompletas e critérios de comparação antes de transformar diferenças em decisão.

## 15. Referências

As definições de safra, MOB, população observada e taxa seguem o contrato local descrito neste guia. Critérios de comparação e eventual projeção de safras imaturas precisam de validação própria.