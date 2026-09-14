# V07 — testes e evidências

## Escopo automatizado

A suíte específica da V07 é a família `tools/tests/test_temas_v07*.py`, formada por `test_temas_v07.py` e `test_temas_v07_mirror.py`. Ela prova, sem Databricks remoto:

- o registro estruturado cobre todos os nove consumidores runtime de `display`/`ml` identificados para esta sprint;
- controles declarados pela V07 possuem ao menos um consumidor suportado;
- `get_tokens_plotly` revalida `ResolvedTheme`, devolve cópia e falha fechado para entrada crua/inválida;
- APIs legadas dos consumidores alterados mantêm suas assinaturas públicas;
- curvas de ML preservam dados/métricas e usam `palette.curves_legacy` na rota resolvida;
- timeline do monitor preserva períodos, valores e thresholds; apenas cores/layout variam;
- UMAP resolvido reaproveita as mesmas coordenadas/labels e não torna `umap-learn` import obrigatório;
- vintage resolvido preserva pontos e matriz e usa paletas categórica/sequencial;
- a correlação resolvida usa `palette.diverging`, coerente com o domínio simétrico de -1 a +1, e a guarda rejeita regressão para `palette.sequential`;
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

## `34861318310` — SUCCESS permanente antes da revisão semântica

Depois da reconciliação, o workflow V07 foi restaurado para `contents: read` e `persist-credentials: false`. Nesse head permanente concluíram com `success`:

- suíte específica V07: **18/18**;
- regressões cumulativas V01–V07: **382/382**;
- compatibilidade visual V00: **12/12**;
- validação estrutural/documental;
- escopo.

Esse run permanece sucesso real, mas foi superado por uma revisão semântica posterior antes da PR.

## Revisão semântica da correlação

A revisão do diff antes da PR identificou uma inconsistência que os testes anteriores não capturavam: o heatmap de correlação possui domínio simétrico de **-1 a +1**, enquanto a primeira implementação V07 havia conectado a rota resolvida a `palette.sequential`.

O contrato de temas já possui `palette.diverging`, com centro neutro e extremos de sinais opostos. A correção, portanto, foi usar `palette.diverging` na correlação, sincronizar código/README no ambiente simulado, atualizar o registro estruturado e acrescentar uma guarda permanente que falha se a implementação voltar a usar `palette.sequential` nesse consumidor. Cálculo Spark, matriz, threshold e pares fortes não foram alterados.

## `34861831151` — SUCCESS transitório da correção semântica

A rodada transitória que sincronizou a correção semântica concluiu com:

- V07: **19/19 PASS**;
- regressões V01–V07: **383/383 PASS**;
- V00: **12/12 PASS**;
- validação estrutural/documental: **APROVADO — 0 falhas, 0 avisos**;
- métricas do README conferidas em **1345 arquivos** de identidade e **1849 links fora da raiz**;
- escopo: **PASS**.

Esse run usou permissão de escrita somente para sincronizar os arquivos envolvidos e, por isso, não substitui a evidência de um head permanente read-only.

## `34862109553` — SUCCESS permanente após a correção semântica

No head `a7982d3d439584dd9d952df8ced326bf908f40e3`, com workflow novamente permanente (`contents: read`, `persist-credentials: false`), passaram:

- suíte V07: **19/19**;
- regressões cumulativas V01–V07: **383/383**;
- compatibilidade visual V00: **12/12**;
- validação estrutural/documental: **APROVADO — 0 falhas, 0 avisos**;
- métricas conferidas: **1345 arquivos** de identidade e **1849 links fora da raiz**;
- escopo: **PASS**.

Esse head também confirmou a guarda `test_correlation_uses_diverging_palette` e a equivalência byte a byte entre fonte e ambiente simulado.

## Último gate antes da PR

Esta atualização consolida o histórico e cria um novo SHA. Por governança, o workflow permanente V07 deve ser repetido nesse SHA exato. Somente depois de verde serão feitas a revisão final de diff/base e a abertura da PR em **draft**. Os checks disparados pela PR também precisarão concluir no mesmo head antes de solicitar aceite de integração.

Nenhum failure acima é convertido retroativamente em sucesso. Nenhuma publicação Databricks foi realizada e a V08 não foi iniciada.

## O que PASS não prova

- render real no browser Databricks;
- acessibilidade visual;
- UAT humano;
- Spark/SQL/MLflow remoto;
- ACL/workspace;
- PNG Plotly/Kaleido;
- PDF ou PPTX;
- suporte temático de SHAP ou Kaplan–Meier.
