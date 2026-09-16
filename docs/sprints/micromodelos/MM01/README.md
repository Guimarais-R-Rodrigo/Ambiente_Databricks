# MM01 — Contrato canônico de micromodelos

Status da sprint: **NONA REAUDITORIA FINAL INDEPENDENTE `NAO_APTA` PRESERVADA; D-01/R02 CORRIGIDO; 47 + 3 R02 + 1 R03 TESTES PERMANENTES; RECONCILIAÇÃO COM V13 S2 REALIZADA; CERTIFICAÇÃO FINAL E NOVA REAUDITORIA INDEPENDENTE PENDENTES; NÃO ACEITA; NÃO INTEGRADA**  
Base inicial: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`  
Branch: `micromodelos/mm01-contrato-canonico`  
PR: `#51`

## Objetivo

A MM01 transforma as decisões arquiteturais aceitas na MM00 em um contrato estrutural verificável para cada micromodelo. Ela define o conteúdo mínimo de `micromodelo.yaml`, a máquina de fases, as condições operacionais, a proveniência das afirmações materiais, os gates de validação e a ferramenta de construção/CI que verifica esse contrato.

A MM01 não cria a skill `hub-ml-micromodelos`. O validador vive em `tools/` como oráculo de construção e CI. A skill só pertence à MM04 e, quando existir, deverá derivar o contrato vigente sem criar uma segunda fonte de verdade.

## Autoridade de fechamento

A condição objetiva de término está congelada em:

`docs/sprints/micromodelos/MM01/MATRIZ_ACEITE_FINAL.md`

A matriz define R01–R08, entradas suportadas e não requisitos. Uma auditoria pode criar adversariais novos, mas um caso só pode bloquear se demonstrar violação de requisito já assumido pela matriz ou de ADR aceito. A auditoria não pode ampliar implicitamente o threat model.

## Entregas

- `micromodelo.schema.json`: schema formal Draft 2020-12, versão `1.0.0`;
- `micromodelo.template.yaml`: template inicial válido e sanitizado;
- `CONTRATO_MICROMODELO.md`: semântica dos grupos e regras de preenchimento;
- `ESTADOS_E_PROVENIENCIA.md`: máquina de fases, condições, proveniência e gates;
- `MATRIZ_ACEITE_FINAL.md`: R01–R08 e condição objetiva de término;
- `tools/micromodelo_mm01_contract.py`: validador de referência/CI;
- fixtures sintéticos positivos e negativos em `tools/tests/fixtures/micromodelos_mm01/`;
- `tools/tests/test_micromodelo_mm01.py`: **47 métodos canônicos**;
- `tools/tests/test_micromodelo_mm01_r02.py`: **3 métodos permanentes** para pontuação terminal versus inicial;
- `tools/tests/test_micromodelo_mm01_r03.py`: **1 método permanente** para tipos numéricos externos/NumPy;
- `.github/workflows/micromodelos-mm01-ci.yml`: gate permanente read-only;
- `TESTES.md` e `CHECKPOINT.md`;
- pacote histórico em `docs/auditoria/2026-09-14_micromodelos-mm01/`, sem reclassificação retroativa dos relatórios.

## Como o contrato deve ser entendido

### Fase e condição são dimensões diferentes

A fase analítica segue:

```text
IDEIA
→ EM_DESCOBERTA
→ EM_ESTUDO
→ EM_VALIDACAO
→ VALIDADO
→ CANDIDATO_PRODUTO
→ EM_VALIDACAO_GOVERNANCA
→ PUBLICADO
```

`BLOQUEADO`, `SUSPENSO` e `DEPRECATED` são condições ortogonais. Elas não substituem a máquina de fases.

`fase_anterior` permite verificar a coerência local do snapshot. Sem `--previous`, a CLI certifica somente o snapshot e declara `HISTORICO_NAO_CERTIFICADO`. Com um snapshot anterior confiável fornecido explicitamente, `--previous` também verifica identidade, versão, transição observada e rewind pós-`PUBLICADO` na mesma versão.

### R01 — texto material é Unicode e fail-closed

`material-text` é a autoridade de conteúdo humano/auditável. A regra:

1. exige `str`;
2. aplica NFKC;
3. remove `Default_Ignorable_Code_Point`;
4. exige ao menos uma letra ou número Unicode restante.

Assim, whitespace, zero-width, variation selectors, fillers, pontuação, símbolos e combining marks isolados não fabricam conteúdo material. Texto legítimo latino acentuado, CJK, árabe, grego, cirílico, Devanagari, dígitos Unicode e combining marks acompanhados de base material continuam válidos.

### R02 — equivalência editorial, não equivalência semântica

A MM01 só evita que `TRUE`, `FALSE` e `INDETERMINADO` sejam duplicados por maquiagem editorial. A canonicalização autorizada é conservadora:

- NFKC;
- `casefold`;
- remoção de `Default_Ignorable_Code_Point`;
- normalização de whitespace;
- tolerância somente à pontuação **terminal** explicitamente definida.

Diferenças potencialmente semânticas precisam ser preservadas: diacríticos, `<`, `>`, `≤`, `≥`, `+`, `-`, pontuação interna e pontuação inicial.

Depois da nona reauditoria independente, `_normalize_editorial_text` foi corrigida para remover pontuação apenas à direita:

```python
normalized = normalized.strip()
return normalized.rstrip(_EDITORIAL_EDGE_PUNCTUATION).rstrip()
```

Portanto:

- `resultado?` e `resultado` podem ser equivalentes editorialmente;
- `?resultado` e `resultado` permanecem distintos;
- `…resultado` e `resultado` permanecem distintos, mesmo que NFKC represente a elipse como `...`;
- pontuação interna continua preservada.

A regressão end-to-end garante que pontuação inicial não gere falso `AMBIGUOUS_BINARY_SEMANTICS`.

### `FALSE` não significa ausência de evidência

A classificação possui definições distintas para `quando_true`, `quando_false` e `quando_indeterminado`. A política de ausência de evidência é estruturada por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência. `INDETERMINADO` não pode ser convertido silenciosamente em `FALSE`.

### R03 — domínio numérico canônico é estrito

A API Python direta aceita:

- `int` Python, inclusive arbitrariamente grande;
- `float` Python desde que `math.isfinite` seja verdadeiro.

Recusa deterministicamente:

- `NaN`;
- `+Infinity` e `-Infinity`;
- `Decimal`;
- escalares NumPy;
- outros tipos numéricos externos ao domínio canônico.

A implementação usa identidade estrita de tipo, não `isinstance(value, float)`. A regressão R03 injeta `np.float64` tanto em limiar quanto em peso e exige rejeição por schema.

### R04 — decisão humana final é coerente

`APROVADO` e `REPROVADO` exigem ator, timestamp e referência auditáveis. Uma decisão final não pode coexistir com `validacao.status=PENDENTE` ou `EM_ANALISE`, e o status humano precisa coincidir com o status final da validação.

### R05 — proveniência é válida localmente

Qualquer bloco de proveniência precisa ser intrinsecamente válido independentemente da fase. `APROVADO` exige aprovação completa; `MEDIDO` exige medição completa e referência de execução. Blocos incompatíveis com o status são recusados.

### R06 — resultado observado só existe depois da execução

Experimento não `EXECUTADO` precisa manter `resultado=null` e não pode declarar proveniência `MEDIDO`. `EXECUTADO` exige resultado material e proveniência medida.

### R07 — snapshot não é histórico

Sem `--previous`, a ferramenta certifica somente consistência interna. Com histórico fornecido, também verifica transição, versão e anti-rewind. A MM01 não descobre histórico por conta própria e não antecipa fingerprint/MM02.

### R08 — perfil de autoria do schema é fechado

A MM01 não tenta implementar um resolvedor universal de JSON Schema. O schema oficial segue o perfil de composição revisado e protegido pela suíte: `allOf`/`oneOf` não fazem parte do perfil, `anyOf` é restrito e constraints irmãs de `$ref` são recusadas pelo guard de autoria.

## Score 0–100 não é probabilidade por padrão

`score.tipo_semantica` é a autoridade executável. `FORCA_EVIDENCIA`, `PROBABILIDADE_CALIBRADA` e `OUTRA_APROVADA` são estados estruturados.

Se a semântica for probabilística, o contrato exige calibração medida e `evidencia_ref` resolvida para experimento existente, `EXECUTADO` e `MEDIDO`. A normalização também é estruturada e, em `EM_VALIDACAO+`, precisa estar definida e aprovada.

## Publicação preserva `INDETERMINADO`

A partir de `CANDIDATO_PRODUTO`, o contrato de publicação precisa estar explícito. `indeterminado_vira_false=false` é estrutural. `OUTRA_APROVADA` exige referência auditável.

A autoridade final de publicação continua `GOVERNANCA_EXTERNA`; esta sprint não publica nada no ambiente corporativo.

## Fronteiras de escopo

A MM01 não implementa:

- fingerprint/MM02;
- descoberta, crawler ou binding corporativo/MM03;
- skill `hub-ml-micromodelos` ou novo tipo do Hub/MM04;
- contrato definitivo de MLflow/MM06;
- publicação corporativa real;
- ACL real;
- dado corporativo real;
- migração de legado;
- integração visual própria.

## Histórico de auditoria

As auditorias anteriores permanecem verdadeiras para os SHAs julgados. Nenhum relatório é reclassificado por correções posteriores.

O pacote histórico contém as A1 exploratórias, a matriz final congelada e duas rodadas finais relevantes para o fechamento atual.

### Auditoria final fechada — R03 e `behind_by`

`11_resultado_a1_reauditoria_8.md` julgou `337055d70a28c6d595594fa1e8c351a47615e66b` e concluiu `NAO_APTA_PARA_FECHAMENTO_DOCUMENTAL` por dois bloqueios:

1. R03 aceitava `np.float64` por classificação ampla de subtipo;
2. a branch estava atrasada em relação à `main` vigente.

Ambos foram corrigidos. R03 passou na rodada independente seguinte.

### Nona reauditoria final independente — R02

`12_resultado_a1_reauditoria_9.md` julgou `4dc6bb12d2e4df6c3dbff7aa4711a99bf660bb6b` e concluiu `NAO_APTA` por um único finding:

**D-01 / R02 / DIVERGE / BLOQUEANTE** — pontuação inicial era apagada por `strip(chars)` apesar de a matriz autorizar tolerância somente terminal.

O finding foi aceito como procedente porque deriva diretamente do texto congelado de R02. A correção técnica está em `b6c266924fcbc387f826c08aa4c0f275746fa5bf` e a regressão permanente está em `tools/tests/test_micromodelo_mm01_r02.py`.

A sanitização posterior de metadados no relatório histórico foi necessária pelo gate de higiene do repositório e não altera seu conteúdo técnico ou veredito.

## Reconciliação com a `main`

Durante a rodada corretiva, a `main` avançou pelas integrações V13 S1 e S2. A candidata foi reconciliada por merge real com a base S2 em:

`877a3b9325281de3a276c909cabe6dfed4913b79`

O merge preserva as alterações V13 trazidas pela `main`; a MM01 não reimplementa runtime, preflight ou documentação funcional da frente de Temas.

A sincronização é um gate vivo: imediatamente antes do próximo congelamento será necessário reconfirmar a `main`, merge-base e `behind_by=0`.

## Testes permanentes

O workflow MM01 executa, em Python 3.12:

```bash
python -B -m unittest tools/tests/test_micromodelo_mm01.py -v
python -B -m unittest tools/tests/test_micromodelo_mm01_r02.py -v
python -B -m unittest tools/tests/test_micromodelo_mm01_r03.py -v
python -B tools/validate_assistant.py --root ambiente_fonte
```

São **47 métodos canônicos + 3 R02 + 1 R03 = 51 métodos permanentes**, além de subtests e fixtures negativas.

O run intermediário `35044200964` comprovou os 51 métodos em `CPython 3.12.14`. Ele ainda falhou no gate estrutural exclusivamente por higiene do relatório histórico recém-preservado. Os dois falsos positivos documentais identificados foram corrigidos; a árvore documental final precisa ser recertificada.

## Workflow corretivo temporário

Uma primeira tentativa de automação transitória gerou o run `35043439501`, que encerrou antes de abrir jobs (`jobs=[]`) e não publicou a correção. O mecanismo foi removido. Esse registro é administrativo e não representa falha funcional do contrato.

## Gate de saída

A sequência obrigatória permanece:

1. certificar todos os workflows aplicáveis no SHA final técnico/documental;
2. reconfirmar HEAD, `main`, merge-base, `ahead_by`, `behind_by`, PR e merge-ref;
3. exigir `behind_by=0` e equivalência material HEAD × merge-ref;
4. congelar o SHA candidato;
5. executar **nova reauditoria final independente**, em contexto separado da sessão que implementou a correção;
6. executar contraditório final;
7. somente se a auditoria for limpa, sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte a byte o restante do arquivo;
8. revalidar a árvore exata;
9. obter aceite explícito do usuário;
10. somente então integrar a PR #51.

**MM01 ainda não está aceita nem integrada. MM02 permanece bloqueada.**
