# Contexto da auditoria — módulos novos da biblioteca

> **Nomenclatura da época.** Os nomes `x_*` e `rodrigo-*` neste registro são
> os que existiam na data. A tradução para os nomes atuais está na tabela de
> correspondência do [ADR-0006](../../decisions/ADR-0006-identidade-hub.md);
> este documento não é reescrito porque descreve o que foi observado, não o
> estado atual.

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

## Perguntas já tratadas antes da auditoria

Três das cinco perguntas originais eram fragilidades reais e foram corrigidas
pelo implementador antes de submeter o material. Ficam registradas porque a
correção também merece revisão.

1. **Empate de instante no `pit_join`** — era mesmo indeterminado: duas versões
   publicadas no mesmo instante deixavam a escolha a cargo do plano de execução,
   e o mesmo código podia devolver resultados diferentes entre execuções. Agora
   há desempate determinístico pelos valores trazidos, e o diagnóstico reporta
   `linhas_com_empate_de_instante`, já que empate normalmente indica duplicidade
   na fonte. Verificado com três execuções consecutivas devolvendo o mesmo valor.
2. **`monotonically_increasing_id`** — a preocupação procedia, e o identificador
   sintético foi **eliminado**. A resolução passou a ser feita por par
   (chave, instante de decisão) distinto, com junção de volta aos fatos. O
   desenho novo também trata corretamente duas decisões da mesma entidade no
   mesmo instante, que antes disputavam a mesma partição de janela.
3. **Chave composta com nulo em um só lado no `join_diagnostics`** — conferido:
   linhas com qualquer componente nulo são excluídas da análise de casamento e
   contabilizadas à parte, o que corresponde ao comportamento real do join em
   SQL. Sem alteração.

Na correção da pergunta 2 surgiu um defeito adicional, também já resolvido: a
junção de volta aos fatos gerava `AMBIGUOUS_COLUMN_REFERENCE`, porque a tabela
resolvida descende da própria base de fatos. As colunas de junção passaram a ser
renomeadas antes da volta.

Estado após as correções: **13 verificações, nenhuma falha**.

## Perguntas em aberto para a auditoria

1. A recusa do `mlflow_run` a fechar run incompleto é rigor útil ou obstáculo
   que levará as pessoas a contornar o helper?
2. Algum dos quatro módulos deveria simplesmente não existir, pelo critério de
   admissão declarado no plano da biblioteca?
3. O desempate por ordem crescente dos valores trazidos é a convenção certa, ou
   seria preferível falhar diante de empate em vez de escolher?
4. O `pit_join` assume que `ts_feature` é o instante de referência do dado e que
   o atraso é constante por fonte. Fontes com atraso variável — por evento, por
   entidade — ficam fora do contrato. Isso é limitação aceitável ou lacuna?
5. O que os testes atuais **não** cobrem e deveria ser coberto antes de o
   material ir para o workspace do trabalho?

## Critério de bloqueio

Achado crítico ou alto impede a inclusão do módulo no runbook de replicação.
Divergência não resolvida entre auditores vira pendência com dono declarado, não
decisão por maioria. Discordância sobre comportamento da plataforma é resolvida
pela documentação oficial, conforme `.claude/rules/genie-code-oficial.md`.
