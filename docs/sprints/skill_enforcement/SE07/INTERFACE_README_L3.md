# Contrato de integração do piloto — v1, antes de implementação

Base aceita/promovida: d49c8728f0e47adc15f7f78293c9fcc58c809a15.
Escopo único: create/readme/agregador. Skill/policy continuam L2, target L3.
Mandato humano em evidence/MANDATO_HUMANO.txt. Não há autorização de produto real:
escritas de demonstração devem ocorrer somente em fixtures sintéticas externas.

## APIs runtime (arquivo canônico da skill scripts/run.py)

`generate(context, document, *, base_sha, assistant_root=None) -> dict`

`apply(candidate, authorization, validation, *, assistant_root=None,
        evidence_dir=None, evidence_authorized=False) -> dict`

`verify_evidence(payload, *, assistant_root=None) -> dict` com `valid`, `issues`.

CLI subcomandos generate/apply aceitam arquivos JSON explícitos e imprimem JSON.
Não escrever candidato em disco implicitamente: generate retorna memória/stdout.
Consumidores podem salvar esse JSON em staging externo explicitamente autorizado.
Apply exige evidence_dir externo novo, evidence_authorized True; nenhuma escrita
de evidência/staging dentro da raiz produto. Artefatos são evidência, não objetos
instalados. Falha de persistência pré-escrita bloqueia; pós-escrita conserva o
efeito observado e impede sucesso. Nunca apagar arquivo parcial ou tentar overwrite.

Context mantém campos L2 existentes; somente operation=create, object_type=readme,
readme_scale=agregador, destination_relative terminando README.md. Não aceitar
source_relative, convert ou flags novas de overwrite. Não alterar preflight.py.
base_sha: string SHA Git40, declarada no runtime, verificada pelo gate repo-side.

Document (objeto JSON, entradas editoriais explícitas, não narrativa inventada):
`title`, `identity`, `purpose`, `usage`, `limitations`, `next_steps` (strings não
vazias). `items`: lista de objetos `path`, `description`, apontando a filhos reais
da pasta, sem assumir que o conteúdo foi executado. Geração segue o template
agregador canônico, UTF-8/LF com newline final. Mesmas entradas/árvore/template
produzem mesmos bytes. Não inserir run_id/timestamp no conteúdo do README.
Próxima ação pode ser leitura de guia, sem comando analítico. Tabela visual de
inventário; nenhuma seção de objeto/quinze títulos aplicada ao agregador.

Generate retorna envelope com:
- `status`: GERADO ou BLOCKED/FAIL; `writes_performed` False;
- `candidate`: objeto somente se gerado, com `binding` e `content_utf8`;
- `trace`: preflight_status, fases chamadas/concluídas, template lido, issues;
- `evidence`: registro de integridade limitado ao piloto, sem homologação.

Binding, compartilhado exatamente por autorização e validação:
`operation`, `object_type`, `readme_scale`, `destination_relative`,
`content_sha256` (bytes UTF8), `content_size`, `generation_id`, `base_sha`,
`release_sha256` (manifest), `template_sha256`.
Candidate inclui context/document necessários para reverificação, identidade da
raiz/ancestrais e evidência da geração (campos adicionais permitidos se não
mudarem o binding público). Integridade estrutural usa canonical_json_bytes e
sha256_digest canônicos de hub_scripts.skill_execution.receipt; hash de bytes
usa hashlib padrão, sem implementação criptográfica/serialização paralela.

Authorization: `{ "decision":"AUTHORIZE_CREATE", "binding":<igual>,
"authorization_id":<string não vazia>, "authority":"external_confirmation_record" }`.
Não oferecer helper runtime que autorize automaticamente. B/C podem construir
registro de autorização sintético em testes explicitamente identificados.
Isso prova apresentação de registro correspondente, não identidade humana,
assinatura, ACL ou autenticidade criptográfica. Não alterar threat model.

Validation: `{ "status":"PASS", "binding":<igual>, "validator":
"repo_side_create_readme_v1", "validation_id":<digest>, "checks":<não vazio> }`.
Gate C fornece campos adicionais de proveniência/head/logs/overlay. Apply valida
forma e igualdade de binding/ID; não afirma ter executado tools nem autentica
criptograficamente o emissor local. C e A devem usar exatamente o mesmo cálculo
de validation_id: sha256_digest do objeto inteiro sem validation_id.

Apply recebe candidate (não envelope generate), nunca regenera o conteúdo.
Revalida release/template, conteúdo/binding, L2 e superfície estrita writer,
raiz e cadeia material até parent, ausência, identidades observadas na geração.
Criação exclusiva demonstrada: sem sobrescrever em corrida; dois applies, só um
cria. Proteger contra troca concorrente de ancestral com primitivas do host;
mera resolve/check/open não é defesa suficiente. Topologia não demonstrada =>
BLOCKED/UNSUPPORTED explicados, não downgrade silencioso. Usar stdlib; não novas
dependências. Não alegar atomicidade universal/durabilidade de transação.

Retorno apply: `status` ESCRITO, BLOCKED, FAIL, INCONCLUSIVE ou INTERRUPTED;
`writes_performed` reflete efeito real (inclusive arquivo criado vazio/parcial);
`trace`, `evidence`, `issues`, hashes/tamanho observados quando disponíveis.
`homologated` False sempre. Nunca converter GERADO ou registro de validação em
ESCRITO. Retry em destino existente bloqueia, mesmo se bytes idênticos.
Interrupção/código externo não zero e artifact fallback não devem apagar efeitos.

Receipt V1 e postflight atuais têm invariantes EDA/numeric_columns e writes=False:
não reutilizar builder fabricando esses fatos. Reusar hashing/serialização;
envelope/verificador exclusivamente local da skill é compatível com precedente
do auditor. Sem nova versão UNIVERSAL de Receipt nem mudança em infraestrutura.

## Gate C repo-side

`tools/skill_enforcement/validate_create_readme.py`:
`validate_candidate(candidate, *, repo_root, evidence_dir) -> dict`.
Recebe candidate, exige repo HEAD==binding.base_sha e árvore limpa; cria clone
descartável completo em evidence_dir explícito/novo, overlay único no path
ambiente_fonte/.assistant/destination_relative (ausente), roda validator real
do clone sem alterar tools/validate_assistant.py, verifica estrutura/template/
links/bytes. Resultado PASS/FAIL/BLOCKED sempre vinculado ao binding exato,
logs/exit/SHA antes e depois. O overlay não precisa ser commitado. Não contornar
checks de inventário/histórico; não conferir README snapshot sobre overlay como
se fosse snapshot de base inalterada. Renderer e FULL são gates finais separados.
Pode ter API check de compatibilidade estática para geração em workspace distinto
da cópia repo, mas não aceitar base arbitrária. Fixtures de teste são commits
sintéticos em clones externos; nunca remover README real para fabricar destino.

## Ownership

A: somente ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/scripts/run.py e
se necessário módulo(s) exclusivamente runtime dessa mesma pasta; nenhum outro
arquivo versionado. Manifest/contrato/SKILL do coordenador. Propor lista exata de
artefatos para manifest, antes de seu congelamento. Fixtures privadas geram seu
manifest próprio fora da árvore. Clones agent_a, evidência agent_a_evidence.
B: somente tools/tests/test_skill_enforcement_se07_create_l3.py. Independente,
oráculos externos de bytes/efeitos/concorrência/interrupção. Não editar A/C.
Clone agent_b, evidência agent_b_evidence.
C: somente tools/skill_enforcement/validate_create_readme.py e
tools/tests/test_validate_create_readme.py. Não editar runner, validator geral,
certifier, renderer ou policy. Clone agent_c, evidência agent_c_evidence.
Coordenador: contrato aditivo se necessário, manifest, SKILL, docs/changelog,
README snapshot medido, renderer, integração e gates. Nenhuma mudança policy.

Todos: máximo três auxiliares, sem subdelegação, sem push/PR/Actions/Free/merge.
Nenhum acesso Ambiente_Antigo. Nenhuma instalação/ACL/credencial/config global.
Guardar ledger ANTES de cada teste/probe; primeiro negativo antes de implementação,
classificando writer ausente NOT_IMPLEMENTED_BASELINE, não falha funcional antiga.
Não FULL nos auxiliares. Compartilhar commits/snapshots hash-pinned, não worktrees
em edição. Toda revisão de interface deve ser comunicada ao coordenador antes
de adotar divergência; novas versões serão adendos explícitos, não alteração muda.

## Síntese de leitura e limites

Plano SE07 exige policy explícita14/14, não promoção de todos targets. G2 mantém
SE06 incompleta24/25/A1-R4 NOT_RUN. SKILL/preflight L2 resolve templates e paths,
não comprova leitura nem autorização e preserva relações D2 de conversão.
Template agregador fornece nove seções com escala curta condicionada; template
de objeto é outro contrato. Validator do repo depende de inventário Git e tools,
renderer copia só fonte e markerLF. Auditor e EDA têm manifests hash-pinned e
limites de authenticidade; não generalizar os receipts existentes por conveniência.
F04 aceita localmente conserva Linux/Python histórico NOT_RUN e WinError32 conhecido.
