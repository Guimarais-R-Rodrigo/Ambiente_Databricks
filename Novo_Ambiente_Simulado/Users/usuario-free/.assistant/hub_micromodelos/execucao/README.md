# Execução de Micromodelos

Biblioteca de contrato, descoberta por metadados e ensaios sintéticos para um micromodelo de domínio.

<!-- readme-objeto: 1.0.0 -->

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Funções Python reutilizáveis do módulo `hub_micromodelos.execucao`. |
| Para que serve? | Validar especificação, calcular assinatura, descobrir metadados, preparar estudo e exemplos. |
| Quando usar? | Depois de definir escopo e permissões; para aprender, use a fixture sintética. |
| Quando evitar? | Quando a origem e a autoridade dos dados ou da decisão ainda não foram definidas. |
| Exige? | Python, `jsonschema`, `regex` e `PyYAML`; Databricks e MLflow só em rotas específicas. |
| Entrega? | Objetos de contrato, descoberta, artefatos e resultados sintéticos explícitos. |

## 1. O que é?

É o código do framework dentro do Hub. A [especificação](especificacao.py) valida o YAML; [assinatura](assinatura.py) identifica a parte material do contrato; os demais módulos implementam as etapas delimitadas abaixo.

## 2. Que problema este recurso resolve?

Permite verificar se um candidato descreve o mesmo micromodelo ao longo do estudo e se suas operações seguem a semântica declarada, sem perder a distinção entre proposta, medição, aceite e publicação.

## 3. Quando faz sentido usar?

No rascunho, valide o contrato e calcule sua assinatura. Na descoberta, use o coletor de metadados. No laboratório, rode a fixture sintética antes de avaliar adaptação a fontes autorizadas.

## 4. Quando não usar?

Não use o ensaio sintético como predição corporativa. Por exemplo, o score didático de recência classifica sete pessoas fictícias; ele não estima desempenho em clientes reais.

## 5. Como funciona, intuitivamente?

O YAML passa pelo schema e pelos invariantes de domínio. A assinatura fixa os campos materiais. O fluxo compõe uma proposta com fontes e regras. O laboratório aplica regras fechadas a fixtures locais e produz contagens reconciliadas.

## 6. Exemplo de situação

Um analista quer entender por que `pessoa_c` não é `FALSE` quando só existe um contato antigo. O [caso de recência](../exemplos/recencia_contato/README.md) mostra a especificação, os eventos sintéticos e o motivo `SOMENTE_CONTATO_ANTIGO`.

## 7. O que você precisa antes de usar?

Para o exemplo local, bastam Python e as dependências da visão rápida. Para Databricks, forneça uma sessão e um catálogo explicitamente autorizados ao [adaptador](databricks.py). Defina entidade, chave lógica, instante e janela antes de analisar registros.

## 8. O que este recurso entrega?

O contrato devolve problemas estruturados; a assinatura devolve SHA-256 do material versionado; o coletor devolve um envelope de metadados; o laboratório devolve especificação, resultado e resumo. O score sintético é força de evidência na escala 0–100, sem interpretação probabilística.

## 9. Como usar este recurso no Hub?

Com a raiz `.assistant` no caminho Python, importe `hub_micromodelos.execucao.especificacao` e `hub_micromodelos.execucao.fluxo`. A entrada [exemplo_execucao.py](exemplo_execucao.py) executa o piloto de recorrência via `python -m hub_micromodelos.execucao.exemplo_execucao`; a demonstração de recência é [executar_exemplo.py](../exemplos/recencia_contato/executar_exemplo.py). Nenhuma delas publica ou grava tabelas.

## 10. Decisões e configurações que mais importam

`fluxo.SCHEMA` e `fluxo.TEMPLATE` apontam para `../contratos/`. `metadados.Limits` restringe páginas e bytes da coleta. O caso de recência fixa limiar inclusivo de sete dias e pesos 0,7/0,3 no YAML; mudar esses valores altera o cálculo e a assinatura.

## 11. Limitações, riscos e armadilhas

Os módulos de execução não certificam o comportamento do Genie. O laboratório `execucao.py` contém uma heurística fechada para sua fixture; a função recusa uma assinatura de perfil diferente. O adaptador Databricks exige sessão injetada e não amplia permissões de acesso.

## 12. Quais são as alternativas?

Para descrever um caso sem executar dados, use a [skill](../../skills/hub-ml-micromodelos/SKILL.md) e os prompts do Hub. Para acompanhar runs de MLflow, use o recurso compartilhado em [mlflow_run](../../hub_snippets/ml/mlflow_run/README.md), que mantém sua própria API.

## 13. Como saber se o resultado faz sentido?

Confira schema e invariantes, compare a assinatura antes e depois de mudanças materiais, conte novamente as três classes e execute o oráculo do [exemplo de recência](../exemplos/recencia_contato/README.md). Uma conferência local não substitui decisão humana sobre finalidade e fontes.

## 14. Arquivos relacionados e próximos passos

`__init__.py` identifica o pacote; [exemplo_execucao.py](exemplo_execucao.py) demonstra o piloto sintético. `especificacao.py`, `assinatura.py`, `metadados.py`, `fluxo.py`, `artefatos.py`, `databricks.py`, `entrega.py`, `catalogo.py` e `execucao.py` preservam as responsabilidades atuais. Veja a [visão geral](../README.md) e o [contrato](../contratos/micromodelo.schema.json).

## 15. Referências

O comportamento descrito é o dos módulos desta pasta e do [schema](../contratos/micromodelo.schema.json). As decisões de domínio estão no Manual Técnico do Hub e na documentação arquitetural da frente de Micromodelos.
