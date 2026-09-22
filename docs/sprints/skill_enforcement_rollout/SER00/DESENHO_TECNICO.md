# SER00 — decisões arquiteturais aceitas e limites de implementação

Status: A01–A03 aceitas humanamente em 2026-09-22; A01/A02 consolidadas no ADR-0022. Isso congela a direção arquitetural, não implementa certifier/schema/runner e não autoriza SER01. Base `11851e137dd7793b351ac08fc211c0be90005dee`.

## A01 — certificação histórica versus árvore mutável — ACEITA

Em tools/tests/test_skill_enforcement_se08.py, a suíte vigente exige simultaneamente: criar-objeto current=L2; README com cinco contratos; integração de ci_local apontando ao perfil se08. O certifier inclui essa suíte no perfil cumulativo se08. A promoção legítima de criar-objeto ou a criação de novos contratos conflita com essas assertions sobre a árvore atual.

Portanto não é correto prometer que um perfil novo, sozinho, resolverá o problema. Também não é permitido apagar a assertion, mudar L2 para L3 por conveniência, filtrar silenciosamente testes, marcar FAIL como PASS ou reescrever a semântica histórica de --profile se08.

**Decisão aceita:** separar certificação histórica SE08 de certificação operacional SER. O controle SER será aditivo, terá identidade própria, executará invariantes de mecanismo e regras atuais de catálogo, e documentará a migração do ponto de integração de CI local. A decisão está registrada no ADR-0022. A implementação e os testes adversariais pertencem à primeira sprint funcional autorizada; falhas observadas nos comandos históricos sobre árvore nova continuam registradas, não ocultadas.

**Alternativa:** adiar promoções e manter as verificações atuais intactas. Essa alternativa não fecha gaps; apenas mantém o estado vigente.

O aceite não cria exceção silenciosa ao gate nem converte a campanha histórica em evidência SHA-bound da candidata SER. SER01 continua NOT_STARTED e só poderá iniciar após integração da SER00 e autorização separada.

## A02 — condições de domínio e verdade por superfície — ACEITA

O schema execution_contract 0.1 fixa mode=audit e aceita sete condition kinds, orientados a amostra, preview, numerais, distribuições, tema, visualização e PK. validate_contracts.py replica esse vocabulário. Nenhum deles expressa diretamente PIT, maturidade do target, autorização de materialização ou deployment intent.

Decisão aceita: evoluir condições/contexto de forma aditiva, versionada e fail-closed, preservando contratos 0.1. Campos desconhecidos e aplicabilidade não determinada bloqueiam. Nunca reutilizar `pk_columns_available` ou `resolved_theme_selected` como sinônimo de autorização/PIT e nunca aceitar expressão arbitrária/eval. Preferir condição local da skill quando a semântica for específica; elevar ao schema compartilhado somente quando houver significado transversal estável. A fronteira entre preflight específico e engine compartilhada deve permanecer explícita e testada.

O campo protected_surfaces.level é desejado; ele não registra por si um current por superfície. Promoção parcial exige delimitação inequívoca e aceita do que está protegido. Não inferir cobertura total a partir do nível máximo de uma rota piloto.

## A03 — criar-objeto: target L3 confirmado; escopo de prova fica para SER01 — ACEITA

O target L3 é proporcional à validação objetiva do objeto, mas o piloto disponível restringe-se a create/readme/agregador no Windows/NTFS, com validação repo-side. O SKILL cobre create/convert e seis tipos de objeto. O scope já é stage_specific; não propor whole_skill sem justificativa.

Decisão aceita: manter target L3 e `scope_mode=stage_specific`. A SER01 deve congelar e provar a matriz operação×tipo×host×efeito antes de qualquer promoção: geração, validação e aplicação separadas; APIs públicas por tipo; destino; overwrite proibido ou explicitamente autorizado por novo contrato; conversão; falha parcial; rollback; Receipt; suporte Free. Nenhuma célula não provada pode entrar no claim L3. Enquanto apenas o piloto estiver provado, current global continua L2.

Regra para SER01: primeiro fechar a matriz e validar as rotas existentes; ampliar somente a superfície comprovada. Se o claim global L3 não puder ser sustentado sem abarcar operações ainda não provadas, manter `current_level=L2` e replanejar com aceite, em vez de promover nominalmente.

## A04 — auditoria de novas produtoras

O adapter documentado revalida o payload EDA. Para outras produtoras, manter NOT_REVERIFIED até haver verifier de domínio compatível e testes que recusem receipt adulterado, stale e conclusão indevida. Registrar adapter na sprint da produtora quando necessário para a prova, e reconciliar catálogo na SER15. Isso não reabre o rollout funcional da auditoria L3.

## A05 — host, dependências e efeitos externos

Compatibilidade Free/Genie é uma evidência a obter, não inferência de presença de pacote. Datas e restrições de plataforma descritas em SKILL/Manual são observações históricas do projeto, não uma verificação externa atual nesta sessão. Antes de promoção, testar o runtime pessoal autorizado. Se faltar API de tracking/deploy, não converter NOT_RUN em NOT_APPLICABLE para elevar L4.

Autorização é específica a destino/mode/objeto/efeito. L4 implementado não autoriza por si materializar, promover modelo, conceder grants, disparar jobs ou escrever em workspace compartilhado. Dados exclusivamente sintéticos/isolados; promoção corporativa bloqueada.

## A06 — ciclo de promoção e identidade da evidência

Não editar current para orientar testes. Implementar e testar artefatos mantendo o current vigente; apresentar proposta de superfície/nível/rollout para decisão humana. O commit de policy é a última mudança funcional autorizada e cria nova candidata: recertificar esse SHA exato, verificar Free/conteúdo e comportamento aplicável, e obter aceite final antes de integrar. Evidência do commit anterior não prova o commit de promoção. A promoção operacional não é efetivada por um rascunho de PR.

Toda evidência externa identifica parent/main/candidate/tree/dirty state, plataforma, comandos, códigos de saída, logs, hashes e limitações. Documentos não precisam conter seu próprio SHA autorreferente: um manifesto externo e comentário da PR vinculam a árvore final sem ciclo infinito de commits de checkpoint.

## A07 — validação documental e integração repo-side pendentes

O acesso GitHub funcionou, mas o clone pelo container falhou por resolução de rede. Não existe checkout integral autenticado nesta sessão. Validação documental própria não substitui validate_assistant/README snapshot/CI/renderer. Antes de merge, executar esses gates no clone local e atualizar somente snapshots documentais que o comando comprovar. O CHANGELOG raiz não foi reescrito parcialmente: ENTRADA_CHANGELOG.md preserva a entrada preparada para aplicação byte-preserving, ainda pendente.

Com A01–A03 aceitas, o bloqueio arquitetural da SER00 está resolvido. A07 ainda impede declarar a candidata pronta para integração. Nenhuma proteção será desabilitada para superar o bloqueio. Esta rodada preserva o máximo documental possível, sem falsa certificação.
