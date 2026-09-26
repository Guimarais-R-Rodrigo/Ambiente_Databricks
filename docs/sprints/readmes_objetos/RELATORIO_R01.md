# Relatório R01 — fundação documental e controles

Estado: implementação candidata validada localmente; aceite humano pendente.
R02 não iniciada. Autoria e revisão própria: Codex. Data: 2026-09-12.

## O que foi implementado

Contrato único com quinze seções e abertura de consulta rápida, checklist
editorial, três READMEs de exemplar e atualização cirúrgica das regras existentes.
O Manual preserva a responsabilidade pelo catálogo e pelos termos integrados.
A matriz de alterações separa texto de autoria, cópias sincronizadas, derivados,
ferramentas, workflows e registros da própria migração.

A cobertura é progressiva e identificada por caminho. O novo gate recusa aumento
ou reintrodução de dispensas, inclusive depois de commit, exige histórico completo
e distingue as três famílias de objetos e os exemplares. Títulos dentro de
código/comentário não contam como seções; um documento sem conteúdo não passa.
Links locais, versão e arquivos obrigatórios são verificados sem importar helpers.
Fontes externas, domínio estatístico e acolhimento continuam sendo revisão humana.

## Baseline

`python tools/ci_local.py --verbose` foi executado antes das alterações. As duas
falhas foram divergências preexistentes das contagens citadas no README raiz.
Biblioteca: 45 testes aprovados; ferramentas: 39 aprovados; transição: 43 casos,
36 aprovados e sete pulados. Os sete exigem execução Spark opcional, ausente na
sessão. Não foram convertidos em aprovação.

## Comandos de fechamento

O registro de evidência acompanha o pacote desta entrega. O gate é executado com
Python local, sem credencial Databricks. Logs e hashes não representam homologação
no workspace do trabalho.

```text
python tools/tests/test_readme_objeto_contract.py
python tools/render_simulado.py --write
python tools/validate_assistant.py
python tools/ci_local.py --verbose
```

## Limites do aceite

Não foi alterada lógica de treinamento, transformação, diagnóstico ou prompt
colável. As modificações em `.py` de exemplo e no template de notebook são
somente comentários Markdown; a AST é comparada com o snapshot. Imagens,
identidade visual e Concierge experimental permanecem iguais em bytes.

O baseline Git local tem a árvore verificada do snapshot, mas não o histórico
remoto. A trava histórica tem testes com repositórios temporários de vários
commits; a integração em GitHub deve confirmar o mesmo contrato com fetch-depth
zero. Não se usa ausência de histórico para aprovar uma regressão.

Revisão independente, aceite humano, execução Spark/Databricks e teste do
comportamento de Genie Code permanecem pendentes. Este relatório não certifica
um nível de auditoria independente.

## Documentações além dos READMEs

Consulte a [matriz nominal](MATRIZ_ALTERACOES_R01.md). Cada entrada informa o
motivo da mudança e separa os arquivos derivados dos documentos autorais. Os
[achados](ACHADOS_R01.md) explicam correções e ressalvas feitas nos exemplares.

## Evidências anexas

- [Baseline completo](evidencias/baseline.txt).
- [Testes adversariais de README](evidencias/testes-readmes.txt).
- [Gate final](evidencias/gate-final.txt).
- [Preservação de código, prompts e cópias do Manual](EVIDENCIAS_R01.json).

Os resultados finais são os registrados nesses arquivos. Sete testes opcionais
Spark pulados continuam visíveis; não foram substituídos por sucesso fictício.

## Resultado local efetivamente obtido

Gate completo: **cinco etapas aprovadas**. Biblioteca: 45 testes aprovados;
ferramentas: 39 aprovados; transição: 43 descobertos, 36 aprovados e sete pulados;
READMEs: 39 testes aprovados. Total: 166 casos, 159 aprovados e sete pulados.
Validação estrutural: zero falhas e zero avisos; cobertura de objeto: zero de
74 operacionais (migração não iniciada), três de três exemplares presentes.

A comparação de preservação examinou 424 arquivos protegidos. Quatro arquivos
Python tiveram mudanças somente em comentários; AST igual à base. Os 17 blocos
coláveis dos prompts conferidos permaneceram iguais. As três cópias do Manual
produziram o mesmo SHA-256. Nenhuma imagem, helper analítico ou arquivo do
Concierge experimental foi modificado.

Python local: 3.13.5. Uma advertência de parsing de datas já observada no
baseline da biblioteca permanece no log; não é uma falha do validador.
