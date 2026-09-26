# `smart_sample` — criar amostras limitadas com opção de preservar estratos

<!-- readme-objeto: 1.0.0 -->

Amostragem reduz volume para exploração, mas o desenho da amostra define quais conclusões continuam válidas. Este helper oferece um modo simples com semente e um modo estratificado que garante presença de cada estrato quando isso é matematicamente possível.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Helper PySpark de amostragem limitada, simples ou estratificada. |
| Para que serve? | Criar recortes menores para prototipação e inspeção controlada. |
| Use quando... | Você aceita trabalhar com amostra e entende se precisa preservar categorias raras. |
| Evite quando... | Precisa de estimativa exata da população ou de uma cota aleatória exatamente `n` no modo simples. |
| Precisa de... | DataFrame, `n > 0`, seed e, opcionalmente, coluna de estratificação. |
| Entrega... | DataFrame Spark com no máximo `n` linhas; no modo estratificado elegível, alvo total de `n`. |

Leia a [implementação](smart_sample.py), a [fachada](__init__.py) e o [notebook](exemplo_smart_sample.py). O helper executa contagens para decidir o caminho, mas não coleta as categorias para o driver.

## 1. O que é?

`smart_sample` reduz um DataFrame Spark. Se a base já tem `<= n` linhas, devolve o próprio DataFrame sem sortear. Se `stratify_col` for omitida, usa `DataFrame.sample` com fração superdimensionada e `limit(n)`.

No modo estratificado, reserva pelo menos uma linha por estrato e distribui as vagas restantes proporcionalmente ao tamanho excedente de cada estrato usando método de maiores restos. Depois sorteia linhas dentro de cada estrato com `F.rand(seed)` e `row_number`.

## 2. Que problema este recurso resolve?

A pergunta é: “Como obter um recorte menor para explorar os dados sem simplesmente pegar as primeiras linhas e, se necessário, sem perder categorias raras?”.

O helper não transforma a amostra em retrato imparcial para qualquer estimativa. Preservar todo estrato altera deliberadamente suas proporções quando estratos raros recebem pelo menos uma linha.

## 3. Quando faz sentido usar?

Use para prototipação, inspeção visual e testes em que o dataset completo é desnecessário. O modo simples é apropriado quando uma amostra aleatória limitada basta.

Use `stratify_col` quando a presença de todas as categorias é mais importante que manter proporções exatas — por exemplo, revisar exemplos de cada canal ou UF antes de uma regra de qualidade.

## 4. Quando não usar?

Não use o modo estratificado para estimar média ou prevalência global sem pesos adequados: estratos pequenos podem ficar superrepresentados.

Não use esperando exatamente `n` linhas no modo simples. A amostra aleatória pode produzir menos que `n`; `limit(n)` é teto, não mecanismo para completar faltantes.

Contraexemplo: estimar a participação real de um segmento raro com uma amostra que força uma linha de cada segmento. O código funciona, mas a proporção observada na amostra deixa de estimar diretamente a proporção da população.

## 5. Como funciona, intuitivamente?

A função começa com `df.limit(n + 1).count()`. Se não houver mais que `n` linhas, encerra e devolve `df`.

Sem estratificação, conta a base completa para calcular `fraction = min(1, 1.2*n/total)`, amostra sem reposição com `seed` e aplica `limit(n)`. A margem de 20% aumenta a chance de alcançar o teto, mas não é garantia matemática.

Com estratificação, conta quantos estratos distintos existem. Se forem mais que `n`, levanta erro. Caso contrário, calcula uma meta inteira por estrato que soma `n`, junta essa meta ao DataFrame e escolhe as primeiras linhas de cada estrato segundo ordenação aleatória com seed.

## 6. Exemplo de situação

Uma base sintética tem 5.020 linhas, sendo apenas 20 de um segmento `XX`. Uma amostra simples de 200 pode não conter `XX`. A estratificada por `uf` garante ao menos uma linha de cada UF desde que o número de UFs seja menor ou igual a 200.

Essa garantia é de **presença**, não de proporção populacional.

## 7. O que você precisa antes de usar?

`n` deve ser positivo. Se `stratify_col` for informado, o nome precisa existir. A função aceita estrato nulo e usa comparação null-safe na junção da alocação.

Antes de estratificar, defina o que a coluna representa e quantos valores distintos pode ter. Coluna de identificador quase único transforma cada linha em estrato e tende a gerar erro ou custo desnecessário.

A seed ajuda a reproduzir o sorteio sob a mesma entrada e plano; ela não é garantia de identidade eterna se partições, versões, dados ou plano mudarem.

## 8. O que este recurso entrega?

Retorna DataFrame Spark com o mesmo schema de entrada. Se a base possui `<= n` linhas, o retorno é o DataFrame original.

No modo simples, a saída tem **no máximo** `n` linhas e pode ter menos. No modo estratificado, quando a entrada tem mais que `n` linhas e o número de estratos não excede `n`, a alocação é construída para totalizar `n` linhas e preservar cada estrato ao menos uma vez.

A função não retorna pesos de amostragem nem relatório de proporções.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.spark.smart_sample import smart_sample

amostra = smart_sample(df, n=1000, seed=42)
revisao_por_uf = smart_sample(df, n=1000, stratify_col="uf", seed=42)
```

O [notebook](exemplo_smart_sample.py) cria uma categoria rara e compara os dois modos. Não persiste tabelas.

## 10. Decisões e configurações que mais importam

`n` é limite de volume. `stratify_col=None` preserva o mecanismo simples; informar uma coluna muda o desenho amostral. `seed=42` controla as expressões aleatórias, mas deve ser registrada junto com versão dos dados quando reprodutibilidade importa.

No modo simples, a margem 1,2 é fixa na implementação. No estratificado, as vagas depois da primeira linha por estrato são distribuídas proporcionalmente a `count - 1`, com desempate pelo hash da chave.

## 11. Limitações, riscos e armadilhas

O modo simples executa uma contagem limitada e, se precisar amostrar, uma contagem completa para obter a fração. O modo estratificado executa contagem de estratos e cria agregações, janela global sobre a tabela de estratos, join e janela por estrato.

A seed não protege contra mudanças de particionamento/plano. A amostra simples pode ter menos de `n`. A estratificada altera proporções e não devolve pesos para desfazer essa distorção.

Estratos de cardinalidade muito alta aumentam shuffle e custo; mais estratos que `n` são recusados explicitamente.

## 12. Quais são as alternativas?

Para apenas ver primeiras linhas, [`safe_display`](../safe_display/README.md) ou `limit` são mais simples e não fingem ser amostra. Para estimativas populacionais, considere desenho amostral e pesos específicos do problema em vez de assumir que esta função basta.

`DataFrame.sample` diretamente é adequado quando você quer controlar a fração e aceita tamanho aleatório.

## 13. Como saber se o resultado faz sentido?

Conte a saída e confirme `<= n`. No modo estratificado, compare os estratos distintos da entrada e da saída; todos devem estar presentes quando o helper não levantou erro e a entrada era maior que `n`.

Compare proporções por estrato antes e depois para visualizar a distorção. Teste duas seeds sobre a mesma base; diferenças são esperadas. Para reproducibilidade relevante, repita também com a mesma versão dos dados e mesma preparação.

## 14. Arquivos relacionados e próximos passos

- [Implementação](smart_sample.py): caminhos simples e estratificado.
- [Fachada](__init__.py): exporta `smart_sample`.
- [Notebook](exemplo_smart_sample.py): categoria rara e comparação dos modos.
- [`safe_display`](../safe_display/README.md): prévia limitada sem desenho amostral.
- [`distribution_grid`](../../display/distribution_grid/README.md): usa amostragem para visualização de distribuições.
- [Coleção](../../README.md): demais snippets Spark.

## 15. Referências

O comportamento foi conferido no código e no notebook desta pasta. As afirmações de tamanho distinguem explicitamente modo simples, estratificado e DataFrame já pequeno para não transformar um resultado histórico de 500 linhas em garantia universal.

A R04-A executa casos sintéticos com Spark no runner e registra skips locais separadamente. Não há inferência de representatividade estatística, benchmark ou homologação Databricks.
