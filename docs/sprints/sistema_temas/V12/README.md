# V12 — homologação de jornadas com pessoas e ambiente

## Estado

**Candidata em preparação.** A V12 começa na `main` `d106ef3158e5827a2eec3aa183dbb3b47885c960`, onde V00–V11 já estão integradas. Esta sprint não cria um novo engine de tema nem reabre a arquitetura V11.

A V12 é a etapa canônica em que os gaps deliberadamente deixados como “não homologados” passam a ser organizados como jornadas observáveis de **pessoa + ambiente**. Ela não transforma CI em UAT e não transforma uma observação no Databricks em “pronto para produção”.

## Fonte canônica recuperada

A V01 determina que **“V12 testa jornadas com pessoas; V13/V14 consolidam operação e suporte”**. A matriz V01 mantém cinco cenários humanos/ambientais pendentes: `DOC-02`, `DOC-03`, `A11-01`, `SEC-01` e `UAT-01`. V05, V10 e V11 acumulam os pré-requisitos de ambiente necessários para repetir essas jornadas em superfícies reais.

O repositório não fixa tamanho estatístico para a amostra formativa. Portanto a V12 registra toda sessão executada e não inventa `n`, representatividade ou SLA. A meta de 60 segundos de `DOC-02` e a meta exploratória de p95 da prévia permanecem medições candidatas até decisão explícita.

## O que é

A V12 acrescenta uma camada de **protocolo e evidência**, não uma nova camada de tema:

- matriz canônica de casos e fronteiras;
- protocolo para ambiente Databricks e para UAT;
- validador local `tools/temas_v12_homologacao.py`;
- testes negativos para impedir falso `PASS`;
- workflow GitHub Actions read-only;
- registros de ambiente/humano somente quando realmente executados.

## Classes de evidência

| Classe | Pode provar | Não pode provar |
|---|---|---|
| Git/local | contrato, parser de evidência, regressões, CI, hashes, higiene e escopo | comportamento real Databricks ou UAT |
| Databricks environment | comportamento observado naquele workspace/browser/identidade autorizados | compreensão de usuário ou representatividade |
| Human/UAT | execução e compreensão observadas por pessoa autorizada | autorização administrativa, deploy ou produção |

Estados como “revisado por mantenedor”, “testado por administrador”, “testado por usuário técnico”, “testado por usuário não técnico”, “UAT aprovado”, “acessibilidade avaliada”, “pronto para produção” e “publicado” não são sinônimos. Cada um exige evidência própria.

## Escopo V12

A V12 cobre:

1. documentação/primeiro uso (`DOC-02`, `DOC-03`);
2. render final e acessibilidade (`A11-01`);
3. identidade/permissões efetivas (`SEC-01`);
4. primeiro uso sem ajuda verbal (`UAT-01`);
5. Visual Lab real quando houver ambiente autorizado;
6. App V10 real quando houver deploy de teste explicitamente autorizado;
7. AI/BI V11 em dashboard draft real, incluindo export SHA-256, binding revisado, import, light/dark e preservação semântica;
8. workspace theme/snapshot/reaplicação somente em workspace de teste e com autorização administrativa específica.

Operação recorrente, suporte, custos/retention operacionais e readiness de produção ficam para V13/V14 ou gates posteriores.

## O que não é autorizado por esta candidata

A existência destes documentos **não autoriza**:

- deploy de Databricks App;
- criação ou alteração de dashboard;
- `Import theme`;
- mudança de workspace theme;
- ACL/grupos;
- publicação de dashboard;
- compute ou recurso pago;
- dados reais/corporativos.

Antes da primeira mutação real, a execução deve parar e obter autorização explícita para operação, ambiente, risco, rollback e evidência esperada.

## Próxima ação

Para preparar Git/local, execute:

```bash
python -B tools/tests/test_temas_v12.py -v
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Para homologação real, leia [PROTOCOLO_HOMOLOGACAO.md](PROTOCOLO_HOMOLOGACAO.md). Para os critérios e a classificação dos gaps, use [ESCOPO_E_ACEITE.md](ESCOPO_E_ACEITE.md).

## Saída segura

Se faltar autorização, ambiente, identidade, rollback, evidência ou pessoa apropriada, registre `BLOQUEADO_*` ou `PENDENTE`. Não converta o bloqueio em `PASS`.
