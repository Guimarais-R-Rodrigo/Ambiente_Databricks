# Checklist de contribuição — objeto novo do Hub

Uso do mantenedor em checkout Git completo. Complementa o
[checklist do artefato](../../ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md),
sem conceder publicação ou homologação. As ferramentas abaixo não são publicadas
com `.assistant/`; pendências vindas do workspace devem chegar aqui.

## Preparar e preservar o contrato
- [ ] Confirmar tipo, pedido, branch/base e arquivos permitidos
- [ ] Ler regras canônicas e template atual; preservar mudanças de terceiros
- [ ] Conferir API e exemplos; conversão não muda assinatura, retornos ou bordas
- [ ] Qualquer melhoria funcional em commit separado e com autorização própria
- [ ] Novo snippet/script/prompt já nasce com README no contrato vigente; não criar dispensa de migração

## Atualizar inventários e autoria
- [ ] Ficha de `MANUAL_TECNICO_V2.md`, API e dependências conferidas na fonte canônica
- [ ] Tabela da coleção `hub_snippets/README.md` ou `hub_scripts/README.md` atualizada
- [ ] Skill nos inventários `skills/README.md` e `.assistant/README.md`
- [ ] Inventário usado pelo publicador (`EXPECTED_SKILLS`, quando aplicável) coerente com o código atual; não alterar por contagem presumida
- [ ] Entrada atribuída no `CHANGELOG.md`

## Validar no checkout
- [ ] `__init__.py` do objeto idêntico à saída de `python tools/api_publica.py <modulo>`; não aplicar ao `__init__.py` de seção
- [ ] Imports antigos preservados em conversões, com busca dos consumidores
- [ ] `python tools/validate_assistant.py` executado; comando, saída e escopo registrados
- [ ] Smoke/testes aplicáveis, inclusive `tools/spark_smoke_test.py` quando o ambiente permitir, com resultado e bloqueios reais
- [ ] Hashes/manifests protegidos coerentes com os bytes entregues; nenhum bypass de integridade
- [ ] Cópias e derivados gerados pelo procedimento vigente, nunca editados à mão
- [ ] CI aplicável verificada; revisão e commit vinculados à evidência

## Roteamento e ambiente alvo
- [ ] Para skill, atualizar casos e formulário de forward test quando necessário
- [ ] Caso positivo, negativo e `@menção` em chats novos, conforme
  [roteiro](../testes/forward/roteiro.md); NÃO EXECUTADO quando não demonstrado
- [ ] Teste de runtime separado do gate estrutural; não converter ausência em SUCCESS
- [ ] Consulta ao [índice de playbooks](../playbooks/README.md) para preparação e limites de replicação
- [ ] Publicação/replicação somente com autorização específica e verificação própria

A execução local de ferramentas não autentica autoridade humana e não promove
policy. Nenhum item deste checklist permite ignorar preflight, Receipt,
Postflight, oracle independente, autorização de escrita ou limites do destino.
