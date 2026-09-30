# SD-VF-P-D01 — diagnóstico com seleção explícita — 2026-09-29

(Codex) [Resposta integral como recebida](SD-VF-P-D01_resposta.txt).
SHA256: `f3681a0e0a47998a84a2e7032de3d079c8eeb383f91a9d6d22ae313e63efd41e`.

- Executor: Rodrigo; coleta no Genie Code / Free.
- Confirmação humana literal: **“selecionei”**, em resposta à instrução de
  selecionar hub-ml-analise-safra pelo seletor @. O anexo também traz o nome antes
  do prompt; esse texto isolado não seria prova de seleção.
- Chat, horário exato, runtime e path efetivo do notebook: não fornecidos.
- Publicação de referência: R2 + SAFRA-UI-01, hash
  `cf6fc86449834ffca9abb48bfb780ed56f53a7483f5504e42b9e485fe586993a`.
- Seleção explícita: **CONFIRMADA POR OBSERVAÇÃO HUMANA**; critério de seleção
  D01 PASS. Não atesta bytes carregados nem roteamento automático.
- Carregamento interno/contexto: **NOT_OBSERVABLE**; sem evento independente no anexo.
- TASK_CORRECTNESS: **PASS** no caso conceitual; AGENT_ADHERENCE: **PASS**;
  CANONICAL_COMPLIANCE: **PASS** limitado à resposta textual e ao escopo declarado.
- Execução: **NOT_RUN**, coerente com a pergunta conceitual; não houve alegação de
  execução canônica. Não é prova de runner/Receipt/efeito remoto.
- VEREDITO: **PASS do diagnóstico nesta execução**.

## Evidência dos critérios

1. Denominador dois preservado e contas das quatro células completas corretas.
2. CUMULATIVE usado como estoque já acumulado, com não decrescimento por contrato.
3. Janeiro/MOB2 conserva numerador desconhecido e taxa não finalizada; reconhece
   explicitamente que o valor da única observação não foi informado.
4. Não identifica arbitrariamente qual contrato é observado nem atribui causa à
   ausência. Possibilidades mencionadas são hipóteses, não fatos estabelecidos.
5. A tabela descreve cobertura informal. A resposta ressalva que sem corte não
   se pode emitir classificação formal IMMATURE/INCOMPLETE. Essa ressalva também
   limita qualquer comparação formal entre safras às validações temporais faltantes.
6. Distingue contas ilustrativas de execução, aponta scripts/run.py e solicita
   IDs, datas, corte e targets antes de preparar uma execução real.

## Limites e decisão

D01 altera a condição de seleção, não o prompt analítico. Não substitui SD-VF-P
nem SD-VF-A, não apaga os FAIL de T01/T02 e não prova que selecionar @ foi a causa
única da melhora. A coleta é insuficiente para afirmar que a skill só funciona
com @ ou que o modo espontâneo foi corrigido.

SAFRA-UI-01 permanece parcialmente pendente no modo espontâneo; falha de
preenchimento não reproduzida nesta execução com seleção explícita. Nenhuma
nova edição/publicação é indicada por D01. Próximo caso independente: SD-VF-N,
chat novo sem @ para avaliar se uma tarefa de drift é distinguida de Safra.
SD-VF-A permanece NOT_RUN e será coletado separadamente.

Auditoria independente confirmou o PASS conceitual limitado a D01, sem achado
material, e a continuidade com SD-VF-N sem alterar o produto.
