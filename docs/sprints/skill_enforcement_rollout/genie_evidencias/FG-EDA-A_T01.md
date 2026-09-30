# FG-EDA-A/T01 — @ EDA com contexto insuficiente — 2026-09-30

(Codex) Prompt e resposta originais preservados em
`.artifacts/skills-delivery-evidence/genie-20260930-eda-a/response-original.txt`;
SHA-256 `caa360da0740ade12398cb502443ef98de8d6d60359ee99bfeba4e883217cf19`.
O usuário confirmou chat novo,
seleção de `@hub-ml-eda-profissional` no menu e indicador separado de
carregamento. O texto colado começa com `hub-ml-eda-profissional ssional`;
portanto é variante do prompt preparado, não envio literal byte a byte.

## Versão e efeitos

O pacote B1 anteriormente verificado tinha hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
Houve publicação paralela posterior de micromodelos relatada pelo usuário;
a versão remota efetiva não foi conferida nesta coleta. O Genie declarou
skill carregada, mas esta transcrição não contém eventos internos de leitura.
Nenhum notebook, consulta a tabela, output de código ou Receipt foi enviado.

## Vereditos separados

- Roteamento @: **PASS por seleção e indicador confirmados pelo usuário**.
- Limite de evidência: **PASS no núcleo**. A resposta estruturou EDA como
  plano, pediu grão, chave, período e domínio do valor, e recusou concluir
  qualidade, perfil, nulos, contagem ou unicidade sem linhas. Não alegou
  análise executada; o cenário permaneceu sem números inventados.
- Precisão: **FAIL parcial**. Na coluna “Tem”, tratou `valor` como numérico
  e `cliente` como identificador sem schema informado; os nomes são apenas
  pistas. Também disse que, se `cliente` tiver duplicatas, o grão “é compra”,
  quando linhas repetidas não estabelecem sozinhas se a unidade é compra,
  agregado ou outro evento. A expressão “dados reais” para uma fonte
  declarada sintética é imprecisa. O contrato da skill já exige não preencher
  tipo, chave, grão ou dados ausentes por suposição.
- Execução: **NOT_RUN na evidência fornecida**. As sugestões de `GROUP BY`,
  percentis e gráficos são plano futuro, não chamadas observadas.

**Veredito T01: PASS de seleção e da fronteira sem dados; FAIL parcial de
inferências sobre schema e grão.** O objetivo de menção no nome atual foi
observado, mas a correção transversal de não presumir atributos ainda não
foi seguida integralmente. Nenhuma edição de produto ou publicação foi
feita nesta coleta; preserve a resposta como primeira tentativa.
