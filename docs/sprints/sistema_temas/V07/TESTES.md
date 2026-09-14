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

## `34858836840` — FAILURE documental inicial

O primeiro run V07 não foi reclassificado como sucesso. Antes da etapa documental, passaram:

- suíte específica V07: **18/18 PASS**;
- regressões cumulativas V01–V07: **382/382 PASS**;
- compatibilidade visual V00: **12/12 PASS**.

A execução reprovou em `validate_assistant.py --conferir-readme` por duas classes de divergência:

1. quatro fachadas `__init__.py` (`correlation_matrix`, `distribution_grid`, `curves_plotly` e `vintage_analysis`) haviam sido escritas manualmente e não coincidiam byte a byte com a saída canônica de `tools/api_publica.py`;
2. o README raiz ainda registrava `1339` arquivos de identidade e `1840` links fora da raiz, enquanto o validador mediu **1344** e **1841** naquele checkout.

A correção das fachadas foi feita pelo contrato exaustivo de API pública, não por relaxamento do validador.

## `34859769442` — FAILURE documental da migração

A rodada transitória que atualizou sete READMEs fonte/simulado concluiu com:

- suíte específica V07: **18/18 PASS**;
- regressões cumulativas V01–V07: **382/382 PASS**;
- compatibilidade visual V00: **12/12 PASS**.

O run permaneceu **FAILURE** porque o validador mediu **1345 arquivos** na identidade do repositório e **1841 links fora da raiz**, enquanto o README ainda registrava 1339/1840. Esse failure é evidência histórica e não é convertido em sucesso por execuções posteriores.

Sete READMEs operacionais receberam uma nota `Atualização V07 — estado atual` imediatamente após o marcador `readme-objeto: 1.0.0`, com a mesma alteração aplicada ao ambiente simulado. O mecanismo transitório existiu somente para evitar reescrever/truncar documentos longos. Depois da escrita, o workflow permanente foi restaurado para `contents: read`, checkout sem credencial persistente, e o script transitório foi removido da árvore permanente.

## `34860697409` — FAILURE documental de medição final

Depois de checkpoint, índices vivos e estado explícito da candidata já estarem presentes, as camadas funcionais voltaram a passar:

- V07: **18/18 PASS**;
- regressões V01–V07: **382/382 PASS**;
- V00: **12/12 PASS**;
- guarda de espelho fonte/simulado: **PASS**.

A única reprovação foi a saída colada do README raiz. O validador mediu o estado documental estabilizado em **1345 arquivos** de identidade e **1849 links fora da raiz**, enquanto o README ainda continha 1339/1840. Foram exatamente duas falhas numéricas e zero avisos; não houve novo erro de API pública, link quebrado ou contrato de objeto.

## `34861248396` — SUCCESS transitório de reconciliação

Uma rodada de escrita controlada substituiu no checkout os dois números do README por **1345/1849** e inseriu no changelog a entrada V07 como **candidata**, sem links relativos novos. Nessa árvore, passaram suíte V07, regressões V01–V07, V00, validação estrutural/documental e escopo.

Esse sucesso é preservado como evidência da reconciliação, mas não é usado sozinho como aceite da candidata porque o workflow daquele run possuía permissão de escrita transitória. O commit produzido tocou somente `README.md` e `CHANGELOG.md`.

## `34861318310` — SUCCESS com workflow permanente read-only

Depois da reconciliação, o workflow V07 foi restaurado para `contents: read` e `persist-credentials: false`. Nesse head permanente concluíram com `success`:

- suíte específica V07: **18/18**;
- regressões cumulativas V01–V07: **382/382**;
- compatibilidade visual V00: **12/12**;
- validação estrutural/documental;
- escopo.

A `main` continuava em `0c0c71bce4bbc09130ec51eec8245057be4f3d81`, portanto a branch permanecia `behind_by=0`.

## Estado antes da PR

Este registro é a última edição documental planejada antes da PR. Como a própria atualização deste arquivo cria um novo SHA, o workflow permanente V07 deve ser repetido nesse head exato. Só depois de verde o diff será revisado novamente e a PR será aberta em draft; CI agregado e demais checks disparados pela PR devem ser auditados no mesmo SHA.

Nenhum failure acima é convertido retroativamente em sucesso.

## O que PASS não prova

- render real no browser Databricks;
- acessibilidade visual;
- UAT humano;
- Spark/SQL/MLflow remoto;
- ACL/workspace;
- PNG Plotly/Kaleido;
- PDF ou PPTX;
- suporte temático de SHAP ou Kaplan–Meier.
