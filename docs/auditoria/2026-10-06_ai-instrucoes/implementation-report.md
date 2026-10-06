# Implementação local da arquitetura de instruções de IA

## Resultado e limites

Candidata documental/tooling implementada sobre a branch README aprovada. Produto
preservado: 691 pares de bytes fonte/espelho; policy, schemas, manifests, licenças e
Manual sem alterações. Só o marcador do simulado muda por renderer isolado.

Núcleo AGENTS, docs modulares, cinco skills canônicas, adaptadores determinísticos,
registro oficial e gate aditivo estão presentes. Nenhum cliente é declarado
homologado. Claude Code, Gemini CLI, Grok Build e Windows estão BLOCKED por acesso
ou ferramenta ausente; o ensaio Codex é registrado separadamente. Chats/APIs não
recebem contexto automaticamente. Nenhum workspace Databricks foi acessado.

## Rastreabilidade

Há 58 registros originais (22 controles, 24 dependências, 12 achados), dez
consumidores adicionais e 215 obrigações por trecho. Fontes antigas são preservadas
em dados históricos e Git; rotas ativas migram sem reescrever campanhas ou ADRs.
IA-12 permanece explicitamente fora do payload: o exemplar transportado não é
skill operacional; uma mudança nele exige escopo de produto próprio.

## Validação

Baseline: 12 etapas locais aprovadas. Candidata final: aguardando execução no SHA
congelado. Os testes novos são locais, sintéticos e offline, com negativos que
precisam reprovar pela causa esperada. Skips herdados não viram testes executados.

## Revisão

Revisor distinto dos autores confere fonte, diff, 215 obrigações e casos adversos.
É revisão de contexto completo, mesma origem/coordenador, nível A0_light; não é
homologação multi-fornecedor A1 nem auditoria cega. Os primeiros defeitos e correções
ficam preservados na evidência de revisão distribuída com o pacote.

## Fronteiras

Sem mudança de settings, auth, tokens, ACL, MCP ou permissões; sem publicação,
produção, API paga, PR ou merge. Push será manual pelo usuário; SHA remoto e CI
continuam não verificados. Sessões nativas e Windows dependem do operador e do
escopo autorizado, conforme docs/ai/native-test-protocol.md.

## Reversão e manutenção

A reversão restaura o conjunto inteiro de commits desta migração em clone de ensaio,
preserva mudança alheia e valida o conteúdo anterior; depois reaplica e compara
com a candidata. O pacote registra o resultado real e comandos seguros.
Editar skills somente em .agents/skills e gerar integrações; nunca editar cópia
Claude. Claims exigem revisão oficial por evento e antes de nova declaração de
suporte. O freeze de produto é desta campanha e não veta evolução futura autorizada.
