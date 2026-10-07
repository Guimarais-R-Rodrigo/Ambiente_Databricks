# Execução da faxina — 07/10/2026

Owner: Codex, coordenador desta sessão. Baseline:
`8dd8da57de89122241890b8b6b059fd2f9be25d0`.
Branch: `codex/plano-faxina-20261007`. Estado inicial: relatório, plano, inventário
e README de workflows locais, preservados nesta execução.

## Escopo autorizado e decisões

O usuário autorizou executar: documentação dos workflows; revisão de adaptadores
mantidos; rename confirmado para `ambiente_databricks`; remoção do protótipo;
catálogo/manutenção das ferramentas; Manual Técnico V2 como única edição vigente.
Autorizou executores e auditores auxiliares. Não houve pedido de publicação remota.

| Lote | Owner executor | Escopo | Integração |
|---|---|---|---|
| Fonte/caminhos/CI/adaptadores | Codex coordenador | checkout principal | owner único das rotas comuns |
| Manuais | executor_manuais | worktree isolada faxina-manuais | copiar somente diff permitido e revisar |
| Protótipo/tools | executor_tools_prototipo | worktree isolada faxina-tools-prototipo | copiar somente diff permitido e revisar |
| Revisão | auditoria_ia_ci | somente leitura, contexto completo | apoio de mesma sessão, não origem A1 |

## Uso atual e história

A fonte corrente é `ambiente_databricks/`. Não é um simulador: o espelho gerado
continua em `.artifacts/simulado/`. Código, workflows e rotas atuais usam o novo
nome. Relatórios fechados, snapshots, fixtures datadas e corpos de ADRs mantêm o
nome original para representar sua revisão. O inventário da análise anterior é
fotografia da baseline, não catálogo corrente.

O [manifesto de referências históricas](referencias-historicas-faxina.json)
enumera os hrefs antigos preservados. Cada entrada informa fonte/hash, destino,
objeto Git e SHA256 no commit original. Para navegar, abra o [snapshot completo
no GitHub](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/tree/8dd8da57de89122241890b8b6b059fd2f9be25d0)
e o caminho `source`/`target` da entrada. Localmente, use
`git show 8dd8da57de89122241890b8b6b059fd2f9be25d0:<target>` para arquivo.
Links históricos recuperáveis não são links locais funcionando, e o gate não
verifica fragmentos/âncoras. Histórico Git ausente bloqueia essa prova.

O protótipo será recuperável pelo [registro Concierge](../historico/concierge.md)
e manifesto original. Isso não recria uma segunda pasta de produto no checkout.

## Evidência e limites

Implementação integrada no commit local `031fc559`, seguida de correções dos gates
da migração. O CI agregado inicial reprovou quatro etapas; as correções e repetições
focais serão registradas abaixo. A execução local não é homologação de destino. Apoios da mesma sessão não satisfazem
auditoria independente A1/A2. Copilot no VS Code do trabalho e runtime Databricks
permanecem NOT_RUN nesta execução local.


## Lotes executados

1. **Instruções e CI:** mantidos os adaptadores mínimos de Claude/Gemini e as
   cinco skills editoriais em `.agents/`, com cópias `.claude/skills` geradas e
   verificadas. A matriz distingue suporte documentado de ativação observada.
   Os 20 workflows têm catálogo de eventos, jobs, dependências, efeitos e limites.
2. **Fonte e ferramentas:** produto em `ambiente_databricks/`, paths correntes
   migrados, schema alterado somente no namespace de metadados e hash vigente
   atualizado. O dicionário histórico V01 conserva seu digest original.
   Ferramentas mantidas e catalogadas; 19 arquivos do protótipo retirados,
   recuperáveis e verificáveis no Git original.
3. **Manual:** Técnico V2 é a edição única; o Manual do Usuário continua separado.
   Mapa de migração preserva 69 âncoras legadas e as rotas semânticas, com exemplos
   E01–E14 conservados. Manifesto das 55 partes recomposto com bytes/hash reais.
4. **Integração e revisão:** ADRs sucessores [0028](../decisions/ADR-0028-manual-tecnico-v2-canonico.md)
   e [0029](../decisions/ADR-0029-faxina-fonte-e-prototipo.md) registram a mudança;
   corpos decisórios anteriores e evidência datada permanecem históricos.

### Render e ativo visual

Pré-flight final inventariou 709 arquivos geridos no destino resolvido
`.artifacts/simulado/`, com paths/bytes comparados ao commit `031fc559`, nenhum
extra, diretório desconhecido, symlink ou junction. A substituição decorre do
escopo de limpeza autorizado. Validação prévia: zero falhas e zero avisos.
`render_simulado.py --write` produziu 709 arquivos; `--check` comprovou equivalência
por paths, bytes, hashes e tipos. O marcador fica fora dos 708 arquivos de produto.

Somente SVG/PNG `raiz.02_arquitetura_ecossistema` mudaram entre 42 arquivos de
figuras. A área da pasta foi ampliada para o nome novo; fonte essencial de 32 px
mantida, largura medida 340,265625 px e mínimo efetivo 14,4 px na escala de 720 px.
Inspeção visual local observou nome completo, seta e caixas sem sobreposição.
As 12 figuras congeladas e cinco assinaturas aprovadas não foram promovidas.
Manifesto, hashes de inputs e metadata da figura foram atualizados pelo renderer.
QA atual: `node tools/readme_visuals/validate_production.mjs`, 7.829 checks,
zero falhas. Não equivale a aceite humano independente.

| Arquivo | SHA256 anterior na revisão de integração | SHA256 atual |
|---|---|---|
| PNG raiz.02 | `d6882c0b60257cae22b6deaef0aedfb02f21f8dc1b21163bd4f5f5d98c0e4775` | `44ec0ce54f7f2f7747a63b30169ed250d3fbc3b41eed8a2acc85260b97faf2bf` |
| SVG raiz.02 | `9421269d21d55bf6828f40c57c5c499f85e52cb25c4654dc571a8e7ad49dabdb` | `3d5ce67c22728eadc3bad30a2521646031a34b7541d77c12f8c2a12311188f01` |

O SVG anterior já tinha aria-label migrado, mas os paths visuais ainda mostravam
nome antigo. A comparação acima usa a integração, sem reescrever a baseline visual.

### Diagnóstico dos testes

O CI inicial do commit `031fc559` rodou 14 etapas: dez passaram e quatro falharam
(Temas, SEF, READMEs e regressões IA). As correções preservam gates estritos:
stdout UTF-8/LF dos dicionários; runbook S6 corrente; figura e metadata atuais;
cinco hashes de release após delta documental/schema autorizado; ledger estreito
da figura (`tools/tests/runtime/visual_successor.json`) com predecessor Git e
negativos de mutação não autorizada; proveniência de
relocação no commit original, separada do caminho vivo; tabela contínua de ADRs.

Fixtures precisam escrever LF para testar a regra pretendida no Windows. Criar
symlink exige privilégio indisponível; skip de ambiente não comprova a guarda.
O subprocesso Python isolado exclui user site: `typing_extensions 4.16.0` existe
somente nele, e `referencing 0.37.0` falha em `TypeVar(default=...)` sem essa
dependência. Não houve instalação nem relaxamento das flags de isolamento.

A descoberta indiscriminada `test_*.py` em um único processo foi interrompida
após deixar de produzir saída; não gerou sumário e é **INTERRUPTED**, sem contagem
ou aprovação. O resultado verificável usa as receitas separadas de `ci_local.py`
e os módulos afetados. Os logs locais ficam em `.artifacts/faxina/` (ignorados).

## Reversão

As mudanças permanecem revisáveis no Git local. Os lotes dos executores foram integrados; worktrees isolados serão arquivados
com snapshot recuperável após a conferência final.
Não usar reset destrutivo: recuperar somente arquivos deste lote, preservando o
trabalho documental anterior e quaisquer alterações alheias.
