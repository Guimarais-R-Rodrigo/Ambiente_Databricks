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
- A reconciliação MM00 sobre essa base ocorreu no merge `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`.
- O snapshot técnico `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843` passou CI geral, V00, V01 e V02 antes da auditoria A1.
- A auditoria A1 independente verificou esse head contra a `main` `55f7006c...` e devolveu `APTA_COM_CORRECOES`: Q-01 para o `CHANGELOG.md` e M-01 para esta cronologia. Nenhuma quebra funcional ou divergência arquitetural material foi reportada.
- Depois da A1, a frente visual avançou novamente: V09 foi integrada pelo PR #45 em `0f7234c4734f1974ebb1a20123f3c26626c67ef3` e a correção de preparação Node pelo PR #46 levou a `main` a `4ae714a35a0aafd930a8cd796d962b0a79449b88`.
- A MM00 foi reconciliada com essa `main` V09 pelo merge de dois pais `922ae38491cb7a502b834b092ea637620b54300a`, preservando os arquivos funcionais da V09 e reaplicando somente a documentação própria da MM00 e os documentos compartilhados necessários.
- O gate dessa composição mediu 1374 arquivos e 1859 links; a falha do CI geral ocorreu somente porque o README raiz ainda continha as métricas da `main` V09 isolada. V00, V01 e V02 permaneceram verdes.
- As correções pós-reconciliação devem ser revalidadas antes do aceite; snapshots anteriores continuam evidência histórica, não autorização para avançar.

V09 é a fonte vigente da frente de temas/transição. A MM00 não altera seus arquivos funcionais.

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

## Relação com o Sistema de Temas

V08 integrou o Sistema de Temas transversalmente a skills, padrões e Manual; V09 levou seu contrato ao kit offline de transição. Essas são dependências vigentes para futuras skills do Hub, mas aparência e transporte não se tornam regras analíticas. O desenho dos micromodelos continua sem tema próprio e a composição visual específica permanece adiada para a fase de hardening, quando será validada contra o contrato então vigente.

## Gate

MM01 permanece bloqueada até: correção ou exceção humana explícita do Q-01 do `CHANGELOG.md`; CI verde no head corrigido; reconsulta da `main`; decisão explícita sobre ADR-0014 a ADR-0020; aceite da MM00; e merge.