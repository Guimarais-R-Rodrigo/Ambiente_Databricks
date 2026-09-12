# Relatório R02 — seis READMEs operacionais do piloto

## Entrega e alcance

A R02 acrescenta READMEs a `train_xgboost`, `isolation_forest`, `pit_join`,
`format_br`, `quick_profile` e `eda_rapida`. O contrato permanece
`0.1.0-candidata`, agora exercitado em seis recursos operacionais. O próximo
passo é avaliação editorial do piloto; não foi iniciada a produção em massa.

Todos os textos seguem as quinze seções: conceito, pergunta apoiada, escolha,
contraexemplos, mecanismo, cenário, requisitos, saída, operação, configurações,
limites, alternativas, checagem do resultado, navegação e referências. Os
requisitos refletem a implementação, não uma descrição genérica da biblioteca.

A [matriz nominal](MATRIZ_ALTERACOES_R02.md) separa novos READMEs, outras
documentações, controle, testes de evidência e derivados. O
[checkpoint](CHECKPOINT_R02.md) registra a base, a autorização e a parada.

## Outras documentações atualizadas

Os seis notebooks receberam backlink e ajustes de interpretação. Seus códigos,
magics executáveis, blocos de resultados e prompt preenchido foram preservados.
O formulário de eda_rapida recebeu um link ao README fora do bloco colável.
Os READMEs das três coleções receberam navegação para os pilotos.

O Manual recebeu caminhos locais dos guias e ressalvas nos pontos pertinentes,
sem duplicar explicações longas nem alterar sua função de catálogo. A cópia
raiz foi sincronizada; o simulado foi gerado pelo renderer. Índices operacionais,
plano, changelog e entrada de sprints receberam a rota para o estado R02.

Somente seis entradas saíram de `CONTROLE_MIGRACAO.json`; não houve mudança no
validador, nos testes permanentes, na regra de ratchet ou no arquivo de
requisitos de desenvolvimento. O novo script de evidências é suplementar e
não foi apresentado como integração automática ao gate permanente.

## Principais achados

Os [achados R02](ACHADOS_R02.md) descrevem os casos completos. Foram corrigidas
universalizações sobre comparação de modelos, contaminação, tracking,
amostragem e garantia de ausência de vazamento. O caso de precisão de inteiros
em `fmt_int` e `fmt_n` foi reproduzido, mas não corrigido funcionalmente.
O risco de overwrite do preparo de eda_rapida aparece antes da rota de uso.

O texto distingue biblioteca e wrapper, ilustração e execução, arquivo de
prompt e ferramentas do agente. A revisão não transforma um defeito conhecido
em característica recomendada; delimita o uso e preserva a evidência.

## Verificação reprodutível

Comandos de manutenção, no checkout da branch:

```bash
python docs/sprints/readmes_objetos/evidencias_r02/verificar_pilotos.py
python tools/render_simulado.py --write
python tools/validate_assistant.py
python tools/ci_local.py --verbose
```

O script suplementar tem 13 casos: três de formatação, quatro de XGBoost,
três de Isolation Forest e três de Spark sobre dados sintéticos. Sem
bibliotecas reais instaladas, os casos pertinentes são pulados explicitamente.
A opção `--require-all` exige todas as dependências e é reservada ao runner
preparado. Não usa mocks para declarar execução.

Na execução local registrada, Python 3.13.5, NumPy 2.3.5, pandas 2.2.3,
scikit-learn 1.8.0 e XGBoost 3.1.3 estavam disponíveis; MLflow e PySpark não.
Os sete casos disponíveis passaram e seis foram pulados. O bloco Python do
README de formatação foi executado literalmente. A comparação de AST e
blocos verifica preservação, não execução dos notebooks Databricks.

Os resultados concretos do gate, checks de preservação e versões ficam em
[EVIDENCIAS_R02.json](EVIDENCIAS_R02.json) e nos arquivos de `evidencias_r02/`.
A validação de contagens do README raiz foi reconciliada com a saída do
validador depois de completar os arquivos, sem remover guardas.

## Estado editorial e operacional

Autoria, revisão técnica e revisão didática: ChatGPT, por autorrevisão.
Auditoria independente e aceite humano dos textos finais: pendentes.
A orientação de prosseguir autorizou o piloto, não é registrada como revisão
de documentos que ainda não existiam. O template não foi congelado.

A branch depende da R01, sem merge automático. Não houve publicação Databricks,
confirmação de políticas do workspace, avaliação conversacional Genie Code ou
execução da escrita persistente de demonstração. A CI permanente do PR e
ensaios suplementares de runner, quando disponíveis, têm seus resultados
registrados no fechamento remoto do PR e no pacote de entrega; não são
presumidos a partir da existência de um workflow.
