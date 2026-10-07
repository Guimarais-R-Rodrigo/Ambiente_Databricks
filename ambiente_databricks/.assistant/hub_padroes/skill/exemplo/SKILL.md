---
name: hub-ml-analise-campanha
description: Analisa resultado de campanha de relacionamento encerrada — taxa de resposta por segmento e canal, precisão da estimativa e recomendação de alocação de orçamento para a próxima rodada. Use quando a pergunta for onde investir o próximo orçamento de contatos. Não cobre desenho experimental, teste A/B nem atribuição de causa.
---

> **EXEMPLO DOS PADRÕES DO HUB — NÃO PUBLICADO.** Esta skill vive em
> `hub_padroes/skill/exemplo/` e **não** deve ser copiada para
> `.assistant/skills/`. Publicada, entraria no roteamento real e disputaria
> vocabulário com as skills de verdade.

# Análise de campanha de relacionamento

## Quando esta skill se aplica

**Caso típico.** Uma campanha terminou, existe uma base com uma linha por
contato, e alguém precisa decidir a alocação da próxima.

**Não se aplica** quando: a campanha ainda está em curso — taxa parcial compara
períodos de exposição diferentes; ou quando a pergunta é "por que este cliente
respondeu", que é explicabilidade de modelo e não medição de campanha.

## Fluxo

1. **Confirme a unidade de análise.** Uma linha por contato, ou por cliente? Se a
   mesma pessoa foi contatada duas vezes, a taxa passa a pesá-la em dobro.
   Rode `checar_base_campanha` antes de qualquer medição.
2. **Declare a restrição de orçamento em número de contatos.** Sem ela a
   pergunta vira "qual segmento responde mais", que tem resposta diferente.
3. **Meça com a precisão junto.** Taxa sem base e sem intervalo não sustenta
   comparação entre segmentos de tamanhos diferentes.
4. **Separe significância de relevância.** Um segmento pequeno pode ter
   diferença estatisticamente real e ainda assim ser irrelevante — o teto
   absoluto de respostas é o tamanho dele.
5. **Recomende, e diga o que a recomendação não sustenta.** Custo por canal,
   receita por resposta e capacidade de atendimento raramente estão na base.

## Usar helpers da biblioteca

A tabela é conceitual: `hub_scripts.checar_base_campanha` e `hub_snippets.campanha.taxa_resposta_campanha` são caminhos fictícios desta skill não roteável. Não tente importá-los. Estude os exemplares em [script](../../script/checar_base_campanha/README.md) e [snippet](../../snippet/taxa_resposta_campanha/README.md); use apenas APIs verificadas da instalação real.

| Demanda | Módulo | API |
|---|---|---|
| Validar grão, nulos e base mínima antes de medir | `hub_scripts.checar_base_campanha` | `checar_base_campanha` |
| Taxa por segmento com intervalo e marca de decisão | `hub_snippets.campanha.taxa_resposta_campanha` | `taxa_resposta_campanha` |
| Comparar distribuição entre períodos | `hub_snippets.spark.psi_calculator` | `calcular_psi` |
| Formatar número para leitura executiva | `hub_snippets.constants.format_br` | `fmt_int`, `fmt_pct` |

## O que nunca fazer

- **Recomendar segmento por taxa, ignorando o tamanho.** É o erro mais comum e o
  mais caro: o segmento com a maior taxa costuma ser o menor.
- **Projetar a próxima campanha sobre as mesmas pessoas assumindo a mesma taxa.**
  Responder a um segundo contato em poucas semanas não é o mesmo processo.
- **Tratar resposta nula como não-resposta.** Enviesa a taxa para baixo sem
  deixar rastro. Recuse e peça a decisão.
- **Comparar seis intervalos e escolher o maior.** É comparação múltipla
  disfarçada de leitura de tabela.

## Formato de saída

Duas peças, sempre:

- **Tabela por segmento** com contatados, respostas, taxa, intervalo, largura do
  intervalo e se sustenta decisão.
- **Síntese executiva de até 8 linhas**, em português, sem código, dizendo a
  recomendação, o volume esperado de respostas e **o que não foi possível
  concluir**. Esta última parte não é ressalva de rodapé: é o que separa análise
  de relatório.
