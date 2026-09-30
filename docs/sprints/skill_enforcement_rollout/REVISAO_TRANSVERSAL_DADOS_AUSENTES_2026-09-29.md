# Revisão transversal — dados ausentes e evidência — 2026-09-29

(Codex) Revisão solicitada após a experiência de Safra. Escopo: instruções das
14 skills e templates pertinentes, com revisão independente das seis skills
transversais e de Baseline, Monitoramento e Pipeline. São achados documentais e propostas de reforço, **não falhas de
runtime demonstradas nem homologação conversacional das demais skills**.

## O que aconteceu em Safra

Após T01, foi editado SKILL.md e gerado/publicado o derivado: distinção entre
resposta conceitual e execução, CUMULATIVE/EVENT, quatro estados de cobertura,
maturidade dependente do corte e proibição de inventar ID/valor/causa ausentes.
O runner não mudou. T02 ainda inventou o valor de MOB2. Entre T02 e D01 não houve
nova edição/publicação: D01 usou seleção explícita @ e respondeu corretamente.
Isso não isola causalmente o efeito da alteração nem da seleção. Os resultados
originais estão no [registro consolidado](GENIE_SKILLS_RESULTADOS_2026-09-28.md).

## Princípio aplicável às outras skills

1. Separar informação fornecida, hipótese explícita, dado desconhecido e resultado observado.
2. Conservar desconhecidos: não substituir por zero, data, ID, label ou causa plausível.
3. Explicação pode usar cenário hipotético identificado; esse cenário não altera as entradas do caso real nem legitima conclusão sobre ele.
4. Distinguir conta ilustrativa, execução canônica, verificação e efeito remoto. Preservar preflights, runners, Receipt/Postflight e bloqueios existentes.
5. Templates devem aceitar pendente/não informado/não suportado/não aplicável com motivo; não pressionar o preenchimento fictício de todos os campos.
6. Exigir prova adequada ao estado alegado: declaração, proposta, seleção de skill, chamada, readback e conclusão não são equivalentes.

Os estados IMMATURE/NO_OBSERVATIONS/COMPLETE/INCOMPLETE pertencem ao contrato
Safra. Não são uma taxonomia genérica para copiar em todas as skills. Também
não é adequado exigir runner de uma skill editorial ou explicativa que não o tem.

## Matriz da revisão

| Skill / fonte | Proteção existente ou tensão documental | Aplicação recomendada |
|---|---|---|
| [Safra](../../../ambiente_fonte/.assistant/skills/hub-ml-analise-safra/SKILL.md) | Ajuste já aplicado: conceitual versus execução, quatro estados e dados ausentes. T01/T02 FAIL, D01 PASS com seleção explícita. | Manter evidências separadas; não atribuir causalidade à mudança ou ao @ com três respostas. Modo espontâneo permanece pendente. |
| [EDA](../../../ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md) | Seção Definir o contrato permite continuar com hipóteses; gates L4, chave confirmada e pendências materiais já são explícitos. | Priorizar clareza: hipóteses para planejamento não preenchem entradas objetivas nem permitem bypass do runner/Postflight. |
| [Cross-EDA](../../../ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/SKILL.md) | Contexto L2 distingue DECLARED_NOT_READ de cobertura medida; PIT UNKNOWN permanece pendente. Receber o contexto diz “Exigir ou inferir explicitamente”. | Priorizar delimitação de inferência: proposta de chave/grão/corte não vira confirmação; sem fonte e disponibilidade não inferir elegibilidade nem match. |
| [Estatística](../../../ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md) | Perfil KS declara IC não suportado e pressupostos fornecidos pelo usuário. Formato geral de saída pede effect size com intervalo. | Priorizar coerência do formato: marcar IC não suportado/pendente; não inventar amostra, desenho, alfa ou p-valor para completar o card. |
| [Tutor](../../../ambiente_fonte/.assistant/skills/hub-ml-tutor-databricks/SKILL.md) | Distingue intenção do código de resultado comprovado; permite exemplos pequenos. Templates ainda pressionam status e “Tabela escrita”. | Priorizar exemplos explicitamente fictícios, status NÃO INFORMADO e saída esperada versus observada. Exemplo didático não completa o caso real. |
| [Explainability](../../../ambiente_fonte/.assistant/skills/hub-ml-explainability/SKILL.md) | Runner exige modelo, X, background e ordem vinculados; separa Receipt de verificação e SHAP de causalidade. | Reforço específico útil: background/intercepto/features desconhecidos não recebem zero por conveniência; contas conceituais não são SHAP executado. |
| [Features](../../../ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md) | Sem contexto, modo exploratório sem afirmar ausência de leakage; lag por observação, PIT e materialização possuem contratos distintos. | Reforço específico útil: ausência de histórico não é zero; disponibilidade desconhecida não é atraso zero; exemplo exploratório não prova PIT/fit/materialização. |
| [Baseline](../../../ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/SKILL.md) | Contrato obrigatório, sem target/tempo não executar; não inventar AUC sem labels; tracking exige readback e verificação antes da limpeza. | Reforço narrativo proporcional: métricas planejadas ou esperadas ficam distintas de medidas; split/períodos/labels não devem ser fabricados para completar exemplos. |
| [Monitoramento](../../../ambiente_fonte/.assistant/skills/hub-ml-monitoramento-modelo/SKILL.md) | Já proíbe limiares universais, separa drift de performance e exige labels disponíveis no corte e política externa. | Reforço específico útil: bins propostos não são política aprovada; sem labels/corte não atribuir AUC ou maturidade; sem limiar não fabricar severidade. |
| [Pipeline](../../../ambiente_fonte/.assistant/skills/hub-ml-pipeline-builder/SKILL.md) | Separa spec L2, Spark temporário e Delta; escrita exige autorização externa/readback; UNKNOWN não permite repetir escrita. | Prioridade menor: explicitar destino, SLA e DQ ainda propostos; plano não é efeito. Preservar o protocolo existente, sem outro executor. |
| [Criar Objeto](../../../ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md) | Separa gerado/validado/escrito e exige evidência literal. Formato pede artefatos completos, não esboços. | Ajuste opcional: completude estrutural não autoriza inventar requisito funcional ausente. Manter gates atuais. |
| [Auditoria](../../../ambiente_fonte/.assistant/skills/hub-ml-auditoria-skills/SKILL.md) | Distingue evidência observada/reverificada, informação ausente, autorrelato e execução canônica. | Sem lacuna material identificada neste eixo; manter as regras e verificar comportamento nos testes próprios. |
| [Concierge](../../../ambiente_fonte/.assistant/skills/hub-ml-concierge/SKILL.md) | Proíbe inventar target/chave/limiar/autorização e distingue menção, carregamento e handoff. | Sem lacuna material identificada neste eixo; não duplicar instruções existentes. |
| [Comentar Notebook](../../../ambiente_fonte/.assistant/skills/hub-ml-comentar-notebook/SKILL.md) | Exige valores observados ou pendência; proíbe inventar resultados e preencher placeholders por suposição. | Sem lacuna material identificada neste eixo; manter os controles existentes. |

## Referências pontuais e ordem sugerida

Primeiro, resolver ambiguidades existentes: EDA (SKILL linha 19), Cross-EDA
(linha 77), Estatística (perfil sem IC, linhas 33–35, versus formato nas linhas
179–183) e Tutor. No Tutor, examinar também
[status do notebook](../../../ambiente_fonte/.assistant/skills/hub-ml-tutor-databricks/templates/explicacao_notebook.md)
e [saídas do bloco](../../../ambiente_fonte/.assistant/skills/hub-ml-tutor-databricks/templates/explicacao_bloco_codigo.md).

Depois, reforços curtos específicos de Explainability, Features, Monitoramento e
Baseline. Pipeline e Criar Objeto já têm barreiras explícitas; qualquer reforço
deve melhorar a clareza das entradas narrativas sem duplicar mecanismos.
Auditoria, Concierge e Comentar Notebook não justificam uma cópia do bloco Safra.

Possíveis verificações direcionadas, ainda **propostas / NOT_RUN**:

- EDA/Cross: contexto sem chave/corte; propor confirmação sem inventar dados ou declarar cobertura/PIT validado.
- Estatística: pedido de IC no piloto que não o suporta; manter UNSUPPORTED_IN_PROFILE.
- Tutor: notebook sem saída nem status; descrever intenção, não afirmar escrita ou ambiente produtivo.
- Explainability: background ausente; não completar com zero nem alegar SHAP executado.
- Features: disponibilidade ausente; não certificar elegibilidade temporal.
- Monitoramento: scores sem labels ou política; não fabricar performance ou severidade.
- Baseline/Pipeline: plano sem resultados/readback; não preencher métricas, IDs de execução ou efeitos como fatos.

Essas sugestões não alteram os estímulos congelados nem acrescentam resultados
à campanha atual. Devem ser vinculadas a uma versão e a um ID antes da execução.

## Estado desta revisão

Somente relatório e CHANGELOG atualizados; nenhuma skill, template, contrato,
runner ou policy foi editado nesta revisão, e nenhuma nova publicação ocorreu.
A versão do próximo teste SD-VF-N permanece a mesma. A matriz prioriza mudanças
pontuais; não afirma que todas as skills têm o defeito observado em Safra.

Revisão independente BL/MO/Pipeline encerrada sem achado material adicional:
contratos e gates atuais já protegem cálculo e efeitos; reforços propostos
limitam-se à distinção narrativa entre plano, entrada confirmada e resultado.
Não introduzir enumerações novas nos schemas fechados para esses reforços.

## Implementação posterior autorizada

Os ajustes prioritários de EDA, Cross-EDA, Estatística e Tutor foram aplicados
após esta revisão. Estado de validação/publicação no [registro da implementação](CORRECOES_TRANSVERSAIS_2026-09-29.md). As demais propostas permanecem não aplicadas.
