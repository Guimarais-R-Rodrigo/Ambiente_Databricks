# Regressões do publicador visual

[test_publish_production.py](test_publish_production.py) verifica guardas do
publicador de escopo fechado com fixtures e mocks. Não publica durante esta suíte.

Da raiz, com as dependências já disponíveis:

```sh
python -B -m unittest discover -s tools/readme_visuals/tests -p 'test_*.py'
```

O owner de execução real é [publish_production.py](../publish_production.py),
com pré-condições no [guia visual](../README.md). Os demais testes de geração,
temas, congelamento e baseline ficam em [tools/tests](../../tests/README.md).
Aprovar mocks não comprova permissões, backup real ou equivalência de um workspace.
