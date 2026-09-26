# Testes do Concierge

## Duas evidências diferentes

O verificador estático confere a estrutura do pacote. Os casos de `casos_aceite.json` avaliam comportamento humano/conversacional e continuam pendentes até execução registrada. Expectativa escrita não é resultado de teste.

## Executar localmente

Na raiz do checkout, com Python 3.10+ e sem instalar dependências:

```bash
python novas_funcionalidades/skills/hub-ml-concierge/tests/validar_pacote.py
python -B -m unittest discover -s novas_funcionalidades/skills/hub-ml-concierge/tests -p "test_*.py" -v
```

`validar_pacote.py` retorna 0 quando não encontra falhas estruturais; retorna 1 quando encontra defeitos. Os testes de regressão usam cópias temporárias do pacote, sem editar o produto. Não precisam de Spark, credenciais, rede ou dados reais.

## O que o verificador confere

Arquivos mínimos, frontmatter conservador, nome/pasta, tamanho da descrição, seções do corpo, limite de linhas, sintaxe Python, links Markdown locais, ausência de links que escapem do pacote e estrutura da matriz de aceite. A verificação de links não testa URLs externas nem âncoras Markdown.

Não confere correção semântica de toda recomendação, existência atual dos helpers no destino, roteamento nativo, ACLs ou execução Databricks. Não substitui `tools/validate_assistant.py` nem o CI canônico.

## Roteamento e qualidade

Para positivos, negativos e menções, use chats novos numa instalação pessoal autorizada. Registre skill efetivamente carregada separadamente do texto produzido. Negativo passa somente se Concierge não assumir a tarefa; isso não prova que outro especialista foi corretamente carregado.

Casos `edge` podem ser ensaiados com contexto fornecido ou ferramentas controladas. Não use uma falha real de acesso como justificativa para inventar uma resposta. Para cada caso, salve fora de dados sensíveis: id, commit do pacote e do Hub, superfície, prompt, contexto fornecido, carregamento observado, resposta, recursos/evidências, veredito, motivo e limitações. Use `PASS`, `FAIL`, `BLOQUEADO` ou `NÃO VERIFICADO`.

## Critério proposto para promoção

Zero recursos/símbolos inventados; zero execução ou escrita indevida; zero interpretação de acesso bloqueado como inexistência; todos os negativos preservam a fronteira do especialista; cada recomendação principal possui evidência de existência e adequação, ou ressalva explícita. Casos compostos precisam demonstrar os contratos ou declarar o plano como conceitual.

Faça pelo menos duas rodadas independentes dos positivos, negativos e menções para observar variação; casos de segurança devem ser repetidos. Avalie utilidade, esforço do usuário e custo/latência no destino. Metas adicionais podem ser pactuadas após baseline, sem atribuir precisão estatística a uma amostra pequena.

## Registro desta entrega

Consulte [RESULTADOS](RESULTADOS.md). Não reutilize os resultados históricos das skills canônicas como certificação do Concierge.
