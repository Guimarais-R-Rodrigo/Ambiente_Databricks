# Integração do Concierge ao Hub — 12/09/2026

Autor: Codex. Base: `f748c144dbb6909c7437b53498b25dd4f4854ab7`.
Ambiente local: Linux, Python 3.13.5. Sem conexão Databricks.

## Escopo

Integração autorizada da skill em `ambiente_fonte/.assistant/skills/`, mantendo
protótipo histórico congelado. Atualizados política de skills, instruções,
READMEs, Manual/cópia, ADR, roteiros de forward test e estágios do CI. O simulado
foi gerado exclusivamente pelo renderer. Helpers, prompts, imagens e os corpos
das skills especializadas foram preservados.

## Baseline anterior à mudança

O gate local da base reprovou exclusivamente em duas contagens coladas no README:
identidade (846 documentados versus 865 observados) e links de repositório
(387 versus 416). A adição experimental alterara o inventário sem sincronizar o
bloco. As suítes de biblioteca, ferramentas e transição passaram, com 7 testes
Spark opcionais não executados. Não atribuir esse defeito à nova integração.

## Execução local

Comandos:

```bash
python tools/validate_assistant.py
python tools/render_simulado.py --write
python tools/validate_assistant.py --conferir-readme
python tools/ci_local.py --verbose
```

Os comandos foram executados na worktree de integração; o inventário foi
conferido com os arquivos novos adicionados ao índice Git. Os números mutáveis
estão na saída do README raiz, que o gate reconfere. Não se atribuem os arquivos
novos ao hash da base: o hash acima identifica apenas o ponto de partida.

Resultado consolidado do CI:

```text
OK validacao
OK biblioteca
OK ferramentas
OK transicao
OK concierge-pacote
OK concierge-regressoes
OK concierge-integracao
APROVADO: 7 etapa(s)
```

Nas cinco suítes unittest, 153 testes foram coletados: 146 passaram, zero falhas,
7 skips (contratos Spark opcionais da transição, sem runtime local correspondente).
As duas etapas restantes são validações estruturais, não testes conversacionais.
O resultado é local: não certifica Genie Code, Spark Databricks ou permissões.

A primeira execução de integração detectou a falta do Concierge no guia offline
de aceite do trabalho. O inventário desse guia foi atualizado e ganhou um caso
humano adicional; o gate inteiro foi então reexecutado e aprovado.

## Evidências específicas da funcionalidade

[Resultados do pacote](../../ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/RESULTADOS.md)
separam validação estática, regressões do verificador e aceite conversacional.
O CI executa 14 regressões do verificador e 12 testes de integração, além das
suítes já existentes. O renderer produziu um espelho conferido por conteúdo.

## Não realizado

Não houve chamada ao Genie Code, forward test, publicação Databricks, treino ou
consulta a dados reais. Os testes locais de Spark opcionais da suíte de transição
permanecem skips, não PASS. A publicação e o aceite no destino continuam pendentes.

A documentação oficial de Agent Skills foi reconferida em 12/09/2026; consulte
[Fontes do pacote](../../ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/fontes.md).
