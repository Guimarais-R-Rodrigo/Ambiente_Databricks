# MM00 — Matriz de riscos

| ID | Risco | Prob. | Impacto | Detecção/Gatilho | Mitigação | Gate |
|---|---|---:|---:|---|---|---|
| R01 | Transformar micromodelo em sétimo tipo do Hub | M | A | criação de novo `hub_padroes/micromodelo` ou alteração da lista fechada | manter templates de domínio dentro da skill e projetos reais fora da taxonomia | parar e decidir |
| R02 | Confundir micromodelo com Produto de Dados | M | A | notebook de estudo começa a incorporar publicação/governança como se fossem a mesma camada | separar estudo, validação, handoff e materialização | impedir avanço |
| R03 | Versionar nomes/paths reais do trabalho | M | C | catálogo/schema/grupo/path real aparece no diff | placeholders no Git; binding somente no ambiente autorizado | bloquear commit |
| R04 | Metadata parcial ser interpretado como catálogo completo | A | A | ausência de objetos vira conclusão de inexistência | registrar `ESCOPO_OBSERVADO`, permissões e limites | bloquear claim |
| R05 | Prompt injection em comentários/tags | M | A | metadata contém instruções para agente | tratar metadata como dado não confiável; nunca executar instruções recuperadas | bloquear ação |
| R06 | Skill duplicar EDA/cross-EDA/feature engineering | A | M | SKILL.md cresce com metodologia já existente | handoffs explícitos e progressive disclosure | auditoria de sobreposição |
| R07 | YAML virar formulário burocrático manual | M | M | cientista precisa editar dezenas de campos | skill preenche progressivamente; humano decide apenas pontos materiais | UX do piloto |
| R08 | IA marcar hipótese como fato/aprovação | M | C | `proposto` vira `aprovado` sem decisão humana | proveniência e máquina de estados fail-closed | bloquear transição |
| R09 | IA inventar resultado experimental | M | C | campo `medido` sem execução/evidência | exigir referência de run/notebook para estado medido | bloquear validação |
| R10 | FALSE absorver “evidência insuficiente” | A | A | classificação binária sem política de ausência | contrato explícito TRUE/FALSE/indeterminado quando aplicável | decisão humana |
| R11 | Score 0–100 ser interpretado como probabilidade | A | A | documentação usa “% probabilidade” sem calibração | campo obrigatório `score.significado`; validação semântica | bloquear publicação |
| R12 | `spec_fingerprint` mudar por edição de prosa | M | M | hash muda em reorder/whitespace/README | canonicalização material em MM02 e testes metamórficos | reprovar MM02 |
| R13 | `spec_fingerprint` não mudar após mudança material | B | C | threshold/peso muda e hash permanece | lista de campos materiais e mutantes negativos | reprovar MM02 |
| R14 | MLflow armazenar scores individuais | M | C | artifact contém identificadores de clientes | somente agregados/distribuições no tracking; dados individuais em camada governada | bloquear run |
| R15 | Criar sistema de tracking concorrente | M | M | novo wrapper ignora `mlflow_run` | reutilizar/adaptar helper existente | gate em MM06 |
| R16 | Alteração de `mlflow_run` quebrar modelos tradicionais | M | A | regressão no perfil atual | extensão aditiva + regressões completas antes de merge | aceite explícito |
| R17 | Migração de legados contaminar desenho greenfield | A | A | requisitos antigos forçam arquitetura antes do piloto | manter migração em MM12 após V1 | bloquear MM12 |
| R18 | Migração alterar comportamento silenciosamente | M | C | output antes/depois diverge | migração conservadora + equivalência; modernização separada | parar e decidir |
| R19 | Duplicar regras da governança externa | M | A | Hub copia catálogo institucional de regras | handoff fracamente acoplado; validador externo continua autoritativo | remover duplicação |
| R20 | Visual virar segunda fonte de verdade | M | M | cores/CSS hardcoded em skill/template | consumir Sistema de Temas vigente; integração tardia | bloquear MM11 |
| R21 | Estado visual documentado ficar obsoleto durante projeto | A | M | `main` avança V08+ | reconsultar `main` antes de MM11; não congelar API futura na MM00 | reconciliar |
| R22 | Free ser tratado como homologação do trabalho | A | A | teste sintético vira claim de produção | matriz Free × trabalho; MM08 obrigatório | bloquear piloto |
| R23 | Permissões adicionais serem solicitadas/alteradas automaticamente | B | C | metadata não visível e fluxo tenta ampliar acesso | reportar lacuna e parar; ACL é decisão humana/institucional | parar |
| R24 | Catálogo de micromodelos virar cadastro paralelo manual | M | M | status/fontes duplicados em planilha/README | catálogo futuro derivado dos YAMLs | impedir fonte paralela |
| R25 | Escalar antes de provar | M | C | MM12 começa sem piloto/Freeze V1 | pré-condições formais de MM12 | bloquear sprint |

## Severidade

- **C**: crítico — pode expor dado, quebrar governança ou produzir decisão materialmente errada.
- **A**: alto — pode invalidar resultado, compatibilidade ou arquitetura.
- **M**: médio — produz retrabalho ou ambiguidade relevante.
- **B**: baixo — melhoria controlável sem efeito material imediato.

## Regra

Risco classificado como crítico não é neutralizado por score médio de auditoria, CI verde ou documentação extensa. O gate associado precisa ser resolvido explicitamente.
