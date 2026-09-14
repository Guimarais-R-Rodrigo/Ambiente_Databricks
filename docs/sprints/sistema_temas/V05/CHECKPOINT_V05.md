# Checkpoint V05 — Visual Lab em fechamento

## Estado vigente — reconciliação pós-D05/R13 em 14/09/2026

A V05 candidata está na branch `codex/temas-v05-fechamento-r13-20260913`, reconciliada com a `main` `24ffce298ed543755eb15d5d7c553d02ce15e73e`, que já contém a D05 documental pós-R13. A comparação após a reconciliação confirmou merge-base exatamente nessa `main`, `behind=0` e preservação integral da D05. A `main` não foi alterada pela V05.

A PR #26 e as branches anteriores permanecem históricas; não devem ser tratadas como a candidata final. Não há aceite V05, merge da V05 na `main`, publicação Databricks ou início da V06.

### Estado funcional da candidata

As lacunas registradas em checkpoints antigos — seleção visual de presets, vínculo com a base original e reabertura autônoma — foram implementadas na candidata corrente e exercitadas por regressões específicas:

- launcher com escolha de presets de demonstração/manutenção;
- chave desconhecida e contexto incompatível recusados sem fallback;
- sessão com `base.json`, `proposal.json`, histórico e manifesto;
- hashes da base/proposta/histórico registrados e conferidos;
- reabertura restaurando base original, proposta, revisão e histórico;
- `undo()` funcional após roundtrip;
- sessão parcial sem manifesto ocultada/recusada;
- proposta adulterada recusada sem “reparo” de hash.

Isso é fechamento do contrato Python testado, não homologação do frontend Databricks. Renderização real, callbacks no navegador, acessibilidade, p95, ACL real do destino e UAT por iniciante permanecem gates separados.

### Execuções desta retomada

O run `34797774791`, no commit `147541a5c24ec3b10d262f243bb575c192342280`, falhou com 30/31 testes específicos: a única falha era o contrato textual que exigia a expressão literal `não publica`. A correção foi documental e não relaxou o teste.

Enquanto essa correção era preparada, a PR #36 (D05) foi integrada à `main`. A candidata V05 foi então reconciliada por fast-forward da branch e commit de combinação `4447fb2877662c662a1a7e6dd0ae5c877466916a`, preservando o conteúdo D05 e mantendo o diff líquido funcional restrito à V05.

No run `34798200237` dessa composição, os gates funcionais passaram: 31/31 V05, 14/14 sessões, 359/359 regressões `test_temas*.py` e 12/12 legado visual V00. O workflow permaneceu corretamente **FAILURE** porque o validador documental encontrou o README `theme_lab` fora do contrato editorial 1.0.0 da R13 e métricas desatualizadas no README raiz. Essa falha está preservada e não deve ser reclassificada.

O commit `81052d099627b3ab919217fa4f78a9d9e57d770b` migrou o README do Visual Lab para as quinze seções obrigatórias, em fonte e simulado, preservando o comportamento documentado e a frase explícita de não publicação. Novas edições documentais exigem nova execução; nenhum run anterior aprova automaticamente esta árvore.

### Fechamento técnico e PR final

O Manual canônico, a cópia raiz e o derivado foram sincronizados sem substituir a redação D05/R13. O README do Hub e seu derivado, `CLAUDE.md`, índices e CHANGELOG também foram reconciliados. As métricas do README raiz foram medidas no run `34831939535` e atualizadas sem estimativa manual.

No head limpo `efb9dd3270ac0f5240612cf3b7e9e39111e51c46`, o workflow V05 `34832202757` terminou com **success** em todas as etapas. A PR final **#37** foi aberta em draft contra a `main` `24ffce298ed543755eb15d5d7c553d02ce15e73e`. Os checks disparados pela PR também concluíram com **success**: CI geral `34832408423`, V00 `34832408496`, V01 `34832408407`, V02 `34832408460` e V05 `34832408426`.

Os workflows V03/V04 isolados não foram disparados pela PR porque seus filtros de caminho não abrangem os arquivos V05. Isso não remove suas regressões da bateria: o workflow V05 executa a descoberta `test_temas*.py`, que inclui V01–V05 e passou com 359 casos no head técnico validado.

Após este registro documental, a própria PR deve repetir os checks no novo head. Permanecem como próximas ações somente: confirmar o CI do head documental final, revisar o diff final, manter a PR em draft e parar antes de qualquer merge para aceite explícito. Nenhuma dessas etapas autoriza publicação Databricks ou início da V06.

### Limites que permanecem

Nenhum teste Python comprova navegador/runtime Databricks. Continuam pendentes: acessibilidade por teclado/leitor de tela, contraste percebido/zoom, desempenho p95 no ambiente real, permissões reais da pasta de sessões, UAT por usuário iniciante, submissão/aprovação/publicação e auditoria independente da experiência final.

---

## Histórico preservado — reconciliação com R08 em 13/09/2026

V05 continuava em desenvolvimento na PR #26, branch `codex/temas-v05-visual-lab-20260912`. Não havia aceite V05, merge na main, publicação Databricks ou início da V06.

A composição `5cace7f876b2bdb2a1eecaa73e3f7958dfd2764e` incorporou a main R08 `d5945e04328609878f63857cc15cf5e5039b3e75` à branch de desenvolvimento, preservando todos os arquivos dessa main e os 16 arquivos novos da candidata. A comparação das duas frentes mostrou sobreposição somente no README raiz, em suas contagens derivadas; sua narrativa R08 foi preservada.

O commit `57062e86e0741e88fcd0b30c902ff57ece4be1c8` atualizou as métricas com a saída medida no run `34761074646`. Sua árvore era `d9ef6099313f1ab2622e42677b5a3f7e4d812ac5`. As alterações dessa rodada não modificavam a implementação, API, schema, fixtures ou ativos visuais da V05.

### Resultado efetivo daquela composição

O workflow V05 `34761250018` terminou com success. V00 `34761250014`, V01 `34761250034` e V02 `34761250027` também terminaram com success. O CI geral `34761250016` continuou FAILURE: oito de nove etapas passaram, mas a guarda do inventário do Manual não encontrou a seção `hub_snippets.visual.theme_lab`. A validação estrutural passou com zero falhas e zero avisos. Isso não equivalia a CI transversal aprovado.

Os checks de PR usaram um commit de teste de merge. Para o head `57062e8`, o log registrou `1d83a9456518a0bba639f708bb8e95f9dce8f808`. Resultados pertenciam àquela composição e não se estendiam automaticamente ao próximo commit documental.

### Próxima ação registrada naquele momento

Completar a seção do laboratório no Manual canônico, preservar todo o texto anterior, sincronizar sua cópia da raiz e gerar o derivado pela ferramenta oficial. Registrar V05 e a rodada no CHANGELOG raiz, completar índices e repetir gates.

Naquele checkpoint, presets escolhidos pela interface, vínculo automático com a base original e reabertura autônoma ainda eram lacunas. **Essa frase é histórica:** a candidata pós-D05 implementou esses contratos e os testes atuais os exercitam; isso não reescreve o estado observado em R08.

Não foi criado workflow transitório, ampliada permissão ou executado force-push. A main não foi alterada por aquela rodada.

## Estado anterior — retomada R07 em 13/09/2026

V05 estava em desenvolvimento na branch `codex/temas-v05-visual-lab-20260912`. A retomada preservava integralmente a main R07 `b73bbb91961f9ba5f9031d648c42ec0891b63347` e acrescentava os sete arquivos da candidata `133966bf8ee7555d1d9dadd3922d2fc75a4641e9`. Essa composição não era aprovação dos testes anteriores e exigia nova rodada.

Rodrigo havia autorizado continuar o desenvolvimento. Não havia concedido aceite à V05 nem integração, publicação no Databricks ou início da V06.

## Bloqueios de fechamento — registro da retomada R07

- corrigir navegação do README dentro do produto publicado;
- ajustar o notebook sem relaxar a guarda de contrato e registrar saída executada;
- conferir segurança de salvamento e comportamento da interface;
- completar documentação de primeiro uso, catálogo integrado do Manual e índices;
- registrar a execução no CHANGELOG raiz sem truncar seu histórico;
- gerar fachadas e espelho com as ferramentas canônicas;
- recalcular o README pela execução na árvore final;
- executar regressões e revisão sobre a composição final antes do aceite.

## Evidências anteriores

A execução `34733554922` da candidata `a45ebd6` aprovou 31 casos V05, 329 casos de temas e 12 legados visuais V00, mas REPROVOU a validação documental. Não era CI aprovado e não testava a composição R07. Consulte [TESTES.md](TESTES.md).

## Limites históricos e atuais

Testes Python de objetos ipywidgets não comprovam renderização nem callbacks em Databricks. Acessibilidade, usuário iniciante, runtime do workspace, permissões reais e auditoria independente permanecem pendentes. O laboratório usa dados sintéticos; não aprova nem publica temas.

## Recuperação

Enquanto esta branch não for integrada, nenhuma reversão de main ou publicação é necessária. Não fazer force-push, não alterar proteções e não sobrescrever mudanças paralelas da `main`. Preservar execuções reprovadas como evidência.

[Escopo V05](README.md) · [Testes](TESTES.md)

## Diagnóstico de acesso e retomada — 13/09/2026

Rodrigo solicitou pesquisar o bloqueio de ferramentas e aplicar uma solução. A inspeção da configuração do aplicativo GitHub encontrou permissão específica Allow all actions. Ela já estava configurada; não foi ampliada nessa rodada. Essa configuração não elimina as proteções de segurança da plataforma.

As tentativas anteriores de transportar um script de preparação foram recusadas. A causa específica não foi informada. Não atribuir o bloqueio a falta de aceite, expiração de token, tamanho de arquivo ou erro do GitHub sem evidência própria. A manutenção documental deve preferir edição direta de texto, com leitura prévia do arquivo inteiro e conferência do SHA, sem scripts transitórios de escrita.

Naquela consulta, a main já estava em `d5945e04328609878f63857cc15cf5e5039b3e75`. A PR #26 continha a candidata `5f2dc583a04f66f1851836424d4ed2489188cb78` e indicava conflito de integração. Portanto, a composição R07 anterior não era suficiente para o fechamento.

O teste de acesso pelo cliente Git do ambiente de edição não conseguiu resolver o host github.com. Isso era uma limitação de conectividade daquele ambiente, não prova de falha de credenciais nem explicação do bloqueio do aplicativo. Nenhum segredo foi solicitado ou transferido e nenhuma proteção foi alterada.

Essa nota documentava o diagnóstico, não a conclusão da V05.
