# Auditoria da implantação do plano consolidado — Codex

Data: 09/09/2026. Autor: Codex. Referência: branch `claude/plano-consolidado-2026-09-08`, commit `9e9fa788c6c8058e2beeb7b84ec3aeeae30ff4fe`. Comparação: `bdf33ee10c788fd7afb854175b62037ed0aaf800`.

## Parecer executivo

**A implementação avançou de forma substancial, mas o plano ainda não está encerrado.** O defeito temporal original foi corrigido. Há comparação de conteúdo remoto, guarda fonte–espelho, teste PIT mais forte, proteção inicial do CSI e um executor de CI local. Reexecutei os gates locais com sucesso.

Encontrei três inconsistências reproduzidas localmente, além de lacunas de teste e documentação: descarte silencioso de métrica inválida, perda de coluna de entrada no helper temporal e diferença entre o conjunto filtrado pela guarda e o diretório entregue à publicação. Não observei erro de publicação em um workspace real; a última reprodução usa CLI simulada e demonstra a passagem do diretório sem filtragem pelo código local.

A implementação está na branch do Claude. A `main` permaneceu no commit anterior durante esta auditoria. Não houve merge nem alteração funcional nesta rodada. Os documentos acrescentados registram esta revisão de segunda origem; não constituem consenso A2 nem autorização de adoção corporativa.

## Escopo e evidência

Obtive os 917 arquivos da referência, conferindo os hashes dos blobs Git. Examinei o diff dos componentes alterados, os testes, `.gitattributes`, o handoff, a documentação de execução e os contratos envolvidos. Fonte e espelho contêm 316 arquivos implantáveis cada, idênticos.

Execução local em Python 3.12.14, pandas 2.2.3 e NumPy 2.3.5, após instalar as dependências de teste declaradas:

| Verificação | Resultado |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python tools/ci_local.py --verbose` | 3 etapas aprovadas |
| Biblioteca | 37 testes aprovados |
| Ferramentas | 23 testes aprovados |
| Validador antes de acrescentar esta auditoria | 0 falhas, 0 avisos; 741 arquivos e 353 links no escopo do repositório |
| Contraexemplo de datas textuais | Lags corrigidos: dia 2 recebe 1; dia 10 recebe 2 |
| Fonte versus espelho | 316/316 idênticos |

Não reexecutei Spark, exportação de conteúdo no Databricks, conversação Genie Code ou aceite corporativo. O teste PIT em PySpark 3.5.3 é evidência registrada pelo Claude, não execução desta sessão. A falta de Plotly inicialmente encontrada nesta máquina foi resolvida pela instalação das dependências; não é defeito do projeto.

## Situação dos pacotes do plano

| Pacote | Avaliação |
|---|---|
| T0 — EOL | Política implementada com exceção para material congelado. Diagnóstico Windows registrado; não reproduzido nesta máquina. |
| T1 — temporal | Defeito original corrigido, contrato explícito e dez testes adicionais; há colisão residual de coluna interna, R02. |
| T2 — PIT | Avanço real de cobertura e mutantes registrados; comparação exata de todas as linhas ainda incompleta, R04. Free pendente. |
| T3 — escopos/documentação | Parcial, como o handoff admite. Validador não mudou; inventário versionado e separação do README remoto continuam pendentes. |
| T4 — conversacional | Pendente por acesso; não inferir disponibilidade pela data da cota antiga. |
| T5 — publicação | Comparação de conteúdo implementada e testada por simulação; ainda sem evidência remota nova. Fechar conjunto publicado e proveniência. |
| T6 — integração/CI/CSI | Executor local e mapeamento de métricas implementados; não há workflow remoto versionado. Ajustar descarte de métrica e validar limite CSI. |
| T7 — aceite final | Pendente: publicação da versão corrigida, smoke no Free e no destino. |

## R01 — métrica inválida desaparece e o monitor pode ficar saudável

**Prioridade P1 para monitoramento; reprodução local.**

Em `hub_snippets/ml/performance_monitor/performance_monitor.py`, função `selecionar_metricas_do_relatorio`, valores não numéricos, booleanos e não finitos são descartados com `continue`. Se houver qualquer outra métrica válida, o retorno é aceito. O teste da biblioteca com AUC NaN confirma intencionalmente esse comportamento.

Reprodução:

```python
selecionadas = selecionar_metricas_do_relatorio({'auc_roc': float('nan'), 'ks_pct': 40.0})
# {'ks_pct': 40.0}
monitor = PerformanceMonitor(selecionadas)
monitor.add_period('p1', selecionadas)
# get_current_status(): Saudável
```

O helper resolve o esquecimento da AUC por diferença de nome, mas reintroduz uma ausência silenciosa quando a AUC é inválida no baseline. O monitor não sabe que ela deveria existir. Se a AUC já estiver declarada no baseline, o contrato de completude do monitor pode detectá-la em períodos posteriores; o problema demonstrado é a seleção inicial.

**Correção:** descartar métricas sem política pode ser legítimo; métrica selecionada pela política com valor inválido deve gerar erro ou diagnóstico explícito de incompletude. Permitir exclusão apenas por decisão declarada. Não exigir automaticamente todas as métricas da política genérica, que mistura classificação e regressão. Definir as métricas obrigatórias da tarefa. Detectar também aliases conflitantes, como `auc` e `auc_roc` com valores diferentes.

**Aceite:** o exemplo não pode retornar um monitor saudável sem sinalização; ausência deliberada e valor inválido são distinguíveis; testes cobrem baseline e atualização.

## R02 — coluna interna apaga dados do chamador

**Prioridade P2; reprodução local.**

Em `hub_snippets/ml/lgbm_temporal/lgbm_temporal.py`, linhas 169–175, o código atribui a chave temporal a `__hub_ordem` e depois remove a coluna. Uma entrada que já possua esse nome perde a coluna silenciosamente.

Reproduzi com datas 1/2/10 de janeiro, valores 1/2/10 e `__hub_ordem=['a','b','c']`. O lag ficou correto, mas a coluna original não apareceu no resultado. O nome não está declarado como reservado nem é recusado. `__hub_data`, usado na tabela de grão, também merece proteção contra colisão com chaves de entidade.

**Correção:** usar nome temporário comprovadamente ausente, ordenar por índice posicional auxiliar, ou recusar colisões com mensagem explícita. Preservar todas as colunas não pertencentes às saídas declaradas.

**Aceite:** uma entrada com cada nome interno preserva seu conteúdo ou falha antes de alterá-lo; o contraexemplo temporal continua correto e o DataFrame original não sofre mutação.

## R03 — guarda e operação de publicação examinam conjuntos diferentes

**Prioridade P2; reprodução local com chamada externa simulada.**

`conferir_fonte_espelho` ignora caches e sufixos temporários nos dois lados. `local_tree` lista todos os arquivos e `cmd_plan` entrega a raiz inteira a `workspace import-dir`. Assim, a aprovação da guarda não comprova que só o conjunto filtrado será enviado.

Na reprodução, fonte e espelho tinham dois arquivos iguais; acrescentei apenas ao espelho `.assistant/__pycache__/extra.pyc`. A guarda devolveu lista vazia de divergências. O caminho `cmd_plan(..., executar=True)` retornou sucesso e chamou `import-dir` sobre a raiz contendo o extra. A CLI foi simulada: não afirmo que observei o upload remoto desse arquivo.

**Correção:** montar um staging temporário exclusivamente a partir do inventário aprovado e publicar esse staging; ou reprovar extras no espelho antes da escrita. Não confiar em um filtro não demonstrado da CLI. Compartilhar esse inventário com o bundle e o verify. Higiene da fonte pode ignorar caches, mas isso não autoriza sua presença no pacote.

**Aceite:** mutantes com cache, temporário e arquivo não autorizado não chegam à chamada de upload; nenhuma escrita acontece antes da validação completa.

## R04 — teste PIT ainda não compara o multiconjunto inteiro

**Prioridade P2, cobertura de teste; inspeção do código.**

`t_pit_join_preservacao` confere total, categorias, duas linhas C1 e valores das demais chaves. Porém, para C2/C3/C4/chave nula, faz apenas `all(valor is None for valor in valores)`. Uma lista vazia satisfaz essa expressão. Datas coletadas também não são comparadas ao esperado.

Um mutante que retire C2, duplique C3 e preserve o diagnóstico original pode manter total e C1 corretos e passar pelas verificações restantes. Isso é lacuna do teste, não demonstração de defeito atual do `pit_join`.

**Correção:** comparar um `Counter` de tuplas completas esperadas com o da saída, incluindo chave, data e feature, e manter as asserções de diagnóstico. Acrescentar mutantes fora de C1 e mutante de data.

**Aceite:** perdas/duplicações de qualquer linha e mudanças indevidas de data reprovam. Reexecutar no Free; o teste local registrado continua válido dentro de seu alcance.

## R05 — limite de cardinalidade não tem validação de tipo e finitude

**Prioridade P2 de robustez, especialmente se vier de configuração; inspeção.**

`calcular_csi` repassa `max_categorias` sem validar. A proteção depende de `max(n_base, n_atual) > max_categorias`. Com NaN ou infinito positivo, a barreira deixa de barrar cardinalidade elevada. A anotação `int` não aplica validação em runtime.

O padrão 1000 protege o caso usual; não há OOM observado nesta análise. A guarda também limita quantidade de categorias, não bytes totais ou custo do shuffle.

**Correção:** exigir inteiro positivo, rejeitar bool, NaN, infinito e valores incompatíveis antes de ações Spark. Adicionar casos de baixo/alto limite e provar que `collect` não ocorre no caso recusado. Documentar que dois períodos podem somar até duas vezes o limite em categorias distintas.

**Aceite:** entradas inválidas falham antes de contagem/coleta; caso normal preserva resultado; alta cardinalidade é bloqueada no runtime testado.

## R06 — documentação de migração KS contém informação histórica invertida

**Prioridade P2 documental pelo risco de conversão indevida.**

O novo docstring de `performance_monitor.py` diz que o antigo `metrics_report` devolvia KS em fração e que a escala mudou. Na referência antiga auditada, `_calculate_ks` já multiplicava por 100. A correção preservou a escala do relatório, mudou a chave para `ks_pct` e ajustou a política do monitor para pontos percentuais.

**Correção:** explicar a migração de chave e limiar sem mandar converter valores que já estavam em 0–100. Não reabrir o cálculo KS, que continua correto.

**Aceite:** exemplo de migração mantém KS 40 como 40; documentação e testes concordam com o histórico.

## Pendências já conhecidas e aperfeiçoamentos de proveniência

O handoff é honesto ao deixar T3/T4/T7 abertos. Entretanto, sua ordem para T3 deve incluir explicitamente separar a conferência remota do README: corrigir apenas o escopo de contagem não elimina a dependência de autenticação de `--conferir-readme`.

O handoff informa 741/347; o checkout examinado produziu 741/353 antes desta documentação. O README ainda contém números mais antigos. Registrar contagens com commit/escopo; não recapturar números como se isso resolvesse a causa.

`ci_local.py` é um executor útil, não uma automação instalada no GitHub. Dependências com pisos e sem teto não reproduzem uma combinação exata; guardar versão testada/constraints e testar compatibilidade mínima se ela for prometida. O pré-check usa descoberta de módulo, não importação nem verificação de versão; os testes subsequentes continuam sendo a prova efetiva de execução.

A comparação remota é nova e ainda precisa de rodada real com FILE e NOTEBOOK, conteúdo divergente e falha de exportação. Seus testes locais substituem `_exportar_remoto`, portanto não validam por si sós o protocolo da CLI/base64. Acrescentar testes de parsing e integração.

A proveniência também pode melhorar: `_commit_atual` usa Git relativo ao diretório corrente, aceita commit desconhecido e não trata erro de `git status` como estado indeterminado. A saída imprime hashes agregados abreviados, diferentes do hash do ZIP, sem manifesto persistente por arquivo nesta rotina. Isso não anula a comparação individual implementada, mas limita a evidência durável. Reutilizar manifesto e registrar SHA completo, estado da árvore e escopo com erro explícito quando não puder certificá-los.

## Plano de correção e implantação

| Ordem | Entrega | Critério de aceite |
|---|---|---|
| 1 | R01 + R06: contrato de métricas e migração | Métrica obrigatória inválida não desaparece; KS não sofre conversão indevida. |
| 2 | R02: nomes internos temporais | Colunas do usuário preservadas; testes temporais verdes. |
| 3 | R03 e proveniência da publicação | Somente inventário aprovado chega ao upload; fonte, espelho e manifesto concordam. |
| 4 | R04 + R05: PIT e CSI | Multiconjunto completo verificado; limite inválido falha antes de ação Spark. |
| 5 | Concluir T3 | Contagens versionadas reproduzíveis, higiene local separada, README local sem credenciais. |
| 6 | Atualizar fonte, exemplos e derivado | APIs/contratos coerentes; render pelo script; gate local aprovado. |
| 7 | Validar no Free | Publicação de commit identificado, verify por conteúdo, smoke novo e testes conversacionais afetados. |
| 8 | Aceite no trabalho | Pacote mínimo, permissões, runtime e MLflow verificados no destino; evidência sanitizada. |

Para o executor: trabalhar na branch correta ou em branch derivada dela; preservar mudanças do Claude; acrescentar regressões antes de alterar cada comportamento; registrar decisões e resultados no CHANGELOG; não atualizar manualmente o espelho. Não usar os 37/23 testes como meta fixa: novos casos devem reprovar os contraexemplos acima.

Ao concluir, atualizar o handoff com estado por pacote, commit e ambiente de teste. A publicação deve ocorrer após a versão final estar identificada; o verify precisa usar a mesma origem, perfil e host. Executar em sessão nova quando necessário para não confundir módulos já carregados com o conteúdo recém-publicado. Manter rollback e não transportar o histórico Git ao corporativo por uma rota ainda não autorizada.

## Limites do parecer

Nenhum dos achados acima autoriza afirmar que houve perda de dados corporativos, upload indevido efetivo ou falha em produção. São reproduções locais e lacunas de contrato/cobertura identificadas no código. Não foi feita auditoria completa de todos os módulos inalterados. A aprovação dos gates locais e o mérito das correções permanecem reconhecidos; o encerramento do plano depende das correções e evidências indicadas.
