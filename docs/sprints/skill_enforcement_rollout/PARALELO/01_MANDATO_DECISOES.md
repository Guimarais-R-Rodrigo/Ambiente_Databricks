# 01 — Mandato, baseline e decisões de desenho

## 1.1 Autorização recebida e fronteira desta entrega

O usuário aprovou a proposta de 23/09/2026 e solicitou: “siga para montar o plano de forma extremamente bem detalhada com o intuito de evitar derivas e idas e vindas de correções que poderiam ser evitadas”. A autorização cobre o detalhamento da mudança de rota. Ela não contém uma lista de novos SHAs aceitos, destinos de escrita externos ou promoções antecipadamente aprovadas.

A arquitetura aprovada é preservada: oito frentes lógicas por skill, autoria repo-side, execução local paralela limitada, revisão independente e integração/publicação serializada. O plano não é uma delegação de desenvolvimento ao Codex local. Havendo lacuna de implementação, o item retorna à fila de autoria aqui.

O usuário não precisa responder repetidamente a perguntas técnicas que a inspeção e a autoria possam resolver. Questões realmente materiais — população real, destino, overwrite, efeito remoto, scope ou target — são consolidadas num formulário único por lote antes do respectivo gate. Ausência dessas decisões bloqueia o efeito correspondente, não todo o trabalho independente.

## 1.2 Baseline e fontes de verdade

A ref `main` foi consultada no GitHub e apontou para `d2988e97e7b6c5fe1fd561852e947a155c2d731b`. O plano aprovado usa a mesma base. Não confundir cabeçalhos históricos de SER00 com a `main` vigente; os documentos SER00 preservam bases mais antigas.

Hierarquia preservada: `CLAUDE.md` → `.claude/CLAUDE.md` → regras pertinentes → decisões aceitas → especificação desta campanha → pacote executável de cada skill. `AGENTS.md` continua adapter fino. O novo adendo explicita a exceção de paralelismo e da divisão de papéis; não reescreve decisões aceitas nem cria autoridade maior que a do usuário.

`ambiente_fonte/` é fonte de produto; `Novo_Ambiente_Simulado/` é derivado. Workspace Free é cópia operacional. A biblioteca de evidências externas não se torna fonte de código. Nenhum segredo, matrícula ou path corporativo é versionado. Dados das campanhas são sintéticos e os efeitos remotos, quando aprovados, pessoais.

## 1.3 Vetor de capacidade a preservar

| Skill | Current na baseline desta frente | Target | Tratamento |
|---|---|---|---|
| hub-ml-criar-objeto | L3 | L3 | Regressão; SER01 integrada |
| hub-ml-eda-profissional | L4 | L4 | Regressão; preservar enforce |
| hub-ml-auditoria-skills | L3 | L3 | Regressão e adapters de verificação explicitamente aprovados |
| hub-ml-concierge | L1 | L1 | Regressão de descoberta e handoff |
| hub-ml-comentar-notebook | L1 | L1 | Regressão editorial, preservação de código |
| hub-ml-tutor-databricks | L0 | L0 | Regressão proporcional, sem runner artificial |
| hub-ml-explainability | L0 | L3 | SER02 |
| hub-ml-analise-safra | L0 | L3 | SER03 |
| hub-ml-validacao-estatistica | L0 | L3 | SER04 |
| hub-ml-cross-eda-ml | L0 | L4 | SER05 L2; SER06 L4 |
| hub-ml-feature-engineering | L0 | L4 | SER07 L2; SER08 L4 |
| hub-ml-baseline-ml | L0 | L4 | SER09 L2; SER10 L4 |
| hub-ml-monitoramento-modelo | L0 | L4 | SER11 L2; SER12 L4 |
| hub-ml-pipeline-builder | L0 | L4 | SER13 L2; SER14 L4 |

O vetor é premissa de planejamento, a ser confirmado pelo preflight da futura candidata; não é permitido recalculá-lo a partir da própria policy modificada e chamar isso de aprovação. O arquivo de autorização conterá a projeção `before` e a projeção `allowed_after` nominalmente. A cardinalidade 14 é da baseline; MM04 não pode aumentá-la incidentalmente nesta frente.

## 1.4 Mudanças explícitas em relação à execução antiga

**DEC-P01 — Ordem de execução.** Substituir a espera universal pela integração anterior por dependências declaradas. Manter as etapas L2→L4 e os identificadores históricos. Skills independentes podem ser implementadas aqui e testadas localmente antes de a anterior ser integrada. Integrar candidatas somente depois de revisão, reconciliação e autorização própria.

**DEC-P02 — Unidade de autoria.** Um dossiê completo inclui código, testes e decisões, não apenas um prompt. `AUTHORING_READY` exige evidência de verificações de autoria no ambiente em que forem possíveis e lacunas ambientais explicitamente separadas. Se a autoria aqui não tiver runtime adequado, registrar `AUTHORING_RUNTIME_NOT_RUN`; não chamar o primeiro ensaio local de certificação.

**DEC-P03 — Dois regimes locais.** Diagnóstico pode reunir falhas independentes predefinidas, sem alterar arquivos nem repetir o mesmo comando. Certificação é uma execução por candidato/rodada, com freeze e sem retry-until-green. A primeira falha é preservada nos dois regimes.

**DEC-P04 — Motor único.** Uma infraestrutura comum de campanha, com perfis declarativos e adapters de domínio finos. Não criar um certificador particular para cada skill. Não criar um runner analítico universal copiando cálculos dos helpers.

**DEC-P05 — Integração em lotes pequenos.** Um lote inicial pode conter no máximo duas skills; depois do piloto, até três, desde que o vetor de autorização e o conjunto de dependências estejam fechados. Um aceite pode abranger um vetor explícito de várias skills, mas não autoriza membros ausentes, efeitos diferentes nem fases L4 ainda não aceitas. Não usar “aceito o lote” sem identificador/digest da proposta que delimita o lote.

**DEC-P06 — Observabilidade.** Relato de seleção/carregamento de skill é distinto de evento observável. Ausência de telemetria recebe `NOT_OBSERVABLE`; o critério não é flexibilizado depois do resultado. A decisão histórica da SER01 não é apagada, mas seu uso de narrativa não será reproduzido como padrão probatório.

**DEC-P07 — Recursos.** Duas frentes no piloto; três slots de skill após prova de isolamento. Dois slots de auditoria, máximo cinco subagentes ativos e um coordenador, sujeitos a limites mais baixos do host/cliente. Threads de IA e processos pesados são quotas diferentes.

**DEC-P08 — Escopo externo.** Um publicador por workspace/pacote. Workers não compartilham credenciais Free. Nenhuma ação corporativa, compra, agendamento produtivo, modelo real de clientes ou concessão de permissão integra esta campanha.

**DEC-P09 — Política.** `current_level` só muda depois das provas pré-policy aplicáveis e de autorização específica da proposta. `target_level`, `scope_mode`, `rollout_mode` e `execution_contract.mode` não mudam por efeito colateral. O ato de promoção deve ser seguido de render, freeze e certificação do SHA final.

**DEC-P10 — Sem defeito conhecido no handoff.** Uma falha de autoria já identificada é corrigida aqui antes de delegar. Não enviar teste sabidamente stale, literal inválido, símbolo inventado ou número estimado esperando que o laboratório encontre o erro.

## 1.5 O que não muda

Sem rebase/amend/force sobre candidata congelada; sem normalização ampla de bytes para ocultar divergência; sem remoção de resultados históricos; sem mudança de teste para obter verde; sem confundir geração, validação, autorização, escrita, homologação e publicação; sem assumir Windows a partir de Linux, nem Free a partir de mock.

A política permanece por superfície, operação, tipo, host e efeito. Um helper existente não prova L3. Um Receipt de integridade não prova execução. Um dry-run não prova materialização. Um Postflight que retorna PASS sem observar a conclusão protegida não prova L4.

## 1.6 Não criar um projeto de plataforma desnecessário

A implementação inicial deve ser biblioteca/CLI pequena, schemas, perfis e relatórios, usando Python e dependências já aceitas quando adequadas. Não criar serviço de fila, banco de dados, painel web, broker remoto, SDK próprio de agentes ou DSL com expressões. Se surgir necessidade de novo componente, documentar o problema que o exige e seu teste discriminante antes de expandir B0.

O propósito é eliminar decisões improvisadas e repasses repetidos, não aumentar documentos sem consumidores. Toda regra normativa tem um dono; templates e resumos apontam para ele.

## Nota de rota — 06/10/2026

A hierarquia registrada em §1.2 descreve a baseline daquela campanha. A manutenção
corrente segue AGENTS.md e docs/ai, conforme ADR-0025; esta nota não altera os
resultados, autorizações, templates não executáveis ou demais decisões da campanha.
