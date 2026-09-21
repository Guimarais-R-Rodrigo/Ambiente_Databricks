# Handoff — SE07, piloto L3 README agregador

Data: 2026-09-21 · De: Codex coordenador e auxiliares A/B/C · Para: supervisão externa.

## Identidade e estado

Base aceita: `d49c8728f0e47adc15f7f78293c9fcc58c809a15`, promovida exclusivamente
por fast-forward para `sef/SE07-generalizacao` antes da implementação. Main
`72894c5511abfa9a5ede3edb4a6f7c5fe11231b3` e review F-04 d49c8728 preservadas;
zero Actions runs observados para d49 após promoção. [Checkpoint](../sprints/skill_enforcement/SE07/CHECKPOINT.md).

Código dos auxiliares integrado em `c1e1a67e9af96519983cbf2f3d3e474f2e8bf4ef`. O commit que introduz este
handoff contém também a integração compartilhada, manifest e derivado e é o
SHA final documental a certificar. Seu SHA/tree são resolvidos no Git; não há
autorrefência literal impossível. Certificação externa posterior deve citar
exatamente esse SHA, HEAD/status antes/depois e exits externos.

Estado **NAO_PRONTA no congelamento para certificação**: gates do commit que
contém este documento são `NOT_RUN_AT_FREEZE`. Isso não antecipa resultado.
O executor só poderá emitir **PRONTA_PARA_REVISAO** após gates completos e
conferência de preservação, com resultado vinculado ao SHA no bundle final.
Nunca ACEITA. Próximo gate: **auditoria externa → decisão humana**.

Publicação autorizada somente em `sef/review-SE07-criar-objeto-l3-readme-piloto`,
depois dos gates e nova leitura dos workflows/PRs/refs. A canônica permanece
na F-04 aceita; a ref de review lida depois do push estará no índice externo.

## Delegação e integração

| Papel | Commit original | Commit integrado pelo coordenador |
|---|---|---|
| A | `c7bb7e27322d0646bc2b9383e34466db7b5045d9` | `2f1c511df42cba2589bb10de6892ea3067d94e4d` |
| B | `60836973244105d4ca60408e28bb1bac313b9282` | `53325af51b996fe01965edaa7b99da4b366e8938` |
| C | `7df698664c279052c3277a5a6c816a8e74185432` | `c1e1a67e9af96519983cbf2f3d3e474f2e8bf4ef` |

Quatro clones completos independentes, sem hardlinks/alternates, partiram de
d49. A: somente dois módulos runtime; B: suíte adversarial; C: gate repo-side
e sua suíte. Coordenador único integrador via cherry-pick com procedência,
autor de SKILL/manifest/docs/CHANGELOG/renderer e executor dos gates finais.
A [interface v1](../sprints/skill_enforcement/SE07/INTERFACE_README_L3.md) foi
congelada antes do dispatch; os snapshots compartilhados foram hash-pinned.

Solicitado `gpt-6-astra/high`. A/B: dispatch nativo com esses parâmetros aceito.
Tentativa de criar novo agente C falhou por limite total de threads; foi
reutilizado o agente nativo F-04 B já concluído, em clone/evidência novos, por
followup aceito. Seu dispatch original solicitou Astra/high; a API de followup
não confirmou nem sobrescreveu configuração. Máximo três auxiliares ativos.
Backend/modelo/esforço efetivos não introspectáveis, inclusive no coordenador.
Nenhum ganho percentual de paralelismo alegado.

## Escopo e arquitetura

Somente `create/readme/agregador`: um README ausente em diretório real existente.
Policy/registry continuam L2; contrato, L2, certifier, validator, receipt,
postflight, scorer, SE06 e workflows são preservados. D2/D9 só parcialmente
aprovada; conversão/overwrite/merge/replace e demais opções continuam não aprovadas.

Decisões, limites e recuperação estão no
[piloto](../sprints/skill_enforcement/SE07/PILOTO_README_L3.md).
Generate lê template canônico, chama L2 e produz bytes UTF-8/LF em memória.
Apply não regenera; exige autorização e validação vinculadas a operação/tipo/
escala/path/hash/tamanho/geração/base/release/template. Revalida topologia e
ausência; CREATE_NEW impede overwrite. Handles GENERIC_READ sem SHARE_DELETE
fixam ancestrais durante a operação. Envelope comprovado: Windows/NTFS local.
Sandbox deste host bloqueou acesso a ancestral; positivos ocorreram no contexto
normal autorizado, sem mudança de ACL, credenciais, privilégios ou infraestrutura.

Gate C usa clone completo e overlay único, validator real e checks de README/
links; não transporta tools ao produto. Reusa subprocessos do certifier F-04
em instância privada. Diretório vazio não versionado não é criado artificialmente
no overlay. Checks editoriais não provam qualidade ou execução de exemplos.
Autorizações locais e hashes não autenticam pessoa; runtime não executa validator.
GERADO, VALIDADO_NO_REPOSITORIO, AUTORIZADO e ESCRITO são distintos;
`homologated=False` sempre. Falha parcial permanece inconclusiva, sem rollback.

## Allowlist

- Fonte: `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/` — SKILL.md,
  release_manifest.json, scripts/run.py, scripts/_windows_writer.py.
- Derivado: os mesmos quatro paths sob `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/`,
  gerados somente por tools/render_simulado.py.
- Repositório: tools/skill_enforcement/validate_create_readme.py;
  tools/tests/test_validate_create_readme.py;
  tools/tests/test_skill_enforcement_se07_create_l3.py.
- Docs SE07: README.md, CHECKPOINT.md, TESTES.md, PROPOSTA_D2_D9.md,
  PILOTO_README_L3.md, INTERFACE_README_L3.md; este handoff e índice de handoffs;
  CHANGELOG.md e snapshot medido no README raiz.

Total esperado: 21 paths. O índice final relaciona cada path/blob e verifica
proteções contra a base. Nenhum ZIP versionado, nenhuma edição manual derivada,
PR, Actions, Free/Genie, main merge, R2, SE08 ou acesso a Ambiente_Antigo.
Checkout original do operador em F-03 e clone F-04 aceito permanecem preservados.

## Provas e tentativas antes do freeze

A base não tinha writer: cenários materiais classificados
`NOT_IMPLEMENTED_BASELINE`, não falhas de funcionalidade anterior.
Snapshot A v1 foi **NAO_APTO**: rename da pasta com READ_ATTRIBUTES,
arquivo criado antes de conversão fd reportado sem escrita, erro de close
escapando depois de sucesso e envelope contraditório aceito pelo verifier.
A, B e coordenador preservaram esses vermelhos antes das correções.

A v2 demonstrou GENERIC_READ causalmente com controles de rename com/sem
handles, CREATE_NEW contra existente e dois processos. Coordenador C03
reproduziu três defeitos v1; C04 repetiu os mesmos oráculos em v2 e confirmou
efeitos/status corretos. Oito probes de falhas A passaram. B08: **35/35 PASS**,
zero skips Windows/Python3.12.14, incluindo concorrência exits0/2 e interrupção
real após17 bytes/fsync, sem resultado final inventado; parciais preservados.
Os registros de validação A/B eram fixtures sintéticas, não validator real.

C demonstrou geração A v2 → validator real PASS; bytes alterados depois,
com autorização correspondente mas validação anterior, bloquearam apply,
sem arquivo e com Git original limpo. C005 foi BLOCKED no sandbox. C006
preservou checkout incompleto por caminhos longos apesar de Git exit0; guard
de limpeza bloqueou. C007 usou core.longpaths=true somente por invocação e
passou; nenhuma configuração global foi alterada.

C008: **25 PASS / 1 ERROR** na suíte de desenvolvimento. Erro de compartilhamento
depois de interrupção no helper aceito; gate FAIL e processo INTERRUPTED/130
conservados, mas a asserção esperava exit_code que não fora recuperado. O wrapper
antigo só reteve repr(PermissionError), sem stack/path/winerror numérico. A
identificação reportada como WinError32 é compatível com a mensagem, não foi
reconstruída como prova numérica. Oráculo posterior: três PIDs encerrados;
não identifica detentor do handle no instante. Hipótese de término assíncrono
não equivale a causa raiz estabelecida. Certifier aceito permanece intacto.

C010 reproduziu deterministicamente a perda da classificação com interrupção
real + erro de cleanup **sintético**, mantendo separados o incidente original
e a injeção. C011 confirmou FAIL/interrupted/130 e erro preservados. O gate
agora retém detalhes de exceção futuros, sem declarar cleanup resolvido.
O relatório C no núcleo selado registra a suíte final e seu número exato.

Preservados também FAILs sandbox, expectativas incorretas de harness corrigidas
sem flexibilizar oráculos, erro de apresentação cp1252, tentativas de commit
sem identidade configurada e erros de consulta PowerShell sem efeito Git.
Uma tentativa verde posterior nunca reclassifica esses fatos.

Na preparação documental, uma chamada do renderer sem `--write` foi somente
DRY-RUN. O stage seguinte falhou por usar path sem `Users/usuario-free`;
nenhum commit ocorreu. Logs preservados fora do núcleo já selado. A preparação
corrigida usa o destino canônico verificado e `--write`, seguida de validator
e conferência de delta; o dry-run não é contado como materialização.

## Gates finais, execução e limites

Executar serialmente no SHA documental exato e em clones novos: duas suítes
dedicadas, F-04, SE07/P01/F-02/F-03, renderer específico, validator com snapshot
README, ensaio integrado generate→validator→apply com autorização sintética,
releitura/verifier/retry e FULL SE07 sem atalhos. FULL aceito tem16 gates e
não incorpora automaticamente as duas suítes novas. Matriz: [TESTES](../sprints/skill_enforcement/SE07/TESTES.md).

Retenção: SE07_L3_EVIDENCE_DIR para B; SEF_CREATE_README_TEST_ARTIFACT_DIR para C;
SEF_CERTIFIER_TEST_ARTIFACT_DIR para F-04. Oráculos externos devem comparar
bytes/efeitos/PIDs/exits e HEAD/status, além dos summaries. O timeout configurado
dos comandos finais não implica timeout exercitado; testes curtos específicos
exercitam cancelamento/timeout e registram seus processos próprios.

Windows3.12.14 é o runtime desta rodada. WSL retornou lista vazia: Linux
`NOT_RUN`. Python histórico3.12.10 `NOT_RUN`; probe sandbox recebeu acesso
negado. Sem alegação multiplataforma. F-04 histórica Linux/Python e WinError32
continuam com seus limites; R1 NAO_APTA, SE06 24/25/A1-R4 NOT_RUN preservados.
Recorrência inesperada de compartilhamento em gate final exige investigação
específica e avaliação da prontidão, sem herdar dispensa automática da F-04.

## Índice probatório

Núcleo externo imutável `development_evidence_compact.zip`: SHA-256
`0baeab61543af69053b48bc50208bfd8812525ab7dc3bd557980630c7037f634`; manifesto SHA-256
`5b498678552fcb5fab1f3b614255d06712ee99e965ae77a2c85584333a713cfd`; 3774 entradas físicas mais manifesto,
63007 paths lógicos, todos os hashes conferidos. FILEMAP.json
mapeia cada path a seus bytes; conteúdos idênticos são armazenados uma só vez,
sem perda ou exclusão de tentativas. O ZIP original maior permanece intacto.
Contém A/B/C, baseline, snapshots, patches, ledgers,
fault injection, concorrência, interrupção, análise C008, ambiente e promoção
aceita. Omite somente .git de fixtures, caches e aliases, com lista no SCOPE;
nenhum conteúdo de quarentena foi lido. Não certifica este SHA documental.

O bundle único final inclui esse núcleo e registros posteriores ao freeze:
identidade/tree/allowlist, gates completos, efeitos reais do ensaio integrado,
refs/publicação e manifesto de cobertura. Seu hash final será entregue após
selagem; gravá-lo dentro do próprio commit certificado criaria autorreferência.
O índice externo amarra o pacote ao SHA exato e conserva o núcleo citado aqui.

GitHub permite verificar código, contratos preservados, manifests, testes,
ancestralidade/delta, decisões e estes documentos. Execução local, PIDs,
concorrência, cleanup, parciais, timeout realmente disparado, tentativas e
observações remotas no instante exigem o bundle; presença de teste não é PASS.
O bundle F-04 anterior permanece imutável e separado:
`33c7756bd83011b34d653bb5df22afa53061c97a5d0ccecb5baa72d74a184c48`.

## Pendências e parada

Medir os gates finais vinculados ao commit que contém este documento, confirmar
preservações e publicar review somente se seguro. Depois, exclusivamente
auditoria externa e decisão humana. Sem promoção L3, sem avanço da canônica,
sem Free/Genie e sem iniciar outra frente por consequência.
