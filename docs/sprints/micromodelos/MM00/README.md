# MM00 — Baseline e arquitetura

## Objetivo

Registrar o estado real do repositório e congelar as fronteiras da iniciativa antes de qualquer implementação funcional.

## Baseline e reconciliação

O detalhe mutável do estado de fechamento pertence ao `CHECKPOINT.md`. Esta seção preserva somente os marcos necessários para reconstruir a cronologia sem transformar snapshots intermediários em estado corrente.

- Branch: `micromodelos/mm00-baseline`.
- Base de abertura: `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.
- Na abertura, V00–V07 do Sistema de Temas estavam integradas no Git.
- Durante a MM00, a V08 foi integrada na `main` pelo commit `622d2c962a80998cf990b57036f7ae503bfc0458`.
- O fechamento documental pós-merge da V08 levou a `main` a `55f7006c47d90ae7f760992d252b658f53a59636`.
- A reconciliação final da MM00 sobre essa base ocorreu no merge `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`.
- O snapshot técnico `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843` passou CI geral, V00, V01 e V02 antes da auditoria A1.
- A auditoria A1 independente verificou esse head contra a `main` `55f7006c...` e devolveu `APTA_COM_CORRECOES`: Q-01 para o `CHANGELOG.md` e M-01 para esta cronologia. Nenhuma quebra funcional ou divergência arquitetural material foi reportada.
- As correções pós-A1 devem ser revalidadas antes do aceite; snapshots anteriores continuam evidência histórica, não autorização para avançar.

A integração V08 permanece a fonte vigente do Sistema de Temas; a MM00 não altera seus arquivos funcionais.

## Entregas

- `INVENTARIO.md`
- `MATRIZ_REUSO.md`
- `MATRIZ_RISCOS.md`
- `MATRIZ_DEPENDENCIAS.md`
- `TESTES.md`
- `CHECKPOINT.md`
- ADRs da iniciativa
- pacote da auditoria A1 e seu resultado independente

## Fora do escopo

MM00 não cria skill, prompt funcional, helper, template executável, consulta de dados, run MLflow, Produto de Dados, micromodelo real nem migração de legado.

## Sanitização

Arquivos versionados usam placeholders para nomes do ambiente de trabalho, por exemplo `<CATALOGO_PRODUTO>`. O vínculo com nomes reais ocorre somente no ambiente autorizado.

## Relação com V08

V08 integra o Sistema de Temas transversalmente a skills, padrões e Manual. Isso é uma dependência vigente para futuras skills do Hub, mas não transforma aparência em regra analítica. O desenho dos micromodelos continua sem tema próprio e a composição visual específica permanece adiada para a fase de hardening, quando será validada contra o contrato vigente.

## Gate

MM01 permanece bloqueada até: correção dos achados A1 procedentes; CI verde no head corrigido; `CHANGELOG.md` conforme a regra do projeto; reconsulta da `main`; aceite explícito; e merge da MM00.
