# {{NOME_DO_PROJETO}} — ficha detalhada

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Esta ficha é documentação de apoio.
> Anexe-a com **Add context**/`@` quando necessário. Para instruções automáticas do
> projeto, crie `AGENTS.md` na raiz real usando `AGENTS_TEMPLATE.md`.

## Como preencher

Substitua todos os `{{PLACEHOLDERS}}`. Use `NÃO INFORMADO` quando apropriado e
registre o responsável por resolver a lacuna. Não armazene PII, segredos ou tokens.

## Metadados

- **Status:** {{RASCUNHO_ATIVO_PAUSADO_CONCLUIDO}}
- **Owner técnico:** {{OWNER_TECNICO}}
- **Owner de negócio:** {{OWNER_NEGOCIO}}
- **Início / revisão:** {{YYYY_MM_DD}} / {{YYYY_MM_DD}}
- **Repositório/Git folder:** {{CAMINHO_OU_NAO_INFORMADO}}
- **Ambientes:** {{DEV_STAGE_PROD}}

## Problema e decisão

- **Problema:** {{PROBLEMA}}
- **Decisão suportada:** {{DECISAO}}
- **População/unidade:** {{POPULACAO_E_GRANULARIDADE}}
- **Fora de escopo:** {{FORA_DE_ESCOPO}}

## Sucesso e guardrails

| Métrica | Definição | Baseline | Alvo | Janela | Owner |
|---|---|---:|---:|---|---|
| {{METRICA}} | {{DEFINICAO}} | {{BASELINE}} | {{ALVO}} | {{JANELA}} | {{OWNER}} |

## Recursos e contratos

| Recurso | Papel | Chaves | Período | Owner | Sensibilidade |
|---|---|---|---|---|---|
| `{{catalog.schema.table}}` | {{PAPEL}} | {{CHAVES}} | {{PERIODO}} | {{OWNER}} | {{CLASSE}} |

## Tempo e prevenção de leakage

- **Ponto de observação/predição:** {{CUTOFF}}
- **Horizonte:** {{HORIZONTE}}
- **Disponibilidade temporal crítica:** {{REGRAS}}
- **Colunas proibidas/proxies sensíveis:** {{COLUNAS}}

## Decisões

| Data | Decisão | Evidência/justificativa | Impacto | Autor |
|---|---|---|---|---|
| {{YYYY_MM_DD}} | {{DECISAO}} | {{EVIDENCIA}} | {{IMPACTO}} | {{AUTOR}} |

## Alternativas descartadas

| Alternativa | Motivo | Condição para revisitar |
|---|---|---|
| {{ALTERNATIVA}} | {{MOTIVO}} | {{CONDICAO}} |

## Riscos e bloqueios

| Prioridade | Risco/bloqueio | Mitigação | Owner | Prazo |
|---|---|---|---|---|
| {{P0_P1_P2}} | {{RISCO}} | {{MITIGACAO}} | {{OWNER}} | {{DATA}} |

## Validação e Definition of Done

- [ ] {{CRITERIO_TESTAVEL_1}}
- [ ] {{CRITERIO_TESTAVEL_2}}
- [ ] Evidências e limitações registradas.
- [ ] Segurança, custo, lineage e rollback revisados quando aplicáveis.

## Estado atual e próximos passos

**Estado:** {{RESUMO_FACTUAL}}

1. {{ACAO}} — owner: {{OWNER}} — prazo: {{DATA}}
2. {{ACAO}} — owner: {{OWNER}} — prazo: {{DATA}}

## Histórico de atualizações

| Data | Alteração factual | Evidência/link |
|---|---|---|
| {{YYYY_MM_DD}} | {{ALTERACAO}} | {{REFERENCIA}} |
