# Micromodelos — concluir a entrega local antes da transferência

> **Atualização de direção — 2026-09-29:** o responsável solicitou integrar o framework em `.assistant/hub_micromodelos/` e levar o ambiente inteiro, consolidado com a outra frente. O [plano de integração ao Hub](PLANO_INTEGRACAO_HUB_MICROMODELOS.md) governa essa próxima etapa e substitui a solução de runtime em ZIP técnico separado descrita abaixo. O kit anterior conserva suas evidências, mas não representa a entrega integrada final. O restante deste documento preserva a preparação anterior e os critérios aplicáveis.

**Data:** 2026-09-29. **Referência de execução:** PR #116 e o manifesto do kit final, ambos identificados por commit. Direção solicitada pelo responsável: preparar e auditar aqui uma candidata completa, transferir depois ao computador do trabalho e retornar defeitos para sprint local de correção.

Este documento é dono da preparação local restante. As portas corporativas continuam em [PLANO_PREPARACAO_E2.md](PLANO_PREPARACAO_E2.md). A entrega será uma **candidata local pronta para homologação**, conservando a skill L1/audit. Freeze V1, publicação e migração real continuam dependentes da sequência do plano mestre e do piloto institucional.

## Diagnóstico antes de ampliar a implementação

Três agentes fizeram inspeções paralelas somente leitura: transporte/runtime, gates e estratégia de testes. A referência inspecionada foi `d5f34acc26dd1dfe5ea255b18c37229ba67b1264`. CI da PR #116 conferido: 14 SUCCESS, SE02 SKIPPED. Essa evidência pertence a esse commit; a PR permanece Draft, sem merge.

| Lacuna comprovada | Evidência | Entrega necessária |
|---|---|---|
| Kit corporativo contém a skill e briefings, mas não schema/template MM01 nem módulos de execução. | `tools/kit_transicao_trabalho.py`, ZIP Hub em `.artifacts/kit-mm-e2-d5f34acc/`; paths exigidos em `tools/micromodelo_mm04_flow.py`. | Pacote complementar com allowlist fechada e paths relocáveis, fora da instalação `.assistant`. |
| Aceite genérico não exercita o fluxo Micromodelos. | `tools/aceite_trabalho.py`. | Entrada própria de aceite sintético, integridade antes dos imports, veredito por etapa. |
| Kit Free tem configuração e setup específicos do Free. | `tools/free_kit/RUN_FREE.py`, `SETUP_METADATA_FREE.py`. | Entrada de destino com tracking e metadata opcionais desligados, sem criação automática de tabelas ou instalação. |
| Dependências declaradas têm limites inferiores; não registram combinação reproduzida fechada. | `tools/micromodelo_free_kit.py`, `REQUIREMENTS`. | Versões testadas, capabilities mínimas e procedimento para dependências ausentes; instalações no destino dependem da política local. |
| Teste do kit Free executa a pasta de build; não executa o ZIP extraído. | `tools/tests/test_micromodelo_free_kit.py`. | Ensaio do artefato final extraído fora do checkout, sem imports acidentais do repositório. |

O ZIP corporativo já gerado é evidência de integridade do Hub; ainda não é a entrega completa do fluxo Micromodelos. As evidências E0/E1 existentes são preservadas. Não repetir testes de injection, metadata-only, score e tracking já cobertos sem mudança ou risco concreto.

## Trabalho paralelo e responsabilidade

Máximo de três agentes executores e um integrador. Cada implementação recebe revisão de outro agente; isso constitui revisão separada de autoria, não diversidade de modelos nem certificação externa.

| Frente | Responsabilidade e arquivos próprios | Saída verificável |
|---|---|---|
| A — transporte | Novo gerador complementar e seus testes; alterações no gerador corporativo somente com coordenação do integrador. | Runtime mínimo, schema/template, fixtures, manifesto com commit/hashes/tipos; rejeição de conteúdo ausente/corrompido. |
| B — execução e compatibilidade | Novo aceite Micromodelos, capabilities e respectivos testes. Mudanças em módulos existentes coordenadas antes de editar. | YAML e readback, fingerprint, greenfield sintético, classificação e score, handoff/reconciliação; etapas opcionais explícitas; diagnóstico de dependências. |
| C — operação e auditoria | Guia do pacote, matriz requisito→caso→evidência e formulário de retorno sanitizado. | Roteiro completo, backup/rollback, decisões pendentes; revisão inicial das interfaces e auditoria posterior do pacote entregue por A/B. |
| Integrador | Docs compartilhadas, CHANGELOG, renderer, Git, CI, composição final e interface B1/SE08. | Candidata de um único commit, achados resolvidos ou limites explícitos; uma entrega coerente. |

Primeiro, o integrador fixa layout, interfaces e allowlists. A e B implementam em paralelo; C prepara critérios e guia. Após integração, B revisa A, A revisa B e C ensaia o ZIP final usando apenas o guia e dependências declaradas. O integrador resolve achados e consolida evidências. Não editar o checkout B1 compartilhado nesta preparação.

## Sequência local e critério de saída

1. Completar o pacote complementar, a entrada de aceite e o guia único. Distribuir módulos necessários em área técnica própria; não publicar todo `tools/` como produto Hub.
2. Executar ensaio em diretório e ambiente Python limpos, a partir do ZIP extraído, sem checkout no caminho de imports. Verificar integridade antes da execução; cobrir paths com espaços, ausência/corrupção de arquivos, dependências ausentes e reexecução sem sobrescrever artefatos alheios.
3. Exercitar a jornada sintética completa suportada: briefing → YAML validado → fingerprint → estudo/validação sintéticos → tracking quando habilitado → handoff e reconciliação. Artefatos agregados fornecidos continuam `SUPPLIED_UNVERIFIED`; ambientes e capacidades não exercitados ficam explícitos. Não converter o laboratório em validação estatística real.
4. Reexecutar no Free apenas componentes alterados que dependam de Databricks; se o empacotamento mudar o caminho de execução, ensaiar esse novo caminho. Conferir bytes/readback. Retestes conversacionais apenas se o contrato/roteamento mudar ou houver falha específica; orçamento indisponível mantém o caso pendente.
5. Resolver todos os defeitos bloqueantes de instalação/execução e achados altos/críticos do escopo. Uma rodada de revisão independente da autoria e uma rechecagem focal dos achados; ampliar somente por falha ou risco concreto.
6. Consolidar alterações localmente, enviar um lote para CI e corrigir somente gates realmente falhos. Gerar a entrega definitiva do commit limpo/remoto aprovado, conferir hashes e associar resultados ao mesmo conteúdo. Repetir o aceite do ZIP final se algum conteúdo executável ou gerador mudar.
7. Emitir checkpoint **PRONTO_LOCAL_PARA_HOMOLOGACAO** somente quando o operador conseguir seguir o guia com os arquivos entregues, sem reconstruir partes do checkout, e todos os requisitos locais tiverem evidência ou limite aceito explícito.

Não há novo PASS presumido pelo planejamento. O aceite local existente não é revogado; esta etapa fecha a completude de entrega ainda ausente. Não gerar pushes de documentação intermediária apenas para atualizar status. Não reduzir gates exigidos para economizar crédito.

## O que levar e o que observar no trabalho

Entrega planejada: Hub, aceite genérico, pacote/aceite Micromodelos, guia único, manifesto e hashes, versões/capabilities testadas, relatório sintético, matriz de pendências E2, formulário de retorno e rollback. Nenhum identificador ou dado corporativo será preenchido aqui.

A primeira ida será para executar o roteiro pronto: conferir runtime/permissões, importar em staging autorizado, verificar integridade/tipos e repetir o aceite sintético. G2 (ativação/Genie), G3 (metadata real) e G4–G6 (dados, piloto/publicação/V1) conservam decisões próprias. Permissões, Unity Catalog, runtime real e autoridade institucional só podem ser comprovados no destino. Não é possível garantir que uma única ida encerre esses gates.

SE08 mantém `PROMOCAO_TRABALHO=BLOQUEADA`. Preparar localmente o dossiê de compatibilidade e decisão de rollout; não apagar dívida histórica SE06/SE07 nem transformar teste de código em evidência conversacional ausente. Se uma decisão humana continuar necessária, apresentar exatamente o impedimento e o escopo da decisão antes da transferência; staging e promoção permanecem distintos.

## Retorno para sprint de correção

No destino, guardar logs completos no canal autorizado. Devolver somente: versão/hash do pacote, etapa/caso, esperado versus observado, código de erro sanitizado, versões de runtime/dependências permitidas e reprodução sintética possível. Não exportar linhas, nomes reais, paths institucionais ou segredos.

Classificar o retorno em defeito do produto, incompatibilidade de runtime, configuração/permissão ou decisão de negócio. Para defeito reproduzível: criar regressão sintética → corrigir fonte → revisar patch por outro agente → testar componentes afetados → emitir nova versão completa e instruções de atualização/rollback. Retestar no destino o caso corrigido e suas dependências; ampliar somente quando o alcance da mudança exigir. Novas demandas de negócio viram backlog separado de defeitos da entrega.
