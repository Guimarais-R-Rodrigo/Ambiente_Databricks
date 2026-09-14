# V06 — testes e evidências

## Suíte específica

Arquivo: `tools/tests/test_temas_v06.py`.

Casos permanentes:

- `theme_id` canônico resolve pelo núcleo V02 e id desconhecido falha fechado;
- geração repetida com mesmo `SOURCE_DATE_EPOCH` é byte a byte determinística;
- 12 recursos de `editorial-v2-congelado` são verificados por SHA-256 e permanecem inalterados;
- legado editorial produz somente assinaturas congeladas ou equivalentes paramétricos, sem promoção implícita;
- manifesto/arquivos gerados podem ser verificados novamente;
- adulteração de PNG é detectada por hash;
- saída dentro do pacote visual ativo é recusada;
- contrato `theme_generation.yaml` é idêntico entre fonte e ambiente simulado.

## Execuções preservadas

### `34845378370` — FAILURE

Falha de bootstrap: `actions/setup-node` tentou usar cache `pnpm` antes de o binário ser instalado. Nenhum teste funcional foi executado.

### `34845593931` — FAILURE

O bootstrap avançou, mas `pnpm` recusou o `pnpm-workspace.yaml` sem campo `packages`. Nenhum teste funcional foi executado.

### `34845754341` — FAILURE do gate agregado

A instalação Node passou e a suíte V06 concluiu **5/5 PASS**. A etapa agregada V01–V06 falhou por dependências Python ausentes (`plotly` e `pandas`), porque o workflow inicialmente instalava apenas `requirements-temas-dev.txt`. A correção passou a instalar `requirements-dev.txt` e `ipywidgets>=8,<9`, como exigido para cobertura completa das versões anteriores.

### `34845937711` — FAILURE documental

A suíte V06 concluiu **5/5 PASS**, as regressões V01–V06 **364/364 PASS** e a compatibilidade V00 **12/12 PASS**. O workflow reprovou exclusivamente porque o README raiz ainda registrava métricas anteriores à inclusão dos novos arquivos V06.

### `34846291082` — FAILURE documental

Na árvore com a documentação V06 estruturada, 5/5 testes específicos, 364/364 regressões V01–V06 e 12/12 V00 passaram. O workflow reprovou somente porque o README raiz ainda trazia métricas anteriores: `1382→1383` links Markdown, `1334→1339` arquivos de identidade e `1838→1841` links fora da raiz. A execução permanece registrada como FAILURE.

### `34847723861` — FAILURE histórico

Permanece registrado como reprovado. O fechamento V06 não reclassifica essa execução.

### `34848445012` — FAILURE do CI geral

O gate agregado `tools/ci_local.py` descobriu corretamente `test_temas_v06.py`, mas o workflow geral ainda preparava apenas dependências Python. Três testes V06 que utilizavam o compositor Node falharam pela ausência das dependências do renderer. A correção foi preparar Node 22, `pnpm@10.34.5` e `node_modules` do compositor; nenhum teste foi relaxado.

### `34848898532` e `34848898536` — FAILURE V04/V05 cumulativo

V04 e V05 mantinham a descoberta cumulativa `test_temas*.py`. Depois da V06, essa descoberta também passou a exigir o compositor Node. Os dois workflows falharam nesse pré-requisito, embora suas suítes específicas tivessem passado. O head final corrigiu o ambiente de V04/V05 em vez de filtrar a V06.

## Head final da PR #38 — `70499e1803ce0d61a148a0da975c4f52611046e0`

Todos os workflows disparados para o head final concluíram com `success`:

- `34849332915` — Regressões da instrumentação V00;
- `34849332504` — Contrato de temas V01;
- `34849332510` — Núcleo de temas V02;
- `34849332547` — Componentes HTML e tabelas V04;
- `34849332540` — Visual Lab notebook V05;
- `34849332509` — Assets e geração V06;
- `34849332601` — CI local reproduzível.

No workflow V06, permaneceram verdes:

- suíte específica V06: **5/5**;
- regressões cumulativas V01–V06: **364/364**;
- compatibilidade visual V00: **12/12**;
- validação estrutural/documental;
- escopo.

O head final só ajustou o preparo de ambiente dos workflows V04/V05 para a regressão cumulativa; não removeu nem filtrou `test_temas_v06.py`.

## Pós-merge na `main` — `418946de8d1e95e87cbfd9df528ddcced5075237`

A árvore do merge é a mesma árvore do head final testado: `68ddec3d691047e890ba2785e1e2e007039fa0e3`.

Os oito workflows disparados por `push` concluíram com `success`:

- `34849703278` — Regressões da instrumentação V00;
- `34849703186` — Contrato de temas V01;
- `34849703185` — Núcleo de temas V02;
- `34849703168` — Adaptador Plotly V03;
- `34849703237` — Componentes HTML e tabelas V04;
- `34849703178` — Visual Lab notebook V05;
- `34849703234` — Assets e geração V06;
- `34849703315` — CI local reproduzível.

O job V06 pós-merge executou, em ordem, checkout, Python, Node, dependências Python, dependências do compositor, suíte V06, regressões V01–V06, V00, validação estrutural/documental e escopo. Todas as etapas concluíram com `success`.

O CI geral pós-merge também concluiu com `success` depois de configurar Node e instalar as dependências do compositor antes de `Executar o gate sem credenciais`.

## Interpretação

PASS em Python/GitHub Actions prova os contratos exercitados naquele checkout. Não prova aparência em navegador Databricks, acessibilidade, UAT, permissões do workspace, publicação nem aprovação de uma variante visual.

A V06 foi integrada no Git; nenhuma execução reprovada acima foi convertida retroativamente em sucesso. Não houve publicação Databricks e a V07 não foi iniciada.
