# SE06 — runbook Databricks Free

## Objetivo

Executar os 25 runs comportamentais da matriz SE06 no Genie Code real, sem alterar o produto L4 integrado pela SE05.

## Economia

A SE06 é local-first.

Durante desenvolvimento/coleta:

- não abrir PR;
- não usar Actions;
- não criar commit por run;
- resultados ficam fora do repositório até a consolidação agregada;
- não republicar o Hub entre runs.

## 1. Pré-condição local

Exigir:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE06_LOCAL
DERIVED_STALE       = false
failures            = 0
```

## 2. Identidade do Free

PowerShell:

```powershell
$DBX_PROFILE = "FREE"
$DBX_HOST = "https://dbc-72c8503a-bc27.cloud.databricks.com"

databricks --profile $DBX_PROFILE auth describe -o json
databricks --profile $DBX_PROFILE current-user me -o json
```

Não prosseguir se host/usuário não forem o laboratório pessoal esperado.

## 3. Verificar produto publicado

A SE06 não modifica `.assistant`. Portanto, preferir verify read-only antes de republicar:

```powershell
$EVID = Join-Path $HOME ".ambiente_databricks\sef_certifications"
New-Item -ItemType Directory -Force -Path $EVID | Out-Null
$HEAD12 = (git rev-parse HEAD).Substring(0,12)

python tools/publicar_free.py --verify --conteudo `
  --profile $DBX_PROFILE `
  --expected-host $DBX_HOST `
  --relatorio (Join-Path $EVID "se06_free_verify_$HEAD12.json")
```

Se houver mismatch real do pacote controlado, parar e diagnosticar. Não republicar automaticamente no meio de uma rodada já iniciada.

## 4. Criar bundle externo

```powershell
$SE06_DIR = Join-Path $HOME ".ambiente_databricks\sef_certifications\se06"
New-Item -ItemType Directory -Force -Path $SE06_DIR | Out-Null

$RESULTS = Join-Path $SE06_DIR "results.json"

python -B tools/skill_enforcement/se06_eval.py `
  --validate-spec `
  --init-results $RESULTS
```

O arquivo fica fora do repositório.

Vincule a identidade experimental pelo próprio Python, sem editar JSON via PowerShell:

```powershell
$SE06_HEAD = (git rev-parse HEAD).Trim()
$PRODUCT_SHA = (git rev-parse origin/main).Trim()

python -B tools/skill_enforcement/se06_eval.py `
  --bind-results $RESULTS `
  --source-head $SE06_HEAD `
  --assistant-package-sha $PRODUCT_SHA
```

Esse comando grava UTF-8 sem BOM e falha se:

- qualquer SHA não tiver 40 hexadecimais;
- o arquivo não for um bundle SE06;
- a identidade já estiver vinculada a outro SHA;
- já existir qualquer run `OBSERVED`.

Depois do binding, não alterar `source_head` nem `assistant_package_sha` durante a rodada.

## 4.1 Troca de candidata após early-stop

Quando uma candidata já tiver runs `OBSERVED` e for corrigida:

1. **não rebind** o `results.json` existente;
2. preservar o arquivo antigo com nome que contenha o HEAD diagnóstico;
3. criar novo skeleton para a candidata corrigida;
4. vincular o novo HEAD e o SHA do pacote efetivamente publicado;
5. zerar o contador da candidata final para 0/25, mantendo o acumulado histórico separado.

Exemplo:

```powershell
$OLD = Join-Path $SE06_DIR "results.json"
$ARCHIVE = Join-Path $SE06_DIR "results_diag_<HEAD12>.json"
Move-Item -LiteralPath $OLD -Destination $ARCHIVE

python -B tools/skill_enforcement/se06_eval.py --validate-spec --init-results $OLD
python -B tools/skill_enforcement/se06_eval.py `
  --bind-results $OLD `
  --source-head <NOVO_HEAD_SE06> `
  --assistant-package-sha <SHA_DO_PACOTE_PUBLICADO>
```

O archive é evidência histórica. Não editar runs diagnósticos para fazê-los parecer parte da candidata final.

## 4.2 Homologar a correção antes do novo 0/25

Se a correção alterar `.assistant`:

1. executar `FULL_SE06_LOCAL`;
2. publicar no Free pelo publicador canônico;
3. verify por conteúdo;
4. executar `se06_correction_free_probe.py`;
5. somente com probe PASS iniciar chats da nova candidata.

## 5. Execução

Para cada run de `genie_chat`:

1. abrir chat novo;
2. copiar o prompt literalmente de `se06_cases.json`;
3. não acrescentar instruções;
4. deixar a primeira resposta terminar;
5. salvar notebook/artefato ou caminho;
6. registrar evidência no `results.json`;
7. só então iniciar o run seguinte.

## 6. Auditorias A1

Executar quatro chats:

- primeiro artefato P1;
- primeiro artefato M1;
- primeiro artefato R1;
- primeiro artefato B1.

Substituir somente `<ARTEFATO>` no prompt-template.

## 7. Validação incremental

É permitido inspecionar a coleta sem fazê-la passar:

```powershell
python -B tools/skill_enforcement/se06_eval.py `
  --results $RESULTS `
  --allow-incomplete
```

`DOD=INCOMPLETE` é o estado normal antes de 25/25.

## 8. Scoring final

Usar o `summary.json` do certifier FULL_SE06_LOCAL como prova da structural suite:

```powershell
$CERT = "<caminho para summary.json do FULL_SE06_LOCAL>"
$SUMMARY = Join-Path $SE06_DIR "summary.json"

python -B tools/skill_enforcement/se06_eval.py `
  --results $RESULTS `
  --certification-summary $CERT `
  --summary-out $SUMMARY
```

Critério:

`DOD = PASS`

## 9. O que não fazer

- não repetir run ruim até conseguir um bom;
- não editar o prompt para ajudar o agente;
- não usar o mesmo chat em duas repetições;
- não classificar autorrelato como evidência de completed;
- não modificar `.assistant` durante a rodada;
- não subir o `results.json` bruto se ele contiver caminhos/observações desnecessárias; a consolidação deve ser sanitizada.

## 10. Encerramento

Depois de DOD PASS:

1. consolidar métricas em `RESULTADOS.md`;
2. preservar hashes/caminhos dos bundles externos;
3. recertificar HEAD documental;
4. congelar RC;
5. abrir PR uma única vez;
6. observar Actions sem rerun automático.
