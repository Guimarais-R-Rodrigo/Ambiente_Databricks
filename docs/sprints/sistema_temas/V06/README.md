# V06 — assets e geração orientados por tema

## Estado desta sprint

**CANDIDATA EM EXECUÇÃO; SEM ACEITE OU MERGE.** A V06 parte da `main` já contendo a V05 integrada (`d728b872c77c89723a016919bd80534fb297b488`) e trabalha somente na branch `codex/temas-v06-assets-geracao-20260914`.

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

## Testes

`tools/tests/test_temas_v06.py` cobre seleção fail-closed por `theme_id`, determinismo, proteção dos 12 assets congelados, hashes/dimensões da variante, adulteração, proibição de saída no pacote ativo e paridade do contrato fonte/espelho.

O workflow permanente `.github/workflows/temas-v06-ci.yml` usa `contents: read`, instala as dependências declaradas, roda a suíte V06, regressões V01–V06, compatibilidade V00 e `validate_assistant.py --conferir-readme`.

Falhas históricas não são reclassificadas como sucesso. Consulte [TESTES.md](TESTES.md) e [CHECKPOINT_V06.md](CHECKPOINT_V06.md).

## O que não foi provado

A V06 não prova renderização no navegador Databricks, acessibilidade percebida, UAT por iniciante, ACL real, publicação, promoção de variante ou operação em workspace corporativo. Essas evidências continuam gates separados.

## Ponto de parada

A sprint só deve ir a aceite quando a mesma árvore candidata tiver suíte V06, regressões, V00 e validação documental verdes, documentação sincronizada, diff revisado e PR draft final. Mesmo depois disso, merge exige aceite explícito e publicação Databricks continua fora do escopo.
