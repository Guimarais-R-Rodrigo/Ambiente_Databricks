# B1 — pacote de skills isolado do controller

(Codex) Este pacote parte de `main` em `4ba7f551` e reutiliza os arquivos
de produto do candidato `c7e9f3da` (#117). Inclui as oito skills de execução
B1, as regressões proporcionais nas demais skills, o contexto MM04 escolhido
pelo usuário, runners, verificadores, testes e evidências sintéticas. O
derivado `Novo_Ambiente_Simulado/` foi gerado com
`python -B tools/render_simulado.py --write` a partir de `ambiente_fonte/`.

O empacotamento exclui `.codex/`, hooks, papéis do controller,
`docs/operations/`, ADRs do controller, o state source `PARALELO/B1` e o
framework congelado de execução G6. O manifesto literal de prompts G6 é
mantido apenas como referência histórica dos documentos da Genie. A
configuração humana não commitada em `C:\b1_runtime\b1_p1_4ba7f551_20260924`
permanece intacta. #115 e #117 também permanecem intactos e em rascunho;
o [PR #118](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/pull/118)
substitui seu uso como pacote de integração B1.

## Evidência e limites

- `validate_assistant.py --conferir-readme` passou com zero falhas/avisos em
  checkout limpo do commit `2beeb8b5`. No mesmo checkout, após instalar 25
  pacotes Node do cache **offline**, `tools/ci_local.py` passou nas 10 etapas:
  temas, validação, SEF, biblioteca, ferramentas, transição, READMEs e três
  gates de Concierge. O gate local não cobre Databricks, Spark ou Genie.
  Caches `__pycache__` do worktree de autoria são ignorados pelo Git e geram
  apenas um aviso transitório ali. O conteúdo de produto não mudou em relação
  ao snapshot `c7e9f3da`.
- `unittest` local sem Spark/SHAP: 109 testes, OK, um skip. Dois oráculos de
  SER12 foram ajustados para aceitar as duas casas decimais possíveis no
  exato limite de meia unidade; o verificador independente já aceitava ambas
  e vincula a decisão ao valor efetivamente reportado. O código do produto
  SER12 não foi alterado por esse ajuste.
- Testes que exigem `pyspark`, `jdk4py` ou `shap` ficaram `NOT_RUN` neste
  ambiente. As provas anteriores de Delta/FE/SER03/SER05 pertencem às versões
  documentadas nas fichas B1; não são substituídas por este empacotamento.
- O job principal [`validar` do PR #118](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/36786781333)
  passou no HEAD `6b055225`. SE01, MM01 e três regressões de base também
  passaram. Oito workflows temáticos foram cancelados após iniciar para
  poupar saldo; SE02 ficou `SKIPPED` pela configuração. O HEAD documental
  posterior não modifica bytes do produto e é conferido localmente.
- A publicação Free e os testes Genie já registrados conservam seus limites:
  readback de conteúdo não prova execução da Genie; nenhuma das 14 skills foi
  homologada integralmente nesta campanha. O G6 R7 congelado segue
  incompleto e não é promovido por este pacote.

O escopo tem **aceite parcial**; o estado de integração é o do PR #118.
Policy e Databricks corporativo seguem gates separados. A reconciliação do
PR #116 de Micromodelos vem depois do B1, conforme a ordem escolhida.
