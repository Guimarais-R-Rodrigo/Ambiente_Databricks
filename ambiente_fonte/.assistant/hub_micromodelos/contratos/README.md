# Contrato `micromodelo.yaml`

## Revisar uma alteração

Copie o template para um caso autorizado e preserve o original. Preencha fatos conhecidos e pendências honestas; execute da raiz `.assistant`:

```python
from pathlib import Path
from hub_micromodelos.execucao import especificacao, assinatura
spec = especificacao.load_document(Path("hub_micromodelos/exemplos/recencia_contato/micromodelo.yaml"))
schema = especificacao.load_schema(Path("hub_micromodelos/contratos/micromodelo.schema.json"))
issues = especificacao.validate_spec(spec, schema)
for issue in issues:
    print(issue)
if not issues:
    print(assinatura.calculate_spec_fingerprint(spec, schema))
```

Resolva erros de schema e invariantes antes de comparar assinatura. YAML válido com `validacao.status=PENDENTE` ainda é proposta. Um score de força de evidência não é probabilidade. Fingerprint compara conteúdo material; não é assinatura criptográfica de um aprovador.

O [JSON Schema](micromodelo.schema.json) define campos, tipos e condições; o [template](micromodelo.template.yaml) é o ponto de partida. O YAML do [exemplo preenchido](../exemplos/recencia_contato/micromodelo.yaml) mostra escolhas concretas. O [README do exemplo](../exemplos/recencia_contato/README.md#mapa-de-todos-os-atributos-do-yaml) percorre os atributos e justifica os valores.

## Leitura por blocos

| Bloco | Pergunta que responde |
|---|---|
| `identidade`, `negocio` | Qual característica, decisão, versão, fase e usos permitidos ou vedados? |
| `entidade`, `fontes` | Quem é classificado, em qual grão/instante e de onde viriam os sinais? |
| `evidencias`, `contra_evidencias`, `classificacao` | O que sustenta cada classe, como resolver conflito e o que fazer na ausência de evidência? |
| `score` | O que o número significa, como é calculado e se exige calibração? |
| `experimentos`, `validacao` | Que hipóteses e critérios serão medidos, qual resultado foi observado e quem aprovou? |
| `saida`, `tracking`, `publicacao` | Qual é o formato do estudo, qual política de saída foi definida, onde ficam runs e qual é o estado do handoff? |
| `governanca`, `proveniencia` | Quem responde por dados e uso, e qual parte foi proposta, descoberta, medida ou aprovada? |

Um YAML que passa no schema ainda pode conter `PENDENTE`, `PROPOSTO` ou fontes candidatas: **validade estrutural não é validação de negócio**. Campos `null` não são lacunas escondidas quando o estado ainda não ocorreu; o motivo e a condição de preenchimento devem aparecer no caso e na revisão. A fase do micromodelo e as provas de proveniência são verificadas também por invariantes em `execucao/especificacao.py`.

## O que muda a assinatura

`execucao/assinatura.py` calcula um hash da parte material da especificação. Mudanças em fontes, evidências, regras, limiares, score e contrato de saída podem mudá-lo; texto editorial sem efeito material pode preservá-lo. A assinatura permite comparar especificações, **não comprova execução, aprovação nem integridade de um Produto de Dados**.

## Condições que não podem ser preenchidas por suposição

- `INDETERMINADO` não vira `FALSE` apenas porque não há registros. Regra explícita de ausência precisa de referência e proveniência aprovadas.
- `PROBABILIDADE_CALIBRADA` exige método e evidência de calibração; um score 0–100 pode ser somente força de evidência.
- `validacao.status=APROVADO` exige resultado medido e aprovação humana correspondente.
- `saida.publicacao.estado=DEFINIDO` exige política de saída, inclusive tratamento estruturado do indeterminado.
- `publicacao` depende da governança externa; o handoff técnico não concede esse estado.

O [caso de recência](../exemplos/recencia_contato/README.md#atributos-condicionais-do-schema) explica os campos condicionais e por que permanecem pendentes no exemplo. Para operar a sequência, volte ao [guia de jornada](../guias/README.md).
