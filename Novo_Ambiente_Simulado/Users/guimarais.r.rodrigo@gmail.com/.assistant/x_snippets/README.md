# `x_snippets` — biblioteca Python customizada

> **EXTENSÃO CUSTOMIZADA (`x_`) — não auto-descoberta nem instalada pela Genie Code.**

Esta pasta preserva helpers reutilizáveis de notebook. Ela não é uma Agent Skill e
nenhum módulo é carregado automaticamente. Importe somente o que o notebook usa.

Para localizar o módulo a partir da demanda ("preciso calcular PSI", "preciso de
split temporal"), consulte o [catálogo de helpers](../x_docs/catalogo_helpers.md),
que cobre `x_snippets` e `x_scripts` e marca as dependências opcionais.

## Uso no Databricks

Se `.assistant` estiver no diretório do projeto/repositório:

```python
from pathlib import Path
import sys

project_root = Path.cwd()  # ajuste se o notebook estiver em uma subpasta
assistant_root = project_root / ".assistant"
if not assistant_root.is_dir():
    raise FileNotFoundError("Defina assistant_root para a pasta .assistant deste projeto")
sys.path.insert(0, str(assistant_root))

from x_snippets.visual.theme_plotly import aplicar_tema
from x_snippets.spark.null_summary import null_summary
from x_snippets.spark.safe_display import safe_display
```

Para uma instalação no diretório do usuário, use o caminho parametrizado
`/Workspace/Users/<username>/.assistant`; nunca copie um e-mail pessoal de um
exemplo. Em serverless, confirme as regras atuais para dependências e reinicie o
Python quando a instalação do notebook exigir.

## Onde procurar um módulo

O mapa completo — 54 módulos organizados por demanda, com função pública e
dependências marcadas — está em
[x_docs/catalogo_helpers.md](../x_docs/catalogo_helpers.md). É a única lista
mantida; procure lá em vez de navegar pelas pastas.

A divisão por pacote serve apenas para situar:

| Pacote | Finalidade | Cuidados |
|---|---|---|
| `constants` | cores, estilos, emojis e formatação BR | a paleta é customizada, não Databricks |
| `visual` | tema Plotly, cabeçalhos, badges, KPIs e índice | o HTML gerado escapa o texto recebido |
| `spark` | nulos, amostragem, display, datas e PSI | ações Spark têm custo; declare amostra e referência |
| `display` | correlação, distribuições e tabela estilizada | conversão ao driver é sempre limitada |
| `ml` | baselines, validação, drift, SHAP, séries, survival e monitoramento | dependências opcionais; valide versão e runtime |

Use `requirements-optional.txt` como inventário, não como lockfile universal. Instale
somente o subconjunto necessário e registre versões no projeto consumidor.

## Quando o import falha

| Mensagem | Causa | Correção |
|---|---|---|
| `ModuleNotFoundError: No module named 'x_snippets'` | foi adicionada ao `sys.path` a pasta `x_snippets` | adicione a `.assistant`, que a contém |
| `ModuleNotFoundError: No module named 'lightgbm'` (ou `xgboost`, `catboost`, `optuna`, `torch`) | dependência opcional exigida já no import | instale com versão fixada, ou use outro módulo do catálogo |
| Import passa e o erro só aparece ao chamar a função | dependência opcional resolvida na chamada — caso de SHAP, lifelines, Prophet, UMAP, TabNet e ARIMA | mesma correção; o catálogo marca esses casos |
| `NOT_SUPPORTED_WITH_SERVERLESS: PERSIST TABLE` | código novo chamando `cache()` em compute serverless | remova o cache; os helpers já operam sem ele |
| `NameError: name 'spark' is not defined` | código novo contando com a variável global de notebook dentro de um módulo | resolva a sessão com `SparkSession.getActiveSession()` |

As três últimas linhas vieram de falhas reais encontradas ao executar a
biblioteca no runtime, não de suposição.

## Contrato de segurança

- Não use `toPandas()` sem limite verificável.
- Em dados temporais, ajuste preprocessamento apenas no treino e respeite o instante
  de decisão.
- Em dados por entidade, informe a chave para lags/janelas.
- Defina explicitamente classe positiva e direção do score.
- PSI e thresholds de alerta são heurísticas calibráveis.
- Não silencie exceções com sentinelas como `-1`; retorne diagnóstico ou falhe.

## Verificação rápida

```python
from x_snippets.constants.format_br import fmt_brl, fmt_pct

assert fmt_brl(1.999) == "R$ 2,00"
assert fmt_pct(1.0) == "100,0%"              # escala ratio
assert fmt_pct(1.0, input_scale="percent") == "1,0%"
```

Após alterar os módulos, execute os testes locais e a compilação sintática. O fato de
um arquivo importar não comprova compatibilidade com o runtime Spark do workspace.
