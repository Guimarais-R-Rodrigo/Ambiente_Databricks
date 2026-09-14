# V07 — testes e evidências

## Escopo automatizado

A suíte específica é `tools/tests/test_temas_v07.py`. Ela deve provar, sem Databricks remoto:

- o registro estruturado cobre todos os nove consumidores runtime de `display`/`ml` identificados para esta sprint;
- controles declarados pela V07 possuem ao menos um consumidor suportado;
- `get_tokens_plotly` revalida `ResolvedTheme`, devolve cópia e falha fechado para entrada crua/inválida;
- APIs legadas dos consumidores alterados mantêm suas assinaturas públicas;
- curvas de ML preservam dados/métricas e usam `palette.curves_legacy` na rota resolvida;
- timeline do monitor preserva períodos, valores e thresholds; apenas cores/layout variam;
- UMAP resolvido reaproveita as mesmas coordenadas/labels e não torna `umap-learn` import obrigatório;
- vintage resolvido preserva pontos e matriz e usa paletas categórica/sequencial;
- consumidores PySpark possuem rotas resolvidas sem duplicar contrato analítico;
- SHAP e Kaplan–Meier permanecem exceções declaradas, não suporte implícito;
- exportação HTML local de uma figura resolvida preserva o tema;
- PDF/PPTX/PNG Plotly não aparecem como formatos homologados;
- funções resolvidas não introduzem literais hexadecimais locais para contornar o contrato.

## Regressões obrigatórias

Além da suíte V07, o workflow específico executa:

```bash
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Os testes V06 continuam exigindo Node 22, `pnpm@10.34.5` e dependências do compositor. O workflow V07 deve preparar o mesmo ambiente; não é permitido filtrar V06 para obter verde.

## Evidência ainda não executada

Este documento nasce antes do primeiro run V07. IDs, failures, correções e contagens reais serão acrescentados conforme os gates forem executados. Nenhum failure deve ser reclassificado retroativamente.

## O que PASS não prova

- render real no browser Databricks;
- acessibilidade visual;
- UAT humano;
- Spark/SQL/MLflow remoto;
- ACL/workspace;
- PNG Plotly/Kaleido;
- PDF ou PPTX;
- suporte temático de SHAP ou Kaplan–Meier.
