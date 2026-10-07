# Compositores de figuras

Módulos internos Node usados pelos renderers visuais. Não são CLIs independentes.
A receita pública de geração pertence ao [guia visual](../README.md).

| Módulo | Família |
|---|---|
| [top.mjs](top.mjs) | Figuras da raiz e do índice `.assistant` |
| [snippets.mjs](snippets.mjs) | Biblioteca de snippets |
| [scripts.mjs](scripts.mjs) | Helpers e diagnósticos |
| [methods.mjs](methods.mjs) | Skills e prompts |
| [signatures.mjs](signatures.mjs) | Composição de assinaturas/protótipos visuais; a produção ativa preserva as assinaturas aprovadas como inputs |

`production.mjs` seleciona módulos por `--family`. Contratos e tokens do produto
orientam a composição; `lib.mjs` mede tipografia e reúne primitivas. Mudança aqui
pode alterar PNG/SVG, metadata QA e hashes do manifesto: comparar bytes, conferir
ativos congelados e revisar visualmente antes de promover. Não reduzir fonte nem
mudar pins para disfarçar overflow. [QA](../qa/README.md) registra as verificações.
