# Databricks App V10 — gestão visual do Hub

Este diretório contém a superfície **Databricks App** da V10 do Sistema de Temas. Ela reutiliza o núcleo V02 e o Visual Lab V05 para experimentar e persistir sessões de autoria de temas de contexto `notebook`. **O App não aprova, promove nem publica temas.**

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Interface Streamlit para autoria visual, executável como Databricks App. |
| Para que serve? | Escolher uma base, ajustar tokens, comparar base × proposta, salvar e reabrir a própria sessão. |
| O que reutiliza? | `hub_snippets.visual.tema`, `hub_snippets.visual.theme_lab` e consumidores V03/V04. |
| Onde persiste? | Em Unity Catalog Volume fornecido ao App pelo recurso `theme_storage`. |
| Quem identifica o usuário? | O proxy do Databricks Apps via `X-Forwarded-User`; o código não aceita papel escrito dentro do tema. |
| O que não faz? | Aprovar, publicar, promover, ativar tema, alterar dados, consultar SQL ou executar ML. |

Comece pelo [guia de primeiro uso](GUIA_PRIMEIRO_USO.md). Para implantação autorizada e retorno, use [DEPLOY_ROLLBACK.md](DEPLOY_ROLLBACK.md).

## 1. O que é?

É a primeira superfície de App do Sistema de Temas. O App não cria um novo motor de temas: ele chama o contrato e as funções já integradas nas V02–V05. Isso evita que Streamlit vire uma segunda fonte de verdade para schema, tokens, validação, preview ou persistência de sessão.

A V10 também **não implementa o contexto temático `app`** reservado no contrato antigo. O App gerencia propostas de tema `notebook`; tematizar a própria interface do App é outro problema e não é inferido desta entrega.

## 2. Que problema resolve?

O Visual Lab V05 já permite autoria rastreável em notebook, mas exige abrir o notebook e lidar com a superfície de widgets. A V10 fornece uma entrada de App dedicada para o mesmo fluxo: base → ajustes → validação → comparação → persistência → reabertura.

O objetivo operacional é reduzir a dependência de código para autoria sem transformar conveniência de interface em privilégio de governança.

## 3. Quando usar?

Use quando o App estiver implantado em ambiente autorizado, com acesso restrito ao público definido pelo proprietário do ambiente e com o recurso `theme_storage` configurado para um Unity Catalog Volume com leitura/gravação.

A superfície desta candidata é `authoring_only`: foi desenhada para proponentes e mantenedores autorizados. Os demais papéis continuam definidos pela política V01, mas aprovar e publicar não existem tecnicamente neste App.

## 4. Quando não usar?

Não use para:

- declarar alguém `aprovador` ou `publicador` pela interface;
- promover um JSON a padrão compartilhado;
- alterar o tema global do Hub;
- editar dados, métricas ou regras analíticas;
- acessar SQL warehouse, Model Serving, MLflow, Jobs ou Genie;
- substituir revisão de acessibilidade, UAT ou homologação no navegador.

Se um botão, arquivo ou parâmetro sugerir publicação, trate como defeito: a V10 não contém essa capacidade.

## 5. Como funciona?

`app.py` é somente a camada Streamlit. `app_service.py` concentra identidade e persistência e importa o Visual Lab V05 para salvar, listar e reabrir sessões.

Na inicialização:

1. o App localiza `hub_snippets` e `hub_padroes` no bundle;
2. exige `HUB_THEME_VOLUME` e, fora de desenvolvimento local explícito, aceita somente caminho sob `/Volumes/`;
3. lê a identidade encaminhada pelo Databricks em `X-Forwarded-User`;
4. calcula SHA-256 dessa identidade para criar um namespace de sessão sem colocar o identificador bruto no caminho;
5. carrega os presets de demonstração V05 e cria um `ThemeLabDraft`;
6. todos os ajustes passam pelas mesmas validações e adaptadores já usados pelo laboratório.

## 6. Identidade e papéis

O App não possui seletor de papel. A política canônica continua em `docs/sprints/sistema_temas/V01/politica_workflow.json` com `leitor`, `proponente`, `aprovador`, `publicador` e `mantenedor`.

Nesta V10, a instância de autoria deve ser disponibilizada pelo administrador somente aos grupos reais mapeados para `proponente` e/ou `mantenedor`. A interface não consulta nem grava grupos corporativos, não aceita `role=...` do navegador e não transforma acesso ao App em aprovação.

A ausência de identidade encaminhada bloqueia o App. O fallback de identidade só existe quando `HUB_THEME_LOCAL_DEV=true` e exige `HUB_THEME_LOCAL_USER_ID`, exclusivamente para desenvolvimento/teste local.

## 7. Persistência

A persistência operacional usa um **Unity Catalog Volume** associado como recurso do Databricks App com chave `theme_storage`. O `app.yaml` converte esse recurso na variável `HUB_THEME_VOLUME` por `valueFrom`.

Cada usuário recebe:

```text
<volume>/hub-theme-manager-v10/sessions/<sha256-do-user>/
  <nome-da-sessao>/
    base.json
    proposal.json
    history_000.json ...
    session.json
```

A estrutura interna da sessão é a mesma da V05. `session.json` continua sendo gravado por último e seus hashes são verificados na reabertura. O App não duplica esse contrato.

## 8. Retenção

A política V10 é conservadora: **nenhuma exclusão automática e nenhum botão de apagar sessão para usuário final**. A aplicação também não reescreve histórico.

Qualquer retenção corporativa futura deve ser aplicada por processo administrativo autorizado no destino. Até que exista essa política, a V10 preserva registros em vez de inventar prazo de expiração.

## 9. Custos e recursos

A arquitetura padrão usa somente:

- execução serverless do Databricks App;
- armazenamento do Unity Catalog Volume;
- dependências Python da interface e dos adaptadores já existentes.

Ela não requer SQL warehouse, Lakebase, Model Serving, Jobs ou chamadas a LLM. Portanto, esses serviços não devem ser adicionados “por conveniência”. Valores monetários dependem do contrato/cloud/workspace e não são inventados pela documentação do Hub.

## 10. Configuração

O `app.yaml` usa:

```yaml
command: ['streamlit', 'run', 'app.py']
env:
  - name: HUB_THEME_VOLUME
    valueFrom: theme_storage
  - name: HUB_THEME_APP_MODE
    value: authoring_only
  - name: STREAMLIT_GATHER_USAGE_STATS
    value: 'false'
```

Não coloque PAT, token OAuth, caminho `/Volumes/<...>` específico, usuário, catálogo ou schema corporativo no repositório. O recurso é configurado no ambiente autorizado.

## 11. Segurança e fail-closed

Guardas principais:

- sem identidade do proxy → App para;
- modo diferente de `authoring_only` → App para;
- sem storage → App para;
- storage de produção fora de `/Volumes/` → App para;
- raiz indisponível/symlink → App para;
- sessão de outro usuário → não aparece porque o namespace deriva da identidade atual;
- adulteração de sessão → reabertura V05 recusa hashes divergentes;
- nome de sessão inválido ou existente → salvamento recusa;
- aprovação/publicação → não há função nem botão correspondente.

Os headers identificam a requisição dentro de Databricks Apps; eles não são um mecanismo para conceder papel novo pelo cliente.

## 12. Execução local

A execução local é apenas desenvolvimento. Prepare uma pasta temporária e use um usuário sintético:

```powershell
$env:HUB_THEME_LOCAL_DEV = "true"
$env:HUB_THEME_LOCAL_USER_ID = "usuario-teste"
$env:HUB_THEME_VOLUME = "C:\temp\hub-theme-v10"
streamlit run app.py
```

A pasta precisa existir. Nunca use esse modo como evidência de autenticação Databricks ou de persistência em Unity Catalog.

## 13. Como saber se o resultado faz sentido?

Em ambiente de teste autorizado:

1. abra o App com uma identidade real encaminhada pelo Databricks;
2. altere um token primário e aplique;
3. confirme que base e proposta usam os mesmos dados sintéticos;
4. salve uma sessão;
5. encerre o estado em memória e reabra a sessão;
6. confirme revisão/histórico e hashes;
7. com outra identidade autorizada, confirme que a sessão anterior não aparece;
8. confirme que não existe ação de aprovar ou publicar.

O CI cobre a lógica com diretórios temporários. Só o workspace autorizado pode comprovar headers reais, permissões do App, UC Volume e renderização final do navegador.

## 14. Implantação e retorno

O repositório não envia este App ao workspace automaticamente. `tools/temas_v10_app.py` gera um bundle derivado em `.artifacts/`, contendo App + dependências canônicas necessárias. O procedimento autorizado está em [DEPLOY_ROLLBACK.md](DEPLOY_ROLLBACK.md).

Rollback do **App** significa voltar a uma versão anterior do código/bundle validado. Isso não apaga sessões do Volume. Rollback de **tema publicado** não pertence a esta V10 porque o App não publica temas.

## 15. Referências e próximos gates

- [Guia de primeiro uso](GUIA_PRIMEIRO_USO.md)
- [Deploy e rollback](DEPLOY_ROLLBACK.md)
- [`app.py`](app.py)
- [`app_service.py`](app_service.py)
- [`app.yaml`](app.yaml)
- [Visual Lab V05](../../../hub_snippets/visual/theme_lab/README.md)
- [Contrato de identidade visual](../README.md)
- [Matriz de papéis V10](../../../../../docs/sprints/sistema_temas/V10/MATRIZ_PAPEIS.json)

A V10 candidata não equivale a deploy, UAT, acessibilidade ou publicação. V11/AI-BI não é iniciada por este diretório.
