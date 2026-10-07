# ADR-0010 — Manual Técnico unificado para usuários do Hub

- **Status:** Aceito por solicitação do usuário
- **Data:** 2026-09-11
- **Supersede:** ADR-0007 somente quanto ao arquivo e à forma do catálogo central.

## Contexto

O usuário optou pelos READMEs e componentes visuais vigentes, descartou os
rascunhos de revisão e solicitou um manual didático abrangente que substitua
o catálogo de helpers e o glossário como documentos independentes.

## Decisão

A redação de autoria é `ambiente_fonte/.assistant/MANUAL_TECNICO.md`.
O inventário completo vive na âncora `catalogo-helpers`; as definições e o índice
integrado, em `indice-termos`. O renderer leva esse documento ao simulado.
A raiz Git recebe uma cópia de leitura com bytes iguais, conferida por teste,
para atender ao acesso direto solicitado, sem uma segunda redação autônoma.

Removem-se `CATALOGO_HELPERS.md` e `GLOSSARIO.md` da fonte e, por renderização,
do derivado. Referências ativas são migradas. Histórico e corpos decisórios
aceitos não são reescritos; os mecanismos de declaração explícita de helpers,
pasta de objeto e API pública permanecem.

O manual distingue API local, Spark, serviços REST e contexto da IA. Assinaturas
são referência de código, não prova de execução. Testes locais não homologam
Databricks, serviços remotos, ACL ou roteamento conversacional.

## Consequências

Na raiz do Hub, os documentos gerais passam a ser README e Manual Técnico.
Arquivos de controle Git, instruções dos agentes e governança na raiz do
repositório permanecem: não são os dois documentos de usuário cuja exclusão
foi pedida. READMEs visuais recebem somente ajustes de navegação necessários.

Uma alteração posterior exige sincronizar a cópia Git, renderizar o derivado,
validar links, inventário e exemplos. A retirada de cópias remotas antigas não
é presumida por exclusão no Git; exige publicação/conferência autorizadas.

## Referências

- [ADR-0007](ADR-0007-catalogo-e-pasta-de-objeto.md), preservado em seu corpo.
- [Manual Técnico da edição decidida](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/8dd8da57de89122241890b8b6b059fd2f9be25d0/MANUAL_TECNICO.md).

## Registro de sucessão — 2026-10-07

O ADR-0028 substitui somente o nome da edição vigente e a cópia integral na
raiz. O corpo decisório acima permanece histórico. A referência do livro aponta
ao commit em que a edição anterior estava presente.
