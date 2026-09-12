# Fontes e dependências da composição V01

## Proveniência e alcance

Base confirmada pelo conector GitHub em 12/09/2026:
`b88a9ccdde6e61892bc25eb7cf4f4b2577badb23`, árvore
`e339983237bd21b2127248f38705c685b03da0f0`. A main já integra os PRs #7 e #8.
ADR-0011 é o Concierge; ADR-0012 é a proposta de READMEs. Seus textos e estados
não foram sobrescritos. A nova proposta usa ADR-0013, disponível nessa base.

O ZIP local V01 entregue anteriormente, commit `aa70abcf`, foi lido como insumo,
não aplicado por cima da main. Schema, fixtures e testes foram reaproveitados;
rotas, dependências, leitura operacional e evidências foram reconciliadas.
Não trouxemos a V00 local alternativa nem criamos `docs/sprints/temas/` concorrente.
O mapa de procedência fica em [PROVENIENCIA.json](PROVENIENCIA.json).

A obtenção da base pelo workflow temporário ocorreu sem credenciais persistidas.
O primeiro checkout raso foi corretamente recusado pelo gate de READMEs. O segundo
usou histórico completo (run `34706140181`, artefato `10301865696`), cujo ZIP tem
SHA-256 `89b8100dae8045e273b19ace79754a8b853446f3326deefc3ee8bd4f4d110720`.
O transporte não certifica testes; estes foram executados e registrados à parte.
Não distribuir o arquivo de checkout/histórico como pacote de implantação.

## Leitura do projeto por decisão

| Fonte na base de composição | Decisão informada |
|---|---|
| `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, regras e templates | Autoria, fonte única, proteção de dados, hierarquia documental e ADR. |
| `docs/decisions/`, especialmente ADR-0007/0009/0010/0011/0012 | Pastas de objetos, pacote, Manual e coexistência com READMEs/Concierge. |
| `docs/sprints/sistema_temas/` e `docs/testes/sistema_temas/V00/` | Instrumentação integrada, pendências e significado limitado do aceite Git. |
| `tools/inventario_visual.py`, `executar_baseline_visual.py` e três suítes V00 | Inventário e capturas existentes; evitar uma implementação rival. |
| `colors.py`, `styles.py`, `theme_plotly.py`, componentes HTML, tabelas e curvas | Defaults, contratos e limites de compatibilidade. |
| Tokens editoriais, compositor v2 e registros de aprovação | Desvios entre declaração e uso; assets estáticos e integridade. |
| `tools/ci_local.py`, workflow V00, ferramentas e kit de transição | Oito gates preservados, CI adicional e nenhuma publicação nesta sprint. |
| Plano V00–V14 e catálogo de testes anexados à conversa | Escopo V01 e rastreabilidade CON-01–12, DOC-02/03, A11-01, SEC-01 e UAT-01. |

A referência de tokens aponta os caminhos reais dos consumidores, sem declarar
que já consomem o tema. A revisão semântica completa da V00 continua pendente.

## Referências públicas primárias verificadas

Consultadas em 12/09/2026, com uso restrito à fundamentação técnica:

- JSON Schema Draft 2020-12 e objetos fechados:
  https://json-schema.org/draft/2020-12 e
  https://json-schema.org/understanding-json-schema/reference/object .
  Fundamentam o dialeto, `required` e `additionalProperties`, não uma instalação no Hub.
- jsonschema 4.26, validação e FAQ:
  https://python-jsonschema.readthedocs.io/en/stable/validate/ e
  https://python-jsonschema.readthedocs.io/en/stable/faq/ .
  Defaults não são inseridos automaticamente; contrato e parser têm responsabilidades diferentes.
- W3C, contraste mínimo:
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html .
  Razões pertinentes de 4,5:1 e 3:1 sem arredondar aprovação; verificar exceções/contexto.
- Azure Databricks, widgets:
  https://learn.microsoft.com/en-us/azure/databricks/notebooks/widgets .
  Reexecução por controles exige projetar laboratório seguro; não foi testada em workspace aqui.
- Plotly, templates:
  https://plotly.com/python/templates/ .
  Templates fornecem defaults e propriedades explícitas podem prevalecer; efeito global deve ser isolado.

Essas fontes não certificam a implementação do Hub, a acessibilidade de seus
ativos, a segurança de um App nem compatibilidade no trabalho. Evidência local
é fornecida pelos logs e pelo relatório desta execução.


## Questões ainda abertas

O contrato é candidato 0.1.0. Interface, persistência operacional, designação
real de responsáveis, autorização no destino e orçamento de desempenho continuam
pendentes. O protocolo-alvo 1.0.0 não é engine instalado. Apps e AI/BI não fazem
parte dos contextos suportados por este contrato inicial. A V02 precisará
promover a fonte do contrato de forma única e seguir o template de objeto vigente.

[Voltar à V01](README.md)
