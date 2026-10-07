# MM00 — Baseline e arquitetura

> **Nota administrativa — 06/10/2026.** MM00 integrada pela PR #43 em `36e89515`. Gates de candidatura e próxima etapa abaixo são registros daquele fechamento, não pedidos atuais. [Estado e continuidade](../README.md); [módulo distribuído](../../../../ambiente_databricks/.assistant/hub_micromodelos/README.md). FAILs e limites originais permanecem; nenhuma homologação corporativa decorre desta nota.

## Registro histórico preservado

## Objetivo

Registrar o estado real do repositório e congelar as fronteiras da iniciativa antes de qualquer implementação funcional.

## Estado final

**MM00 encerrada e integrada. MM01 é a próxima sprint e não foi iniciada.**

A PR #43 foi aceita explicitamente e integrada na `main` pelo commit `36e89515a46df24f41deea4791b109f5a1f938f2`. O último débito documental da A1, Q-01, foi fechado imediatamente após o merge por inserção estritamente aditiva no `CHANGELOG.md`, com comparação de **22 adições e 0 deleções** contra o merge MM00.

## Baseline e reconciliação

O detalhe mutável do fechamento está consolidado em `CHECKPOINT.md`. Os marcos principais são:

- branch de execução: `micromodelos/mm00-baseline`;
- base de abertura: `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`;
- V08 integrada durante a MM00 e incorporada sem alterar sua implementação;
- auditoria A1 independente sobre `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`, com resultado `APTA_COM_CORRECOES`;
- V09 integrada/fechada durante a MM00 e reconciliada antes do aceite;
- head final aceito: `e3809b15b61f2bc1eeec06c9de6f38a329868e98`;
- merge da MM00: `36e89515a46df24f41deea4791b109f5a1f938f2`;
- fechamento Q-01 em branch separada `micromodelos/mm00-fechamento-pos-merge`, preservando os bytes históricos do changelog.

V09 continua sendo a fonte vigente da frente de temas/transição no baseline da MM00. Nenhum arquivo funcional dessa frente foi alterado pela iniciativa de micromodelos.

## Entregas

- `INVENTARIO.md`
- `MATRIZ_REUSO.md`
- `MATRIZ_RISCOS.md`
- `MATRIZ_DEPENDENCIAS.md`
- `TESTES.md`
- `CHECKPOINT.md`
- ADR-0014 a ADR-0020 aceitos
- pacote da auditoria A1 e resultado independente
- entrada própria no `CHANGELOG.md`, fechando Q-01

## Fora do escopo

MM00 não criou skill, prompt funcional, helper, template executável, consulta de dados, run MLflow, Produto de Dados, micromodelo real nem migração de legado.

## Sanitização

Arquivos versionados usam placeholders para nomes do ambiente de trabalho, por exemplo `<CATALOGO_PRODUTO>`. O vínculo com nomes reais ocorre somente no ambiente autorizado.

## Relação com o Sistema de Temas

O micromodelo continua consumidor do Sistema de Temas, não proprietário de uma camada visual paralela. A composição visual específica permanece para a fase de hardening prevista no Plano Mestre e deverá ser validada contra o contrato vigente naquele momento.

## D1 — Q-01

D1-B autorizou excepcionalmente diferir a entrada MM00 no `CHANGELOG.md` até imediatamente após o merge, porque a primeira rota de substituição integral alterava histórico.

A pendência foi posteriormente fechada por uma operação byte a byte, com workflow transitório auto-removido e comparação final mostrando somente adições no changelog. **D1-B está consumida e encerrada; não vira dispensa permanente da regra de changelog.**

## D2 — ADRs

ADR-0014 a ADR-0020 foram **aceitos sem ressalvas em 14/09/2026** e integrados pela PR #43. O aceite congela as fronteiras arquiteturais, mas não antecipa detalhes próprios de MM01/MM02 e sprints seguintes.

## Gate encerrado

A candidata final passou CI geral, V00, V01 e V02 no mesmo head antes do merge. A auditoria A1 não encontrou `DIVERGE`; M-01 foi corrigido; Q-01 foi fechado pós-merge.

A MM00 está concluída. O próximo passo previsto é **MM01 — contrato canônico `micromodelo.yaml`**, ainda não iniciado.
