# Handoff — evolução visual v2

Data: 2026-09-10 · De: Codex · Para: próxima sessão

Integração e fechamento local retomados em 2026-09-11.

## Escopo e arquitetura

O usuário aprovou as cinco assinaturas da Sprint 0 e os cabeçalhos CRM/Squad.
A integração segue o [plano de execução](../sprints/2026-09-10-evolucao-visual-v2.md),
preservando a organização editorial dos cinco guias, com dois READMEs físicos
na sprint de topo. A fonte única dos recursos ativos é
`ambiente_databricks/.assistant/hub_readmes_visual_assets/`.

- `headers/`: dois PNGs compartilhados e arte-base original; CRM serve a guias
  e notebooks gerais; Squad é opção para notebooks específicos, sem empilhar banners.
- `readmes/`: 21 diagramas com SVGs de distribuição e PNGs; 23 ocorrências nos
  seis READMEs físicos porque atlas e confluência são compartilhados.
- `specs/approved_signatures.json` e `approved_headers.json`: hashes aprovados.
- `manifest.yaml`, `qa/` e `CONTEUDO_FIGURAS.md`: inventário e evidência textual.
- `tools/readme_visuals/`: fontes de autoria, composição e validação.

Os cinco SVGs assinatura são entradas aprovadas congeladas; os demais 16 são
saídas dos módulos `archetypes/`. As rotinas normais de produção não leem
`READMEs_refeitos/`. A pasta de revisão preserva a história e o baseline antigo.

## Auditoria cruzada

| Frente | Autor | Auditor independente | Correções verificadas |
|---|---|---|---|
| Topo | coordenador Codex | auditoria_relatorio_a + auditoria_topo_final | canais de contexto, runtime/evidência, direção e retorno global dos gates, procedência da skill e margens internas corrigidos |
| Snippets | auditoria_relatorio_a | auditoria_baseline_visual + coordenador | chip cortado corrigido e reinspecionado; cor de arquivo customizado corrigida; banner padronizado |
| Scripts | contratos_semanticos | auditoria_relatorio_a + coordenador | seta WARN, execução condicional, cores de procedência, margens e saídas reais corrigidas; dois títulos originais restaurados |
| Skills e prompts | auditoria_baseline_visual | coordenador | nomes completos das famílias a 28 px; pontas das setas; convergência real das rotas; margem do rodapé |
| Publicação | auditoria_baseline_visual | auditoria_publicacao_v2 + coordenador | alvo restrito, QA atual, espelho RAW, backup validado, retries reconciliados e resposta real da CLI cobertos por 29 testes |

## Decisões desta sessão

- Preservar os sete PNGs aprovados byte a byte: cinco assinaturas e dois headers.
- Separar identidade decorativa de diagrama informativo. Texto copiável e
  equivalente semântico permanecem nos READMEs, mesmo com suporte a imagens da Genie Code.
- Não sugerir leitura automática de toda pasta, contrato de retorno universal,
  enforcement implícito ou aprovação humana obrigatória em toda ação da plataforma.
- Não inserir códigos de decisões nem histórico de ambientes nos guias da equipe.
- Publicar apenas o escopo visual após validação e render canônico, com backup,
  detecção de divergência remota e conferência de bytes; não executar notebooks.

## Gates

Resultados locais concluídos em 2026-09-11:

- QA visual global: 8.154 verificações, zero falhas; fontes essenciais com pelo
  menos 14,4 px efetivos a 720 px e contraste mínimo conservador de 4,86:1.
- Duas execuções Node independentes: 44 arquivos comparados (21 SVGs, 21 PNGs e
  dois cabeçalhos), nenhum hash alterado. Sete PNGs aprovados continuam intactos.
- Títulos e subtítulos originais preservados, 23 alts alinhados aos contratos,
  âncoras adicionais válidas e exemplos Python/SQL preservados, exceto o retorno
  fictício incorreto de `data_quality_check`, corrigido contra sua implementação.
  `specs/editorial_corrections.json` fixa hashes antigos, corrigidos e da fonte.
- Nenhuma alteração nos módulos, instruções, SKILL.md ou templates do produto;
  o gate compara os demais arquivos do produto com o baseline por hash bruto.
- `tools/ci_local.py`: três etapas aprovadas, incluindo 45 testes da biblioteca
  e 35 das ferramentas; 29 testes adicionais do publicador visual aprovados.
- `tools/validate_assistant.py --conferir-readme`: sem falhas nem avisos.
- Espelho gerado exclusivamente por `tools/render_simulado.py --write`: 415 arquivos.
- Plano de publicação restrita: cinco READMEs e 98 arquivos visuais, total 103.

Uma figura geometricamente válida não garante que toda curva, ícone ou máscara
esteja correta. Por isso a revisão visual independente complementou os checks.

## Publicação e inspeção no workspace

Execução em andamento. Backup e preflight do escopo remoto concluídos sem
conflitos: 54 objetos anteriores, 103 envios previstos e 12 legados conhecidos.
Não registrar sucesso antes do recibo final. O navegador integrado abriu na tela
de login; a sessão autenticada é necessária para fechar a inspeção visual remota.

## Armadilhas conhecidas

- Não usar o renderer legado sobre v2. Os dois pontos de entrada antigos agora
  recusam sobrescrever o manifesto ativo v2.
- Não executar `validate.mjs` da Sprint 0 como gate da produção: ele exige que o
  conjunto antigo esteja intacto. Usar `validate_production.mjs`.
- `--retire-legacy` é migração pontual; depende do baseline histórico e não faz
  parte da regeneração diária. Nunca apagar por glob diretórios de assets.
- Publicação por CLI prova armazenamento e tipo; abrir no workspace prova
  renderização. Nenhum desses testes equivale a homologação Spark ou conversacional.
- Alterações desta rodada começaram sobre trabalho anterior ainda não commitado;
  não atribuir ao novo código de figura mudanças prévias de higiene e validação.
- O publicador visual desta release usa baseline Git fixo `f5461d8`: é uma
  migração controlada, não autorização para sobrescrever qualquer versão futura.
  Para outra release, revisar explicitamente sua referência antes de publicar.
