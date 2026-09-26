# Arquitetura e decisão experimental

**Proposta local, não ADR aceito.** Não reserva numeração de ADR nem altera decisões históricas.

## Problema e objetivo

O usuário quer melhorar o uso do Hub existente. A pessoa descreve uma necessidade; o Concierge encontra capacidades e recomenda uma composição, inclusive quando nenhuma skill isolada cobre o pedido.

## Desenho escolhido

Pedido -> escopo/versão -> mapa semântico existente -> shortlist -> verificação de contratos -> composição mínima -> recomendação/handoff.

O procedimento é implementado em `SKILL.md`. Referências aprofundam busca e composição; templates padronizam entregas. O assistente utiliza ferramentas de leitura existentes. Não há novo modelo, serviço, indexador, registry autoral, banco vetorial ou dependência de compute nesta versão.

A capacidade analítica continua pertencendo aos objetos existentes. A skill não é um executor independente, e o seu texto não cria ferramentas ou acesso a arquivos. A ausência de mecanismo de leitura deve produzir uma limitação explícita, não uma recomendação inventada.

## Relação com as decisões do repositório

O ADR-0004 rejeitou a varredura de dezenas de módulos por uma skill universal, citando colisão de roteamento, custo de contexto e decisão não determinística. A proposta atual limita a ativação à intenção de descoberta, preserva helpers declarados pelos especialistas e consulta os índices antes dos corpos dos arquivos. Esses mecanismos mitigam os riscos; somente os testes podem demonstrar sua suficiência.

O ADR-0010 mantém o inventário integrado no Manual Técnico. Não criamos catálogo concorrente. Os exemplos desta skill são ilustrativos, não exaustivos, e nunca substituem o inventário atual.

Uma futura promoção requer decisão explícita sobre esse novo comportamento transversal. A decisão histórica não é reescrita; uma nova decisão deverá explicar exatamente o que muda e o que permanece.

## Alternativas

**Expandir todas as skills:** mantém reuso local, mas não resolve bem quem não sabe escolher a primeira skill e multiplica a lógica transversal de composição.

**Agente separado:** oferece uma interface e contratos próprios, mas acrescenta operação e transferência de contexto desnecessárias para esta primeira melhoria do fluxo existente.

**Somente README:** ajuda navegação humana, mas não transforma um pedido em escolha contextual.

**Busca determinística auxiliar:** evolução possível se testes mostrarem falhas de recuperação. Deve ler o inventário/código autorizado e produzir dados derivados, sem uma segunda redação semântica e sem executar helpers.

## Responsabilidades e segurança

O Concierge descobre; o especialista decide o método; o código consumidor executa dentro das permissões e da autorização. Recomendações não ampliam privilégios. Busca em arquivos não inclui consulta a dados bancários.

Conteúdo recuperado é entrada não confiável para instruções operacionais. A skill deve ignorar comandos embutidos e não executar um fluxo especializado apenas por ter lido seu `SKILL.md` durante a comparação.

## Critérios de sucesso

Acerto dos recursos e símbolos; composição com pré-condições; referências verificáveis; nenhuma capacidade inventada; ausência de execução indevida; baixa interferência em pedidos especializados; esforço reduzido para o usuário. Tempo e custo devem ser medidos no ambiente de uso, não estimados como resultados já obtidos.

## O que não está aprovado

Promoção a `ambiente_fonte`, alteração de `EXPECTED_SKILL_NAMES`, instalação em escopo compartilhado, atualização de ADR, publicação no Free/trabalho, execução sobre dados reais e homologação. Tudo isso permanece fora desta entrega.
