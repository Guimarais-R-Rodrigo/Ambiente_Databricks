# Relatório de auditoria e implementação

> **ENTREGA CUSTOMIZADA (`x_delivery`) — não auto-descoberta pela Genie Code.**
> Data: 13 de agosto de 2026 · Plataforma-alvo: Azure Databricks Genie Code

## Resultado

O ecossistema foi reorganizado, corrigido e documentado. As 12 skills pessoais
continuam presentes e agora usam a estrutura oficialmente suportada
`.assistant/skills/<skill>/SKILL.md`. Estruturas não institucionais receberam o
prefixo `x_`, deixando explícito que precisam de `@`/Add context, import ou execução
manual.

Status desta entrega: **aprovada para revisão e testes no workspace de destino**.
Não declarar implantação produtiva concluída antes dos gates de runtime listados ao
final.

## Escopo revisado

| Componente | Resultado |
|---|---|
| `.assistant_instructions.md` fornecido | reescrito e reduzido a 7.371 caracteres |
| Agent Skills | 12/12 preservadas e validadas |
| Prompts | 16 briefings completos, cobrindo as 12 skills e utilitários |
| Contexto de projeto | migrado para modelo `AGENTS.md` oficialmente descoberto |
| Scripts | 7 utilitários revisados/corrigidos |
| Snippets Python | 47 módulos funcionais + pacote/testes revisados |
| Documentação | README raiz, README do ecossistema, manifestos e roadmap sincronizados |
| Segurança editorial | zero paths/e-mails pessoais, PII ou credenciais detectados |
| Integridade | zero links Markdown relativos quebrados; zero mojibake detectado |

## Arquitetura implantável

```text
assistant_optimized_2026-08-13/
├── .assistant_instructions.md           # SUPORTE NATIVO: instruções pessoais
├── .assistant/
│   ├── skills/                          # SUPORTE NATIVO: descoberta de skills
│   │   └── rodrigo-*/SKILL.md           # CONTEÚDO PERSONALIZADO
│   ├── x_prompts/                       # CUSTOM: Add context/@
│   ├── x_projects/                      # CUSTOM: modelos; copiar como AGENTS.md
│   ├── x_scripts/                       # CUSTOM: executar/importar
│   ├── x_snippets/                      # CUSTOM: importar explicitamente
│   ├── x_docs/                          # CUSTOM: documentação/histórico
│   └── x_config/                        # CUSTOM: legado/manual
├── x_delivery/                          # CUSTOM: relatório e handoff
├── .gitignore
└── README.md
```

O prefixo `rodrigo-` identifica skills pessoais; ele não significa skill built-in da
Databricks. O mecanismo de descoberta é nativo, o conteúdo é customizado.

## Achados estruturais corrigidos

### Descoberta e contexto

- Seis skills sem frontmatter passaram a ter `name` e `description` válidos.
- Todas as 12 descrições agora explicam função e gatilhos de uso.
- Skills extensas foram reduzidas com progressive disclosure; os `SKILL.md` ficaram
  entre 64 e 120 linhas.
- Frontmatter deste pacote usa somente `name` e `description` por política
  conservadora local. O padrão Agent Skills admite campos opcionais suportados.
- Prompts, projetos, scripts e snippets deixaram de parecer interfaces nativas e
  foram movidos para diretórios `x_`.
- Memória de projeto foi migrada para `AGENTS_TEMPLATE.md`, que deve ser copiado como
  `AGENTS.md` no diretório ancestral do projeto real.
- Aliases como `/eda` e `/baseline` agora são descritos como convenções humanas. A
  seleção explícita suportada é `@nome-da-skill`; `/findTables` permanece identificado
  como recurso nativo.
- O JSON MCP vazio/legado foi movido para `x_config` e marcado como inativo. MCP deve
  ser configurado em **Genie Code → Settings**.

### Instruções pessoais

- O arquivo fornecido foi renomeado para o nome oficial `.assistant_instructions.md`.
- Contexto muito específico, sprints e memórias históricas foram movidos para
  `x_docs/LEGACY_CONTEXT.md`.
- Foram mantidas preferências úteis: PT-BR, PySpark, Spark SQL, Plotly, MLflow,
  serverless compatível, anti-leakage, qualidade e documentação.
- Foram removidas promessas de hooks, slash commands e memória automática.
- Foram adicionadas fronteiras de escrita, PII, custo, inferência, conformidade,
  MLflow, Unity Catalog, Lakeflow e Declarative Automation Bundles.
- Foi registrada a exceção oficial: instruções não se aplicam a Quick Fix e
  Autocomplete.

### Prompts

Os 11 prompts existentes foram ampliados e cinco prompts antes apenas implícitos
foram adicionados: explicabilidade, monitoramento, pipeline, safras e auditoria.
Todos os 16 incluem:

- campos `{{...}}` e explicação do que preencher;
- contexto por `@`/Add context e skill recomendada;
- briefing, premissas e defaults;
- limites de execução, escrita, custo e PII;
- contrato de saída e validação final;
- exemplo mínimo e follow-ups.

## Correções técnicas principais

### Dados e Spark

- `drift_detector.py`: substituição do falso PSI baseado em média/desvio por PSI de
  distribuição com bins da referência, bucket de ausentes e thresholds opcionais.
- `data_quality_check.py`: aplicação real de `null_warn`, `null_fail` e freshness,
  alertas estruturados e agregação de nulos em uma varredura.
- `quick_profile.py`: uso real da fração de amostragem; separação explícita entre
  estatísticas full-table e sample.
- `rfv_calculator.py`: exclusão de eventos posteriores à data de referência, janela
  inclusiva correta e remoção de default mutável.
- `schema_to_yaml.py`: escaping seguro com PyYAML e fallback JSON válido em YAML 1.2.
- `naming_checker.py`: prefixos passam a ser política configurável, não requisito
  universal da Databricks.
- `safe_display.py`: limite sempre aplicado e contagem limitada, sem scan completo.
- `smart_sample.py`: amostragem estratificada distribuída, limites e tratamento de
  excesso de estratos.
- `date_features.py`: separação entre feriados nacionais fixos e calendário de
  projeto; alias de compatibilidade preservado.
- `psi_calculator.py`: missing explícito, categorias suportadas, sem sentinela `-1`
  silenciosa e interpretação dependente de política calibrada.
- Correlação/distribuição: tipos `decimal(p,s)`, seleção vazia, aliases de API e
  limites no driver corrigidos.

### ML, estatística e monitoramento

- Métricas: validação de shapes/probabilidades/classes, lift para amostra pequena e
  MAPE indefinido quando todos os valores reais são zero.
- Score bands/scorecard: direção de score e de evento adverso explicitadas; ties,
  labels e sinal do logit corrigidos.
- LightGBM/XGBoost/CatBoost/Optuna: tasks/classes validadas, multiclass corrigido,
  early stopping aplicado e MLflow opcional somente quando solicitado.
- Ranking: grupos e labels validados; claim indevido de MAP removido.
- Temporal: splits usam períodos de calendário; lags/rollings podem ser particionados
  por entidade; walk-forward normaliza períodos e usa o target no contrato.
- Vintage: incidência acumulada calculada no nível contrato×MOB, evitando soma
  incorreta de taxas.
- Survival/Cox: validações de duração/evento e retorno real do teste de
  proporcionalidade.
- WOE/IV: target binário, ambas as classes e smoothing consistente.
- SHAP/explicabilidade: AUC não é apresentada como acurácia; importância SHAP não é
  “percentual do poder preditivo” nem causalidade.
- Monitoramento: melhora de métrica não gera alerta; thresholds/direção são política
  explícita; o helper nunca autoriza retreino automático e exige investigação,
  champion-challenger e aprovação.
- Autoencoder/MLP/TabNet: batching, escala de treino, melhor estado restaurado,
  validações de tarefa/categorias e menor risco de memória.
- Clustering/UMAP: algoritmos e parâmetros validados; crashes de formatação e
  cenários vazios corrigidos.

### Segurança e documentação

- Inputs HTML de badges, KPIs e headers são escapados.
- 46 ocorrências de caminhos/identificadores pessoais foram parametrizadas.
- Imports `snippets.*` foram migrados para o pacote válido `x_snippets.*`.
- APIs documentadas foram sincronizadas (`null_summary`, aliases de correlação,
  distribuição e datas).
- Claims regulatórios foram separados de boas práticas e condicionados a fonte
  oficial e revisão de Compliance/Risco.
- A skill de auditoria preserva dois modos: auditoria da implementação da skill e
  auditoria do output gerado contra o contrato da skill produtora.

## Validações executadas

| Validação | Resultado |
|---|---|
| `quick_validate.py` | 12/12 skills aprovadas |
| Tamanho dos `SKILL.md` | 64–120 linhas |
| Links internos das skills | 56 resolvidos |
| Imports `x_snippets` em recursos das skills | 8 verificados |
| Blocos Python em templates das skills | 19 compilados |
| Parsing AST do pacote | 61/61 arquivos Python |
| Testes driver-side | 13/13 aprovados |
| Links Markdown relativos globais | 0 quebrados |
| Cercas Markdown | 0 desbalanceadas |
| UTF-8/mojibake | 0 falhas detectadas |
| PII/paths pessoais | 0 correspondências |
| Tamanho das instruções | 7.371/20.000 caracteres |

Os testes driver-side usaram dependências temporárias isoladas em `work/test_deps`;
essas dependências não fazem parte do pacote implantável.

## Gates pendentes antes de produção

1. Executar testes Spark dos helpers em uma sessão Azure Databricks com o runtime
   alvo.
2. Testar workflows opcionais com versões fixadas de LightGBM, XGBoost, CatBoost,
   SHAP, lifelines, Prophet, PyTorch/TabNet e UMAP.
3. Publicar primeiro no diretório/target de desenvolvimento.
4. Abrir novo chat e executar, para cada skill, casos positivo, negativo e
   `@menção` explícita; hard refresh se o metadata estiver em cache.
5. Validar permissões, PII, escrita, custo e paths do workspace real.
6. Para pipelines/bundles, executar `databricks bundle validate`, testes e smoke
   antes de deploy/run produtivo.

## Fontes oficiais prioritárias

- [Agent Skills na Genie Code — Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções customizadas](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Dicas para Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [MCP na Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp)
- [Lakeflow Spark Declarative Pipelines — melhores práticas](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices)
- [Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
- [MLflow Tracking](https://learn.microsoft.com/en-us/azure/databricks/mlflow/tracking)
- [Models in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/)
- [Agent Skills specification](https://agentskills.io/specification)

## Conclusão

Não restaram achados P0/P1 na auditoria independente após a última correção de
painéis vintage incompletos, métricas de monitoramento ausentes/não finitas, anotação
de lift parametrizada, formatos SHAP multiclass/regressão e multiplicidade em
comparações Kaplan–Meier.
O pacote final exclui caches/bytecode e preserva o manifesto da exportação original
apenas em `x_docs` para rastreabilidade. Os limites remanescentes são ambientais e
estão registrados como gates, sem declaração indevida de execução no Databricks.
