# Prompt de auditoria A1 — MM01 — contrato canônico de micromodelos

Audite a candidata MM01 da branch `micromodelos/mm01-contrato-canonico`.

Leia primeiro `docs/auditoria/2026-09-14_micromodelos-mm01/01_contexto.md` e obedeça integralmente às fontes permitidas e vedadas ali definidas.

**Não implemente correções. Não altere arquivos. Não faça merge.** Sua função é tentar reproduzir, quebrar e classificar a candidata.

## 1. Identificação obrigatória

Antes de qualquer conclusão, registre:

- repositório;
- branch auditada;
- HEAD exato auditado;
- merge-base com `main`;
- versão de Python usada;
- se as dependências puderam ser instaladas;
- qualquer limitação de ambiente que afete a prova.

Se a branch não existir, não puder ser lida ou não for possível identificar o HEAD, o veredito é `NAO_APTA` por impossibilidade de auditoria reproduzível.

## 2. Execuções mínimas obrigatórias

Em checkout limpo da branch candidata, execute pelo menos:

```bash
python -m pip install -r tools/requirements-dev.txt
python -B -m unittest tools/tests/test_micromodelo_mm01.py -v
python -B tools/validate_assistant.py --root ambiente_fonte
```

Além disso, valide diretamente o template pela CLI da candidata:

```bash
python -B tools/micromodelo_mm01_contract.py \
  docs/sprints/micromodelos/MM01/micromodelo.template.yaml \
  --schema docs/sprints/micromodelos/MM01/micromodelo.schema.json
```

Não considere o fato de testes existentes passarem como prova suficiente. Inspecione se os testes realmente exercitam os requisitos abaixo.

## 3. Critérios arquiteturais que devem ser provados

Audite, no mínimo, os seguintes pontos:

1. **micromodelo continua artefato de domínio**, sem criação de sétimo tipo do Hub e sem criação antecipada da skill `hub-ml-micromodelos`;
2. existe uma especificação canônica estruturada compatível com a decisão de `micromodelo.yaml`;
3. o schema formal é válido Draft 2020-12 e não aceita livremente propriedades desconhecidas em blocos materiais;
4. `fase` e `condicao` não são confundidas;
5. a máquina de fases rejeita saltos inválidos e permite somente rework explicitamente previsto;
6. `PUBLICADO` não pode ser silenciosamente rebobinado na mesma versão material;
7. `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO` e `MEDIDO` têm significado operacional distinto;
8. `APROVADO` exige evidência de decisão humana suficiente para ser auditável;
9. `MEDIDO` exige referência de execução, não apenas um texto afirmando que houve medição;
10. `FALSE` não é equivalente a ausência de evidência e deve ser distinguível de `INDETERMINADO`;
11. a política de ausência de evidência não pode transformar silêncio em `FALSE` sem regra explícita aprovada;
12. score habilitado tem semântica explícita e escala 0–100;
13. score 0–100 não é tratado automaticamente como probabilidade;
14. semântica probabilística exige calibração observada/medida e referência de execução;
15. pesos e limiares materiais não podem avançar como decisão válida sem aprovação humana;
16. fontes são restringidas ao binding simbólico autorizado `CATALOGO_PRODUTO` por padrão e os fixtures não expõem nomes corporativos reais;
17. referências de evidência/contra-evidência não podem apontar silenciosamente para fontes inexistentes;
18. estudo pode preservar `TRUE`, `FALSE` e `INDETERMINADO`;
19. preparação para publicação exige saída final BOOLEAN e política explícita/aprovada para `INDETERMINADO`, sem mapeamento implícito para `FALSE`;
20. a autoridade final de publicação permanece externa ao Hub;
21. o YAML não vira histórico crescente de runs;
22. a candidata não antecipa fingerprint, crawler de catálogo, feature engineering, contrato definitivo de MLflow, visual, migração de legado ou publicação real;
23. nenhum teste/fixture depende de dado real, ACL real, workspace real ou segredo corporativo;
24. o workflow permanente MM01 é read-only e não executa ações corporativas.

## 4. Casos adversariais independentes

Crie seus próprios casos temporários, sem editar arquivos versionados. Eles não podem ser simples cópias dos fixtures negativos existentes.

Exercite pelo menos:

- remoção de um campo obrigatório profundo, não apenas de grupo de topo;
- propriedade desconhecida em bloco material;
- salto de fase não listado;
- tentativa de avançar para `VALIDADO` com decisão humana ausente ou contraditória;
- `quando_false` semanticamente igual a `quando_indeterminado` com diferenças apenas cosméticas, se o validador alegar detectar ambiguidade;
- ausência de evidência configurada para virar `FALSE` sem aprovação;
- limiar/peso `PROPOSTO` em fase que exige aprovação;
- proveniência `MEDIDO` com timestamp mas sem referência de execução;
- score 0–100 descrito como probabilidade sem calibração suficiente;
- calibração marcada como medida mas sem referência executável;
- score desabilitado com resíduos materiais de score;
- referência a fonte não declarada;
- fonte fora de `CATALOGO_PRODUTO`;
- tentativa de `PUBLICADO` sem confirmação externa e sem referência de Product Data;
- contrato de publicação que transforma `INDETERMINADO` em `FALSE` implicitamente;
- uso de YAML com chaves problemáticas `true:`/`false:` para avaliar se existe ambiguidade de parser e se o template canônico evita esse risco.

Para cada adversarial, registre se foi rejeitado, por qual código/erro e se a rejeição ocorreu pelo motivo correto. Uma rejeição por motivo incidental não conta como cobertura do requisito pretendido.

## 5. Testes de consistência cruzada

Compare schema, template, validador e testes entre si. Procure especificamente:

- campos permitidos pelo schema mas ignorados semanticamente pelo validador;
- gates implementados no validador sem representação formal clara no schema;
- fixture positivo que só passa por valores artificiais incompatíveis com o contrato;
- regras documentadas no código que não são exercitadas por teste;
- checks que podem ser burlados por `null`, string vazia, lista vazia, duplicidade de ID, caixa/espaços ou referência circular/órfã;
- divergência entre fase atual, fase anterior e gates esperados;
- aprovação humana que possa ser forjada apenas trocando uma string de status sem os demais campos obrigatórios;
- `MEDIDO` que possa ser forjado sem execução referenciável;
- qualquer caminho que silenciosamente confunda `FALSE`, `INDETERMINADO` e “sem evidência”.

## 6. Classificação dos achados

Use somente estas categorias:

- `QUEBRA`: defeito que impede uso confiável, execução, validação ou preservação de guardrail obrigatório;
- `DIVERGE`: implementação executa, mas contradiz requisito/ADR/contrato aceito;
- `MELHORÁVEL`: melhoria não bloqueante, sem quebra de requisito material.

Não eleve preferência estética ou de nomenclatura a `DIVERGE` sem demonstrar impacto contratual.

## 7. Formato obrigatório da resposta

Entregue **exatamente** nesta estrutura:

```text
# RELATÓRIO DE AUDITORIA A1 — MM01

## 1. Identificação
- Repositório:
- Branch:
- HEAD auditado:
- Merge-base com main:
- Python:
- Limitações de ambiente:

## 2. Execuções reproduzidas
| Execução | Resultado | Evidência objetiva |
|---|---|---|
| ... | PASS/FAIL | ... |

## 3. Casos adversariais independentes
| Caso | Resultado observado | Código/erro | Motivo correto? |
|---|---|---|---|
| ... | ... | ... | SIM/NÃO |

## 4. Achados

### [QUEBRA-01 | DIVERGE-01 | MELHORÁVEL-01] Título objetivo
- Severidade: BLOQUEANTE/NÃO BLOQUEANTE
- Arquivo/trecho:
- Como reproduzir:
- Esperado:
- Observado:
- Impacto:
- Recomendação:

(repita apenas quando houver achado real; se uma categoria estiver vazia, escreva explicitamente “Nenhum achado”.)

## 5. Cobertura dos critérios
| Critério | Status | Evidência |
|---|---|---|
| ... | PASS/FAIL/INCONCLUSIVO | ... |

## 6. Veredito
VEREDITO: APTA | APTA_COM_CORRECOES | NAO_APTA

Bloqueios para aceite:
- ...

Melhorias não bloqueantes:
- ...

Condições para reauditoria:
- ...
```

### Regra do veredito

- `APTA`: nenhuma `QUEBRA`, nenhum `DIVERGE` e nenhuma lacuna material inconclusiva;
- `APTA_COM_CORRECOES`: nenhum defeito que invalide a arquitetura como um todo, mas existe ao menos uma correção material verificável antes do aceite;
- `NAO_APTA`: qualquer `QUEBRA` estrutural, `DIVERGE` material não contornável, ou impossibilidade de reproduzir os gates essenciais.

Não implemente nada depois do veredito. Pare após entregar o relatório.
