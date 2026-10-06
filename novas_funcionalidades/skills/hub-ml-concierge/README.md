# Concierge Hub

> **Arquivo histórico do protótipo.** Não instalar ou testar esta cópia como produto atual. Use a [versão canônica](../../../ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md). Comandos, próximos passos e resultados abaixo preservam a experiência original; não concedem autorização para nova execução.

**Estado: protótipo experimental 0.1.0, não instalado e não homologado no Databricks.**

## O que é e para quem é

A skill `hub-ml-concierge` ajuda quem sabe o que precisa fazer, mas não sabe quais recursos do Hub utilizar. Ela transforma uma necessidade em uma recomendação verificável: método, briefing, helpers, exemplos e ordem de uso. Não exige que a pessoa conheça a taxonomia do repositório.

É uma especialização do assistente existente, não um novo agente ou executor universal. Uma necessidade simples pode terminar em uma única função; uma demanda ampla pode exigir uma composição. Ela também reconhece cobertura parcial e acesso insuficiente.

## Próxima ação

Para revisar comportamento, leia [SKILL.md](SKILL.md). Para entender as escolhas, consulte [Arquitetura](docs/arquitetura_e_decisao.md). Para experimentar sem alterar o produto, siga [Instalação, testes e promoção](docs/instalacao_testes_promocao.md). Para conferir a entrega localmente, use [Testes](tests/README.md).

## O que é automático e o que não é

Nesta pasta experimental, o pacote **não se torna uma skill ativa da Genie Code por existir no GitHub**. Após uma instalação autorizada em um local suportado, a plataforma pode selecioná-lo por relevância ou menção explícita. Isso não carrega toda a biblioteca nem importa Python automaticamente. Os mecanismos oficiais e seus limites estão em [Fontes](docs/fontes.md).

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
