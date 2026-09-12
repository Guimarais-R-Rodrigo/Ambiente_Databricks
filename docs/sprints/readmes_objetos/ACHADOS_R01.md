# R01 — achados e tratamento delimitado

Data: 2026-09-12. Autor e revisor: Codex, mesma sessão. A revisão é estática e
os testes descritos no relatório são locais. Não é auditoria independente.

## A01 — contagens anteriores desatualizadas no README da raiz

O baseline do snapshot `399bb553b250e5f7fcb8d727b829bb25678bbda2` falhou em duas
linhas do README: identidade dizia 846 e o gate contava 865; links dizia 387 e o
gate contava 416. O snapshot inclui o Concierge experimental, que é anterior à
R01 de conteúdo. Tratamento: regenerar somente as linhas locais, com a execução
real após o fechamento do diff. Não alterar o bloco de verificação remota como
se houvesse nova publicação Databricks.

## A02 — `decidivel` é uma política de tamanho de base

No exemplar `taxa_resposta_campanha`, a implementação calcula esse campo com
`contatados >= minimo_para_decisao`. Não representa significância, suficiência
causal nem autorização de negócio. Tratamento: README explica a regra e uma
nota datada no notebook corrige a interpretação sem editar a saída histórica.
O limite superior de um intervalo de Wilson também não é um teto absoluto da
taxa verdadeira. A fórmula não foi modificada.

## A03 — parâmetro declarado e não utilizado

`checar_base_campanha` inclui `pct_nulo_alerta` no dicionário de limites, mas não
usa esse valor para decidir o status: qualquer nulo na resposta produz falha.
Tratamento: README identifica a limitação; não promete tolerância configurável.
A implementação não foi modificada. Mudança de comportamento exige outra tarefa.

## A04 — base vazia e semântica de chave exigem cuidado

O mesmo script não bloqueia explicitamente base vazia; `countDistinct` e contagem
de linhas também não permitem tratar toda diferença como duplicação pura quando
existem chaves nulas. Tratamento: README orienta contagem independente, qualidade
de chaves e interpretação do diagnóstico. Nenhuma validação nova foi injetada no
helper como efeito colateral da documentação.

## A05 — efeitos do exemplo diferentes dos efeitos do helper

Os exemplos de campanha usam tabelas persistentes sintéticas com sobrescrita;
o script de checagem remove sua tabela de exemplo ao final. “Temporária” no
sentido coloquial do texto antigo não equivale a uma view temporária Spark.
Tratamento: aviso antes do link de execução e nota documental, sem mudar destinos
ou modos. O exemplo de prompt também precisa conferir se sua tabela será criada.
Não houve escrita em workspace nesta sessão.

## A06 — saída histórica e custo não revalidados

Há transcrições parciais ou inconsistentes no exemplo de checagem. O número de
chamadas de coleta não prova custo constante nem uma contagem universal de scans.
Tratamento: não usar esses registros como saída recém-executada; apontar a
limitação e pedir reexecução controlada em uma etapa de runtime autorizada.
Os blocos históricos permanecem intactos, com uma ressalva acrescentada.

## A07 — pedido a uma IA não garante uma resposta válida

O exemplar de prompt solicita análise e código. Isso não prova execução nem
estabelece desenho de identificação causal. Tratamento: README separa entrega
solicitada, evidência observada e decisão humana. O bloco colável original não
foi alterado. Uma revisão do conteúdo desse prompt fica fora da R01.

## Decisão sobre os achados

A01 é corrigido no escopo documental. A02–A07 recebem delimitação e alertas, não
mudanças analíticas. Pendências de runtime não são tratadas como testes aprovados.
O leitor pode estudar os exemplares sem precisar executar os notebooks.
