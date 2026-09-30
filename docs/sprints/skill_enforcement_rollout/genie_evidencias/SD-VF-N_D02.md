# SD-VF-N-D02 — reteste de Monitoramento — 2026-09-29

(Codex) [Resposta literal](SD-VF-N_D02.txt); notebook original preservado em
`.artifacts/skills-delivery-evidence/genie-20260929-monitor-d02/`.
O notebook contém caminho pessoal e não foi versionado nem executado localmente.
SHA256 notebook `f074b37568e34ef2b036169f1be6c3d887e37dec51af12fcafa89190e7fc8153`; resposta `1d0b1ce5189c60b831e3d7aa2d9d51460d91dff28ea2fe5ef81f67cf83f982b8`.
Versão Free esperada: `fe949b83dbf5bc8aa0ba9ff7442328668c408e1d8b253a868f8265d60c34c396`.
O usuário confirmou seleção real de `@hub-ml-monitoramento-modelo` no menu e
indicador de carregamento na interface. Não há inspeção dos bytes carregados
internamente, mas a evidência de roteamento é observável por confirmação humana.

## Vereditos separados

- Roteamento: **PASS observado na interface** para Monitoramento; não forçou Safra.
- Enquadramento: PASS. Tratou o pedido como exploração, sem presumir SER11,
  inventar janelas/IDs ou alegar Receipt.
- Execução exploratória: OBSERVED nas saídas salvas do notebook para os helpers
  `calculate_psi`/`calculate_ks`; sem validação canônica/Receipt porque o perfil
  não foi pedido. HTML do Plotly contém `Plotly.newPlot`; visualização efetiva
  no navegador não foi aferida separadamente.
- Aritmética: PASS. PSI para 2/3/4/10 bins = 0,2746530722 /
  3,2086578970 / 3,2805784151 / 3,2805784151; KS=0,25, p=1.
  Recalculado localmente dos arrays sintéticos, sem executar o anexo. A
  diferença na última casa dos totais bin a bin vem de somar contribuições
  arredondadas antes da soma.
- Interpretação: **FAIL parcial**. Os seis bins vazios nas duas janelas para
  n_bins=10 contribuem zero, apesar de a resposta atribuir-lhes inflação do PSI.
  O bin dominante tem 25% na referência e 0% na atual, suavizado para eps;
  sua contribuição é 3,10729162. A resposta e o markdown qualificam a potência
  do KS como “mínima” sem alternativa, alfa ou análise de potência.
- Severidade operacional: não classificada; sem falsa alegação de performance
  ou recomendação automática de retreino.
- Veredito D02: **FAIL parcial de interpretação**. É diagnóstico fora dos 37 SD
  e 42 FG; T01 e D01 mantêm seus vereditos e versões originais.

Auditoria independente somente leitura confirmou os valores, a saída HTML e
as duas falhas interpretativas. O helper calculou corretamente; não há evidência
de defeito no runner. Um ajuste proporcional foi feito apenas em `SKILL.md` de
Monitoramento: distinguir bins vazios em ambas as janelas dos vazios em um lado
só e não qualificar potência sem estudo específico. O reteste dessa correção
exige publicação conferida e chat novo; nenhum PASS comportamental foi presumido.

## Correção publicada para D03

(Codex) Apenas `skills/hub-ml-monitoramento-modelo/SKILL.md` mudou frente à
publicação anterior. 15 testes SER11/SER12 PASS; validador antes e após renderer
com zero falhas/avisos; skill válida na checagem estrutural. Backup e
comparação de 657 objetos remotos antes do envio: PASS, zero conflitos.
Publicação canônica plano → execute → verify integral: **PASS**, 657 arquivos
comparados, zero erros. Hash normalizado `2965556ecdb3a8a543d93610430da35dba752d2c35fda124e5b389146f847ba8`.
Evidência `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d02/publish-verify.json`.
Comparação dos dois inventários publicados: só SKILL.md de Monitoramento mudou.
D02 permanece vinculado à versão anterior; D03 é NOT_RUN.
