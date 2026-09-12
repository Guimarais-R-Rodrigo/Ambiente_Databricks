# Template — README do Hub

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Este template vale
> para todo README do projeto, do menor ao da raiz.

Selecione a escala antes de escrever. Curta, Padrão e Longa usam o esqueleto
agregador abaixo; Objeto usa o contrato especializado referenciado. A ordem é
fixa dentro de cada escala, para o leitor localizar a mesma resposta sem
reaprender a navegação.

## Escalas

A pasta de um recurso individual pede explicação conceitual e decisão de uso;
uma pasta agregadora pede navegação. Não selecione a escala pela quantidade de
arquivos Python. Objeto é uma escala do tipo README, não um novo tipo de objeto.

| Escala | Quando usar | Seções |
|---|---|---|
| **Objeto** | pasta de um snippet, script ou prompt | contrato candidato em [template_objeto.md](template_objeto.md) |
| **Curta** | pasta com até 5 **pastas de objeto** | 1, 3, 5, 6, 7, 9 |
| **Padrão** | pasta de seção (`hub_snippets/spark/`, `hub_scripts/`) | as 9 |
| **Longa** | raiz do repositório e `.assistant/` | as 9 + extras posicionadas |

**Conte pastas de objeto, não arquivos.** `hub_snippets/display/` tem 3 objetos
(curta); `hub_snippets/spark/` tem 7 (padrão); `hub_padroes/` tem 7 subpastas
(padrão). A dúvida é real e produz READMEs de tamanhos diferentes para a mesma
pasta.

Na escala curta, "visão estrutural" e "o que existe aqui" viram o mesmo conteúdo
em dois formatos — mantenha só a tabela. E FAQ com menos de três perguntas reais
é FAQ inventada: omita.

## Transição da escala Objeto

A R01-A apresenta o contrato `objeto-v0.1-candidata`. Sua adoção é gradual:
esta entrega não instala novos gates nem declara os objetos existentes
migrados. Templates dos tipos, skill de criação, exemplares e integração serão
tratados nas próximas micro-sprints. O piloto R02 estabiliza o contrato.

Para escrever um README de objeto, use somente
[template_objeto.md](template_objeto.md) e confira
[checklist_objeto.md](checklist_objeto.md). Não acrescente as nove seções
agregadoras às quinze seções de objeto. `exemplo.md` continua sendo exemplar
agregador; os exemplares de objeto ainda não são entregues nesta micro-sprint.

## As nove seções — escalas agregadoras

| # | Seção | Responde | Obrigatória |
|---|---|---|---|
| 1 | Título + frase de identidade | "o que é isto, em uma linha" | sempre |
| 2 | Aviso de natureza | nativo da plataforma ou do Hub? | só onde há ambiguidade real |
| 3 | Para que serve / quando usar | "isto resolve o meu problema?" | sempre |
| 4 | Visão estrutural | diagrama ou árvore do que existe aqui | escala padrão e longa |
| 5 | Como usar — exemplo copiável | "me dá o comando" | sempre que houver o que executar |
| 6 | O que existe aqui | tabela do conteúdo, uma linha por item | se houver filhos |
| 7 | Limites e armadilhas | "o que dá errado e não é óbvio" | sempre |
| 8 | Perguntas frequentes | dúvidas reais de quem chega | quando houver ≥ 3 |
| 9 | Onde continuar | links para o próximo passo | sempre |

Na escala longa, seções extras entram entre a 7 e a 9, nunca antes da 5.

### Sobre a seção 2

Depois da reestruturação, quase tudo que tem README é do Hub. Repetir "isto é
customizado" em vinte pastas é ruído. Ela é obrigatória apenas onde alguém pode
se confundir de verdade: em `skills/`, que é estrutura **nativa** com conteúdo
nosso, e nos dois READMEs de topo.

## Regras de escrita

| Regra | Por quê |
|---|---|
| Um bloco visual por documento — tabela, mermaid ou saída real | parede de texto não é consultável |
| Termo técnico definido no primeiro uso, ou remetido ao vocabulário | o leitor que trava não volta |
| Nenhum número em prosa que envelheça sozinho | "as 12 skills" vira mentira na décima terceira; prefira "as skills de `skills/`" |
| Exemplo sempre copiável e testado | exemplo que não roda custa mais do que exemplo nenhum |
| Diagrama que ensina errado é pior que diagrama nenhum | confira o mermaid contra o código antes de publicar |
| PT-BR na prosa; preservar nomes reais da API, inclusive os existentes em português | não quebrar contratos para traduzir identificadores |
| Constante de domínio pode ser português | `AZUL_CAIXA` nomeia a paleta institucional; traduzir apaga o referente |

## Antes de dar por pronto — escalas agregadoras

```text
[ ] as seções obrigatórias da escala estão presentes, na ordem
[ ] há ao menos um bloco visual
[ ] todo link relativo resolve (o validador confere)
[ ] a tabela "o que existe aqui" bate com o conteúdo real da pasta
[ ] nenhuma contagem em prosa que vá envelhecer
[ ] os exemplos foram executados
```

O exemplo preenchido, no tema de campanha de CRM, está em
[`exemplo.md`](exemplo.md).
