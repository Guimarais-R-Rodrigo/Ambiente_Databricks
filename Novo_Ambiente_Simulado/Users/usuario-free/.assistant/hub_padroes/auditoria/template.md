# Template — prompt de auditoria de sprint

Toda sprint fecha com uma rodada em **aba nova**, sem o contexto de quem
executou. Este arquivo monta o prompt.

## Por que em sessão sem contexto

Quatro rodadas neste projeto, quatro resultados: 13 achados na biblioteca, 22 e
25 na documentação, 25 no plano — todos em material que o autor já havia
revisado. A taxa não cai. Autorrevisão não encontra pressuposto do autor, porque
o pressuposto é invisível para quem o tem.

## As três invariantes

Presentes em todo prompt, e é o que fez as quatro rodadas funcionarem:

1. **Acesso ao disco e à CLI.** Auditor que só lê julga o texto; auditor que
   executa encontra o que quebra.
2. **Instrução para executar, não ler.** "Refaça o que a sprint fez, sobre um
   objeto, numa cópia temporária" produz achados que leitura nenhuma produz.
3. **Bloqueio de `CHANGELOG.md`, `docs/auditoria/`, `docs/sprints/` e do
   histórico do git.** Todos contêm o raciocínio de quem executou. `git log`
   sozinho entrega a sprint inteira.

## Profundidade por tipo de sprint

| Tipo de sprint | Profundidade | Foco do prompt |
|---|---|---|
| Fundação (ferramentas) | completa | o que a ferramenta deixa passar |
| Padrões | completa + leitura humana | ambiguidade que faria dois executores divergirem |
| Renomeação mecânica | de execução | o que quebrou sem ninguém ver; referência órfã; remoto sujo |
| Portão de formato | completa | se o formato aguenta os extremos do que virá |
| Conteúdo repetido | por amostragem | o auditor escolhe os objetos; 3 a fundo, varredura rasa no resto |
| README de topo | completa | percurso do leitor que chega sem contexto |
| Skill nova | completa + forward test | colisão de roteamento com as existentes |

## O esqueleto

```text
Você vai auditar o resultado de uma sprint de reestruturação. O objetivo não é
julgar o texto: é descobrir o que quebra quando alguém usar isto.

CONTEXTO
- Repositório: <caminho>
- O que a sprint entregou: <uma frase, sem justificativas>
- Arquivos no escopo: <lista ou pasta>

O QUE VOCÊ PODE LER
<pastas liberadas>

O QUE VOCÊ NÃO DEVE LER
CHANGELOG.md, docs/auditoria/, docs/sprints/, e o histórico do git
(git log, git show, git diff de commits). Contêm o raciocínio de quem executou.
git status e git ls-files são permitidos.

SOMENTE LEITURA
Não edite arquivo do repositório, não faça commit, não rode --execute. Para
experimentos, use pasta temporária fora do repositório e diga onde.

OS TESTES
T1 — EXECUTE, não leia. <a tarefa concreta de refazer/usar o que a sprint fez>
T2 — Reproduza todo número afirmado, com o comando que usou.
T3 — Teste toda afirmação técnica; confirmada, contradita ou não testável.
T4 — Divergência: onde dois executores competentes produziriam resultados
     diferentes? Cite o trecho, as duas leituras e a diferença no arquivo final.
T5 — O que a sprint não menciona e vai atingir.
T6 — Confronte com as regras do projeto em .claude/rules/.
<T7+ específicos da sprint>

FORMATO
Comece pelo T1, em prosa. Depois três listas ordenadas por custo de descobrir
tarde: QUEBRA (não funciona / falta algo sem o qual para), DIVERGE (ambiguidade
entre executores), MELHORÁVEL (só entra se disser o que se perde mantendo).
Termine com: o maior risco; a pergunta que você faria antes de continuar; o que
acertou e deve sobreviver; o que não conseguiu avaliar.

REGRAS
- Não elogie, não resuma de volta, não abra com apreciação geral.
- Achado sem evidência que você produziu não vale: descarte.
- Distinga "não funciona" de "eu faria diferente"; a segunda só entra com o
  custo concreto de manter.
- Trate justificativa como afirmação a verificar, não como explicação a aceitar.
- Priorize o defeito que só apareceria depois de dezenas de arquivos escritos.
```

## O que fazer com o resultado

Verifique **cada achado contra o disco** antes de aceitar. Nas quatro rodadas
deste projeto todos procederam, o que não é garantia para a próxima — e um
achado aceito sem verificação vira correção que quebra outra coisa.

Registre em `docs/auditoria/<data>_<tema>/`, com o que foi confirmado e o que a
correção não precisou tocar. A segunda lista delimita o escopo tanto quanto a
primeira.
