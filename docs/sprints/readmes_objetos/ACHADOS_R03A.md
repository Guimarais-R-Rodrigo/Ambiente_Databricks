# Achados R03-A — descrição fiel sem alteração funcional

Base integrada: `5493f7db68f397ad7040485cb09bad53eb79be74` (2026-09-12).
Autor e revisor: ChatGPT, autorrevisão A0_light. Estes achados não são decisões
novas de negócio nem autorização para alterar cores, CSS ou validações.

| ID | Objeto | Evidência / consequência | Tratamento nesta sprint |
|---|---|---|---|
| A01 | styles | Módulo importa colors, mas notebook dizia que não havia import. Componentes visuais não consomem styles. | Corrigida a prosa e delimitada a centralização efetiva no README. Nenhum CSS alterado. |
| A02 | styles / badge | Texto #B26A00 sobre #FFF8E1: contraste 3,9894588488:1, fonte 11px, abaixo de 4,5:1 para texto comum. | Teste de caracterização e aviso; não atribuir conformidade. Alteração visual depende de tarefa própria. |
| A03 | badge | 79.6 arredonda para “80/100”, mas continua warn; 49.6 aparece “50/100” em fail. | Diferença entre corte e apresentação explicada, com teste de fronteira. |
| A04 | badge | Máximo zero e valores fora da faixa não são recusados; tipo desconhecido cai em info. | Entradas a conferir pelo chamador; testes descrevem tolerância, não recomendam o uso. |
| A05 | kpi_card | Markdown escapa somente pipe; chaves 1 e "1" colidem após conversão para string. | Recomendadas chaves textuais únicas e conteúdo controlado; não promover saída a sanitização geral. |
| A06 | kpi_card | Não calcula nem formata números; HTML não se limita ao notebook e Markdown não é renderizado por todo destino. | Corrigida prosa do exemplo, preservando saída histórica e funções. |
| A07 | colors | Paletas são listas; repetição, agrupamento e centro da escala dependem do consumidor. | Retiradas garantias de automação da prosa; exemplos de cópia local e avisos de contraste. |
| A08 | emojis | Dicionários não executam EDA nem impõem ordem. Trio ok/falha/atenção não é binário. | Corrigidas as afirmações e o contraexemplo que mencionava etapa inexistente. |
| A09 | fixtures | Sorteios com probabilidades não são quotas. Versão futura tem probabilidade por decisão, não proporção de todas as features. | Contrato e denominadores explicados; conferência real de Spark fica discriminada das leituras estáticas. |
| A10 | fixtures | n_entidades=0 cai no default n; fatos_e_features aceita zero decisões; strings de safra não são validadas como datas. | Testes de caracterização específicos, sem mudar API nem código gerador. |
| A11 | fixtures | Geração monta lista local antes de Spark; atraso_real_dias desloca data, não cria coluna de publicação; inadimplência é acumulada. | Limites de volume, de causalidade e de simulação esclarecidos. |
| A12 | divider | Traços não substituem títulos; afirmações de percepção não eram teste com leitores. | Descrição funcional e recomendação proporcional, sem pretender validação perceptual. |

A02 usa o cálculo de luminância sRGB da referência primária
[WCAG — contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
Os demais comportamentos são rastreáveis aos módulos da base e ao
[script de testes](evidencias_r03a/verificar_r03a.py). Passar em um teste de
caracterização não sana a limitação reproduzida. Não há benchmark, treino,
dados reais de clientes ou publicação nesta rodada.
