# V08 — integração transversal com skills, padrões e Manual

> **Estado atual:** em execução na branch `codex/temas-v08-integracao-transversal-20260914`, criada a partir da `main` estabilizada em `1b6632194f4b25afc09960c27b069c16df365ee6`. Sem aceite, merge ou publicação Databricks.

## Objetivo

A V08 conecta o Sistema de Temas já implementado às superfícies que orientam o uso do Hub: **Agent Skills, Hub Padrões, entrada `.assistant` e Manual Técnico**. Ela não cria um novo resolvedor, nova paleta, nova UI ou nova API runtime.

A regra de propriedade é explícita:

- schema e limites: `hub_padroes/identidade_visual/theme.schema.json`;
- tokens: `hub_padroes/identidade_visual/TOKENS.md`;
- validação/resolução: `hub_snippets.visual.tema` / `ResolvedTheme`;
- adaptação Plotly: `hub_snippets.visual.theme_plotly`;
- uso por componente: README/API local do consumidor;
- conceitos transversais e navegação operacional: Manual Técnico e padrões;
- metodologia: skills, sem redefinir a política visual.

## Problema que a sprint resolve

Depois da V07, o runtime e os READMEs locais estavam atualizados, mas parte da orientação transversal ainda refletia estados antigos. Exemplos encontrados no inventário inicial:

- o Manual ainda dizia “V04 integrada; V05 candidata”;
- o padrão central de identidade visual ainda parava em V04;
- o template visual da EDA se declarava fonte central, repetia hexadecimais e construía `TEMA_EDA` próprio;
- a criação de objetos podia fazer `constants.colors` parecer a fonte configurável para novos temas;
- skills que consomem curvas, safras e monitoramento não distinguiam claramente cálculo de aparência temática;
- a skill de explicabilidade não registrava que SHAP/Matplotlib permanece exceção ao theming V07.

A [`MATRIZ_INTEGRACAO.json`](MATRIZ_INTEGRACAO.json) registra cada superfície, motivo e efeito esperado.

## Princípios de implementação

1. **Sem segunda fonte de verdade.** Skills e templates não repetem paleta/hexadecimais para representar tema configurável.
2. **Sem mudança de runtime.** V08 não edita módulos Python de `hub_snippets` ou `hub_scripts`.
3. **Rotas opt-in continuam opt-in.** Documentação não transforma `_resolvido` em efeito global ou automático.
4. **Sem semântica analítica no tema.** Thresholds, dados, métricas, agregações, amostras e decisões não mudam com a aparência.
5. **Exceções permanecem visíveis.** SHAP/Matplotlib e Kaplan–Meier não são apresentados como tematizados onde o contrato ainda não suporta isso.
6. **Sem falsa homologação.** Integração Git continua distinta de publicação Databricks, browser, acessibilidade, ACL e UAT.

## Escopo de edição

A V08 pode atualizar:

- entrada `.assistant/README.md`;
- catálogo `skills/README.md`;
- skills que roteiam ou usam diretamente consumidores visuais relevantes;
- template `estilo_visual_eda.md`;
- `hub_padroes/README.md` e `hub_padroes/identidade_visual/*` de orientação;
- seção viva do Sistema de Temas no Manual Técnico;
- cópias derivadas dessas superfícies no `Novo_Ambiente_Simulado` e do Manual raiz.

A skill `hub-ml-comentar-notebook` foi deliberadamente classificada como **sem edição**: ela documenta notebook e proíbe alteração de código; fazer V08 injetar theming nela contrariaria o contrato da própria skill.

## Escopo proibido

- alterar código runtime de snippets/scripts;
- alterar schema ou conjunto de tokens;
- mudar defaults das APIs legadas;
- registrar tema global por simples import ou orientação padrão;
- publicar tema, asset ou pacote no Databricks;
- afirmar que dark/high-contrast, SHAP, browser ou acessibilidade estão homologados sem evidência correspondente.

## Critérios de aceite

A candidata V08 precisa demonstrar:

1. matriz transversal completa e consistente;
2. template EDA sem paleta/tema paralelo e sem literais `#RRGGBB` usados como política visual;
3. skills relevantes apontando para o Sistema de Temas e preservando separação entre cálculo e aparência;
4. Manual e padrão de identidade sem rótulos V04/V05 obsoletos;
5. fonte e ambiente simulado sincronizados nas superfícies alteradas;
6. três cópias do Manual byte a byte iguais;
7. nenhum módulo Python runtime alterado em relação à base V08;
8. suíte V08, regressões V01–V08, V00 e validador documental verdes;
9. workflow permanente read-only;
10. PR draft no SHA final e parada para aceite explícito antes de merge.

## Limites

A V08 melhora orientação, roteamento e documentação. Ela não prova que a Genie Code sempre selecionará a skill correta por relevância, não homologa o visual no navegador Databricks e não transforma documentação em controle técnico de permissão.
