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

O workflow específico executa também:

```bash
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Os testes V06 continuam exigindo Node 22, `pnpm@10.34.5` e dependências do compositor. O workflow V07 prepara o mesmo ambiente; não é permitido filtrar V06 para obter verde.

## Failures históricos preservados

### `34858836840` — FAILURE documental inicial

Antes da etapa documental, passaram 18/18 V07, 382/382 regressões V01–V07 e 12/12 V00. A execução reprovou porque quatro fachadas `__init__.py` não coincidiam com a saída canônica de `tools/api_publica.py` e porque o README raiz trazia métricas anteriores. As fachadas foram corrigidas conforme o contrato, sem relaxar o validador.

### `34859769442` — FAILURE documental da migração

Passaram novamente 18/18 V07, 382/382 regressões e 12/12 V00. O validador mediu 1345 arquivos de identidade e 1841 links fora da raiz, enquanto o README ainda registrava os valores anteriores. O mecanismo transitório utilizado para atualizar READMEs foi posteriormente removido.

### `34860697409` — FAILURE documental de medição final

As camadas funcionais ficaram verdes, mas o README raiz ainda não refletia a medição estabilizada de 1345 arquivos e 1849 links fora da raiz. Foram duas falhas numéricas e zero avisos; não houve erro novo de API pública, link quebrado ou contrato de objeto.

Nenhum desses failures foi convertido retroativamente em sucesso.

## Sucessos de reconciliação e revisão

- `34861248396`: sucesso transitório ao reconciliar métricas/changelog;
- `34861318310`: sucesso permanente read-only antes da revisão semântica;
- revisão do diff detectou que correlação [-1,+1] deveria usar `palette.diverging`, não `palette.sequential`;
- `34861831151`: sucesso transitório da sincronização dessa correção;
- `34862109553`: sucesso permanente read-only após a correção semântica.

## Head final pré-merge — `6b50151738a311eff8530c3191e24693af3fb036`

O run permanente `34862446870`, com `contents: read` e `persist-credentials: false`, concluiu:

- V07: **19/19 PASS**;
- regressões V01–V07: **383/383 PASS**;
- V00: **12/12 PASS**;
- validação estrutural/documental: **APROVADO — 0 falhas, 0 avisos**;
- métricas conferidas: **1345 arquivos** de identidade e **1849 links fora da raiz**;
- escopo: **PASS**.

A PR #40 foi aberta sobre esse SHA exato. Os sete workflows disparados pelo evento `pull_request` — CI geral, V00, V01, V02, V03, V05 e V07 — concluíram todos com `success`. V04 e V06 não foram disparados separadamente pela regra de paths da PR; ambos já estavam contidos na regressão cumulativa V01–V07 do próprio gate V07.

Rodrigo então autorizou explicitamente a aprovação e integração da V07.

## Integração e pós-merge

A PR #40 foi mesclada com proteção pelo expected head SHA `6b50151738a311eff8530c3191e24693af3fb036`. O merge commit resultante é `67114605c7345a01c1144e5d6c6d24e9c24e2491` e sua árvore `5438288bda2326e96372c7464b3aef0cb8375102` coincide com a árvore do head final testado.

O push na `main` disparou nove checks, todos concluídos com `success`:

- V00 — `34863452273`;
- V01 — `34863452340`;
- V02 — `34863452364`;
- V03 — `34863452332`;
- V04 — `34863452339`;
- V05 — `34863452252`;
- V06 — `34863452347`;
- V07 — `34863452328`;
- CI geral — `34863452363`.

Esse fechamento pós-merge confirma que a composição efetiva da `main`, e não apenas a branch candidata, preserva os gates V00–V07.

## O que PASS não prova

- render real no browser Databricks;
- acessibilidade visual;
- UAT humano;
- Spark/SQL/MLflow remoto;
- ACL/workspace;
- PNG Plotly/Kaleido;
- PDF ou PPTX;
- suporte temático de SHAP ou Kaplan–Meier.

Nenhuma publicação Databricks foi realizada durante V07.
