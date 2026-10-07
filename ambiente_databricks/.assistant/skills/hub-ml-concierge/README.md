# Concierge Hub

O contrato estático é L1/audit. Uma recomendação aceitável identifica recurso existente, API/contrato consultados, adequação, limites, sequência mínima e próxima decisão. Estrutura, transporte da release e comportamento conversacional são provas distintas: um registro local não confirma publicação ou aceite no ambiente-alvo.

Use o Concierge para localizar recursos existentes e obter uma recomendação com evidências e limites. A busca não executa análises nem amplia permissões.

## O que é e para quem é

A skill `hub-ml-concierge` ajuda quem sabe o que precisa fazer, mas não sabe quais recursos do Hub utilizar. Ela transforma uma necessidade em uma recomendação verificável: método, briefing, helpers, exemplos e ordem de uso. Não exige que a pessoa conheça a taxonomia do repositório.

É uma especialização do assistente existente, não um novo agente ou executor universal. Uma necessidade simples pode terminar em uma única função; uma demanda ampla pode exigir uma composição. Ela também reconhece cobertura parcial e acesso insuficiente.

## Próxima ação

Para revisar comportamento, leia [SKILL.md](SKILL.md). Para entender as escolhas, consulte [Arquitetura](docs/arquitetura_e_decisao.md). Para instalar em escopo pessoal e conferir o comportamento, siga [Instalação, testes e promoção](docs/instalacao_testes_promocao.md). Para conferir a entrega localmente, use [Testes](tests/README.md).

## O que é automático e o que não é

Mesmo integrado a `ambiente_databricks/`, o pacote **não se torna uma skill ativa da Genie Code por existir no GitHub**. Após uma instalação autorizada em um local suportado, a plataforma pode selecioná-lo por relevância ou menção explícita. Isso não carrega toda a biblioteca nem importa Python automaticamente. Os mecanismos oficiais e seus limites estão em [Fontes](docs/fontes.md).

O Concierge usa as ferramentas de leitura/pesquisa já disponíveis ao assistente. Quando não houver acesso aos arquivos, pede o contexto mínimo ou informa o bloqueio. Esta versão não inclui indexador, servidor, embeddings ou dependência de rede adicional.

## Exemplo de uso

Depois de instalar e testar o pacote em escopo pessoal:

```text
@hub-ml-concierge
Tenho uma tabela nova e quero descobrir quais recursos do Hub ajudam
na verificação de nulos e duplicidades antes de modelar.
Quero uma recomendação, sem executar consultas nem alterar arquivos.
Use apenas recursos existentes, mostre as evidências e diferencie
uma checagem pontual de uma EDA completa.
```

Sem instalar, anexe o `SKILL.md` e os recursos necessários e peça uma **simulação do procedimento**. Isso avalia a resposta, não comprova descoberta nativa ou ativação por `@`.

## Estrutura e donos de cada assunto

| Arquivo/pasta | Responsabilidade |
|---|---|
| [SKILL.md](SKILL.md) | Fluxo principal e fronteiras de atuação |
| [Descoberta](references/descoberta.md) | Escopo, fontes, verificação e cobertura da busca |
| [Composição](references/composicao.md) | Compatibilidade, escolhas mínimas e transferência de contexto |
| [Exemplos](references/exemplos.md) | Casos ilustrativos, nunca evidência de execução |
| [Recomendação](templates/recomendacao.md) | Template principal de resposta ao usuário |
| [Handoff](templates/handoff.md) | Template de repasse para a etapa especializada |
| [Registro de busca](templates/registro_busca.md) | Rastro resumido e auditável dos recursos consultados |
| [Documentação](docs/arquitetura_e_decisao.md) | Decisão experimental, instalação e fontes |
| [Testes](tests/README.md) | Critérios de aceite e validação reproduzível |

## Limites e manutenção

O Concierge não autoriza execução, não homologa um helper e não prova compatibilidade só por encontrar uma função. A existência no Git não demonstra publicação no workspace. Recomendações sobre partes de um módulo priorizam sua API pública; detalhes internos não são promovidos silenciosamente a contratos.

O Manual Técnico continua sendo o dono do inventário semântico. Não há catálogo novo mantido manualmente neste pacote. Exemplos citam recursos candidatos e exigem nova verificação na instalação consultada.

Ao alterar a descrição ou as fronteiras, repita os testes de colisão com especialistas. Ao alterar o Hub, revise exemplos e execute o procedimento de descoberta novamente. Consulte o estado efetivamente verificado em [RESULTADOS](tests/RESULTADOS.md).
