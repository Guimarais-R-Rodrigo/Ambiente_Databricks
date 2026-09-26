# 14 — Checklist que impede o próximo handoff defeituoso

Este checklist é a matriz genérica de prontidão criada durante B0, não um status vivo. B0 já foi qualificado/integrado. Para B1, cada item só vale quando o gate corrente o referencia; o state source vivo é `B1/AUTHORING_STATE.json`. Não converter antigos `NOT_YET_PROVEN` de planejamento em blockers atuais sem evidência.

| ID | Área | Condição objetiva | Fase |
|---|---|---|---|
| RD01 | Mandato | Adendo formalizado, scope/roles claros e nenhuma contradição normativa sem decisão. | AUTHORING |
| RD02 | Base | SHA/tree e vetor before/allowed_after nominais, independentes da candidata. | AUTHORING |
| RD03 | Implementação | Código real e APIs públicas existentes, assinaturas/retornos/efeitos inspecionados. | AUTHORING |
| RD04 | Sintaxe | Parse/imports/schemas dos arquivos alterados e fixtures sem erro conhecido. | AUTHORING |
| RD05 | Fases | Testes e gates funcionam na fase a certificar; fixture L2 não exige policy global L2 após promoção. | AUTHORING |
| RD06 | Cobertura | Todas as famílias SE08/CI/SER01 mapeadas até métodos, sem omissão inexplicada. | AUTHORING |
| RD07 | Oráculos | Positivos conferíveis e negativos que chegam à fronteira pretendida; sem cálculo esperado circular. | AUTHORING |
| RD08 | Casos | Todos os casos aplicáveis têm test IDs, parâmetros, fixture hashes, tolerâncias e saídas. | AUTHORING |
| RD09 | Coleta | Lista de testes coletados fecha com a lista esperada; skips/xfails/NA autorizados e explícitos. | QUALIFICATION |
| RD10 | Mecanismo | M01–M28 implementados/qualificados; nenhuma falsificação de PASS aceita. | QUALIFICATION |
| RD11 | Cliente | Modelos/versão/configuração efetivos observados; TOML suportado e sem overrides perigosos. | QUALIFICATION |
| RD12 | Sandbox | Tentativas negativas de escrita/credencial/escape realmente bloqueadas; não apenas prompt. | QUALIFICATION |
| RD13 | Recursos | Clones, processos, temporários, budgets e leases exclusivos prontos. | QUALIFICATION |
| RD14 | Concorrência | Dois pilotos sem mistura de evidência, colisão ou propagação excessiva de falha. | QUALIFICATION |
| RD15 | Diagnóstico | Falhas independentes coletadas com first failure preservado, sem reparo automático. | QUALIFICATION |
| RD16 | Freeze | Renderer/snapshot realizados antes, git limpo, deltas permitidos, envelope externo SHA-bound. | FREEZE |
| RD17 | Comandos | Registry fechado e hashes de argv/scripts, sem placeholder não resolvido ou shell arbitrário. | FREEZE |
| RD18 | Evidência | RAW imutável, SHARE separado, verificador independente e falha de persistência exercitada. | FREEZE |
| RD19 | Auditoria | Dois papéis independentes, contratos/finding schemas prontos e critérios anteriores aos resultados. | FREEZE |
| RD20 | Externo | Capacidade/identidade do ambiente e destinos autorizados; caso literal e transporte testados. | EXTERNAL |
| RD21 | Observabilidade | Grau mínimo por caso estabelecido; ausência de UI não é substituída por narrativa privada. | EXTERNAL |
| RD22 | Efeitos | Exit e efeito separados; readback/cleanup autorizados; sem retry de escrita desconhecida. | EXTERNAL |
| RD23 | Promoção | Somente após provas/aceite específico; delta final permitido de policy e nova certificação. | PROMOTION |
| RD24 | Merge/Publicação | Aceite do SHA exato, remotos reconfirmados, árvore integrada e deployment distinguidos. | INTEGRATION |

## Contraditório obrigatório antes da delegação

O revisor tenta demonstrar que a candidata ainda pode produzir um resultado enganoso: teste temporal stale, pacote com schema que aceita campo desconhecido, chamada omitida com output plausível, um ERROR escondido entre falhas admitidas, ou uma publicação com efeito não observado. Se o problema já é conhecido, corrigi-lo na autoria; não entregar ao executor como surpresa deliberada.

Confirmar também a economia do processo: a task não contém etapas duplicadas sem motivo, uma falha independente não cancela tudo, um finding editorial não reabre automaticamente uma campanha funcional e o usuário não precisa copiar repetidamente a mesma evidência. Rigor deve detectar risco, não acrescentar cerimônia sem informação.

## Critério de saída

Gates da fase sem bloqueio material; evidências verificáveis; nenhum teste obrigatório não implementado; limites explícitos. O marco resultante é liberação da próxima fase, não aprovação de todas as seguintes.
