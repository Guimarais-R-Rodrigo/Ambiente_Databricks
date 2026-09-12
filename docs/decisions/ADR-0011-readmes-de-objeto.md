# ADR-0011 — README didático por pasta de objeto

Data: 2026-09-12
Status: Proposto — implementação candidata R01; aceite humano pendente
Autor: Codex

## Contexto

A pasta de objeto já reúne implementação, fachada e notebook. Essa rota ensina
a executar, mas exige que o leitor saiba por que escolher o recurso. O plano
R00 autorizou a R01 de fundação antes da produção em massa.

## Decisão proposta

Adicionar `README.md` a cada pasta de snippet, script e prompt, como escala
Objeto do tipo README. Não criar sétimo tipo nem aplicar quinze seções a índices
ou skills. O contrato editorial vive em
[`template_objeto.md`](../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md).

Preservar o catálogo e os termos integrados no Manual (ADR-0010). O README local
explica conceito aplicado e adequação; o notebook demonstra; código e fachada
continuam definindo a API. Materiais de exemplo em `hub_padroes/` ficam fora da
contagem operacional. Não alterar comportamento analítico nesta migração.

Exigir README de novos objetos. Os legados têm dispensa temporária por caminho,
com sprint de destino, no controle da migração. A dispensa só diminui; READMEs
presentes precisam ser validados mesmo durante a transição. A obrigatoriedade
integral começa no fechamento R12. Aceite editorial é separado do gate técnico.

A fonte é `ambiente_fonte/`; o simulado é gerado, não editado. O Manual da raiz
é cópia sincronizada. Não publicar workspace como efeito da documentação.

## Alternativas consideradas

README por arquivo físico multiplicaria explicações de um mesmo objeto.
Introdução teórica longa em todo notebook esconderia a decisão de escolha.
Um catálogo central mais extenso não daria autonomia ao leitor de cada pasta.
Geração paralela sem piloto propagaria a mesma interpretação ruim aos lotes.

## Consequências

Há mais documentação a manter e links a conferir. O custo é controlado por
contrato único, mudanças pequenas em documentos compartilhados, testes de
estrutura e checkpoints. O validador não prova correção estatística nem
acolhimento didático. A revisão independente continua pendente até ocorrer.

Esta proposta complementa a anatomia do ADR-0007 e preserva o ADR-0010; seus
corpos aceitos não foram reescritos. R01 entrega candidata; R02 testa seis
objetos antes do congelamento do molde.

## Referências

- [Pasta de objeto — ADR-0007](ADR-0007-catalogo-e-pasta-de-objeto.md).
- [Manual — ADR-0010](ADR-0010-manual-tecnico-unificado.md).
- [Migração e checkpoint](../sprints/readmes_objetos/README.md).
