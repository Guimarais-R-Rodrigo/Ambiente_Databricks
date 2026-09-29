# Plano de paralelização da candidata de laboratório

**Data:** 2026-09-29. **Estado:** planejado; nenhum agente foi iniciado por este plano.
**Objetivo:** concluir a revisão e as correções proporcionais da candidata MM04–MM13-LAB, preparando um checkpoint de aceite com evidências e pendências explícitas.

## Base e autoridade

Base observada: branch `micromodelos/autonomia-local-v2`, commit `faeffc99ba1fa61f257e0663f7c0274edf73135f`, tree `333776fd2e59ef371a94190ff3cb2a739c86f89d`. O coordenador registra HEAD/tree e estado local novamente ao iniciar a execução. Alteração do código durante a primeira revisão exige identificar o delta e atualizar somente as revisões afetadas.

O [plano operacional de laboratório](PLANO_EXECUCAO_LAB.md) governa esta missão: entregas incrementais, testes proporcionais e revisão por autor diferente. Freeze/FULL/bundle não são pré-requisitos automáticos de cada alteração de laboratório. A [matriz MM04](MATRIZ_LOCAL_MM04.md) é apoio proposto para uma eventual certificação formal, não obrigação adicional aceita por este plano.

CI remoto permanece adiado por falta de saldo. O trabalho usa código e fixtures locais; os relatórios Free existentes são evidência histórica. Homologação E2, publicação institucional, promoção L3 e migração real não integram este fechamento de laboratório. MM08–MM13 corporativas continuam com seus próprios pré-requisitos.

## Equipe: quatro agentes ativos no máximo

| Papel | Responsabilidade | Entrega |
|---|---|---|
| Coordenador/integrador | Fixar snapshot e escopos, preparar evidências, inspecionar interfaces B1, consolidar achados, executar integração e validação final. | Registro único de achados, delta de integração e checkpoint de fechamento. |
| Agente A — produto e prompts | Revisar MM04–MM05: skill, contrato estático, dois prompts/READMEs/exemplos, fluxo E0 e respostas Genie. Conferir metadata-only, injeção, proveniência, YAML/schema, ausência de score inventado e policy por handoff. | Pareceres separados MM04/MM05; classificação das ressalvas P1/P2c e das falhas históricas P2/P2b. |
| Agente B — execução e transporte | Revisar MM06–MM08-LAB: artefatos, MLflow, adapter, kit portátil e comandos Free. Conferir retrocompatibilidade, agregados, allowlist, dependências, escopo e diferença entre código local e capacidade instalada. | Parecer de execução/transporte com riscos reproduzíveis e limites E0/E1/E2. |
| Agente C — piloto e consumidores | Revisar MM09–MM13-LAB: piloto sintético, scoring, handoff, equivalência fictícia, catálogo/impacto e limites MM11. Conferir contra-evidência, indeterminado, reconciliação, identidade material e ausência de autopublicação. | Parecer por capacidade, identificando o que é validado em laboratório e o que depende do piloto corporativo. |

A primeira rodada usa revisores novos, distintos dos autores dos arquivos revisados. Não reutilizar automaticamente os agentes anteriores de produto/runtime como revisores independentes de sua própria implementação. Revisão por agentes da mesma equipe não equivale a auditoria institucional externa.

## Etapa 1 — preparação serial

O coordenador:

1. Confirma árvore, branch, hashes e alterações alheias. Define o snapshot exato de leitura, sem declarar freeze formal.
2. Fornece a cada revisor `CLAUDE.md`, índice operacional, regras pertinentes, plano de laboratório, seu diff e os relatórios necessários. Revisores devem examinar código e evidência, não aceitar o veredito do integrador por declaração.
3. Usa o [smoke local](SMOKE_LOCAL_SEM_CI_MM04_2026-09-29.md) como histórico de testes, incluindo erro inicial de encoding e skip. Configura `PYTHONUTF8=1` para testes com subprocessos Windows.
4. Informa escopo de arquivos, restrições e formato de retorno. Nenhuma nova consulta Databricks é necessária para esta etapa.

## Etapa 2 — três revisões simultâneas

A, B e C leem o mesmo snapshot. A primeira rodada não modifica produto, testes, Git ou relatórios compartilhados; os pareceres retornam ao coordenador por mensagem. Cada revisor pode reproduzir um risco específico em diretório temporário isolado. Testes que regeneram o produto, usam paths fixos ou modificam arquivos compartilhados são encaminhados ao coordenador para execução serial.

Em paralelo, o coordenador inspeciona B1 apenas para mapear diferenças em skill, policy, instruções e empacotamento. Registra conflitos e um patch proposto sem copiar sobre o checkout compartilhado. Também identifica documentos vivos desatualizados: por exemplo, afirmações de Genie ainda pendente em `CLAUDE.md` e de prompts sem reteste em `PLANO_EXECUCAO_LAB.md`. Registros históricos preservam seus resultados originais.

Formato obrigatório de cada achado: ID A/B/C + número, commit examinado, arquivo/linha, requisito aplicável, impacto concreto, reprodução/evidência, correção sugerida e teste que demonstraria o fechamento. Separar defeito de produto, lacuna de evidência, documentação desatualizada e pendência ambiental. Todo teste informado inclui comando, exit code, resultado e skips; uma inspeção sem execução é declarada como tal.

A revisão termina com escopo coberto, achados priorizados e limites. Se não houver achados, declarar também o que não foi verificado. P1/P2c não apagam FAILs históricos nem certificam automaticamente a PR inteira.

## Etapa 3 — triagem serial e correções em paralelo

O coordenador verifica os achados e fixa uma lista de correções justificadas. Divergências são resolvidas pela evidência e pelo contrato vigente. Mudanças materiais de arquitetura, semântica ou autoridade seguem os gates já aceitos do projeto.

Se os achados forem independentes, até três agentes corrigem em paralelo, com propriedade exclusiva dos arquivos:

| Responsável | Arquivos que pode alterar na rodada de correção |
|---|---|
| A | Skill `hub-ml-micromodelos/`, prompts `micromodelo_novo/` e `descobrir_micromodelos/`, `tools/micromodelo_mm04_flow.py` e seu teste. |
| B | `hub_snippets/ml/mlflow_run/`, ferramentas MM06/MM07, `micromodelo_free_kit.py`, `tools/free_kit/` e respectivos testes. |
| C | Ferramentas MM09/MM10/MM12/MM13 e respectivos testes. MM11 fica limitado à classificação de lacunas do ensaio. |
| Coordenador | Policy, instruções globais, índices, `project_policy.py`, validadores, changelog e relatórios consolidados. Contratos MM01–MM03 exigem análise de impacto antes de alteração. |

O coordenador transforma os grupos acima em allowlists de arquivos exatos antes de qualquer escrita. Arquivo não atribuído permanece somente leitura. Alterações de interface entre grupos são acordadas antes dos patches dependentes; consumidores esperam a assinatura estabilizar. No mesmo checkout não há checkout/reset/stash/rebase nem Git concorrente. Se a correção exigir isolamento Git, o coordenador prepara checkout separado antes de iniciar aquele agente.

Cada correção retorna delta, testes focais e riscos remanescentes. Apenas o coordenador atualiza o changelog consolidado. O autor de uma correção não é seu aprovador final: rechecagem por outro agente, por exemplo B revisa A, C revisa B, A revisa C. O revisor cruzado recebe o requisito e a reprodução original, além do patch.

## Etapa 4 — integração e checkpoint serial

Com os agentes sem escrever, o coordenador:

1. Consolida os patches e os pareceres por sprint; reavalia mudanças de main e das interfaces B1. Só aplica a reconciliação B1 em janela segura, preservando mudanças alheias; indisponibilidade dessa janela bloqueia essa integração, não as revisões da candidata.
2. Atualiza documentos vivos e registra `(Codex)` no changelog. Executa renderer somente se houver delta na fonte; nunca edita o simulado à mão.
3. Executa `python -B tools/validate_assistant.py --root ambiente_fonte`, testes focais dos deltas e regressões justificadas pelas interfaces alteradas. Uma bateria ampla já aprovada não é repetida por cada agente.
4. Confere o espelho fonte/derivado quando aplicável e registra SHA/tree, resultados, skips e pendências. CI remoto continua com seu status real.
5. Entrega checkpoint de laboratório: escopo implementado, revisão por sprint, achados corrigidos/pendentes, evidências E0/E1 e fronteira E2. O aceite final e a integração Git são decisões posteriores sobre esse resultado concreto.

## Critério de conclusão desta rodada

- Três pareceres entregues contra snapshot identificável, cobrindo os grupos da PR #116.
- Achados materiais reproduzidos e corrigidos, ou pendência explícita com impacto e responsável; nenhum bloqueador do escopo declarado escondido em ressalva.
- Correções verificadas por agente diferente do autor; contratos compartilhados e renderer integrados serialmente.
- Validador e testes proporcionais aprovados, skips justificados e falhas históricas preservadas.
- Checkpoint permite ao usuário avaliar o aceite do laboratório. Homologação corporativa, publicação, V1 e migração real mantêm seus gates próprios.

## Ganho esperado e dependências

A maior economia vem da primeira leitura dos três grupos e de correções sem arquivos comuns. O tempo dessa leitura tende ao grupo mais demorado, em vez da soma dos três. Preparação, triagem, alterações compartilhadas, renderer, reconciliação B1 e checkpoint permanecem no caminho sequencial; não há base para prometer ganho de três vezes ou prazo fechado antes dos achados.

Este plano está pronto para despacho. Ele não iniciou agentes, não publicou arquivos no Free e não solicitou execução de GitHub Actions.
