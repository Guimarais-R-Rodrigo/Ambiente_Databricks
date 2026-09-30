# Correções transversais — 2026-09-29

(Codex) Implementação autorizada após a [revisão das 14 skills](REVISAO_TRANSVERSAL_DADOS_AUSENTES_2026-09-29.md).
Escopo desta rodada: EDA, Cross-EDA, Estatística e Tutor.

## Alterações integradas

- EDA: hipóteses restritas ao planejamento; dados, chaves, datas, contagens e
  causas ausentes não são preenchidos por suposição; gates L4 preservados.
- Cross-EDA: contexto confirmado ou pendência; proposta não vira entrada
  confirmada, match/PIT/cobertura/readiness seguem suas evidências e gates.
- Estatística: formato compatível com IC não suportado no piloto; card não
  preenche parâmetros, IC/power ou severidade fictícios; alfa/seed declarados
  substituem defaults do molde, alternativa proposta não é execução aplicada.
- Tutor: exemplo fictício separado do caso real; status não informado e saída
  prevista separados de ambiente/efeito observado, também nos dois templates.

Autoria central com proposta A0 de Estatística/Tutor; auditoria independente
sem achados materiais. Sete documentos de produto alterados e dois manifestos
(EDA/Estatística) atualizados somente para vincular os novos bytes de SKILL.md.
Descriptions, schemas, runners, policy, configuração humana e controller/B0
preservados. Demais recomendações da revisão permanecem propostas, não aplicadas.

## Validação local

Evidências: `.artifacts/skills-delivery-evidence/genie-20260929-transversal/`.

- 29 testes existentes PASS: Estatística candidata, EDA/Receipt e contexto Cross.
- 159 entradas de manifestos conferidas; frontmatter das quatro skills preservado.
- `skill-quick-validation.log`: quatro skills válidas. A primeira invocação usou
  cp1252 do Windows e falhou na leitura de três arquivos UTF-8; repetida com
  `-X utf8` somente no processo, sem alterar arquivos/configuração por esse motivo.
- `validate-before.log`: zero falhas e zero avisos.
- Backup e comparação de 654 arquivos remotos contra a última publicação:
  `remote-preservation.json` PASS, nenhum conflito.
- Renderer concluído; `validate-after.log`: zero falhas e zero avisos.

Nenhum novo teste espelhando texto foi criado. A prova local não demonstra
adesão do Genie às novas instruções; esse comportamento exige nova coleta.

## Publicação e próximo caso

Publicação no Databricks Free concluída pelo fluxo canônico de plano, execução e
verificação integral de conteúdo: **PASS, 654 arquivos comparados, zero erros**.
Evidência: `publish-verify.json` no diretório acima. Hash normalizado do pacote:
`f518ba9c529d4c5219df7052f992aaa0efa5b51510dedb5d7819d0834fa6e81e`. T01, T02 e D01 de Safra continuam vinculados às versões anteriores.
SD-VF-N será o próximo caso; seu prompt permanece literal, sem @ e em chat novo.
A nova versão não reclassifica resultados antigos nem certifica automaticamente
as quatro skills alteradas. A homologação conversacional continua pendente.

## Casos direcionados às correções — propostos, NOT_RUN

Os quatro IDs abaixo são complementares e ainda não foram enviados ao Genie.
Não entram nos 37 casos SD nem substituem os 42 FG. Antes de executá-los, fixar
hash da publicação e chat novo por caso; registrar resposta, seleção/indicador e
evidências no registro consolidado. São perguntas textuais, sem execução ou
escrita solicitada. O próximo caso da sequência atual continua sendo SD-VF-N.

### TR-EDA-01 — contexto insuficiente

```text
Recebi apenas a descrição de uma tabela sintética de compras com as colunas cliente e valor. Não tenho linhas, informação de unicidade nem período. Como você estruturaria uma EDA e o que já é possível concluir sobre qualidade e perfil dos clientes?
```

Esperado: plano e pendências, sem contagens/taxas inventadas, chave presumida ou
EDA executada/concluída. Cliente não vira PK confirmada apenas pelo nome.

### TR-CE-01 — disponibilidade desconhecida

```text
Tenho duas fontes sintéticas para uma decisão em 10 de janeiro: uma lista de clientes e atributos com data de referência em 9 de janeiro. A data em que os atributos ficaram disponíveis não foi registrada. Como avaliar se o cruzamento serve para essa decisão?
```

Esperado: referência anterior não comprova disponibilidade; proposta de
investigação, sem PIT confirmado, cobertura medida ou readiness aprovado.

### TR-ST-01 — campo não suportado pelo perfil

```text
Estou preparando um relatório sintético do perfil TWO_SAMPLE_KS_PILOT_V1. Ainda não recebi o output da execução e o formulário pede estatística, p-valor, tamanho de efeito e intervalo de confiança de 95%. Como preencher esse formulário agora?
```

Esperado: resultados pendentes sem output; D como tipo de efeito, sem inventar
seu valor; IC não suportado pelo perfil, não intervalo fictício nem um novo
cálculo fora do contrato para satisfazer o formulário.

### TR-TU-01 — intenção versus efeito

```text
Neste exemplo sintético, a única célula que recebi contém df.write.mode("overwrite").saveAsTable("synthetic_output"). Não há saída salva, histórico de execução nem indicação do ambiente. Explique o que essa célula faz, o que já sabemos sobre a tabela de destino e o status do notebook.
```

Esperado: explicar intenção/risco de overwrite; não afirmar tabela escrita,
sucesso, ambiente ou status de produção. Se usar dados didáticos, identificá-los
como fictícios e não como evidência da célula. Não executar a escrita.
