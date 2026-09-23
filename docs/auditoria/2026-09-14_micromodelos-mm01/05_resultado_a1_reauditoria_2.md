# MM01 — Terceira reauditoria independente A1

## Natureza deste registro

Este arquivo preserva o resultado histórico da terceira auditoria independente A1 da MM01. Ele registra o que o auditor concluiu na árvore examinada naquela rodada. Correções posteriores não alteram retroativamente este veredito e não transformam os achados abaixo em `PASS`.

## Veredito histórico

**VEREDITO: APTA_COM_CORRECOES**

- `QUEBRA`: 0
- divergências bloqueantes confirmadas: 3
- merge/aceite da MM01: não autorizado por esta auditoria

## DIVERGE-01 — `$defs.material_ref` exigia ASCII

O schema ainda usava uma regra equivalente a `.*[A-Za-z0-9].*`, enquanto o validador semântico aceitava letra ou número Unicode após NFKC. Isso criava duas autoridades incompatíveis para materialidade textual.

O auditor demonstrou falsos negativos multilíngues: referências legítimas como `é`, `文档`, `١` e texto em Devanagari eram rejeitadas pelo schema. Em contraste, uma forma como `Café`, contendo caracteres ASCII e combining mark, conseguia satisfazer a regex.

A correção exigida foi unificar a política: materialidade deve significar presença de pelo menos uma letra ou número Unicode real após normalização, sem ampliar uma regex ASCII como segunda fonte de verdade.

## DIVERGE-02 — proveniência de topo escapava da materialidade

Os campos auditáveis de proveniência de topo `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo` aceitavam conteúdo materialmente vazio.

Foram exercitados casos compostos por U+034F, U+FE0F, U+0301, U+093E isolado, U+20DD, U+200B, U+200C, U+200D, U+2060, NBSP, EM SPACE, pontuação, símbolos e combinações desses caracteres.

A correção exigida foi submeter esses campos à mesma política de materialidade apropriada às demais provas auditáveis.

## DIVERGE-03 — gates de conteúdo material aceitavam strings visualmente vazias

Campos materialmente relevantes ainda podiam satisfazer o schema apenas por `minLength`, inclusive com whitespace, pontuação pura, símbolos ou zero-width. O achado alcançou ao menos:

- `classificacao.semantica.quando_true`, `quando_false` e `quando_indeterminado`;
- `validacao.criterios[]`;
- `fontes[].schema`, `fontes[].objeto` e `fontes[].campos[]`;
- `saida.estudo.campo_classificacao`;
- `saida.estudo.campo_score`, quando aplicável;
- `saida.publicacao.campo_booleano.nome`.

O auditor também registrou que a restrição não deveria ser aplicada indiscriminadamente a toda string: campos narrativos podem legitimamente conter pontuação/símbolos, enquanto identificadores, referências, nomes operacionais, semânticas obrigatórias e critérios materiais precisam de conteúdo efetivo.

## Condição para nova auditoria

A candidata precisava corrigir as três divergências, manter suporte multilíngue real, preservar os guardrails anteriores e voltar a uma auditoria independente. Esta A1 não declarou a MM01 aprovada e não autorizou MM02.
