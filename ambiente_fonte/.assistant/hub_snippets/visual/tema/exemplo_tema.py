"""Exemplo sem efeito visual do núcleo de temas.

Defina CAMINHO_TEMA apenas quando possuir um JSON completo do contrato 0.1.0.
Este notebook/script não publica nem aplica o tema em gráficos.
"""
from hub_snippets.visual.tema import ErroTema, resolver_tema

CAMINHO_TEMA = None  # mantenha None para preservar o comportamento legado

try:
    tema = resolver_tema(CAMINHO_TEMA)
    if tema is None:
        print("Tema não selecionado: comportamento legado preservado.")
    else:
        print(f"Tema validado: {tema.theme_id} v{tema.theme_version} ({tema.context})")
        print(f"SHA-256 dos bytes carregados: {tema.sha256}")
except ErroTema as exc:
    print(f"Tema recusado [{exc.codigo}]. {exc.orientacao}")
    raise
