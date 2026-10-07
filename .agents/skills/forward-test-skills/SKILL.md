---
name: forward-test-skills
description: >-
  Prepara e registra testes de seleção das skills de produto no Genie Code,
  com positivo, negativo e @menção em chats novos. Use após mudanças de
  descoberta/description; não como prova de qualidade, execução ou homologação.
---

# Forward tests das skills no Genie Code

## Intenção e pré-condições

O objeto é **roteamento observado** no Genie Code: qual skill foi carregada
para cada pedido. Não é teste de análise, qualidade da resposta, execução de
helper, enforcement ou carregamento destas cinco skills de manutenção em
clientes de código. Essas avaliações precisam de campanhas próprias.

Leia o [índice vigente](../../../docs/testes/forward/README.md), o
[roteiro histórico e suas ressalvas](../../../docs/testes/forward/roteiro.md)
e o [catálogo atual do produto](../../../ambiente_databricks/.assistant/skills/README.md).
Precisa de SHA escolhido, descrições e inventário desse SHA, publicação
verificada no destino autorizado e chat Genie disponível. Sem comprovar qual
versão foi publicada, não atribua a ela o resultado. Cota/interface indisponível
bloqueia os casos, mesmo se compute e APIs continuarem funcionando.

Preparar uma campanha não autoriza publicar, escrever registros no workspace,
executar dados, mudar `description` ou usar um destino corporativo. Nesta migração,
teste apenas o procedimento com registros sintéticos locais; não envie casos
reais ao Genie como prova de portabilidade sem escopo próprio.

## Preparar a campanha e seu corpus

A matriz histórica tem **14 skills × 3 casos = 42**; o conjunto anterior tem
39/39 PASS registrados. O índice preserva pendências do Concierge; Micromodelos
e SER/B1 possuem evidências próprias. Não converter a matriz 42, 39/39 ou essas
campanhas em **45/45 PASS** do catálogo atual. Números históricos não mudam
quando entra uma skill nova.

Para outra rodada, crie manifesto de casos identificado: campanha/data,
branch/SHA, catálogo/descrições, destino sanitizado, casos P/N/M, prompt exato,
artefatos exigidos, resultado esperado, observador e forma de evidência.
Comece casos não executados em `NOT_RUN`, sem copiar PASS anterior.

“Sem contexto extra” significa sem pistas/anexos **não previstos** que induzam
a seleção. Forneça o notebook, tabela fictícia ou outro artefato sintético
exigido pelo caso. Omissão desse corpus pode invalidar o instrumento. Leia o
[handoff de calibração](../../../docs/handoffs/2026-08-14_calibracao-descriptions.md)
antes de atribuir uma falha à `description`. Se revisar o corpus, versione o
caso e preserve a tentativa anterior; não a reclassifique silenciosamente.

Se uma avaliação exigir sessão cega, declare corpus permitido/proibido e
confirme contexto inicial. Histórico pré-carregado incompatível invalida o
rótulo “cego”; prossiga apenas como contexto completo, com essa limitação.

## Método de observação

1. Abra **um chat novo por caso** para evitar histórico/metadata de outra
   tentativa. Não reutilize o chat entre casos. Mudanças de skill requerem nova
   conversa para teste; cache persistente pede hard refresh e nova tentativa
   identificada, preservando a anterior.
2. Envie o prompt exato com apenas o corpus exigido. O roteiro usa uma primeira
   mensagem de seleção e uma segunda de registro: não antecipe o pedido de
   gravação na primeira, pois isso altera a intenção testada.
3. Observe o indicador de carregamento na interface. Nome citado na resposta
   ou autorrelato do agente não prova seleção; evidência insuficiente fica
   `NÃO VERIFICADO`/`PENDENTE`. Registre observação separada da interpretação.
4. Se a segunda mensagem pedir arquivo remoto, só a envie com destino e escrita
   autorizados. Caso contrário, registre localmente a observação. Não copie
   identidades/paths do roteiro histórico para o destino de outra pessoa.
5. Não execute código ou consulte dados reais para medir seleção. Registre
   separadamente qualquer avaliação de qualidade ou execução autorizada.

## Veredito por caso

| Caso | PASS exige observação |
|---|---|
| Positivo (P) | a skill alvo foi carregada por relevância |
| Negativo (N) | a skill alvo ficou de fora; a vizinha ideal é informação adicional |
| Menção (M ou @) | a seleção explícita `@nome-da-skill` carregou a alvo |

`@` é seleção explícita a verificar, não garantia universal de determinismo ou
da qualidade da resposta. Falta de observação não é FAIL de roteamento
comprovado nem PASS: descreva o limite. Tentativa impedida fica `BLOQUEADO`;
caso não tentado fica `NOT_RUN`.

## Registro, correção e encerramento

Use uma cópia do [template](../../../docs/testes/forward/template_resultados.md)
em `docs/testes/forward/resultados/<YYYY-MM-DD>_rodada<N>.md`, adaptando apenas
a nova cópia ao manifesto da campanha. Preserve a matriz histórica e inclua
SHA, IDs, prompt/corpus, sessão, esperado, observado, evidência e veredito.

Falha P/N: primeiro confira instrumento, corpus e vizinhas. Se uma correção de
`description` for necessária e autorizada, edite em `ambiente_databricks/`, valide,
renderize com preflight, publique com autorização e repita os casos afetados e
vizinhos em chats novos. Não altere produto automaticamente para fechar este
teste. Falha de menção: confira path, frontmatter, duplicatas e versão publicada.

Feche a rodada no resultado datado acima, informando descrições alteradas e casos
não testados. Registre no [CHANGELOG](../../../CHANGELOG.md) apenas mudanças
relevantes de uso/contrato, conforme o [critério](../../../docs/ai/templates/changelog-entry.md). Um PASS de seleção não certifica runtime nem
libera replicação corporativa por si só.

## Casos de aceitação do procedimento

- **Positivo:** “Prepare os P/N/M para as descrições deste SHA.” Produzir casos
  identificados `NOT_RUN`, preservando histórico e corpus exigido.
- **Negativo de intenção:** “Prove que o modelo treinou corretamente.” Não usar
  roteamento como evidência de execução/qualidade.
- **Pré-requisito ausente:** chat/cota, publicação do SHA ou indicador observável
  indisponível. Marcar BLOQUEADO/PENDENTE conforme o caso, sem PASS inventado.
