# Checkpoint V05 — Visual Lab em desenvolvimento

## Estado vigente — reconciliação com R08 em 13/09/2026

V05 continua em desenvolvimento na PR #26, branch
`codex/temas-v05-visual-lab-20260912`. Não há aceite V05, merge na main,
publicação Databricks ou início da V06.

A composição `5cace7f876b2bdb2a1eecaa73e3f7958dfd2764e` incorporou a main
R08 `d5945e04328609878f63857cc15cf5e5039b3e75` à branch de desenvolvimento,
preservando todos os arquivos dessa main e os 16 arquivos novos da candidata.
A comparação das duas frentes mostrou sobreposição somente no README raiz,
em suas contagens derivadas; sua narrativa R08 foi preservada.

O commit `57062e86e0741e88fcd0b30c902ff57ece4be1c8` atualizou as métricas
com a saída medida no run `34761074646`. Sua árvore é
`d9ef6099313f1ab2622e42677b5a3f7e4d812ac5`. As alterações desta rodada não
modificam a implementação, API, schema, fixtures ou ativos visuais da V05.

### Resultado efetivo desta composição

O workflow V05 `34761250018` terminou com success. V00 `34761250014`, V01
`34761250034` e V02 `34761250027` também terminaram com success.
O CI geral `34761250016` continua FAILURE: oito de suas nove etapas passaram,
mas a guarda do inventário do Manual não encontrou a seção
`hub_snippets.visual.theme_lab`. A validação estrutural passou com zero falhas
e zero avisos. Isso não equivale a CI transversal aprovado.

Os checks de PR usam um commit de teste de merge. Para o head `57062e8`, o log
registra `1d83a9456518a0bba639f708bb8e95f9dce8f808`. Resultados pertencem a essa
composição e não se estendem automaticamente ao próximo commit documental.

### Próxima ação e pendências

Completar a seção do laboratório no Manual canônico, preservar todo o texto
anterior, sincronizar sua cópia da raiz e gerar o derivado pela ferramenta
oficial. Registrar a V05 e esta rodada no CHANGELOG raiz; os commits e este
checkpoint não substituem esse registro obrigatório. Completar os índices e
as rotas de navegação, repetir os gates na árvore final e conferir o diff.

Presets escolhidos pela interface, vínculo automático com a base original e
reabertura autônoma continuam lacunas funcionais, não concluídas por este ajuste.
A reabertura atual depende do mantenedor e transforma a proposta em nova base;
hash do JSON não comprova sua linhagem. Não solicitar aceite integral apenas
porque um futuro CI documental ficar verde.

Não foi criado workflow transitório, ampliada permissão ou executado force-push.
A main não foi alterada por esta rodada. Os arquivos da V05 e suas cópias já
derivadas foram reutilizados por seus blobs; não houve re-render completo novo.
Os registros abaixo preservam o estado das tentativas anteriores.

## Estado anterior — retomada R07 em 13/09/2026

V05 em desenvolvimento na branch `codex/temas-v05-visual-lab-20260912`.
A retomada preserva integralmente a main R07 `b73bbb91961f9ba5f9031d648c42ec0891b63347`
e acrescenta os sete arquivos da candidata `133966bf8ee7555d1d9dadd3922d2fc75a4641e9`.
Essa composição não é aprovação dos testes anteriores: exige nova rodada.

Rodrigo autorizou continuar o desenvolvimento. Não concedeu aceite à V05 nem
integração, publicação no Databricks ou início da V06.

## Bloqueios de fechamento — registro da retomada R07

- Corrigir navegação do README dentro do produto publicado.
- Ajustar o notebook sem relaxar a guarda de contrato; registrar saída executada.
- Conferir e corrigir segurança de salvamento e comportamento da interface.
- Completar documentação de primeiro uso, catálogo integrado do Manual e índices.
- Registrar esta execução no CHANGELOG raiz sem truncar seu histórico.
- Gerar fachadas e espelho com as ferramentas canônicas.
- Recalcular o README pela execução na árvore final, sem reutilizar contagens antigas.
- Executar regressões e revisão sobre a composição final; depois solicitar aceite.

## Evidências anteriores

A execução `34733554922` da candidata `a45ebd6` aprovou os 31 casos V05,
329 casos de temas e 12 legados visuais V00, mas REPROVOU a validação documental.
Não é CI aprovado e não testa a composição R07. Consulte [TESTES.md](TESTES.md).

## Limites

Testes Python de objetos ipywidgets não comprovam a renderização nem callbacks
em Databricks. Acessibilidade, usuário iniciante, runtime do workspace, persistência
de sessão, permissões reais e auditoria independente permanecem pendentes.
O laboratório usa dados sintéticos; não aprova nem publica temas.

## Recuperação

Enquanto esta branch não for integrada, nenhuma reversão de main ou publicação
é necessária. Não fazer force-push, não alterar proteções e não sobrescrever
mudanças da frente R07. Preservar execuções reprovadas como evidência.

[Escopo V05](README.md)

## Diagnóstico de acesso e retomada — 13/09/2026

Rodrigo solicitou pesquisar o bloqueio de ferramentas e aplicar uma solução.
A inspeção da configuração do aplicativo GitHub encontrou permissão específica
Allow all actions. Ela já estava configurada; não foi ampliada nesta rodada.
Essa configuração não elimina as proteções de segurança da plataforma.

As tentativas anteriores de transportar um script de preparação foram recusadas.
A causa específica não foi informada. Não atribuir o bloqueio a falta de aceite,
expiração de token, tamanho de arquivo ou erro do GitHub sem evidência própria.
A manutenção documental deve preferir edição direta de texto, com leitura prévia
do arquivo inteiro e conferência do SHA, sem scripts transitórios de escrita.
Não sobrescrever um documento completo usando apenas um trecho retornado pela leitura.

Na consulta desta rodada, a main já estava em
`d5945e04328609878f63857cc15cf5e5039b3e75`. A PR #26 ainda continha a candidata
`5f2dc583a04f66f1851836424d4ed2489188cb78` e indicava conflito de integração.
Portanto, a composição R07 anterior não é mais suficiente para o fechamento:
preservar o avanço da main, reconciliar a candidata e repetir a validação.

O teste de acesso pelo cliente Git do ambiente de edição não conseguiu resolver
o host github.com. Isso é uma limitação de conectividade desse ambiente, não
prova de falha de credenciais nem explicação do bloqueio do aplicativo.
Nenhum segredo foi solicitado ou transferido e nenhuma proteção foi alterada.

Esta nota documenta o diagnóstico, não a conclusão da V05. Manual, CHANGELOG,
índices, geração dos derivados e testes finais continuam exigindo comprovação
de aplicação. Presets, vínculo automático com a base e reabertura autônoma
continuam pendências de escopo; não são encerradas por uma correção de acesso.
