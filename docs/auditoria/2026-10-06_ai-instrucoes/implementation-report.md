# Implementação local da arquitetura de instruções de IA

## Resultado e alcance

Implementação documental/tooling concluída localmente sobre a branch README
aprovada. Base: f2843eafae84d44cd751f307101de84f11981bd7; tree da base:
035c31b1e4c27549ab012d574dec54421dd9ea31. Branch: docs/ai-architecture-20261006.
Candidata executada: 420976e7b76373721998a5df96e996530764688d; tree:
ade8ff3bab3533cfa10803cdc44b537a3c22ab50. O pacote final identifica a revisão de
entrega e traz revalidação exata separada, sem SHA autorreferente neste documento.

S00–S05 têm implementação repo-side concluída. O aceite integral das etapas
continua bloqueado pelos casos nativos/plataforma aplicáveis. S06 está BLOCKED;
S07 conclui revisão/entrega local, sem aceite pleno multi-cliente nem publicação.
Não se declara os quatro fornecedores homologados.

## Entrega e rastreabilidade

AGENTS tem 72 linhas/4.725 bytes. A fonte editorial fica em docs/ai; exatamente cinco
skills em .agents/skills geram cinco integrações Claude com proveniência e hashes.
CLAUDE e GEMINI são shims mínimos, sem política concorrente ou settings modificados.
Há 215 obrigações por trecho, 58 ações originais (22/24/12), dez consumidores novos,
36 testes de aceite e 36 claims oficiais DOCUMENTED. Não há claim SUPPORTED.

Os 691 pares de produto permanecem byte-idênticos; policy, schemas, manifests,
licenças, Manual e instrução irmã ficam congelados. Os 1.383 paths rastreados sob
fonte/espelho não mudaram. Só README_GERADO.md muda, produzido pelo renderer em
cópia isolada após preflight de 692 arquivos, sem extras, e duas gerações iguais.

IA-12 continua encaminhado ao mantenedor para escopo documental do produto: o
exemplar transportado é template, não skill operacional. O aviso foi corrigido
nesta camada; nenhum ajuste do exemplar, renderer/payload ou manifest de produto
é alegado. ADR0001, resultados 14/42 e templates não executáveis são preservados.

## Comandos e evidência observada

Executar da raiz, com dependências existentes descritas em tools/README.md:

- python -B tools/ai_controls.py --check --release --migration-freeze
- python -B tools/tests/test_ai_controls.py -v
- python -B tools/validate_assistant.py --conferir-readme
- python -B tools/ci_local.py --verbose

Python usado: 3.12.14; Node instalado: 24.19.0; Linux x86_64. Dependências locais já
instaladas foram reutilizadas; nenhuma instalação ou chamada de modelo integra o CI.
--migration-freeze é só para esta campanha; evolução de produto autorizada futura
segue seus gates, sem reescrever os hashes históricos desta baseline.

Baseline: 12/12 etapas locais PASS. Candidata: 14/14 etapas PASS, preservando as 12
originais e acrescentando controles + regressões IA. Os 60 novos testes passaram;
negativos exigem a causa esperada. Validator: exit0, zero falhas e avisos.
Logs sanitizados: logs/baseline-ci.log, logs/candidate-ci.log,
logs/candidate-controls.log e logs/unit-tests.log, nesta pasta.

Skips herdados: 11 em Temas (UI opcional/escopo GitHub), 4 em SEF e 7 em transição
Spark. Não são testes executados nem homologação Windows/Databricks/runtime.
negative-probes.json registra detecção de HEAD divergente/worktree suja e rejeição
de identificador corporativo sintético pelo guardião existente, sem dado real.

rollback-result.json registra ensaio real em clone descartável: revert completo,
igualdade exata da árvore base, reaplicação dos três commits de implementação,
igualdade da árvore candidata, validação em ambos e preservação de nota alheia.

## Bloqueios e próxima ação

- Codex CLI 0.159.2: autenticação existente reportada, mas a tentativa read-only/
  ephemeral retornou exit1 antes da sessão por filesystem read-only ao inicializar
  app-server. JSONL vazio; nenhum arquivo carregado/modelo foi observado. Owner:
  operador, repetir em ambiente autorizado capaz de inicializar normalmente.
- Claude Code, Gemini CLI e Grok Build: executáveis ausentes. Owner: operador,
  usar clientes instalados/autorizados e executar docs/ai/native-test-protocol.md.
  Instalação/login/configuração, se necessários, exigem autorização própria.
- Windows: executor e PowerShell ausentes. Owner: operador, testar clone, caixa,
  LF/UTF-8, espaços, descoberta e cinco skills no host autorizado.
- Chats/Projects/Gems/APIs: pacote manual e manifesto não demonstram autoload nem
  leitura no serviço. Owner: usuário/mantenedor decide superfícies reais e autoriza
  uploads/configurações necessários; depois executa T29 com provas de SHA/conteúdo.
- Publicação Git: owner usuário, push manual da branch dedicada sem force/main
  merge; depois conferir ref remoto e CI do SHA. T36 está NOT_RUN. Nenhuma escrita
  GitHub, PR, merge ou implantação Databricks foi executada nesta migração.

As versões/modelos/superfícies efetivamente adotados permanecem decisão do operador;
a proposta conservadora dos quatro clientes não foi reduzida para esconder bloqueio.

## Revisão e manutenção

Revisor distinto dos autores conferiu os 215 trechos/âncoras, diff e mutantes reais.
É contexto completo, mesma origem/coordenador, A0_light; não é A1 multi-origem nem
cego. Os defeitos encontrados no gerador foram corrigidos antes do freeze.
O laudo final do pacote identifica o SHA exato da revisão de entrega.

Editar skills só em .agents/skills, depois python tools/ai_controls.py --generate.
Gerador recusa paths fora da allowlist, symlink, saída alheia/editada, inventário
vazio, YAML inválido e divergência. Check é read-only/offline. Claims exigem revisão
oficial por evento e antes de novo suporte; >30 dias avisa normalmente e bloqueia
--release. OBSERVED/SUPPORTED só poderão ser promovidos com schema de evidência
validado em evolução revisada. Sem mudanças automáticas de segurança ou settings.
