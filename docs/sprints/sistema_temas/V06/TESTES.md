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

## Interpretação

PASS em Python/GitHub Actions prova os contratos exercitados naquele checkout. Não prova aparência em navegador Databricks, acessibilidade, UAT, permissões do workspace, publicação nem aprovação de uma variante visual.

A execução final verde e os IDs do head final serão registrados no fechamento da PR sem reescrever as falhas acima.
