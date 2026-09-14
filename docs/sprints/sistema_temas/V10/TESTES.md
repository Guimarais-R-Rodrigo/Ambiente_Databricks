# V10 — testes e evidências

## Estado

Candidata em execução. Este arquivo registra somente evidências observadas; não transforma teste local em homologação Databricks.

## Suíte específica

`tools/tests/test_temas_v10.py` cobre:

- identidade encaminhada e namespace SHA-256;
- recusa de identidade ausente;
- fallback local explicitamente opt-in;
- recusa de storage produtivo fora de `/Volumes/`;
- recusa de modo diferente de `authoring_only`;
- persistência roundtrip reutilizando sessão V05;
- isolamento entre duas identidades;
- não sobrescrita de sessão;
- recusa de sessão adulterada;
- política sem delete automático/usuário e sem reescrita de histórico;
- política sem aprovação/publicação/promoção;
- papéis V10 idênticos aos canônicos da V01;
- equivalência source/simulado da superfície do App;
- `app.yaml` usando `valueFrom: theme_storage` sem segredo/caminho hardcoded;
- ausência de chamadas Databricks SDK/publicação no shell;
- geração e verificação do bundle derivado.

## Workflow permanente

`.github/workflows/temas-v10-ci.yml` é read-only (`contents: read`) e executa:

```bash
python -B tools/tests/test_temas_v10.py -v
python -m py_compile ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app.py ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app_service.py
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/temas_v10_app.py --output .artifacts/v10-app
python -B tools/temas_v10_app.py --verify .artifacts/v10-app
python -B tools/validate_assistant.py --conferir-readme
```

O workflow não recebe credencial Databricks, não usa Databricks CLI e não faz deploy.

## Camadas de evidência

- **Python local/CI:** identidade sintética controlada, paths temporários, persistência e mutantes.
- **Bundle local:** integridade do artefato implantável derivado.
- **Documentação:** correspondência entre UI, código, papéis e procedimento.
- **Workspace futuro:** headers reais, App permissions, UC Volume, renderização, concorrência e UAT. Esses itens permanecem não testados até execução autorizada.

## Resultados

Os resultados serão preenchidos a partir dos runs reais desta branch/PR. Nenhuma contagem é presumida pela existência dos métodos.

## Failures

Qualquer run reprovado durante V10 deve permanecer identificado como FAILURE com causa e correção. Não reclassificar run antigo ou novo por uma execução posterior verde.

## O que PASS não prova

PASS no GitHub Actions não prova deploy, autenticação real do workspace, privilégios corporativos, persistência efetiva em UC Volume, isolamento hostil multiusuário, browser, acessibilidade, desempenho percebido, custo observado ou publicação de tema.
