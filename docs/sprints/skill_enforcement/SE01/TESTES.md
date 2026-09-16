# SE01 — testes

## 1. Gates da árvore candidata final

Os comandos canônicos da SE01 são:

```powershell
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/tests/test_skill_enforcement_se01.py
python tools/validate_assistant.py
python tools/render_simulado.py --write
python tools/validate_assistant.py --conferir-readme
python tools/ci_local.py --verbose
```

`Novo_Ambiente_Simulado/` é derivado. A única forma admitida de rematerialização é `python tools/render_simulado.py --write`; edição manual do derivado não é evidência válida.

O workflow dedicado `Skill Enforcement SE01` executa, em runner GitHub real, o validator, a suíte dirigida, `validate_assistant.py`, o renderer, um `git diff --exit-code` sobre o derivado e `validate_assistant.py --conferir-readme`. Ele é evidência de CI, não substituto retórico para um comando que não tenha sido executado.

## 2. Matriz automatizada vigente

A suíte `tools/tests/test_skill_enforcement_se01.py` contém 14 casos. Ela cobre:

| Caso | Resultado esperado |
|---|---|
| contrato canônico v0.1 | PASS |
| schema ↔ validator | vocabulários coerentes |
| helper/módulo inexistente | `RESOURCE_MODULE_NOT_FOUND` |
| símbolo fora da API pública | `RESOURCE_SYMBOL_NOT_EXPORTED` |
| template ausente | `TEMPLATE_NOT_FOUND` |
| `schema_version` não suportada | `SCHEMA_VERSION_UNSUPPORTED` |
| resource duplicado | `RESOURCE_DUPLICATE` |
| condição fora do vocabulário | `CONDITION_INVALID` |
| skill divergente da pasta | `SKILL_FOLDER_MISMATCH` |
| `mode="enforce"` na SE01 | `MODE_INVALID` |
| API pública do index generator | `hub_snippets.visual.index_generator.gerar_indice_eda` |
| probe temporário aposentado | fonte e seção temporária ausentes |
| publicador com notebook já materializado | não reenviar desnecessariamente |
| fallback do publicador | SOURCE preservado quando necessário |

## 3. Resultado atual do gate dirigido

Na composição reconciliada de 16/09/2026, o workflow dedicado observou:

- contrato v0.1: **PASS — 1/1**;
- recursos: **10**;
- templates: **4**;
- suíte SE01: **14/14 PASS**;
- `validate_assistant.py`: **APROVADO — 0 falhas / 0 avisos**;
- renderer: **550 arquivos renderizados**;
- `git diff --exit-code -- Novo_Ambiente_Simulado`: **PASS** depois da materialização canônica;
- snapshot medido: **1501 arquivos / 1979 links**;
- `validate_assistant.py --conferir-readme`: passou depois da atualização do bloco raiz.

A execução intermediária que mediu `1501/1979` reprovou somente porque o README ainda continha `1490/1978`. Ela permanece `failure` histórica e não foi reclassificada. A execução seguinte, com o snapshot corrigido, concluiu o workflow dedicado em `success`.

## 4. Capability probe — procedimento histórico, não gate vigente do produto

Durante a fase experimental, o teste local e o teste no Databricks Free usavam o marcador:

```json
{
  "marker": "SEF_CAPABILITY_PROBE_V0_1",
  "status": "PASS",
  "sample_result": "1.234",
  "writes_performed": false
}
```

O prompt histórico no Genie Code foi:

```text
@hub-ml-eda-profissional Execute somente o capability probe SE01 da própria skill, sem iniciar a EDA. Use o script relativo scripts/capability_probe.py e retorne integralmente o marcador JSON produzido. Não reimplemente o probe.
```

O Run 1 real produziu `PASS` após recuperação do JSON bruto no canvas. A cópia textual isolada havia perdido o conteúdo rico como `canvascanvas`; por isso a observabilidade textual inicial foi `NOT_OBSERVABLE` e a evidência do canvas complementou o mesmo run.

Esse procedimento está congelado como histórico. O script temporário e sua seção foram removidos do produto final, e a suíte atual protege essa aposentadoria em vez de voltar a executar o probe.

## 5. Regressão natural histórica SE00-P1

Depois do probe, foi executado em chat novo o prompt natural congelado:

```text
Faça uma EDA profissional da tabela samples.nyctaxi.trips. Avalie estrutura e qualidade dos dados, nulos, estatísticas descritivas, distribuições, relações e correlações quando aplicáveis, possíveis outliers e achados relevantes. Organize o trabalho de forma eficiente para Databricks/Spark, evite computação redundante e finalize com um resumo executivo dos principais achados, limitações e próximos passos.
```

Resultado histórico: `PASS — nenhuma degradação material atribuível ao contrato/probe`.

Esse PASS não é enforcement. A execução ainda omitiu/reimplementou recursos e não provou consumo individual dos templates; os detalhes permanecem em `RESULTADOS.md`.

## 6. Publicação histórica no Databricks Free

A candidata `637a4b38178c63ffee12ece801e847eedd83a054`, que ainda continha o probe experimental, foi publicada e verificada por conteúdo:

- dry-run: PASS;
- arquivos publicáveis: 550;
- 14/14 skills;
- 5/5 diretórios `hub_`;
- conteúdo: 550/550;
- ausentes: 0;
- obsoletos: 0 após remoção controlada de resíduo SE00;
- resultado final: `APROVADO — 0 problema(s)`.

Essa é evidência histórica da experimentação. A retirada do probe não apaga nem reclassifica esse teste.

## 7. Critério para revalidação remota

A retirada do probe é uma redução de pacote já coberta por:

- teste automatizado de aposentadoria;
- renderer canônico;
- equivalência fonte ↔ simulado;
- validação estrutural;
- CI da árvore final.

Nova publicação no Free só é necessária se houver necessidade objetiva de certificar o pacote remoto sem o instrumento histórico. Ela não é executada automaticamente apenas para apagar a evidência do experimento anterior.

## 8. Classificação de evidências

- `PASS`: comando/teste executou e satisfez o critério observado;
- `FAIL`: comando/teste executou e reprovou;
- `BLOCKED`: execução necessária não pôde ocorrer por bloqueio externo/material;
- `NOT_OBSERVABLE`: não há evidência suficiente para classificar como PASS ou FAIL.

Runs intermediários continuam vinculados ao commit em que ocorreram. Nenhum failure histórico é convertido retroativamente em PASS.

## 9. Escopo negativo dos testes

Nenhum teste da SE01 deve provar ou simular como já implementado:

- preflight definitivo;
- runner determinístico;
- Execution Receipt;
- postflight;
- fail-closed runtime;
- `mode="enforce"`;
- SE02.

Esses itens permanecem fora da sprint.