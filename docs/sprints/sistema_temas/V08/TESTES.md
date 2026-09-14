# V08 — testes e evidências

## Estado inicial

A V08 foi aberta a partir da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`. Nenhuma mudança runtime é permitida nesta sprint.

A suíte específica é `tools/tests/test_temas_v08.py`. Ela cobre:

- completude da matriz transversal;
- equivalência byte a byte entre superfícies `.assistant` alteradas e `Novo_Ambiente_Simulado`;
- equivalência entre as três cópias do Manual Técnico;
- remoção de rótulos vivos obsoletos V04/V05;
- template EDA sem `TEMA_EDA`, `PALETA_EDA`, hexadecimais de política ou registro global legado recomendado;
- presença de `ResolvedTheme`, `load_reference_theme` e `aplicar_tema_resolvido` no fluxo de EDA;
- roteamento de Concierge/criação de objeto ao padrão central;
- skills de baseline, safra e monitoramento distinguindo aparência de cálculo/política;
- explicabilidade registrando SHAP/Matplotlib como limite de theming;
- workflow V08 permanente read-only.

O workflow também executa:

```bash
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Além disso, compara `HEAD` com o SHA-base V08 e reprova se houver qualquer alteração Python em `ambiente_fonte/.assistant/hub_snippets/**` ou `hub_scripts/**`.

## Evidência ainda em formação

Este arquivo foi criado antes da primeira candidata completa. Runs, failures e correções serão acrescentados com sua conclusão real. Nenhum failure será reclassificado retroativamente.

## O que PASS não prova

- seleção determinística de uma skill pela Genie Code;
- publicação/instalação no workspace;
- render real no browser Databricks;
- acessibilidade ou UAT humano;
- permissão/ACL real de pastas;
- que SHAP/Matplotlib ou Kaplan–Meier estejam tematizados;
- que documentação impeça tecnicamente um agente de ignorar orientação.
