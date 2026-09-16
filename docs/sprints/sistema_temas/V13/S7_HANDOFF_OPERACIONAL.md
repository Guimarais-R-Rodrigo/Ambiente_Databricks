# V13 — S7: handoff operacional e fechamento

Status: **candidata S7; homologação humana executada e registrada em PASS**.

Baseline de abertura: merge certificado da S6 na `main`,
`6dfb8707835921f2f48020f383cf571902080109`.

Certificação pós-merge observada antes de abrir esta candidata: **15/15 workflows de `push` com `success`**. O workflow V13 repetiu S1–S6, regressões, V00, validação e fronteiras; o workflow V12 executou também seu gate estrito de `push` com `success`.

Esta etapa implementa somente o handoff operacional e o fechamento candidato da V13. Ela não cria uma nova engine de tema, não executa Databricks remoto, não publica nada e não inicia V14.

O gate humano canônico desta candidata foi inicialmente:

`HUMAN-01 = BLOCKED` — `HUMAN_EVIDENCE_MISSING`.

Após sessão real registrada pelo mantenedor conforme [o protocolo S7](S7_HOMOLOGACAO_HUMANA.md), o estado atual é:

`HUMAN-01 = PASS` — `HUMAN_EVIDENCE_RECORDED`.

Git/CI não fabricaram esse PASS; apenas podem verificar a evidência humana versionada.

## 1. Comece aqui

Este é o ponto de entrada para uma pessoa que não construiu o procedimento.

A regra operacional é simples:

1. identifique a superfície e a ação na [matriz operacional S1](MATRIZ_OPERACIONAL.json);
2. execute o [preflight S2](S2_PREFLIGHT_OPERACIONAL.md) antes de qualquer operação;
3. se o resultado for `FAIL` ou `BLOCKED`, **pare** e use o [runbook de diagnóstico S4](S4_OBSERVABILIDADE_DIAGNOSTICO.md);
4. se for necessário preparar release/staging local, use o [runbook S3](S3_RELEASE_OPERACIONAL.md);
5. para limites de contraste, Light/Dark/high-contrast e consumidores fora do contrato, consulte [S5](S5_COMPATIBILIDADE_ACESSIBILIDADE.md);
6. para saber o que já foi exercitado localmente/simulado, consulte [S6](S6_ENSAIOS_OPERACIONAIS.md);
7. só execute ação remota quando existir autorização específica, identidade/permissão efetiva e rollback aplicável — nenhum desses requisitos é fabricado por esta S7.

### O que os estados significam

| Estado | O que o operador deve entender |
|---|---|
| `PASS` | os checks aplicáveis daquele owner passaram no alcance observado; não implica autorização remota ou Publish |
| `BLOCKED` | falta uma condição que o sistema não pode fabricar; pare até resolver o bloqueio |
| `FAIL` | um contrato/check verificável falhou; corrija a causa antes de repetir |
| `NOT_APPLICABLE` | o check não pertence à ação; não o chame de PASS |

Precedência operacional herdada: `FAIL > BLOCKED > PASS > NOT_APPLICABLE`.

## 2. Escolha a rota certa

| Se você quer... | Owner/artefato a abrir primeiro | Próximo gate |
|---|---|---|
| verificar tema notebook/Plotly/HTML | S1 + V02/V03/V04 | S2 preflight |
| revisar proposta no Visual Lab | V05 | S2; persistência real continua separada |
| preparar/transitar bundle V09 | V09 | S2 → S3 local |
| preparar bundle do App V10 | V10 | S2 → S3 local; deploy real separado |
| trabalhar com AI/BI draft | V11 | S2; import, verificação e Publish continuam separados |
| tratar workspace theme | V11/S1 | S2 deve permanecer `BLOCKED` sem autorização/identidade/snapshot reais |
| diagnosticar `FAIL`/`BLOCKED` | S4 | seguir `safe_code` e próxima ação segura |
| verificar contraste/compatibilidade | S5 | manter issue #57/A11 até nova evidência aplicável |
| conferir ensaios já executados | S6 | não promover PASS local para ambiente real |

A S7 referencia esses owners; ela não copia schema, tokens, papéis, bindings ou manifesto para uma nova fonte de verdade.

## 3. Primeira operação — treinamento local seguro

A homologação humana S7 usa somente bytes versionados e artefatos sintéticos/sanitizados. Ela **não** requer Databricks real.

O exercício tem dois cenários: um `PASS` local e um `BLOCKED` esperado. O participante deve executar ambos sem instrução verbal do autor.

### 3.1 Pré-requisitos

- checkout da candidata S7;
- Python disponível;
- dependências de manutenção instaladas conforme o repositório;
- diretório `.artifacts/` disponível para arquivos temporários locais;
- nenhum token Databricks é necessário;
- nenhuma autorização remota é necessária porque nenhuma mutação remota será executada.

### 3.2 Cenário A — notebook local deve retornar PASS

Tema de treinamento:

`ambiente_fonte/.assistant/hub_padroes/identidade_visual/exemplos/legado_notebook.json`

Calcule o SHA-256 dos bytes atuais:

```powershell
python -B -c "from pathlib import Path; import hashlib; p=Path('ambiente_fonte/.assistant/hub_padroes/identidade_visual/exemplos/legado_notebook.json'); print(hashlib.sha256(p.read_bytes()).hexdigest())"
```

Crie `.artifacts/s7-notebook-preflight.json`, substituindo `<SHA256>` pelo valor exibido:

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
          "expected_sha256": "<SHA256>",
          "expected_context": "notebook"
        }
      }
    }
  ]
}
```

Execute:

```powershell
python -B tools/temas_v13_preflight.py --request .artifacts/s7-notebook-preflight.json
```

Resultado esperado no alcance local:

- `overall_status = PASS`;
- código `THEME_VALID` presente;
- `network_access = false`;
- `remote_mutation_performed = false`.

O participante deve explicar por escrito por que esse PASS **não** prova browser, workspace, publicação ou ambiente Databricks.

### 3.3 Cenário B — workspace theme deve permanecer BLOCKED

Crie `.artifacts/s7-workspace-preflight.json`:

```json
{
  "request_version": 1,
  "mode": "surface",
  "operations": [
    {
      "surface_id": "workspace_theme",
      "action_id": "apply_workspace_theme",
      "inputs": {}
    }
  ]
}
```

Execute:

```powershell
python -B tools/temas_v13_preflight.py --request .artifacts/s7-workspace-preflight.json
```

Resultado esperado:

- exit code 2;
- `overall_status = BLOCKED`;
- código `AUTHORIZATION_CANONICALLY_BLOCKED` presente;
- nenhuma mutação remota.

O participante deve registrar que a ação correta é **parar**, não inventar autorização, identidade ou snapshot.

### 3.4 Diagnóstico do bloqueio

Use o [runbook S4](S4_OBSERVABILIDADE_DIAGNOSTICO.md) para classificar o bloqueio como governança/autorização e localizar a próxima ação segura. Não cole token, URL privada, path de Volume, usuário, e-mail ou mensagem sensível no registro.

### 3.5 Localize o rollback

Sem executar mudança remota, o participante deve localizar no [runbook S3](S3_RELEASE_OPERACIONAL.md):

- o conceito de Last Known Good;
- o runbook de rollback;
- a regra de que rollback precisa ser preparado antes da mutação;
- a distinção entre rollback local e rollback de ambiente.

Isso mede capacidade de navegação operacional; não autoriza uma restauração real.

## 4. Matriz de decisão — “o que fazer quando...”

| Situação observada | Classificação | Ação segura | Não faça |
|---|---|---|---|
| request/schema/contexto inválido | `FAIL` / contrato | volte ao owner e corrija a entrada | não ajuste hash/campo para contornar o gate |
| SHA/inventário/manifesto divergente | `FAIL` / artefato | regenere/revalide pelo owner canônico | não edite hash manualmente |
| preflight local `BLOCKED` por autorização | `BLOCKED` / governança | obtenha autorização específica no fluxo existente | não invente `authorization_ref` como prova |
| identidade/permissão real não comprovada | `BLOCKED` / ambiente | valide no ambiente autorizado | não use CI como prova de identidade viva |
| rollback não preparado | `BLOCKED` | prepare LKG/snapshot/estado anterior antes de mutar | não execute primeiro para “testar” |
| staging local falhou | `FAIL` | interrompa, preserve evidência e corrija a causa | não emita recibo de sucesso |
| S2/S3 passou, mas falta evidência | `BLOCKED` / evidence gap | colete a classe de evidência faltante | não promova ausência a PASS |
| contraste A11 histórico reaparece | `FAIL` de acessibilidade | mantenha issue #57 e siga S5 | não transforme `cellFormat` em token nem amplie V11 |
| estado não foi exercitado | `NOT_APPLICABLE` ou não observado | registre o limite | não infira PASS |
| AI/BI draft foi importado | alcance limitado | verifique semântica/rollback | não confunda Import theme com Publish |
| workspace theme solicitado | admin separado | exija autorização, identidade e rollback próprios | não trate como “AI/BI maior” |
| dúvida sobre superfície/owner | navegação | volte à matriz S1 | não crie segunda regra local |

## 5. Registro dos ensaios já disponíveis

Este handoff não reexecuta nem reescreve evidências históricas. Ele aponta para os registros canônicos:

| Evidência | Registro | Leitura correta |
|---|---|---|
| inventário/owners | [S1](S1_INVENTARIO_OPERACIONAL.md) | referência operacional; não duplica contratos |
| preflight/mutantes | [checkpoint S2](CHECKPOINT_S2.md) | decisão local read-only |
| release/staging/rollback dry-run | [checkpoint S3](CHECKPOINT_S3.md) | não é aplicação remota |
| diagnóstico/sanitização | [checkpoint S4](CHECKPOINT_S4.md) | não autentica evidência externa |
| compatibilidade/acessibilidade | [checkpoint S5](CHECKPOINT_S5.md) | A11/#57 permanecem honestos |
| cinco ensaios locais/simulados | [checkpoint S6](CHECKPOINT_S6.md) | PASS local não vira PASS de ambiente |

Estados herdados que permanecem distintos:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 já evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

## 6. Dívidas transferíveis à V14

A S7 registra dívida; não antecipa governança V14.

### 6.1 Dívida técnica/experimental ainda aberta

1. **A11-01 / issue #57:** contraste insuficiente em formatação condicional explícita continua FAIL até correção + nova evidência aplicável. `cellFormat` não vira token por conveniência.
2. **V12-LAB-01:** ambiente Visual Lab real permanece `BLOQUEADO_AUTORIZACAO`.
3. **V12-APP-01:** deploy real do App permanece `BLOQUEADO_AUTORIZACAO`.
4. **V12-AIBI-02:** workspace theme real permanece `BLOQUEADO_AUTORIZACAO`.
5. **Estados Light/Dark/high-contrast não observados:** continuam não inferidos além da evidência disponível.

### 6.2 Assuntos reservados à V14 pelo Plano Mestre

A S7 **não define** nesta candidata:

- production readiness final;
- owner operacional definitivo ou substitutos;
- suporte sustentado;
- severidades/incidentes formais;
- SLA/SLO sem base real;
- canais corporativos/escalonamento final;
- retenção/housekeeping final;
- custos observados em operação real;
- calendário de revisão/depreciação;
- decisão final de go-live.

`V14_NOT_STARTED = true` enquanto esta candidata não tiver sido aceita, integrada e auditada pós-merge.

## 7. Rollback do próprio release V13

O fechamento V13 é um release de Git/documentação/ferramentas locais; esta S7 não altera Databricks. Portanto o rollback do release V13 deve ser **não destrutivo e rastreável**.

### 7.1 Last Known Good pré-fechamento

Antes da integração S7, o LKG de Git é o merge S6 certificado:

`6dfb8707835921f2f48020f383cf571902080109`.

Esse SHA identifica o estado anterior à candidata S7. Ele não é um “rollback de workspace”.

### 7.2 Se a integração S7/V13 causar regressão

1. pare novas promoções;
2. identifique o merge exato que integrou a S7;
3. preserve logs/checks do failure;
4. crie uma reversão normal do merge em branch/PR própria — **não use force-push/reset da `main`**;
5. execute novamente os gates aplicáveis;
6. confirme que contratos V01–V12, issue #57 e os três casos bloqueados mantêm o estado correto;
7. só considere a restauração concluída quando a nova `main` estiver certificada.

Como não houve mutação Databricks nesta S7, não há estado remoto criado por ela para apagar. Se no futuro existir uma ação remota separadamente autorizada, o rollback dessa ação pertence ao owner/runbook específico e não é substituído pelo revert Git.

### 7.3 Critério de abandono seguro

Se a reversão não reproduzir o LKG esperado, se o artefato/commit não puder ser identificado ou se algum owner canônico divergir, pare e preserve evidência. Não force a `main` e não improvise correção em produção.

## 8. Homologação humana — executada

O protocolo executado e a evidência sanitizada estão em [S7_HOMOLOGACAO_HUMANA.md](S7_HOMOLOGACAO_HUMANA.md).

Critério canônico do Plano Mestre: um operador autorizado que não tenha construído o procedimento deve, sem instrução verbal do autor:

- encontrar o runbook correto;
- executar o preflight;
- interpretar `PASS`, `BLOCKED` ou `FAIL` corretamente;
- verificar o alcance do resultado;
- localizar o rollback.

Sessão registrada pelo mantenedor:

- participante sanitizado: `Tester`;
- autorizado: `true`;
- não construtor: `true`;
- duração: `5 minutos`;
- ajuda verbal: `0`;
- ajuda documental extra: `0`;
- erros de interpretação: `0`;
- H1–H6: `PASS`;
- resultado humano: `PASS`.

Estado atual:

`HUMAN-01 = PASS` — `HUMAN_EVIDENCE_RECORDED`.

Esse resultado é formativo e de uma única sessão. Não produz inferência estatística, SLA/SLO, production readiness ou autorização Databricks.

## 9. Fronteira de segurança S7

Esta candidata preserva:

- `V13_S7_NETWORK=0` no núcleo do handoff;
- `V13_S7_REMOTE_MUTATION=0`;
- `V13_S7_DATABRICKS_MUTATION=0`;
- `V13_S7_HUMAN_VALIDATION=PASS` sustentado por evidência humana versionada, não por CI autônoma;
- `V13_V14_NOT_STARTED=1`;
- nenhum `DATABRICKS_HOST`/`DATABRICKS_TOKEN` no workflow;
- nenhum segredo/PII em evidência versionada;
- nenhuma publicação implícita.

## 10. Ponto de parada

A candidata S7 já cumpriu:

1. validação automatizada do handoff;
2. regressões S1–S6/V01–V13;
3. validação documental;
4. homologação humana S7 real e sanitizada.

Restam:

5. checkpoint final S7/V13;
6. recertificação do SHA exato que contém a evidência e o checkpoint;
7. reconfirmação de `main`, merge-base, ahead/behind, issue #57, concorrência e diff;
8. aceite explícito para integrar.

Mesmo com `HUMAN-01 = PASS`, a V13 ainda não deve ser chamada de integrada/encerrada até o checkpoint final, recertificação e aceite do mantenedor.

**Não iniciar V14 por esta candidata.**
