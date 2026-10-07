# Duas ampliações de API em caminhos já existentes

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt10-current-api-additions-map"></a>
<a id="mt10-current-api-additions-map"></a>
### Duas ampliações de API em caminhos já existentes

Uma reconciliação por nomes de arquivos não encontra todas as mudanças de contrato. A fachada de MLflow continua na mesma pasta, mas agora expõe uma segunda operação. O helper de SHAP conserva seu nome e acrescenta uma referência opcional. Estas ampliações precisam de explicação própria mesmo sem criar novos caminhos no inventário. O mapa registra o que o chamador pode fornecer, o que recebe e quais efeitos precisam ser autorizados. As interfaces anteriores continuam descritas no [mapa de métricas e scripts](MT-mt10-mt11-code-map.md#mt-mod-mt10-mt11-code-map).

<a id="mt-mod-mt10-current-api-additions-map-h-registrar-uma-execução-sintética-baseada-em-regras"></a>
#### Registrar uma execução sintética baseada em regras

`run_micromodelo` é um gerenciador de contexto: a preparação efetiva acontece quando se entra no bloco de uso. Ele oferece um coletor com `parametros`, `agregados_medidos` e `pendencias`. Esse coletor não oferece os métodos de modelo ou artefato do contexto legado `run_governado`. A distinção impede transportar para uma execução baseada em regras a obrigação de registrar um modelo treinado que não existe. Também impede usar a nova superfície para enviar predições individuais ou arquivos ao tracking por um método que ela não implementa.

O prefixo `synthetic:` é uma declaração do chamador. O helper não abre a fonte para demonstrar que todos os dados são sintéticos. Da mesma forma, conferir que um fingerprint tem 64 caracteres hexadecimais não recalcula a identidade de uma especificação. O chamador precisa obter essa identidade pela rota de assinatura apropriada e fornecer somente informações autorizadas. A validação limita a forma da entrada e algumas relações internas; não autentica a origem nem transforma um texto de limitação em aprovação humana.

Imagine um exemplo ilustrativo com população dez e contagens seis, três e um nas três classes. Essa soma é coerente. Se a classe indeterminada passar a duas sem alterar as demais, o total onze viola o contrato e precisa ser recusado. Se houver score declarado, mínimo vinte, média cinquenta e cinco e máximo noventa podem ser uma combinação estruturalmente válida, desde que a quantidade de scores e a habilitação também sejam coerentes. Esses números ensinam a conferência; não são métricas executadas por esta edição nem evidência sobre um micromodelo real.

Se MLflow estiver ausente, entrar no contexto gera ImportError. As verificações explícitas usam ValueError; erros de tipos não iteráveis, dependências ou backend também podem propagar. O contexto pode selecionar um experimento, abrir um run e registrar tags, parâmetros e métricas agregadas. Portanto, usá-lo exige decidir o backend e a autorização antes da chamada. Fechar normalmente sem parâmetros ou sem agregados gera erro, mas registros anteriores podem já ter sido persistidos. Não há rollback dos logs. Uma falha durante um registro também pede inspeção do estado antes de repetir. Após o encerramento, os métodos de mutação recusam novas chamadas; a consulta de pendências não deve ser confundida com reabertura do run.

<a id="mt-mod-mt10-current-api-additions-map-h-assinatura-e-entrada-do-contexto"></a>
##### Assinatura e entrada do contexto

`run_micromodelo(nome, *, tipo, spec_fingerprint, dataset, split, limitacoes, contrato_saida, experimento=None)` cede o coletor durante o contexto.

| Caminho ou argumento | Tipo e regra implementada | Significado e limite |
|---|---|---|
| `nome` | String não vazia, sem controles ASCII (U+0000–U+001F e U+007F), até 128 caracteres | Nome do run; validação remove espaços externos do valor usado |
| `tipo` | String exata `DEVELOPMENT`, `VALIDATION` ou `SCORING` | Classe declarada da execução; não promove fase do YAML |
| `spec_fingerprint` | String de 64 caracteres `[0-9a-f]` | Identidade fornecida; a chamada não verifica o YAML correspondente |
| `dataset`, `split` | Strings não vazias, sem controles ASCII (U+0000–U+001F e U+007F), até 500 caracteres, começando por `synthetic:` após limpeza | Referências declaradas do recorte e divisão; não são detector de dados reais |
| `limitacoes[]` | Iterável com 1–20 strings não vazias de até 500 caracteres, sem controles ASCII (U+0000–U+001F e U+007F); `str` e `bytes` isolados são recusados | Limitações explícitas; difere do comportamento legado que pode iterar uma string por caracteres |
| `contrato_saida` | `dict` com exatamente as cinco chaves abaixo | Contrato fechado serializado na tag do run |
| `contrato_saida.grain` | String não vazia, sem controles ASCII (U+0000–U+001F e U+007F), até 500 caracteres | Unidade declarada de cada resultado; não mede o grão dos dados. A validação confere o texto, mas a serialização conserva seu valor original |
| `contrato_saida.classification_field` | Identificador ASCII `[A-Za-z_][A-Za-z0-9_]{0,63}` | Nome declarado do campo de classificação |
| `contrato_saida.classification_values[]` | Lista ou tupla de três strings, conjunto exato `TRUE`, `FALSE`, `INDETERMINADO` | Classes aceitas; a ordem fornecida é conservada na serialização |
| `contrato_saida.score_field` | Mesmo formato de identificador, ou `None` | `None` declara ausência de campo de score |
| `contrato_saida.score_semantics` | `None` sem score; `FORCA_EVIDENCIA` quando há campo | Esta superfície não aceita declarar probabilidade calibrada |
| `experimento` | `None`, ou string não vazia sem controles ASCII (U+0000–U+001F e U+007F), até 500 caracteres | Se informado, chama `mlflow.set_experiment`; pode alterar o destino do tracking |
| Tags iniciais | `mm06.run_type`, `mm06.spec_fingerprint`, `mm06.dataset`, `mm06.split`, `mm06.limitacoes`, `mm06.output_contract`, `mm06.complete` | Contrato como JSON; limitações unidas por separador; completude começa em `false` |

<a id="mt-mod-mt10-current-api-additions-map-h-campos-aceitos-pelo-coletor"></a>
##### Campos aceitos pelo coletor

`parametros(valores)` exige um dicionário não vazio com um subconjunto das sete chaves permitidas. Nem todas são obrigatórias: o registro de uma chave aceita já satisfaz a presença de parâmetros no fechamento. A revisão de negócio continua responsável por verificar se a configuração descrita é suficiente.

| Caminho | Tipo, condição e valores | Consumo |
|---|---|---|
| `parametros.regra`, `parametros.versao_regra` | Strings `[A-Za-z][A-Za-z0-9_.-]{0,99}` | Rótulos registrados por `mlflow.log_params` |
| `parametros.limiar` | `int` ou `float` finito entre 0 e 100; booleano recusado | Valor declarado; o coletor não aplica o limiar aos registros |
| `parametros.janela_dias` | Inteiro não booleano de 1 a 3.650 | Janela declarada; não executa filtro temporal |
| `parametros.normalizacao` | `PENDENTE`, `SOMA_PONDERADA_0_100`, `MIN_MAX_0_100`, `LINEAR_0_100` ou `CUSTOM_APROVADO` | Nome do método; o coletor não calcula nem aprova a normalização |
| `parametros.politica_indeterminado` | Valor exato `INDETERMINADO` | Registra tratamento; não recodifica resultados |
| `parametros.score_habilitado` | Booleano | `True` exige campo no contrato; `False` é incompatível com estatísticas de score já registradas |
| `agregados.population` | Inteiro não booleano entre 0 e `2**53`, obrigatório | Denominador declarado |
| `agregados.count_true`, `agregados.count_false`, `agregados.count_indeterminate` | Inteiros no mesmo intervalo, obrigatórios; soma igual a `population` | Contagens de classes; registradas como métricas numéricas |
| `agregados.score_count` | Opcional, omita em vez de enviar `None`; inteiro de 0 a `population` | Exige campo de score; sem estatísticas, só pode ser ausente ou zero |
| `agregados.score_min`, `agregados.score_mean`, `agregados.score_max` | Todos presentes ou todos ausentes; valores finitos, não booleanos, com `0 <= min <= mean <= max <= 100` | Exigem população positiva, campo de score, score não desabilitado e `score_count > 0` |
| `agregados_medidos(..., referencia_execucao=...)` | Referência obrigatória, string não vazia sem controles ASCII (U+0000–U+001F e U+007F), até 200 caracteres | Registrada em `mm06.measurement_ref`; não reverifica a medição externamente |

`agregados_medidos(valores, *, referencia_execucao)` pode concluir um registro de agregados apenas uma vez por coletor. Os métodos de registro retornam None; `pendencias()` retorna uma lista de nomes pendentes. A chamada registra primeiro as métricas e depois a referência: se a segunda etapa falhar, a primeira pode ter persistido, sem que o coletor marque os agregados como completos. `pendencias()` informa a falta de `parametros` ou `agregados_medidos`; o contexto não possui argumento para relaxar esse fechamento. A tag `mm06.complete` só muda para `true` após a conferência final. Nenhuma dessas marcas substitui aprovação, publicação ou registro de modelo no Registry.

<a id="mt-mod-mt10-current-api-additions-map-h-escolher-uma-referência-explícita-para-shap-linear"></a>
#### Escolher uma referência explícita para SHAP linear

`background` define a referência comparativa entregue ao explicador linear. Não é a matriz das observações que você quer explicar: essa continua sendo `X`. Se o argumento ficar como `None`, a implementação mantém o comportamento anterior e usa `X` também como referência. Se você fornecer outra matriz, precisa justificar por que ela representa a comparação pertinente ao estudo. Uma referência válida para a biblioteca não comprova representatividade, ausência de vazamento ou estabilidade da explicação.

A validação exige duas dimensões, ao menos uma linha, a mesma quantidade de colunas de `X` e valores convertíveis em números finitos. Essa conversão serve à conferência; o objeto original é encaminhado ao SHAP. A correspondência semântica entre as colunas continua sendo obrigação do chamador. O helper genérico não exige uma única linha: essa restrição pertence ao perfil B1 `LINEAR_REGRESSION_SYNTHETIC_V1`. Confundir o perfil restrito com a API geral recusaria usos que o helper admite ou atribuiria ao perfil uma flexibilidade que ele não oferece.

| Ponto da API | Regra e comportamento atual |
|---|---|
| Assinatura ampliada | `compute_shap(model, X, feature_names, model_type="tree", max_samples=5000, *, task="classification", output_index=None, background=None)` |
| `background` explícito | Aceito somente em `model_type="linear"`; outros modos geram `ValueError` |
| Forma | `background` e `X` precisam ser bidimensionais nesta validação; referência não vazia e mesma quantidade de colunas |
| Valores | A referência deve permitir conversão temporária a `float` finito; entrada inválida gera erro |
| `background=None` | `shap.LinearExplainer(model, X)` |
| Referência explícita | `shap.LinearExplainer(model, background)` após as conferências |
| Resultado | Preserva a tupla matriz de contribuições e valor-base; regras de múltiplas saídas e alinhamento permanecem |
| Falhas e precedência | O import de SHAP ocorre antes da validação: biblioteca ausente pode falhar primeiro. Background inválido gera ValueError, mas erros do modelo/biblioteca também propagam |
| Outros efeitos | SHAP é importado na chamada; cálculo e prints continuam. Kernel mantém sua própria subamostra/referência, e plots só persistem quando chamados com destino |

<!-- editorial:exclude:start -->
Fontes: [fachada MLflow](../../hub_snippets/ml/mlflow_run/__init__.py), [implementação MLflow](../../hub_snippets/ml/mlflow_run/mlflow_run.py) e [SHAP](../../hub_snippets/ml/shap_explainer/shap_explainer.py). Aprofundamento: [MT10](MT-parte-ii.md#mt10-3), [MM02 e assinatura](MT-parte-v.md#mt22-2) e [perfis B1](MT-mt14-b1-code-map.md#mt-mod-mt14-b1-code-map).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
