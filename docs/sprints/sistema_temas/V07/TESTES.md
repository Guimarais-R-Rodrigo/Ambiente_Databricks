# V07 — testes e evidências

## Escopo automatizado

A suíte específica é `tools/tests/test_temas_v07.py`. Ela prova, sem Databricks remoto:

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
- funções resolvidas não introduzem literais hexadecimais locais para contornar o contrato;
- arquivos alterados e READMEs operacionais permanecem byte a byte iguais entre fonte e ambiente simulado.

## Regressões obrigatórias

Além da suíte V07, o workflow específico executa:

```bash
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Os testes V06 continuam exigindo Node 22, `pnpm@10.34.5` e dependências do compositor. O workflow V07 prepara o mesmo ambiente; não é permitido filtrar V06 para obter verde.

## Primeira execução — `34858836840` — FAILURE documental

O primeiro run V07 não foi reclassificado como sucesso. Antes da etapa documental, passaram:

- suíte específica V07: **18/18 PASS**;
- regressões cumulativas V01–V07: **382/382 PASS**;
- compatibilidade visual V00: **12/12 PASS**.

A execução reprovou em `validate_assistant.py --conferir-readme` por duas classes de divergência:

1. quatro fachadas `__init__.py` (`correlation_matrix`, `distribution_grid`, `curves_plotly` e `vintage_analysis`) haviam sido escritas manualmente e não coincidiam byte a byte com a saída canônica de `tools/api_publica.py`;
2. o README raiz ainda registrava `1339` arquivos de identidade e `1840` links fora da raiz, enquanto o validador mediu **1344** e **1841** naquele checkout.

A correção das fachadas foi feita pelo contrato exaustivo de API pública, não por relaxamento do validador. As métricas do README não foram corrigidas imediatamente porque a documentação dos objetos ainda acrescentaria arquivos/links e exigiria nova medição.

## Migração documental dos objetos

Sete READMEs operacionais receberam uma nota `Atualização V07 — estado atual` imediatamente após o marcador `readme-objeto: 1.0.0`, com a mesma alteração aplicada ao ambiente simulado. A migração foi executada por mecanismo transitório de escrita somente para evitar reescrever/truncar documentos longos; depois da escrita, o workflow permanente foi restaurado para `contents: read`, checkout sem credencial persistente e o script transitório foi removido.

A guarda `test_temas_v07_mirror.py` foi ampliada para comparar também esses sete READMEs byte a byte. O run associado à migração e os runs posteriores devem permanecer registrados com sua conclusão real quando finalizados.

## O que PASS não prova

- render real no browser Databricks;
- acessibilidade visual;
- UAT humano;
- Spark/SQL/MLflow remoto;
- ACL/workspace;
- PNG Plotly/Kaleido;
- PDF ou PPTX;
- suporte temático de SHAP ou Kaplan–Meier.
