# Handoff — plano consolidado, pacotes T0 a T6

Data: 2026-09-09 · De: sessão Claude (Cowork) · Para: qualquer IA ou pessoa que continue o plano

## Estado atual

Branch `claude/plano-consolidado-2026-09-08`, publicado em `origin`, com seis commits
e os gates locais verdes na máquina do laboratório (Python 3.12.10):

```text
validate_assistant.py : APROVADO, 0 falha(s), 0 aviso(s)
repo (identidade)     : 741   |  repo (links): 347
render_simulado.py    : 317 arquivos
ci_local.py           : 3 etapas OK — validador, 37 testes, 23 guardas
```

| Pacote | O que entrou |
|---|---|
| T0 | `.gitattributes` (`* text=auto eol=lf`, `Ajustes_Codex/** -text`) e 648 arquivos normalizados de CRLF para LF, em commit isolado e sem alteração funcional |
| T1 | `hub_snippets/ml/lgbm_temporal`: a data é convertida antes de `sort_values` e independe de `calendar_features`; contrato de formato declarado; 10 testes novos |
| T2 | `t_pit_join_preservacao` em `tools/spark_smoke_test.py`: compara com `fatos.count()`, multiplicidade por entidade e valor escolhido linha a linha |
| T5 | `tools/publicar_free.py`: `--verify --conteudo`, `conferir_fonte_espelho` antes de qualquer escrita, hash bruto e hash normalizado registrados separados |
| T6 | Guarda de cardinalidade no CSI categórico, `selecionar_metricas_do_relatorio`, e o gate local `tools/ci_local.py` com `tools/requirements-dev.txt` |
| T3 (parcial) | Checklist e runbook de replicação reconciliados, contexto do Free datado, `.gitignore` |

Evidências datadas: [diagnóstico de EOL](../testes/2026-09-08_diagnostico-eol.md) e
[preservação de linha no `pit_join`](../testes/2026-09-08_pit-join-preservacao.md).
O detalhamento por arquivo está no [changelog](../../CHANGELOG.md), seção 2026-09-08.

## Em andamento / bloqueado

**O escopo do validador continua sendo o item mais importante em aberto.**
`REPO_IGNORE`, em `tools/validate_assistant.py`, é um conjunto fixo — `.git`,
`.artifacts`, `Ambiente_Antigo`, `Ajustes_Codex`, `__pycache__`, `.venv` — e **não lê
o `.gitignore`**. Qualquer arquivo local não versionado entra na contagem certificada.
Duas manifestações observadas do mesmo defeito:

- uma pasta gerada por ferramenta externa na raiz levou `repo (identidade)` de 741 a 742;
- o `GUIA_REPLICACAO_TEMPORARIO.md`, que é git-ignored, explica por que um checkout
  limpo conta 736/345 enquanto a máquina de origem contava 737/347.

Enquanto isso não for separado em inventário versionado, higiene da worktree e
inventário do pacote publicável, o número certificado depende do que existe na máquina.
A recaptura do bloco de saídas de referência do `README.md` raiz depende disso: os
números colados lá ainda são os antigos.

Bloqueado por acesso, não por código:

- os 3 casos de roteamento da `hub-ml-criar-objeto` e as 16 famílias de prompts
  ([forward tests](../testes/forward/README.md)). A cota registrada em agosto está
  **pendente de revalidação** — testar a disponibilidade, nunca inferir por decurso de prazo;
- a replicação no workspace corporativo ([runbook](../playbooks/replicacao-trabalho.md));
- reexecutar `t_pit_join_preservacao` no Free, em Spark 4.2.0. A rodada desta sessão foi
  em PySpark 3.5.3 local, porque a máquina disponível só tinha Java 11, que não roda
  Spark 4. É evidência sobre o código, não sobre o runtime de destino.

## Decisões tomadas nesta sessão

- **Data em texto no `lgbm_temporal`:** ano-mês-dia é convertido automaticamente, porque
  a ordem dos campos não é ambígua; qualquer outro formato exige `date_format` explícito.
  Nenhuma inferência silenciosa de dia/mês contra mês/dia.
- **Empate no grão entidade+data** passa a levantar erro por padrão, porque o lag ficaria
  dependente da ordem de entrada. `on_duplicate_dates='keep'` aceita, com ordenação estável.
- **Normalização da comparação de conteúdo é mínima e declarada:** fim de linha, e fim de
  arquivo apenas em notebook. Comentário, espaço e linha em branco permanecem — removê-los
  mascararia diferença real, que é o que a comparação existe para achar.
- **O gate local não toca no Databricks.** Publicação, verify remoto, smoke e testes
  conversacionais são etapas próprias, com evidência datada.
- **`--verify` sem `--conteudo` declara o próprio alcance** em toda rodada, para que
  "conferido" não seja confundido com "conteúdo igual".
- Nenhum ADR novo foi necessário: as escolhas acima são implementação dentro dos ADRs
  vigentes ([índice](../decisions/README.md)).

## Próximos passos recomendados (em ordem)

1. Separar o escopo do `validate_assistant.py` em inventário versionado (`git ls-files`),
   higiene da worktree e inventário do pacote. Falha do Git reprova; nunca vira conjunto
   vazio aprovado.
2. Recapturar o bloco de saídas de referência do `README.md` com
   `python tools/validate_assistant.py --conferir-readme`, já com o escopo corrigido.
3. Rodar os 19 cenários conversacionais em chats novos e registrar o resultado datado,
   incluindo falhas e bloqueios.
4. Publicar no Free a partir de HEAD limpo e conferir com `--verify --conteudo`.
5. Reexecutar o smoke no Free, em Spark 4.2.0, cobrindo `t_pit_join_preservacao`.
6. Executar a replicação no trabalho pelo runbook, com aceite próprio de runtime,
   permissões e MLflow no destino.
7. Decidir as duas dívidas nomeadas do [PLANO_HUB](../../PLANO_HUB.md) §12.2 e §12.3:
   a paleta divergente de `ml/curves_plotly` e as cinco funções públicas em português.

## Armadilhas conhecidas

- **`api_publica.py` gera `__init__.py` em ordem de definição no módulo**, não alfabética.
  Escrever à mão reprova no validador. E no PowerShell 5.1 o operador `>` grava UTF-16:
  regenerar por redirecionamento corrompe o arquivo. Prefira gravar sem BOM e em LF.
- **No Windows, `Path.write_text` traduz `\n` para CRLF.** Fixture de teste gravada assim
  mede a tradução do sistema operacional em vez do contrato — use `write_bytes`.
- **Subprocesso Python no Windows escreve no code page do console.** Decodificar como
  UTF-8 estrito mata a thread leitora do `subprocess`: a etapa reprova com a saída vazia e
  a causa fica invisível. Passe `PYTHONUTF8` ao filho e tenha fallback de locale.
- **`PerformanceMonitor` recusa alto** um relatório inteiro como baseline. O risco
  silencioso é o contorno óbvio: filtrar só as chaves de nome coincidente deixa a AUC de
  fora, porque o relatório a chama de `auc_roc`. Use `selecionar_metricas_do_relatorio`.
- **Casar objeto remoto por `endswith` depende da ordem de iteração e do separador de
  path.** `.../exemplo_modulo` termina em `modulo`. Monte um mapa explícito.
- **A invariante que soma categorias e compara com o total** prova completude de rótulo,
  não preservação de linha: perder uma linha e duplicar outra mantém a soma. Compare
  sempre contra a contagem da entrada.

## Revisão de segunda origem — 09/09/2026 (Codex)

O estado acima é preservado como relato da implementação. A [rodada Codex](../auditoria/2026-09-09_implantacao-plano/02_codex.md) revisa o commit `9e9fa78`, confirma os gates locais e registra achados residuais e plano de correção. Consultá-la antes de encerrar T1, T2, T5 ou T6 e antes de retomar publicação. O escopo do validador, os testes conversacionais e o aceite no destino continuam pendentes. Não há consenso formal registrado nesta adição.

## Implementação posterior — Codex, 09/09/2026

As correções da revisão e a separação de escopos T3 foram implementadas.
O [novo handoff](2026-09-09_correcoes-codex.md) é a entrada para retomar a execução;
o texto acima preserva o estado anterior. Gates remotos continuam pendentes.
