# Template: Especificação de Pipeline de Dados ou ML

## Escopo e estado
- Objetivo: [dado/feature/scoring/outra entrega]
- Modo solicitado: [planejar/gerar código/execução explicitamente autorizada]
- Perfil/rota da [skill](../SKILL.md): [confirmado ou pendente]
- Estado: [PLANEJADO/NÃO EXECUTADO/parcial/executado e evidência]
- Owner, versão e datas: [informados/observados ou NÃO INFORMADO]

Preflight de especificação não autoriza efeitos: `effects_authorized=false` e
`deployment_status=NOT_RUN` devem ser preservados quando retornados. PASS local
não cria job, schedule, serving ou implantação. Receipt, verificador, Postflight
e oráculo independente aplicáveis continuam exigidos pela rota; este documento
não os substitui nem transforma plano em recurso implantado.

## Datasets e etapas pertinentes

Não impor Bronze/Silver/Gold/Scoring a todos os casos. Criar somente fronteiras
com função clara. Para pipeline sem ML, modelo/Registry/scoring são NÃO APLICÁVEL.

| Etapa/camada necessária | Dataset pretendido | Grão/chave/schema | Regra incremental/replay | Recurso observado |
|---|---|---|---|---|
| [nome] | [destino autorizado ou pendente] | [contrato] | [regra determinística] | [ID/evidência ou NÃO IMPLANTADO] |

## Dependências
- Fontes: [identidade, snapshot, disponibilidade e permissão verificados]
- Modelo, se aplicável: [versão/URI comprovadas ou NÃO APLICÁVEL]
- Feature table, se aplicável: [contrato e identidade ou NÃO APLICÁVEL]
- Compute/dependências: [configuração suportada e autorização]
- Temporalidade: [event_time, available_at, cutoff e tratamento de atraso]

## Schedule e operação, se solicitados

| Etapa | Frequência/SLA pretendidos | Schedule efetivamente configurado | Alerta/runbook/owner |
|---|---|---|---|
| [etapa] | [contrato ou NÃO APLICÁVEL] | [ID e evidência/NÃO EXECUTADO/NÃO APLICÁVEL] | [configuração observada ou plano] |

## Qualidade e monitoramento

| Regra | População/etapa | Critério e autoridade | Ação pretendida | Evidência da execução |
|---|---|---|---|---|
| [schema/chave/freshness/domínio] | [recorte] | [limite definido] | [observar/falhar/descartar com governança] | [resultado ou NÃO EXECUTADO] |

Drift/performance só quando fizerem parte do pipeline; labels, referência,
limiares, custo e disponibilidade devem ser declarados. Quarentena precisa de
implementação/contrato próprio, não é API presumida de uma expectation.

## Persistência e recuperação
- Escritas pretendidas e autoridade: [destino, operação, limites e responsável]
- Overwrite: nunca implícito; idempotência não equivale a sobrescrever tudo.
- Efeito/cleanup observado: [registro, readback, posse e ausência, ou UNKNOWN]
- Após UNKNOWN, recuperar destino exato, effect record e autorização; inspecionar
  somente leitura. Não repetir CREATE/MERGE/DROP para provar efeito anterior.
  Posse sozinha não autoriza nova limpeza; exigir autoridade aplicável.

## Checklist de evidência

| Item | Aplicabilidade | Planejado | Observado e fonte |
|---|---|---|---|
| Fontes e permissões | [sim/N/A e motivo] | [requisito] | [verificado/NÃO VERIFICADO] |
| Modelo UC | [se pipeline ML exigir] | [destino autorizado] | [versão/NÃO EXECUTADO/NÃO APLICÁVEL] |
| Validações | [contrato] | [regras] | [resultados/NÃO EXECUTADO] |
| Schedule | [sim/N/A e motivo] | [configuração] | [ID/NÃO EXECUTADO/NÃO APLICÁVEL] |
| Alertas | [sim/N/A e motivo] | [canal e owner] | [evidência/NÃO EXECUTADO/NÃO APLICÁVEL] |

Nenhum campo preenchido constitui aprovação de deploy, promoção de policy ou
homologação. O próximo passo depende do pedido, do perfil e da autorização.
