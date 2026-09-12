# Template — README do Hub

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Este template vale
> para todo README do projeto, do menor ao da raiz.

Todo README do Hub segue o esqueleto de sua escala. A ordem das seções é fixa: ela responde
às perguntas do leitor na sequência em que elas surgem, e trocar a ordem obriga
a ler o documento inteiro para achar o que se procurava.

## Quatro escalas

As nove seções abaixo orientam entradas agregadoras. Uma pasta de objeto tem
perguntas de conceito e escolha próprias, atendidas pelo molde específico.

| Escala | Quando usar | Seções |
|---|---|---|
| **Objeto** | pasta de snippet, script ou prompt | [quinze seções próprias](template_objeto.md) |
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

## As nove seções das escalas agregadoras

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
| PT-BR na prosa; preserve identificadores existentes, inclusive em português | não quebrar contratos em nome da tradução |
| Constante de domínio pode ser português | `AZUL_CAIXA` nomeia a paleta institucional; traduzir apaga o referente |

## Antes de dar por pronto

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

Na escala Objeto, aplique o [checklist editorial](checklist_objeto.md). A presença
das seções não comprova correção conceitual, execução nem aceite humano.
