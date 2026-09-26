# Sprint 5 — `hub_prompts`, as partes 1 e 2

Data: 2026-08-17 · Executor: Claude · Escopo: os 16 prompts convertidos para
pasta de objeto, cada um com o notebook de três partes — **com a terceira em
branco por decisão de projeto**.

Esta sprint saiu do caminho crítico na calibração do plano justamente por
depender de você. O que dava para adiantar foi adiantado.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 11 aviso(s)
                        78 notebooks
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
notebooks               16 de 16 SUCCESS (partes 1 e 2)
parte 3                 16 de 16 PENDENTE — depende de interação humana
```

## Por que a parte 3 fica em branco

O template de prompt é explícito: *"A parte 3 exige uma pessoa. Não há como
gerá-la, e resposta inventada é pior que resposta nenhuma — ela ensina que o
assistente faz algo que ele não faz."*

Prompt existe para produzir uma resposta de assistente. Colar uma resposta que eu
escrevesse seria a versão mais grave do defeito que as auditorias vêm pegando
desde a Sprint 7: **saída fabricada apresentada como real**. E seria pior aqui do
que nos notebooks de helper, porque um número inventado alguém confere
reexecutando — uma resposta de assistente inventada, ninguém.

Cada um dos 16 traz o bloco canônico de não executado com o motivo, mais um
roteiro de cinco passos para quem for preencher.

## O que os 16 notebooks entregam prontos

**Parte 1 — preparo executável.** Cada notebook cria a base sintética a que o seu
prompt se refere, com a fixture certa e com o defeito certo plantado:

| Notebook | Base | O que foi plantado, e por quê |
|---|---|---|
| `data_quality` | `base_tabular(n_entidades<n)` | 4.000 linhas para 3.200 clientes — a duplicata de chave é o defeito que o prompt existe para achar |
| `comparar_tabelas` | duas versões | volume e taxa de nulo diferentes; nenhuma das duas aparece comparando só esquema |
| `cross_eda`, `feature_engineering` | `fatos_e_features` | uma em cada cinco features tem data **posterior** à decisão — vazamento plantado |
| `safra` | `safras` de três meses | a safra mais antiga tem MOB maior, que é a armadilha inteira |
| `monitoramento_modelo` | dois períodos | prevalência de 0,18 para 0,11 e nulo triplicado — mudanças reais com causas diferentes |
| `comentar_notebook`, `tutor_explicar`, `auditoria_skills` | nenhuma tabela | o insumo é um notebook, um módulo e uma skill, todos já publicados |

**Parte 2 — o prompt preenchido.** Os briefings têm de 7 a 12 placeholders cada;
todos os **~160** estão preenchidos, para a base da parte 1, prontos para copiar.

Onde a resposta honesta era "não sei", está escrito **"não informado"** — e o
notebook explica que isso é informação: dizer que você não conhece a chave é
diferente de omitir a linha, porque o assistente passa a ter de descobri-la em
vez de assumir.

## O que a conversão quebrou, e o que pegou

Os prompts desceram um nível — `hub_prompts/eda_rapida.md` virou
`hub_prompts/eda_rapida/eda_rapida.md` — e os 16 links para
`../CATALOGO_HELPERS.md` quebraram. É a mesma classe de defeito da Sprint 2, e
foi corrigida do mesmo jeito: **recalculando a profundidade com `os.path.relpath`**,
não com substituição cega de texto.

A validação pegou os 16 de uma vez. O `--verify` pegou o que ela não vê: os 16
briefings planos continuavam no workspace depois de removidos da fonte.

E a execução pegou um erro meu: `agg({"id_contrato": "countDistinct"})` não
resolve — o nome não existe como rotina SQL. A forma que funciona é
`F.countDistinct`, e o notebook agora explica a diferença no comentário.

## O que fica para você

Os 16, na ordem que preferir. Para cada um:

1. rodar a Parte 1 — ela cria a tabela;
2. colar a Parte 2 num **chat novo**;
3. colar a resposta, com a data;
4. registrar **qual skill foi carregada**;
5. comentar o que o assistente fez bem e **o que deixou de fora**.

O passo 4 é o que transforma isto em evidência de roteamento fora da bateria de
forward tests — são 16 observações a mais, em pedidos realistas.

Dois casos merecem atenção especial: `comparar_tabelas` e `novo_projeto` **não
declaram skill recomendada** no cabeçalho, de propósito. O que o Genie Code
escolher neles é informação sobre o roteamento que nenhum outro teste produz.

## O que fica para depois

| Item | Por quê |
|---|---|
| As 16 partes 3 | dependem de você, no Genie Code |
| Dívida de saída colada: 11 notebooks | §12.1 do plano |
| Duplicação de cor em 12 módulos | §12.2 do plano |
