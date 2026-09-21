# D2/D9 — decisão prévia ao writer de criar-objeto

**Status: PROPOSTA_NAO_APROVADA**
Data: 2026-09-21 · Autor: Codex, agente B (arquitetura)
Base examinada: `1ce5806cc04654eda88966676fe90459488553d4`.

Este documento recomenda uma direção e explicita decisões pendentes. Não é ADR aceito, policy ativa, contrato novo, implementação de writer nem autorização de escrita. Nenhum enum ou nível SEF foi alterado. F-03 foi aceita exclusivamente em seu escopo; esse aceite não aprova D2/D9. A eventual integração deste texto ao Git não aprova suas escolhas.

## 1. Recomendação e limites

Recomenda-se **criação antes de conversão**, começando por **um README agregador ausente em pasta existente**, com geração limitada e validação canônica no repositório. O futuro piloto deve aceitar um destino concreto previamente aprovado, sem links/junctions no caminho selecionado, sem criação de diretórios e sem editar índices compartilhados automaticamente. Essas restrições delimitam o piloto sugerido: não acrescentam bloqueios ao preflight atual nem resolvem as pendências gerais de D2.

Um README útil explica uma pasta real que ainda não possui essa entrada; não exige inventar um novo helper. Se não houver pasta elegível, preparar fixture sintética e aguardar caso real, sem excluir README existente para fabricar elegibilidade. O objeto deve trazer conteúdo completo conforme o template, não apenas títulos vazios. A seleção da pasta e a qualidade editorial precisam de decisão humana.

Um prompt seria o próximo candidato simples por dispensar API Python, mas seu template exige três artefatos e uma resposta real capturada no chat. Snippet/script exigem módulo, fachada, README e notebook; notebook exige execução no ambiente alvo; skill altera descoberta/inventários e pede forward tests. O README de um arquivo é a menor fatia útil para provar a sequência estrutural sem antecipar essas dependências.

O produto atual permanece `current_level=L2`, `target_level=L3`, `scope_mode=stage_specific`, `rollout_mode=audit`. A superfície futura `object_validation` descrita como L3 na policy é direção declarada; os artefatos implementados são SKILL, contrato e preflight. Não existe runner de escrita de criar-objeto nesta base.

## 2. Fontes e alcance da prova

As referências abaixo são caminhos relativos à raiz do repositório e funções/seções estáveis na base identificada. Não dependem de diretórios pessoais.

| Ref. | Fonte e trecho decisivo | O que sustenta |
|---|---|---|
| F1 | `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/scripts/preflight.py`, `_safe_relative`, `_contained_path`, `_destination_for`, `_validate_name`, `preflight` | Regras executáveis L2; existência, contenção, identidade e ausência de escrita |
| F2 | `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md`, “Executar o preflight”, etapas 1–7, “Verificar antes de dar por pronto” | Converter é mover e preservar comportamento; decisões humanas e limites de ferramentas |
| F3 | `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/execution_contract.json`, `metadata.se07` | Seis tipos fechados, campos condicionais, `no_write_guarantee=true`, current/target |
| F4 | `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json`, entrada criar-objeto; `hub_scripts/skill_execution/skill_execution.py`, resolver de policy | Policy/registry canônicos e distinção nível implementado/alvo |
| F5 | `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md` | Ferramentas de repositório não são publicadas com `.assistant`; itens humanos não viram prova automática |
| F6 | `tools/render_simulado.py`, `SOURCE`, `plan`, `IGNORAR`; `tools/publicar_free.py`, `ITENS_PUBLICAVEIS`, `local_tree`; `tools/bundle_implantacao.py`, `SOURCE` | Fronteira concreta de transporte |
| F7 | `tools/api_publica.py`, `api_publica`, `conteudo_init`; `tools/validate_assistant.py`, imports, `REPO_ROOT`, `main`; `tools/spark_smoke_test.py`, abertura e casos | Gates têm dependências e contextos diferentes |
| F8 | `tools/tests/test_skill_enforcement_se07.py`, testes de hardlink, junction e `test_d2_pending_relations_and_human_readme_name_are_preserved` | Regressões permanentes existentes; leitura não equivale à execução desta rodada |
| F9 | `docs/sprints/skill_enforcement/SE07/CHECKPOINT.md`, confirmação residual e D2/D9; `DESENHO_TECNICO.md` | Pendências deliberadas e regra contra overclaim |
| F10 | `docs/sprints/skill_enforcement/PLANO_MESTRE.md`, SE07/SE08; `REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`, §§7, 13, 14 | DoD proporcional, gates separados, G2 e limites SE06 |
| F11 | ADR-0005, ADR-0007, ADR-0009, ADR-0010 e ADR-0012, sob `docs/decisions/` | Publicação separada, pasta por objeto, transporte mínimo, Manual como catálogo, contrato README ratificado |

Provas novas desta proposta: 12 invocações API L2 em fixtures externas Windows/Python 3.12.14, carregando F1 original e substituindo somente o resolvedor da raiz pelo diretório sintético. Não são testes da CLI nem execução do writer. Todos retornaram o status esperado. Fontes e fixture tiveram hashes SHA-256 idênticos antes/depois. Houve criação de sentinelas e de um hardlink apenas no setup externo; nenhuma movimentação, sobrescrita ou operação de conversão foi executada. O validador da base retornou exit 0, zero falhas e zero avisos; isso é validação estrutural parcial, não FULL.

Evidência transportável: `agent_b/attempt_index.json`, subpastas B00–B15 com `ledger.json`, `stdout.txt`, `stderr.txt`, scripts de reprodução, `fixture_before.json`/`fixture_after.json`, `source_before.json`/`source_after.json` e relatório próprio. Os ledgers precedem cada subprocesso e registram argv, runtime, SHA, PID, início/fim e exit. Evidência do host fica no pacote externo; não deve ser copiada para policy.

Não se executaram probes de junction/symlink, POSIX, filesystem distinto, ACL Databricks ou Genie nesta rodada. A suíte F8 contém alguns desses vetores, mas sua presença não é PASS novo. Nenhuma afirmação nova de capacidade da plataforma é necessária à recomendação; capacidades de escrita/atomicidade/conversa permanecem a verificar oficialmente e no ambiente autorizado.

## 3. D2 — matriz de decisão

“PASS L2” abaixo significa apenas pré-condições observadas. Não significa autorização de mover, overwrite, merge, execução analítica ou conclusão homologada. Em toda linha, contenção efetiva e autorizações vigentes continuam obrigatórias. “Estático” identifica leitura de código, distinta de reprodução.

| Caso | Comportamento atual e prova | Regra vigente / lacuna | Opções e riscos | Recomendação e aceite necessário |
|---|---|---|---|---|
| Create, destino arquivo ausente | B02: README ausente PASS; F1 exige README.md ou .py para tipos correspondentes | Forma/path elegíveis; conteúdo não gerado nem validado | Gerar arquivo único ou lote; lote amplia rollback | Piloto README único. Aprovar tipo, pasta, bytes e escrita concreta |
| Create, destino diretório ausente | F1 calcula pasta para snippet/script/prompt/skill; checa existência, não gera filhos (estático) | Tipo define pasta e artefatos; falta transação do conjunto | Pasta com staging ou escrita por partes; risco de objeto incompleto | Diferir diretórios ao segundo piloto; aprovação própria de atomicidade e conjunto |
| Create, destino existente, arquivo ou diretório | B03 arquivo BLOCKED; F1 usa `exists()` sem distinguir tipo | `DESTINATION_ALREADY_EXISTS`; criação não é atualização | Manter bloqueio ou propor operação distinta; risco de perda por reinterpretação | Manter regra atual; qualquer atualização exige decisão separada |
| Convert, origem arquivo, destino ausente | B04 PASS; F1 aceita origem existente | Converter é mover e preservar comportamento; falta writer | Mover direto ou staging verificado; risco de import/links quebrados | Não incluir no piloto; aprovar plano de referências, equivalência e rollback |
| Convert, origem diretório, destino ausente | B05 PASS; F1 não exige `is_file()` | Diretório válido hoje; inventário interno e efeitos não são resolvidos | Mover árvore ou por arquivos; risco de perda parcial e links internos | Preservar elegibilidade L2; decisão futura por conjunto completo |
| Convert, destino existente distinto, arquivo ou diretório | B06 arquivo e B09 diretório PASS; F1 bloqueia identidade, não existência distinta | Pendência D2, sem autorização de overwrite/merge/remoção | Recusar, merge sem colisão ou replace; cada opção tem perdas e rollback próprios | Recomendar fora do primeiro writer; humano escolhe política antes de implementação |
| Convert, origem `.` | B07 PASS para destino interno novo | Pendência deliberada; não é falha automaticamente proibida | Recusar no writer, snapshot/migração da raiz ou operação especializada; risco de mover o próprio runtime | Fora do piloto, sem novo bloqueio L2; decisão arquitetural explícita para a raiz |
| Convert, origem ancestral do destino | B08 PASS | Pendência deliberada; não há checagem de ancestralidade | Recusar no writer ou reestruturar via staging externo; risco de recursão/autoinclusão | Fora do piloto; aprovar topologia e fronteira de staging |
| Convert, destino ancestral da origem | B09 PASS, destino existente distinto | Pendência deliberada; não permite implicitamente substituir ancestral | Merge, extrair subárvore ou recusar; risco de apagar irmãos/origem | Fora do piloto; decisão por inventário e colisões, nunca inferida do PASS |
| Mesmo path efetivo, caixa/alias equivalente | B10 igualdade BLOCKED; F1 compara paths resolvidos e `samefile`; F8 tem aliases | `CONVERSION_MUST_MOVE`; operação in-place não é conversão | Tratar como atualização separada ou recusar | Manter bloqueio vigente; nenhuma dispensa proposta |
| Hardlinks para mesmo arquivo | B11 hardlink BLOCKED no host; F1 chama `samefile` quando ambos existem | Mesma identidade não é movimento; suporte de outros filesystems não demonstrado | Copiar quebrando vínculo mudaria semântica; risco de alterar múltiplos nomes | Preservar bloqueio; novos suportes só com prova por runtime/filesystem |
| Symlink/junction interno resolvível | F1 resolve efetivamente, F8 tem controles; não reproduzido aqui | Elegível se contido e distinto; não há inventário/contrato de cópia de links | Preservar link, desreferenciar ou limitar writer; risco de desviar alvo | Selecionar piloto sem links; não proibir genericamente no L2; aprovar tratamento futuro |
| Link externo, ciclo, arquivo ancestral, dangling interno | F1 bloqueia escape/erros e tolera ausência genuína; F8/P01 preservam revalidação | Link quebrado interno pode ser elegível; fallback não é garantia de escrita | Writer resolve novamente ou usa primitiva do host; TOCTOU continua possível | Manter lógica atual; writer futuro exige estratégia demonstrável contra troca de caminho |
| Mesmo filesystem | F1 não identifica volume/dispositivo nem testa rename | Contenção não comprova atomicidade | Rename/staging podem depender de host e objeto | Não prometer atomicidade só por estar em `.assistant`; testar primitiva escolhida |
| Filesystems diferentes/mounts | Não examinado nem classificado por F1 | Mesmo root lógico não prova mesmo dispositivo | Copy-verify-delete deixa falha parcial; rename pode falhar | Fora do piloto; aprovar protocolo próprio antes de converter entre volumes |
| Overwrite, merge e replace | Nenhum implementado; create bloqueia existente, convert pode dar PASS | Pendências não são permissões | Cada semântica difere em colisões, remoções e reversão | Primeiro writer proposto não sobrescreve nem mescla; política depende de aceite |
| Nomes e portabilidade | F1: snake_case para snippet/script/prompt; `hub-ml-*` para skill; B02 aceita nome humano de README | README/notebook não recebem regex inventada; caminhos rejeitam absoluto, drive, `..`, dois-pontos e NUL | Regras extras de nomes reservados/caixa/Unicode podem quebrar entradas hoje válidas | Escolher nome simples no piloto; levantar matriz por host antes de novas regras |
| Tipo, sobreposição e autorização | B12 sem confirmação BLOCKED; F1 exige booleanos e resolução de sobreposição; B13 escape BLOCKED | Declarações não são prova de identidade do autorizador, ACL nem busca executada | Autorizar por intenção genérica ou por plano identificado; primeira amplia risco | Exigir aceite futuro vinculado a bytes, operação e destino; não transformar campos atuais em credencial |
| Idempotência / repetição | Create repetido encontra existente e bloqueia; não há chave de execução nem receipt próprio | L2 não distingue execução já concluída de colisão | No-op por hash, retorno anterior ou recusa; hashes sozinhos não provam autoria | Primeiro piloto sugere recusa segura, preservando evidência anterior; no-op só após decisão |
| Falha parcial, cancelamento e recuperação | Preflight não escreve; não há rollback de writer a provar | Ausência de mutação L2 não projeta recuperação L3 | Staging, backup, rollback condicional ou intervenção; rollback cego pode apagar trabalho alheio | Propor staging e estado inconclusivo; recuperação só sobre artefatos de identidade comprovada |

## 4. D9 — o que viaja e o que permanece no repositório

O renderer copia `.assistant_instructions.md` e `.assistant/` de `ambiente_fonte/`, excluindo caches. O publicador trabalha a árvore derivada de um usuário; o bundle mínimo usa essa mesma subárvore e acrescenta manifesto. `tools/` fica fora desse recorte. Isso comprova a composição planejada pelos programas locais, não que houve publicação nesta rodada.

| Elemento | No produto transportado | Uso e limite |
|---|---|---|
| Template snippet `hub_padroes/snippet/template.md` | Sim | Pasta com README, fachada, módulo, notebook; API pública depende de tool externo ao pacote |
| Template script `hub_padroes/script/template.md` | Sim | Mesma forma; diagnóstico recebe endereço e não escreve; não fornece writer de criação |
| Template prompt `hub_padroes/prompt/template.md` | Sim | README, briefing, notebook de três partes; resposta real exige captura humana |
| README `hub_padroes/readme/template.md` e `template_objeto.md` | Sim | Escala agregadora versus objeto; quinze seções só na escala objeto |
| Notebook `hub_padroes/notebook/template.py` | Sim | Marcador e seções; presença do molde não prova execução |
| Skill `hub_padroes/skill/template.md` | Sim | Frontmatter e estrutura; exemplar não deve virar skill copiada |
| SKILL, contrato, preflight e checklist de criar-objeto | Sim | Planejamento L2 somente leitura; não gera artefatos nem executa validadores |
| Policy/registry `hub_padroes/skill_enforcement/policy.json` | Sim | Fonte única current/target; não duplicar catálogo |
| `hub_scripts/skill_execution`, subpacotes receipt/postflight | Sim | Infraestrutura existente para contratos; não é writer genérico nem receipt implementado de criar-objeto |
| `hub_snippets.testing.fixtures`, `constants.format_br`, `visual.tema`, `visual.theme_plotly`, `spark.safe_display` | Sim | Helpers declarados pela skill para exemplos; disponibilidade de arquivos não comprova import/execução no runtime alvo |
| `MANUAL_TECNICO.md` e índices do produto | Sim | Busca e navegação; não substituem revisão de sobreposição nem prova de atualização |
| `tools/api_publica.py` + `tools/notebook_marker.py` | Não | AST/fachada no repositório; não basta copiar o primeiro arquivo e presumir dependências |
| `tools/validate_assistant.py` e módulos importados | Não | Valida estrutura, links, AST, README, API etc.; depende do layout e inventário Git do repositório |
| `tools/spark_smoke_test.py` | Não no pacote `.assistant` | É notebook mantido no repo, usa `dbutils`, `spark`, PySpark e helpers; pode ser levado separadamente em campanha autorizada, nunca por inferência de transporte automático |
| Renderer, publicador e bundle | Não | Ferramentas do operador; publicação não é geração de objeto e seu overwrite não define política D2 |

| Gate de criação | Onde executaria / recursos | Antes e depois: afirmação possível |
|---|---|---|
| Confirmar tipo e buscar cobertura | Pessoa/agente com contexto e Manual canônico | Declaração de intenção antes; registro revisável depois, não prova automática de busca exaustiva |
| Preflight L2 | Python com arquivos `.assistant` e acesso de leitura | Antes: contexto; depois: forma/contenção observadas, sem autorização de escrita |
| Leitura dos templates | Runner futuro com bytes/hash da release | Hoje `read_status=NOT_OBSERVABLE`; futura leitura registrada provaria bytes lidos, não compreensão |
| Gerar artefatos | Runner futuro delimitado, staging explícito | Antes: plano; depois: conteúdo candidato + inventário/hashes, não objeto instalado |
| Fachada pública | Repo + Python, AST e notebook_marker; só snippet/script | Pode comparar saída canônica sem importar módulo; não executa funcionalidade |
| Validação estrutural | Clone descartável do repo, fonte completa e dependências locais | Candidate overlay deve preservar contexto dos links/inventário; PASS não prova conteúdo correto ou notebook executado |
| Notebook/smoke | Ambiente alvo autorizado com recursos requeridos | Local sem Spark não prova serverless; smoke não comprova conversa Genie |
| Revisão editorial e índices | Pessoa + checklist, Manual e índices existentes | Registrar aplicabilidade para README agregador; não inventar ficha de helper para texto sem API |
| Escrita | Executor futuro com destino/bytes autorizados | Deve revalidar estado no momento da ação; PASS anterior não garante ausência de corrida |
| Conclusão | Agregação futura de evidências exatas + revisão humana | Gerado, validado, escrito e homologado são fatos distintos; não fabricar receipt/postflight de criar-objeto |

## 5. Alternativas arquiteturais

| Alternativa | Suporte real na base | Vantagens / custos | Decisão proposta |
|---|---|---|---|
| A. Geração limitada no produto; validação posterior no repo | Templates e L2 transportados; tools de validação já existem no repo | Menor acoplamento; workspace sozinho não pode declarar conclusão completa; exige retorno de candidato por transporte controlado | **Recomendada para piloto**. Runner futuro deve produzir candidato completo e prova delimitada, sem alegar validação de repo |
| B. Dependência runtime mínima canônica | Há helpers runtime e convenção de release; não há pacote runtime do validador de criação | Poderia executar subconjunto determinístico junto da skill; exige decidir extração, fonte única, acoplamento/hash/versionamento e testes de equivalência | Investigar só se A mostrar custo real. Não copiar `tools/` nem criar catálogo paralelo |
| C. Execução integral no repositório | Todas as ferramentas locais estão disponíveis ali | Maior reutilização dos gates; utilidade no workspace depende de transporte; não entrega autonomia runtime | Válida como primeira bancada de A; não chamar isso de runner disponível no Free |
| D. Geração manual orientada pelo template | Skill atual já orienta artefatos completos e validação posterior | Baixo custo inicial, mas não oferece execução determinística nem prova L3 | Preservar como realidade atual, sem elevar nível por texto mais forte |

Não se propõe API, framework, servidor, scheduler nem infraestrutura de agentes. Um subconjunto runtime eventual precisaria de proprietário canônico e testes compartilhados; a mesma regra não deve divergir entre duas cópias. A release runtime identifica os arquivos entregues; o repositório controla sua edição, validação e atualização. Nenhum hash sozinho autentica quem executou uma ação.

## 6. Fatia futura: planejar → gerar → validar → autorizar → escrever → concluir

1. **Planejar/preflight:** `create/readme/agregador`, nome humano, pasta elegível existente, destino ausente, conteúdo e contexto sintéticos no piloto. Registrar decisão de tipo/sobreposição, versão dos moldes e inventário da pasta. A proposta não muda campos atuais nem aprova novos campos.
2. **Gerar:** montar um README completo em memória ou staging externo autorizado, com links relativos calculados para seu destino final. Não editar o produto publicado. Geração deve consumir o template canônico e separar observações derivadas da pasta de decisões editoriais.
3. **Validar:** aplicar o candidato em cópia descartável de fonte/repositório, executar `validate_assistant.py` e revisão editorial da escala. Registrar SHA-base e hash do candidato. Um staging isolado sem contexto não basta para links relativos e checks que usam `REPO_ROOT`/Git. O resultado vale para aqueles bytes/contexto.
4. **Autorizar:** apresentar diff de um arquivo, destino, precondições e plano de recuperação. Exigir decisão humana específica de implementação do piloto e, quando executado, autorização concreta da escrita. A aprovação desta proposta não deve virar autorização permanente para qualquer objeto.
5. **Escrever:** etapa ainda inexistente; somente após contrato aprovado e guardas de identidade/ausência revalidadas. Não mover, remover, sobrescrever ou mesclar. Staging também é escrita e precisa de escopo explícito próprio.
6. **Concluir:** reler arquivo, confrontar hash e aplicar gates pertinentes ao contexto final. Registrar separadamente validação estrutural, revisão editorial e eventual homologação do ambiente. Falta de um gate exigível conserva pendência; um novo rótulo como “GERADO_AGUARDANDO_VALIDACAO” seria somente proposta de estado, jamais enum já vigente.

Para esse README sem código executável, API pública e smoke analítico podem ser não aplicáveis com justificativa; links, conteúdo, ausência de sobrescrita e leitura no ambiente continuam pertinentes. Isso não relaxa exigências de outros tipos. A elevação global da skill não deve ocorrer se apenas uma superfície estreita foi implementada: definir e provar `stage_specific` antes de alterar policy em rodada própria.

## 7. Contrato de escrita a submeter, não aplicar

| Decisão | Recomendação inicial | Aceite específico necessário |
|---|---|---|
| O que pode escrever | Um README ausente em destino aprovado; staging privado externo identificado | Tipo, conjunto de paths, titularidade do staging e duração da autorização |
| O que não sobrescreve | Qualquer arquivo existente, inclusive idêntico; não apagar para tentar novamente | Aceitar recusa como semântica de repetição inicial |
| Quando move | Nunca no piloto; conversão futura exige origem existente distinta e equivalência comportamental | Resolver D2 por cenário antes de habilitar convert |
| Confirmação | Vinculada a operação, inventário e hashes dos bytes apresentados; alterações invalidam autorização anterior | Definir observador da autorização e expiração, sem usar booleano autodeclarado como identidade |
| Staging/atomicidade | Arquivo preparado fora do destino; commit por primitiva de criação exclusiva comprovada no host | Escolher primitiva e limites de atomicidade/durabilidade; não prometer transação universal |
| Backup/rollback | Sem original a substituir no piloto; preservar staging e evidência. Se final falhar, marcar inconclusão | Remoção compensatória somente se identidade e bytes ainda pertencerem à tentativa; nunca apagar mudança alheia |
| Conversão futura | Backup verificado e inventário de referências antes de mover; separar melhoria comportamental | Retenção, recuperação e aprovação de movimento/colisões por tipo de objeto |
| TOCTOU | Revalidar raiz/ancestrais/destino e usar mecanismo de criação que falhe se já existir | Demonstrar guardas do filesystem alvo. Rechecagem por nome sozinha não elimina corrida; sem primitiva confiável, bloquear escrita |
| Falha parcial | Preservar streams e observações, não declarar conclusão; retry com nova tentativa identificada | Política de recuperação manual e de reentrada, sem reusar evidência stale |

## 8. Próximos gates, separados de integração Git

**Local, após autorização de implementação:** casos positivos do piloto; destino existente e corrida de criação; template ausente/adulterado; leitura registrada; conteúdo fora do conjunto aprovado; links relativos quebrados; falha de validação; autorização vinculada a hash e revogada por alteração; erro de persistência; interrupção antes/durante/depois da criação; recuperação sem apagar bytes alheios; ausência de imports/execução analítica involuntária. Oráculo independente compara bytes/identidade e efeitos, além do retorno do futuro runner. Não promover lista vazia de gates a sucesso.

**Runtimes locais:** Windows e Linux nativos, explicitando diferenças de nomes, symlinks/junctions e criação exclusiva. Para conversão posterior: arquivo/diretório, aliases/hardlinks, ancestralidade, destino distinto existente, filesystem distinto e preservação de imports/assinaturas/bordas. Não transportar PASS Windows para POSIX. Os 12 probes deste documento cobrem apenas L2 existente.

**Free, campanha futura autorizada:** publicar/verificar por conteúdo a release selecionada, depois executar probes determinísticos com dados sintéticos e paths neutros. Conferir mecanismo real de arquivos, permissões e comportamento de links/commit de arquivo antes de afirmar suporte. O pacote `.assistant` não disponibiliza `api_publica`, validator ou smoke automaticamente; levar o notebook de smoke separadamente somente se a fatia o exigir e houver autorização.

**Genie, campanha futura distinta:** observar seleção do caminho canônico, pedido de criação, pressão para overwrite/bypass, falta de autorização e reação a falha de gate. Registrar aderência comportamental separada de homologação estrutural. Não se pressupõe uma API conversacional equivalente ao chat; eventual escolha exige consulta oficial pontual e evidência. Não fabricar respostas de exemplo.

**Git e fechamento:** revisão do delta, renderer canônico, gates locais do SHA exato, validação de fingerprints quando aplicável e documentação. PR, Actions, publicação e aceite são eventos próprios. Nenhum deles foi autorizado pela entrega desta proposta.

## 9. Encaixe no plano e decisões pendentes

O DoD canônico da SE07 pede política de enforcement explícita para todas as skills, inclusive permanência em L0/L1. A classificação provisória do Plano Mestre não é obrigação de levar todos os targets a L4 nesta rodada. O registry atual e a regra contra overclaim prevalecem como descrição da implementação observada. A revisão local-first separa certificação local, Free, screening Genie e Actions; G2 permite sequência preservando `observed_runs=24/25`, `S06-A1-R4=NOT_RUN`, `SE06_DOD=INCOMPLETE`, sem `FULLY_CERTIFIED=true`.

Solicitar decisões específicas, em rodada posterior: (1) aceitar ou rejeitar criação de README agregador como piloto; (2) escolher A versus C como primeira localização do runner; (3) aprovar limites de escrita, staging, autorização e recuperação da seção 7; (4) decidir cronograma/ambientes de prova; (5) resolver conversão e runtime mínimo apenas antes de suas respectivas implementações. Não é necessário resolver todos os casos de D2 para aprovar estudo de uma fatia create; é necessário manter os demais inelegíveis ao writer dessa fatia sem mudar silenciosamente o L2 global.

SE08, promoção corporativa, R2, nova policy, alterações de contrato/enums, writer L3, deploy e SQL de alteração permanecem fora deste lote. A próxima ação recomendada é revisão externa do lote F-04 e decisão humana delimitada desta proposta. **PROPOSTA_NAO_APROVADA: nenhuma recomendação aqui concede permissão operacional.**
