# V09 — testes e evidências

## Estado

**V09 aceita e integrada no Git; sem publicação Databricks.** Este documento preserva successes e failures conforme realmente ocorreram e registra a correção pós-merge sem reclassificar resultados históricos.

## Suíte específica final

`tools/tests/test_temas_v09.py` possui **12 testes** e cobre:

- existência real de todos os nove caminhos obrigatórios no produto sanitizado;
- metadados fail-closed de transporte, ativação e publicação;
- mutante negativo removendo, um a um, cada caminho obrigatório;
- coerência entre inventário e bloco `theme_contract`;
- integração da guarda ao gerador antes da escrita do ZIP;
- preservação de `schema_version = 2`;
- instrução operacional no checklist;
- workflow V09 permanente read-only;
- ZIP sintético válido com conferência dos bytes reais;
- ZIP com arquivo temático ausente ou adulterado recusado;
- workflow operacional preparando Node/pnpm/dependências do compositor V06 antes de `ci_local.py`;
- ambos os workflows executando a validação pós-build, com o workflow operacional verificando antes do upload.

O 12º teste foi adicionado após o primeiro pós-merge revelar uma lacuna real de preparação do runner operacional. Ele não reduz nenhum gate anterior.

## Gate V09 permanente

O workflow `.github/workflows/temas-v09-ci.yml` executa:

```bash
python -B tools/tests/test_temas_v09.py -v
python -B tools/tests/test_transicao_trabalho.py -v
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/kit_transicao_trabalho.py --output .artifacts/v09-kit
python -B tools/temas_v09_transicao.py --kit-dir .artifacts/v09-kit
python -B tools/validate_assistant.py --conferir-readme
```

A chamada de `test_transicao_trabalho.py` desse workflow não usa `--spark`. Portanto, quando os 43 testes são descobertos nessa etapa, o resultado correto é **36 PASS + 7 SKIP explícitos** de Spark local desabilitado, e não “43 PASS”.

A geração e inspeção do kit são locais ao runner e não usam credenciais Databricks. O workflow permanente declara `contents: read` e o checkout usa `persist-credentials: false`.

## Workflow operacional do kit

`.github/workflows/kit-transicao-trabalho.yml` é o gate que exerce os contratos Spark locais. No estado final V09 ele prepara:

- Python 3.11;
- Java 17;
- Node 22;
- dependências Python e `pyspark==4.0.1`;
- `pnpm@10.34.5`;
- dependências de `tools/readme_visuals` com `--frozen-lockfile`.

Depois executa, nesta ordem relevante:

```bash
python tools/ci_local.py --verbose
python -B tools/tests/test_temas_v09.py -v
python tools/tests/test_transicao_trabalho.py --spark -v
python tools/kit_transicao_trabalho.py --output .artifacts/kit-trabalho
python -B tools/temas_v09_transicao.py --kit-dir .artifacts/kit-trabalho
```

Somente depois da verificação do ZIP ocorre `actions/upload-artifact@v4`. Esse upload é um artefato de CI no GitHub Actions; não instala nem publica nada no Databricks.

## Failures preservados

### `34877035267` — FAILURE de oráculo textual da suíte V09

No head `17a95762b9f6dc19c13cf008ee581bc7c1041d26`, sete dos oito testes V09 passaram. O único failure foi `test_transition_checklist_names_theme_contract`: o checklist registra corretamente a chave real `manual_opt_in`, mas o teste procurava a expressão inexistente `manual/opt-in`. A implementação do contrato não foi alterada para acomodar o teste; o oráculo foi corrigido no commit seguinte. As etapas posteriores foram puladas porque a suíte específica já havia reprovado.

Esse run permanece **FAILURE**.

### `34877297808` — FAILURE documental após todos os gates funcionais passarem

No head `b7d16ab6eccf59a266353dc74502cf51703ad8c3` passaram:

- V09 específica: **8/8**;
- regressões do kit de transição: **43 testes executados, 36 PASS e 7 SKIP** porque a chamada dessa etapa não usa `--spark`;
- regressões cumulativas V01–V09: **413/413**;
- compatibilidade V00: **12/12**;
- geração real do kit offline: **535 arquivos + `MANIFEST.json`**, commit do kit `b7d16ab6eccf...`.

O único bloqueio foi `validate_assistant.py --conferir-readme`: a execução mediu `1355` arquivos no repositório editável/derivado, enquanto o README raiz ainda continha `1350`. O validador terminou com **1 falha e 0 avisos**. A correção alterou somente esse número no README; nenhum contrato ou runtime foi relaxado.

Esse run permanece **FAILURE**.

### `34880619346` — FAILURE pós-merge do PR #45

No merge funcional `0f7234c4734f1974ebb1a20123f3c26626c67ef3`, o workflow `Kit de transição para o trabalho` falhou no passo `Gate local sem credenciais Databricks`.

Causa reproduzida nos logs: o runner ainda não havia instalado as dependências Node exigidas pelo compositor V06. O próprio `ci_local.py` recusou a execução e orientou instalar:

```bash
npm install --global pnpm@10.34.5
pnpm --dir tools/readme_visuals install --frozen-lockfile
```

Como o primeiro gate falhou, as etapas V09, Spark local, geração do kit, conferência do ZIP e upload permaneceram corretamente `skipped`.

A implementação do produto e os testes não foram relaxados. O PR #46 corrigiu a preparação do runner e acrescentou um teste de regressão que exige a ordem correta antes do `ci_local.py`.

Esse run permanece **FAILURE**.

## Evidência da candidata funcional antes do aceite

O head final original da PR #45 era `3b69dd25fd4af434fda414496c2ca3d80fd78a8e`. Os cinco workflows realmente disparados pelo evento `pull_request` concluíram com `success`:

- Regressões da instrumentação V00 — run `34879872894`;
- Contrato de temas V01 — run `34879872928`;
- Núcleo de temas V02 — run `34879872921`;
- CI local reproduzível — run `34879873342`;
- Kit de transição e temas V09 — run `34879872930`.

O workflow operacional `Kit de transição para o trabalho` não possuía evento `pull_request` e, por isso, não deve ser descrito como um check dessa PR.

## Evidência da correção — PR #46

No head `d1c67f06d96b929a58961c50fc31c06ca7c0cfe2`, os cinco checks de PR realmente disparados concluíram com `success`:

- V00 — `34881120187`;
- V01 — `34881120270`;
- V02 — `34881120196`;
- CI local — `34881120184`;
- V09 — `34881120261`.

A correção tocou somente `.github/workflows/kit-transicao-trabalho.yml` e `tools/tests/test_temas_v09.py`.

## Gate pós-merge final

### SHA `4ae714a35a0aafd930a8cd796d962b0a79449b88` — 12/12 workflows de push em SUCCESS

O inventário nominal dos runs está em `CHECKPOINT_V09.md`. Os resultados técnicos principais foram:

- suíte V09: **12/12 PASS**;
- dentro do CI local, regressões do kit sem `--spark`: **43 testes, 36 PASS + 7 SKIP explícitos**;
- no workflow operacional, `test_transicao_trabalho.py --spark -v`: **43/43 PASS** com Spark **local no runner**;
- gate cumulativo de temas no CI local: **417 testes executados, OK com 9 skips previstos/condicionais**;
- kit offline real: **535 arquivos + `MANIFEST.json`**;
- `theme_contract` v1: **9/9 caminhos presentes e SHA256 válido no ZIP**;
- `activation = manual_opt_in`;
- `publication = not_performed`;
- SHA256 do `MANIFEST.json`: `7b8e811038bb34a4aebade9d3c58e2c308495ce60ccc563bb860ff43ade8e6ea`;
- validador: **APROVADO — 0 falhas / 0 avisos**;
- repositório medido: **1355 arquivos**;
- links fora da raiz: **1850**;
- `GITHUB_TOKEN`: `Contents: read`, `Metadata: read`;
- workflow operacional completo: run `34881426374` — **SUCCESS**.

O artefato GitHub Actions foi criado somente após a validação do ZIP. Nenhum passo desse gate publicou, instalou, ativou ou promoveu temas em Databricks real.

## O que PASS não prova

- importação real no workspace corporativo;
- render visual no navegador Databricks;
- acessibilidade ou UAT humano;
- ativação ou promoção de tema;
- permissão/ACL do destino;
- publicação Databricks.

**A V10 não foi iniciada por este fechamento.**
