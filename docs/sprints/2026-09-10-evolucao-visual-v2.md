# Execução da evolução visual v2

## Escopo aprovado

A fundação da Sprint 0 definiu 21 contratos semânticos e cinco assinaturas
aprovadas pelo usuário. Em seguida, dois cabeçalhos foram aprovados: CRM e
Squad Modelos Analíticos e Preditivos. Esta rodada integra essa direção aos
documentos ativos, sem reescrever sua organização editorial.

Este é o plano da evolução v2, posterior à primeira rodada descrita em
`2026-09-10-readmes-visuais.md`. Não reabre a aprovação estética da Sprint 0.

## Arquitetura e responsabilidade

`ambiente_fonte/.assistant/hub_readmes_visual_assets/` permanece o proprietário
único dos assets ativos. O nome solicitado pelo usuário é preservado.

- `readmes/<familia>/sources/` e `png/`: diagramas exatos, por consumidor.
- `headers/src/` e `headers/png/`: arte-base, texto editável e cabeçalhos
  compartilhados entre READMEs e notebooks. Um arquivo CRM, não cópias por uso.
- `specs/` e `visual_system/`: contratos, linguagem gráfica e tokens.
- `licenses/`: avisos de licença das dependências visuais.
- `manifest.yaml` e `qa/`: inventário ativo, proveniência e verificações.
- `tools/readme_visuals/`: composição determinística e validação.

O pacote não depende de `READMEs_refeitos/` para carregar uma imagem. Essa pasta
preserva protótipos e baseline, como histórico de avaliação. O espelho continua
sendo gerado pela ferramenta canônica. Nenhum arquivo derivado é editado à mão.

## Sequência de integração

Preparação de módulos independentes pode ocorrer em paralelo. Promoção dos
READMEs e conclusão dos gates seguem a ordem abaixo.

| Sprint | Documentos | Figuras e trabalho específico |
|---|---|---|
| 1 — Topo | raiz e `.assistant/README.md` | preservar atlas e duas rotas aprovados; criar corte arquitetural, pista de sete gates, bússola e confluência de contexto; compartilhar a mesma confluência nos dois consumidores; integrar CRM e explicar arquitetura dos assets |
| 2 — Snippets | `hub_snippets/README.md` | anatomia explodida, paisagem de seis categorias, jornada de quatro passos e ponte de reuso; preservar imports, catálogos e limites |
| 3 — Scripts | `hub_scripts/README.md` | preservar bancada aprovada; anatomia, panorama heterogêneo de retornos, zonas de responsabilidade e estados irmãos de data_quality_check; não generalizar status ou bloqueios |
| 4 — Skills | `skills/README.md` | preservar dossiê aprovado; rotas relevância/@ e corte método/runtime; frontmatter dentro de SKILL.md e recursos opcionais; não alterar skills executáveis |
| 5 — Prompts | `hub_prompts/README.md` | preservar blueprint aprovado; roteador de quatro famílias e storyboard de cinco etapas; manter campos, exemplos e critérios copiáveis |
| Encerramento | conjunto | revisão cruzada, auditoria global, integração dos headers, consistência de links/manifestos, validação local, espelho e publicação com conferência |

## Critérios contra deriva

1. Cada figura responde à pergunta de seu contrato; não inventar capacidades,
   dados de execução, retorno universal ou passagem automática de contexto a runtime.
2. Preservar tópicos, subtópicos, códigos e catálogos. Corrigir afirmações falsas
   e acrescentar explicações; não substituir a narrativa por um novo README.
3. Preservar os PNGs aprovados byte a byte. O texto dos headers é exato e não
   contém a palavra rejeitada pelo usuário. O acabamento raster é reservado à
   identidade de cabeçalho; os diagramas permanecem informativos e determinísticos.
4. Nenhuma decisão codificada ou histórico de migração entre ambientes é inserido
   nos READMEs destinados à equipe. Governança interna permanece em `docs/`.
5. Cor não é o único canal. Rótulos, formas, legendas e texto equivalente mantêm
   acessibilidade e contexto textual para Genie Code.
6. A referência de fonte efetiva é 14 px em imagens exibidas a 720 px, sem
   colisões de texto. Revisão visual humana/independente complementa os checks.
7. PNGs antigos só deixam o pacote ativo após conferência de referências e
   preservação no baseline; não apagar protótipos ou outras alterações locais.

## Gates e evidências

- Contratos/IDs e consumidores resolvidos; todos os ativos referenciados.
- Hashes do original e entradas, fonte Inter fixa e ícones licenciados.
- Dimensões, integridade, ausência de dependências remotas, limites, contraste,
  fonte reduzida, ausência de colisões e inspeção de todas as figuras.
- Preservação dos títulos e exemplos; âncoras antigas continuam válidas e as
  ASCII são adicionadas sem quebrar links existentes.
- `tools/validate_assistant.py`, testes proporcionais e render canônico.
- Dry-run de publicação, escrita autorizada via CLI e comparação remota de
  inventário, tipo e conteúdo. Sem compute ou chat por reflexo de alteração visual.
- Inspeção da renderização no workspace e registro dos limites que restarem.

## Fontes de plataforma revisadas nesta rodada

- [Agent Skills](https://docs.databricks.com/aws/en/genie-code/skills).
- [Instruções](https://docs.databricks.com/aws/en/genie-code/instructions).
- [Contexto e imagens para Genie Code](https://docs.databricks.com/aws/en/genie-code/tips).
- [Política de aprovação do modo agente](https://docs.databricks.com/aws/en/genie-code/agent-mode).
- [Imagens em Markdown de notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-media).

Estas páginas sustentam as afirmações de plataforma, não certificam a execução
de helpers nem a renderização de cada PNG. A evidência de cada teste será registrada
ao concluir, sem declarar resultado antes de executar.
