# `x_snippets` — biblioteca Python customizada

> **EXTENSÃO CUSTOMIZADA (`x_`) — não auto-descoberta nem instalada pela Genie Code.**

Esta pasta preserva helpers reutilizáveis de notebook. Ela não é uma Agent Skill e
nenhum módulo é carregado automaticamente. Importe somente o que o notebook usa.

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

## Catálogo

| Pacote | Finalidade | Cuidados |
|---|---|---|
| `constants` | cores, estilos, emojis e formatação BR | a paleta é institucional/customizada, não Databricks |
| `visual` | tema Plotly, cabeçalhos, badges, KPIs e índice | HTML gerado escapa texto fornecido pelo usuário |
| `spark` | nulos, amostragem, display, datas e PSI | ações Spark têm custo; declare amostra e referência |
| `display` | correlação, distribuições e tabela estilizada | conversão ao driver sempre é limitada |
| `ml` | baselines, validação, drift, SHAP, séries, survival e monitoramento | dependências são opcionais; valide versão/runtime |

Use `requirements-optional.txt` como inventário, não como lockfile universal. Instale
somente o subconjunto necessário e registre versões no projeto consumidor.

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
