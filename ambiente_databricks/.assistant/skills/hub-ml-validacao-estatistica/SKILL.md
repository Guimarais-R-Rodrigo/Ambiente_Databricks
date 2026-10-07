---
name: hub-ml-validacao-estatistica
description: Planeja e executa validação estatística no Databricks para qualidade, pressupostos, regressão/econometria, séries temporais, ML tabular, deep learning e inferência, com amostragem controlada, effect size, intervalos, múltiplos testes e prescrições. Usar quando pedirem testes estatísticos, hipótese/p-valor, normalidade, homocedasticidade, VIF, ADF/KPSS, drift, power, comparação de grupos, pressupostos de modelo ou diagnóstico estatístico de dataset/notebook.
---

# Validar estatisticamente

## Quando esta skill se aplica

- Pedem **teste estatístico, hipótese, p-valor, normalidade, homocedasticidade,
  VIF, ADF/KPSS, power, comparação de grupos** ou pressupostos de modelo.
- A pergunta exige **decisão com incerteza declarada**, não descrição.

**Não cobre:** descrever a base (`hub-ml-eda-profissional`) nem calcular PSI para
acompanhar modelo em produção (`hub-ml-monitoramento-modelo`), onde o limiar vem
de política e não de teste.

## Execução verificável do perfil KS

Para uma comparação diagnóstica de **duas amostras independentes** com variável
numérica contínua e hipótese bicaudal pré-registrada, use a rota canônica
[preflight.py](scripts/preflight.py) → [run.py](scripts/run.py) →
[verify.py](scripts/verify.py). O contrato fechado está em
[input.schema.json](input.schema.json) e [execution_contract.json](execution_contract.json).
Exemplo sintético e comandos: [scripts/README.md](scripts/README.md).
Ao usar a CLI, capture o stdout JSON do runner em arquivo próprio e passe-o
como `--payload` a `verify.py`, junto com request, run_id e oráculo independente.
Confirme o JSON `valid=true` **e** o código de saída zero. Rodar o arquivo
sem payload ou receber stdout vazio não executa/comprova a função `verify()`.

O perfil piloto aceita **somente dados realmente sintéticos fornecidos inline**.
`synthetic: true` declara a origem dos dados, não o formato do request: coletar,
limitar ou agregar dados reais de uma tabela não os torna sintéticos. Quando a
origem não for informada, confirme-a antes de montar o request. Dados reais
ficam fora deste perfil executável; ofereça planejamento e aponte a lacuna, sem
usar uma chamada manual como substituta da rota protegida. A orientação genérica
de coleta em Spark abaixo não amplia o escopo deste piloto. Peça o `alpha` já
pré-especificado quando ausente; `0,05` só pode ser proposto para confirmação
antes de olhar os dados, nunca aplicado como default silencioso.

O perfil `TWO_SAMPLE_KS_PILOT_V1` chama
`hub_snippets.ml.drift_detection.calculate_ks` e emite a estatística KS D
como tamanho de efeito e o p-valor do SciPy. A declaração de independência,
amostragem i.i.d. e continuidade é uma **pré-condição fornecida pelo usuário**;
o código apenas rejeita empates no vetor recebido, sem certificar o desenho
amostral. A comparação única pré-registrada tem multiplicidade não aplicável,
com motivo expresso no request. O perfil não calcula intervalo de confiança;
`confidence_interval_status=UNSUPPORTED_IN_PROFILE` não deve ser preenchido
por estimativa inventada. Falha em rejeitar H0 não demonstra equivalência.

A execução só pode ser descrita como **candidata local verificável** quando
`run.status=PASS`, o Receipt V1 verifica a release/request/run e o oráculo
independente confere D, p e decisão. O verificador recebe request, run_id e
oráculo de fonte confiável externa ao payload. `VALID` não autoriza promoção
de policy, conclusão de negócio, publicação ou homologação Genie. Para
Welch/Mann-Whitney, pares, séries, regressão, múltiplas comparações e IC,
a skill continua oferecendo planejamento; não reivindique essa rota executável.

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

Evitar limiares universais. Um p-valor pequeno não mede magnitude, probabilidade de H0 nem relevância de negócio. Não inferir potência do p-valor, da não rejeição ou de N isolado: qualificá-la como baixa/alta exige alternativa, desenho, alfa e cálculo ou simulação específicos. Amostra pequena limita resolução, mas `p=1` não demonstra equivalência nem potência quase nula. Power pós-hoc baseado apenas no efeito observado costuma adicionar pouca informação; priorizar intervalo de confiança e planejamento a priori.

## Prescrever ações proporcionais

- Separar falha de dado, violação de pressuposto e ausência de evidência.
- Propor transformação, método robusto, reamostragem, modelo hierárquico ou coleta adicional somente quando ligada ao diagnóstico.
- Não ordenar remoção de feature ou retreino automaticamente por um único teste.
- Registrar risco residual e critério de aceite.

Usar [templates/severity_rubric.md](templates/severity_rubric.md) como linguagem customizada e calibrar ao risco real. Usar [templates/test_result_card.md](templates/test_result_card.md) para resultados individuais e [templates/relatorio_diagnostico.md](templates/relatorio_diagnostico.md) para consolidação.

## Estruturar o notebook

Usar [templates/notebook_output_stat.md](templates/notebook_output_stat.md) como estrutura editável, mas adaptar imports às funções realmente existentes no pacote de snippets e à pasta customizada instalada. Não assumir que helpers visuais fazem parte do Databricks.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO_V2.md#catalogo-helpers](../../MANUAL_TECNICO_V2.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Amostragem controlada e reprodutível | `hub_snippets.spark.smart_sample` |
| KS, PSI e CSI driver-side sobre amostra | `hub_snippets.ml.drift_detection` |
| PSI/CSI nativo em escala | `hub_snippets.spark.psi_calculator` |
| Qualidade prévia (nulos por coluna) | `hub_snippets.spark.null_summary` |
| Formatação numérica da narrativa | `hub_snippets.constants.format_br` |

Os helpers entregam a estatística, não a decisão: classificação de severidade exige limite calibrado para a população e o risco em questão.

## Validar a conclusão

1. Recalcular amostra de resultados por método independente quando material.
2. Testar edge cases: grupo vazio, uma classe, variância zero, N pequeno, nulls e divisão por zero.
3. Confirmar que a conclusão segue o estimando e não somente o p-valor.
4. Separar evidência estatística, julgamento de negócio e exigência regulatória.
5. Entregar plano, código reproduzível, resultados, limitações e próximas ações.
## O que nunca fazer

- **Escolher o teste depois de ver o resultado.** A decisão vem antes do dado.
- **Reportar p-valor sem effect size.** Com amostra grande, tudo é significante e
  quase nada é relevante.
- **Testar pressuposto e seguir mesmo assim** sem dizer o que muda na conclusão.
- **Ignorar múltiplas comparações.** Sob vinte nulas verdadeiras e testes de
  tamanho 5%, o número esperado de falsos positivos é um; isso não garante
  um achado. A probabilidade `1−0,95^20≈64%` exige testes independentes.
  Sem dependência conhecida, não atribua essa probabilidade à família;
  correção de multiplicidade não converte escolha pós-hoc em teste confirmado.
- **Usar a API clássica de `pyspark.ml`** — `VectorAssembler` e `Correlation.corr`
  estão bloqueados sob Spark Connect no Free.

## Formato de saída

Um card por teste: pergunta, teste escolhido e por quê, pressupostos conferidos,
estatística, p-valor, effect size e intervalo de confiança quando calculado e suportado pelo perfil, e a **prescrição** — o que fazer com o resultado ou qual evidência ainda obter.

No piloto `TWO_SAMPLE_KS_PILOT_V1`, reportar D como tamanho de efeito e `confidence_interval_status=UNSUPPORTED_IN_PROFILE`. Não preencher IC, N, alfa, p-valor ou pressupostos com valores inventados para completar o card. Preservar a distinção entre desenho declarado pelo usuário e pressuposto efetivamente verificado. Nos campos sem evidência, indicar pendência; quando não aplicáveis ou não suportados, explicar o motivo.

Perguntas conceituais podem receber contas ilustrativas identificadas, sem alegar execução canônica. O plano, a hipótese e o resultado observado devem permanecer separados. A prescrição pode ser obter a entrada faltante; não exige uma conclusão estatística sem suporte.
