# V02 — núcleo de temas, validação e resolução

> **ACEITA E INTEGRADA · PR #14 · 12/09/2026.** Rodrigo concedeu aceite explícito
e a V02 foi integrada à `main` no commit
`d4cabdca4ac68c0a2edbd7f9f621f68962c8f6b8`. Os quatro checks pós-merge passaram.
Isso não equivale a publicação no Databricks nem a homologação operacional.

Para quem nunca entrou no Hub: o visual e sua rotina continuam iguais. A nova
capacidade confere dados de uma proposta sem desenhar gráficos. Comece pelo
[guia operacional](../../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).
Não há seletor para procurar, tabela para consultar ou pacote para publicar nesta etapa.

## Escopo entregue

Objeto `hub_snippets.visual.tema`, schema promovido sem alteração dos bytes,
validação compartilhada com o verificador V01, dados imutáveis, leitura local com
raiz explícita, hashes, exportação em memória e referências legadas versionadas.
Ajudas, erros, exemplo sintético e catálogo integrado do Manual acompanham o código.
A fachada é gerada pelo extrator AST existente, não por uma seleção manual.

Os adaptadores Plotly/HTML continuam na V03/V04; nenhum consumidor legado passa a
usar o novo núcleo implicitamente. Não existem herança, cache global, busca remota,
aprovação autodeclarada, publicação, serviço multiusuário ou App nesta entrega.

## Decisões de implementação dentro do ADR-0013

`jsonschema`/`referencing` são dependências explícitas de validação, não dependências
no import. Reutilizamos o schema e o código de validação no verificador V01, sem
implementar um validador paralelo. A normalização de cores é uma ação de autoria
separada; importar minúsculas onde o contrato exige maiúsculas continua reprovando.
Não há precedência entre perfis: todos os valores são explícitos no documento.
Não introduzimos cache antes de haver uma necessidade e uma medição reais.

O arquivo `theme.schema.json` saiu da V01 para o padrão do produto. A referência
textual é gerada. As fixtures V01 e seus relatos continuam históricos; suas cópias
publicadas e o manifesto relativo têm equivalência conferida por testes.

## Testes, evidências e continuidade

[Checkpoint](CHECKPOINT_V02.md) registra escopo, validação observada e pendências.
[Testes e reprodução](TESTES.md) liga famílias de risco aos comandos. Não somar
reexecuções como novos casos. O CI e a inspeção pelo mesmo agente não substituem
auditoria independente, teste com iniciante ou homologação no Databricks.

A candidata remota foi integrada pelo PR #14. Antes do merge, o head
`cda22c2963660ecd94e77698fcd7a5e56eca7092` passou CI geral, regressões V00,
contrato V01 e núcleo V02. O merge preservou exatamente a mesma árvore da candidata,
e os quatro checks de push na `main` também concluíram com sucesso.

Integração Git, publicação e homologação no Databricks continuam sendo gates
separados. A V02 está integrada apenas no Git; a V03 ainda não foi iniciada.

[Voltar à iniciativa](../README.md)
