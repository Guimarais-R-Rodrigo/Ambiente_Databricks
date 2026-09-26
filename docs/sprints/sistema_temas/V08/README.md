# V08 — integração transversal com skills, padrões e Manual

> **Estado atual:** aceita por Rodrigo e integrada no Git em 14/09/2026 pelo PR #42. O head final validado foi `9af5615d79b02cbd86f5a6d084444c83f203ae03` e o merge efetivo na `main` é `622d2c962a80998cf990b57036f7ae503bfc0458`. Sem publicação Databricks. O [checkpoint](CHECKPOINT_V08.md) e o [registro de testes](TESTES.md) concentram evidências, failures preservados e limites do fechamento.

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
- o template visual da EDA se declarava fonte central, repetia hexadecimais e construía política visual própria;
- a criação de objetos podia fazer `constants.colors` parecer a fonte configurável para novos temas;
- skills que consomem curvas, safras e monitoramento não distinguiam claramente cálculo de aparência temática;
- a skill de explicabilidade não registrava que SHAP/Matplotlib permanece exceção ao theming V07.

A [`MATRIZ_INTEGRACAO.json`](MATRIZ_INTEGRACAO.json) registra cada superfície, motivo e efeito esperado.

## O que a V08 integrou

- `.assistant/README.md` apresenta V00–V07 como camadas integradas e separa autoria, consumo, geração e publicação;
- `skills/README.md` declara que templates/skills não são fonte de tokens;
- Concierge ganha rota explícita para tema/identidade visual;
- criação de objeto passa a tratar `ResolvedTheme`/padrão central como fonte configurável e `constants.colors` como compatibilidade legada;
- EDA profissional usa consumidores `_resolvido` quando houver tema selecionado e mantém análise independente da aparência;
- baseline, safra e monitoramento passam a registrar explicitamente que tema não muda métricas, denominadores ou policy;
- explainability registra SHAP/Matplotlib como exceção ao theming atual;
- Hub Padrões, identidade visual e guia operacional chegam ao estado V07;
- a seção viva do Manual Técnico passa a descrever V02–V07 e os limites atuais;
- as três cópias do Manual permanecem byte a byte iguais.

A skill `hub-ml-comentar-notebook` foi deliberadamente classificada como **sem edição**: ela documenta notebook e proíbe alteração de código; fazer V08 injetar theming nela contrariaria o contrato da própria skill.

## Template EDA

O antigo `estilo_visual_eda.md` foi convertido de fonte visual paralela em guia editorial sobre o Sistema de Temas. A V08 preserva orientações úteis de escolha de gráficos, anotações, emojis, números, tabelas, KPI-line, hierarquia, narrativa pós-código, índice e cabeçalhos, mas remove:

- paleta/dicionário local usados como política de tema;
- literais hexadecimais de política visual;
- recomendação de registro global legado como preparação padrão;
- CSS/HTML manual como substituto dos componentes V04.

Quando houver tema notebook válido, o guia usa `ResolvedTheme` e rotas `_resolvido`; sem tema selecionado, preserva APIs legadas.

## Princípios de implementação

1. **Sem segunda fonte de verdade.** Skills e templates não repetem paleta/hexadecimais para representar tema configurável.
2. **Sem mudança de runtime.** V08 não edita módulos Python de `hub_snippets` ou `hub_scripts`.
3. **Rotas opt-in continuam opt-in.** Documentação não transforma `_resolvido` em efeito global ou automático.
4. **Sem semântica analítica no tema.** Thresholds, dados, métricas, agregações, amostras e decisões não mudam com a aparência.
5. **Exceções permanecem visíveis.** SHAP/Matplotlib e Kaplan–Meier não são apresentados como tematizados onde o contrato ainda não suporta isso.
6. **Sem falsa homologação.** Integração Git continua distinta de publicação Databricks, browser, acessibilidade, ACL e UAT.

## Escopo proibido

- alterar código runtime de snippets/scripts;
- alterar schema ou conjunto de tokens;
- mudar defaults das APIs legadas;
- registrar tema global por simples import ou orientação padrão;
- publicar tema, asset ou pacote no Databricks;
- afirmar que dark/high-contrast, SHAP, browser ou acessibilidade estão homologados sem evidência correspondente.

## Critérios comprovados

A V08 demonstrou antes do merge:

1. matriz transversal completa e consistente;
2. template EDA sem paleta/tema paralelo e sem literais `#RRGGBB` usados como política visual;
3. skills relevantes apontando para o Sistema de Temas e preservando separação entre cálculo e aparência;
4. Manual e padrão de identidade sem rótulos V04/V05 obsoletos;
5. fonte e ambiente simulado sincronizados nas superfícies alteradas;
6. três cópias do Manual byte a byte iguais;
7. nenhum módulo Python runtime alterado em relação à base V08;
8. suíte V08, regressões V01–V08, V00 e validador documental verdes;
9. workflow permanente read-only;
10. PR #42 validada no SHA final, aceita explicitamente e mesclada somente depois de todos os checks verdes.

## Evidência final

No head final `9af5615d79b02cbd86f5a6d084444c83f203ae03`, o gate permanente de push `34872178809` concluiu com **22/22 V08**, **405/405 regressões V01–V08**, **12/12 V00**, validador **0 falhas / 0 avisos**, `V08_RUNTIME_EDIT=0` e escopo verde. Os nove checks da PR #42 também concluíram com `success` no mesmo head.

Depois do merge `622d2c962a80998cf990b57036f7ae503bfc0458`, os dez workflows disparados na `main` — CI geral e V00–V08 — concluíram com `success`. O histórico completo está em [TESTES.md](TESTES.md).

## Limites

A V08 melhora orientação, roteamento e documentação. Ela não prova que a Genie Code sempre selecionará a skill correta por relevância, não homologa o visual no navegador Databricks e não transforma documentação em controle técnico de permissão.

Nenhuma publicação Databricks foi executada pela V08. A V09 não foi iniciada.
