# Hub Micromodelos

Área de domínio para especificar, explorar e demonstrar micromodelos no ecossistema `.assistant`.

## Para que serve e quando usar

Use esta área para ler o contrato `micromodelo.yaml`, validar sua consistência, descobrir oportunidades apenas com metadados, preparar artefatos de estudo e aprender pelo caso fictício de recência de contato. A [skill](../skills/hub-ml-micromodelos/SKILL.md) conduz o trabalho no Genie Code. Projetos com dados reais dependem do catálogo e das permissões corporativas.

## Visão estrutural

```text
hub_micromodelos/
├── contratos/  especificação JSON Schema e ponto de partida YAML
├── execucao/   funções de contrato, descoberta e laboratório
└── exemplos/   dados e roteiros inteiramente sintéticos
```

## Como usar

Abra o [exemplo completo de recência de contato](exemplos/recencia_contato/README.md). Com Python, `jsonschema`, `regex` e `PyYAML` disponíveis, execute o arquivo `exemplos/recencia_contato/executar_exemplo.py --conferir`. A execução lê somente os arquivos sintéticos vizinhos, imprime as classificações e compara com o resultado esperado.

## O que existe aqui

| Recurso | Papel |
|---|---|
| [Contrato JSON Schema](contratos/micromodelo.schema.json) | Define campos, tipos, valores e condições da especificação. |
| [Modelo YAML](contratos/micromodelo.template.yaml) | Ponto de partida, com decisões pendentes identificadas. |
| [Execução](execucao/README.md) | Biblioteca reutilizável e laboratório sintético. |
| [Exemplos](exemplos/README.md) | Casos didáticos e ensaio de migração fictícia. |

## Limites e armadilhas

O estudo sintético calcula classificações e uma força de evidência, não uma probabilidade nem uma decisão de negócio aprovada. A ausência de registros não vira `FALSE` automaticamente. A importação de módulos não lê catálogo, inicia MLflow ou publica objetos. A skill permanece em `L1/audit`; o código de laboratório e os exemplos não representam homologação corporativa.

## Onde continuar

Para entender cada atributo, siga o [README do micromodelo fictício](exemplos/recencia_contato/README.md). Para a API, consulte [execução](execucao/README.md). Os briefings conversacionais continuam em [Hub Prompts](../hub_prompts/README.md), e o panorama do ecossistema está no [Manual Técnico](../MANUAL_TECNICO.md).
