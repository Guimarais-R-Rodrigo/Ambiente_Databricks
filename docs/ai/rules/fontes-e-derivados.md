# Fontes, derivados e efeitos

Leia antes de editar produto/Manual, gerar, empacotar ou publicar. Invariantes
críticas também estão no [núcleo](../../../AGENTS.md); este detalhe não as reduz.

## Camadas

| Camada | Local/owner | Contrato |
|---|---|---|
| Canônica | Git deste repositório | única fonte editorial editável |
| Produto | `ambiente_databricks/` | `.assistant/` e `.assistant_instructions.md` editáveis apenas em escopo de produto |
| Derivada | `.artifacts/simulado/` | espelho produzido por `tools/render_simulado.py`, nunca à mão |
| Operacional | workspaces Free/trabalho | cópias publicadas, não canônicas |
| Congelada | `Ambiente_Antigo/` e entregas históricas | referência read-only; quarentena local não publicável |

Melhoria descoberta no workspace precisa ser registrada na fonte sanitizada antes
de ser incorporada/republicada. Não importar indiscriminadamente estado remoto.
O Manual Técnico V2 é escrito no produto, tem partes de leitura conferidas e é renderizado;
veja [regra editorial](documentacao.md#manual-tecnico).

## Dados

Nada de identificadores corporativos, PII, username/path real do trabalho ou
segredos no Git, Free, prompts/skills ou evidência compartilhada. Use placeholders;
backup/erros brutos corporativos permanecem no destino autorizado. Quarentena não
é corpus de auditoria pública. A exceção `AZUL_CAIXA` e nomes equivalentes da paleta
([decisão da paleta](../../../CHANGELOG.md#paleta-institucional)) permanece; `CORPORATE_RE` não deve alcançá-la. Nenhuma outra
identidade corporativa é permitida por essa exceção (ADR-0003/0009).

Free usa somente sintéticos; trabalho usa dados reais sob política/UC/PII e escopo
expressamente autorizado. Segredos pertencem ao mecanismo de credenciais
aprovado, nunca a instruções, template, Git ou logs.

## Ciclo

Mudança no comportamento exige na mesma sessão: validador, re-render autorizado,
marco no changelog e ADR quando estrutural; detalhe da execução fica no owner
da evidência. Não reivindique conclusão se um gate exigido
está ausente; reporte BLOCKED e motivo. Documentação de manutenção não muda
runtime, manifests, schemas, policy nem licença por associação.

Owners executáveis: `tools/project_policy.py` lista identidades/diretórios geridos;
`tools/validate_assistant.py` verifica seu escopo; `tools/notebook_marker.py`
diferencia módulo de notebook; publicador/kit definem inventário e manifesto.
Não congelar quantidade antiga como critério nem presumir todo `.py` como FILE.

## Render

Sem flag, `python tools/render_simulado.py` mostra o plano local. `--write` remove
e recria a árvore completa; uma divergência não autoriza apagar diretório alheio.
`--output-root` permite somente subdiretórios gerados dentro de `.artifacts/`;
`--check` compara paths, bytes/hashes e tipos com inventário não vazio. O diff Git
não cobre saída ignorada e não substitui esse gate.
Antes de escrever: valide a fonte, registre destino/inventário/extras, confira
ownership e autorização, preserve trabalho desconhecido e prefira clone/cópia
isolada em ensaio. Extras ou conflito bloqueiam a parte destrutiva até decisão.

Na campanha IA anterior, o payload foi congelado; sua baseline e evidências
continuam imutáveis. `ai_controls --migration-freeze` reproduz essa exigência
histórica e pode falhar após uma mudança de produto autorizada posteriormente.
O gate normal verifica paridade dinâmica da fonte atual com o derivado atual.
O [ADR-0026](../../decisions/ADR-0026-arquitetura-projeto-e-historia.md) separa esses
contratos: não reescreva a baseline para legitimar o delta. `README_GERADO.md`
continua gerado, nunca editado à mão; só o integrador finaliza derivados comuns.

## Publicacao

O Free usa `tools/publicar_free.py` (ADR-0005, supersede engine do ADR-0002), com
critérios de conferência no código (ADR-0008). A sequência é validar → render
autorizado → plano → execute autorizado → verify; o plano do publicador consulta
CLI autenticada e não é offline. Confirme profile, host Free e identidade runtime.

Publicação e verificação são distintas: inventário/tipos/ausentes/obsoletos não
provam bytes; `--verify --conteudo` compara conteúdo na forma documentada. Falha
parcial exige conferir recibo/estado antes de repetir. Remover obsoleto é efeito
separado com alvo e autorização, nunca limpeza de pasta inteira por conveniência.
Preserve MCP, `global-*` de outra origem e todo conteúdo não gerido.

Trabalho segue [runbook manual](../../playbooks/replicacao-trabalho.md) e
[checklist](../../playbooks/checklist-replicacao.md): manifesto físico atual,
backup completo Zip - Source (DBC sozinho não basta), staging, promoção seletiva
e instruções por último. Não presumir número fixo de pastas. MLflow/UC começam
desativados; ativação exige escopo. Notebook de aceite não instala/exclui por
conta própria. Reexecute após promoção em nova sessão Python/chat.

Squad requer revisão/admin/governança próprios. Arquivo transportado, Git
integrado, kit preparado, teste Free ou texto de skill não comprova instalação,
ativação, publicação, homologação corporativa ou autorização de produção.

## Evidencia

Registre SHA, comando/ação, ambiente/versão, esperado, observado, exit code quando
aplicável e limites. Só observação sustenta PASS. Preservado/encaminhado é
disposição de rastreabilidade, não resultado executado. Static check não comprova
Spark, forward test não comprova resultado numérico, Free não comprova ACL do
trabalho. Falta de permissão/capacidade bloqueia somente a ação dependente.

## Referências congeladas no produto

Na campanha IA de 06/10, os metadados `fact_sources` de `visual_contracts.yaml`
foram preservados no payload congelado. Na faxina de 07/10, autorizada também
para o produto, essas rotas passaram aos owners atuais em `docs/ai/` e à fonte
`ambiente_databricks/`. A baseline e seus hashes históricos continuam intactos;
`--migration-freeze` reproduz o contrato antigo e não aprova esta revisão nova.
O exemplar de skill transportado continua template, sem contar como procedimento
operacional. Ver [execução](../../manutencao/execucao-faxina-2026-10-07.md).
