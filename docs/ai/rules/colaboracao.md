# Colaboração, revisão e auditoria

## Papeis

Papéis são atribuídos por capacidade, escopo e independência, nunca pela marca do
modelo. Coordenador controla baseline/contratos/integração; executor implementa
lote permitido; revisor não escreveu o lote; auditor verifica o conjunto final.
O padrão tem origem no ecossistema Verg, mas o contrato necessário está aqui:
clone isolado não depende de outro repositório ou caminho pessoal.

Cada lote declara ID, objetivo, base/head SHA, arquivos permitidos, requisitos,
fontes, executor/revisor reais, entradas/saídas, efeitos autorizados, testes,
evidência, rollback e parada. Revisores conferem diff e fontes, não só resumo.

Editores concorrentes usam branches/worktrees isoladas. Núcleo, mapa, registro,
CI, índices e gerador têm um owner por vez. Outros enviam propostas ao owner;
só o integrador gera adaptadores definitivos/marcador. Após conflito, rebase ou
configuração alterada, repita testes afetados e revisão.

## Conflitos

Preserve trabalho do usuário e de outros agentes; não sobrescreva conflito.
Distinga: instruções carregadas incompatíveis; história tratada como presente;
documentação contra código/policy; pedido além de autorização/capacidade.
Pare apenas a ação dependente, exponha fontes/impacto e peça decisão. Não escolha
a variante mais permissiva, atribua precedência pelo fornecedor ou trate prompt
como ACL. Políticas superiores/gerenciadas e permissões reais prevalecem.

Dentro do projeto, código/policy rege contrato executável; owner vivo rege estado;
evidência histórica é datada. Precedência de arquivo carregado depende do cliente
real e da [compatibilidade](../compatibility.md), não desta organização editorial.

## Fechamento

Toda sessão que altera algo mantém data, autoria, arquivos e evidência no owner
da tarefa: teste, auditoria, handoff quando há continuidade ou commit/PR para
manutenção trivial. O CHANGELOG da raiz registra apenas marcos que afetam uso,
arquitetura, compatibilidade, contrato, distribuição ou risco material. Use o
[template](../templates/changelog-entry.md). Não é exigido importar ou ler todo o
histórico no início: busque o trecho pertinente à retomada/investigação.

Mudança estrutural exige ADR e/ou [handoff](../templates/handoff.md); mudar uma
decisão aceita exige novo ADR. Handoff tem SHA/branch, efeito autorizado,
resultados, bloqueio e condição de retomada; não concede execução futura.

Estados de trabalho: PLANNED, IN_PROGRESS, READY_FOR_REVIEW, ACCEPTED, BLOCKED,
REJECTED. Evidência: PASS, FAIL, NOT_RUN, BLOCKED, NOT_APPLICABLE_WITH_REASON.
Nunca converter falta de prova, preservação ou tempo decorrido em PASS.

## Auditoria

Contrato mínimo internalizado, com [template](../templates/auditoria.md):

| Nível | Mínimo de origens de revisão | Uso e prova |
|---|---|---|
| A0_light | uma | revisão local; declarar se autorrevisão ou contexto completo |
| A1_standard | duas independentes | análise individual antes de conciliar; não aprovar próprio patch |
| A2_strict | três independentes | revisão aprofundada, evidência por origem e divergências registradas |
| A3_incident | três ou mais independentes | incidente/alto impacto; apuração e decisões rastreáveis |

Origem independente exige sessão/contexto identificáveis e avaliação própria,
sem apenas reproduzir a conclusão anterior. Marca diferente não basta. Auxiliares
da mesma sessão/coordenador são apoio de revisão, não elevam A0 automaticamente
para A1. Revisor que não editou o lote ajuda, mas não é, sozinho, prova de segunda
origem. Se a independência exigida não estiver disponível, o requisito é BLOCKED;
entregue cobertura parcial sem diminuir o nível para chamar de aprovado.

Gatilhos mínimos A1+: antes de compartilhar com squad, antes de replicar mudança
grande no trabalho e quando duas IAs divergem sobre plataforma. Nessa divergência,
consulte fonte oficial aplicável e registre a decisão; se permanecer ambígua,
PENDENTE/DECISAO com owner. Não reduza nível quando houver dados sensíveis,
produção, publicação externa ou decisão que afete squad/missão.

Revisão de contexto completo deve ser chamada assim. Auditoria cega exige corpus
permitido/proibido, manifesto de arquivos/hash, sessão nova e evidência de contexto
inicial. Histórico proibido já recebido invalida “cega”; pedir que o modelo esqueça
não corrige. Pode continuar como contexto completo, registrando o limite.

Use `docs/auditoria/YYYY-MM-DD_<tema>/`: `01_contexto.md`, rodadas por auditor e
`99_consenso.md`. Contexto inclui motivo do nível, exclusões, autoridade e pacote
exato sanitizado recebido por cada origem. Rodadas têm severidade/evidência.
Consenso preserva divergências/riscos e fecha ações priorizadas, owner e critério
de verificação. Atribuição real e corpus verificável importam mais que contagem.
