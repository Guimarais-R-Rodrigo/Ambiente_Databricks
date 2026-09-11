# Handoff — Sprint 0 da evolução visual

Data: 2026-09-10 · De: Codex · Para: próxima sessão de revisão visual

> Nota de manutenção de 11/09/2026: este handoff preserva o registro histórico.
> Para o conjunto vigente, consulte o [guia das ferramentas visuais](../../tools/readme_visuals/README.md).
> Referências a protótipos locais não são links para arquivos disponíveis no Git.

## Estado registrado em 10/09/2026

Implementada a fundação para revisar a direção gráfica antes das cinco sprints
documentais. A galeria isolada (`../../READMEs_refeitos/readmes_viasual_melhorado/sprint_0/README_SPRINT_0.md`; artefato local não versionado neste checkout)
contém cinco assinaturas em variantes README/apresentação, comparações, contratos
de 21 figuras futuras, licenças, manifesto e QA. O
estado da sprint (`../../READMEs_refeitos/readmes_viasual_melhorado/sprint_0/ESTADO_SPRINT_0.md`; artefato local não versionado neste checkout)
é a referência para a publicação e os limites dos testes.

Os seis READMEs físicos ativos e os 22 ativos anteriores permanecem preservados.
`Novo_Ambiente_Simulado/` foi regenerado pela ferramenta canônica, sem edição manual.

## Em andamento / condição de continuidade

As cinco assinaturas foram aprovadas pelo usuário em 2026-09-10. Depois da
aprovação, ele solicitou dois cabeçalhos adicionais, com CRM e Squad, e pediu
novo OK antes da continuidade. As propostas locais de cabeçalho (`../../READMEs_refeitos/readmes_viasual_melhorado/sprint_0/cabecalhos/README_CABECALHOS.md`; artefato local não versionado neste checkout)
usam uma arte-base raster com tipografia determinística; não foram publicadas.
Não produzir os outros dezesseis ativos nem substituir imagens dos READMEs ativos
antes da nova confirmação solicitada.
Sprint 0 não é homologação de toda a documentação, runtime nem uso conversacional.

## Decisões de implementação

- Usar SVG determinístico e PNG rasterizado para diagramas técnicos exatos.
- Separar contrato semântico, microcopy, tokens e composição; manter snapshot
  derivado junto da galeria para que outra LLM possa conferir o pacote.
- Preservar cinco sprints documentais: raiz e `.assistant` são dois consumidores
  dentro da mesma sprint de topo; snippets, scripts, skills e prompts têm as demais.
- Validar os nomes e retornos dos sete scripts sem inventar um contrato universal.
- Representar frontmatter dentro de `SKILL.md` e recursos adicionais como
  opcionais suportados, distinguindo-os do inventário atual.
- Usar política de aprovação configurada, sem afirmar aprovação manual universal.
- Publicar somente a galeria em estrutura espelhada, sem executar notebook,
  iniciar compute, alterar permissões ou publicar o pacote ativo inteiro.

## Próximos passos recomendados

1. Obter a avaliação do usuário para os dois novos cabeçalhos. As cinco assinaturas
   existentes estão aprovadas e não foram alteradas na rodada dos cabeçalhos.
2. Se houver ajustes nos cabeçalhos, editar seu `src/copy.json` e/ou compositor
   `tools/readme_visuals/headers.mjs`, preservando o original raster.
3. Após o novo OK, integrar os cabeçalhos e validar seus caminhos e leitura no
   Databricks. A entrega anterior de 102 objetos não inclui os cabeçalhos.
4. Executar as sprints documentais uma a uma, seguindo os contratos e preservando
   tópicos, subtópicos, didática e conteúdo copiável dos READMEs.
5. Só promover aos READMEs ativos quando os respectivos gates forem aprovados.

## Armadilhas conhecidas

- Não editar `renders/`, `baseline/` nem `contracts/` da galeria: são derivados.
- `sources/` do conjunto antigo também contém SVGs gerados, apesar do nome.
- `tokens.yaml` v2 é candidato; o renderer antigo conserva a implementação anterior.
- Algumas âncoras existentes contêm um seletor Unicode e apontam a seções-pai.
  A matriz declara a diferença entre âncora atual e ID ASCII proposto. Migrar só
  durante a sprint documental correspondente.
- Os seis blocos da figura de briefing não são os cinco macroestágios de uso.
- Publicação confirmada por exportação de bytes não comprova renderização visual.
  A inspeção no navegador é uma etapa separada.
- Falhas de colisão entre textos são automáticas; curvas, silhuetas, entendimento
  humano e compartilhamento de tela exigem revisão visual.
- O publicador isolado não exclui objetos inesperados. Deve parar e explicar a
  divergência em vez de limpar uma pasta remota por conveniência.
