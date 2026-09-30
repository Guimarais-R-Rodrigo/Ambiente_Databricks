# Features — lag sintético local

O perfil `FIXED_LAG_L1_V1` executa
`hub_snippets.ml.lgbm_temporal.create_temporal_features`, sem fit ou persistência.
O preflight fechado fica em `run.py::preflight`; `run.py::run` emite Receipt
e `verify.py::verify` recebe request, run_id e features esperadas independentes.

Campos exigidos: `schema_version=SER07-REQUEST-1`, profile, synthetic=true,
population_id, decision_at UTC, window_days inteiro entre 1 e 365,
requested_effect=NONE, temporal e rows. O contexto temporal exige
reference_column=event_at, availability_column=available_at, lag_kind=CONSTANT,
lag_days=1, boundary=LE, timezone=UTC, tie_break=REJECT, bitemporal=false.
Cada linha contém id, entity_id, event_at, available_at e value numérico finito
entre -1e9 e 1e9. Eventos são à meia-noite UTC, com disponibilidade um dia depois;
o grão entidade/instante e os IDs são únicos. No máximo 1.000 linhas.

A janela de eventos é inclusiva: [decision_at - window_days, decision_at].
Só entram linhas disponíveis até decision_at. O lag é a observação anterior
**dentro dessa janela elegível e da mesma entidade**, não o dia anterior.
O helper ordena as observações; warm-up sem histórico é removido.
`eligible_ids` mantém o denominador antes do warm-up; `features=[]` significa
que nenhuma linha tinha histórico suficiente, não sucesso analítico de negócio.

Exemplo completo reproduzível: fixture `_request` em
`tools/tests/test_ser07_feature_engineering.py` no repositório de desenvolvimento.
Na raiz da skill, a entrada CLI aceita:

```text
python scripts/run.py --request request.json --run-id execution-id
```

Nunca marque dados reais como sintéticos. Receipts são evidência de integridade
e vínculos, não autenticação de origem ou homologação Genie.


## Vista de features derivada do PIT Cross-EDA

scripts/run_pit_features.py::compose chama run_pit, finalize e verify_finalized
do Cross-EDA para o perfil COMPOSED_PIT_FEATURE_VIEW_V1. Só projeta
feature_value e available_at por decision_id após a prova local PASS.
scripts/run_pit_features.py::verify recebe inputs/IDs esperados externos,
revalida o Postflight upstream e compara toda a projeção. O payload inclui
prova upstream literal e linhagem de hashes/cutoff/janela/Receipt/Postflight.
Sem Receipt FE novo, fit, materialização ou prontidão de negócio. O contrato
pit_view_contract.json limita a composição ao perfil sintético.
# Materialização PIT sintética (SER08)

`run_pit_materialization.py::effect_request` recebe a view produzida por
`run_pit_features.py::compose` e os inputs externos originais. O digest desse
request compõe a autorização explícita para `execute`. A operação requer
Spark UTC, principal e namespace `workspace.default` correspondentes,
alvo pessoal novo `skills_delivery_<32 hex>` e cleanup `DROP_OWNED`.

O efeito usa o motor Delta compartilhado com Pipeline Builder, com perfil
fechado de cinco colunas. Preserva IDs texto, timestamps UTC de micros e
`feature_value` BIGINT nullable. Propriedades Delta ligam a tabela a hashes
da view, fontes, contexto, cutoff, Receipt e Postflight. O registro de efeito
separa versões observadas após primeiro MERGE e replay, hash do readback,
ID da tabela e resultado da remoção. Não executa fit nem materialização de
negócio; um `UNKNOWN` nunca autoriza retry automático.
O limite de valor aceito pelo PIT upstream continua [-1.000.000, 1.000.000];
`BIGINT` descreve o armazenamento, não amplia o domínio permitido.
