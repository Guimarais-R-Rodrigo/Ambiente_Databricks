# 06 — Auditoria independente e contrato de evidência

## 6.1 Duas perspectivas, não dois votos

O auditor de domínio verifica o significado do resultado e a suficiência do oráculo. O auditor de evidência/enforcement verifica se a conclusão está sustentada por execução, integridade, cobertura e autoridade. Ambos precisam de contextos distintos do executor. Modelo diferente é desejável quando acrescenta diversidade; não é requisito suficiente para independência.

O executor não edita o relatório de auditoria. O auditor não edita o código nem reclassifica o esperado para concordar com o resultado. O coordenador não resolve conflito contando PASSs. O autor responde com análise causal e mudança proposta; decisões de escopo/risco material vão ao usuário.

## 6.2 Pacote mínimo para cada auditor

Receber release spec, candidato/hash/tree, contrato da skill, matriz de escopo, mapa caso→test_id, fixture/oráculo, outputs e processo/effect ledgers. O relato do executor fica separado. Quando viável, auditor escreve a primeira lista de achados antes de ler o veredito do executor.

Contexto mínimo suficiente deve ser independente de uma conversa longa: toda referência usada precisa estar no repositório ou no bundle identificado. Nunca instruir auditor a “validar que está bom”. A pergunta é se a evidência suporta a claim, incluindo hipóteses adversariais pré-definidas.

## 6.3 Escala de evidência observável

| Nível | O que existe | O que não prova |
|---|---|---|
| DECLARED | Texto afirma que selecionou/usou/calculou | Carregamento, chamada ou conclusão reais |
| LOCATED | Caminho/símbolo foi localizado | Leitura, import ou execução |
| READ_OBSERVED | Evento de leitura/skill carregada visível | Chamada do helper ou sucesso |
| CALL_OBSERVED | Evento/trace da chamada com argumentos vinculados | Output completo ou correção |
| OUTPUT_OBSERVED | Saída persistida com identidade e processo concluído | Correção numérica/autoridade, sozinha |
| VERIFIED | Verificador/oráculo independente confrontou entradas/saídas | Autenticação humana universal, governança ou publicação |
| NOT_OBSERVABLE | Canal não permite observar o evento necessário | Não equivale a ausência de evento nem a PASS |

No teste negativo de roteamento, não ver o nome no texto final é insuficiente para provar que uma skill não foi carregada. Uma UI/trace completa ou outro mecanismo de observação precisa sustentar essa afirmação. Sem isso, a conclusão é limitada ao comportamento observável e a claim de roteamento recebe NOT_OBSERVABLE. Não coletar raciocínio privado como substituto de evento de ferramenta.

## 6.4 Perguntas do auditor de domínio

A unidade estatística é a declarada? Denominador/população e amostra efetiva correspondem ao cálculo? A fixture consegue detectar o defeito pretendido? O helper é semanticamente adequado, ou apenas possui nome parecido? O resultado foi confrontado com um oráculo independente? NaN legítimo é preservado? A tolerância estava aprovada? Temporalidade/PIT/fit/train-only foram observados? Dependência ausente foi tratada como bloqueio? Dry-run, recomendação e simulação estão corretamente rotulados? A conclusão extrapola causalidade, performance, fairness ou efeito executado?

A auditoria deve mostrar pelo menos um negativo discriminante importante e seu positivo correspondente para cada superfície promovida. Não é necessário reinspecionar todos os bytes manualmente quando o verificador íntegro comprova a cobertura, mas findings materiais exigem localização precisa.

## 6.5 Perguntas do auditor de evidência

O SHA executado é o candidato anunciado? Os manifestos existem e os hashes foram recalculados? Os testes obrigatórios foram coletados e finalizados? Há filtros/variáveis escondidos? Os logs estão completos? As etapas before/after têm IDs diferentes? Há erros adicionais num canal histórico? A execução terminou sem processos/resíduos não declarados? A claim de no-write cobre todos os destinos pertinentes? Houve edição ou reexecução não autorizada? O efeito foi observado independentemente do status do comando? O summary e seu verifier concordam? A evidência externa corresponde ao deployment correto? RAW e SHARE não foram confundidos?

Não aceitar `valid=true` de um verificador como prova de que ele cobre todas essas perguntas. O próprio verificador precisa de metatestes e escopo documentado.

## 6.6 Finding padronizado

Campos: finding_id, audit_id, campaign/round/candidate, severity, category, affected_scope, path/symbol/test_id, requirement_id, expected, observed, evidence_refs, reproduction, impact, suggested_minimal_resolution, status, author_response e closure_evidence.

Categorias mínimas: DOMAIN, CONTRACT, COVERAGE, AUTHORITY, EVIDENCE, ISOLATION, ENVIRONMENT, INTEGRATION, EDITORIAL. Severidade material não é diminuída porque “todos os outros testes passaram”.

- **F0:** quebra de autoridade, exposição de segredo, mistura de campanhas, adulteração ou mecanismo que pode certificar falso PASS. Bloqueio global ou do conjunto de consumidores afetados.
- **F1:** erro de cálculo, temporalidade, effect verification ou cobertura obrigatória ausente. Bloqueia a superfície e os dependentes.
- **F2:** limitação não crítica ou documentação ambígua que não altera resultado/autoridade, mas pode induzir uso incorreto. Resolver antes de compartilhar a capacidade afetada; adjudicar alcance, sem regra de dispensar automaticamente.
- **F3:** higiene editorial/empacotamento sem efeito na prova. Registrar sem forçar nova campanha numérica quando o código/escopo não mudam; verificação documental proporcional é suficiente.

Nova deficiência material descoberta durante auditoria é registrada e impede aceite. Não editar o teste congelado para avaliar retroativamente outra regra. Criar revisão de autoria e nova rodada pertinente, preservando a descoberta e a primeira evidência.

## 6.7 Contestação e encerramento

O autor pode contestar um finding com paths, contrato e reprodução. Auditor responde por evidência. Até duas rodadas de contraditório por finding antes de escalar a decisão de escopo ao usuário; isso é limite de conversação, não autorização para fechar finding inconclusivo como PASS. Não criar loops ilimitados de agentes.

Fechamento permitido: FIXED_VERIFIED; NOT_A_DEFECT_WITH_EVIDENCE; ACCEPTED_LIMITATION_BY_USER com limite explícito; ou OPEN/BLOCKED. Uma limitação que retira capacidade material reduz a claim, nunca se transforma em capacidade certificada por aceite retórico.

## 6.8 Estrutura probatória externa

```text
<evidence-root>/<campaign>/<round>/
  identity/       # Git, tool versions, role/permissions metadata
  manifests/      # candidate/test/fixture/dependency/profile hashes
  processes/      # started/finished, stdout/stderr, effects
  cases/          # inputs, outputs, expected, comparisons
  domain/         # Receipts/Postflights e dados sintéticos pertinentes
  audits/         # domínio, enforcement, contraditório
  external/       # publication/readback/probe/Genie literal
  summary/        # resultado, verificação própria e externa
```

Diretórios são exclusivos por rodada. Evidências grandes desnecessárias, `.git`, caches, homes, `.claude/context` e datasets reais não entram no SHARE. A auditoria de arquivo ZIP limita tamanho/expansão, proíbe traversal, links e membros duplicados antes de extrair. Nada do bundle é executado automaticamente.

## 6.9 RAW, SHARE e hashes

RAW é imutável e privado. SHARE é derivado sanitizado, com ID e manifesto próprios. `raw_bindings` pode conter hashes dos bytes RAW e referências não sensíveis; não prova por si só a execução. `transformation_manifest` registra arquivos transformados e política de sanitização, sem expor os valores secretos removidos.

Manifesto interno exclui a si próprio do conjunto hasheado e declara a exclusão. Hash externo do ZIP cobre o arquivo completo. Não criar ciclo em que manifesto precisa conter seu próprio hash final. O relatório de auditoria de um ZIP também não pode afirmar que audita a si mesmo dentro do ZIP; seu digest externo ou revisão sucessora resolve o vínculo.

O SHARE pode ter um resumo próprio de integridade para facilitar análise, mas nunca reutilizar o `certification_id` RAW como se fosse recalculável sobre bytes alterados. Preservar o output de verificação RAW com hash quando ele não exige sanitização; caso contrário, declarar também sua transformação. Sem RAW acessível, o auditor limita a conclusão ao que pode verificar no derivado, não inventa autenticidade.

## 6.10 Verificação independente do agregado

O verificador recebe manifestos aprovados de fora do payload candidato; confere schema e enums; resolve paths seguros; recalcula hashes; confronta documentos e outputs; compara case/test IDs, argumentos, ordem causal e tempo; exige provas dos effects e desautorização pertinente; e rederiva o veredito. Não basta verificar `status=PASS` nem confiar em expected_outcomes fornecidos pelo próprio summary.

Hashes e registros são tamper evidence, não assinatura de pessoa. Numa máquina controlada pelo operador, um agente com acesso irrestrito poderia forjar todos os dados; por isso permissões, isolamento, revisão e aceites observáveis continuam necessários. Não prometer segurança criptográfica que esta arquitetura não oferece.
