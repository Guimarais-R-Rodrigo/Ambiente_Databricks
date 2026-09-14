# V06 — assets e geração orientados por tema

## Estado desta sprint

**INTEGRADA NO GIT; SEM PUBLICAÇÃO DATABRICKS; V07 NÃO INICIADA.** A V06 foi aceita por Rodrigo em 14/09/2026 e integrada pelo PR #38. O head final validado foi `70499e1803ce0d61a148a0da975c4f52611046e0`; o merge na `main` é `418946de8d1e95e87cbfd9df528ddcced5075237`. A árvore do merge (`68ddec3d691047e890ba2785e1e2e007039fa0e3`) é idêntica à árvore do head final testado.

O objetivo canônico desta sprint é **documentar assets e geração**. A implementação conecta o compositor editorial v2 ao núcleo de temas V02 sem criar uma segunda fonte de verdade: o usuário fornece um `theme_id` canônico, o tema é carregado e revalidado como `ResolvedTheme` e somente um derivado controlado é entregue ao renderer.

A V06 não publica no Databricks, não aprova tema ou asset, não altera ACL/compute e não antecipa a integração transversal da V08 nem os guias de Apps/AI-BI de versões posteriores.

## Para quem nunca entrou no Hub

Existem duas coisas diferentes:

1. **pacote visual ativo** — os PNGs/SVGs atualmente distribuídos pelo Hub;
2. **variante candidata** — uma nova renderização criada localmente para comparação e revisão.

A V06 só cria a segunda. Ela grava em `.artifacts/visual-v2/theme-variants/` e se recusa a usar `hub_readmes_visual_assets/` como destino. Portanto, gerar uma variante não muda o que os usuários veem no Hub.

Assets congelados são tratados como bytes protegidos por SHA-256. Eles não são recoloridos automaticamente. Se um asset paramétrico mudar de bytes, o manifesto o classifica como `variant_review_required`; isso significa “precisa de revisão e nova revisão/versionamento antes de promoção”, não “aprovado”.

## Arquitetura

A cadeia é:

`theme_id` → `theme_bridge.py` → `hub_snippets.visual.tema.load_theme()` → `ResolvedTheme` → derivado controlado → `theme_assets.mjs` → compositor v2 existente → `.artifacts/.../manifest.yaml`.

O bridge não aceita caminho JSON arbitrário como API pública. Ele procura o `theme_id` no conjunto canônico de exemplos, exige correspondência única e delega schema, contexto, hashes e `asset_set_id` ao núcleo V02.

O renderer reaproveita `tools/readme_visuals/lib.mjs`, os arquétipos existentes, `visual_contracts.yaml` e as assinaturas aprovadas. A V06 não duplica layout nem mantém outro YAML de tema.

## Classes de asset

- `frozen`: baseline contratual imutável; hash diferente falha fechado.
- `frozen_approved_signature`: assinatura aprovada copiada sem reinterpretar o design.
- `parametric_equivalent`: renderização por tokens é byte a byte equivalente ao PNG ativo.
- `variant_review_required`: renderização é válida, mas difere do ativo e precisa de nova revisão antes de qualquer promoção.

O registro canônico dessas regras é `ambiente_fonte/.assistant/hub_readmes_visual_assets/specs/theme_generation.yaml`.

## Reprodutibilidade

A geração exige `SOURCE_DATE_EPOCH`. Assim, duas execuções do mesmo tema, mesma revisão do renderer e mesmo epoch produzem a mesma árvore de arquivos e o mesmo manifesto.

Exemplo PowerShell, a partir da raiz do repositório:

```powershell
$env:SOURCE_DATE_EPOCH = '1700000000'
python tools/readme_visuals/theme_bridge.py --theme-id hub-legado-editorial --context readme
node tools/readme_visuals/theme_assets.mjs --theme-id hub-legado-editorial --family all
node tools/readme_visuals/theme_assets.mjs --theme-id hub-legado-editorial --verify
```

Antes disso, instale as dependências fixadas do compositor com `pnpm --dir tools/readme_visuals install --frozen-lockfile` e as dependências Python declaradas pelo projeto.

## Manifesto de evidência

Cada geração candidata registra no manifesto:

- identidade e versão do tema;
- `fingerprint`, hashes do conteúdo, schema e manifesto de assets usados pelo `ResolvedTheme`;
- renderer/gerador e epoch;
- classificação e ação esperada de cada figura;
- dimensões e uso pretendido;
- hash do SVG e do PNG candidato;
- hash do PNG ativo usado como baseline;
- lista dos 12 recursos congelados e seus hashes.

O manifesto declara `status: candidate_not_approved` e `approval_or_publication_performed: false`.

## Testes e integração

`tools/tests/test_temas_v06.py` cobre seleção fail-closed por `theme_id`, determinismo, proteção dos 12 assets congelados, hashes/dimensões da variante, adulteração, proibição de saída no pacote ativo e paridade do contrato fonte/espelho.

No head final `70499e18...`, os workflows da PR concluíram com `success`: CI geral, V00, V01, V02, V04, V05 e V06. A suíte específica V06 permaneceu em **5/5**, a descoberta cumulativa V01–V06 em **364/364** e a compatibilidade V00 em **12/12**.

Depois do merge `418946de...`, oito workflows disparados por `push` na `main` concluíram com `success`: CI geral e V00–V06, incluindo o V03. Os IDs finais estão registrados em [TESTES.md](TESTES.md).

A correção final de CI não removeu nem filtrou testes: V04 e V05 continuaram executando `test_temas*.py` cumulativamente até V06, com Node 22 e `pnpm@10.34.5` preparados antes da regressão. `ci_local.py` continua fail-closed e não instala dependências Node silenciosamente para o operador local.

Falhas históricas não são reclassificadas como sucesso. Consulte [TESTES.md](TESTES.md) e [CHECKPOINT_V06.md](CHECKPOINT_V06.md).

## O que não foi provado

A V06 não prova renderização no navegador Databricks, acessibilidade percebida, UAT por iniciante, ACL real, publicação, promoção de variante ou operação em workspace corporativo. Essas evidências continuam gates separados.

## Fechamento

A integração Git da V06 está concluída. O pacote ativo não foi publicado nem alterado por uma promoção de candidata; nenhuma ação remota de Spark, SQL, MLflow, ACL ou workspace foi executada nesta rota. A V07 ainda não foi iniciada.
