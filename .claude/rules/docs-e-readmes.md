# Regra — Padrão de documentação

O usuário exige documentação de alto padrão. Referência de qualidade mínima: o
`README.md` da raiz deste repositório (tabelas + mermaid + exemplos + fontes).

- Todo diretório de primeiro nível tem README explicando papel, uso e limites.
- Documentos ricos têm: visão em diagrama (mermaid) quando houver fluxo, tabelas
  para fatos enumeráveis, exemplos concretos copiáveis, e seção de fontes/links.
- PT-BR na prosa; inglês em função, classe, parâmetro e coluna devolvida. **Constante de domínio pode ser português** — a paleta institucional e as seções da EDA nomeiam coisas que só existem aqui, e traduzir apaga o referente.
  A biblioteca mede: 85 funções públicas em inglês contra 5 em português, e
  37 constantes em português — quase todas de `constants/colors` e
  `constants/emojis`.
- Sempre distinguir visualmente o que é **nativo** da plataforma do que é
  **customizado** (prefixo `hub_`/`hub-`, avisos "não auto-descoberto").
- Números em narrativa executiva no padrão brasileiro (`3.375.674`, `92,8%`).
- Nunca documente capacidade não verificada como existente; marque como
  `PENDENTE/DECISAO` ou "planejado".
- Docs de decisão (ADR) são imutáveis após aceitos; mudanças geram novo ADR que
  supersede o anterior.
