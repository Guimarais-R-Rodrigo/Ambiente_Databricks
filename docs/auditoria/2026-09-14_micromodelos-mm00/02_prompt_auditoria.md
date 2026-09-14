# MM00 — prompt de auditoria independente A1

Você vai auditar a candidata da MM00 do Framework de Micromodelos. O objetivo não é resumir o plano nem opinar sobre estilo: é descobrir o que quebrará ou fará dois executores competentes divergirem quando a MM01 começar.

## Contexto

- Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`.
- Branch alvo: `micromodelos/mm00-baseline`.
- PR alvo: #43.
- Entrega declarada: baseline, arquitetura, inventário, matrizes, ADRs propostos e gates; nenhuma implementação funcional de micromodelos.
- Leia primeiro `01_contexto.md` desta pasta.

## Regras de independência

Não leia `CHANGELOG.md`, comentários/discussão da PR, outros arquivos desta pasta de auditoria nem histórico Git antes de formar seus achados. Não use justificativas do autor como prova. Verifique a árvore atual.

Não edite arquivo do repositório. Não publique, não altere ACL, não consulte dado real e não rode comandos com efeitos persistentes.

## Testes obrigatórios

### T1 — Reconstituir a arquitetura

A partir apenas dos documentos MM00 e dos contratos atuais do Hub, reconstrua:

- o que é micromodelo;
- o que não é;
- onde termina a responsabilidade do Hub;
- onde começa a governança externa;
- por que migração é posterior ao piloto novo.

Marque qualquer ponto em que duas leituras competentes produzam estruturas diferentes.

### T2 — Taxonomia do Hub

Verifique se a afirmação “seis tipos e lista fechada” é sustentada pelos arquivos atuais. Procure qualquer trecho da MM00 que, apesar disso, introduza implicitamente um sétimo tipo.

### T3 — Reuso

Para cada item classificado como REUSAR/ADAPTAR em `MATRIZ_REUSO.md`, confirme que o componente existe e que seu contrato realmente cobre a responsabilidade atribuída. Registre sobreposição ou lacuna material.

### T4 — Ausência de mudança funcional

Compare nominalmente a branch com a base. Confirme se nenhum arquivo funcional de `ambiente_fonte/.assistant/`, `tools/` ou workflow foi alterado. Se houver, classifique como QUEBRA de escopo.

### T5 — Sanitização

Procure nomes, paths, grupos, usuários ou outros identificadores externos que não deveriam estar versionados. Diferencie nomes públicos de tecnologias de identificadores do ambiente de trabalho.

### T6 — YAML/proveniência

Avalie se o desenho proposto permite distinguir sem ambiguidade: descoberto, inferido/proposto, aprovado e medido. Procure transições ou estados impossíveis de auditar no plano atual.

### T7 — Fingerprint

Teste conceitualmente o contrato: liste pelo menos cinco mudanças que deveriam preservar o fingerprint e cinco que deveriam alterá-lo. Aponte qualquer campo do plano cuja materialidade esteja ambígua antes da MM02.

### T8 — MLflow

Confirme o contrato atual de `hub_snippets.ml.mlflow_run`. Verifique se a MM00 promete algo que o helper atual não faz e se isso está corretamente adiado para gate futuro. Procure risco de quebrar o perfil atual ao adaptar micromodelos rule-based.

### T9 — Visual

Verifique o estado real do Sistema de Temas no branch/base e se a decisão de adiar integração definitiva é coerente. Confirme que a MM00 não hardcode tema/paleta específica.

### T10 — Migração

Tente encontrar qualquer dependência da fundação que exija a skill de migração antes do piloto greenfield. Se não houver, confirme que MM12 pode permanecer independente. Se houver, descreva a dependência concreta.

### T11 — Próxima sprint

Assuma que MM01 começará amanhã. Liste somente informações ainda ausentes que impediriam dois implementadores independentes de construir o mesmo contrato YAML. Diferencie lacuna que MM01 deve resolver de lacuna que já deveria estar resolvida na MM00.

### T12 — Regras do projeto

Confronte a candidata com `CLAUDE.md` e regras relevantes em `.claude/rules/`, especialmente fonte de verdade, documentação, multi-LLM e separação de ambientes.

## Formato da resposta

Comece por T1 e registre evidência concreta. Depois organize achados em:

1. **QUEBRA** — impede avanço seguro ou viola contrato/regras;
2. **DIVERGE** — dois executores competentes podem implementar coisas materialmente diferentes;
3. **MELHORÁVEL** — só inclua quando houver custo concreto de manter como está.

Para cada achado: arquivo/trecho, evidência, impacto, correção mínima e teste de aceite.

Termine com:

- maior risco residual;
- pergunta que precisa de decisão humana antes de MM01;
- elemento do desenho que deve ser preservado;
- o que não foi possível avaliar;
- veredito `APTA_PARA_ACEITE_MM00`, `APTA_COM_CORRECOES` ou `NAO_APTA`, sem converter score médio em aprovação.

Não elogie, não resuma o plano de volta e não aceite afirmação sem verificá-la contra a árvore.
