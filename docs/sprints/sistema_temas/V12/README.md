# V12 — homologação de jornadas com pessoas e ambiente

## Estado

**Baseline técnico Git/local verde; homologação real ainda pendente.** A V12 parte da `main` `d106ef3158e5827a2eec3aa183dbb3b47885c960`, onde V00–V11 estão integradas. O primeiro head V12 que concluiu integralmente o workflow específico foi `c2cf064b1d1bb9983af75932b22976765df51c56`, no run `34910391401`. Qualquer commit posterior, inclusive fechamento documental, precisa de CI próprio antes de compor a candidata final da PR.

A V12 não cria um novo engine de temas e não reabre a arquitetura V11. Ela organiza e instrumenta a etapa canônica em que gaps deliberadamente deixados como “não homologados” passam a ser jornadas observáveis de **pessoa + ambiente**. CI não vira UAT, e observação em Databricks não significa “pronto para produção”.

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

## Quando usar

Use a V12 quando a pergunta depender de algo que teste local ou CI não consegue provar sozinho. Exemplos: uma pessoa consegue completar o primeiro uso sem ajuda verbal; a renderização final é legível no browser; a identidade e a permissão efetivas são as esperadas; um dashboard draft preserva queries, filtros, datasets e semântica após uma operação autorizada; ou uma configuração de workspace produz o comportamento observado que a documentação descreve.

Também use este protocolo para registrar corretamente um bloqueio. Falta de permissão, ambiente, participante, rollback ou autorização é resultado operacional válido e deve ficar como `PENDENTE` ou `BLOQUEADO_*`, nunca como `PASS` presumido.

## Quando não usar

Não use a V12 para:

- alterar tokens, paletas ou arquitetura só para facilitar a homologação;
- substituir testes unitários, regressões ou CI por uma avaliação humana;
- tratar revisão do autor como UAT independente;
- usar fixture sintético como se fosse artefato nativo do Databricks;
- automatizar capacidades V11 classificadas como `approximated` ou `unsupported`;
- transformar importação/configuração em autorização de publicação;
- declarar produção pronta apenas porque uma jornada funcionou uma vez em ambiente controlado.

## Pré-requisitos

Antes de qualquer sessão de homologação, confirme:

1. caso da matriz e oráculo que será avaliado;
2. ambiente de teste autorizado e identificado sem expor dados pessoais ou corporativos;
3. dados exclusivamente sintéticos ou sanitizados conforme a política da sprint;
4. participante e papel adequados quando houver evidência humana;
5. artefatos de entrada e hashes necessários à jornada;
6. forma de coletar a evidência sem credenciais, segredos ou PII;
7. rollback ou saída segura, quando houver possibilidade de mutação;
8. autorização explícita adicional se a próxima ação modificar Databricks real.

Sem esses pré-requisitos, não avance para a mutação.

## Passo a passo operacional

1. Localize o caso em `matriz_homologacao.json` e leia seu oráculo.
2. Execute primeiro os gates Git/local descritos abaixo. Falha local bloqueia a sessão de ambiente.
3. Classifique a evidência que deseja produzir como Git/local, Databricks environment ou Human/UAT.
4. Se a jornada puder ser apenas observacional, prepare o ambiente e registre identidade, versão, browser/runtime e artefatos relevantes.
5. Se houver qualquer mutação real, pare antes da ação e registre operação, ambiente, risco, rollback, evidência esperada e referência da autorização explícita.
6. Execute exatamente a jornada prevista em [PROTOCOLO_HOMOLOGACAO.md](PROTOCOLO_HOMOLOGACAO.md), sem ampliar escopo durante a sessão.
7. Preserve os artefatos exigidos, incluindo SHA-256 quando aplicável, e registre resultado, ajuda recebida, duração observada e observações humanas quando o caso exigir.
8. Valide o registro com `tools/temas_v12_homologacao.py`. O validador deve falhar fechado diante de evidência incompleta ou incoerente.
9. Marque `PASS` somente quando o oráculo estiver explicitamente satisfeito pela classe correta de evidência.
10. Em caso de erro ou ambiguidade, interrompa a jornada, execute o rollback previsto se necessário e registre o estado real.

## Resultado esperado e como saber se funcionou

O resultado esperado depende da classe de evidência:

| Classe | Sinal de sucesso | O que continua não provado |
|---|---|---|
| Git/local | suíte, regressões, V00, validador e gate de escopo/higiene verdes no mesmo head | comportamento real Databricks e compreensão humana |
| Databricks environment | jornada realmente observada no ambiente autorizado, com artefatos e oráculo satisfeitos | UAT e representatividade de usuários |
| Human/UAT | participante autorizado executa a jornada e satisfaz o oráculo documentado | autorização administrativa, deploy, produção ou generalização estatística |

Estados como “revisado por mantenedor”, “testado por administrador”, “testado por usuário técnico”, “testado por usuário não técnico”, “UAT aprovado”, “acessibilidade avaliada”, “pronto para produção” e “publicado” não são sinônimos. Cada um exige evidência própria.

## Erros comuns

Os erros que devem interromper ou invalidar a homologação incluem:

- usar CI como evidência de UAT;
- marcar tempo estimado como duração observada;
- aceitar participante não autorizado como prova humana;
- usar export AI/BI diferente daquele cujo SHA-256 foi revisado;
- tentar criar JSON Pointer ou campo nativo inexistente;
- alterar query, filtro, dataset ou semântica do widget durante a jornada;
- automatizar token `approximated` ou `unsupported`;
- publicar acidentalmente um dashboard ao testar tema;
- interpretar snapshot de workspace theme como vínculo vivo;
- prosseguir sem rollback ou sem autorização específica para a mutação;
- usar dado real/corporativo para produzir evidência de teste.

## O que é automatizado e o que depende de humano

A automação V12 verifica formato e coerência das evidências, hashes, contratos V11 preservados, cenários negativos, regressões e ausência de ações remotas no CI. Ela **não** executa uma pessoa, não abre browser Databricks, não concede permissão administrativa e não transforma um ambiente não autorizado em ambiente de teste.

Observação de render, permissões efetivas, comportamento de draft/publicação, acessibilidade e UAT dependem de ambiente e/ou pessoa apropriados. O resultado humano continua humano mesmo que o arquivo de evidência seja validado automaticamente depois.

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

## Limitações e o que ainda não foi homologado

O estado Git/local verde não homologa browser/runtime Databricks, deploy do App V10, export/import real AI/BI, permissões administrativas, workspace theme, snapshot/reaplicação, preservação real de queries/filtros/datasets, light/dark real, acessibilidade em render final nem os cinco casos humanos da V01.

Esses itens só mudam de estado quando a respectiva evidência real existir. Ausência de execução não é failure do produto, mas também não é `PASS`.

## Gates Git/local

Execute:

```bash
python -B tools/tests/test_temas_v12.py -v
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Para critérios e classificação dos gaps, use [ESCOPO_E_ACEITE.md](ESCOPO_E_ACEITE.md).

## Saída segura e rollback

Se faltar autorização, ambiente, identidade, rollback, evidência ou pessoa apropriada, registre `BLOQUEADO_*` ou `PENDENTE` e encerre a sessão sem fabricar resultado.

Se uma mutação autorizada já tiver ocorrido e o oráculo falhar, execute somente o rollback que foi registrado **antes** da operação. Se o rollback não estiver disponível ou não puder ser confirmado, interrompa novas ações e registre o estado como bloqueado até revisão humana.