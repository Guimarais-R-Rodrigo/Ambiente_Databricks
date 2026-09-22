# SER00 — decisões arquiteturais pendentes

Status: proposta para decisão humana, não ADR aceito nem implementação. Base `11851e137dd7793b351ac08fc211c0be90005dee`.

## A01 — certificação histórica versus árvore mutável (bloqueador)

Em tools/tests/test_skill_enforcement_se08.py, a suíte vigente exige simultaneamente: criar-objeto current=L2; README com cinco contratos; integração de ci_local apontando ao perfil se08. O certifier inclui essa suíte no perfil cumulativo se08. A promoção legítima de criar-objeto ou a criação de novos contratos conflita com essas assertions sobre a árvore atual.

Portanto não é correto prometer que um perfil novo, sozinho, resolverá o problema. Também não é permitido apagar a assertion, mudar L2 para L3 por conveniência, filtrar silenciosamente testes, marcar FAIL como PASS ou reescrever a semântica histórica de --profile se08.

**Recomendação:** aprovar uma separação explícita entre certificação histórica SE08, executada contra árvore histórica pinada, e certificação operacional SER na candidata atual. O controle SER deve ser aditivo, possuir identidade própria, executar invariantes de mecanismo preservadas e regras atuais de catálogo, e documentar a migração do ponto de integração de CI local. A composição exata e o tratamento de cada assertion temporal precisam de ADR prospectivo, teste adversarial e aceite antes de SER01. Falhas observadas nos comandos antigos sobre a árvore nova continuam registradas, não ocultadas.

**Alternativa:** adiar promoções e manter as verificações atuais intactas. Essa alternativa não fecha gaps; apenas mantém o estado vigente.

A SER00 não escolhe por conta própria uma exceção ao gate solicitado pelo usuário. Até decisão explícita, SER01 está bloqueada. A campanha histórica nunca será apresentada como evidência SHA-bound da candidata SER.

## A02 — condições de domínio e verdade por superfície

O schema execution_contract 0.1 fixa mode=audit e aceita sete condition kinds, orientados a amostra, preview, numerais, distribuições, tema, visualização e PK. validate_contracts.py replica esse vocabulário. Nenhum deles expressa diretamente PIT, maturidade do target, autorização de materialização ou deployment intent.

Recomendação: desenho aditivo de condições/contexto de domínio, com versões e handlers públicos explícitos, preservando contratos 0.1. Campos desconhecidos e aplicabilidade não determinada bloqueiam. Nunca reutilizar pk_columns_available ou resolved_theme_selected como sinônimo de autorização/PIT; nunca aceitar expressão arbitrária/eval no contrato. A fronteira entre preflight específico e schema compartilhado precisa ser documentada e testada, sem transformar a engine em framework analítico universal.

O campo protected_surfaces.level é desejado; ele não registra por si um current por superfície. Promoção parcial exige delimitação inequívoca e aceita do que está protegido. Não inferir cobertura total a partir do nível máximo de uma rota piloto.

## A03 — criar-objeto: target numérico mantido, escopo não congelado

O target L3 é proporcional à validação objetiva do objeto, mas o piloto disponível restringe-se a create/readme/agregador no Windows/NTFS, com validação repo-side. O SKILL cobre create/convert e seis tipos de objeto. O scope já é stage_specific; não propor whole_skill sem justificativa.

Antes de qualquer promoção, aprovar uma matriz operação×tipo×host×efeito: geração, validação e aplicação separadas; APIs públicas por tipo; destino; overwrite proibido ou explicitamente autorizado por novo contrato; conversão; falha parcial; rollback; receipt; suporte Free. Nenhuma célula não provada pode entrar no claim L3. Enquanto apenas o piloto estiver provado, current global continua L2.

Recomendação para SER01: primeiro fechar essa matriz e validar as rotas existentes; ampliar somente a superfície aprovada. Se a implementação completa exigir dividir a sprint, registrar replanejamento e pedir aceite, sem criar promoção nominal para encerrar SER01.

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

Mesmo com decisões A01–A03 aceitas, A07 impede declarar a candidata totalmente pronta para integração. Nenhuma proteção será desabilitada para superar o bloqueio. Esta rodada preserva o máximo documental possível, sem falsa certificação.
