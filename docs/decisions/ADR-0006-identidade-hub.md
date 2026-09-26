# ADR-0006 — De ambiente pessoal a Hub de equipe

- **Status:** Aceito
- **Data:** 2026-08-16
- **Supersede:** nada. Complementa o ADR-0001 (arquitetura) e o ADR-0004
  (declaração explícita de helpers).

## Contexto

O ecossistema nasceu como ambiente pessoal e vai ser apresentado a uma equipe.
Duas convenções que funcionavam para uma pessoa deixam de funcionar para um time:

**O prefixo `x_`** marcava o que não é nativo da plataforma. Ele exige uma
legenda: quem bate o olho na árvore de pastas não deduz o significado, e o
projeto passou a depender de cada README explicar a convenção. Numa base que
circula por uma área inteira, a legenda não acompanha o leitor.

**O prefixo `rodrigo-`** nas skills identificava o autor. Num Hub de equipe, o
autor deixa de ser a informação relevante, e o nome passa a sugerir que aquilo
pertence a alguém.

## Decisão

**Prefixo `hub_` para pastas, `hub-ml-` para skills.** A regra tem duas metades,
e a divisão não é estética:

> **Underscore onde o Python importa. Hífen onde a plataforma nomeia.**

`hub-snippets` com hífen é impossível — `from hub-snippets.spark.pit_join import
pit_join` é erro de sintaxe, porque nome de pacote Python não aceita hífen. A
alternativa seria obrigar todo notebook a usar `importlib.import_module(...)`, o
que inviabiliza o uso por uma equipe. Skills não têm essa restrição e usam hífen,
que é a forma que as 12 originais já usavam e que funciona.

O ganho colateral é que a regra informa: ao ver `hub_`, sabe-se que aquilo se
importa no Python; ao ver `hub-`, que é a plataforma que carrega.

## Tabela de correspondência

Esta é a razão principal de o ADR existir. Registros datados — `CHANGELOG.md`,
ADRs anteriores, auditorias e evidência de teste — **não são reescritos**: eles
descrevem o que foi observado na época. Para que continuem legíveis, a tradução
precisa morar em um lugar estável, e é aqui.

### Pastas

| Nome anterior | Nome atual | Observação |
|---|---|---|
| `x_snippets/` | `hub_snippets/` | biblioteca Python importável |
| `x_scripts/` | `hub_scripts/` | utilitários de diagnóstico |
| `x_prompts/` | `hub_prompts/` | briefings prontos para colar |
| `x_docs/` | **removida** | ver desdobramento abaixo |
| `x_config/` | **removida** | continha lista MCP vazia; o projeto não usa MCP |
| `x_projects/` | **removida** | guardar `AGENTS.md` ali nunca fez ele ser descoberto |
| `/Users/<user>/x_lab/` | `/Users/<user>/hub_lab/` | área de teste no workspace |
| — | `hub_padroes/` | **novo**: os moldes de todo objeto do Hub |

### Conteúdo de `x_docs/`

| Arquivo anterior | Onde está agora |
|---|---|
| `x_docs/glossario.md` | `.assistant/GLOSSARIO.md` |
| `x_docs/catalogo_helpers.md` | `.assistant/CATALOGO_HELPERS.md` |
| `x_docs/notebooks/*.py` | `hub_snippets/_notebooks_a_migrar/`, até serem desmembrados por snippet |
| `x_docs/SKILL_TEMPLATE.md` | substituído por `hub_padroes/skill/template.md` |
| `x_docs/ROADMAP_SKILLS.md` | `docs/historico/ROADMAP_SKILLS.md` |
| `x_docs/LEGACY_CONTEXT.md` | `docs/historico/LEGACY_CONTEXT.md` |
| `x_docs/skills_manifest.md` | `docs/historico/skills_manifest.md` |
| `x_docs/x_original_export_manifest.json` | `docs/historico/` — nome preservado, é evidência de exportação |
| `x_config/mcp_servers.legacy.json` | removido |
| `x_projects/AGENTS_TEMPLATE.md` | `docs/historico/AGENTS_TEMPLATE.md` |
| `x_projects/README.md`, `_template_projeto.md`, `exemplo_churn_previdencia.md` | removidos |

### Skills

Renomeação prevista para a Sprint 3. O padrão é `rodrigo-<tema>` →
`hub-ml-<tema>`, com o `<tema>` inalterado:

| Nome anterior | Nome atual |
|---|---|
| `rodrigo-eda-profissional` | `hub-ml-eda-profissional` |
| `rodrigo-cross-eda-ml` | `hub-ml-cross-eda-ml` |
| `rodrigo-feature-engineering` | `hub-ml-feature-engineering` |
| `rodrigo-validacao-estatistica` | `hub-ml-validacao-estatistica` |
| `rodrigo-baseline-ml` | `hub-ml-baseline-ml` |
| `rodrigo-explainability` | `hub-ml-explainability` |
| `rodrigo-monitoramento-modelo` | `hub-ml-monitoramento-modelo` |
| `rodrigo-pipeline-builder` | `hub-ml-pipeline-builder` |
| `rodrigo-analise-safra` | `hub-ml-analise-safra` |
| `rodrigo-comentar-notebook` | `hub-ml-comentar-notebook` |
| `rodrigo-tutor-databricks` | `hub-ml-tutor-databricks` |
| `rodrigo-auditoria-skills` | `hub-ml-auditoria-skills` |

Nenhuma `description` muda na renomeação, então o roteamento automático
permanece certificado. A `@menção` muda, e os 12 testes de menção são refeitos.

## Consequências

**O que melhora.** A árvore de pastas comunica sozinha o que é nativo e o que é
do Hub. O nome deixa de sugerir dono. E a regra de nomenclatura passa a carregar
informação técnica útil.

**O que custa.** Toda referência aos nomes antigos em camada viva precisou ser
reescrita — foram 85 arquivos na Sprint 2. Documentos datados mantêm os nomes
antigos e dependem desta tabela para serem lidos.

**O que fica em aberto.** Um documento com nome antigo e sem link para cá é
dívida: quem o encontrar por busca não sabe traduzir. A nota de cabeçalho nas
camadas preservadas aponta para este ADR justamente por isso.

## Alternativas descartadas

**Manter `x_` e explicar melhor.** É a solução que a documentação já tentava, e
depende de o leitor encontrar a explicação. Numa base que circula por uma área,
a explicação não acompanha o arquivo.

**Hífen em tudo, inclusive nas pastas.** Impossível em Python, como acima.

**`hub-` sem o `ml` nas skills.** Mais curto, mas perde a marca de domínio num
workspace que pode vir a hospedar skills de outras frentes.
