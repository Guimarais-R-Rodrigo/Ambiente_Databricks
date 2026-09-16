# V13 — S2: preflight operacional unificado

Status: **candidata S2**.

Esta etapa cria uma porta de entrada local e read-only para responder uma pergunta simples antes de qualquer operação do Sistema de Temas:

> **os pré-requisitos que podem ser comprovados localmente estão íntegros e o que ainda impede a operação?**

A S2 não executa a operação. Ela não instala tema, não cria bundle, não salva sessão, não faz deploy de App, não importa ou publica dashboard e não altera workspace theme.

## Para quem nunca entrou no Hub

Pense no preflight como uma lista de conferência automática antes de uma atividade sensível.

Ele pode confirmar, por exemplo:

- se o tema é válido;
- se o SHA-256 informado ainda corresponde aos bytes;
- se um bundle V09 está completo;
- se um bundle V10 passa no verificador já existente;
- se o contexto do tema é compatível;
- se um binding AI/BI aponta para um campo que realmente existe;
- se a operação exige autorização;
- se há rollback preparado;
- se uma identidade de ambiente ainda precisa ser verificada.

O preflight **não transforma uma informação declarada em autorização** e **não autentica o Databricks**. Quando uma condição depende do ambiente real, a saída permanece `BLOCKED`.

## 1. Artefato da S2

A ferramenta é:

`tools/temas_v13_preflight.py`

Os testes permanentes estão em:

`tools/tests/test_temas_v13_s2.py`

A S2 consome a matriz S1:

`docs/sprints/sistema_temas/V13/MATRIZ_OPERACIONAL.json`

e valida essa matriz por composição com:

`tools/temas_v13_operacional.py`

A matriz e o validador S1 **não são reescritos** para declarar que a S2 existe. Eles preservam a fronteira histórica da S1 e continuam dizendo que a S1 não implementou preflight.

## 2. Princípio de composição

A S2 não cria validadores concorrentes quando já existe owner canônico.

Ela compõe:

- V02: `load_theme()` para schema, hash, contexto e integridade do tema;
- V09: `validate_theme_zip()` para presença e hashes do bundle de transição;
- V10: `verify()` para o bundle local do Databricks App;
- V11: `project_theme()`, `bind_native_template()` e a política local de workspace theme;
- S1: matriz operacional, owners, estados de autorização e estratégias de rollback.

Assim, a S2 coordena decisões sem copiar tokens, papéis, bindings, schema ou `theme_contract`.

## 3. O que significa cada estado

A saída usa quatro estados que não são sinônimos.

| Estado | Significado |
|---|---|
| `PASS` | todos os checks aplicáveis àquela operação puderam ser satisfeitos localmente |
| `BLOCKED` | não há falha técnica local suficiente para reprovar, mas falta uma condição que a S2 não pode fabricar, como autorização, identidade efetiva ou rollback ainda bloqueado pelo owner |
| `FAIL` | um contrato ou pré-requisito verificável localmente falhou |
| `NOT_APPLICABLE` | aquele check não pertence à ação analisada |

Precedência do resultado agregado:

`FAIL > BLOCKED > PASS > NOT_APPLICABLE`

Um `BLOCKED` nunca é promovido a `PASS`.

## 4. Contrato de entrada

A entrada é JSON explícito.

### 4.1 Modo por superfície

Use `mode = "surface"` para uma única operação:

```json
{
  "request_version": 1,
  "mode": "surface",
  "operations": [
    {
      "surface_id": "notebook_visual_core",
      "action_id": "render_with_resolved_theme",
      "inputs": {
        "theme": {
          "root_ref": "ambiente_fonte/.assistant",
          "relative_path": "hub_padroes/identidade_visual/exemplos/legado_notebook.json",
          "expected_sha256": "<sha256-dos-bytes>",
          "expected_context": "notebook"
        }
      }
    }
  ]
}
```

### 4.2 Modo agregado

Use `mode = "aggregate"` para várias operações no mesmo relatório determinístico.

Pares repetidos `surface_id + action_id` são recusados. A saída é ordenada por superfície e ação para permanecer determinística.

## 5. Entrada de tema

Quando a operação consome um tema, `inputs.theme` deve declarar exatamente:

- `root_ref`: raiz local relativa ao repositório;
- `relative_path`: caminho do JSON dentro dessa raiz;
- `expected_sha256`: hash dos bytes que o operador pretende usar;
- `expected_context`: contexto esperado.

A S2 delega a validação ao V02. Entre os resultados estáveis:

- `THEME_VALID`;
- `THEME_INVALID`;
- `THEME_HASH_STALE`;
- `CONTEXT_INCOMPATIBLE`.

A ferramenta não substitui o hash por `latest` e não corrige contexto silenciosamente.

## 6. Bundle V09

Para `transition_bundle / build_transition_bundle`, informe:

```json
{
  "bundle_path": "<zip-relativo-ao-repositorio>",
  "authorization_ref": "<referencia-explicita>",
  "rollback": {
    "prepared": true,
    "state_ref": "<estado-anterior-ou-regra-de-descarte>"
  }
}
```

Apesar do nome histórico da ação na matriz S1, a S2 **não constrói** o bundle. Ela verifica um candidato existente usando o owner V09.

Falha de presença, `theme_contract` ou hash retorna `BUNDLE_INCOMPLETE`.

## 7. Bundle e deploy do App V10

`app_bundle_dir` aponta para um bundle local candidato e é validado por `tools/temas_v10_app.py`.

Para `deploy_app`, a S2 também exige que `storage_path` tenha a forma normalizada `/Volumes/...`.

Isso não autoriza deploy. O estado canônico `V12-APP-01 = BLOQUEADO_AUTORIZACAO` continua preservado e produz `AUTHORIZATION_CANONICALLY_BLOCKED`.

## 8. AI/BI

### 8.1 Projeção local

`aibi_dashboard / project_theme`:

- valida o tema pelo V02;
- projeta pelo V11;
- não exige template nativo;
- não executa import.

### 8.2 Import em draft

`aibi_dashboard / import_theme_draft` exige, além do tema:

- `native_template_path`;
- `binding_path`.

A S2 chama o binder V11. Ela não conhece nem inventa schema nativo global.

Códigos específicos incluem:

- `NATIVE_TEMPLATE_HASH_STALE`;
- `JSON_POINTER_MISSING`;
- `AIBI_CAPABILITY_FORBIDDEN`;
- `NATIVE_TEMPLATE_SYNTHETIC`.

O fixture `hub_v11_synthetic_dashboard_draft` continua proibido como export nativo.

Mesmo com binding local válido, uma operação remota permanece `BLOCKED` enquanto a identidade efetiva não puder ser verificada pelo ambiente.

### 8.3 Publish

`publish_dashboard` continua gate separado.

O estado `NOT_AUTHORIZED` da matriz S1 não pode ser sobrescrito por um campo fornecido pelo chamador. A S2 retorna `AUTHORIZATION_CANONICALLY_BLOCKED`.

## 9. Workspace theme

Workspace theme continua superfície administrativa separada.

A S2 consegue carregar a política V11 local, mas não autentica administrador, não cria snapshot vivo e não aplica tema.

Como a matriz mantém:

- autorização bloqueada;
- rollback dependente de autorização/snapshot ainda não operacional;

o resultado continua `BLOCKED`.

## 10. Autorização

Para uma ação mutável que não esteja canonicamente bloqueada, `authorization_ref` precisa existir.

Exemplo:

```json
{
  "authorization_ref": "operator-explicit"
}
```

Esse campo significa somente que o pedido possui uma referência explícita.

**Não significa que a S2 concedeu, validou ou autenticou a autorização.**

Se o owner canônico já marca a ação como `BLOQUEADO_AUTORIZACAO` ou `NOT_AUTHORIZED`, o chamador não consegue converter esse estado em PASS.

## 11. Identidade

Ações `persistent_mutation` e `remote_mutation` dependem de identidade efetiva.

Sem `identity_ref`:

`IDENTITY_REQUIRED`

Com `identity_ref`, a ferramenta ainda retorna:

`IDENTITY_LIVE_UNVERIFIED`

porque o núcleo S2 é deliberadamente offline e não autentica o Databricks.

Isso evita false reassurance: uma referência local não vira prova de identidade viva.

## 12. Rollback

Quando a matriz exige rollback, o pedido precisa declarar:

```json
{
  "rollback": {
    "prepared": true,
    "state_ref": "<referencia-do-estado-anterior>"
  }
}
```

Ausência ou shape incompleto:

`ROLLBACK_NOT_PREPARED`

Se a própria matriz diz que o rollback está bloqueado até existir autorização ou snapshot operacional:

`ROLLBACK_CANONICALLY_BLOCKED`

Um `state_ref` fornecido pelo chamador não substitui essa dívida canônica.

## 13. Saída

A saída é JSON determinístico, sem timestamp.

Estrutura resumida:

```json
{
  "report_version": 1,
  "engine": "V13-S2",
  "mode": "surface",
  "overall_status": "PASS",
  "request_checks": [],
  "operations": [],
  "network_access": false,
  "remote_mutation_performed": false
}
```

Cada operação contém checks com:

- `check_id`;
- `status`;
- `code`;
- `message`.

Os valores arbitrários de `authorization_ref`, `identity_ref` e `rollback.state_ref` **não são reproduzidos no relatório**.

## 14. Execução

Crie um request JSON local e execute:

```bash
python tools/temas_v13_preflight.py --request caminho/do/request.json
```

Exit codes:

| Resultado | Exit code |
|---|---:|
| `PASS` | 0 |
| `NOT_APPLICABLE` | 0 |
| `BLOCKED` | 2 |
| `FAIL` | 1 |

O exit code 2 permite distinguir “operação não está autorizada/preparada” de “contrato local falhou”.

## 15. Códigos estáveis

Os códigos são registrados em `STABLE_CODES` no próprio preflight e cobertos por testes.

A S2 não usa texto livre como contrato de automação. Consumidores devem tomar decisão pelo `status` e pelo `code`, não por parsing da mensagem humana.

## 16. Determinismo

Com os mesmos bytes locais, a mesma matriz e o mesmo request, o relatório é idêntico:

- sem timestamp;
- sem ID aleatório;
- sem consulta de rede;
- sem estado remoto;
- ordem agregada estável.

Se uma condição depende do ambiente remoto, a S2 registra `BLOCKED` em vez de consultar silenciosamente esse ambiente.

## 17. Segurança e fronteiras

O núcleo S2 não importa:

- `requests`;
- `socket`;
- `urllib`;
- `httpx`;
- cliente `databricks`;
- `subprocess`;
- `shutil`.

A ferramenta não escreve arquivos.

Os validadores compostos V09/V10 são usados somente pelas rotas de verificação existentes. Nenhuma função de build/deploy é chamada pela S2.

## 18. Casos obrigatórios de teste

A suíte permanente cobre:

- tema válido;
- tema inválido;
- hash stale;
- contexto incompatível;
- bundle V09 incompleto e válido;
- bundle V10 inválido;
- storage App incompatível;
- JSON Pointer inexistente;
- binding fixado a SHA stale;
- fixture sintético recusado como export nativo;
- autorização ausente;
- autorização canonicamente bloqueada;
- identidade ausente;
- identidade referenciada sem falsa promoção a “verificada”;
- rollback ausente;
- rollback canonicamente bloqueado;
- modo agregado;
- request malformado;
- códigos estáveis;
- ausência de eco de referências sensíveis;
- determinismo;
- ausência de imports de rede/Databricks/mutação no núcleo.

## 19. O que a S2 não faz

A S2 não implementa S3.

Portanto ainda não existem nesta etapa:

- runbook consolidado de release/install/update;
- execução ou dry-run de rollback operacional S3;
- definição de last known good;
- recibo de release;
- staging remoto;
- publicação;
- deploy;
- alteração de ACL;
- workspace theme;
- import remoto adicional;
- fechamento da issue #57.

Esses itens seguem os owners e as etapas do Plano Mestre.

## 20. Ponto de parada

A candidata S2 deve:

1. passar a suíte própria;
2. passar regressões S1 e V01–V12;
3. passar o validador estrutural;
4. preservar qualquer failure intermediário;
5. registrar métricas do README somente depois da medição real;
6. produzir checkpoint S2;
7. reconfirmar `main`, merge-base, ahead/behind e concorrência.

**Parar antes da S3 e aguardar aceite explícito.**
