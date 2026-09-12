# Governança de propostas, aprovação e publicação

**Especificação, não mecanismo de segurança instalado.** A fonte das transições
é [politica_workflow.json](politica_workflow.json); o verificador local testa seu
modelo com identidades sintéticas. Não autentica pessoas nem concede acesso.
O ambiente real precisará verificar identidade, permissões e destino sem confiar
nos valores enviados pelo navegador, widget ou arquivo.

## Papéis e responsabilidades

| Papel | Pode fazer | Não recebe automaticamente |
|---|---|---|
| Leitor | Ver temas a que tem acesso e experimentar em sessão própria. | Salvar proposta persistente de outra pessoa, aprovar ou publicar. |
| Proponente | Criar/editar rascunho próprio, exportar, submeter ao destino autorizado. | Aprovar a própria proposta ou alterar padrão compartilhado. |
| Aprovador | Revisar proposta congelada, aprovar/rejeitar e registrar revogação. | Poder técnico de publicação pelo simples ato de aprovar. |
| Publicador | Promover revisão aprovada em destino autorizado, com backup e conferência. | Aprovar conteúdo novo ou editar o que foi aprovado. |
| Mantenedor | Manter contrato, testes e dependências; propor revisões. | Aprovação estética ou acesso administrativo aos workspaces. |

Os papéis serão associados a responsáveis/grupos reais pelo proprietário do
ambiente. A especificação não escolhe pessoas nem cria grupos. Uma pessoa pode
ter múltiplos papéis formalmente concedidos; a verificação de não ser autora
da própria proposta continua obrigatória. Ausência de revisor independente
bloqueia publicação compartilhada, não autoriza autopromoção.

## Estados e ações

Uma alteração pessoal nasce `rascunho`. Editar mantém esse estado e exige
propriedade e validade do documento. Salvar/exportar continua sendo proposta.
**Submeter** congela uma revisão para escopo projeto ou compartilhado e passa
para `em_revisao`. O escopo nessa transição é o destino solicitado, não uma
permissão escrita no tema.

**Aprovar** exige papel de aprovador validado, autor diferente, hash correspondente,
assets verificados, revisão de acessibilidade, revisão independente e destino
definido. `aprovado` significa conteúdo aceito para aquele destino; não significa
instalado. Rejeitar registra motivo e versão revisada, preservando o histórico.

**Publicar** só parte de `aprovado`. Verifica identidade, aprovação ainda válida,
bytes, manifesto de dependências, autorização de destino, backup e revisão
anterior esperada. Sucesso muda para `publicado` somente depois de verificar o
estado efetivo da entrega. Falha parcial precisa de recibo e recuperação;
não pode deixar um rótulo de sucesso apenas porque a ação começou.

**Revogar** registra decisão de não usar uma publicação. Revogação não restaura
bytes automaticamente nem apaga o histórico. Precisa indicar destino e motivo.
Arquivar rascunho próprio é outra ação, sem efeitos no produto.

Editar conteúdo em revisão, aprovado, publicado, rejeitado ou revogado cria
**novo rascunho com nova revisão**. O original permanece imutável. Não existe
`force_publish`, botão secreto, promoção baseada só no nome do arquivo ou
remoção de uma guarda para concluir uma apresentação.

## O que a aprovação deve vincular

O registro confiável deve conter SHA-256 dos bytes exatos do tema, SHA-256 do
schema, SHA-256 do manifesto de assets, versão do renderizador, escopo solicitado,
ID do destino e revisão anterior esperada. Estes campos são definidos em
`trusted_revision_components`. O hash não é uma assinatura de identidade:
a autenticidade do aprovador depende do processo ou servidor confiável.

Qualquer mudança desses componentes invalida a reutilização daquele aceite.
Reabrir um tema com o mesmo nome não dispensa revisão. A aprovação também deve
registrar responsável autenticado, data, motivo, evidências e decisão. Não
armazenar segredos no registro nem no próprio JSON. Retenção e acesso seguem a
política autorizada do destino; a V01 não inventa prazo corporativo.

## Concorrência e separação entre usuários

A prévia de uma pessoa não deve mudar a de outra. O mecanismo futuro deve usar
configuração explícita e não alterar constantes/globais compartilhadas a cada
movimento do seletor. Compatibilidade do alias histórico é uma rota separada.

Uma publicação exige que o destino ainda esteja na revisão anterior esperada.
Se outra publicação ocorrer primeiro, a segunda proposta é bloqueada e deve ser
reavaliada contra o novo estado. Essa é a proteção contra atualizar uma versão
sobre trabalho que o publicador não viu. O modelo local testa a exigência da
guarda; atomicidade de escrita real depende da implementação e da plataforma.

## Persistência, recibos e retorno

No laboratório, somente “aplicar na prévia” é volátil. “Salvar/exportar proposta”
deve mostrar onde foi salvo, nome e confirmação de sucesso; destino indisponível
não pode exibir “salvo”. Rascunhos de desenvolvimento podem ficar em
`.artifacts/temas/rascunhos/`, já excluído do Git, nunca como publicação autorizada.
A operação não técnica terá um destino autorizado mostrado na interface.

A publicação futura terá recibo com arquivos previstos, efetivamente alterados,
hashes, falhas e estado anterior. A cópia offline deve conter as dependências
compatíveis necessárias. A rota de staging pessoal e promoção seletiva do
projeto permanece a mesma; tema não cria uma rota de deploy paralela.

Retornar significa publicar uma revisão anterior **ainda aprovada**, novamente
verificando as guardas e dependências. Se ela foi revogada, exige novo aceite
antes do uso. Não apagar registros, não reescrever histórico, não fazer
force-push ou limpeza recursiva de conteúdo desconhecido.

Nesta V01 nada foi publicado. Retorno local é encerrar a candidata preservando
as evidências; eventual reversão de commit integrado deve ocorrer por revisão
normal, sem desfazer alterações alheias.

## Limites das provas nesta sprint

Os testes enviam valores sintéticos como `revision_match=True` ao oráculo.
Isso prova que o modelo exige a guarda, **não que uma identidade real foi
verificada ou que o hash foi assinado**. Autorização direta de endpoint,
sessões simultâneas, revogação de grupo, falhas de armazenamento e destino
estão reservados aos testes de integração. O contrato rejeita autodeclaração
de papéis no tema, mas não equivale a uma homologação de segurança do App.

[Voltar ao contrato](CONTRATO_TEMAS.md) · [Aceite](TESTES_E_ACEITE.md)
