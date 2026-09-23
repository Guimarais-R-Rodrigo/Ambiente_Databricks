# MM03 — descoberta metadata-only

Núcleo interno para organizar descoberta progressiva de fontes de micromodelos.
Destina-se aos mantenedores do framework; ainda não é uma skill publicada.

**Estado: POS_CERTIFICACAO / AUDITORIA_INDEPENDENTE_APTA / GATE_HUMANO_PENDENTE.**
A MM02 foi integrada pela PR #109 no merge `073762fd8e38afadf27aca0f4d77351d9bfb627f`.
A MM03 está na PR #110. A candidata funcional corrigida é
`ebbe6ec374e38686bb76d56d7e76f6b3dcd73cb0`; FULL R2 e bundle passaram,
a auditoria independente não deixou finding aberto e o fechamento documental
mínimo precede apenas a revalidação final e o aceite humano.

## Próxima ação

Revalidar a árvore após este fechamento documental e solicitar aceite humano da
PR #110. Não iniciar MM04, não retirar o Draft e não fazer merge antes desse gate.
O [checkpoint](CHECKPOINT.md) preserva a R1 reprovada, a correção mínima e a R2.
O [contrato](CONTRATO_METADATA.md) continua dono do escopo técnico; a
[matriz de testes](TESTES.md) continua dona dos gates.

## Certificação e auditoria

```text
PRE_CERTIFICATION_SMOKE = PASS
FULL_R1 = FAIL_HISTORICAL_ON_b432596
CORRECTED_SHA = ebbe6ec374e38686bb76d56d7e76f6b3dcd73cb0
MICRO_SMOKE_R2 = PASS
FULL_R2 = PASS
BUNDLE_LINT = PASS
INDEPENDENT_AUDIT = APTA
AUDIT_FINDINGS_OPEN = 0
SNAPSHOT = 1716/2166/0
LIVE_DATABRICKS = NOT_RUN
MM04 = NOT_STARTED
```

## O que foi implementado

`tools/micromodelo_mm03_metadata.py` oferece `MetadataCollector`, `Binding`,
`Limits`, `Page`, o contrato `MetadataProvider` e `FixtureProvider` offline.

O fluxo é: listar schemas visíveis, listar objetos somente nos schemas escolhidos,
receber uma shortlist explícita e obter colunas, tags de coluna e constraints
somente dessas candidatas. O coletor não escolhe a shortlist a partir de instruções
em comentários. Julgamento semântico e orquestração conversacional continuam
reservados às skills/modos previstos em MM04/MM05.

O binding físico é um argumento explícito e todas as respostas precisam coincidir
com ele. A referência lógica permanece `CATALOGO_PRODUTO`. O provider incluído usa
apenas `catalogo_sintetico`; não existe conexão ou binding corporativo implantado.

## Exemplo copiável, na raiz do repositório

```text
python -B tools/micromodelo_mm03_metadata.py --fixture tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json --catalog catalogo_sintetico --schema crm_sintetico --candidate crm_sintetico.eventos_sinteticos
```

Sem `--schema`, a CLI lista apenas schemas. Com `--schema` e sem `--candidate`,
lista objetos sem solicitar detalhes. Ambos os argumentos aceitam repetição.
A saída é JSON; nenhum arquivo de saída é gravado automaticamente.

A fixture possui um schema com acesso negado e metadata adversarial. Esses casos
são sintéticos, não observações de permissões reais nem execução de SQL.

## Limites

A ferramenta não executa SQL, Spark, SDK Databricks, rede, profiling, contagem de
registros, amostragem, ACLs, MLflow, publicação ou escrita de YAML/fingerprint.
Não chama `schema_to_yaml`, `quick_profile` ou EDA: não há tabela real autorizada
e a MM00 já distingue snapshot técnico de crawler do catálogo.

Metadata livre recebe marcação não confiável e higiene de exposição rastreável.
Isso não é garantia universal de remoção de PII nem prova de resistência de um
LLM consumidor a prompt injection. Esse consumidor ainda não foi criado/testado.

O provider Python pertence à base de código confiável; a interface não impede
um provider malicioso de produzir efeitos externos. Não há carregamento dinâmico
de provider pela CLI. O provider incluído é sintético; um adaptador real exige
implementação/revisão próprias e homologação ambiental, sem alegar capacidade
Databricks a partir destes testes locais.

## Autoridades preservadas

[Plano Mestre](../PLANO_MESTRE.md), [revisão pós-SEF](../REVISAO_PLANO_POS_SEF_2026-09-23.md),
[protocolo de certificação](../PROTOCOLO_CERTIFICACAO_SPRINTS.md),
[ADR-0020](../../../decisions/ADR-0020-fontes-catalogo-configurado.md) e
[matriz de reuso MM00](../MM00/MATRIZ_REUSO.md).
Não há alteração em MM01/MM02, policy, skills, prompts, workflows ou derivado.
