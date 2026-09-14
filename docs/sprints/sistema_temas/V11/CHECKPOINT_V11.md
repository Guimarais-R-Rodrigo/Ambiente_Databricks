# Checkpoint V11 — temas nativos AI/BI

## Estado

**CANDIDATA V11 COM HEAD DOCUMENTAL FINAL VERDE; PR AINDA NÃO ABERTA/VALIDADA; SEM ACEITE, MERGE OU HOMOLOGAÇÃO DATABRICKS.**

Base: `a9480391c78e2402986885db0ce08b10e0619a1a`.

Branch: `codex/temas-v11-aibi-20260914`.

Primeiro head integralmente verde: `0d3180c50428d8716b44f264b915a91243ba96c3`.

Primeiro run integralmente verde: `34902083889`.

Head documental revalidado antes deste registro final: `5bb8234422fdd284a9e14815ef566ec0b52a2952`.

Run integralmente verde nesse head: `34902853430`.

## Decisões congeladas para esta sprint

- `ResolvedTheme` continua a fonte de verdade;
- o schema V01/V02 não é ampliado silenciosamente;
- `context="aibi"` continua reservado;
- a projeção V11 parte do contexto `notebook`;
- o JSON nativo exportado pelo AI/BI é tratado como formato externo não documentado;
- nenhum JSON nativo é inventado;
- binding nativo exige template real fixado por SHA-256;
- somente correspondências traduzidas podem ser aplicadas automaticamente;
- aproximações exigem revisão;
- itens não suportados permanecem explícitos;
- workspace theme e dashboard theme não são tratados como o mesmo escopo;
- atualizações de workspace theme não são descritas como propagação automática;
- publicação permanece fora do código;
- nenhum efeito remoto é permitido pela CI.

## Artefatos

- `hub_padroes/identidade_visual/aibi/aibi_theme.py` — fachada pública;
- `hub_padroes/identidade_visual/aibi/_aibi_theme_impl.py` — implementação interna;
- `hub_padroes/identidade_visual/aibi/aibi_mapping.json`;
- `hub_padroes/identidade_visual/aibi/dashboard_sintetico.json`;
- README e guia de primeiro uso;
- espelho equivalente;
- `tools/tests/test_temas_v11.py`;
- `.github/workflows/temas-v11-ci.yml`;
- documentação V11 e fontes oficiais.

## Failures preservados

### `34900693160`
Primeira composição: **19/20** na suíte V11. A única falha foi a exceção V02 escapando pela fronteira pública V11 para contexto editorial. Corrigido sem alterar V02.

### `34901091132`
Head `5eca34c95fc9970f864869282f59e2bb4cc61d56`: V11 **20/20**, regressões V01–V11 **456/456** e V00 **12/12**; validador **3 falhas / 0 avisos** apenas por métricas antigas no README raiz (`markdown 222`, `Python AST 221`, `repo identidade 1409`). Escopo ficou `SKIP` por consequência.

### `34901776770`
Head `8785822e045edf158f04ea41ea0f6c059ef11cb1`: o novo teste de import pelo namespace funcionou, mas o oráculo esperava `legado_notebook` em vez do ID canônico `hub-legado-notebook`. Resultado: **20/21 PASS**, 1 failure de teste; etapas posteriores ficaram `SKIP`. A correção alterou somente essa expectativa e preservou a guarda.

### `34904363803`
Head `795edf879c6f013553afa725a02473d49c909624`: V11 **21/21**, regressões V01–V11 **457/457** e V00 **12/12** passaram. O validador reprovou com **3 falhas / 0 avisos** porque este checkpoint abreviou a base como um prefixo seguido de reticências; esse formato coincidiu com a guarda de identificador corporativo plausível, impedindo a emissão da linha `APROVADO` e fazendo o README raiz falhar por consequência. O escopo V11 ficou `SKIP`. A correção usa o SHA completo e não altera validador ou código funcional.

Nenhum desses runs é reclassificado.

## Evidências integralmente verdes

### Run `34902083889` — primeiro gate verde

No head `0d3180c50428d8716b44f264b915a91243ba96c3`:
- V11 específica: **21/21 PASS**;
- sintaxe em memória: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- escopo V11: **PASS**;
- `Contents: read` e checkout sem credenciais persistentes.

### Run `34902853430` — head documental revalidado

No head `5bb8234422fdd284a9e14815ef566ec0b52a2952`, depois da reconciliação de navegação e documentação viva, o gate completo repetiu **SUCCESS**:
- V11 específica: **21/21 PASS**;
- sintaxe em memória: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- escopo V11: **PASS**;
- source/simulado V11 equivalentes;
- workflow read-only e sem operação remota Databricks.

Métricas observadas nesse run:

```text
markdown / links   : 222 arquivos / 1395 links relativos
python (AST)       : 221 arquivos
repo (identidade)  : 1409 arquivos varridos no repositório editável/derivado
repo (links)       : 1887 links fora da raiz analisada
worktree (extras)  : 0
APROVADO            : 0 falhas / 0 avisos
```

## Gates para pedir aceite

1. suíte V11 verde — **FECHADO**;
2. regressões V01–V11 verdes — **FECHADO**;
3. V00 verde — **FECHADO**;
4. source/simulado equivalentes — **FECHADO**;
5. validador 0/0 — **FECHADO NO ÚLTIMO HEAD INTEGRALMENTE VERDE; A REVALIDAR NESTA CORREÇÃO DOCUMENTAL**;
6. escopo sem operação remota — **FECHADO NO ÚLTIMO HEAD INTEGRALMENTE VERDE; A REVALIDAR NESTA CORREÇÃO DOCUMENTAL**;
7. diff limpo/sem credenciais — **FECHADO NA AUDITORIA PRÉ-PR**;
8. documentação viva reconciliada — **FECHADO**;
9. PR real mergeável/checks verdes — **PENDENTE**;
10. aceite explícito — **PENDENTE**.

A comparação contra a base `a9480391c78e2402986885db0ce08b10e0619a1a` mostra oito commits à frente e zero atrás, com mudanças restritas à superfície AI/BI V11, seu espelho, testes/CI e documentação. O schema central e o núcleo V02 não são alterados.

## Limites de homologação

Mesmo depois dos gates Git, continuarão pendentes export/import real, admin real, snapshot/reaplicação real, browser, acessibilidade e UAT. V12 não deve iniciar antes do fechamento V11.

## Próximo passo

Reexecutar o workflow no head produzido por esta correção documental. Se continuar integralmente verde, abrir a PR V11 em **draft**, auditar mergeabilidade e todos os checks reais e então apresentar a candidata para aceite explícito. Não fazer merge nem iniciar V12 antes disso.
