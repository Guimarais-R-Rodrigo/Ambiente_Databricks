# Instruções do projeto `{{NOME_DO_PROJETO}}`

> TEMPLATE PERSONALIZADO. Copie este arquivo para a raiz real do projeto e renomeie
> a cópia para `AGENTS.md`. O arquivo com nome `AGENTS_TEMPLATE.md` não é descoberto
> automaticamente. Remova este aviso da cópia final.

## Escopo

- Aplique estas instruções somente a arquivos deste diretório e descendentes.
- Objetivo: {{OBJETIVO_E_DECISAO_SUPORTADA}}.
- Unidade de análise: {{GRANULARIDADE}}; chave: {{CHAVE}}.
- Owner técnico: {{OWNER_TECNICO}}; owner de negócio: {{OWNER_NEGOCIO}}.

## Recursos autorizados

- Desenvolvimento: `{{CATALOGO_SCHEMA_DEV}}`.
- Stage: `{{CATALOGO_SCHEMA_STAGE_OU_NAO_APLICAVEL}}`.
- Produção: `{{CATALOGO_SCHEMA_PROD_OU_SOMENTE_LEITURA}}`.
- Fontes permitidas: {{FONTES_E_PAPEIS}}.
- Não invente recursos, colunas, credenciais ou regras. Se algo essencial não estiver
  no contexto atual, sinalize a lacuna e peça o recurso com **Add context** ou `@`.

## Regras de dados e tempo

- Ponto de observação/predição: {{CUTOFF_OU_NAO_APLICAVEL}}.
- Horizonte: {{HORIZONTE_OU_NAO_APLICAVEL}}.
- Preserve a granularidade após joins e reporte contagens antes/depois.
- Não use informação disponibilizada depois do cutoff nem proxies proibidos:
  {{COLUNAS_OU_REGRAS_PROIBIDAS}}.
- Trate PII conforme {{POLITICA_OU_REFERENCIA}}; nunca exponha linhas identificáveis.

## Convenções do projeto

- Linguagens/bibliotecas: {{PYSPARK_SPARK_SQL_PLOTLY_OUTRAS}}.
- Nomes e organização: {{CONVENCOES_ESPECIFICAS}}.
- Parâmetros de ambiente devem ficar em configuração; não codifique caminhos pessoais,
  tokens, senhas ou IDs de recursos no código.
- Prefira operações idempotentes e funções nativas do Spark a UDFs Python.

## Limites de ação

- Pode realizar leituras e inspeções de baixo impacto necessárias à tarefa.
- Antes de executar operação cara, instalar dependência, gravar tabela, alterar
  permissão, fazer deploy, iniciar job/pipeline ou afetar produção, apresente plano,
  alvo e impacto e obtenha autorização explícita.
- Nunca sobrescreva produção como etapa de exploração.

## Testes e conclusão

- Execute: `{{COMANDO_DE_TESTE_OU_VALIDACAO}}`.
- Valide schema, contagens, granularidade, nulos críticos e período.
- Definition of Done: {{CRITERIOS_TESTAVEIS}}.
- Ao concluir, entregue evidências, limitações, mudanças feitas e ações pendentes.

## Referências essenciais

- {{ARQUIVO_OU_LINK_ESSENCIAL_1}}
- {{ARQUIVO_OU_LINK_ESSENCIAL_2}}

Não presuma que referências são carregadas automaticamente: inclua aqui o detalhe
indispensável e solicite que recursos adicionais sejam anexados ao chat.
