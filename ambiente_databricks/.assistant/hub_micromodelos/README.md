# Hub Micromodelos

## Conferir o primeiro resultado

Os comandos abaixo partem da raiz `.assistant`, que contém `hub_micromodelos/`, e leem a fixture original. Saída esperada: população 7, `TRUE=2`, `FALSE=1`, `INDETERMINADO=4`, três scores, handoff `DRAFT_NOT_SUBMITTED` e `published=false`. Imprimem em stdout; não consultam nem gravam tabelas. Se divergir, compare YAML, dados e oráculo antes de adaptar o caso. Este quickstart é aprendizado, não validação de uso real.

Dependências: Python com `jsonschema`, `regex` e `PyYAML`. O ensaio local de documentação foi conferido em Python 3.12.14; isso não estabelece uma faixa universal de runtimes suportados.

Micromodelo é uma **característica delimitada, com regra, evidências e incerteza explícitas**, usada para apoiar uma decisão. Esta área do Hub guarda o contrato e o código de estudo. Cada micromodelo concreto é descrito em um `micromodelo.yaml`; a [skill conversacional](../skills/hub-ml-micromodelos/SKILL.md) orienta a Genie Code, mas não executa automaticamente a biblioteca. Os briefings continuam em `hub_prompts/`.

## Por onde começar

| Seu objetivo | Primeira leitura | Próxima ação |
|---|---|---|
| Entender o funcionamento completo | [Jornada e limites](guias/README.md) | Seguir as etapas de descoberta, especificação, estudo e entrega. |
| Avaliar um micromodelo preenchido | [Recência de contato](exemplos/recencia_contato/README.md) | Conferir as sete pessoas fictícias, a classificação e o rascunho de entrega. |
| Criar ou revisar um YAML | [Guia do contrato](contratos/README.md) | Partir do template, validar e registrar decisões ainda pendentes. |
| Usar o código | [Execução](execucao/README.md) | Escolher o módulo da etapa; informar ambiente e permissões explicitamente. |
| Conversar com a Genie Code | [Skill](../skills/hub-ml-micromodelos/SKILL.md) | Selecionar a skill e fornecer um briefing com escopo e restrições. |

Para ver o exemplo local, a partir da raiz `.assistant`, com Python, `jsonschema`, `regex` e `PyYAML` disponíveis:

```powershell
python hub_micromodelos/exemplos/recencia_contato/executar_exemplo.py --conferir
python hub_micromodelos/exemplos/recencia_contato/conferir_entrega.py
```

O primeiro comando valida o YAML e reconcilia classes e scores com o resultado esperado. O segundo monta **apenas um rascunho de handoff**, com contagens conferidas e decisões pendentes; não publica.

## Como as peças se encaixam

```text
.assistant/
├── skills/hub-ml-micromodelos/    método de conversa e contrato estático de roteamento
├── hub_prompts/                  briefings de uso da skill
└── hub_micromodelos/            módulo de domínio e código instalado com o Hub
    ├── guias/                   percurso, responsabilidades e limites por etapa
    ├── contratos/               schema, template e leitura dos estados do YAML
    ├── execucao/                módulos de validação, descoberta e laboratório
    └── exemplos/                fixtures e ensaios inteiramente sintéticos
        └── recencia_contato/    YAML preenchido, dados, resultado e handoff
```

As pastas correspondem a trabalhos diferentes. `contratos/` define **o que um micromodelo declara**; `execucao/` contém **o que o código consegue conferir ou calcular**; `exemplos/` mostra **como isso aparece em um caso**; `guias/` liga essas peças às decisões humanas. O [mapa de capacidades](guias/README.md#capacidades-atuais-e-seus-limites) distingue implementação, demonstração local e etapas posteriores. Nenhuma pasta vazia representa uma capacidade futura.

## Percurso em poucas linhas

1. **Descobrir ou receber um objetivo.** No modo `DESCOBRIR_OPORTUNIDADES`, metadata autorizada gera hipóteses para triagem. No modo `OBJETIVO_CONHECIDO`, um briefing define a decisão e pode iniciar um YAML. Metadata não autoriza leitura de registros.
2. **Especificar.** Declarar entidade, grão, tempo, fontes, evidências, contraevidências, regras de `TRUE`/`FALSE`/`INDETERMINADO`, score, validação e proveniência no YAML. Validar contrato e calcular sua assinatura material.
3. **Estudar.** Executar somente com dados e permissões próprios do ambiente. O laboratório incluso é sintético; qualidade, calibração e generalização precisam de avaliação separada.
4. **Registrar e revisar.** MLflow guarda histórico de runs quando uma rota o utiliza; o YAML continua sendo a especificação. Uma run não aprova o micromodelo. O handoff apenas prepara evidências e pendências para a governança externa.
5. **Publicar, se autorizado.** Produto de Dados, permissões, retenção e aceite pertencem à autoridade institucional; este módulo não faz autopublicação.

## Uso e limites

A skill ajuda a especificar e revisar o caso. A biblioteca e os exemplos são chamados explicitamente. O exemplo usa dados fictícios e não demonstra validade sobre dados reais, autorização institucional ou publicação. Consulte também a policy da skill: seu nível atual e o escopo protegido continuam sendo contrato operacional. Código importável não concede execução protegida, Receipt ou promoção de nível. A skill permanece `L1/audit`; `target_level=L3` não é capacidade presente. Consulte a [policy](../hub_padroes/skill_enforcement/README.md), o [Manual](../MANUAL_TECNICO_V2.md#micromodelos) e a [jornada](guias/README.md).
