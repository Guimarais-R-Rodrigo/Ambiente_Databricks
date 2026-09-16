# ADR-0021 — Contrato verificável de execução de Agent Skills

Data: 2026-09-16
Status: Aceito
Autor: ChatGPT

## Contexto

A SE00 do Skill Enforcement Framework mediu o comportamento pré-enforcement da
`hub-ml-eda-profissional` em 16 runs. Nos 12 executores EDA, nenhum helper
aplicável foi concluído (`0/69`), nenhum consumo de template foi comprovado
(`0/48`), houve 67 reimplementações manuais e as três tentativas adversariais
aceitaram bypass do contrato. As quatro auditorias A1 também falharam como fonte
única de conformidade: nenhuma produziu state ladder completo.

O ADR-0004 continua válido ao exigir declaração explícita dos helpers nas
skills. A SE00 demonstrou, porém, que declaração textual é orientação e não
evidência de resolução, import, chamada ou conclusão.

A documentação vigente do Databricks para Genie Code Agent Skills permite
recursos relativos à raiz da skill, incluindo scripts com código executável.
Essa capacidade precisa ser confirmada no laboratório Free antes que preflight
ou runner sejam projetados sobre ela.

## Verificação da superfície suportada

Em 2026-09-16, a documentação oficial vigente de Genie Code Agent Skills foi
reverificada. Ela afirma que skills podem incluir scripts com código executável,
arquivos adicionais e referências por caminhos relativos à raiz da skill. A
mesma documentação recomenda separar orientação em Markdown de automação
repetível em scripts.

Essa evidência confirma que o capability probe usa uma superfície oficialmente
suportada. Ela **não** comprova que a Genie Code executará um script relativo de
forma previsível no fluxo específico deste Hub; essa previsibilidade continua
sendo hipótese experimental e só pode ser homologada pelo teste real no
Databricks Free, em chat novo.

## Decisão

1. Introduzir um arquivo adjacente `execution_contract.json` nas skills que
   aderirem ao SEF.
2. Iniciar o schema em `0.1`, em JSON declarativo, sem expressão arbitrária
   executável e com versionamento explícito.
3. Manter o frontmatter de `SKILL.md` limitado a `name` e `description`; o
   contrato estruturado não será embutido no frontmatter.
4. Representar recursos com `id`, `module`, `symbol`, `policy`, `evidence` e,
   somente quando `policy=conditional`, uma condição de vocabulário fechado.
5. Admitir em `0.1` as políticas `required`, `conditional` e `optional`.
6. Resolver helpers estaticamente contra a fachada pública `__init__.py` da
   pasta de objeto. A simples existência de um arquivo interno não satisfaz o
   contrato.
7. Resolver templates como paths Markdown relativos à raiz da skill e recusar
   traversal (`..`), paths absolutos e destinos ausentes.
8. Operar a SE01 exclusivamente em `mode="audit"`. O contrato descreve e é
   validável, mas ainda não bloqueia a EDA e não autoriza a palavra
   “enforcement”.
9. Não copiar implementações de helpers para dentro da skill. Scripts da skill
   devem ser orquestradores finos sobre APIs públicas canônicas.
10. Executar um capability probe read-only no Databricks Free para comprovar,
    no Genie Code real, que um script relativo consegue localizar `.assistant`,
    importar uma API pública e retornar marcador estruturado.
11. Não definir a arquitetura definitiva de preflight/runner antes do resultado
    desse probe. SE02 e SE03 ficam explicitamente fora desta decisão.

## Alternativas consideradas

- **Somente reforçar o texto de `SKILL.md`.** Rejeitada porque a SE00 já
  demonstrou 0% de helper adherence mesmo com recursos declarados.
- **Adicionar metadados ao frontmatter.** Rejeitada nesta etapa para preservar a
  superfície conservadora já adotada e evitar acoplar contrato experimental ao
  mecanismo de descoberta da plataforma.
- **Permitir condição Python/expressão livre no JSON.** Rejeitada por criar
  execução arbitrária dentro do que deve ser validável estaticamente.
- **Validar fazendo import dos helpers.** Rejeitada porque validação estática não
  deve executar dependências opcionais, Spark ou efeitos colaterais para
  descobrir a API.
- **Ir diretamente para preflight/runner.** Rejeitada porque a previsibilidade de
  scripts relativos ainda precisa de evidência no Genie Code real.

## Consequências

- O projeto passa a ter uma fonte machine-readable da obrigação de execução sem
  substituir o `SKILL.md` como guia humano/LLM.
- Contratos quebrados podem ser recusados antes da publicação.
- A política `audit` evita confundir SE01 com enforcement real.
- O vocabulário de condições precisará evoluir por versão quando surgirem casos
  objetivos novos.
- O validador depende da disciplina de API pública das pastas de objeto; símbolos
  internos não exportados são deliberadamente inválidos.
- O resultado do capability probe poderá confirmar ou alterar a estrutura
  prevista para SE02/SE03 sem reescrever esta evidência histórica.

## Resultado experimental da SE01 — registro append-only

Em 16/09/2026, o capability probe foi executado no Databricks pessoal/Free em
chat novo e retornou evidência observável do marcador esperado, incluindo
`assistant_root_resolved=true`, import de
`hub_snippets.constants.format_br.fmt_int`, `sample_result="1.234"`,
`status="PASS"` e `writes_performed=false`.

Esse resultado confirma a viabilidade da superfície **no cenário testado**. Ele
não demonstra execução determinística universal pelo Genie Code e não transforma
`mode="audit"` em enforcement.

Após cumprir a função experimental, o probe temporário foi conscientemente
aposentado antes da homologação da SE01:

- `scripts/capability_probe.py` foi removido da fonte e do derivado;
- a seção temporária foi removida do `SKILL.md`;
- a suíte passou a proteger essa ausência;
- a evidência histórica do experimento foi preservada em documentação;
- o contrato v0.1, schema e validador permanecem;
- preflight, runner, receipt e postflight continuam fora do escopo da SE01.

A forma definitiva dessas camadas permanece decisão de sprints posteriores e
não é antecipada por este ADR.

## Aceite humano

Em 16/09/2026, após a candidata SE01 ser reconciliada com a `main`, ficar com
`behind_by=0`, permanecer mergeável e concluir os 11 workflows aplicáveis em
`SUCCESS`, o usuário concedeu aceite explícito para homologação e integração da
SE01. Esse aceite muda o status deste ADR de **Proposto** para **Aceito**.

O aceite não amplia o escopo: `mode="audit"` permanece vigente e SE02, preflight,
runner determinístico, Execution Receipt e postflight continuam não iniciados.

## Referências

- `docs/sprints/skill_enforcement/PLANO_MESTRE.md`
- `docs/sprints/skill_enforcement/SE00/RESULTADOS.md`
- `docs/sprints/skill_enforcement/SE00/CHECKPOINT.md`
- `docs/sprints/skill_enforcement/SE01/README.md`
- `docs/sprints/skill_enforcement/SE01/RESULTADOS.md`
- `tools/skill_enforcement/execution_contract.schema.json`
- `tools/skill_enforcement/validate_contracts.py`
- `ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/execution_contract.json`
- Databricks Genie Code Agent Skills: `https://docs.databricks.com/gcp/en/genie-code/skills` (verificado em 2026-09-16)