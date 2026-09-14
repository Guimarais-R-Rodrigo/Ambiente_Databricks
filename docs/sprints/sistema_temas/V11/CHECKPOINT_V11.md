# Checkpoint V11 — temas nativos AI/BI

## Estado

**CANDIDATA FUNCIONALMENTE VERDE; RECONCILIAÇÃO DOCUMENTAL/HEAD FINAL AINDA PENDENTES; SEM ACEITE, MERGE OU HOMOLOGAÇÃO DATABRICKS.**

Base: `a9480391c78e2402986885db0ce08b10e0619a1a`.

Branch: `codex/temas-v11-aibi-20260914`.

Head funcional pós-correção: `5eca34c95fc9970f864869282f59e2bb4cc61d56`.

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

## Evidências já observadas

### `34900693160` — FAILURE preservado

Primeira composição no head `ed1fdaac22e3ceece54b6ada96427b5a8afcba95`: **19/20** na suíte V11. A única falha foi a exceção V02 escapando pela fronteira pública V11 para contexto editorial. Corrigido sem alterar V02 e sem enfraquecer o caso negativo.

### `34901091132` — FAILURE preservado

Head `5eca34c95fc9970f864869282f59e2bb4cc61d56`:
- V11: **20/20 PASS**;
- regressões V01–V11: **456/456 PASS**;
- V00: **12/12 PASS**;
- validador: **3 falhas / 0 avisos**, somente por métricas antigas no README raiz (`markdown 222`, `Python AST 221`, `repo identidade 1409` medidos);
- etapa de escopo: `SKIP` por consequência do failure do validador.

Nenhum dos dois runs é reclassificado.

## Gates para pedir aceite

1. suíte V11 verde — **FECHADO FUNCIONALMENTE; A REVALIDAR NO HEAD FINAL**;
2. regressões V01–V11 verdes — **FECHADO FUNCIONALMENTE; A REVALIDAR NO HEAD FINAL**;
3. V00 verde — **FECHADO FUNCIONALMENTE; A REVALIDAR NO HEAD FINAL**;
4. source/simulado equivalentes — **FECHADO FUNCIONALMENTE; A REVALIDAR NO HEAD FINAL**;
5. validador 0/0 — **PENDENTE DA RECONCILIAÇÃO DOCUMENTAL**;
6. diff limpo/sem credenciais — **PENDENTE DA AUDITORIA FINAL**;
7. documentação reconciliada — **EM EXECUÇÃO**;
8. PR real mergeável/checks verdes — **PENDENTE**.

## Endurecimento antes do head final

A revisão documental/técnica intermediária também:
- torna a fachada importável tanto localmente quanto via namespace do produto;
- amplia a guarda negativa para todos os módulos Python da ponte;
- atualiza somente métricas realmente medidas pelo validador.

## Limites de homologação

Mesmo depois dos gates Git, continuarão pendentes export/import real, admin real, snapshot/reaplicação real, browser, acessibilidade e UAT. V12 não deve iniciar antes do fechamento V11.
