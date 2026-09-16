# SE01 — testes

## 1. Testes estáticos/locais

Comandos previstos na raiz do repositório:

```powershell
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/tests/test_skill_enforcement_se01.py
python tools/validate_assistant.py
python tools/render_simulado.py --write
python tools/validate_assistant.py --conferir-readme
python tools/ci_local.py --verbose
```

O renderer deve ser executado pelo mecanismo canônico. `Novo_Ambiente_Simulado/` não pode ser corrigido manualmente.

## 2. Matriz negativa do contrato

O teste automatizado deve provar rejeição de:

| Caso | Resultado esperado |
|---|---|
| helper/módulo inexistente | `RESOURCE_MODULE_NOT_FOUND` |
| símbolo fora da API pública | `RESOURCE_SYMBOL_NOT_EXPORTED` |
| template ausente | `TEMPLATE_NOT_FOUND` |
| `schema_version` não suportada | `SCHEMA_VERSION_UNSUPPORTED` |
| resource duplicado | `RESOURCE_DUPLICATE` |
| condição fora do vocabulário | `CONDITION_INVALID` |
| skill divergente da pasta | `SKILL_FOLDER_MISMATCH` |
| `mode="enforce"` na SE01 | `MODE_INVALID` |

O teste também fixa explicitamente o caminho público real do `index_generator`: `hub_snippets.visual.index_generator.gerar_indice_eda`.

## 3. O que o teste local do probe prova

O teste local executa o script contra `ambiente_fonte/.assistant` e exige:

```json
{
  "marker": "SEF_CAPABILITY_PROBE_V0_1",
  "status": "PASS",
  "sample_result": "1.234",
  "writes_performed": false
}
```

Isso prova apenas portabilidade Python/read-only do script. **Não prova que o Genie Code escolhe ou executa o script.**

## 4. Estado técnico já observado

No commit `fda26d130e559d3fdb8ee69fcb785ffecc76a049`, o workflow SE01 executou efetivamente e registrou:

- contrato: 1/1 PASS;
- suíte SE01: 11/11 PASS;
- `validate_assistant.py`: 0 falhas / 0 avisos;
- renderer canônico: limpo após materialização do espelho.

O snapshot medido foi 1494 arquivos / 1961 links, posteriormente colado no README raiz.

A rodada de Actions seguinte não obteve runner (`runner_id=0`, `runner_name=""`, `steps=[]`), inclusive em rerun manual de um único job. Portanto, o CI final do HEAD vigente continua pendente; esse evento não substitui teste nem é classificado como regressão funcional.

## 5. Preparação do Databricks Free

Somente depois de fonte/simulado estarem consistentes e com a branch local sincronizada:

```powershell
git status --short
git fetch origin --prune
git switch sef/SE01-contrato
git pull --ff-only origin sef/SE01-contrato
```

Se `git status --short` mostrar alterações locais não intencionais, não executar reset destrutivo. Preservar ou resolver conscientemente antes de sincronizar.

Validar a candidata localmente:

```powershell
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/tests/test_skill_enforcement_se01.py
python tools/validate_assistant.py --conferir-readme
```

Publicação no Free:

```powershell
$FreeProfile = "FREE"
$FreeHost = "https://<SEU-WORKSPACE-FREE>"

python tools/publicar_free.py --profile $FreeProfile --expected-host $FreeHost
python tools/publicar_free.py --execute --profile $FreeProfile --expected-host $FreeHost

New-Item -ItemType Directory -Force .artifacts\sef | Out-Null
python tools/publicar_free.py --verify --conteudo --profile $FreeProfile --expected-host $FreeHost --relatorio .artifacts\sef\se01-verify-conteudo.json
```

Critério de publicação: `APROVADO: 0 problema(s)`.

## 6. Capability probe no Genie Code

Abrir **chat novo**. Selecionar explicitamente `@hub-ml-eda-profissional` e enviar exatamente:

```text
@hub-ml-eda-profissional Execute somente o capability probe SE01 da própria skill, sem iniciar a EDA. Use o script relativo scripts/capability_probe.py e retorne integralmente o marcador JSON produzido. Não reimplemente o probe.
```

Critérios mínimos observáveis:

1. a skill é explicitamente selecionada;
2. o agente usa o script relativo, em vez de copiar sua lógica para uma célula;
3. a saída contém `marker = SEF_CAPABILITY_PROBE_V0_1`;
4. `status = PASS`;
5. `assistant_root_resolved = true`;
6. `import_target = hub_snippets.constants.format_br.fmt_int`;
7. `sample_result = 1.234`;
8. `writes_performed = false`.

Se o agente apenas disser que executou, sem evidência material da execução do script, classificar como `NOT_OBSERVABLE`, não como PASS.

## 7. Regressão mínima de uso da skill

Depois do probe, abrir outro chat novo e repetir o prompt natural congelado da SE00-P1:

```text
Faça uma EDA profissional da tabela samples.nyctaxi.trips. Avalie estrutura e qualidade dos dados, nulos, estatísticas descritivas, distribuições, relações e correlações quando aplicáveis, possíveis outliers e achados relevantes. Organize o trabalho de forma eficiente para Databricks/Spark, evite computação redundante e finalize com um resumo executivo dos principais achados, limitações e próximos passos.
```

Esta regressão não espera enforcement novo. Ela serve apenas para detectar se adicionar contrato/probe impediu ou degradou materialmente o carregamento/uso da skill.

## 8. Evidência a registrar

Para cada teste no Free:

- data/hora;
- branch e commit publicados;
- verify por conteúdo;
- chat novo confirmado;
- prompt exato;
- skill selecionada/observada;
- notebook/artefato, quando houver;
- marcador bruto do probe;
- se houve execução real do script ou reimplementação;
- limitações/erros;
- veredito `PASS`, `FAIL` ou `NOT_OBSERVABLE`.

Resultados reais entram somente em `RESULTADOS.md`.