# Regra — Free Edition vs. workspace do trabalho

Dois ambientes com papéis distintos. Nunca trate "passou no Free" como "validado
para o trabalho" sem conferir esta matriz.

| Dimensão | Databricks Free (laboratório) | Trabalho (Azure Databricks) |
|---|---|---|
| Acesso | CLI configurada nesta máquina | **sem CLI**; outro computador; cópia manual |
| Compute | somente serverless, Python/SQL | conforme políticas do workspace |
| Dados | **somente sintéticos** — nunca dados reais do banco | dados reais, governados |
| Publicação | `tools/publicar_free.py` (ADR-0005; conferência no ADR-0008) | runbook de cópia manual |
| Valida | estrutura das skills, descoberta/`@menção`, código Spark serverless, forward tests | runtime real, permissões, Unity Catalog, dados reais |
| Não valida | jobs permanentes, serving, políticas corporativas, ACLs | — |

## Diferenças de runtime já observadas

Registradas a partir da execução no laboratório (Spark 4.1 serverless, 2026-08-13):

| Comportamento | Free (serverless) | Trabalho (compute conforme política) |
|---|---|---|
| `cache()` / `persist()` | **bloqueado** (`NOT_SUPPORTED_WITH_SERVERLESS`) | disponível em compute clássico |
| `spark.conf.get` de config de cluster | bloqueado | normalmente disponível |
| Bibliotecas ML opcionais (LightGBM, XGBoost, CatBoost, Optuna, PyTorch, SHAP, UMAP, lifelines, Prophet, pmdarima, TabNet, tabulate) | ausentes do runtime, mas **instaláveis por `%pip` na sessão** — as 12 foram exercitadas com chamada real em 2026-08-17 | confirmar disponibilidade e política de instalação |
| Instalar pmdarima + shap + umap-learn na mesma sessão | **quebra o `import numpy` do notebook**; isoladas, as três funcionam | não verificado |
| Variável global `spark` dentro de módulo importado | inexistente (vale nos dois) | inexistente |
| Abrir run do MLflow (`start_run`, `set_experiment`) | Chamada implícita bloqueada em 2026-08-17 e reproduzida em 2026-09-29: o `MlflowClient` lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config. Em 2026-09-29, `mlflow.set_registry_uri("databricks")` e nome absoluto do experimento na home permitiram três runs sintéticas completas. | confirmar configuração conforme compute/política |
| `tabulate` (exigido por `DataFrame.to_markdown()`) | ausente | confirmar |
| `jinja2` (exigido por `DataFrame.style`) | ausente | confirmar |
| API clássica de `pyspark.ml` (`VectorAssembler`, `Correlation.corr`) | **bloqueada** — o Spark Connect não expõe essas classes da JVM | disponível em compute clássico |
| Chat do Genie Code | tem **orçamento próprio**, que esgota sozinho e trava até a virada do mês — sem afetar compute nem workspace | limite é política corporativa, não cota mensal pessoal |

Os helpers foram ajustados para funcionar nos dois casos: degradam sem cache no
serverless e mantêm o cache onde ele existe.

### Instalar biblioteca no serverless: o que vale hoje

`%pip install` na primeira célula, seguido de `%restart_python`, **funciona**.
Custa de 200 a 280 segundos de job. Três bibliotecas exigem pin — `shap==0.44.1`,
`umap-learn==0.5.5` e `pmdarima==2.0.4` (esta com `numpy==1.23.5` junto) — e as
outras nove resolvem sozinhas. Instale **uma por notebook**: as três da lista de
pin, juntas na mesma sessão, derrubam o `import numpy`.

O inventário completo, com a prova de execução de cada uma, está em
`ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt`.

### O orçamento do assistente esgota separado do resto

Observado em **18/08/2026**: `Budget reached. Contact your admin to resume.
Resets Sep 1.` — no chat do Genie Code, com **quatorze dias** de bloqueio.

O que caiu e o que não caiu, medido e não suposto:

| Capacidade | Estado | Como foi medido |
|---|---|---|
| Chat do Genie Code | ❌ bloqueado | a própria mensagem |
| Compute (job, notebook, smoke test) | ✅ funciona | job submetido entra em `RUNNING` e termina `SUCCESS` |
| Workspace (ler, escrever, publicar, conferir) | ✅ funciona | `mkdirs` + `delete` + `export` com `exit=0` |

Consequência de planejamento: o corte é limpo e cai numa fronteira útil. **Tudo
que passa por conversa com o assistente para; tudo que passa por arquivo ou por
compute segue.** Forward tests e qualquer tarefa que dependa de resposta do Genie
ficam bloqueados; o ciclo editar → validar → renderizar → publicar → conferir
continua inteiro, e job de execução também.

Antes de planejar sprint que dependa do assistente, confira o orçamento. E não
suponha o alcance de um bloqueio: meça, porque as três capacidades acima têm
cotas diferentes.

### O runtime do Free muda sem aviso

A linha do MLflow acima é o caso documentado: `docs/testes/spark/resultados/`
registra `mlflow_run.completo` como **"run completo aceito"** em **14/08/2026**,
e em **17/08/2026**, no mesmo tipo de compute, o mesmo caminho falha na abertura
do run. O registro de 14/08 não está errado — descreve o que era verdade então.
Em 29/09/2026, a configuração explícita do registry URI e um experimento com
caminho absoluto na home fizeram três runs MM06 sintéticas terminarem completas
no Free; isso não comprova outro runtime nem o uso implícito sem configuração.

O movimento contrário também aconteceu no mesmo dia: `prophet` estava registrado
como **"sem combinação funcional conhecida"**, por não inicializar o backend de
inferência, e em 17/08 instalou e ajustou um modelo completo. E o aviso de que
instalar sem fixar versão derrubava o kernel não se reproduziu.

Consequência prática: **"foi testado" tem data de validade em ambiente
gerenciado**. Antes de replicar no trabalho, reexecute; não confie no registro
sozinho, por mais recente que pareça.

## Guardrails

- Nenhum dado real, tabela real, path corporativo ou identificador do banco entra
  no Free nem neste repositório. Fixtures sintéticas sempre.
- Publicação no Free é dry-run por padrão; `--execute` é gate consciente.
- Toda diferença de comportamento encontrada entre Free e trabalho vira nota na
  matriz acima (atualize esta regra) e entrada no CHANGELOG.
- No trabalho, o username muda (placeholder `<username-trabalho>`): a replicação
  usa o runbook, nunca busca/substituição improvisada.
