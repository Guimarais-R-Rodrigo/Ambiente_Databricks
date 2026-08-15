# Contexto da auditoria — módulos novos da biblioteca

Data: 2026-08-14 · Nível: **A2_strict** (3 modelos) · Solicitante: Rodrigo

## Por que A2

O material é código analítico destinado ao workspace do trabalho, onde opera
sobre dados reais de CRM bancário e alimenta decisão de crédito. Dois dos
módulos implementam operações cujo erro é **silencioso**: uma junção temporal
mal feita produz vazamento que só aparece quando o modelo fracassa em produção,
e um join com multiplicidade não percebida infla a base de treino sem alterar
nenhuma mensagem de erro.

## Escopo

| Item | Arquivo |
|---|---|
| Junção point-in-time | `ambiente_fonte/.assistant/x_snippets/spark/pit_join.py` |
| Diagnóstico de join | `ambiente_fonte/.assistant/x_snippets/spark/join_diagnostics.py` |
| Fixtures sintéticas | `ambiente_fonte/.assistant/x_snippets/testing/fixtures.py` |
| Registro governado | `ambiente_fonte/.assistant/x_snippets/ml/mlflow_run.py` |
| Correção aplicada | `ambiente_fonte/.assistant/x_snippets/ml/lgbm_ranker.py` |
| Declarações nas skills | `skills/rodrigo-feature-engineering`, `skills/rodrigo-cross-eda-ml` |
| Catálogo | `x_docs/catalogo_helpers.md` |

Fora de escopo: os 25 módulos anteriores não alterados, a documentação já
auditada em rodadas anteriores e a decisão sobre remover módulos, que depende do
fecho do sprint 0.

## Papéis

Quem implementou não avalia o próprio trabalho. O Claude escreveu os módulos e
sai do papel de auditor; entrega o pacote e responde a questionamentos.

| IA | Papel | Foco |
|---|---|---|
| Codex | Auditoria de implementação | Assinaturas, casos de borda, tipos, aderência ao catálogo e ao padrão dos demais helpers |
| Gemini | Confronto com fonte externa | `pit_join` e `join_diagnostics` contra literatura de as-of join e documentação oficial da plataforma |
| Claude | Implementador | Responde, corrige o que for aceito, não pontua |

## O que já foi verificado (e não precisa ser refeito)

Execução em compute serverless, Spark 4.1, 2026-08-14 — 11 aprovações, nenhuma
falha (`docs/testes/spark/resultados/2026-08-14_modulos_novos.json`):

- nenhuma feature publicada após a decisão sobrevive ao `pit_join`, conferido
  por dois critérios independentes — a marca da fixture e a invariante
  `feature_ts + atraso <= decisão`;
- fator de expansão medido contra multiplicidade conhecida: 1:1 devolve 1,0 e
  1:N controlado devolve 2,0;
- fixtures determinísticas e incidência de safra crescente com o MOB;
- `lgbm_ranker` volta a calcular NDCG em todos os grupos após a correção.

A auditoria deve procurar o que o teste **não** cobre, não repetir o que ele já
provou.

## Perguntas que a auditoria precisa responder

1. O `pit_join` trata corretamente empate de `dt_referencia` para a mesma chave?
   A escolha atual é arbitrária entre versões com o mesmo instante.
2. `monotonically_increasing_id` é estável o bastante como identificador de
   linha dentro da mesma ação, ou há cenário de recomputação que o altere?
3. O `join_diagnostics` conta corretamente quando a chave é composta e uma das
   colunas é nula apenas em um dos lados?
4. A recusa do `mlflow_run` a fechar run incompleto é rigor útil ou obstáculo
   que levará as pessoas a contornar o helper?
5. Algum dos quatro módulos deveria simplesmente não existir, pelo critério de
   admissão declarado em `docs/decisions/` e no plano da biblioteca?

## Critério de bloqueio

Achado crítico ou alto impede a inclusão do módulo no runbook de replicação.
Divergência não resolvida entre auditores vira pendência com dono declarado, não
decisão por maioria. Discordância sobre comportamento da plataforma é resolvida
pela documentação oficial, conforme `.claude/rules/genie-code-oficial.md`.
