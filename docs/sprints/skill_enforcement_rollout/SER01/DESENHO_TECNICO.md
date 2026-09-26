# SER01 — desenho A1 da validação repo-side

## 1. Direção e recorte

Aplicação da direção aceita no [ADR-0022](../../../decisions/ADR-0022-certificacao-prospectiva-ser.md), sem reescrevê-lo. O alvo continua `object_validation=L3`, com `object_shape=L2`, `scope_mode=stage_specific` e `rollout_mode=audit`.

A1 constrói a primitive de validação **antes** da integração na skill e da promoção. Não cria um writer universal. Criar um objeto, validar seus bytes, executar seu exemplo e autorizar sua aplicação são eventos distintos.

## 2. Achados revalidados

O piloto existente em `skills/hub-ml-criar-objeto/scripts/run.py` cobre `create/readme/agregador`, com `generate` e `apply` separados e writer Windows/NTFS. Não é alterado nesta candidata.

`tools/skill_enforcement/validate_create_readme.py` já executa validação de README em overlay. A1 reutiliza seus `_process_runner` e `_readme_checks`; não copia o supervisor de processos, cleanup ou a regra de README agregador. Esse uso de APIs internas repo-side é explícito e exige regressão quando elas mudarem.

O builder/verifier de Receipt V1 em `hub_scripts/skill_execution/receipt/__init__.py` exige proveniência `numeric_columns=runtime_derived`. A1 **não** inventa uma coluna numérica para passar por ele e **não** relaxa o contrato EDA. Emite `SER01-LOCAL-VALIDATION-1`, um registro local ainda não integrado como Receipt da skill.

As assertions em `test_skill_enforcement_se08.py` continuam exigindo criar-objeto L2, cinco contratos e o perfil SE08 no CI. Não são editadas. A composição prospectiva SER precisa ser concluída antes de qualquer promoção; o verde histórico não será obtido trocando L2 por L3 nessa suíte.

## 3. Interface

Entrada fechada `SER01-OBJECT-PACKAGE-1`:

```json
{
  "candidate_version": "SER01-OBJECT-PACKAGE-1",
  "base_sha": "<SHA Git completo da candidata>",
  "context": {
    "operation": "create",
    "object_type": "notebook",
    "object_name": "ensaio_ser01",
    "type_confirmed": true,
    "existing_capability_checked": true,
    "existing_capability_status": "not_found",
    "destination_relative": "<destino .py relativo a .assistant>"
  },
  "files": {
    "<mesmo destino relativo>": "<conteúdo completo UTF-8/LF>\n"
  }
}
```

O exemplo é formato, não payload pronto para executar. A CLI exige `--candidate`, `--repo-root`, `--evidence-dir` e `--evidence-authorized`. Sem autorização da evidência, nenhum processo ou diretório de validação é criado.

Os caminhos são relativos a `.assistant`, nunca a `tools/` ou à raiz do Git. A allowlist exige o pacote exato: quatro arquivos para snippet/script; três para prompt; um para notebook/README agregador. A1 limita cada pacote a quatro arquivos e dois MiB de conteúdo UTF-8. Não normaliza silenciosamente traversal, aliases, drive-relative, UNC, ADS, nomes reservados, case de README ou campos desconhecidos.

## 4. Fluxo implementado

1. Copiar a entrada e conferir schema/bytes/escopo, sem I/O de produto.
2. Exigir evidência externa autorizada, diretório novo, checkout pertencente ao entrypoint, base exata, worktree limpa e histórico completo.
3. Capturar identidade, hashes das ferramentas e policy; executar o preflight L2 real e confrontar seu destino com o envelope.
4. Ler o template efetivo. Leitura e hash não são apresentados como aprovação editorial.
5. Executar o validator na base. Base inválida bloqueia a análise de regressão do objeto.
6. Clonar sem hardlinks, fazer checkout detached do SHA e criar arquivos exclusivamente no overlay.
7. Adicionar **somente os caminhos esperados** ao índice do overlay. Assim, varreduras baseadas no inventário Git não deixam de ver os arquivos propostos.
8. Para snippet/script, executar `api_publica.py` e comparar os bytes da fachada fornecida com a saída canônica, sem consertar o pacote para fazê-lo passar.
9. Para README agregador, executar a verificação existente de forma/inventário/links.
10. Executar `validate_assistant.py` no overlay. Não importar nem executar o módulo/notebook candidato.
11. Conferir HEAD, índice exato, ausência de delta não esperado, igualdade dos bytes e preservação do checkout original.
12. Persistir logs e `validation.json`; falha de evidência ou de pós-checagem mantém FAIL.

O supervisor é o já integrado na manutenção A07, incluindo tratamento de streams Win32. Não se implementam retry, sleep de estabilidade ou remoção adicional de resíduo.

## 5. Limites de segurança e de prova

O overlay é isolamento de autoria, não uma sandbox contra ferramentas canônicas comprometidas. O modelo de confiança é código de manutenção confiável, checkout exclusivo, dados sintéticos e nenhuma mutação concorrente do original. Não se promete transação global ou ausência de alterações temporárias feitas e revertidas por outro processo entre snapshots.

`writes_performed_in_original=false` descreve o que esta ferramenta faz; a preservação observada tem check separado antes/depois. Evidência e overlay são efeitos externos autorizados e permanecem retidos; não são confundidos com escrita no produto.

SHA e `record_id` detectam inconsistência, mas não são assinatura. Um agente que controla todo o bundle pode recalcular hashes. `verify_record` não reverifica execução: o auditor precisa dos logs reais e de uma identidade de código conferida independentemente. Alteração simples de conteúdo, run, base, comandos, checks ou claims é testada adversarialmente.

## 6. Cobertura candidata e bloqueios

Há rotas candidatas para `create` de snippet, script, prompt, notebook e README agregador. A aprovação é **estrutural local**, não correção analítica, qualidade editorial, execução do exemplo, registro no catálogo, autorização de aplicação ou homologação Genie.

README de objeto entra como parte obrigatória dos pacotes snippet/script/prompt. A criação avulsa de README escala Objeto fica explicitamente bloqueada em A1, até existir um envelope próprio para o objeto hospedeiro.

`convert` fica bloqueado antes de qualquer processo: não há move/refactor implícito. Criar skill também fica bloqueado: o catálogo atual exige as quatorze skills esperadas; A1 não fabrica uma décima quinta policy nem contorna esse gate.

## 7. Próximos gates, sem transferência de arquitetura ao Cloud

A1-LAB: executar sete integrações discriminantes e as regressões da base, em host identificado. O agente externo pode apenas instalar dependências declaradas, aplicar a entrada de changelog preparada e atualizar as linhas do snapshot a partir do validator real; depois congela SHA e executa a campanha uma vez.

Após o retorno: decidir aqui o envelope final, ligação do artefato ao fluxo da skill, manifest e contrato pertinentes e o tratamento prospectivo SEF/SER. Só com prova suficiente e autorização humana será proposta/realizada a mudança de policy. Ausência de evidência Windows ou Free fica explícita, sem transpor PASS Linux para outro host.

## 8. A2 — ligação à skill publicada por Receipt de domínio

A A1 provou a primitive repo-side. A A2 não move essa primitive para o Databricks:
`tools/` continua fora do produto publicado. Em vez disso, cria uma fronteira de
prova explícita.

- produtor: `tools/skill_enforcement/ser01_object_validation.py::validate_package`;
- Receipt: `SER01-OBJECT-VALIDATION-RECEIPT-1`;
- verifier publicado: `skills/hub-ml-criar-objeto/scripts/object_validation.py::verify_receipt`;
- superfície: `object_validation`;
- operação positiva: `create`;
- tipos positivos: snippet, script, prompt, notebook e README agregador;
- efeito no original: nenhum;
- runtime de notebook/código candidato: `NOT_RUN`;
- apply/promoção: não autorizados pelo Receipt.

O record local `SER01-LOCAL-VALIDATION-1` continua evidência detalhada da execução
repo-side. O Receipt de domínio não o substitui: vincula seu digest, run, base,
`candidate_sha256`, destino e claims fechados. O verifier pode conferir integridade
e binding no pacote publicado, mas declara `execution_reverified=false` e
`human_authority_authenticated=false`. Hash não vira assinatura.

A ausência do checkout/tools é condição `NOT_AVAILABLE`, não autorização para
bypass. Sem Receipt válido, a skill não pode fazer ready claim L3 dessa superfície.
A rota antiga de writer README permanece separada e não é generalizada nesta A2.

## 9. A3 — certificação prospectiva SER e rota canônica mínima

O ADR-0022 exige identidade de certificação diferente da SE08. A3 materializa essa
fronteira em `tools/skill_enforcement/ser_certify.py`. O primeiro profile é
`ser01-object-validation-pre-promotion`; seu output usa `SER-CERT-1` e
`sercert1:sha256(body)` apenas como tamper evidence, não assinatura.

O certifier exige policy ainda em L2, target L3 e `object_validation` L3/receipt.
Ele valida SKILL, contrato e release manifest; executa a suíte SER01 com integrações
reais; inspeciona independentemente os sete `validation.json`; verifica os cinco
Receipts positivos contra seus records e exige ausência nos dois negativos.

O bypass mínimo agora é explícito: Receipt sem `local_record`, record PASS sem Receipt,
Receipt adulterado ou candidato/base/run divergente não podem produzir prova válida.
Isso não prova aderência conversacional do Genie; esse canal continua externo e deve
ser observado separadamente antes de qualquer promoção final.

O certifier também executa regressões repo/CI e chama `certify_local --profile se08`
somente como canal histórico separado. Um PASS prospectivo nunca muda ou renomeia a
semântica de SE08. A3 permanece pré-promoção e não edita policy.

## 10. A3-R2 — identidade temporal dos probes Git e auto-verificação

Os probes Git de entrada e saída são observações distintas, embora consultem os
mesmos campos. A certificação passa a nomeá-los por fase
(`git_before_*`/`git_after_*`), preservando unicidade e permitindo ao verifier
exigir explicitamente ambos os conjuntos. O produtor também executa
`verify_certification` sobre seu próprio summary antes de retornar sucesso; se o
verifier rejeitar o artefato, o status é convertido para FAIL e o summary é
re-selado. Isso impede a classe de falso verde observada na A3-R1.
