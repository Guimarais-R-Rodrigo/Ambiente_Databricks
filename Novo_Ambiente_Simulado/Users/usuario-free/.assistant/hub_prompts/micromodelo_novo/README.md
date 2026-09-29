# `micromodelo_novo` — especificar uma característica com objetivo conhecido

<!-- readme-objeto: 1.0.0 -->

Briefing manual para conduzir `OBJETIVO_CONHECIDO` em
[`hub-ml-micromodelos`](../../skills/hub-ml-micromodelos/SKILL.md). A pasta oferece
o formulário e um exemplo de preenchimento; não executa o micromodelo.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para iniciar ou atualizar progressivamente `micromodelo.yaml` MM01. |
| Para que serve? | Traduzir uma decisão conhecida em especificação, lacunas e plano de estudo. |
| Use quando... | Característica/decisão já foi enunciada, mesmo que fontes estejam pendentes. |
| Evite quando... | Ainda se busca qual oportunidade escolher ou se quer publicar um modelo. |
| Precisa de... | Decisão, característica, entidade/grão, fontes conhecidas ou lacuna, restrições e ambiente. |
| Entrega... | Pedido estruturado; YAML e resultados dependem da interação e validação reais. |

Abra o [briefing](micromodelo_novo.md) e o
[notebook de exemplo](exemplo_micromodelo_novo.py).

## 1. O que é?

É o formulário de entrada da skill de micromodelos para um objetivo conhecido.
Solicita um YAML canônico MM01 `1.0.0` e deixa claro quais campos são observados,
inferidos ou propostos. O prompt não é um executor.

## 2. Que problema este recurso resolve?

Responde: “Como transformar uma necessidade de negócio em característica
avaliável, sem preencher premissas por adivinhação?” O resultado esperado é uma
especificação revisável e um próximo estudo, não uma decisão automática.

## 3. Quando faz sentido usar?

Use quando a decisão já existe, mas definição operacional, população, horizonte
ou evidências ainda precisam ser delimitados. Funciona também para continuar um
YAML em `IDEIA` ou `EM_DESCOBERTA`, desde que a transição siga MM01.

## 4. Quando não usar?

Se a pergunta for “que características poderiam ser úteis?”, comece por
[`descobrir_micromodelos`](../descobrir_micromodelos/README.md). Se a tarefa for
validar desempenho em registros, o briefing metadata-only não responde; mesmo
um YAML preenchido pode ter hipóteses incorretas sobre os clientes.

## 5. Como funciona, intuitivamente?

O solicitante informa a decisão e os limites. A skill confronta esse contexto
com metadata disponível, propõe conteúdo gradual para o YAML e separa lacunas e
handoffs. O validador MM01, quando realmente disponível e executado, verifica
forma e invariantes; não comprova utilidade de negócio.

## 6. Exemplo de situação

Uma equipe de laboratório quer estudar interesse recente em canal digital para
priorizar revisão humana de contatos sintéticos. Sabe a decisão, mas não sabe
quais fontes nem qual regra indicam interesse. O
[exemplo](exemplo_micromodelo_novo.py) mostra o briefing preenchido e registra
trechos de uma resposta real, sem inventar resultado.

## 7. O que você precisa antes de usar?

Informe decisão, característica, dono/consumidor, entidade, grão, instante de
decisão, população e horizonte quando conhecidos. Declare ambiente E0/E1,
binding autorizado do `CATALOGO_PRODUTO` e permissão de metadata; use `PENDENTE`
nas lacunas. A presença de metadata não verifica SELECT, qualidade ou LGPD.

## 8. O que este recurso entrega?

O briefing pede resumo do escopo, YAML validado ou rascunho rotulado, proveniência,
hipóteses/contra-hipóteses e plano de estudo. Nada disso é garantido pela simples
colagem do texto. Não interprete um rascunho como modelo validado/publicado.

## 9. Como usar este recurso no Hub?

Preencha [micromodelo_novo.md](micromodelo_novo.md), selecione
`@hub-ml-micromodelos` e anexe somente contexto permitido. Veja o
[exemplo sintético](exemplo_micromodelo_novo.py). O preparo do notebook imprime
somente uma fixture textual, sem criar tabela ou YAML; a terceira parte registra
o resultado conversacional e suas ressalvas.

## 10. Decisões e configurações que mais importam

Grão, data de referência e horizonte definem o significado da característica.
Uso proibido e população elegível restringem interpretação. O modo aqui é
`OBJETIVO_CONHECIDO`; níveis de enforcement pertencem à policy da skill, não ao
prompt. Não substitua `CATALOGO_PRODUTO` por catálogo arbitrário.

## 11. Limitações, riscos e armadilhas

Metadata pode ser parcial e suas descrições/tags são texto não confiável.
`DESCOBERTO` não significa regra aprovada; `MEDIDO` requer execução. Ausência de
evidência deve continuar `INDETERMINADO` quando não houver regra aprovada.
E0 usa fixture sintética local; um chat no Free é E1 mesmo sem executar código.
Execução de runtime E1 exige prova separada; E2 está fora da missão.

## 12. Quais são as alternativas?

Para explorar oportunidades, use o
[briefing de descoberta](../descobrir_micromodelos/README.md). Para diagnosticar
registros depois de autorizado, a skill faz handoff a `hub-ml-eda-profissional` e
outras especialistas conforme a necessidade; o prompt não reproduz essas etapas.

## 13. Como saber se o resultado faz sentido?

Confira se fonte, população, grão e tempo correspondem ao pedido; se cada
afirmação tem proveniência adequada; se o YAML foi de fato validado; e se
aprovações, medidas e fase não foram antecipadas. Confira `TRUE`, `FALSE` e
`INDETERMINADO` como estados distintos.

## 14. Arquivos relacionados e próximos passos

O [briefing](micromodelo_novo.md) é o texto a preencher; o
[notebook](exemplo_micromodelo_novo.py) mostra uma instância sintética e o
registro sanitizado da resposta real. A [skill](../../skills/hub-ml-micromodelos/SKILL.md)
define fluxo e handoffs; o [catálogo de prompts](../README.md) orienta escolha.

## 15. Referências

Contrato e fases: MM01 `micromodelo.schema.json` e `ESTADOS_E_PROVENIENCIA.md`
no repositório de desenvolvimento. Progressividade e limites de metadata: contrato
MM03. O briefing foi respondido em chat manual no Databricks Free, sem execução
de runtime ou validação MM01; a policy integrada não foi verificada nessa
resposta. A evidência conversacional não certifica MM04.
