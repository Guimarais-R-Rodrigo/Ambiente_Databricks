# Documentação e READMEs

Leia ao escrever ou revisar documentação. Uma pessoa deve encontrar a próxima
ação rapidamente; um agente deve encontrar o owner sem navegar por duplicações.

## Hierarquia

| Escala | Entrada | Responsabilidade |
|---|---|---|
| Repositório | `README.md` da raiz | finalidade, arquitetura, gates e contribuição |
| Governança | `docs/README.md` | decisões, auditorias, testes, playbooks e histórico |
| Produto | `ambiente_databricks/.assistant/README.md` | instalação e uso no Databricks |
| Coleção | README da coleção | catálogo local, contrato, exemplo mínimo e limites |
| Objeto | README junto ao recurso | conceito aplicado, adequação, requisitos, interpretação e exemplo |

Um nível aponta ao próximo. Fatos mutáveis e regras longas têm um owner; os
demais textos usam link e síntese curta. Não copie cronologia nem inventário
para o núcleo. Regras comuns ficam em docs/ai; peculiaridades de carregador em
adaptação declarada, sem criar política concorrente.

## Readmes

Entradas agregadoras respondem, nesta ordem quando aplicável:

1. O que é e para quem é.
2. Próxima ação por objetivo.
3. O que acontece automaticamente e o que exige ação manual.
4. Exemplo copiável ou rota explícita para ele.
5. Limites, estado verificável e onde continuar.

Use exemplos concretos. Mermaid só quando relações/sequência ficarem mais claras
que em prosa; tabelas para comparação/catálogo, não parágrafos em células. Tome o
README raiz como referência de qualidade. Preserve relato histórico datado:
melhore entrada/sumário/navegação sem reescrever evidência antiga.

## Linguagem

- PT-BR na prosa. Preserve nomes de função, classe, parâmetro e coluna, inclusive
  existentes em português; não traduza APIs por uniformidade.
- Distinga interface nativa Databricks de conteúdo customizado Hub. `hub_`/`hub-`
  marca autoria local; `hub-ml-*` pode usar o mecanismo nativo Agent Skills.
- Regras são claras e imperativas; contexto separa fatos duráveis de observações.
  Nunca promova uma execução datada a lei da plataforma: declare ambiente e fonte.
- Capacidade não verificada recebe PENDENTE, BLOQUEADO ou PLANEJADO, com a prova
  faltante; testes usam PASS/FAIL/NOT_RUN/BLOCKED/NOT_APPLICABLE_WITH_REASON.
- Não duplique contagens/versões mutáveis. Se um número aparecer no README raiz,
  confira-o com gate. Inventário atual vem de policy/código, não de campanhas.
- Números narrativos seguem padrão brasileiro: `3.375.674`, `92,8%`.

## Manutencao

- Cada diretório de primeiro nível tem entrada sobre papel, uso e limites;
  prefira README. Outro índice canônico exige escolha explícita, sem concorrente.
- Links relativos devem resolver no Git e, em produto, na publicação Databricks.
- O corpo decisório de ADR aceito é imutável. Errata factual, ratificação/status
  podem ser anexados com data, preservando texto. Mudar decisão exige novo ADR.
- Preserve registro datado e autoria efetiva no owner da tarefa. A raiz recebe
  apenas marcos relevantes; comandos, contagens e tentativas ficam na evidência.
  Não reescreva entradas antigas nem snapshots fechados.
  [Critério e template](../templates/changelog-entry.md).

## Manual tecnico

O [Manual canônico](../../../ambiente_databricks/.assistant/MANUAL_TECNICO_V2.md) é a
única redação técnica vigente e o dono do catálogo integrado de helpers e do
glossário (ADR-0028, sucessor do ADR-0010). Edite o livro no produto, sincronize
as partes de leitura e confira o manifesto; gere a cópia do simulado pelo renderer.
Não existe cópia integral na raiz Git. O manual do usuário é complementar,
com foco na jornada de uso, e não substitui o contrato técnico.

Essa regra não autoriza editar o produto numa tarefa de manutenção da camada IA.
Use [fontes e derivados](fontes-e-derivados.md) para pré-condições e efeitos.

## Readme de objeto

Contrato vigente: `readme-objeto: 1.0.0`, conforme [template](../../../ambiente_databricks/.assistant/hub_padroes/readme/template_objeto.md),
[checklist](../../../ambiente_databricks/.assistant/hub_padroes/readme/checklist_objeto.md)
e ADR-0012. São quinze seções para README de objeto; índices, skills e outros
agregadores não herdam mecanicamente esse formato.

Todo novo snippet, script ou prompt inclui README na mesma mudança. Não crie
dispensa automática nem reabra `pending`: reintrodução é regressão e deve falhar.
O [CONTROLE_MIGRACAO](../../sprints/readmes_objetos/CONTROLE_MIGRACAO.json) preserva
fechamento/ratchet, não backlog ativo. 75/75 operacionais e 3/3 exemplares são
números históricos R00–R13, não cobertura corrente. Conte pela execução atual de
`tools/validate_assistant.py`/`tools/readme_objeto_contract.py`.

O gate comprova estrutura, links, cobertura e invariantes; não certifica didática,
estatística, execução Databricks, publicação, aceite humano ou auditoria
independente. Freezes e relatórios R00–R13 não são reescritos; estado vivo pertence
aos [índices da frente](../../sprints/readmes_objetos/README.md), regras, Manual e
READMEs agregadores responsáveis.
