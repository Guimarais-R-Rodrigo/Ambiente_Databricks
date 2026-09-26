# Checkpoint V11 — temas nativos AI/BI

## Estado

**V11 ACEITA E INTEGRADA; PÓS-MERGE FUNCIONAL VERDE; ESTA ENTREGA É A RECONCILIAÇÃO DOCUMENTAL FINAL.**

Base de início: `a9480391c78e2402986885db0ce08b10e0619a1a`.

Branch funcional: `codex/temas-v11-aibi-20260914`.

Head final aceito: `5532ca6d8f1b243ca705088f4b57823a333b9b1f`.

PR funcional: **#52**.

Merge funcional: `9305bc49eaf002caec042361bf35efa66af7ca18`.

Aceite explícito: **14/09/2026**.

## Decisões congeladas

- `ResolvedTheme` continua a fonte de verdade;
- o schema V01/V02 não foi ampliado silenciosamente;
- `context="aibi"` continua reservado;
- a projeção V11 parte do contexto `notebook`;
- o JSON nativo exportado pelo AI/BI é tratado como formato externo sem schema público completo e versionado nas fontes verificadas;
- nenhum JSON nativo é inventado;
- binding nativo exige template real fixado por SHA-256;
- somente correspondências traduzidas podem ser aplicadas automaticamente;
- aproximações exigem revisão;
- itens não suportados permanecem explícitos;
- workspace theme e dashboard theme não são tratados como o mesmo escopo;
- atualizações de workspace theme não são descritas como propagação automática;
- publicação permanece fora do código;
- nenhum efeito remoto é permitido pela CI.

## Artefatos integrados

- `hub_padroes/identidade_visual/aibi/aibi_theme.py` — fachada pública;
- `hub_padroes/identidade_visual/aibi/_aibi_theme_impl.py` — implementação interna;
- `hub_padroes/identidade_visual/aibi/aibi_mapping.json`;
- `hub_padroes/identidade_visual/aibi/dashboard_sintetico.json`;
- README e guia de primeiro uso;
- espelho equivalente;
- `tools/tests/test_temas_v11.py`;
- `.github/workflows/temas-v11-ci.yml`;
- documentação V11 e fontes oficiais.

## Failures históricos preservados

### `34900693160`
Primeira composição: **19/20** na suíte V11. A única falha foi a exceção V02 escapando pela fronteira pública V11 para contexto editorial. Corrigido sem alterar V02.

### `34901091132`
Head `5eca34c95fc9970f864869282f59e2bb4cc61d56`: V11 **20/20**, regressões V01–V11 **456/456** e V00 **12/12**; validador **3 falhas / 0 avisos** por métricas antigas no README raiz. Escopo ficou `SKIP` por consequência.

### `34901776770`
Head `8785822e045edf158f04ea41ea0f6c059ef11cb1`: o novo teste de import pelo namespace funcionou, mas o oráculo esperava um ID não canônico. Resultado: **20/21 PASS**; etapas posteriores ficaram `SKIP`. A correção alterou somente a expectativa do teste.

### `34904363803`
Head `795edf879c6f013553afa725a02473d49c909624`: V11 **21/21**, regressões **457/457** e V00 **12/12** passaram. O validador reprovou com **3 falhas / 0 avisos** porque um SHA abreviado no checkpoint coincidiu com a guarda de identificador corporativo plausível; o escopo ficou `SKIP`. A correção passou a usar SHA completo sem alterar validador ou produto.

Nenhum desses runs é reclassificado.

## Evidências verdes

- `34902083889` no head `0d3180c50428d8716b44f264b915a91243ba96c3`: primeiro gate integralmente verde.
- `34902853430` no head `5bb8234422fdd284a9e14815ef566ec0b52a2952`: navegação/documentação revalidada.
- `34904743766` no head `6561dfbe147c454fdc07eebac3d644b6ae1bf6d0`: correção de higiene documental revalidada.
- `34905080083` no head final `5532ca6d8f1b243ca705088f4b57823a333b9b1f`: gate definitivo pré-PR, com V11 **21/21**, regressões **457/457**, V00 **12/12**, validador **0/0** e escopo **PASS**.
- PR #52: **11/11 workflows reais de `pull_request` em `success`** no mesmo head final.
- merge `9305bc49eaf002caec042361bf35efa66af7ca18`: **13/13 workflows de `push` em `success`**.

## Gates de integração

1. suíte V11 verde — **FECHADO**;
2. regressões V01–V11 verdes — **FECHADO**;
3. V00 verde — **FECHADO**;
4. source/simulado equivalentes — **FECHADO**;
5. validador 0/0 — **FECHADO**;
6. escopo sem operação remota — **FECHADO**;
7. diff sem credenciais — **FECHADO**;
8. documentação viva reconciliada — **FECHADA NESTA ENTREGA DOCUMENTAL**;
9. PR funcional mergeável/checks verdes — **FECHADO**;
10. aceite explícito — **FECHADO**;
11. merge funcional — **FECHADO**;
12. pós-merge funcional — **FECHADO, 13/13**.

## Limites de homologação

Continuam **não homologados** e não devem ser convertidos em PASS por inferência:
- export real do theme JSON AI/BI;
- binding revisado contra um export real;
- `Import theme` em dashboard draft real;
- permissões administrativas reais;
- aplicação de workspace theme real;
- snapshot e reaplicação reais;
- preservação de queries/filtros em dashboard real;
- browser e modos visuais;
- acessibilidade;
- UAT.

Nenhum deploy, publicação ou mutação Databricks foi executado pela V11.

## Próximo passo

Depois do merge e da validação pós-merge desta reconciliação documental, a V11 não possui outro passo de fechamento Git. A V12 pode ser iniciada como sprint independente a partir da `main` então vigente, recuperando primeiro o escopo canônico e sem executar operação real no Databricks sem autorização explícita.