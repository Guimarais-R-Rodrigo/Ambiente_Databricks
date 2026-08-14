---
name: rodrigo-validacao-estatistica
description: Planeja e executa validação estatística no Databricks para qualidade, pressupostos, regressão/econometria, séries temporais, ML tabular, deep learning e inferência, com amostragem controlada, effect size, intervalos, múltiplos testes e prescrições. Usar quando pedirem testes estatísticos, hipótese/p-valor, normalidade, homocedasticidade, VIF, ADF/KPSS, drift, power, comparação de grupos, pressupostos de modelo ou diagnóstico estatístico de dataset/notebook.
---

# Validar estatisticamente

## Definir a decisão antes do teste

Registrar:

- pergunta e decisão suportada;
- população, unidade e desenho amostral;
- variáveis, target e grupos;
- período/data de corte;
- estimando ou pressuposto;
- nível de significância e correção de múltiplos testes;
- efeito mínimo relevante;
- modo diagnóstico ou inferencial.

No modo diagnóstico, usar testes como evidência entre outras; no inferencial, exigir desenho, independência e estimando defensáveis.

## Criar um plano de testes

Para cada teste, declarar:

| Campo | Conteúdo |
|---|---|
| Pergunta | hipótese científica/operacional |
| H0/H1 | formulação antes de ver o resultado |
| Estatística | teste e versão |
| Pressupostos | independência, distribuição, tamanho, censura etc. |
| Amostra | regra, seed, N e motivo |
| Efeito | métrica e limite relevante |
| Multiplicidade | família de testes e correção |
| Decisão | como o resultado altera a ação |

Usar [templates/test_plan.md](templates/test_plan.md) e [templates/decisao_pressupostos.md](templates/decisao_pressupostos.md) conforme necessário.

## Preparar os dados

1. Validar schema, chave, unidade e duplicidade.
2. Quantificar missing e padrão por grupos/tempo.
3. Limitar a análise ao período permitido.
4. Fazer agregações no Spark.
5. Coletar para scipy/statsmodels apenas amostra ou resultado pequeno com limite e seed.
6. Preservar pesos/estratos quando o desenho exigir.
7. Evitar pseudorreplicação: agrupar ou modelar dependência por entidade/tempo.

Não inferir MCAR/MAR/MNAR apenas de uma taxa de missing. Não interpretar falha em rejeitar H0 como prova de equivalência.

## Selecionar a suite

### Core de qualidade

Usar conforme relevância: unicidade da chave, missing, cardinalidade, near-zero variance, redundância, imbalance e cobertura temporal. Não executar todos por ritual.

### Regressão/econometria

Avaliar resíduos, especificação, multicolinearidade, heterocedasticidade e dependência temporal com testes/plots compatíveis. Normalidade dos preditores não é requisito geral de regressão linear; o alvo diagnóstico usual envolve resíduos e inferência. VIF não determina remoção automática.

### Séries temporais

Combinar ADF e KPSS quando útil, declarar componentes determinísticos e lags. Avaliar resíduos com Ljung-Box/ARCH e validação fora da amostra. Não confundir estacionariedade da série com adequação do forecast.

### ML tabular

Avaliar leakage, shift entre splits, estabilidade, calibração, sinal e robustez por segmento. Usar PSI com bins de referência e missing explícito. Usar permutation importance somente no conjunto e métrica corretos.

### Deep learning

Avaliar overlap de entidade, duplicatas cross-split, label noise com método validado, escalas, comprimentos/OOV e drift. Não carregar dataset inteiro no driver.

### Inferência entre grupos

- Dois grupos independentes: Welch t-test ou Mann-Whitney conforme estimando/pressupostos.
- Mais de dois: ANOVA/Welch/Kruskal-Wallis e pós-teste apropriado.
- Categóricas: qui-quadrado ou Fisher conforme contagens e desenho.
- Dados pareados/repetidos: usar teste/modelo pareado, não versão independente.
- Equivalência/não inferioridade: usar desenho e margem específicos; p-valor não significativo não basta.

## Interpretar com rigor

Reportar sempre que aplicável:

- N e distribuição por grupo;
- estimativa e intervalo de confiança;
- estatística, graus de liberdade e p-valor;
- effect size com unidade/interpretação;
- correção de múltiplos testes;
- resultado dos pressupostos;
- sensibilidade/robustez;
- consequência prática.

Evitar limiares universais. Um p-valor pequeno não mede magnitude, probabilidade de H0 nem relevância de negócio. Power pós-hoc baseado apenas no efeito observado costuma adicionar pouca informação; priorizar intervalo de confiança e planejamento a priori.

## Prescrever ações proporcionais

- Separar falha de dado, violação de pressuposto e ausência de evidência.
- Propor transformação, método robusto, reamostragem, modelo hierárquico ou coleta adicional somente quando ligada ao diagnóstico.
- Não ordenar remoção de feature ou retreino automaticamente por um único teste.
- Registrar risco residual e critério de aceite.

Usar [templates/severity_rubric.md](templates/severity_rubric.md) como linguagem customizada e calibrar ao risco real. Usar [templates/test_result_card.md](templates/test_result_card.md) para resultados individuais e [templates/relatorio_diagnostico.md](templates/relatorio_diagnostico.md) para consolidação.

## Estruturar o notebook

Usar [templates/notebook_output_stat.md](templates/notebook_output_stat.md) como estrutura editável, mas adaptar imports às funções realmente existentes no pacote de snippets e à pasta customizada instalada. Não assumir que helpers visuais fazem parte do Databricks.

## Usar helpers da biblioteca

Importar de `x_snippets`/`x_scripts` em vez de reimplementar a lógica. Catálogo completo: [x_docs/catalogo_helpers.md](../../x_docs/catalogo_helpers.md).

| Demanda | Módulo |
|---|---|
| Amostragem controlada e reprodutível | `x_snippets.spark.smart_sample` |
| KS, PSI e CSI driver-side sobre amostra | `x_snippets.ml.drift_detection` |
| PSI/CSI nativo em escala | `x_snippets.spark.psi_calculator` |
| Qualidade prévia (nulos por coluna) | `x_snippets.spark.null_summary` |
| Formatação numérica da narrativa | `x_snippets.constants.format_br` |

Os helpers entregam a estatística, não a decisão: classificação de severidade exige limite calibrado para a população e o risco em questão.

## Validar a conclusão

1. Recalcular amostra de resultados por método independente quando material.
2. Testar edge cases: grupo vazio, uma classe, variância zero, N pequeno, nulls e divisão por zero.
3. Confirmar que a conclusão segue o estimando e não somente o p-valor.
4. Separar evidência estatística, julgamento de negócio e exigência regulatória.
5. Entregar plano, código reproduzível, resultados, limitações e próximas ações.
