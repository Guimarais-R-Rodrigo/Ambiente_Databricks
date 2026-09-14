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

## Interpretação

PASS em Python/GitHub Actions prova os contratos exercitados naquele checkout. Não prova aparência em navegador Databricks, acessibilidade, UAT, permissões do workspace, publicação nem aprovação de uma variante visual.

A execução final verde e os IDs do head final devem ser registrados sem reescrever as falhas acima.
