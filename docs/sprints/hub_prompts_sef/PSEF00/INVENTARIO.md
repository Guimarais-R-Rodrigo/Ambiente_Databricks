# PSEF00 — inventário de Hub Prompts

**Snapshot:** `main@17640a6a31f562e9979d235ede27cf44cef9ebbf`.

## Contagem

| Item | Quantidade |
|---|---:|
| Famílias | 16 |
| README raiz | 1 |
| READMEs locais | 16 |
| Briefings `.md` | 16 |
| Notebooks `exemplo_*.py` | 16 |
| **Arquivos totais** | **49** |

Os 65 entries observados no Git tree para o prefixo incluem também os 16 objetos `tree` das pastas; a contagem de arquivos úteis/blobs é 49.

## Arquivos por família

| Família | README blob | Briefing blob | Exemplo blob | Escrita persistente no exemplo | Aviso local explícito |
|---|---|---|---|---:|---|
| `auditoria_skills` | `f96d30c78c…` | `98c29b5056…` | `9eac17b145…` | 0 | não aplicável |
| `baseline_orchestration` | `d2548b9986…` | `89e27ab8f6…` | `3229001c67…` | 1 | sim |
| `comentar_notebook` | `f3dbf92288…` | `e9168feaea…` | `f3d79284ca…` | 0 | não aplicável |
| `comparar_tabelas` | `c62a8a86d8…` | `e712c42f22…` | `56eab98264…` | 2 | sim |
| `cross_eda` | `fa9f43e8ae…` | `8c02def03f…` | `f6f6709628…` | 2 | sim |
| `data_quality` | `f2f1f49881…` | `e131618df0…` | `e9dde2a5cb…` | 1 | sim |
| `eda_completa` | `b9e2460c4a…` | `93485426b1…` | `37fd1ab232…` | 1 | sim |
| `eda_rapida` | `ba506264e6…` | `deb5f22a97…` | `72c94eac6c…` | 1 | sim |
| `explainability` | `46a2bbd9c1…` | `9d71e58b0c…` | `bbc078f070…` | 1 | sim |
| `feature_engineering` | `824ad8e6bd…` | `be4e2c0b48…` | `798da6bc9b…` | 2 | sim |
| `monitoramento_modelo` | `a3e8998f5d…` | `ba79225b44…` | `7835ffd1cb…` | 2 | sim |
| `novo_projeto` | `e89a5ba3a4…` | `fad042b28c…` | `8a9456b4cc…` | 1 | **não** |
| `pipeline` | `faa5104baf…` | `1d751078f0…` | `3432163815…` | 1 | sim |
| `safra` | `ad8851d7fd…` | `b0b4520bd3…` | `3e3023f0ca…` | 1 | sim |
| `stat_check` | `1855a817ba…` | `ff5952a016…` | `5f29e60d66…` | 1 | sim |
| `tutor_explicar` | `8ef3638d5b…` | `7fbc05764e…` | `d20823f6d4…` | 0 | não aplicável |

README raiz: `ambiente_fonte/.assistant/hub_prompts/README.md`, blob `74f37ffe0a03fc9425eca56a6bc99204a12124bd`.

## Efeito operacional dos exemplos

Treze das dezesseis famílias possuem escrita `mode("overwrite").saveAsTable(...)` no preparo sintético. As três sem escrita persistente são `auditoria_skills`, `comentar_notebook` e `tutor_explicar`.

Doze dos treze READMEs de famílias com escrita já alertam explicitamente sobre esse efeito. `novo_projeto` é a exceção: o notebook escreve `workspace.default.hub_exemplo_clientes`, mas o README local não contém o alerta correspondente.

Todos os notebooks auditados separam textualmente o preparo da interação com o assistente (`Prompt não executa`/`NÃO EXECUTADO — depende de uma pessoa`). Portanto, a escrita do exemplo não constitui por si só evidência de execução do prompt nem de bypass SEF.

## Fonte e derivado

`ambiente_fonte/` é a fonte editável. `Novo_Ambiente_Simulado/` não foi editado nem usado como fonte de verdade. A PSEF00 não requer renderer porque nenhum arquivo da fonte operacional foi alterado.

## Referência de plataforma revalidada

`/findTables` aparece em `eda_rapida.md` e no README raiz. A investigação PSEF00 verificou que o comando continua documentado pela Databricks em setembro de 2026 como slash command do Genie Code para localizar tabelas. Fonte oficial: [Get coding help from Genie Code](https://docs.databricks.com/gcp/en/notebooks/code-assistant), seção de slash commands. Logo, a referência não é classificada como legada e não deve ser removida com base no achado candidato original.
