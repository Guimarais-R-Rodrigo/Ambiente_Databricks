# MM00 — Matriz de reuso

## Critério

Cada necessidade é classificada como:

- **REUSAR** — contrato existente atende sem mudança funcional;
- **ADAPTAR** — objeto existente é base correta, mas uma extensão aditiva pode ser necessária;
- **CRIAR INTERNO** — novo recurso específico da skill, sem virar helper global;
- **CRIAR OBJETO HUB** — novo objeto público, somente quando a lacuna for comprovada;
- **ADIAR** — não necessário para provar o MVP.

| Necessidade | Componente atual | Decisão MM00 | Motivo / limite |
|---|---|---|---|
| Descobrir recursos do Hub | `hub-ml-concierge` | REUSAR | evita catálogo concorrente e encaminha para especialista |
| Avaliar múltiplas fontes | `hub-ml-cross-eda-ml` | REUSAR | já cobre entidade, tempo, coverage, multiplicidade e readiness |
| Construir features | `hub-ml-feature-engineering` | REUSAR | já cobre janelas, leakage e especificação de features |
| Explorar uma fonte | `hub-ml-eda-profissional` | REUSAR | não duplicar EDA dentro da skill de micromodelos |
| Validar hipótese/evidência | `hub-ml-validacao-estatistica` | REUSAR | separa método estatístico do workflow de domínio |
| Documentar notebook legado | `hub-ml-comentar-notebook` | REUSAR | preserva código e acrescenta narrativa; não faz migração funcional |
| Auditar skill/output | `hub-ml-auditoria-skills` | REUSAR | já possui modo implementação e modo output |
| Criar objetos do Hub | `hub-ml-criar-objeto` | REUSAR | novos prompts/skills devem seguir os templates atuais |
| Snapshot técnico de tabela candidata | `hub_scripts.schema_to_yaml` | REUSAR | útil após seleção; não é crawler de catálogo |
| Diagnóstico de qualidade | `hub_scripts.data_quality_check` | REUSAR | quando leitura de dados já estiver autorizada |
| Perfil técnico | `hub_scripts.quick_profile` | REUSAR | usar apenas fora do modo metadata-only |
| RFV | `hub_scripts.rfv_calculator` | REUSAR | somente quando a hipótese realmente for RFV/recência |
| Diagnóstico de joins | `hub_snippets.spark.join_diagnostics` | REUSAR | evita reimplementação de coverage/multiplicidade |
| Join temporal | `hub_snippets.spark.pit_join` | REUSAR | protege contra leitura futura quando aplicável |
| Nulos/cobertura | `hub_snippets.spark.null_summary` | REUSAR | diagnóstico após autorização de leitura |
| Tracking de experimentos tradicionais | `hub_snippets.ml.mlflow_run` | REUSAR | contrato atual permanece válido |
| Tracking de micromodelo rule-based | `hub_snippets.ml.mlflow_run` | ADAPTAR EM MM06 | avaliar perfil aditivo sem exigir modelo sklearn artificial |
| Coleta metadata do catálogo configurado | inexistente específico | CRIAR INTERNO EM MM03 | workflow específico da skill; promoção global só após evidência de reuso |
| Validação do `micromodelo.yaml` | inexistente | CRIAR INTERNO EM MM01 | contrato de domínio da skill |
| Fingerprint semântico | inexistente | CRIAR INTERNO EM MM02 | identidade material do micromodelo; não é utilitário geral ainda |
| Handoff para governança externa | inexistente | CRIAR INTERNO EM MM10 | interface específica do fluxo corporativo |
| Skill de criação/descoberta | inexistente | CRIAR OBJETO HUB EM MM04 | lacuna de metodologia de domínio comprovada |
| Prompts de micromodelos | inexistentes | CRIAR OBJETO HUB MM04/MM05 | briefings recorrentes e rotas claras |
| Skill de migração | inexistente | ADIAR ATÉ MM12 | não desenhar migração antes de provar V1 |
| Dashboard/App de portfólio | não necessário | ADIAR | catálogo/index simples primeiro; App só com necessidade demonstrada |
| RAG/vector DB próprio | não necessário | ADIAR | metadata e specs versionadas são suficientes para MVP |
| Multiagentes | não necessário | ADIAR | aumenta coordenação antes de provar fluxo simples |
| Tema visual próprio | Sistema de Temas já existe | NÃO CRIAR | micromodelos serão consumidores do contrato visual central |

## Regra de promoção

Um script interno só poderá ser promovido a `hub_scripts` quando houver, no mínimo:

1. uso real fora da skill de micromodelos ou evidência clara de reutilização transversal;
2. API estável e independente do domínio;
3. README, notebook e testes segundo `hub_padroes/script`;
4. aceite explícito porque a promoção amplia a superfície pública do Hub.

O mesmo princípio vale para snippets: não criar por antecipação para abstrair código usado uma única vez.
