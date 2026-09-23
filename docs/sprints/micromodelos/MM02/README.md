# MM02 — spec fingerprint

## Estado

```text
MM02 = EM_IMPLEMENTACAO
BASE_MAIN = 86d1ff6a52d8ef03f6d5567afed6897c1b96c8c3
BRANCH = micromodelos/mm02-spec-fingerprint
LOCAL_EXECUTION = NOT_RUN
CANDIDATE_FREEZE = NOT_REACHED
```

A MM02 implementa exclusivamente o **fingerprint semântico da especificação material** de um micromodelo já válido segundo o contrato MM01.

Não cria skill, prompt, crawler, tracking, publicação, acesso a Databricks ou segunda autoridade semântica.

## Autoridades consumidas

A sprint parte de:

- `PLANO_MESTRE.md`;
- `REVISAO_PLANO_POS_SEF_2026-09-23.md`;
- `PROTOCOLO_CERTIFICACAO_SPRINTS.md`;
- ADR-0014 a ADR-0020;
- contrato MM01 integrado;
- `MATRIZ_ACEITE_FINAL.md`;
- `tools/micromodelo_mm01_contract.py`.

O documento precisa passar integralmente por `validate_spec` da MM01 antes de receber fingerprint.

## Princípio de separação

```text
definição analítica material
        ↓
spec_fingerprint
```

é distinto de:

```text
fase / aprovação / proveniência / execução
tracking / governança / publicação institucional
```

O fingerprint não prova execução, aprovação, publicação ou homologação.

## Algoritmo

Identidade:

```text
algorithm = mm02-spec-fingerprint-v1
algorithm_version = 1.0.0
digest = SHA-256
encoding = UTF-8
serialization = JSON determinístico
```

O preimage contém explicitamente o identificador e a versão do algoritmo.

A serialização usa:

- chaves ordenadas;
- separadores JSON determinísticos;
- UTF-8 sem escaping ASCII obrigatório;
- coleções semanticamente não ordenadas canonicalizadas;
- números materiais equivalentes `70` e `70.0` com mesma representação decimal;
- equivalência editorial conservadora da MM01 apenas em textos semânticos para os quais ela é apropriada.

Não é hash bruto do YAML.

## Perfil material v1

### Entra no fingerprint

| Grupo | Conteúdo material |
|---|---|
| `schema_version` | versão estrutural do contrato interpretado |
| `negocio` | característica, definição operacional, usos pretendidos e usos proibidos |
| `entidade` | tipo, chave lógica, granularidade, população elegível e referência temporal |
| `fontes` | id, catálogo simbólico, schema, objeto, tipo, campos e papel |
| `evidencias` | id, referências de fontes e regra operacional |
| `contra_evidencias` | id, referências de fontes e regra operacional |
| `classificacao` | tipo, semântica TRUE/FALSE/INDETERMINADO, missing policy e limiares |
| `score` | habilitação, significado, escala, normalização, pesos e calibração; referências entram quando definem regra customizada/calibração |
| `saida.estudo` | nomes e valores do contrato de saída analítica |
| `saida.publicacao` | campo final e política de INDETERMINADO quando definidos |

### Não entra no fingerprint

| Grupo/campo | Motivo |
|---|---|
| `identidade.*` | nome, título, versão humana e estado não são definição analítica; ficam identificáveis separadamente |
| `negocio.objetivo` | prosa explicativa do porquê; não altera a definição operacional |
| descrições auxiliares de evidência/limiar/componente | narrativa editorial; regra/valor/peso permanecem materiais |
| qualquer `proveniencia` | prova de origem/aprovação/medição, não definição |
| `experimentos` | evidência/histórico de estudo; não altera por si a regra do micromodelo |
| `validacao` | resultado e decisão humana; governança da definição, não seu conteúdo |
| `tracking` | pertence à MM06 e às execuções |
| `governanca` | autoridade/metadata institucional separada |
| `publicacao` de topo | estado do handoff institucional, não contrato analítico |
| `saida.publicacao.estado` | estado de ciclo; os campos/política efetivos são o contrato material |

Regras condicionais de referência:
- `score.semantica_ref` é material somente para `OUTRA_APROVADA`; em semânticas estruturadas, funciona como trilha auditável;
- `score.normalizacao.referencia` é material somente para `CUSTOM_APROVADO`; nos métodos estruturados, não redefine a normalização;
- `score.calibracao.evidencia_ref` é material como ID da evidência/calibração escolhida. O conteúdo observado da run, timestamps e proveniência do experimento continuam fora do fingerprint.

A exclusão de `identidade.nome` é deliberada: o fingerprint identifica **conteúdo material**, não o nome do artefato. Dois micromodelos com definições materiais idênticas podem, portanto, compartilhar fingerprint; `identidade.nome` e `micromodel_version` continuam disponíveis separadamente.

## Canonicalização textual

A MM02 não cria equivalência semântica geral.

Para prosa normativa incluída no fingerprint, reutiliza `_normalize_editorial_text` da MM01:

1. NFKC;
2. `casefold`;
3. remoção de `Default_Ignorable_Code_Point`;
4. whitespace normalizado;
5. tolerância apenas à pontuação terminal editorial já congelada.

Identificadores operacionais, nomes de schema/objeto/campo, IDs, enums e referências continuam exatos.

## Canonicalização de coleções

A ordem serial não é identidade quando o contrato não lhe atribui significado:

- `fontes`, evidências, contra-evidências, limiares e componentes: ordenados por `id`;
- `fontes[].campos` e `fontes_ref`: ordenados;
- listas de usos pretendidos/proibidos: normalizadas e ordenadas.

Duplicidades e referências inválidas continuam responsabilidade fail-closed da MM01.

## Fronteiras

MM02 não:

- modifica o schema MM01;
- modifica R01–R08;
- cria `hub-ml-micromodelos`;
- cria prompt;
- acessa catálogo real;
- lê registros;
- executa MLflow;
- cria Receipt;
- aprova especificação;
- publica;
- grava fingerprint dentro do YAML nesta sprint.

A integração do fingerprint com tracking será tratada somente no gate `MM06_EVIDENCE_MODEL`.

## Implementação

- `tools/micromodelo_mm02_fingerprint.py`: implementação read-only;
- `tools/tests/test_micromodelo_mm02_fingerprint.py`: regressões e testes metamórficos;
- fixture válida MM01 é reutilizada; não existe dado real.

## Próximo gate

A candidata ainda não está congelada.

Antes de qualquer FULL:

1. executar a suíte MM02 local;
2. executar regressões MM01;
3. executar CLI positiva da MM02;
4. validar documentação/snapshot;
5. reconfirmar `main`, merge-base e `behind_by=0`;
6. só então decidir a composição proporcional da certificação MM02.

Nenhum PASS local foi atribuído nesta etapa repo-side.
