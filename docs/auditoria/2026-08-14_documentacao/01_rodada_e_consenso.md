# Auditoria da documentação — rodada e consenso

Data: 2026-08-14 · Auditor: Claude em sessão sem contexto, com acesso ao sistema
de arquivos e à CLI do Databricks · Nível: **A1**

## Desenho da rodada

Diferente da auditoria da biblioteca, aqui o auditor podia **verificar** em vez
de acreditar: leu o código para conferir afirmações técnicas, contou arquivos no
disco para conferir números, e usou a CLI para comparar a documentação com o que
está publicado no workspace.

Foi instruído a **não** ler `CHANGELOG.md`, `docs/` nem o guia temporário — os
arquivos que contêm o raciocínio de quem escreveu a documentação. A auditoria
seria inútil se o auditor lesse as justificativas antes de julgar o resultado.

Continua sendo A1: mesmo modelo do autor, pontos cegos comuns permanecem.

## Resultado

22 achados, **todos procedentes**. Dez classificados como erro factual, doze como
oportunidade de melhoria. Nenhum foi descartado.

| Categoria | Achados | Situação |
|---|---|---|
| Números desatualizados em blocos de saída | 2 | corrigidos e marcados como voláteis |
| Contradição entre documentos | 3 | corrigidas |
| Afirmação sobre o próprio sistema, falsa ou imprecisa | 3 | corrigidas, uma com mudança de código |
| Links quebrados no ambiente de leitura | 1 | corrigido |
| Diagramas que ensinam errado | 3 | corrigidos |
| Ausências (pré-requisitos, README, verbetes) | 3 | preenchidas |
| Registro, ordem e navegação | 7 | ajustados |

## Os três achados de maior impacto

**A garantia de segurança não cobria onde o risco existe.** O README afirmava que
há verificação automática de identificador corporativo "inclusive em nome de
pasta". A verificação existia e o docstring dela nomeava exatamente esse vetor —
mas rodava só sobre `ambiente_fonte/`, e o lugar onde o vetor se materializa é
`Novo_Ambiente_Simulado/`, que é versionado. Para um leitor de banco, a frase
autorizava commitar confiando numa rede que não estava estendida ali. Corrigido
nos dois lados: a guarda passou a varrer o repositório inteiro, e o texto passou
a descrever a cobertura real.

**Os blocos de saída mentiam e mandavam confiar neles.** Três dos cinco números
do bloco do validador estavam desatualizados, e o texto logo acima dizia "se o
seu retorno divergir, a diferença é o diagnóstico". Um leitor novo concluiria que
seu ambiente está quebrado quando o repositório está aprovado. Pior: o bloco do
`--verify` omitia a primeira linha da saída real, o que revela que ele foi
editado à mão logo abaixo da frase que afirmava o contrário.

**Faltava o pré-requisito sem o qual metade do percurso não roda.** A "Primeira
hora" leva o leitor até publicar e conferir, e nenhum documento dizia que isso
exige CLI instalada e autenticada. A única menção a CLI no arquivo dizia que o
workspace do trabalho não tem — sugerindo o oposto. O analista que não programa
atribuiria a falha a si mesmo e pararia ali, e esse é justamente o perfil que o
material quer alcançar.

## O que o auditor confirmou

Vale registrar, porque delimita o que a correção não precisou tocar. Foram
verificados contra o código e passaram: a semântica de `pit_join` descrita no
glossário; a distinção entre estatística de tabela completa e de amostra em
`quick_profile`; os três exemplos executáveis do guia; os `assert` de
formatação brasileira; as assinaturas de `data_quality_check` e `drift_detector`;
e a consistência interna do JSON de saída documentado, incluindo a aritmética do
score e a data de captura.

A estrutura publicada no workspace corresponde à documentada, com `.py` da
biblioteca como arquivo e notebooks didáticos como notebook.

`x_scripts/README.md` foi o documento que melhor resistiu: nenhuma afirmação
falsa encontrada.

## O que ficou sem verificação

Os números de teste citados na documentação (36/36 do roteamento, 64 de 71 do
runtime) dependem de `docs/testes/`, que estava fora do escopo de leitura por
instrução. Permanecem como estavam. A contradição entre dois documentos sobre
esse número foi corrigida sem depender da fonte, porque se sustentava sozinha.

Afirmações sobre comportamento da plataforma — que o roteamento lê apenas a
`description`, a precedência entre instruções de workspace e de usuário, e o
limite da busca hierárquica — não são verificáveis a partir do repositório.
A terceira foi suavizada no diagrama, que a afirmava como fato.

## Lição para o processo

Esta é a segunda rodada em que uma sessão sem contexto encontra defeito
relevante em material que já havia passado por revisão do autor. Na biblioteca
foram treze; aqui, vinte e dois. As categorias que escapam à autorrevisão se
repetem: número que envelheceu, promessa mais ampla que a implementação, e
pressuposto que o autor tem e o leitor não.

Dar acesso ao sistema de arquivos mudou a natureza dos achados — vários só
existem porque o auditor pôde contar arquivos e abrir código. Vale manter esse
formato nas próximas.
