# Execução — retirada do localizador histórico do plano

Data: 08/10/2026. Autor: Codex. Base: `a50f35c1a9602d0bb0b05dd9afb020d42e7fda4b`.
Branch: `codex/organizacao-tools-20261007`. Revisão própria A0, contexto completo.
Escopo autorizado: executar a migração e excluir o arquivo. Push/merge não incluídos.

## Efeito e arquivos

- `PLANO_HUB.md` excluído; construção e paleta permanecem no CHANGELOG.
- AGENTS, fontes/derivados, índices de sprints e auditoria e comentário do
  validador apontam para a nova rota. Sua docstring histórica identifica a
  recuperação da dívida antiga por Git, sem mudar a regra de execução.
- Inventário nativo registra novo hash do núcleo; os 215 requisitos e suas
  fontes capturadas permanecem preservados. Adaptadores não precisam regenerar.
- `tools/historical_links.py` ganha resolver separado com allowlist de dois
  pares e hashes/blobs originais; o resolver anterior permanece intacto.
- `tools/tests/test_ai_historical_links.py` ganha positivos, negativos e prova
  do conjunto real de 30 referências anteriores + duas novas.
- Novo manifesto em `referencias-historicas-plano-hub.json`, ADR-0031, navegação
  histórica e marco de retirada. CHANGELOG mantém 199 linhas e os marcos antigos.

A análise partiu das 106 linhas em 53 arquivos da base do plano. Os dois hrefs
locais vigentes foram migrados; os dois hrefs datados foram preservados e
comprovados por Git. As menções restantes são registros antigos, quotes,
inventários, URLs/comandos Git e a documentação desta retirada.

Os scripts R06/R07/R08 são receitas de evidência encerrada; a busca pelos nomes
em `tools/`, workflows e skills não encontrou consumidores atuais. Seus bytes
foram preservados. Não são receitas para executar no checkout corrente.

Produto e seus derivados não foram editados nem renderizados. Workflows, Git
config, ADRs anteriores, snapshot de 198 registros, manifesto anterior e quotes
históricas foram comparados byte a byte com a base: 775 arquivos protegidos preservados,
além dos marcos anteriores, mapa de requisitos e cadeia de rastreabilidade.

## Gates locais

Executados na base acima com o diff desta entrega. Logs locais:
`.artifacts/retirada-plano-hub/`.

| Comando / verificação | Resultado observado |
|---|---|
| `python -B tools/tests/test_ai_historical_links.py -v` | 14 testes aprovados; fontes reais, 30 pares anteriores + dois novos e negativos |
| `python -B tools/tests/test_ai_history.py -v` | 17 testes aprovados; os 198 registros e recuperação preservados |
| `python -B tools/ai_controls.py --check` | PASS; 215 requisitos, cinco skills, 708 pares; zero avisos |
| `python -B tools/package_boundary.py` | PASS; zero erros |
| `python -B tools/ci_workflows.py --check` | PASS; checks/receitas/dependências preservados |
| `python -B tools/validate_assistant.py` | APROVADO; zero falhas e zero avisos; 32 hrefs históricos comprovados |
| Preservação e busca vigente | 775 arquivos protegidos intactos; nenhum resultado nas cinco rotas vigentes migradas |

As contagens reais do README foram atualizadas. A conferência final usa
`python -B tools/validate_assistant.py --conferir-readme` após a última edição.
Os testes cobrem fonte alterada, origem/target/hashes adulterados, quantidade
errada, href inventado, manifesto ausente, Git indisponível e entrada obsoleta.
Reintroduzir o arquivo local invalida o ledger; falta do manifesto não autoriza
os hrefs. Revisão própria A0; não se declara auditoria independente.

## Recuperação e rollback

A [decisão](../decisions/ADR-0031-retirada-localizador-plano-hub.md) identifica
os commits e o hash do plano integral. O [índice histórico](../historico/README.md)
fornece acesso de leitura; hrefs congelados não passam a links locais clicáveis.
Commit/blobs ausentes bloqueiam o gate. Não há dispensa de pasta inteira.

O rollback é a reversão do commit de retirada, preservando trabalho posterior.
Se o resolver falhar, restaurar o localizador e corrigir a migração; não relaxar
checks. CI remoto, runtime, clientes nativos e destino corporativo são NOT_RUN.
