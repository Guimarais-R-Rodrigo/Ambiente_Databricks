# App de autoria visual do Hub

Este diretório contém a superfície **Databricks App** do Sistema de Temas. Ela reutiliza o núcleo de temas e o Visual Lab para experimentar e persistir sessões de autoria de temas de contexto `notebook`. **O App não aprova, promove nem publica temas.**

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Interface Streamlit para autoria visual, executável como Databricks App. |
| Para que serve? | Escolher uma base, ajustar tokens, comparar base × proposta, salvar e reabrir a própria sessão. |
| O que reutiliza? | `hub_snippets.visual.tema`, `hub_snippets.visual.theme_lab` e consumidores Plotly/HTML. |
| Onde persiste? | Em Unity Catalog Volume fornecido ao App pelo recurso `theme_storage`. |
| Quem identifica o usuário? | O proxy do Databricks Apps via `X-Forwarded-User`; o código não aceita papel escrito dentro do tema. |
| O que não faz? | Aprovar, publicar, promover, ativar tema, alterar dados, consultar SQL ou executar ML. |

Comece pelo [guia de primeiro uso](GUIA_PRIMEIRO_USO.md). Implantação e retorno pertencem ao [runbook de administração no repositório](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/readme-readequacao-20261006/docs/guias/temas/DEPLOY_ROLLBACK_APP.md), para o responsável autorizado.

## 1. O que é?

É a interface de autoria do Sistema de Temas. O App não cria um novo motor de temas: ele chama o contrato e as funções do núcleo e do laboratório. Isso evita que Streamlit vire uma segunda fonte de verdade para schema, tokens, validação, preview ou persistência de sessão.

O App também **não implementa o contexto temático `app`** reservado no contrato antigo. O App gerencia propostas de tema `notebook`; tematizar a própria interface do App é outro problema e não é inferido desta entrega.

## 2. Que problema resolve?

O Visual Lab já permite autoria rastreável em notebook, mas exige abrir o notebook e lidar com a superfície de widgets. O App fornece uma entrada de App dedicada para o mesmo fluxo: base → ajustes → validação → comparação → persistência → reabertura.

O objetivo operacional é reduzir a dependência de código para autoria sem transformar conveniência de interface em privilégio de governança.

## 3. Quando usar?

Use quando o App estiver implantado em ambiente autorizado, com acesso restrito ao público definido pelo proprietário do ambiente e com o recurso `theme_storage` configurado para um Unity Catalog Volume com leitura/gravação.

A superfície é `authoring_only`: foi desenhada para proponentes e mantenedores autorizados. Os demais papéis continuam definidos pela política de governança, mas aprovar e publicar não existem tecnicamente neste App.

## 4. Quando não usar?

Não use para:

- declarar alguém `aprovador` ou `publicador` pela interface;
- promover um JSON a padrão compartilhado;
- alterar o tema global do Hub;
- editar dados, métricas ou regras analíticas;
- acessar SQL warehouse, Model Serving, MLflow, Jobs ou Genie;
- substituir revisão de acessibilidade, UAT ou homologação no navegador.

Se um botão, arquivo ou parâmetro sugerir publicação, trate como defeito: o App não contém essa capacidade.

## 5. Como funciona?

`app.py` é somente a camada Streamlit. `app_service.py` concentra identidade e persistência e importa o Visual Lab para salvar, listar e reabrir sessões.

Na inicialização:

1. o App localiza `hub_snippets` e `hub_padroes` no bundle;
2. exige `HUB_THEME_VOLUME` e, fora de desenvolvimento local explícito, aceita somente caminho sob `/Volumes/`;
3. lê a identidade encaminhada pelo Databricks em `X-Forwarded-User`;
4. calcula SHA-256 dessa identidade para criar um namespace de sessão sem colocar o identificador bruto no caminho;
5. carrega os presets de demonstração e cria um `ThemeLabDraft`;
6. todos os ajustes passam pelas mesmas validações e adaptadores já usados pelo laboratório.

## 6. Identidade e papéis

O App não possui seletor de papel. A governança distingue `leitor`, `proponente`, `aprovador`, `publicador` e `mantenedor`; abrir a interface não concede nenhum papel novo.

Nesta interface, a instância de autoria deve ser disponibilizada pelo administrador somente aos grupos reais mapeados para `proponente` e/ou `mantenedor`. A interface não consulta nem grava grupos corporativos, não aceita `role=...` do navegador e não transforma acesso ao App em aprovação.

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

A estrutura interna da sessão segue o contrato do laboratório. `session.json` continua sendo gravado por último e seus hashes são verificados na reabertura. O App não duplica esse contrato.

## 8. Retenção

A política de retenção é conservadora: **nenhuma exclusão automática e nenhum botão de apagar sessão para usuário final**. A aplicação também não reescreve histórico.

Qualquer retenção corporativa futura deve ser aplicada por processo administrativo autorizado no destino. Até que exista essa política, o App preserva registros em vez de inventar prazo de expiração.

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
- adulteração de sessão → reabertura do laboratório recusa hashes divergentes;
- nome de sessão inválido ou existente → salvamento recusa;
- aprovação/publicação → não há função nem botão correspondente.

Os headers identificam a requisição dentro de Databricks Apps; eles não são um mecanismo para conceder papel novo pelo cliente.

**Limite do isolamento:** o namespace organiza a navegação oferecida pelo App. SHA-256 não concede ACL, não cifra conteúdo e não impede acesso direto por identidades que já têm permissão no Volume, inclusive administradores ou service principal. Verifique as permissões reais do App, proxy e Volume no destino.

## 12. Abrir o App autorizado

Abra a instância disponibilizada pelo responsável do ambiente. Se houver erro de identidade ou armazenamento, anote o código e peça suporte. Não habilite modo de desenvolvimento em produção. A preparação local está no [runbook administrativo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/readme-readequacao-20261006/docs/guias/temas/DEPLOY_ROLLBACK_APP.md).

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

Testes com diretórios temporários não comprovam headers reais, permissões do App, UC Volume e renderização final do navegador.

## 14. Implantação e retorno

Implantação e retorno são ações do responsável autorizado, conforme o [runbook administrativo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/readme-readequacao-20261006/docs/guias/temas/DEPLOY_ROLLBACK_APP.md). Reverter o código do App não apaga sessões do Volume nem reverte um tema publicado. O App não publica temas.

## 15. Referências e limites

- [Guia de primeiro uso](GUIA_PRIMEIRO_USO.md)
- [Administração: deploy e rollback](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/readme-readequacao-20261006/docs/guias/temas/DEPLOY_ROLLBACK_APP.md)
- [`app.py`](app.py)
- [`app_service.py`](app_service.py)
- [`app.yaml`](app.yaml)
- [Visual Lab](../../../hub_snippets/visual/theme_lab/README.md)
- [Contrato de identidade visual](../README.md)

O código disponível não comprova deploy, permissões reais, acessibilidade ou experiência no destino. AI/BI possui seu próprio fluxo e não é alterado pelo App.
