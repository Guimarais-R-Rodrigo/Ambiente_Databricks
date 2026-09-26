# MM00 — Resultado da auditoria independente A1

Registro do parecer produzido em sessão independente sobre a PR #43. O conteúdo abaixo preserva o relatório recebido para contraditório e fechamento da MM00.

## T1 — Reconstituição da arquitetura

Alvo auditado: PR #43, `head=f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`, contra `main`/`base=55f7006c47d90ae7f760992d252b658f53a59636`. A verificação final repetida ao término da auditoria confirmou que os dois SHAs permanecem esses; portanto não houve `BASE_AVANCOU` durante a análise.

**O que é micromodelo.** Pelos ADRs e pelo Plano Mestre, é um artefato de domínio que reúne definição analítica, fontes, evidências/contraevidências, classificação/score, validação e demais elementos necessários para tornar a característica rastreável. Sua especificação estruturada canônica será `micromodelo.yaml`. Ele utiliza objetos já existentes do Hub, mas não é um desses objetos.

**O que não é.** Não é um sétimo tipo do Hub; não é um Produto de Dados; não é um run MLflow; não é um sistema próprio de governança institucional; e não deve conter um sistema visual paralelo. O Produto de Dados é a materialização governada para consumo, enquanto o micromodelo permanece a definição analítica e sua evidência.

**Onde termina o Hub.** O Hub pode orientar descoberta, estruturar o YAML, executar/encaminhar EDA, cross-EDA, feature engineering e validação, registrar runs, produzir documentação e preparar um handoff estruturado. Não ganha autoridade institucional apenas porque o micromodelo foi validado tecnicamente.

**Onde começa a governança externa.** Geração/validação final/publicação do Produto de Dados permanecem sob o processo institucional do ambiente autorizado. Handles, nomes, versões, ACLs e paths desse processo não são incorporados ao Hub; o binding ocorre externamente.

**Por que a migração vem depois.** A arquitetura exige primeiro um caso greenfield ponta a ponta, seguido de hardening e freeze da V1. Isso evita que convenções e exceções dos legados contaminem o contrato antes de ele provar que YAML, tracking, handoff, documentação e uso por cientista funcionam em um caso novo. MM12 depende explicitamente do piloto novo e do freeze V1; não encontrei dependência da fundação que exija a skill de migração antecipadamente.

**Divergência arquitetural no T1:** não encontrei duas interpretações competentes que produzam arquiteturas materialmente distintas no nível que cabe à MM00. As indefinições de schema, máquina de estados e fingerprint são reais, mas foram explicitamente atribuídas a MM01 e MM02. Há, contudo, uma inconsistência de rastreabilidade do baseline entre documentos, registrada em MELHORÁVEL M-01.

## 1. QUEBRA

### Q-01 — Falta a entrada própria da MM00 no `CHANGELOG.md`

**Arquivo/trecho:** `CLAUDE.md`, regra “Toda sessão que altera algo termina com entrada no CHANGELOG.md”; `docs/decisions/README.md`, que manda atualizar `CHANGELOG.md` ao adicionar ADR; e `CHANGELOG.md` atual.

**Evidência:** a candidata adiciona ADR-0014 a ADR-0020 e extensa documentação MM00, mas a busca no `CHANGELOG.md` atual retorna zero ocorrência de `MM00`. O próprio checkpoint/testes também mantêm essa pendência aberta. O changelog continua iniciando pela entrada V08, sem registro próprio da nova iniciativa.

**Impacto:** é violação direta de regra canônica do projeto e de gate explicitamente assumido pela MM00. A arquitetura pode estar tecnicamente utilizável, mas a candidata não está em condição de aceite/merge enquanto o gate documental permanecer aberto. Iniciar MM01 assim normalizaria a quebra de uma regra fail-closed usada pelo próprio projeto.

**Correção mínima:** acrescentar uma entrada estritamente aditiva da MM00 ao `CHANGELOG.md`, sem reescrever histórico existente. Como isso acrescentará o changelog ao diff da PR, também será necessário reconciliar qualquer documento vivo que continue afirmando “22 arquivos” como estado atual.

**Teste de aceite:** o `CHANGELOG.md` contém uma entrada MM00 identificando escopo documental, ADRs propostos, limites e ausência de alteração funcional; nenhuma entrada histórica foi reescrita; as contagens/diff documentados correspondem à nova árvore; CI geral e validadores documentais retornam `success`.

## 2. DIVERGE

**Nenhum achado DIVERGE atribuível à MM00.**

Existem decisões que ainda fariam dois implementadores produzirem YAMLs diferentes se tentassem implementar MM01 hoje — tipos, required/optional, cardinalidades, representação da proveniência, máquina de estados, regras cross-field etc. —, mas justamente essas decisões constituem o escopo declarado de MM01. Transformá-las em defeito da MM00 anteciparia indevidamente o contrato da sprint seguinte.

O que a MM00 precisava congelar como invariantes semânticos está suficientemente delimitado: YAML canônico; micromodelo distinto de Produto de Dados e da taxonomia do Hub; proveniência separando descoberto/proposto-aprovado/medido; aprovação humana explícita; resultado `medido` somente com execução/evidência; MLflow separado da definição; governança externa autoritativa; e migração posterior ao greenfield.

## 3. MELHORÁVEL

### M-01 — A cronologia do baseline não está reconciliada uniformemente nos documentos MM00

**Arquivo/trecho:** `docs/sprints/micromodelos/MM00/README.md`, seção “Baseline e reconciliação”; `CHECKPOINT.md` e registros posteriores.

**Evidência:** o README MM00 encerra a narrativa de reconciliação no merge `e322e73fc0dc73c3081c99662ac29cb7721add67`. A cronologia efetivamente verificável prosseguiu: `1b663219...` corresponde ao fechamento V07; V08 foi integrada por `622d2c96...`; a `main` fechada chegou a `55f7006c...`; e a reconciliação final da MM00 com essa base ocorreu em `edfcf58e...`, cujo segundo parent é justamente `55f7006c...`. O checkpoint posterior já registra essa cronologia mais recente.

Além disso, o snapshot `efd866cc...` realmente existe e os quatro workflows exigidos — CI geral, V00, V01 e V02 — concluíram com `success`; no head atual `f5577f...` esses quatro workflows também estão verdes. Assim, qualquer texto que ainda trate essa bateria como pendente está desatualizado, não refletindo o estado efetivamente observado.

**Impacto:** não muda a arquitetura nem o comportamento da futura MM01, mas reduz a reprodutibilidade da auditoria. Um auditor que use `MM00/README.md` como registro de baseline pode reconstruir o delta a partir de um ponto intermediário e obter uma narrativa distinta daquela do checkpoint/current PR.

**Correção mínima:** reconciliar somente os documentos vivos da MM00 para que abertura, V08, fechamento V08, reconciliação final e head validado sejam narrados de modo consistente. Preferencialmente, manter um documento como proprietário dos detalhes mutáveis e os demais apontarem para ele, em vez de repetir SHAs/status em vários lugares.

**Teste de aceite:** README MM00, TESTES, CHECKPOINT e contexto de auditoria não contradizem entre si os marcos `1b663219…`, `622d2c96…`, `55f7006c…`, `edfcf58e…` e o head corrente; qualquer snapshot histórico permanece explicitamente rotulado como histórico.

## Cobertura dos testes obrigatórios T2–T12

**T2 — Taxonomia do Hub: PASS.** O template de skill e `hub-ml-criar-objeto` sustentam a lista fechada de seis tipos: snippet, script, prompt, README, notebook e skill. O próprio criador proíbe inventar sétimo tipo. A MM00 não viola isso: `micromodelo.yaml` é artefato de domínio produzido/consumido pelo fluxo, enquanto a futura `hub-ml-micromodelos` continua sendo uma **skill**, um dos seis tipos existentes.

**T3 — Reuso: PASS, com fronteiras confirmadas.** Todos os itens REUSAR/ADAPTAR da matriz existem. Concierge cobre descoberta/composição; cross-EDA cobre múltiplas fontes; feature engineering cobre janelas/leakage; EDA profissional cobre uma fonte; validação estatística cobre hipótese/evidência; comentar-notebook documenta sem migrar comportamento; auditoria-skills audita contrato, não mérito estatístico; criar-objeto preserva os tipos atuais.

Nos utilitários, `schema_to_yaml` é corretamente limitado a snapshot técnico e não a crawler/catálogo governado; `data_quality_check`, `quick_profile` e `null_summary` realmente leem dados e só devem entrar depois da autorização; RFV, join diagnostics e `pit_join` possuem os recortes especializados atribuídos pela matriz.

Não encontrei lacuna de responsabilidade mascarada por “REUSAR”. A adaptação do MLflow está corretamente classificada como futura, não como capacidade já existente.

**T4 — Ausência de mudança funcional: PASS.** O diff atual tem 22 arquivos e nenhum deles fica em `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`. A PR permanece com 22 changed files no head auditado. Não há QUEBRA de escopo funcional.

**T5 — Sanitização: PASS.** O diff usa `<CATALOGO_PRODUTO>` para o binding externo e explicita que nomes reais de catálogo/schema/grupo/path ficam fora do Git. A inspeção do patch não encontrou `/Workspace`, `username` ou `CAIXA`. Referências a Databricks, MLflow, Unity Catalog, PySpark, Genie Code e `ResolvedTheme` são nomes públicos de tecnologia ou componentes versionados, não identificadores secretos do ambiente.

**T6 — YAML/proveniência: PASS para MM00; contrato exato permanece MM01.** O plano distingue `descoberto`, `proposto/inferido`, `aprovado` e `medido`; aprovação exige decisão humana e a matriz de riscos exige referência de run/notebook para estado `medido`, bloqueando promoção por intenção da IA. O padrão existente de proveniência também proíbe inventar execução, timestamp, snapshot ou validação.

Não encontrei transição atualmente executável e impossível de auditar, porque a máquina ainda é apenas candidata. MM01 deverá tornar fail-closed, em particular, `proposto → aprovado`, `resultado → medido` e qualquer chegada a `PUBLICADO`, esta última dependente de confirmação da governança externa.

**T7 — Fingerprint: contrato conceitual PASS; materialidade fina permanece MM02.**

| Deve preservar `spec_fingerprint` | Deve alterar `spec_fingerprint` |
| --- | --- |
| reindentação/whitespace do YAML | mudança da fonte utilizada |
| reordenação puramente serial de chaves | mudança do grão/entidade operacional |
| correção de prosa explicativa sem efeito analítico | mudança de janela/corte temporal |
| mudança de README/notebook narrativo | mudança de regra/transformação |
| mudança apenas de tema/paleta/apresentação | mudança de peso ou threshold |
| reorganização editorial sem mudar valores semânticos | mudança de tratamento de missing |
| nota administrativa que não entra no cálculo | mudança da semântica TRUE/FALSE/indeterminado |
|  | mudança do significado do score |
|  | mudança do contrato de saída |

A MM00 já determina que não será hash bruto do YAML e cita fonte, janela, regra, peso, threshold, missing, semântica binária, score e contrato de saída como materiais.

Antes da MM02 continuam legitimamente ambíguos: quais partes de `identidade` entram no hash; qual subconjunto de `negocio` é operacional versus descritivo; se referências de `evidencias/contra_evidencias` pertencem à identidade da especificação; e se `experimentos`, `validacao`, `tracking`, `governanca`, `publicacao` e `proveniencia` são metadados de ciclo de vida ou componentes materiais. Isso é precisamente o problema atribuído à MM02 e deve ser resolvido por canonicalização + testes metamórficos, não antecipado na MM00.

**T8 — MLflow: PASS com adaptação futura obrigatória.** `run_governado` atualmente exige dataset, split e limitações; no modo completo exige parâmetros, métricas e assinatura. O método `modelo()` chama `mlflow.sklearn.log_model`, portanto o perfil atual é inadequado para exigir artificialmente um objeto sklearn de um micromodelo rule-based.

A MM00 não afirma que isso já está resolvido: classifica “tracking tradicional” como REUSAR e “tracking rule-based” como ADAPTAR EM MM06, com extensão aditiva e regressões para preservar o perfil tradicional. Não encontrei promessa que exceda a API atual nem autorização para quebrar o comportamento vigente.

**T9 — Visual: PASS.** O estado real é V00–V08 aceitas e integradas no Git, sem publicação Databricks; `ResolvedTheme` permanece fonte de resolução e V08 remove política visual paralela. A MM00 não modifica essas superfícies e o ADR-0019 manda consumir o Sistema de Temas vigente, não hardcodear cor, CSS ou paleta. Adiar a composição específica para MM11 é coerente porque o framework ainda não possui artefato visual de micromodelo a integrar.

**T10 — Migração: PASS.** Não encontrei qualquer requisito da fundação MM01–MM11 que dependa da existência de `hub-ml-padronizar-micromodelo` ou da skill de migração. A dependência é inversa: MM12 depende do piloto, hardening e freeze. Portanto MM12 pode permanecer isolada sem bloquear a esteira greenfield.

**T11 — Informações ainda ausentes para dois implementadores produzirem o mesmo YAML.** São lacunas que **MM01 deve resolver**: tipos e cardinalidades de cada grupo; required/optional/default/null semantics; mecanismo de `schema_version`; identificadores e referências internas; grafo exato de transições; quem/qual evidência autoriza cada transição; como proveniência se liga a campo/claim/evidência; formato da prova de aprovação humana; formato da referência que torna algo `medido`; como confirmação externa sustenta `PUBLICADO`; enums/regras cross-field de classificação, score, fontes e saída; e fixtures positivas/negativas.

Não identifiquei lacuna dessa lista que já precisasse ter o encoding definido na MM00. O que **já deveria estar resolvido na MM00** — e está — são as fronteiras semânticas: YAML é canônico; run não é definição; aprovação não é inferência; medição não é proposta; governança externa não é função do Hub; micromodelo não é sétimo tipo; Produto de Dados não é o micromodelo. A aceitação humana dessas decisões ainda é gate, não uma lacuna de documentação.

**T12 — Regras do projeto: uma QUEBRA e uma inconsistência documental.** Fonte de verdade foi preservada: não houve edição funcional fora de `ambiente_fonte`, nem criação concorrente no simulado. Separação Free × trabalho foi respeitada: nenhum dado corporativo, ACL real ou runtime institucional foi acessado. As regras multi-LLM também foram respeitadas nesta auditoria: nenhuma correção foi aplicada, e A1 foi executada independentemente.

As exceções são exatamente Q-01, pela falta do changelog, e M-01, pela cronologia viva não estar uniforme entre os documentos.

**Maior risco residual:** MM01 modelar proveniência/estado de ciclo de vida e definição analítica de forma excessivamente acoplada. Se isso ocorrer, MM02 pode acabar incluindo aprovação, tracking ou histórico operacional no fingerprint — gerando churn de identidade — ou, no extremo oposto, deixar campos analiticamente materiais fora do hash. O gate mais importante após MM01 será provar que “definição” e “evidência de ciclo de vida” são separáveis e referenciáveis.

**Pergunta que precisa de decisão humana antes de MM01:** os ADR-0014 a ADR-0020 são aceitos como restrições arquiteturais da próxima sprint — em particular micromodelo como artefato de domínio, `micromodelo.yaml` como fonte canônica, MLflow separado da definição, governança institucional externa, piloto greenfield antes de legado, consumo do Sistema de Temas e binding externo da fonte de Produtos de Dados? Eles permanecem formalmente **propostos**, não aceitos.

**Elemento do desenho que deve ser preservado:** a separação de responsabilidades entre **especificação canônica do micromodelo → evidência/runs → handoff → governança/publicação externa**. Essa fronteira evita simultaneamente um sétimo tipo do Hub, um tracking paralelo e a duplicação da governança institucional.

**O que não foi possível avaliar:** não foram avaliados workspace Databricks real, catálogo corporativo, permissões/ACL, skills institucionais externas, publicação de Produto de Dados, runtime MLflow/Spark do ambiente de trabalho ou comportamento de componentes MM01+ inexistentes. Comentários/discussão da PR não foram usados. A auditoria foi somente leitura e, por determinação do protocolo, este parecer não foi gravado no repositório nem convertido em `99_consenso.md`. A compatibilidade operacional futura continua dependendo das sprints/homologações correspondentes.

**Veredito:** **`APTA_COM_CORRECOES`**

A correção bloqueadora é Q-01. M-01 deve ser reconciliado no mesmo fechamento para que a candidata aceita registre uma única cronologia verificável. Não encontrei quebra funcional, criação de sétimo tipo, vazamento de identificador corporativo, dependência antecipada de migração, conflito com o Sistema de Temas ou divergência arquitetural material que justifique `NAO_APTA`.
