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
focais estão registradas abaixo. A execução local não é homologação de destino. Apoios da mesma sessão não satisfazem
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


## Resultado final observado

Implementação e correções: `247ee609e25073966ff7237780551365dd2df298`.
O fechamento seguinte altera somente esta evidência documental. Não houve push,
merge, instalação de dependências, publicação Free ou transposição ao trabalho.
Stash SER00 anterior e branch de origem permanecem preservados.

| Verificação | Revisão / comando | Resultado e alcance |
|---|---|---|
| Fonte e snapshot README | `247ee609`: `python -B tools/validate_assistant.py --conferir-readme` | **PASS**, exit 0, zero falhas/avisos; contagens atuais 1.758 arquivos e 1.965 links no repo |
| Temas | `4be343b1`, etapa `temas` do `ci_local.py --verbose` | **PASS**, 759 testes, 18 skips; código temático e payload não mudaram em `247ee609` |
| Skill Enforcement | `247ee609`: `python -B tools/ci_local.py --etapa sef --verbose` | **PASS**, exit 0, perfil `DIAGNOSTIC_SE08_NO_RENDER`; não é certificação Genie/runtime |
| Regressões IA | `247ee609`: `python -B tools/ci_local.py --etapa ai-regressoes --verbose` | **PASS**, exit 0, 173 testes, nove skips explícitos de ambiente |
| READMEs / fronteira | `247ee609`: `python -B tools/ci_local.py --etapa readmes --verbose` | **FAIL** técnico, exit 1; 79 testes, uma falha por dependência no Python isolado, três skips; bloqueio de ambiente descrito acima |
| Contratos IA | `247ee609`: `python -B tools/ai_controls.py --check` | **PASS**, cinco skills/cópias, 215 requisitos, 708 pares de produto, zero avisos; não certifica loader nativo |
| Render | `python -B tools/render_simulado.py --check` | **PASS**, equivalência integral do payload gerado após o preflight registrado |
| Compilação CI | `python -B tools/ci_workflows.py --check` | **PASS**, nomes dos checks, receitas exclusivas e dependências fail-closed preservados |
| Recuperação Concierge | `python -B tools/verify_concierge_history.py` | **PASS**, 19 blobs com tamanho/SHA256 conferidos; nada restaurado no checkout |
| Fronteira de pacote | `python -B tools/package_boundary.py` | **PASS**, zero erros; predecessor visual não pode contornar o ledger, mesmo com metadata antiga restaurada |
| QA visual | `node tools/readme_visuals/validate_production.mjs` | **PASS**, 7.829 checks, zero falhas; inspeção visual local, sem aceite independente |

O CI agregado inicial teve dez etapas aprovadas na revisão `031fc559`:
biblioteca (45 IDs core sem skips), ferramentas, transição, Micromodelos e aceite
extraído, Concierge/pacote/regressões/integração, controles IA e validação simples.
As quatro etapas que falharam foram corrigidas e repetidas como indicado acima;
READMEs mantém o bloqueio do host. A rodada agregada `4be343b1` passou Temas e
reprovou o snapshot de contagem (1.757 versus 1.758); foi interrompida para corrigir
isso e a proteção do sucessor visual. **Não há reivindicação de CI agregado final
inteiramente aprovado.** Os resultados por revisão acima são as provas disponíveis.

Auditoria auxiliar de mesma sessão revisou o último diff e confirmou que o P2
sobre restaurar metadata antiga está resolvido; nenhum outro P1/P2 permaneceu na
revisão. O teste negativo restaura o blob predecessor e exige falha com e sem
ledger. Mantém-se o limite de independência A0/contexto completo.

**Pendências de destino:** resolver a dependência `typing_extensions` no ambiente
Python isolado de testes e repetir READMEs; executar CI remoto, Copilot no VS Code
do trabalho e runtime Databricks (todos **NOT_RUN** aqui). A limpeza do checkout
foi implementada; essas provas não são substituídas por documentação.

### Integridade dos logs locais

Os arquivos abaixo são ignorados, não pertencem ao payload e não precisam ser
carregados como contexto da próxima LLM. Hashes permitem conferir a cópia local;
um clone novo terá este relatório e o código, mas não esses logs de execução.

| Log em `.artifacts/faxina/` | SHA256 |
|---|---|
| `snapshot-corrigido.log` | `db2227f90723008e0f56dc079ee073dc9329981774e278ad13a1b9db2fa17166` |
| `ci-final.log` | `baab1a59b7450e82a056ecce4c09232337e501076178f09f2f4ebdce0c681e6f` |
| `sef-final.log` | `31a0f565daebcd5b0cabb369d3c7daf2aaf38ad2fe5b41481a9eb61ac346e8eb` |
| `ai-final.log` | `1cea28bab899c307eb11ff8731e7ca1341d8ee2cdb64cadd1ce38c9a7d086c0c` |
| `readmes-final.log` | `090924ae2f1fb978e05732ded56aca99bfb9078061f301c3cd7da61f92dba75c` |
| `ai-controls-final.json` | `cade46e38513694a2d0f2a45a948b75f0af94f410db1058d77636b4d588c01ac` |
| `qa-visual-final.json` | `5ee03368f560307c33e6b580e551351c9ce251d82139ba5722ec4071a12c749a` |
| `preflight-render-final.json` | `fad77d6d915292e3a513d6ea4eeacd1bd90e9567e7c4744b7f2a8d6b52064e31` |
| `promocao-diagrama.json` | `d8d092a78b419d9eba8792debc28b3e9d823978642b71075ba2c1cb6e5ff543a` |

## Reversão

As mudanças permanecem revisáveis no Git local. Os lotes dos executores foram integrados; os dois worktrees foram arquivados
com snapshots recuperáveis pelo app. O registro ignorado do executor de manuais
foi preservado em `.artifacts/faxina/executores/manuais-integracao.txt`.
Não usar reset destrutivo: recuperar somente arquivos deste lote, preservando o
trabalho documental anterior e quaisquer alterações alheias.
