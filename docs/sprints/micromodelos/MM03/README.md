# MM03 — descoberta metadata-only

Núcleo interno para organizar descoberta progressiva de fontes de micromodelos.
Destina-se aos mantenedores do framework; ainda não é uma skill publicada.

**Estado: IMPLEMENTADA_CANDIDATA / PREPARACAO_LOCAL_PENDENTE.**
A MM02 foi integrada pela PR #109 no merge `073762fd8e38afadf27aca0f4d77351d9bfb627f`.
Essa é a base de autoria da MM03; as seções antigas que ainda descrevem MM02 em
implementação são históricas ou índices pendentes de reconciliação, não bloqueio
para reiniciar a MM02.

## Próxima ação

Executar a [preparação local e smoke](PREPARACAO_LOCAL.md), sem modificar lógica
nem testes. O [checkpoint](CHECKPOINT.md) distingue resultados reais de pendências.
O [contrato](CONTRATO_METADATA.md) é o dono do escopo técnico; a
[matriz de testes](TESTES.md) define os gates.

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
