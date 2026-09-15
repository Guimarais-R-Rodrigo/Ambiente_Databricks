# V12 — escopo, dependências e critérios de aceite

## Decisão canônica

A V12 é **homologação formativa de jornadas com pessoas e ambiente**. Ela não adiciona contexto `aibi`, não amplia a matriz V11, não cria engine paralelo e não fecha operação/suporte de produção.

## Classificação dos gaps herdados

| Gap | Classificação | Evidência necessária |
|---|---|---|
| `DOC-02`, `DOC-03`, `UAT-01` | V12 | pessoa autorizada, versão, tarefa, tempo observado quando aplicável e ajuda recebida |
| `A11-01` | V12 | render final observado + medição de contraste + revisão humana de leitura/teclado/zoom |
| `SEC-01` | V12, `databricks_environment` por especialização ratificada | identidade e permissão efetivas observadas no ambiente; teste local não basta |
| Visual Lab browser/runtime/persistência | V12, dependente de ambiente | workspace de teste autorizado e dados sintéticos |
| App V10 browser/identidade/isolamento | V12, dependente de ambiente | App de teste; deploy é pré-requisito mutável e exige autorização própria |
| export real de theme JSON AI/BI | V12, dependente de ambiente | bytes realmente exportados + SHA-256; export não autoriza import |
| binding revisado contra export | V12, Git/local após export | SHA exato + JSON Pointers existentes + somente `translated/direct` |
| `Import theme` em draft | V12, depende de autorização | dashboard de teste sintético + rollback + prova de preservação semântica |
| light/dark e browser AI/BI | V12 | observação real no draft |
| workspace theme, herança, snapshot e reaplicação | V12 condicional de ambiente | admin + workspace de teste + autorização específica; publicação, se necessária ao roteiro oficial, é gate próprio |
| deploy/rollback recorrente, suporte e custos | V13/V14 | operação sustentada, não requisito para o protocolo local V12 |
| production readiness | fora do aceite V12 | gate posterior explícito |
| publicação compartilhada | gate separado | autorização/publicador/revisão conforme V01 |

## Ratificação da especialização de `SEC-01`

A matriz canônica da V01 marca `SEC-01` com `human_required: true` e `human_status: "PENDENTE"`. A V12 trata o caso como `databricks_environment`. Essa divergência era real e não estava registrada em lugar nenhum; fica ratificada aqui.

O fundamento é o próprio oráculo da V01, que determina que **"só ambiente real comprova autorização efetiva"**. Identidade e permissão efetivas são propriedades do ambiente, não da compreensão de um participante: nenhuma pessoa, por mais autorizada que seja, torna verdadeira uma permissão que o workspace não concede. Por isso a classe correta para `SEC-01` é `databricks_environment`.

Termos exatos da ratificação, declarados em `matriz_homologacao.json` sob `cases[SEC-01].v01_specialization` e cobertos por teste:

- a V01 **não é editada**: `alters_v01: false`, e o teste `test_sec01_specialization_is_ratified_in_v12_without_touching_v01` falha se `matriz_testes.json` deixar de declarar `human_required: true` e `human_status: "PENDENTE"` para `SEC-01`;
- a especialização vale **somente** para `SEC-01`. `DOC-02`, `DOC-03`, `A11-01` e `UAT-01` continuam `human_uat` e continuam exigindo participante real autorizado — o teste `test_specialization_does_not_leak_to_the_other_human_cases` impede o contágio;
- a especialização **não reduz** exigência: `SEC-01` ganhou dois fatos obrigatórios que a V01 não pedia — `self_declared_role_used` e `identity_bytes_versioned`, ambos obrigatoriamente `false`.

Um `PASS` ambiental de `SEC-01` continua não provando `DOC-02`, `DOC-03`, `A11-01` nem `UAT-01`, e continua não sendo aceite humano de nada.

## Critérios Git/local

Uma candidata V12 só pode avançar para homologação real quando:

- matriz e protocolo carregam sem erro;
- suíte V12 e mutantes negativos passam;
- regressões V01–V12 passam;
- V00 passa;
- validador estrutural/documental passa;
- workflow V12 é read-only, sem credenciais Databricks;
- diff não altera runtime `.assistant` fora de decisão explícita;
- não há segredo, identidade real, PII ou path corporativo;
- V11 conserva 48 tokens, 3/23/22 e somente três bindings diretos.

## Critérios de ambiente

`PASS` de ambiente exige execução real e registro do commit, data/hora, classe de ambiente sanitizada, autorização, identidade/permissão quando pertinente, dados sintéticos, evidência sanitizada e rollback verificado para mutações.

No AI/BI:

- o export revisado e o usado precisam ter o mesmo SHA-256;
- o binder V11 continua limitado a campos já existentes e `translated/direct`;
- `dashboard_sintetico.json` nunca é entrada Databricks;
- `approximated` e `unsupported` não podem ser automatizados;
- datasets, queries, filtros e semântica dos widgets precisam ser invariantes;
- `Import theme` é distinto de `Publish`;
- snapshot não é vínculo vivo.

## Critérios humanos/UAT

`PASS` humano exige pessoa real autorizada e observação real. Use alias sanitizado no Git; não versione nome, e-mail, username ou identificador corporativo.

A sessão deve registrar:

- versão/commit;
- tarefa;
- papel do participante;
- tempo observado quando aplicável;
- toda ajuda recebida;
- achados e falhas;
- evidência sanitizada;
- conclusão do oráculo específico.

Ajuda durante `UAT-01` não é apagada: é achado. A amostra é formativa; o repositório não autoriza inferência estatística.

## Critério de encerramento V12

V12 só pode ser declarada encerrada depois de:

1. gates Git/local verdes;
2. todos os casos V12 executáveis terem estado explícito;
3. nenhum `PASS` de ambiente sem observação real;
4. nenhum `PASS` humano sem participante real;
5. bloqueios por autorização/ambiente registrados, nunca mascarados;
6. PR funcional aceita e integrada;
7. workflows pós-merge auditados;
8. documentação viva reconciliada em PR separada quando necessário.
