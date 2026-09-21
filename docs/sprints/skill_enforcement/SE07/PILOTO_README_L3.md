# Piloto L3 — create/readme/agregador

## Decisão e escopo

Mandato humano de 2026-09-21: F-04 `d49c8728f0e47adc15f7f78293c9fcc58c809a15`
aceita; D2/D9 aprovada parcialmente para esta única superfície. A implementação
é candidata, sujeita a auditoria externa e decisão humana. Policy e registry
permanecem `current_level=L2`; target L3 e modo stage_specific não mudam.
O [checkpoint](CHECKPOINT.md) distingue a base aceita da candidata nova.

O objeto é um único `README.md` agregador ausente, em diretório real existente
da raiz permitida. Não criar pastas nem completar índices por inferência.
Conversão, destino existente, overwrite, replace, merge, remoção, movimento,
origem `.`, hardlinks, topologia symlink/junction, volumes distintos e rollback
destrutivo continuam fora do piloto. A [proposta D2/D9](PROPOSTA_D2_D9.md)
original permanece histórica; somente a fatia acima recebeu decisão.

## Arquitetura e fases

O [runner](../../../../ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/scripts/run.py)
viaja em `.assistant`. O
[gate repo-side](../../../../tools/skill_enforcement/validate_create_readme.py)
fica em `tools/`, junto ao validator e à certificação. Não há transporte de
ferramentas do repositório para obter autonomia artificial do runtime.
Detalhes de API e ownership foram [congelados antes do dispatch](INTERFACE_README_L3.md).

| Fase | Executa | Evidência e limite |
|---|---|---|
| GERADO | L2, leitura do template, inventário, renderização determinística em memória | Bytes UTF-8/LF, tamanho, destino, base, release, template e geração; produto sem escrita |
| VALIDADO_NO_REPOSITORIO | Clone completo limpo da base, overlay único, checks de README/links e validator real | Relatório vinculado aos bytes; não é execução no Free nem homologação |
| AUTORIZADO | Apresentação de registro externo específico | Decisão `AUTHORIZE_CREATE`, autoridade declarada, ID e binding; não autentica pessoa |
| ESCRITO | Revalidação, criação exclusiva, escrita, fsync, releitura, fechamento e evidência | Efeito medido; não é homologação ou promoção de policy |
| HOMOLOGADO | Não executado pelo piloto | `homologated=False`; depende de gate humano posterior |

As fases são fatos distintos. O runtime recebe o resultado repo-side, verifica
seu binding e hash estrutural, mas não afirma executar o validator nem comprovar
a identidade criptográfica de seu emissor. Não há helper que se autoautorize.

`generate(context, document, *, base_sha, assistant_root)` recebe os campos L2
atuais e o conteúdo editorial explícito: título, identidade, propósito, uso,
limites, próximo passo e lista de filhos/descrições. Não inventa FAQ, exemplos
executados ou resultados analíticos. Lê o template agregador canônico; a tabela
de inventário deve corresponder aos filhos reais. Mesmas entradas, árvore e
template produzem os mesmos bytes; o identificador de geração é distinto.

`apply(candidate, authorization, validation, *, assistant_root, evidence_dir,
evidence_authorized)` não regenera conteúdo. Compara operação, tipo, escala,
path, SHA-256/tamanho, generation_id, base Git, release e template. Reexecuta
L2 e confere conteúdo, manifesto, raiz, ancestrais, ausência e inventário antes
da primitiva exclusiva. Qualquer binding divergente bloqueia.

Gerar não salva candidato implicitamente. O caller pode salvar JSON em staging
externo autorizado. Apply exige diretório externo novo de evidência e autorização
explícita desse staging; uma falha anterior à criação impede a escrita. Essa
evidência externa não é outro objeto instalado no produto.

## Primitiva, prova e limitações

O [módulo Windows](../../../../ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/scripts/_windows_writer.py)
usa `CreateFileW(CREATE_NEW)` para criar se ausente e falhar se existente.
Cada ancestral material, desde o drive até o parent, é aberto com
`GENERIC_READ`, `OPEN_EXISTING`, `BACKUP_SEMANTICS` e `OPEN_REPARSE_POINT`,
compartilhando leitura/escrita, sem `FILE_SHARE_DELETE`. Reparse points e mudança
de volume são rejeitados; os handles permanecem vivos durante a operação.
O arquivo novo usa share zero; sua identidade é observada antes da conversão
de handle para fd. A documentação da Microsoft descreve criação exclusiva e
o controle de acesso de delete/rename pelo compartilhamento;
[CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).

O envelope demonstrado é **Windows nativo, drive fixo local NTFS**. Outros
hosts/filesystems bloqueiam; acesso insuficiente também bloqueia. Isso vale
inclusive para generate, que usa a mesma inspeção protegida. Nenhum privilégio,
ACL ou credencial é alterado. Os probes no sandbox retornaram WinError5 antes
da escrita; os positivos foram medidos no contexto normal do usuário.

A primeira implementação, somente com `FILE_READ_ATTRIBUTES`, foi refutada:
outro processo renomeou a pasta enquanto o handle estava aberto. O teste
pareado da correção demonstrou recusa com `GENERIC_READ` e sucesso depois do
fechamento; CREATE_NEW preservou destino existente e admitiu somente um dos
dois concorrentes. As tentativas anteriores não foram apagadas. WinError32
esperado como recusa de rename nesses probes não é o incidente histórico de
cleanup F-04, cuja causa segue desconhecida.

Não se promete atomicidade de conteúdo, transação universal, journal atômico,
durabilidade sob perda de energia ou proteção depois que os handles terminam.
Uma morte abrupta pode deixar vazio/parcial com registro prévio incompleto.
Não existe recuperação automática destrutiva. Inspecionar o arquivo real,
identidade/hash e último registro; marcar inconclusão e obter decisão humana.
Retry não substitui recuperação: destino existente sempre bloqueia.

## Evidência local

O runner reutiliza `canonical_json_bytes` e `sha256_digest` da infraestrutura
canônica. Usa um envelope e verifier próprios desta skill; não introduz uma
versão universal de Receipt. O Receipt V1/postflight existentes possuem
invariantes de ausência de escrita e contexto EDA, que não são fabricados nem
alterados para acomodar o writer. Contrato L2 e `no_write_guarantee` do preflight
permanecem byte a byte iguais à base aceita.

O manifesto da skill fixa oito artefatos: SKILL, contrato, preflight, runner,
primitiva, checklist, template agregador e receipt engine. Hashes Git blob
protegem integridade da release; hash bruto identifica manifesto/template/bytes.
Isso não constitui assinatura ou autenticação do produtor.

No desenvolvimento C008, houve erro de compartilhamento após interrupção real
no helper do certifier aceito. O gate ficou FAIL, sem escrita original; o record
conservou interrupção/130 e os PIDs estavam encerrados na observação posterior.
O wrapper antigo não reteve stack/path nem código Win32 numérico. A identificação
relatada como WinError32 é compatível com a mensagem, mas não foi reconstruída
como fato numérico. A fronteira C conserva o erro e a interrupção observada;
isso não corrige nem resolve a dívida do certifier. Logs e análise estão no bundle.

Os registros externos de apply distinguem preparação, criação confirmada,
resultado final e falha. Mesmo vazio ou parcial, um arquivo efetivamente criado
implica `writes_performed=True`. Falha de escrita, releitura, fechamento ou
persistência posterior impede `ESCRITO`. O verifier checa integridade e coerência
entre envelope e evidência; não transforma a apresentação de JSON em prova
independente de identidade ou homologação.

## Validação e auditoria

O gate C exige HEAD igual à base declarada, árvore limpa e histórico completo.
Clona externamente, mantém o original, aplica somente os bytes candidatos em
destino ausente e executa L2, checks editoriais/links e `validate_assistant.py`
reais. Renderer/FULL são gates finais separados; o overlay não altera a base
nem é artificialmente commitado para satisfazer o snapshot do README raiz.
O parent precisa ser recuperável nessa base Git: diretório vazio não versionado
desaparece no clone e permanece bloqueado, sem criar topologia adicional.
O checker estrutural admite inventário vazio quando a pasta observada é vazia;
isso não substitui a precondição de existência no clone.

Checks editoriais são estruturais: não provam qualidade do texto, execução de
exemplos ou aceite. Um artefato local pode ter hashes corretos e emissor não
autenticado; a decisão externa é necessária. Os [testes](TESTES.md) e o
[handoff](../../../handoffs/2026-09-21_se07-criar-objeto-l3-readme-piloto.md)
separam contratos verificáveis no Git de execuções dependentes do bundle.

Linux/WSL, Python histórico 3.12.10 e Free/Genie não foram executados nesta
rodada. SE06 permanece 24/25/A1-R4 NOT_RUN; R1 continua NAO_APTA histórica.
O próximo gate deste piloto é somente **auditoria externa → decisão humana**.
