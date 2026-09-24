# 04 — CI local, cobertura herdada e oráculos

## 4.1 Objetivo: não perder cobertura ao trocar de mecanismo

A baseline tem `tools/ci_local.py` com dez etapas e `tools/skill_enforcement/certify_local.py` com perfil SE08 cumulativo. O certifier pós-promoção SER01 seleciona nove etapas não-SEF e suites específicas. Esses conjuntos não são equivalentes apenas porque ambos terminam em PASS.

`catalogos/COBERTURA_BASE.json` lista os entrypoints encontrados e seu destino proposto. O inventário é de suites, não uma contagem de métodos executados. B0 precisa expandi-lo a `test_id` na versão congelada e classificar cada assertion relevante antes de liberar certificação de produção. `METHOD_MAP_PENDING` bloqueia o gate de equivalência, não autoriza omissão.

## 4.2 Três camadas de CI

**CI-A — Autoria/diagnóstico:** syntax, schemas, signatures, fixture validity, imports, coleção, integridade de manifests, fases e oráculos. Objetivo: detectar defeitos baratos antes da campanha. Pode ser executada repetidamente na autoria com mudanças e histórico; a rodada local de diagnóstico não corrige código.

**CI-C — Componente/skill:** preflight, runner, Receipt, Postflight, efeitos autorizados, positivos, negativos, mutantes e dependências daquela skill. Opera em clone isolado e permite execução paralela de componentes independentes. Uma validação local não substitui runtime Free/Spark/MLflow.

**CI-I — Integração:** candidato composto, vetor de policy, regressão de todas as skills existentes, contratos entre produtoras/consumidoras, publicação, renderer, snapshot e prova de árvore. Não reutiliza um certificado de SHA antigo como se fosse deste SHA.

Dentro de uma mesma CI-I congelada, invariantes comuns podem executar uma vez. Dois componentes em SHAs diferentes não compartilham um PASS global só porque o nome do teste é igual. Reuso máximo permitido: evidência de componente identificada por seus digests, conservando a origem; o certificado integrado lista o que executou de novo e o que consultou como suporte.

## 4.3 Destino das suites da baseline

| Família observada | Tratamento no novo mecanismo |
|---|---|
| validate_contracts, se07_policy | Obrigatórios no root explícito da candidata, antes e após policy |
| SE01/SE02/SE03 | Invariantes estruturais/preflight, preservados após mapear assertions temporais |
| SE04 Receipt + runner | Obrigatórios; não substituir por teste do envelope de campanha |
| SE05 Postflight + runner | Obrigatórios; finalização fail-closed permanece distinta de geração |
| SE06 avaliação | Obrigatória; não perder taxonomia de correctness/adherence/compliance |
| SE07 policy tests | Mistos: invariantes vigentes + assertions de vetor histórico, separar explicitamente |
| SE08 policy-I/O | Obrigatória no host pertinente |
| SE08 operacionais | Mistos: operação vigente + assertions temporais de nível/cardinalidade/comandos |
| Storage cleanup / Windows corrective / cleanup diagnostics | Obrigatórios no Windows/NTFS quando reclamado; NA técnico apenas com razão e não promoção daquele host |
| test_certify_local | Regressão do supervisor herdado, sem fingir cobrir o novo executor inteiro |
| validate_assistant / renderer / render_diff / snapshot | Obrigatórios no composto, com root/saídas controlados |
| CI não-SEF | Temas, biblioteca, guardas, transição, READMEs, Concierge: preservar todas as nove etapas |
| SER01 producer/Receipt/writer | Regressão da skill integrada; não repromover SER01 |
| Metatestes novos do mecanismo | Obrigatórios; cobertura de scheduler, evidência e autorização não existe por herança automática |
| Tests de helpers consumidos | Localizar, ler assertions, classificar e executar no perfil de cada domínio |

As suítes históricas podem continuar vermelhas quando testam explicitamente o estado antigo. Isso não permite que o gate novo ignore seus invariantes de segurança ou faça apenas leitura textual. O novo perfil terá testes sucessores que verificam o vetor aprovado, além da prova de preservação do histórico.

## 4.4 Assertions temporais: migração sem máscara

Procedimento para cada assertion histórica: identificar arquivo e ID completo; registrar SHA em que era válida; enunciar a propriedade histórica; identificar a propriedade atual a preservar; criar um teste sucessor contra fixture/projeção de policy aprovada; comprovar que o sucessor reprova um mutante relevante; conservar o resultado antigo sem reclassificar.

Não editar um teste atual para ler `current_level` da policy e comparar com ele mesmo. O esperado vem do manifesto aprovado, independente do candidato. Não usar `L2 ou L3` como atalho quando apenas uma transição foi aprovada.

Um adapter temporário `EXPECTED_TEMPORAL_FAIL` exige identidade completa, razão da assertion, contagem coletada/executada, saída completa e zero ERROR inesperado. Reprova se o mesmo nome falhar por exceção diferente, se faltar um teste, se aparecer expectedFailure novo, se a coleta for menor ou se logs forem truncados. Regex de nome de método não é suficiente.

O adapter é transitório. O objetivo é que a CI prospectiva própria seja o entrypoint vigente, sem obrigar futuras promoções a ampliar interminavelmente listas de FAILs tolerados.

## 4.5 Oráculos independentes

Para cada método de domínio, definir fixture, resultado esperado, justificativa e tolerância antes de rodar o candidato. Não chamar a mesma função do helper para calcular o resultado esperado. Admitir fórmula manual para fixture mínima, implementação de referência deliberadamente independente ou propriedade matemática suficiente para aquele caso, com limites descritos.

Para aproximações numéricas, congelar `atol/rtol`, método, seed, tamanho de amostra e versão. Não elevar tolerância depois do FAIL. Variabilidade legítima exige um protocolo estatístico pré-declarado, não “aceitar porque parece perto”.

Verificação de side effect usa estado real antes/depois e leitura do destino, não apenas `writes_performed=false` gravado pelo próprio executável. Ainda assim, ausência de mudança no fingerprint só prova os paths efetivamente cobertos; não é sandbox de segurança.

## 4.6 Seeds, host e dependências

Lock/fingerprint de Python, bibliotecas analíticas, Node/pnpm quando necessários ao sistema de temas e runtime Spark/MLflow. Não atualizar lock nem baixar pacote no meio da certificação. Uma dependência opcional ausente pode impedir somente o perfil afetado; não produzir verde para a capacidade não executada.

No Windows, paths curtos, separadores e encoding definidos. CRLF de stdout de ferramenta pode ter normalização específica e registrada; bytes candidatos/artefatos não são tratados com `strip` genérico. Os hashes RAW e normalizados têm campos separados.

Python no Linux não prova junction/handle semantics de NTFS. Mock de Spark não prova execução Spark. MLflow local não prova registro num workspace remoto. Essas dimensões aparecem na matriz de cobertura da skill.

## 4.7 Coleta, parametrização e estabilidade

O manifesto aprovado traz os IDs conceituais e o binding para métodos reais. Na qualificação, `inventory` registra a coleta completa, parâmetros e testes condicionais. No freeze, o fingerprint da coleta é ligado à candidata e ao ambiente. Na execução, started/finished devem corresponder a essa lista.

Mudança de collection por plugin, variável de ambiente, versão ou arquivo novo é discrepância, não ganho automático de cobertura. Adicionar testes é permitido na autoria; exige revisão do manifesto antes da nova campanha. A contagem divulgada deve distinguir métodos coletados, invocações parametrizadas, testes que passaram, skips autorizados e casos não iniciados.

## 4.8 Mutação e testes adversariais

Aplicar mutantes somente em clones/fixtures descartáveis destinados à mutação. Exemplos: remover chamada canônica, trocar dataset/hash, omitir finalizer, aceitar autorização booleana, apagar gate do manifesto, forjar step final, confundir sample e população. O mutante precisa provocar a reprovação pelo oráculo pertinente.

Nem todo mutante representa código que será integrado. Não contam como prova de resistência a defeito testes que passam porque uma etapa anterior genérica falhou. Exigir que o negativo alcance a fronteira específica e registre o discriminante. O positivo correspondente precisa passar no mesmo ambiente.

## 4.9 Definição de prontidão de cobertura

B0 só passa se todas as suites da baseline estiverem mapeadas; nenhum método invariante relevante estiver sem destino; os adaptadores históricos tiverem sucessores discriminantes; as seis skills já integradas tiverem regressão proporcional; as lacunas de helper estiverem explícitas por skill; e os testes do próprio mecanismo detectarem omissão/duplicação/forja.

Não declarar equivalência por soma de testes. A prova é a matriz e seus bindings executados. Uma expansão de catálogo por MM04 exige revisão explícita do mapa antes de certificar o composto.
