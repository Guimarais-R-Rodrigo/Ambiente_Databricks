# V10 — testes e evidências

## Estado

V10 aceita e integrada no Git pelo PR #48; o merge funcional é `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`. Este arquivo registra somente evidências observadas; teste Git/local não é homologação do workspace e nenhum deploy Databricks foi executado.

## Suíte específica

`tools/tests/test_temas_v10.py` cobre:

- identidade encaminhada e namespace SHA-256;
- recusa de identidade ausente;
- fallback local explicitamente opt-in;
- recusa de storage produtivo fora de `/Volumes/`;
- recusa de traversal mesmo quando a string começa por `/Volumes/`;
- recusa de modo diferente de `authoring_only`;
- persistência roundtrip reutilizando sessão V05;
- isolamento entre duas identidades;
- não sobrescrita de sessão;
- recusa de sessão adulterada;
- política sem delete automático/usuário e sem reescrita de histórico;
- política sem aprovação/publicação/promoção;
- papéis V10 idênticos aos canônicos da V01;
- equivalência source/simulado da superfície do App, desconsiderando apenas caches transitórios não versionados do interpretador;
- `app.yaml` usando `valueFrom: theme_storage` sem segredo/caminho hardcoded;
- ausência de chamadas Databricks SDK/publicação no shell;
- verificação de que o gate de sintaxe não produz bytecode dentro da árvore do produto;
- geração e verificação do bundle derivado.

## Workflow permanente

`.github/workflows/temas-v10-ci.yml` é read-only (`contents: read`) e executa:

```bash
python -B tools/tests/test_temas_v10.py -v
python - <<'PY'
from pathlib import Path
for path in (
    Path('ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app.py'),
    Path('ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app_service.py'),
):
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')
PY
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/temas_v10_app.py --output .artifacts/v10-app
python -B tools/temas_v10_app.py --verify .artifacts/v10-app
python -B tools/validate_assistant.py --conferir-readme
```

O workflow não recebe credencial Databricks, não usa Databricks CLI e não faz deploy.

## Camadas de evidência

- **Python local/CI:** identidade sintética controlada, paths temporários, persistência e mutantes.
- **Bundle local:** integridade do artefato implantável derivado.
- **Documentação:** correspondência entre UI, código, papéis e procedimento.
- **Workspace futuro:** headers reais, App permissions, UC Volume, renderização, concorrência e UAT. Esses itens permanecem não testados até execução autorizada.

## Failures preservados

### `34884790130` — FAILURE por autocontaminação transitória do runner

No head inicial `41b930fb90bf0df20a5805d138665baffb6fa25c`, a suíte específica V10 e a checagem de sintaxe passaram. O cumulativo executou **434 testes**: **433 passaram e 1 falhou**. A falha foi `test_app_source_and_simulated_mirror_are_identical`, porque a etapa anterior usava `python -m py_compile` e criou `__pycache__/app*.pyc` apenas na árvore fonte do checkout.

Não havia divergência versionada entre fonte e simulado. A correção não relaxou a equivalência: o gate de sintaxe passou a compilar em memória sem escrever bytecode e a comparação V10 passou a ignorar somente `__pycache__`, `.pyc` e `.pyo` transitórios. O run permanece **FAILURE**.

### `34885407907` — FAILURE documental após gates funcionais verdes

No head `0ddcdd6b92372186c130d226c4b72d141cb7d67e`, passaram antes do validador:

- V10 específica: **19/19 PASS**;
- sintaxe do shell sem bytecode: **PASS**;
- regressões cumulativas V01–V10: **436/436 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- bundle derivado V10: **247 arquivos + `V10_APP_MANIFEST.json`**;
- verificação de inventário, tamanho e SHA-256 do bundle: **PASS**.

O único bloqueio foi `validate_assistant.py --conferir-readme`, que terminou com **7 falhas / 0 avisos**. A medição viva foi:

```text
skills             : 14 · 14/14 com as 5 seções estruturais
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 92 caminhos verificados
markdown / links   : 220 arquivos / 1393 links relativos
notebooks / links  : 80 notebooks / 101 links relativos
readmes de objeto  : 76/76 operacionais; 3/3 exemplares; 0 pendentes
pastas de objeto   : 62 conferidas
forma da pasta     : 60 conferidas
contrato de dados  : 62 pares
contrato de entrada: 60 pares
saída colada       : 79 notebooks com bloco real, 0 sem
idioma da docstring: 62 módulos, 0 com docstring em inglês
normas do molde    : 72 arquivos, 0 violações
notebook exercita  : 60 objetos, 0 notebook(s) que só importam
python (AST)       : 219 arquivos
instrucoes         : 9043/20000 caracteres
repo (identidade)  : 1373 arquivos varridos no repositório editável/derivado
repo (links)       : 1862 links fora da raiz analisada
worktree (extras)  : 0
```

Seis falhas decorriam das métricas antigas coladas no README raiz e da impossibilidade consequente de certificar a linha `APROVADO`; a sétima era um link relativo inválido da cópia simulada do README do App para a matriz V10, porque `docs/` não existe dentro do espelho `.assistant`. A correção substituiu esse link externo por referência textual e reconciliou os índices. O run permanece **FAILURE**.

### `34886250755` — FAILURE por quatro métricas stale no README raiz

No head `88cfea4d5cf29991c5bad23b61a3bec97feb2978`, todos os gates substantivos anteriores ao validador ficaram verdes: V10 **19/19**, regressões V01–V10 **436/436**, V00 **12/12**, bundle **247 arquivos + manifesto** e verificação do bundle em PASS.

O validador terminou com **4 falhas / 0 avisos**, exclusivamente porque o README raiz ainda continha quatro medições anteriores. A execução observou:

```text
markdown / links   : 220 arquivos / 1394 links relativos
python (AST)       : 219 arquivos
repo (identidade)  : 1373 arquivos varridos no repositório editável/derivado
repo (links)       : 1869 links fora da raiz analisada
```

Esses valores foram copiados para o bloco verificável sem estimativa e sem alterar o validador. O run `34886250755` permanece **FAILURE**.

## Primeira evidência integralmente verde da candidata

### `34886828579` — SUCCESS no head `c114cddedd7775cecb1cf8b672ad33e4a9f5365f`

A execução confirmou:

- V10 específica: **19/19 PASS**;
- sintaxe do shell Streamlit compilada em memória: **PASS**;
- regressões cumulativas V01–V10: **436/436 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- bundle derivado: **247 arquivos + `V10_APP_MANIFEST.json`**;
- verificação de inventário/tamanho/SHA-256 do bundle: **PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- etapa de escopo: **PASS**, reafirmando ausência de deploy, aprovação, promoção, ativação ou publicação Databricks.

Métricas verificáveis observadas nesse run:

```text
skills             : 14 · 14/14 com as 5 seções estruturais
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 92 caminhos verificados
markdown / links   : 220 arquivos / 1394 links relativos
notebooks / links  : 80 notebooks / 101 links relativos
readmes de objeto  : 76/76 operacionais; 3/3 exemplares; 0 pendentes
pastas de objeto   : 62 conferidas
forma da pasta     : 60 conferidas
contrato de dados  : 62 pares
contrato de entrada: 60 pares
saída colada       : 79 notebooks com bloco real, 0 sem
idioma da docstring: 62 módulos, 0 com docstring em inglês
normas do molde    : 72 arquivos, 0 violações
notebook exercita  : 60 objetos, 0 notebook(s) que só importam
python (AST)       : 219 arquivos
instrucoes         : 9043/20000 caracteres
repo (identidade)  : 1373 arquivos varridos no repositório editável/derivado
repo (links)       : 1869 links fora da raiz analisada
worktree (extras)  : 0
```

## Evidência final antes do merge

O push final original `34887162337`, no head `8e59739cbe3e1ce6d49503e7c953c82a98d2dc2c`, repetiu o gate completo com `success`. Depois da integração da MM00, a candidata foi reconciliada no head `cb942ee955ff9236f19099e5ed4ceee9beb32000`.

Nesse head reconciliado, dez workflows reais de PR concluíram com `success`: `34894892652`, `34894892747`, `34894892632`, `34894892622`, `34894892726`, `34894892777`, `34894892631`, `34894892738`, `34894892661` e `34894892620`. Os primeiros runs de PR anteriores à normalização dos runners permanecem failures históricos; eles não foram reclassificados.

## Evidência pós-merge

Após o aceite explícito de Rodrigo, o PR #48 foi integrado no commit `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`. Os **12 workflows de `push`** disparados nesse commit concluíram com `success`; o workflow específico V10 é `34896944061`. Não houve failure pós-merge nesse SHA.

## O que PASS não prova

PASS no GitHub Actions não prova deploy, autenticação real do workspace, privilégios corporativos, persistência efetiva em UC Volume, isolamento hostil multiusuário, browser, acessibilidade, desempenho percebido, custo observado ou publicação de tema.