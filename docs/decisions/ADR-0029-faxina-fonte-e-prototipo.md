# ADR-0029 — Fonte Databricks e aposentadoria do protótipo

Data: 07/10/2026. Estado: execução local autorizada pelo usuário. Autoria: Codex.

## Contexto

O projeto será mantido no VS Code com Copilot e transportado ao Databricks do
trabalho. A pasta de fonte deve comunicar seu destino, e o protótipo Concierge
já integrado não deve continuar concorrendo com o produto.

## Decisão

1. `ambiente_databricks/` substitui `ambiente_fonte/` como fonte editável.
   `.assistant/` e `.assistant_instructions.md` continuam sendo os dois itens
   publicáveis; o nome da pasta Git não muda a home nem os paths do workspace.
2. Atualizar código, testes, filtros/comandos de workflows, instruções e rotas
   vivas para o novo nome. Não manter symlink nem segunda árvore de produto.
3. Remover `novas_funcionalidades/`. O Concierge vigente permanece no produto;
   recuperar o protótipo somente pelo commit e hashes do manifesto histórico.
4. Preservar bytes de campanhas, snapshots e decisões aceitas. Seus nomes antigos
   descrevem aquela revisão, não a fonte corrente. Links locais antigos têm prova
   específica de recuperação na árvore Git original, separada de links vivos.
5. Manter `.agents/skills` editorial e `.claude/skills` gerada. Documentar Copilot
   no VS Code sem presumir carregamento ou deduplicação no cliente do trabalho.
6. Manter ferramentas úteis e cobertura CI, com catálogo por função e efeitos.
   A consolidação do Manual Técnico é regida pelo ADR-0028.

## Consequências e prova

O clone de manutenção deve conter o histórico Git necessário à recuperação.
Ausência do commit não é referência aprovada. O gate de links históricos aceita
somente pares fonte/href enumerados, fonte idêntica ao blob original, destino
existente com caixa correta e hash do objeto; rejeita alteração, invenção,
duplicação e entrada não consumida. Não comprova âncoras nem navegação local.

A troca de diretório não é publicação, homologação Spark/Genie ou ativação no
trabalho. Testes atuais, render e equivalência do produto devem ser executados
após integrar todos os lotes. Baselines antigas não são regravadas para passar.

## Alternativas e reversão

Uma árvore duplicada ou symlink perpetuaria ambiguidades e problemas de
portabilidade. Reescrever relatórios fechados destruiria evidência; apagar gates
para acomodar a remoção perderia cobertura. A reversão recupera a revisão Git
anterior e reaplica mudanças alheias preservadas, sem tocar workspaces remotos.

Execução e resultados: [registro da faxina](../manutencao/execucao-faxina-2026-10-07.md).

## Registro técnico da migração de metadados

O schema temático mantém versão e regras 0.1.0. Seus campos `x-hub` de origem e
consumidores mudam somente o prefixo da pasta Git. A revisão fixa o novo SHA256
`a0d6bd1780611acae671910d3a4dbc76aa91b678673eaca17fc6de868508955c`;
o teste `test_temas_faxina_migration.py` exige igualdade byte a byte com o schema
original após essa substituição exata. Nenhuma regra de validação é afrouxada.
O gerador `dictionary()` mantém a projeção histórica V01 com namespace original
e hash do dicionário congelado; `operational_dictionary()` usa as rotas atuais.
Registros V01/V07/V08/V13 consumidos por gates são owners vivos e acompanham
a migração; relatórios de execução fechados continuam preservados.
