# Testes e reprodução da V02

## Ambiente e comandos

Use uma cópia limpa do repositório com o histórico completo; o gate dos READMEs
consulta commits históricos. Snapshot sem histórico serve para testes do núcleo,
mas não equivale à validação integral. Prepare as dependências em ambiente de
manutenção autorizado; nenhuma instalação é feita pelo núcleo:

```text
python -m pip install -r tools/requirements-dev.txt -r tools/requirements-temas-dev.txt
python -B tools/tests/test_temas_v02.py
python -B tools/temas_v02_check.py
python -B -m unittest discover -s tools/tests -p 'test_temas_v01*.py' -v
python -B tools/tests/test_inventario_visual.py
python -B tools/tests/test_visual_legado_v00.py
python -B tools/tests/test_baseline_visual_runner.py
python -B -m unittest discover -s tools/readme_visuals/tests -p 'test_*.py' -v
python -B tools/ci_local.py --verbose
```

O exemplo pode ser executado localmente como arquivo Python. O marcador de
notebook e os comentários Markdown permanecem preservados:

```text
python -B ambiente_fonte/.assistant/hub_snippets/visual/tema/exemplo_tema.py
```

Depois de validar a fonte, o mantenedor sincroniza o Manual raiz e executa
`python -B tools/render_simulado.py --write`. Não edite o espelho manualmente.
Os comandos de teste não publicam; não substitua por um publicador real.

## Cobertura e critérios

| Família do plano | Evidência exercitada |
|---|---|
| CON — contrato | Schema único, quatro fixtures, campos/tipos/limites, padrões de cor, versões e recusas herdadas da V01. |
| RES — resolução | Três contextos, cópias isoladas, origem por token, fingerprints estáveis e sensíveis à mudança, exportar/reimportar, nenhuma herança/default injetado. |
| SEC-02 a SEC-07 | Entradas ambíguas, duplicatas, não finitos, ciclos, limites, paths, symlinks/FIFO, integridade de pacote/assets/resultado e mensagens sem conteúdo arbitrário. |
| DOC-04 | Fachada exaustiva, referências de origem, links operacionais, molde de quinze seções, referência gerada, exemplo executável e três cópias do Manual. |
| OPS-01 | Import com `python -S`, ausência de dependência na chamada, zero sockets, ausência de cache e escrita na exportação. |
| Legado | V00, V01, publicador e gate vigente; módulos analíticos, gráficos e assets anteriores preservados. |

Os nomes de cada teste e as asserções estão nos arquivos citados nos comandos.
Cada erro é comparado pelo código esperado, não por “alguma exceção”. Os testes
positivos e mutantes cobrem os mesmos contratos; a descoberta vazia é recusada
pelo verificador V02. Repetições de uma suíte não são casos adicionais.

## Limites da evidência

Não há prova de usabilidade por pessoa iniciante, acessibilidade, desempenho em
produção, Windows/Databricks, autenticação/ACL, revisão independente nem publicação.
O teste de import sem pacotes externos prova apenas o import; validar demanda as
duas bibliotecas declaradas. O teste com socket bloqueado é local, não uma
certificação de isolamento de rede do workspace. Diretórios pais precisam de
permissões controladas; o núcleo não é sandbox contra escritor hostil concorrente.

[Voltar à V02](README.md)
