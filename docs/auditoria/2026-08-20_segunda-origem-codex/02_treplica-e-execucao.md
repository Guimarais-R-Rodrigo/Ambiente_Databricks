# Tréplica, consenso e execução das correções

- **Data:** 2026-08-20
- **Baseline:** auditoria `01_rodada.md` sobre o commit `9c17008`
- **Contraditório:** Claude Opus, resposta fornecida por Rodrigo
- **Executor:** Codex
- **Regra:** reproduzir antes de corrigir; preservar convenções de domínio; não
  declarar teste Databricks que não foi reexecutado

## Resultado do contraditório

O contraditório melhorou a auditoria. Ajustei quatro severidades/enquadramentos,
adotei a correção de unidade proposta para KS, aceitei o agravante do oráculo
MLflow e retirei a proposta editorial de reestruturar os READMEs. Não restou
divergência técnica que exigisse sustentar a posição original contra o Claude.

O veredito final também ficou mais preciso: **o projeto não alegava que a
replicação já estava concluída; o runbook do baseline era inseguro quando
executado**. Depois das correções locais, o runbook deixa de apagar estado alheio
e os gates recuperam propriedades que antes só aproximavam por proxy. A
replicação no trabalho continua condicionada à reexecução Spark pós-correção e
aos forward tests pendentes.

### Severidade revisada do baseline

| Faixa | Quantidade | Itens |
|---|---:|---|
| 🔴 crítico | 2 | F03, F04 |
| 🟠 alto/relevante | 16 | F01, F02, F05–F07, F09–F11, F13–F20 |
| 🟡 melhoria/robustez/documentação | 6 | F08, F12, F21–F24 |

## Onde ajustei minha opinião

| Ponto contestado | Posição final | Consequência aplicada |
|---|---|---|
| F01 | Procedente, mas não crítico: o trabalho não tem CLI; o alcance realista é outro workspace pessoal | rebaixado para 🟠; escrita agora exige perfil e host Free explícitos |
| F02 | O defeito era duplo: portabilidade da identidade pessoal e exceção sem decisão canônica | 44 ocorrências sanitizadas; identidade neutra e pacote mínimo formalizados no ADR-0009 |
| F04 | O defeito era mais grave que o texto original: o oráculo falhava exatamente na propriedade que justificava sua existência | agora exige classe e assinatura da mensagem; exceção alheia é `FAIL` |
| F08 | Robustez local, não segurança externa | rebaixado para 🟡; traversal ainda foi bloqueado e ganhou mutation test |
| F12 | Melhoria de desenho, não quebra atual | rebaixado para 🟡; padrão de proveniência foi implementado sem tratar outputs antigos como inválidos |
| F13 | `metrics_report` seguia a convenção de crédito 0–100; o defeito era a costura com limiar 0–1 | preservado `ks_pct` em pontos percentuais; monitor e teste de composição usam a mesma unidade |
| F22 | A frase sobre auto-descoberta era falsa; “landing page curta” era preferência editorial | frase corrigida; não houve reestruturação geral dos READMEs |
| Veredito | “não seguro para replicação” era largo demais | substituído por “runbook do baseline inseguro quando executado” |

## Reprodução anterior às correções

Os probes foram executados sobre o baseline, antes de editar a implementação:

- KS: `metrics_report` devolveu `100`, enquanto `PerformanceMonitor` tratava
  variação `40 → 39` como delta crítico de `1` contra limiar `0,05`;
- vintage: painel com lacuna produziu `50% → 0% → 50%`, entrada tardia fabricou
  MOB 0 e target nulo virou não-evento;
- temporal: `rolling_window=1` esvaziou a base por `std(ddof=1)`;
- score: coeficiente infinito foi aceito; score constante gerou tabela `0×0`;
  lift com uma classe publicou `1,00x`;
- gates: YAML inválido, pasta extra de skill, chamada qualificada, `cache()` em
  `finally`, comentário com “limit”, `spark` em outro escopo e detector com
  comportamento invertido reproduziram falsos verdes;
- ferramentas: renderer resolveu traversal fora do simulado e bundle aceitou
  `git ls-files` com retorno 128 como pacote vazio.

## Execução por achado

| ID | Decisão/correção | Evidência de aceite | Estado |
|---|---|---|---|
| F01 | host e perfil Free explícitos antes de `--execute`; destino mostrado e comparado | testes de política local; escrita sem alvo explícito é recusada | corrigido localmente |
| F02 | identidade neutra em conteúdo ativo/derivado; ADR-0009; ZIP mínimo | scan de identidade e render em `Users/usuario-free/` | árvore/pacote corrigidos; histórico Git pendente |
| F03 | runbook preserva `.mcp_servers.json` e remove só skills Hub inventariadas | revisão dos comandos e manifesto gerenciado | corrigido |
| F04 | Free e trabalho têm casos distintos; oráculo exige exceção/mensagem; run de trabalho é temporário e limpo | mutation tests locais; runtime real pós-correção ainda pendente | código corrigido; gate externo pendente |
| F05 | conjunto exato de 13 nomes compartilhado por validador e publicador | pasta extra/missing agora reprova | corrigido |
| F06 | contratos usam AST para chamadas qualificadas e colunas realmente produzidas/consumidas | `mod.f(bad=1)` e `select('ghost')` reprovaram em teste | corrigido |
| F07 | normas usam escopo/AST; sync compara comportamento | 14 mutation tests das ferramentas aprovados | corrigido |
| F08 | username validado e destino provado dentro de `Users/` | traversal `..\..\escape` rejeitado | corrigido |
| F09 | retorno do Git obrigatório; modos `canonical/security/full`; manifesto de hashes | falha de `git ls-files` não gera bundle vazio | corrigido |
| F10 | instruções conciliadas com inventário de dependências, contexto automático e precedência de segurança | 8.116/20.000 caracteres; validador aprovado | corrigido |
| F11 | 161/161 campos agora têm como preencher, motivo e exemplo; 16/16 têm QA e limites | novo gate `prompts`; notebooks sem escrita corrigidos | corrigido |
| F12 | bloco customizado de proveniência e auditoria só contra produtor explicitamente nomeado | links/contrato verificados | melhoria implementada |
| F13 | chave `ks_pct`, unidade 0–100 e política do monitor em p.p. | teste conhecido e composição `metrics_report → PerformanceMonitor` | corrigido |
| F14 | snapshots ausentes permanecem ausentes; cobertura e monotonicidade validadas; target nulo falha | testes de lacuna, entrada tardia e nulo | corrigido localmente |
| F15 | diagnóstico do `pit_join` usa categorias mutuamente exclusivas no mesmo grão e reconcilia o total | invariante entrou no smoke test | código corrigido; Spark pendente |
| F16 | `dropna` só nas features geradas; janela mínima 2 | known-answer tests locais | corrigido |
| F17 | finitude, variação do score e duas classes são pré-condições | known-answer tests locais | corrigido |
| F18 | sample estratificado preserva raro e N exato; PK nula falha; data não entra em drift automático | invariantes no smoke test | código corrigido; Spark pendente |
| F19 | documentos vivos apontam para `tools/publicar_free.py` | busca sem referência ativa ao engine supersedido | corrigido |
| F20 | atualização substitui só quatro diretórios Hub-owned e remove obsoletos por manifesto | runbook/checklist sincronizados | corrigido |
| F21 | gate do README cobre todo rótulo atual e falha se o rótulo sumir | linha `prompts` incluída; docs vivos atualizados | corrigido |
| F22 | auto-descoberta corrigida; contagens vivas alinhadas sem reescrever o estilo do README | revisão cruzada e gate do README | parte factual corrigida; proposta de gosto retirada |
| F23 | errata/ratificação append-only normatizada; ADR-0003 ratificado; ADR-0009 registrado | índice bilateral das decisões | corrigido |
| F24 | requisito mudou para CLI nova 0.205+, preferindo 1.0+ GA | documentação oficial Azure Databricks | corrigido |

## Classe de defeito incorporada

**Gate de propriedade substituída:** o instrumento mede um substituto fácil e
apresenta o resultado como se tivesse testado a propriedade real. Exemplos desta
rodada: contar pastas em vez de conferir nomes exatos; procurar constantes iguais
em vez de comportamento igual; aceitar qualquer exceção em vez da assinatura do
bloqueio; encontrar um literal em qualquer lugar em vez de provar o contrato de
dados.

Critério preventivo: toda guarda nova deve declarar a propriedade, construir um
mutante que a viola mantendo o proxy intacto e provar que esse mutante reprova.

## Validação final e artefatos locais

- `validate_assistant.py`: **0 falhas e 0 avisos**;
- biblioteca: **21/21 testes conhecidos aprovados**;
- ferramentas: **14/14 mutation tests aprovados**;
- sintaxe: **219 arquivos Python** analisados por AST;
- higiene: `git diff --check` aprovado e **0** `__pycache__`/`.pyc` no escopo;
- render: **315 arquivos de produto** sob `Users/usuario-free/` (mais o marcador
  da raiz derivada), sem escrita manual no espelho;
- pacote de implantação para revisão: `.artifacts/ambiente-databricks-<commit>-dirty.zip`,
  SHA-256 `31181A2BA12037EB3BD391261429B0FCBEB072C2DECD0F2B5BFA60149F36C1CC`;
- contexto de auditoria de segurança: `.artifacts/auditoria-security-dirty.txt`,
  SHA-256 `B35ADACCF9AD21B7E03CDD6AB3787B652461077BC6EB059D42734DC074D4CDAA`.

Os dois artefatos levam `dirty` no nome porque representam a árvore corrigida
ainda não commitada. Servem para revisão e ingestão de contexto; o ZIP de
implantação limpo deve ser regenerado depois do commit aprovado.

## Limites remanescentes

- O smoke test modificado ainda não foi reexecutado no Databricks Free nem no
  ambiente de trabalho. `pit_join`, amostragem distribuída, MLflow e o conjunto
  de bibliotecas opcionais continuam com risco de integração/runtime.
- As 16 respostas reais dos notebooks de prompt e os 3 forward tests de
  `hub-ml-criar-objeto` dependem de interação humana e continuam pendentes.
- Validação local e AST não substituem Unity Catalog, permissões, Spark Connect,
  MLflow nem versões instaladas no runtime alvo.
- Commits anteriores ainda carregam o antigo path pessoal do simulado. O pacote
  mínimo não leva Git; clone completo permanece bloqueado até reescrita de
  histórico coordenada com quem já possui clones/remotos.

## Fontes oficiais

- [Databricks CLI](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/)
- [Custom instructions no Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Agent Skills no Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
