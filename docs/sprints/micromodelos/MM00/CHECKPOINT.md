# MM00 — Checkpoint

## Estado

**EM EXECUÇÃO — NÃO AUTORIZA MM01.**

Este arquivo é atualizado somente com evidência observada. Não converter pendência em PASS por intenção.

## Baseline

- Base inicial: `1b6632194f4b25afc09960c27b069c16df365ee6`.
- Branch: `micromodelos/mm00-baseline`.
- PR: #43, em draft.
- Sistema de Temas na `main`: V00–V07 integradas.
- Durante a MM00 foi identificada a PR draft #42 para V08 em trabalho paralelo; V08 não está integrada na `main` e a MM00 não presume seu resultado.
- A `main` foi reconsultada durante a execução e permanecia no SHA de base.

## Entregas

| Entrega | Estado |
|---|---|
| Plano Mestre | versionado |
| README da iniciativa | versionado |
| README MM00 | versionado |
| Inventário | versionado |
| Matriz de reuso | versionado |
| Matriz de riscos | versionado |
| Dependências | versionado |
| Testes | versionado e atualizado |
| ADR-0014 a ADR-0020 | versionados como **Propostos** |
| Índice de ADRs | atualizado |
| Índice de sprints | atualizado |
| `CLAUDE.md` | reconciliado com V07 e MM00 proposta; correção adicional de wording V08 pendente |
| Pacote da auditoria A1 | preparado e versionado |
| CI da PR | V00/V01/V02 verdes; CI geral vermelho por validação documental |
| Auditoria A1 independente | **não executada** |
| Entrada `CHANGELOG.md` | pendente |
| Reconciliação final com `main` | pendente no fechamento |

## Achados materiais

### A01 — estado visual avançou

A `main` contém V07 integrada. Existe uma PR draft V08 em evolução paralela; por isso a MM00 não deve usar “V08 não iniciada” como estado global. A integração visual definitiva dos micromodelos continua adiada e será reavaliada em MM11 contra o estado então vigente.

### A02 — contexto canônico estava desatualizado — PARCIALMENTE CORRIGIDO

O `CLAUDE.md` descrevia V05 como candidata e foi atualizado para V07. Depois, a descoberta da PR draft #42 mostrou que a frase “V08 ainda não foi iniciada” também precisava ser refinada. A correção final deve dizer apenas que V08 ainda não está integrada na `main` e há trabalho paralelo em draft.

### A03 — sanitização dos nomes externos

O framework precisa conhecer semanticamente o catálogo corporativo de Produtos de Dados, mas o repositório não deve guardar nomes/paths reais do ambiente externo. Documentos versionados usam `<CATALOGO_PRODUTO>` e outros placeholders.

O primeiro CI encontrou ainda um handle corporativo histórico no ADR-0017; ele foi removido e substituído por descrição genérica do handoff externo. Novo CI deve confirmar a correção.

### A04 — não há artefato de micromodelo versionado

Busca na `main` não encontrou implementação/documentação específica com `micromodel`. MM00 inaugura a iniciativa no repositório; isso não afirma inexistência de micromodelos no ambiente de trabalho.

### A05 — auditoria independente é um gate real

A sessão implementadora preparou `01_contexto.md` e `02_prompt_auditoria.md`, mas não marcou a auditoria como executada. O parecer precisa vir de sessão independente antes do fechamento, salvo exceção humana explícita registrada.

### A06 — changelog canônico ainda não foi atualizado

A regra do projeto exige entrada em `CHANGELOG.md` para a sessão. A atualização precisa ser estritamente aditiva e preservar o histórico.

### A07 — CI geral detectou deriva documental real

No head `5adcac3291ace7a9bcad5ef6201b75e4093d6cd4`, V00, V01 e V02 passaram; o CI geral `34871695827` falhou apenas na etapa `validacao`. O validador mediu `1363` arquivos e `1858` links fora da raiz, enquanto o README raiz ainda registrava `1345`/`1850`. Também detectou o handle do ADR-0017. Nenhum gate foi relaxado. O README raiz deve ser reconciliado com a saída medida e os checks repetidos.

## Evidência de escopo

A comparação da PR contra a base confirmou que os commits da MM00 alteram documentação/ADRs e `CLAUDE.md`; nenhum arquivo em `ambiente_fonte/.assistant/`, `tools/` ou workflows faz parte da mudança funcional. Revalidar após qualquer commit adicional.

## Bloqueios para aceite

1. corrigir o wording de V08 no contexto canônico;
2. reconciliar o bloco de saída do `README.md` raiz com a execução real sem relaxar o validador;
3. registrar entrada aditiva da MM00 no `CHANGELOG.md`;
4. obter checks verdes no head final;
5. executar auditoria A1 independente;
6. verificar cada achado e corrigir o que proceder;
7. reexecutar checks após correções, se houver;
8. reconciliar novamente com `main` e com a frente V08 paralela;
9. atualizar este checkpoint para candidato a aceite;
10. obter aceite explícito de Rodrigo.

## O que o aceite da MM00 autorizará

Somente iniciar MM01 — contrato canônico `micromodelo.yaml`.

Não autoriza metadata real, mudança em helper compartilhado, piloto corporativo, publicação, visual definitivo ou migração de legado.
