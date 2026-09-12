# V03 — plano de testes

## Suíte específica

`python -B tools/tests/test_temas_v03.py`

A suíte cobre compatibilidade das três APIs legadas, equivalência da fixture legada, mapeamento dos tokens configuráveis, preservação de dados/eixos/cores explícitas, rodapé configurado, ausência de efeito global na aplicação por figura, contexto incorreto, modos ainda não suportados, tipo incorreto, fingerprint adulterado, namespace de template, colisão, substituição e ativação explícitas.

## Regressões obrigatórias

- `python -B tools/tests/test_visual_legado_v00.py`
- `python -B -m unittest discover -s tools/tests -p 'test_temas_v01*.py' -v`
- `python -B tools/tests/test_temas_v02.py`
- `python -B tools/ci_local.py --verbose`
- `python -B tools/validate_assistant.py --conferir-readme`

SKIP nunca é convertido em PASS. Testes locais/CI não homologam Databricks, Spark ou renderização visual humana.

## Testes adversariais

A guarda precisa rejeitar: dicionário cru em vez de `ResolvedTheme`; contexto `readme`; modo `dark`/`high_contrast` antes da implementação de superfícies; fingerprint inconsistente; nome fora de `hub-*`; colisão sem `substituir=True`; opções não booleanas.

## Evidência de não regressão

O caso mais importante é a equivalência exata: `get_tema_plotly(load_reference_theme('notebook')) == get_tema_eda()`. Ela prova que a tradução dos tokens da referência legada produz a configuração historicamente observada sem exigir que o legado passe a depender dessa fixture.
