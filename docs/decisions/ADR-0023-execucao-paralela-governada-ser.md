# ADR-0023 — Execução paralela governada do Skill Enforcement Rollout

Data: 2026-09-24  
Status: Aceito  
Autor: ChatGPT  
Origem: decisão humana explícita após integração da SER01 e retrospectiva do seu custo operacional.

## Contexto

O Plano Mestre SER definiu ordem numérica de integração e, operacionalmente, cada sprint partia da `main` após a anterior. A matriz de dependências já registrava que essa ordem não significava dependência funcional universal. A SER01 demonstrou que repetir infraestrutura, handoffs e certificadores particulares cria retrabalho evitável.

## Decisão

1. Preservar identificadores SER02–SER16, targets, superfícies e gates humanos existentes.
2. Substituir a espera universal entre frentes independentes por um DAG explícito de implementação, teste, efeito e integração.
3. Centralizar autoria de implementação, fixtures, testes, oráculos, profiles e command registry no repositório. Agentes locais executam/auditam tarefas fechadas; não redesenham a solução nem corrigem a candidata durante certificação.
4. Usar um mecanismo comum de campanha, fail-closed, declarativo e SHA-bound; adapters de domínio continuam finos e específicos.
5. Separar diagnóstico de certificação. Diagnóstico pode coletar falhas independentes predefinidas; certificação usa candidato congelado e não permite retry-until-green.
6. Preservar dependências L2→L4 da mesma skill e contratos compartilhados necessários. Paralelismo não autoriza salto de nível.
7. Integrar em lotes pequenos nominalmente definidos. Espaços compartilhados (policy, índices, snapshots, derivado, publicação Free) têm escritor serializado.
8. Preservar FAILs históricos e mapear toda cobertura SE08/CI/SER01 antes de declarar equivalência do mecanismo novo.
9. Manter efeitos remotos, promoção de policy e merge como autorizações humanas distintas.
10. Qualificar host, sandbox, modelos, locks e isolamento com dois pilotos antes de ampliar concorrência além de duas frentes.
11. Evidência diferencia declaração textual, evento observado, execução, efeito e verificação independente. Hash não autentica pessoa.
12. `ambiente_fonte/` continua fonte do produto; o orquestrador B0 fica em `tools/` e não é publicado no `.assistant`.

## Consequências

A ordem numérica SER passa a ser rastreabilidade e ordem candidata de integração, não bloqueio para autoria/execução independente. A integração final continua baseada na `main` reconciliada e exige certificação do composto. Uma falha de domínio bloqueia seus dependentes; uma falha compartilhada bloqueia os consumidores afetados.

O B0 não promove nenhuma skill. A execução paralela só é liberada depois de qualificação local e auditoria da infraestrutura comum.

## Relação com ADR-0022

Este ADR complementa o ADR-0022. Não altera a certificação prospectiva/aditiva, a preservação dos perfis históricos, a evolução de condições, a separação target/current nem a regra de recertificar a policy final após promoção.
