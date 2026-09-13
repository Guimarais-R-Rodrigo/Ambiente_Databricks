# Achados R06 — séries, features e validação temporal

**Data:** 2026-09-12
**Base:** `cae94988cda66a8c61ecebbe6ceed487120a76f2`
**Escopo:** leitura estática de implementação, fachada e notebook dos cinco objetos R06; confronto com documentação primária; runtime será registrado separadamente.

## Achados por objeto

### `arima_wrapper`

1. `train_arima` usa `pmdarima.auto_arima` com `stepwise=True`. `random_state=42` e `n_fits=50` também são passados, mas a documentação do pmdarima associa esses parâmetros à busca aleatória (`random=True`, `stepwise=False`); não devem ser descritos como cinquenta fits aleatórios nem como semente do caminho stepwise atual.
2. `predict(..., return_conf_int=True)` calcula intervalos, mas `conf_int` é descartado; o contrato público retorna apenas previsão pontual.
3. AIC, BIC, RMSE e MAPE retornados são todos derivados da amostra ajustada. Não existe holdout ou backtest dentro do helper.
4. O MAPE exclui pontos cujo target é zero. Se todos os valores forem zero, a média opera sobre conjunto vazio e pode produzir `NaN`.
5. O módulo importa MLflow no topo, logo `log_mlflow=False` não elimina a dependência de import.
6. O notebook histórico afirma que `auto_arima` “já resolve” a diferenciação e que uma ordem selecionada é a “melhor descrição” do processo gerador. A formulação excede o que a busca por critério de informação demonstra.
7. O notebook fixa `pmdarima==2.0.4` e `numpy==1.23.5`; isso é um ambiente histórico explícito. Em 12/09/2026 o PyPI lista pmdarima 2.1.1.

### `lgbm_temporal`

8. Apesar do nome e do catálogo histórico, a implementação atual não importa nem treina LightGBM. A única API pública de negócio é `create_temporal_features`.
9. `entity_cols` é opcional. Portanto a frase histórica de que o helper “exige a coluna de entidade” é falsa; omitir entidade em painel é responsabilidade do chamador e pode gerar contrato incorreto.
10. Com várias linhas na mesma data e sem entidade, a política default `on_duplicate_dates="raise"` recusa a chamada. O notebook histórico que tenta demonstrar o caso “sem entidade” sem `on_duplicate_dates="keep"` não acompanha esse contrato atual e pode falhar antes da demonstração pretendida.
11. `lag_n` conta observações anteriores, não duração de calendário. Série irregular pode ligar datas separadas por intervalos diferentes.
12. A implementação ordena internamente após normalizar datas. A instrução histórica de que o chamador precisa ordenar o painel antes de usar não é mais pré-condição técnica.
13. O print atual fala em “warm-up das features geradas”; blocos históricos do notebook ainda exibem “NaN de lags”. Os outputs serão preservados como evidência histórica, não tratados como transcrição do runtime atual.
14. O helper remove somente warm-up das features temporais geradas; nulos preexistentes em outras colunas sobrevivem.

### `prophet_wrapper`

15. A constante pública `SEED=42` não é usada por `train_prophet`. Ela não fixa o modelo nem a amostragem dos intervalos de incerteza.
16. O módulo importa MLflow no topo, mesmo com `log_mlflow=False`.
17. O wrapper descarta todas as colunas além de data e target; não expõe regressoras adicionais.
18. MAPE, RMSE e MAE são in-sample. MAPE divide diretamente por `y`, sem política para target zero.
19. `make_future_dataframe` inclui histórico por padrão, então `forecast` contém datas usadas no fit + datas futuras.
20. A documentação oficial do Prophet alerta que, em séries semanais/mensais agregadas, feriados que não coincidem com a data representativa da observação são ignorados. Com `freq="MS"`, adicionar feriados BR não significa automaticamente modelar o efeito mensal de Carnaval/Natal/etc.
21. O notebook instala `prophet` sem pin. Em 12/09/2026 o PyPI lista 1.4.0; o repositório oficial declara modo de manutenção a partir dessa versão.
22. As faixas `yhat_lower`/`yhat_upper` dependem do mecanismo de incerteza por amostragem; o wrapper não fixa semente para essa etapa. O próprio notebook já registra que elas podem variar.
23. Frases históricas como “sem dois ciclos completos a sazonalidade anual é chute” são heurísticas úteis, não um cutoff universal da API.

### `split_temporal`

24. Percentuais são aplicados ao número de períodos únicos observados, não ao número de linhas. Bases com volumes desiguais por período podem ter proporções de linhas bem diferentes das porcentagens declaradas.
25. `gap_periods` pula posições na lista de períodos **observados**. Se o calendário tiver buracos, `gap_periods=1` não garante exatamente uma unidade contínua de tempo entre partições.
26. Datas nulas viram `NaT`, ficam fora da lista de períodos e não entram em treino, validação ou teste. O helper não levanta erro nem devolve essas linhas separadamente.
27. `group_col` implementa generalização para entidades inéditas, não uma defesa universal contra leakage. Em painel recorrente pode remover todas as entidades da validação/teste e gerar erro de partição vazia.
28. O resumo histórico “tudo até uma data treina, tudo depois testa” é incompleto: existem três partições, percentuais, dois gaps e uma política opcional de entidade.

### `walk_forward`

29. A função organiza folds e chama `model_fn`; não treina nem retreina modelo por conta própria. O callback é responsável por fit, preprocessing e avaliação sem leakage.
30. Assim como `split_temporal`, `gap`, `test_periods` e `step` avançam sobre períodos observados, não sobre uma grade contínua preenchida.
31. Se não houver períodos suficientes para o primeiro fold, a função pode retornar lista vazia sem erro. Contar folds é parte obrigatória da validação do consumidor.
32. O callback recebe o DataFrame de teste com o target presente. O helper não consegue impedir que uma implementação incorreta use o target de teste durante fit/preprocessing.
33. As chaves `fold`, `train_end`, `test_start`, `n_train` e `n_test` retornadas por `model_fn`, se existirem, são sobrescritas pelos metadados do helper.
34. O resumo impresso deriva as chaves do primeiro fold e usa `np.std` com `ddof=0`; não é intervalo de confiança nem desvio-padrão amostral.

## Achados transversais

35. A R06 reúne três problemas diferentes: gerar features temporais (`lgbm_temporal`), separar/retrotestar (`split_temporal` e `walk_forward`) e ajustar candidatos de forecast (`arima_wrapper` e `prophet_wrapper`). Nenhuma dessas camadas substitui as demais.
36. “Gap” só protege maturação de target se o número configurado corresponder ao atraso real e à semântica de períodos observados da base.
37. Métrica in-sample não deve ser comparada diretamente com métrica de validação temporal como se fossem evidências equivalentes.
38. Os cinco objetos são pandas/driver-side. Os notebooks que partem de Spark precisam limitar/reduzir dados antes de `toPandas`.
39. Nenhum dos cinco objetos agenda retraining, publica modelo, homologa forecast, monitora produção ou garante ausência completa de leakage.

## Decisão da sprint

A R06 tratará esses pontos por documentação, caracterização e correções de prosa/backlinks. **Implementações e fachadas permanecem fora de escopo.** Notebooks terão apenas Markdown corrigido; AST Python, magics executáveis e outputs históricos permanecerão preservados, inclusive quando o output registrar comportamento textual antigo.
