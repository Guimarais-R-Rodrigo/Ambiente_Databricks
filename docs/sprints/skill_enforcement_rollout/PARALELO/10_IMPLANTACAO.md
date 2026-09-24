# 10 — Implantação controlada, entregáveis e critérios de saída

## 10.1 Ordem do trabalho

Esta entrega detalha o plano. O próximo trabalho é autoria B0, não executar oito agentes sobre documentação sem implementação. O B0 constrói o mecanismo mínimo comum e seu mapa de cobertura. Em seguida, libera-se autoria dos domínios em paralelo lógico, executando localmente só os pacotes já prontos.

A execução de contratos L2 não precisa esperar todas as L3. Cada L4 depende do próprio L2 aceito e dos contratos compartilhados pertinentes. A integração continua controlada por lote e autorização. Não renumerar SER02–SER16 para esconder ou reiniciar as etapas históricas.

## 10.2 Pacotes B0 — entrega curta e limitada

| Pacote | Autoria repo-side | Evidência de saída | Condição que impede liberar |
|---|---|---|---|
| B0.1 Governança e inventário | Formalizar adendo; confirmar baseline, escopo e autoridades; apontar documentos donos | Decisões sem contradição e vetor nominal das skills | Regra sequencial antiga e paralela tratadas simultaneamente como obrigatórias |
| B0.2 Cobertura e contratos | Mapear SE08/CI/SER01 até métodos; schemas runtime fechados; catálogo de casos e command IDs | Requisito→teste→oráculo→evidência completo; inventário de métodos coletado | Suíte omitida, método sem justificativa, teste temporal misturado a atual |
| B0.3 Executor mínimo | Launcher, registry argv, process adapter, scheduler limitado, locks e result records | Smoke de comandos reais, logs separados, estados e limites de escrita | Comando arbitrário, mutação fora da allowlist ou globals compartilhados |
| B0.4 Verificador e empacotamento | Verificação independente, first-failure, RAW/SHARE, schema, integridade e coletor externo | Mutantes de certificado rejeitados; bundle não circular e seguro | PASS inválido, ERROR mascarado, referência ausente ou output fabricado |
| B0.5 Qualificação de host/cliente | Perfis declarados e probes de recursos, permissões e runtime | Ambiente identificado; limites escolhidos antes da certificação; ausência de secrets nos workers | Host desconhecido, sandbox só nominal, modelo/config inexistente |
| B0.6 Piloto do mecanismo | Dois cenários sintéticos independentes, um fail deliberado, dependente e publicação bloqueada | Concorrência sem colisão; falha propaga só ao necessário; relato humano coerente | Nova tarefa iniciada após stop global, retry oculto ou mistura de evidências |
| B0.7 Revisão de liberação | Auditorias técnica e probatória, metatestes e coverage review | Release do mecanismo marcada LOCAL_QUALIFIED, não skill promovida | Finding material aberto ou cobertura não fechada |

B0 não cria banco de dados, serviço web, fila distribuída, painel comercial, API própria de agentes, novo engine analítico ou módulo de deploy genérico. Persistência em arquivos/journal e processos locais é suficiente para esse escopo. Uma necessidade nova precisa demonstrar por que o mecanismo existente não resolve.

A autoria pode executar seus testes de desenvolvimento aqui quando o ambiente permitir; resultados são rotulados por host e fase. Teste que requer Windows/NTFS ou Free continua qualificação local/externa, não é presumido por um import Linux. Impossibilidade de reproduzir um host não justifica delegar ao laboratório um erro estático já conhecido.

## 10.3 Dossiê que autoriza entrada de uma skill

A saída de autoria de cada skill contém: implementação pronta, diff revisado, contrato/schema, fixtures reais versionadas, oráculos independentes, casos ligados a IDs coletáveis, tolerâncias numéricas, dependências/locks, perfil de execução, matriz operação×tipo×host×efeito, plano Free/Genie literal, definições de não aplicabilidade, critérios de auditoria e rollback.

Toda decisão não resolvida vira blocker identificado com owner e gate. O item não é AUTHORING_READY enquanto um blocker de sua fase estiver aberto. Os casos propostos nesta entrega especificam o que provar; as APIs exatas, métodos efetivamente suportados, bytes de fixtures e IDs Python precisam ser resolvidos pelo autor antes de enviar.

## 10.4 Piloto real de duas frentes

Depois do piloto sintético do mecanismo, a primeira dupla proposta é **análise-safra L3 (SER03)** e **cross-EDA L2 (SER05)**. A escolha testa duas naturezas diferentes — cálculo pandas com oráculo manual e contexto/preflight read-only — sem depender de deploy ou de treinamento externo. O adendo precisa estar formalizado para permitir essa ordem de execução.

A dupla só é lançada quando ambas tiverem pacotes completos. Não promove automaticamente nenhuma das duas. Se a autoria de uma não estiver pronta, usar outra frente independente igualmente preparada, com alteração versionada do manifesto antes do freeze. Não trocar a composição durante o piloto para ocultar um FAIL.

Aprovada a dupla, liberar até três execuções de skill simultâneas, com as duas auditorias dentro do teto global. O aumento exige metatestes de isolamento verdes, nenhum efeito não autorizado, nenhuma mistura de arquivos e nenhum finding material no piloto. Melhor velocidade não compensa violação de autoridade.

## 10.5 B1 — fila das L3 e contratos L2

Fila lógica: EX.L3, VF.L3, ST.L3, CE.L2, FE.L2, BM.L2, MO.L2, PB.L2. O scheduler usa prontidão e dependências, não uma ordem rígida pela numeração. Três slots não significam três instalações concorrentes de dependências nem três jobs Spark pesados: resource classes podem reduzir a concorrência efetiva.

A autoria deve priorizar contratos compartilhados que destravem múltiplos domínios, sem transformar isso em dependência circular. O contrato temporal comum pode destravar CE/FE; um modelo sintético versionado destrava EX/MO sem esperar baseline-ML promovida. ST só entra após fechar seu catálogo de métodos; escopo genérico é inválido.

Cada resultado LOCAL_PASS segue às auditorias. O resultado auditado segue ao lote externo pessoal. As demais frentes continuam localmente, sem esperar cada clique do usuário. A indisponibilidade de Free bloqueia EXTERNAL_PASS, não apaga a prova local do SHA observado.

## 10.6 B2 — avanços L4 por dependência própria

CE.L4, FE.L4, BM.L4, MO.L4 e PB.L4 só executam após seus L2 aceitos e os contratos/implementações necessários prontos. Preservar a regra de não saltar de orientação L0 diretamente para alegação L4.

A promoção intermediária L2 e sua integração continuam gates específicos. Desenvolvimento repo-side do L4 pode ser preparado contra contrato L2 estável e identificado, mas não é liberado como certificação L4 antes do aceite correspondente. Efeitos reais externos permanecem pessoais, sintéticos e autorizados.

Sem materializer ou executor real, limitar a superfície e registrar blocker; não trocar silenciosamente o target para declarar o plano concluído. A proposta de aceitar um escopo parcial é decisão humana explícita, com o restante mantido no backlog.

## 10.7 B3 — composição, promoção e SER15/SER16

Lotes de integração começam com no máximo duas skills/candidatas independentes e passam a três somente após prova do mecanismo. Cada lote define membros, níveis before/after, superfícies e effects; não contém todas as oito por conveniência se algumas não estão prontas.

Sequência: compor bytes aprovados; renderer/snapshot; freeze integrado; CI transversal completa e testes de interoperabilidade; auditoria; coleta externa pertinente na versão publicada; proposta humana de promoção; policy candidata como último ato funcional autorizado; nova certificação final e verificação externa proporcional; aceite humano de merge; confirmação de árvore/parents e publicação operacional conforme autorização.

Se a alteração pós-teste mudar somente a policy no escopo aprovado, conferir a policy publicada e os casos comportamentais sensíveis ao nível/autoridade. Não transportar a certificação inteira entre SHAs. Uma alteração de SKILL.md/runner/contrato exige reexecutar a prova comportamental e computacional afetada, conforme a matriz de impacto.

SER15 atualiza a coerência entre produtoras, auditores, policy, Manual e prompts sem hardcodar capacidades futuras. SER16 prova a árvore efetivamente integrada e o estado por skill, inclusive pendências. Não se encerra afirmando “oito promovidas” se uma parte continua BLOCKED_DESIGN.

## 10.8 Critérios de entrega por bloco

B0 entregue: mecanismo mínimo qualificado e cobertura classificada; nenhuma promoção.

B1 entregue por item: pacote L3/L2 completo, execução local e auditorias pertinentes, estado externo e gate humano explícitos. Não exigir o fim de todas as outras filas para reconhecer um item concluído.

B2 entregue por item: execução real das superfícies L4 suportadas, Postflight, efeitos/destinos verificados e autoridade respeitada. Dry-run não satisfaz esse critério.

B3 entregue: candidatas aceitas integradas e operacionalmente verificadas no alcance autorizado, snapshots e índices coerentes, evidência final disponível, SER15/SER16 com gaps explícitos e histórico imutável.

## 10.9 Métricas para demonstrar que a mudança funcionou

Medir por fase: tempo de autoria, diagnóstico, execução, espera de auditoria, espera humana, publicação e integração. Não somar tempos de comandos aninhados como se fossem esforço independente. Registrar wall-clock de campanha, CPU/processo quando observável, tokens/custo quando expostos e motivo de toda recertificação.

Indicadores de qualidade: taxa de first-pass por etapa; defeitos triviais encontrados apenas no laboratório; findings materiais da auditoria; falsos verdes detectados por mutantes; conflitos de integração; número de handoffs/intervenções humanas; cobertura de requisitos; tentativas com efeitos desconhecidos e preservação de evidência.

Meta operacional de segurança: zero promoção sem autorização, zero nova execução material após efeito desconhecido, zero omission de gate obrigatório não declarada. Metas de produtividade percentuais serão definidas após o piloto, não inventadas a partir de duas medições históricas.

## 10.10 Encerramento desta entrega de planejamento

O pacote contém decisões e especificações, e a candidata B0 implementa o mecanismo mínimo comum. A qualificação local do B0 e os testes das novas skills permanecem pendentes. O laboratório recebe apenas o entrypoint de qualificação do mecanismo; não recebe instrução para construir arquitetura, inventar testes ou corrigir a candidata durante a campanha.


## 10.11 Estado V3 e saída da autoria corretiva

Após a auditoria independente da candidata `f803b50f...`, o B0 foi promovido internamente para contratos V3. Antes de qualquer freeze, a saída de autoria exige três gates baratos e determinísticos no mesmo checkout limpo:

1. `python -B -m tools.skill_enforcement.parallel.preflight`;
2. `python -B -m unittest tools.tests.test_ser_parallel_b0 -v` — atualmente 82 métodos definidos;
3. `python -B -m tools.skill_enforcement.parallel.coverage`.

Nenhum PASS anterior atravessa SHA. O preflight parseia JSON/Python e confronta versões dos schemas/templates; coverage usa coleta unittest real e valida entrypoints `COMMAND_ONLY`; metatestes cobrem os mutantes levantados pela auditoria.

Host/Windows/NTFS/sandbox/headroom continuam gates ambientais. O lease atual restringe o host a uma campanha por vez; portanto, a prova de B0 não depende de coordenar múltiplos launchers. Dispatch por conclusão, cache de inventory e tuning do pool são P2: só entram depois que o piloto fornecer métricas de duração, fila, locks e recurso.

O gerador de handoff para campanhas reais fica no primeiro pacote B1, quando existir o primeiro manifesto de skill materializado; não se generaliza agora um formato sem consumidor real. O B0 já elimina handoff manual entre seus gates porque `b0_release` encadeia preflight, metatestes, coverage, host, pilotos e veredito em uma rodada única.
