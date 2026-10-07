# ADR-0028 — Manual Técnico V2 como única edição técnica vigente

- **Status:** Aceito por solicitação do usuário para implementação local.
- **Data:** 2026-10-07.
- **Autoria:** Codex, executor de manuais; integração e auditoria na mesma sessão.
- **Supersede:** ADR-0010 quanto ao nome do livro e à cópia integral na raiz.

## Contexto

A edição anterior existia no produto e na raiz Git com bytes iguais. O V2
ampliou a explicação técnica, mas sua primeira edição declarava não revogar
ADR-0010. O usuário decidiu conservar somente o manual técnico mais atual.

## Decisão

A única redação técnica vigente é
`ambiente_databricks/.assistant/MANUAL_TECNICO_V2.md`. A edição anterior no produto e
sua cópia integral na raiz são removidas. A raiz aponta diretamente ao livro.
`MANUAL_DO_USUARIO.md` permanece como jornada complementar de uso.

O catálogo integrado, glossário, âncoras e exemplos executáveis portáveis da
edição anterior são incorporados à referência operacional do V2. Sua parte de
leitura é `manuais_v2/partes/MT_REFERENCIA_OPERACIONAL.md`. Os capítulos MT
continuam aprofundando interfaces e contratos; código, schemas e policy
prevalecem quanto ao comportamento executável. Não criar outro catálogo ou
manual técnico concorrente.

Referências vivas migram para V2. ADRs aceitos, evidências fechadas, hashes e
links de fontes presos a commits conservam o texto original. Uma referência
histórica ao livro antigo identifica aquela edição; não constitui rota atual.
O Git preserva a recuperação da edição removida.

Integridade editorial exige atualizar o livro, suas partes pertinentes e o
manifesto após conferência. O renderer gera a cópia operacional sem edição
manual. Testes exigem presença do livro atual, ausência das edições antigas,
catálogo cobrindo objetos atuais, âncoras, exemplos e equivalência do derivado.
O gate V02 confere SHA-256 e tamanho contra o manifesto em vez da antiga cópia
integral na raiz, com teste de mutação preservado.

## Consequências e limites

Há um único nome técnico vigente e nenhum livro integral técnico na raiz Git.
A referência operacional mantém compatibilidade de âncoras sem restaurar uma
segunda edição. O custo é conferir também a parte derivada e o manifesto em
cada alteração pertinente. Publicar ou remover uma cópia remota antiga exige
escopo próprio; exclusão no Git não executa esses efeitos.

A consolidação prova manutenção local quando os gates passam. Não comprova
execução de todos os exemplos do V2, verdade de toda a prosa, instalação,
Databricks, acesso corporativo, publicação ou aceite humano.

## Reversão

Recuperar os dois arquivos da revisão Git anterior, restabelecer os consumidores
e os contratos anteriores e revalidar antes de qualquer publicação. Preservar
esta decisão como registro; nova mudança de autoridade exige ADR sucessor.
