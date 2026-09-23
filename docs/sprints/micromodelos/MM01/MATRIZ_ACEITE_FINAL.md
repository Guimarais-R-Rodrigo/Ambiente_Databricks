# MM01 — Matriz de aceite final

Status: **CONGELADA após o contraditório da oitava A1**

Esta matriz fixa a condição objetiva de término da MM01. A auditoria final deve verificar se a candidata cumpre os requisitos abaixo; ela pode descobrir novos casos adversariais, mas um caso novo só é bloqueante quando demonstra violação de um requisito já assumido nesta matriz ou de um ADR aceito. A auditoria final não pode criar requisitos novos por extensão do threat model.

## 1. Autoridade e escopo

A MM01 define o contrato canônico de `micromodelo.yaml`, seu schema Draft 2020-12, a máquina local de estados, gates semânticos, proveniência, validação e a ferramenta de construção/CI que valida esse contrato.

Continuam fora de escopo:

- fingerprint/identidade material da MM02;
- crawler ou binding corporativo real da MM03;
- criação da skill ou de novo tipo do Hub da MM04;
- contrato definitivo de MLflow da MM06;
- publicação corporativa real, ACLs reais, dados corporativos reais e migração de legado;
- equivalência semântica geral de linguagem natural;
- interpretação de objetos numéricos arbitrários de bibliotecas Python externas;
- resolução formal de toda composição possível de JSON Schema Draft 2020-12;
- descoberta de histórico que não foi fornecido ao validador;
- equivalência lexical perfeita entre YAML e JSON para todas as particularidades do YAML 1.1.

A autoridade final de publicação permanece `GOVERNANCA_EXTERNA`.

## 2. Entradas suportadas

A interface canônica é YAML/JSON lido pelos loaders oficiais da MM01.

A API Python direta aceita o modelo de dados canônico correspondente a JSON/YAML:

- mappings/objetos;
- listas;
- strings;
- booleanos;
- `null`/`None`;
- inteiros Python;
- floats Python finitos.

Tipos numéricos externos, como `Decimal` e escalares NumPy, não fazem parte do domínio programático canônico. Se forem fornecidos diretamente, devem ser recusados deterministicamente; a MM01 não precisa inferir ou adaptar a semântica específica de cada biblioteca.

## 3. R01 — materialidade textual Unicode

`material-text` é a única autoridade de materialidade textual para conteúdo humano/auditável.

Uma string material deve:

1. ser `str`;
2. passar por NFKC;
3. ter caracteres com a propriedade Unicode `Default_Ignorable_Code_Point` removidos antes da decisão de materialidade;
4. conter ao menos uma letra (`L*`) ou número (`N*`) Unicode restante.

Portanto, fillers e caracteres default-ignorable, isoladamente ou repetidos para satisfazer `minLength`, nunca constituem ator, origem, referência, execução ou conteúdo material.

A regra deve preservar texto legítimo latino acentuado, CJK, Devanagari, árabe, grego, cirílico, dígitos Unicode e base + combining mark legítimo.

Não é aceitável manter uma segunda autoridade concorrente baseada em `.strip()`, `\S`, ASCII ou regex textual genérica.

## 4. R02 — equivalência editorial, não equivalência semântica

A MM01 não tenta decidir se duas frases de linguagem natural têm o mesmo significado.

Para o único propósito de impedir que `TRUE`, `FALSE` e `INDETERMINADO` sejam duplicados por maquiagem editorial, a canonicalização deve ser conservadora e previsível:

- NFKC;
- `casefold`;
- remoção de `Default_Ignorable_Code_Point`;
- normalização de whitespace;
- tolerância somente a pontuação terminal editorial explicitamente definida pelo contrato.

A canonicalização deve preservar diferenças potencialmente semânticas, inclusive:

- diacríticos;
- `<`, `>`, `≤`, `≥`;
- `+` e `-`;
- pontuação interna;
- marcas linguísticas capazes de distinguir palavras.

Casos visualmente idênticos que diferem apenas por default-ignorables devem continuar equivalentes, inclusive quando o caractere invisível aparece no início, fim, interior ou em múltiplas posições.

## 5. R03 — números materiais finitos no domínio canônico

`classificacao.limiares[].valor` e `score.componentes[].peso` devem ser números finitos.

No domínio programático canônico:

- qualquer `int` Python é finito e não deve ser convertido para `float` apenas para testar finitude;
- `float` precisa satisfazer `math.isfinite`;
- `NaN` e `±Infinity` devem ser recusados nos caminhos Python/YAML/JSON;
- constantes JSON não finitas continuam proibidas no loader;
- tipos numéricos externos ao domínio canônico devem ser recusados deterministicamente em vez de serem interpretados implicitamente.

Um inteiro JSON/YAML finito maior que o intervalo de `float` não pode derrubar o validador com `OverflowError`.

## 6. R04 — decisão humana é intrinsecamente coerente

`validacao.aprovacao_humana.status` possui significado próprio independentemente da fase.

- `APROVADO` e `REPROVADO` exigem `por`, `em_utc` e `referencia` auditáveis;
- uma decisão humana final não pode coexistir com `validacao.status=PENDENTE` ou `EM_ANALISE`;
- quando `validacao.status` é final, a decisão humana deve coincidir com ele;
- `PENDENTE` não pode carregar metadados que aparentem uma decisão final concluída.

Trocar apenas a string de status nunca pode fabricar aprovação válida.

## 7. R05 — invariantes de proveniência são sempre locais

Qualquer bloco existente que use `$defs.proveniencia` deve ser intrinsecamente válido independentemente da fase.

Em particular:

- `APROVADO` sempre exige bloco `aprovacao` completo e auditável;
- `MEDIDO` sempre exige bloco `medicao` completo e referência de execução material;
- blocos `aprovacao`/`medicao` não podem aparecer sob status incompatível.

A fase serve apenas para dizer **qual status passa a ser obrigatório** naquele momento; ela não suspende a validade interna de um status já declarado.

Isso vale também para a política antecipadamente preenchida de `saida.publicacao.politica_indeterminado`.

## 8. R06 — resultado observado só existe após execução

Conforme ADR-0015, resultados não executados permanecem pendentes.

- `experimentos[].status=EXECUTADO` exige `resultado` material e proveniência `MEDIDO`;
- para `PROPOSTO`, `EM_EXECUCAO` ou `DESCARTADO`, `resultado` deve permanecer `null`;
- se futuramente for necessário registrar resultado esperado, isso exige outro campo/contrato; `resultado` significa resultado observado.

## 9. R07 — snapshot válido e evolução certificada são afirmações distintas

A validação sem histórico prova apenas a consistência interna do snapshot atual.

Ela **não** certifica monotonicidade histórica nem anti-rewind.

A certificação de evolução exige um snapshot anterior confiável fornecido explicitamente por `--previous`. Nesse modo:

- identidade/versionamento são comparados;
- `PUBLICADO` não pode voltar a fase anterior na mesma versão;
- `fase_anterior` precisa refletir o snapshot observado;
- reescrita de histórico na mesma fase/versão é rejeitada.

O CLI não pode usar a mesma mensagem de aprovação para os dois níveis de garantia. Sem `--previous`, deve declarar explicitamente que o snapshot é válido mas o histórico não foi certificado. Com `--previous` e sem problemas, deve declarar aprovação da evolução.

A MM01 não precisa descobrir um snapshot anterior por conta própria; isso anteciparia infraestrutura de outras sprints.

## 10. R08 — perfil canônico de autoria do schema

A MM01 não promete resolver semanticamente toda forma equivalente de JSON Schema.

O schema oficial deve permanecer dentro de um perfil de autoria congelado e exercitado por testes:

- `pattern` somente nos contratos estruturais explicitamente allowlisted;
- nenhum `pattern` textual concorrente com `material-text`;
- `allOf` e `oneOf` não são usados para distribuir constraints materiais;
- `anyOf` é permitido somente nos paths canônicos explicitamente allowlisted;
- nós com `$ref` não podem adicionar silenciosamente `type`, `minLength`, `format` ou `pattern` como constraints irmãs;
- novos formatos de composição exigem revisão explícita desta matriz e dos guards antes de entrar no schema oficial.

O objetivo é preservar o schema realmente mantido pelo projeto sem construir um resolvedor universal de JSON Schema dentro da suíte MM01.

## 11. Requisitos já existentes que continuam bloqueantes

Permanecem obrigatórios todos os requisitos arquiteturais materiais já aceitos para a MM01, incluindo:

- schema Draft 2020-12 e objetos normativos fechados;
- `fase` separada de `condicao`;
- máquina local de fases sem saltos não previstos;
- `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO` e `MEDIDO` distintos;
- silêncio/ausência de evidência não vira `FALSE` sem regra explícita aprovada;
- score 0–100 não implica probabilidade;
- probabilidade exige calibração observada/medida e referência de execução;
- pesos e limiares passam por aprovação quando o gate formal exige;
- referências internas precisam resolver;
- chaves YAML/JSON duplicadas são recusadas;
- fontes permanecem restritas ao binding simbólico autorizado `CATALOGO_PRODUTO` nesta sprint;
- saída publicada permanece BOOLEAN com política explícita para `INDETERMINADO`;
- histórico crescente de runs não é armazenado no YAML;
- workflow MM01 permanece read-only e sem ação corporativa real.

## 12. Não requisitos e backlog

Não bloqueiam o aceite da MM01:

- suporte positivo a `Decimal`, NumPy ou outros tipos numéricos externos;
- prova contra toda composição teoricamente possível de JSON Schema fora do perfil de autoria acima;
- equivalência semântica geral de linguagem natural;
- resolver todo possível code point por blacklist manual — a implementação deve usar a propriedade Unicode assumida em R01/R02;
- coerções lexicais históricas do YAML 1.1 (`010`, `1:20` etc.), registradas como hardening futuro desde que os valores resultantes ainda atravessem o contrato numérico normal;
- descoberta automática de histórico anterior.

Esses itens podem ser registrados em backlog técnico, mas não podem ser promovidos a bloqueio na auditoria final sem alteração explícita desta matriz pelo usuário.

## 13. Gate final objetivo

A MM01 estará tecnicamente apta para o fechamento documental quando, sobre um HEAD congelado:

1. R01–R08 e os requisitos materiais da seção 11 tiverem regressões permanentes verdes;
2. suíte MM01 e CLI passarem em runner limpo;
3. `validate_assistant` passar sem falhas/avisos;
4. workflows permanentes relevantes estiverem verdes em jobs reais;
5. merge-ref, quando usado, for materialmente equivalente ao HEAD ou a diferença for explicada;
6. `behind_by=0` contra a `main` vigente;
7. auditoria final, **restrita a esta matriz**, não demonstrar violação de requisito assumido.

Depois disso ainda permanecem separados: contraditório final, sincronização byte-preserving do bloco MM01 do `CHANGELOG.md`, revalidação da árvore, aceite explícito do usuário e somente então merge.

## 14. Regra de mudança

Esta matriz está congelada para a finalização da MM01.

Qualquer ampliação de requisitos, threat model ou superfície suportada depois deste ponto deve ser tratada como:

- mudança explícita de escopo aprovada pelo usuário; ou
- backlog/sprint posterior.

Uma auditoria não pode alterar implicitamente esta matriz apenas por descobrir um adversarial fora do escopo assumido.