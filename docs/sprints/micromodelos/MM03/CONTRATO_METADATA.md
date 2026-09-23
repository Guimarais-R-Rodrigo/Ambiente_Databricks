# MM03 — contrato metadata v1

Contrato candidato `mm03-metadata-v1`, interno e repo-side/sintético. Não é o schema
de `micromodelo.yaml`, uma policy SEF, um Execution Receipt ou um Postflight.
A autorização humana foi para iniciar MM03, não para aprovar ou integrar esta candidata.

## M01 — escopo e binding

`Binding(physical_catalog, catalog_ref)` exige catálogo físico explicitamente
fornecido e `catalog_ref=CATALOGO_PRODUTO`, conforme ADR-0020. Nenhuma enumeração
de outros catálogos é oferecida. Cada `Page` devolvida precisa repetir o catálogo
configurado e a mesma identidade de observação `snapshot_id`.

O envelope atual aceita identificadores ASCII `[A-Za-z_][A-Za-z0-9_]{0,127}`.
Pontos, curingas, separadores de path e sintaxe de SQL não são identificadores.
Isso delimita este provider sintético, não redefine identificadores Databricks.
Ampliar o envelope requer teste e revisão explícitos; não normalizar silenciosamente.

## M02 — operações e progressividade

As únicas operações são `schemas`, `objects`, `columns`, `column_tags` e
`constraints`. A interface não recebe SQL, código, nome de função ou URL.

`discover()` solicita schemas. `discover([schema])` também solicita objetos dos
schemas escolhidos, que precisam constar no resultado observado. `details()`
exige shortlist não vazia, sem duplicatas e inteiramente contida nos objetos
observados. Toda a shortlist é verificada antes da primeira chamada de detalhe.
Uma nova descoberta exige novo coletor; o estado antigo não é reutilizado.

O provider offline carrega e valida o arquivo inteiro em memória. O teste de
progressividade prova quais operações o coletor solicita e expõe; não prova
leitura remota lazy, minimização de I/O de uma API ou isolamento de processos.

## M03 — observação parcial

Cada coleção possui `status`, `reason`, `items` e `catalog_complete=false`.
Estados: `OBSERVED`, `DENIED`, `UNAVAILABLE`, `TRUNCATED` e `PARTIAL`.
Negação posterior a páginas observadas preserva itens anteriores como `PARTIAL`.
Stream não disponibilizado pelo provider sintético é `UNAVAILABLE`, nunca
inventado como uma coleção vazia conhecida. `None` e texto vazio permanecem distintos.

O envelope sempre declara `coverage=ESCOPO_OBSERVADO`, `catalog_complete=false`,
`metadata_is_instruction=false` e `data_access_authorized=false`. A presença de
qualquer coleção incompleta produz `observation_status=PARTIAL_OBSERVATION`.
`OBSERVED` significa conclusão da coleção visível fornecida, não catálogo completo.
A presença de um objeto não comprova SELECT permitido; ausência não prova inexistência.

## M04 — paginação e limites

Defaults: 50 itens/página, 20 páginas/operação, 500 itens/coleção e 10 candidatas.
Máximos configuráveis: 100, 100, 2.000 e 20, respectivamente. Booleanos não contam
como inteiros de configuração. Limites encerram a coleta com truncamento explícito.
Tokens repetidos, páginas grandes demais, itens duplicados entre páginas, página
vazia não terminal ou dados acompanhados de DENIED/UNAVAILABLE são erros de contrato.
Um token é dado opaco de paginação; nunca URL, instrução ou conteúdo de saída.
Não há retries ou fallback para registros. Paginação não autentica o provider.

## M05 — shape fechado

| Operação | Campos aceitos por item |
|---|---|
| schemas | name, description |
| objects | name, object_type (TABLE/VIEW), description, tags |
| columns | name, data_type, nullable (bool/null), description |
| column_tags | column, tags |
| constraints | name, kind, columns, description |

Tags são pares key/value; `null` significa não fornecidas. Tipos novos de objeto
não são silenciosamente descartados. Propriedades adicionais, incluindo rows,
samples, stats, count, sql e instructions fora de texto livre, são recusadas.

Constraints representam declarações observadas (PRIMARY_KEY, FOREIGN_KEY, CHECK,
UNIQUE, NOT_NULL). Todas saem com `enforcement=NOT_VERIFIED`. O perfil não reconstrói
alvos externos de foreign keys nem interpreta expressão CHECK; não segue referências.
Se a coleta de colunas estiver completa no escopo observado, referências locais
em tags/constraints precisam resolver. Com colunas incompletas essa verificação
não é alegada; os estados incompletos permanecem no envelope.

## M06 — conteúdo não confiável e sanitização

Descrição, tipos textuais, tags e descrição de constraints nunca alteram catálogo,
shortlist, método, autorização ou sequência de chamadas. Não há avaliação/execução
do conteúdo, navegação em links nem conversão para mensagem system/developer.
A defesa exercitada é a separação estrutural entre configuração e evidência, não
uma blacklist de frases suspeitas.

Cada texto emitido inclui `trusted=false`, hash SHA-256 dos bytes fonte e flags
para redactions, controls_escaped e truncated. Controles Cc/Cf são representados
visivelmente; texto de exibição é limitado a 2.000 caracteres após higiene. Input
por campo tem limite de 16.384 bytes UTF-8; Unicode inválido falha. Algumas formas
de paths locais, e-mail e credenciais são redigidas antes do truncamento. A lista
não é exaustiva e não certifica ausência de PII/segredos; o material versionado
deve continuar estritamente sintético.

Hashes de texto vinculam bytes observados; não autenticam origem nem aprovação.
Constraints, descrições e tipos continuam não verificados semanticamente mesmo
quando sua estrutura passa. Um LLM futuro que desrespeite a fronteira ainda é
risco: testes comportamentais pertencem à integração futura, não a este laboratório.

## M07 — provider e fonte

`MetadataProvider.fetch_page` é contrato para código confiável. `FixtureProvider`
valida shape, streams únicos, operações, campos, duplicatas e marcadores sintéticos.
O marcador synthetic é uma declaração de autoria da fixture, não detector de dado real.
A CLI só aceita fixture JSON local, limitada a 1 MiB, sem chaves duplicadas ou NaN/Inf.
Não importa plugin, não possui credencial nem adaptador vivo Databricks.

`snapshot_id` fornece consistência declarada pelo provider, não snapshot transacional
de Unity Catalog. A saída CLI acrescenta `source.kind=SYNTHETIC_FIXTURE`, hash do
arquivo e `live_databricks_verified=false`. Nenhum timestamp de observação remota é inventado.

## M08 — erros e reprodutibilidade

CLI: exit 0 significa relatório estruturalmente produzido; coleções negadas ou
incompletas continuam explícitas, não são convertidas em sucesso de acesso.
Exit 1 indica erro conhecido de contrato. Exit 2 indica erro inesperado/carga
ou uso CLI. Falha não emite relatório parcial no stdout; mensagens próprias não
repetem paths/metadata recebidos. A ferramenta não grava arquivos.

Com a mesma fixture, configuração e provider determinístico, saída JSON e ordem
de itens são determinísticas. Sem truncamento, reorganização serial de itens não
altera a descoberta. Com truncamento, a seleção depende das páginas recebidas e
esse limite não é apresentado como equivalência global do catálogo.

## M09 — fronteiras de integração

O coletor não preenche YAML, não propõe regra analítica, não executa fingerprint,
EDA, dados, tracking, ACL ou publicação. Não altera MM01/MM02 nem qualquer
current_level. PSEF01/PR #99 e SER01/PR #108 abertas não são autoridade integrada.
Este contrato não afirma que MM03 já esteja certificada ou homologada.
