# Skills operacionais deste repositório

## Duas famílias de skill, e por que não se confundem

Este projeto tem skills em dois lugares, com propósitos opostos. Confundi-las é o
mal-entendido mais provável de quem chega:

| | Skills **desta** pasta | Skills `rodrigo-*` |
|---|---|---|
| Onde vivem | `.claude/skills/` | `ambiente_fonte/.assistant/skills/` |
| Quem as executa | o assistente que trabalha **no repositório** | o Genie Code, **dentro do Databricks** |
| Sobre o que agem | os arquivos deste projeto | dados, notebooks e modelos do workspace |
| Exemplo de uso | "valide e publique o ambiente" | "faça a EDA desta tabela" |
| Vão para o workspace? | não, ficam só aqui | sim, são o produto |

Em resumo: as daqui **constroem** o ecossistema; as de lá **são** o ecossistema.
Uma skill que ensina a rodar `validate_assistant.py` não tem utilidade dentro do
Databricks, e uma skill de análise de safra não tem o que fazer no repositório.

## O que existe hoje

| Skill | Faz o quê | Status |
|---|---|---|
| `validar-assistant` | Bateria de validação do `ambiente_fonte/` | ✅ ativa |
| `render-simulado` | Gera `Novo_Ambiente_Simulado/` a partir do fonte | ✅ ativa |
| `publicar-free` | Publica no Free: plano, gate `--execute` e verify | ✅ ativa |
| `forward-test-skills` | Roteiro de testes das 12 skills no Genie Code | ✅ ativa |
| `replicar-trabalho` | Pré-requisitos e guardrails da cópia para o trabalho | ✅ ativa |
| `revisar-docs-oficiais` | Revisão periódica da documentação oficial (vanguarda) | ⏳ planejada |

## Como uma skill daqui é acionada

Pelo pedido em linguagem natural: descrever a intenção ("preciso publicar o
ambiente no Free") faz o assistente carregar a skill correspondente e seguir o
procedimento dela. O efeito prático é que o procedimento não precisa ser
lembrado — nem por você, nem por outra IA que assuma o trabalho depois.

## Criar uma nova

Uma pasta com `SKILL.md` dentro, contendo frontmatter com `name` idêntico ao
nome da pasta e uma `description` que diga **quando** usar, não apenas o que faz.
Descrição vaga produz skill que nunca é escolhida.

O script executável, se houver, mora em `tools/` na raiz do repositório, e a
skill o referencia por caminho relativo. Separar as duas coisas mantém o script
testável fora do contexto de conversa. Registre a nova skill na tabela acima e
no `CHANGELOG.md`.
