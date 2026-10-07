# ADR-0027 — Correção dos controles após auditoria integrada

Data: 2026-10-07
Status: Implementação local autorizada; publicação e homologação separadas
Autor: Codex, execução das correções da auditoria integrada
Autoridade: pedido do usuário “Corrija todos em sequência de prioridade”, em 07/10/2026 UTC
Base: `2c5975c0718ef9e30ec3fc26998338036262e87c`

## Contexto

A revisão conjunta de documentação, instruções IA e arquitetura identificou
15 itens priorizados, além da falha histórica SER. Há defeitos condicionais de
contenção, lacunas de regressão, documentação divergente e uma rota MM01
congelada incompatível com a árvore corrente. O produto executável preservado e
o CI da base não eliminam esses achados; mutantes aceitos também não demonstram
falha real de todos os ambientes. O risco conhecido dos nomes no manifesto de
contexto recebe mitigação adicional, com escopo explícito.

## Decisão

1. Recusar hardlinks dos destinos/manifesto IA e symlinks da raiz e ancestrais
   lexicais da fonte antes da primeira mutação. Preservar bytes externos e a
   saída anterior nos casos recusados. As verificações pressupõem checkout
   exclusivo; não afirmam contenção contra troca concorrente de filesystem.
2. Conferir receitas compartilhadas do CI por passos ordenados, únicos e
   incondicionais, comandos e ambiente exatos. Manter todos os checks legados,
   dependências fail-closed, permissões e matriz Python do kit. Alterar o
   contrato exige revisão conjunta da receita e de seus negativos.
3. Inventariar entradas nativas IA com mecanismo, owner, condição, conteúdo e
   shadowing declarados. Extensões legítimas podem ser revisadas e registradas;
   arquivo novo não ganha autorização nem comprova suporte de cliente.
4. Proteger correspondência granular das obrigações e claims com inventário
   versionado, fonte Git imutável e vinculação das paráfrases aos snapshots.
   Evolução explícita do contrato não reescreve o passado nem congela para
   sempre a contagem de entradas. Links usados pela camada IA recebem
   verificação das formas Markdown suportadas; links HTML e extensões de
   renderizador exigem revisão específica, fora do subconjunto do parser.
5. Separar a identidade AST dos métodos core da prova de execução. O runner
   deve observar cada ID protegido exatamente uma vez, sem skips inesperados,
   mantendo intactos o serializer tipado e os hashes históricos existentes.
6. Corrigir rotas, ajuda, catálogo e estados documentais no owner atual. CI
   remoto deve ser datado e vinculado a SHA; B0 continua uma suíte própria com
   referência CPython 3.12. Verde do kit não prova B0 cross-version.
7. Manter MM01 v1 como rota congelada, com diagnóstico read-only de todos os
   inputs e procedimento corrente separado. A falha SER pré-promoção conserva
   teste, policy L3 e linhagem. Nova certificação requer versão/reconciliação
   específica, em vez de atualizar pins para produzir PASS.
8. Acrescentar ao modo `task` o perfil opt-in `selected-only`: omitir nomes
   fora da seleção do sidecar, mantendo contagens, identidade dos incluídos e
   bytes do corpo. O perfil detalhado `audit` preserva compatibilidade local;
   os modos `canonical`, `security` e `full` mantêm sua semântica. Redução de
   metadados não é anonimização nem autorização para transmitir arquivos.

## Consequências e limites

Os guardas detectam as regressões demonstradas e permitem mudança deliberada
com revisão. Não são defesa contra um mantenedor autorizado a reescrever os
próprios controles. O escopo continua local, sem instalar dependências,
publicar, fazer merge, alterar permissões/policy ou promover qualquer destino.
Arquivos gerados continuam sob seu gerador canônico; histórico e evidência
congelada não são reclassificados.

CPython 3.11/3.12, Windows nativo, clientes IA, Spark/Databricks, acessibilidade
e auditoria institucional exigem suas provas específicas. Uma execução local
3.12 não substitui a matriz real 3.11 nem o aceite de outro ambiente. Revisão
não-autora coordenada na mesma origem não equivale a A1 independente.

## Verificação e reversão

Cada achado tem positivo e contracaso, com comandos, retorno, SHA e limites.
Reexecutar o agregado, FULL SE08 separado, B0, fronteira do pacote e paridade
após integrar os lotes; registrar skips e falhas históricas literalmente.
Comparar bytes de runtime, assets, licenças e snapshots com a base. Nenhum FAIL
histórico ou bloqueio de ambiente justifica relaxar um gate atual.

Reverter o commit específico com revisão de dependências, preservando trabalho
alheio; reverter juntos schema, gerador, testes e documentação quando ligados.
Regenerar derivados no destino isolado e repetir os gates afetados. Reverter
Git não desfaz uma publicação em outro ambiente, que exige seu próprio runbook.

## Owners

- [Controles IA](../ai/README.md) e [contexto por tarefa](../ai/task-context.md)
- [Saída gerada e CI](../manutencao/saida-gerada.md)
- [Fingerprint e execução core](../manutencao/fingerprint-core.md)
- [Certificadores congelados](../manutencao/certificadores-congelados.md)
- [ADR-0025](ADR-0025-arquitetura-instrucoes-ia.md) e [ADR-0026](ADR-0026-arquitetura-projeto-e-historia.md), preservados
