# SD-VF-N-D04 — reteste de Monitoramento — 2026-09-29

(Codex) Resposta literal e notebook original preservados em
`.artifacts/skills-delivery-evidence/genie-20260929-monitor-d04/`, sem
executá-lo localmente. SHA256 notebook
`5c56f70e72f72c9510c5b021b9c16605c498093e04d2aae463ac14d2f1ffe190`;
resposta `68b942bc9bba0acf00db2f589c1cd053d29b5340d462c3476979b4a541530a4e`.
O texto literal contém caminho pessoal do workspace e fica somente na área
privada de evidências; este resumo é a versão publicável.
Versão Free esperada nesta coleta:
`05f952adfa3c5765f37c3df9e812e3ca430ceb06d91940e575880023e45c68d6`.
O usuário confirmou seleção real da skill no menu @ e indicador de
carregamento. Os bytes internos carregados pelo Genie não foram inspecionados.

## Vereditos separados

- Roteamento: **PASS observado na interface** para Monitoramento.
- Enquadramento: **PASS**. Tratou os arrays como análise exploratória; não
  presumiu perfil SER11, metadados operacionais nem Receipt.
- Execução exploratória: **OBSERVED nas saídas salvas**. O notebook importa e
  chama `calculate_psi`/`calculate_ks` do Hub; contém saídas de métricas e duas
  tabelas HTML com bins. Não há prova separada de renderização na interface,
  nem de execução do perfil canônico SER11.
- Aritmética: **PASS**. Recalculei localmente dos arrays sintéticos com o helper
  da fonte: PSI 10 bins `3,2805784151348854`, PSI 2 bins
  `0,2746530721670274`, KS `0,25`, p `1`. Para 10 bins, as contribuições
  relevantes são `3,107291619994899` na cauda esquerda de 25%→0% e
  `0,17328679513998632` na direita de 25%→50%; as outras contribuem zero.
  Os limites internos são quantis apenas da referência, com caudas infinitas.
- Interpretação: **PASS semântico**. Mostrou sensibilidade a bins e eps, não
  atribuiu PSI aos bins vazios em ambas as janelas, não inferiu potência nem
  ausência de drift de p=1, e não classificou severidade sem política. A frase
  “sem smoothing acionado” em dois bins simplifica o bucket de nulos que recebe
  eps em ambos os lados e contribui zero; não muda o resultado.
- Aderência literal ao contrato anterior: **RESSALVA DO CONTRATO**. O SKILL.md
  pedia bins/contribuições “retornados pelo helper”, mas `calculate_psi`
  retorna somente um float. O Genie construiu e identificou uma decomposição
  manual fiel nesta fixture sem nulos, com totais iguais ao helper. Não seria
  correto chamar isso de bins retornados pela API.
- Veredito D04: **PASS da análise exploratória**, com a ressalva documental
  acima. D03 permanece FAIL na versão anterior. D04 é diagnóstico fora dos 37
  SD e 42 FG; não certifica SER11 nem homologação geral da skill.

A instrução contraditória foi esclarecida na fonte: manter o helper como
cálculo oficial e permitir decomposição didática separada com mesma política,
parâmetros e comparação de soma. 15 regressões PASS, renderer e validador
PASS; pré-checagem remota encontrou somente a diferença prevista. Publicação
e readback integral PASS em 657/657 arquivos, zero erros, hash normalizado
`31adacbeb6d842c04382b8936b23648bc1cbe14cef80a1ff6d55d9819a768b57`.
Evidência `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d04/publish-verify.json`.
Não há falha estatística que peça novo teste de Monitoramento; o próximo caso
guiado pode avançar para Safra `SD-VF-B`.
