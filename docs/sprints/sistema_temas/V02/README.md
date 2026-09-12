# V02 — núcleo de temas, validação e resolução

> **CANDIDATA REMOTA EM REVISÃO · PR #14 · 12/09/2026.** A V01 está aceita e
> integrada. O núcleo funcional da V02 já passou pelos gates remotos no commit
> `921f898cbae859b8f6a91862a7b65291c9806906`; alterações documentais posteriores
devem repetir os checks antes do aceite. Este registro não concede merge nem publicação.

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
aprovação autodeclarada, publicação, serviço multiusuário ou App nesta candidata.

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

A candidata remota vigente está na branch `codex/temas-v02-review-20260912`, ligada
ao PR #14. O commit funcional `921f898c…` foi transportado por bundle verificado e
teve CI geral, regressões V00, contrato V01 e núcleo V02 aprovados remotamente. O
transporte auxiliar não integra a PR. A branch `codex/temas-v02-implementacao` e os
baselines anteriores permanecem como rastreabilidade histórica, não como ponto de
operação para quem revisa a entrega atual.

Só um merge explicitamente autorizado altera a `main`. Mesmo depois de integrar no
Git, publicação e homologação no Databricks continuam sendo gates separados. A V03
não foi iniciada.

[Voltar à iniciativa](../README.md)
