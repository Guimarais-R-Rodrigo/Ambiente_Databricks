# ADR-0026 — Arquitetura por tarefa e preservação da história

Data: 2026-10-06
Status: Aceito para implementação local em lotes verificáveis
Autor: Codex, execução local do plano de arquitetura do projeto
Aprovador e evidência: usuário, pedido “execute o plano”, após o diagnóstico da base indicada abaixo
Supersede: somente granularidade de fechamento diário no CHANGELOG prevista pela camada IA; preserva o núcleo e as fronteiras do ADR-0025
launchable=false
execution_authorized=false
Evidência de execução: gates locais por lote; nenhum PASS de destino implícito
Observabilidade do destino: NOT_OBSERVABLE

## Contexto

Base escolhida: `126a2e125cca2251527f187a58696243414c6859`, sucessora da revisão
READMEs/IA, sem presumir integração em `main`. Fonte, ferramentas e provas já têm
donos adequados. O custo de descoberta vem da mistura entre orientação corrente,
cronologia extensa, contexto de auditoria e insumos de manutenção no pacote.

O CHANGELOG da base contém 198 entradas em 4.501 linhas. Encortar o arquivo sem
mudar a regra “uma entrada por sessão” recriaria o mesmo problema. Arquivar
história também não altera sozinho a seleção do bundle textual integral.

## Decisão

Preservar os domínios e contratos públicos, com mudanças pequenas e provas por lote:

1. README e docs/README apontam rotas para usar, manter, entregar e investigar.
   ADRs e classes de regressão reutilizam os índices existentes; owners vivos
   conservam autoridade sobre estado atual. Não criar um diário concorrente.
2. A raiz registra marcos de uso, arquitetura, compatibilidade, contrato,
   distribuição ou risco material. Toda sessão continua rastreável no owner
   de evidência ou handoff, com data e autoria reais. Manutenção trivial pode
   ficar no commit/PR. O [template](../ai/templates/changelog-entry.md) detalha o critério.
3. Arquivar as 198 entradas sem reordenar ou reinterpretar: somente dois hrefs
   relativos são rebaseados. Commit de origem, hashes por entrada e do arquivo,
   mapa das transformações e teste de recuperação tornam o movimento reversível.
   Migrar somente as onze exceções correspondentes por path/hash/origem;
   nenhum diretório histórico recebe exclusão genérica.
4. Concierge tem rota ativa para o produto canônico e localizador para o
   protótipo. Reter fisicamente a árvore antiga enquanto seus consumidores
   não tiverem migração e preservação demonstradas.
5. Contexto por tarefa é recorte aditivo identificado, com SHA, inclusões,
   motivos, exclusões e expansão. `canonical`/`full` preservam seus contratos;
   bundle de auditoria e pacote de instalação continuam artefatos diferentes.
6. Separar manutenção do payload por dependência comprovada: suíte de core em
   `tools/tests/runtime/test_core.py`, QA gráfico em `tools/readme_visuals/qa/`
   e fontes dos cabeçalhos em `tools/readme_visuals/assets/headers/src/`.
   Preservar casos/IDs/assertions, licenças, proveniência, fixtures operacionais,
   recursos runtime e os doze assets protegidos. Extração exige manifesto de
   diferenças explicado e provas de geração/uso, nunca corte por extensão/nome.
7. A raiz gerada corrente é `.artifacts/simulado/`, com seleção limitada de
   `--output-root` e gate `--check` de paths, bytes/hashes e object_type. A
   retirada do espelho rastreado depende de geração limpa, consumidores
   migrados e comparação de pacote; mover o default sozinho não basta.
8. O gate normal de IA compara a fonte atual com a saída atual. A baseline
   congelada da campanha anterior continua intacta e `--migration-freeze`
   continua comprovando somente aquele freeze. Mudança autorizada posterior
   pode reprovar o freeze antigo sem justificar sua reescrita. Eventual
   aposentadoria de exceções ligadas ao espelho deve ter prova própria.
9. Consolidar CI por propriedade e ambiente, preservando checks, negativos,
   Python/Spark/ipywidgets, receitas e artefatos exclusivos. Não alterar
   configurações de required checks, publicar, fazer merge ou homologar destino
   por inferência desta reorganização.

## Alternativas consideradas

- Renomear tudo para novas raízes ou abrir repositórios: amplia risco de paths,
  imports e consumidores sem resolver a seleção de contexto.
- Apagar cronologia, protótipo ou assets por idade/extensão: perde evidência ou
  recursos runtime; a ausência de import não demonstra ausência de dependência.
- Reescrever baseline/ADRs antigos ou excluir todo `docs/historico`: enfraquece
  os controles e confunde mudança atual com o fato histórico.
- Retirar o espelho antes de migrar consumidores: `git diff` deixaria de provar
  paridade e os pacotes poderiam consumir uma saída antiga ou inexistente.

## Consequências

A navegação cotidiana é menor, enquanto o bundle integral pode crescer com os
índices e manifestos. Não é medição de tokens, custo ou carregamento nativo.
Mover QA/build não reduz automaticamente todos os bytes: cada diferença de
payload precisa de explicação. Não há concessão de publicação, login, compute,
instalação, homologação corporativa ou aceitação de risco.

## Verificação e reversão

Por lote: contratos/links, positivo e mutante discriminante, fonte/derivado,
manifestos, geração isolada repetida e gates afetados no SHA final. O lote de
história inclui [teste de recuperação e exceções](../../tools/tests/test_ai_history.py).
PASS local não promove BLOCKED, NOT_RUN ou NOT_AUTHORIZED de outras frentes.
Revisão não-autora local não é nova origem independente A1.

Reverter apenas o lote, preservando mudanças alheias. O snapshot e seu mapa
recuperam byte a byte o CHANGELOG original; restaurar consumidores junto das
fontes e regenerar os derivados pelo owner. Não usar reset destrutivo nem
reescrever a história Git. Caso haja publicação autorizada em outra tarefa,
a reversão Git não desfaz o workspace; vale o runbook de rollback de destino.

## Referências

- [Contrato comum](../../AGENTS.md) e [fontes/derivados](../ai/rules/fontes-e-derivados.md)
- [ADR-0025](ADR-0025-arquitetura-instrucoes-ia.md), [índice ADR](README.md)
- [Snapshot e prova de recuperação](../historico/changelog/README.md)
- [Classes de defeito e guardas](../auditoria/README.md#classes-de-defeito-que-viraram-guardas)
- [Localizador Concierge](../historico/concierge.md)
