# V09 — testes e evidências

## Estado

Candidata em execução. Este documento registra resultados sem transformar failures em successes.

## Suíte específica

`tools/tests/test_temas_v09.py` cobre inicialmente:

- existência real de todos os caminhos obrigatórios no produto sanitizado;
- metadados fail-closed de transporte, ativação e publicação;
- mutante negativo removendo, um a um, cada caminho obrigatório;
- coerência entre inventário e bloco `theme_contract`;
- integração da guarda ao gerador antes da escrita do ZIP;
- preservação de `schema_version = 2`;
- instrução operacional no checklist;
- workflow permanente read-only.

## Gate V09

O workflow `.github/workflows/temas-v09-ci.yml` executa:

```bash
python -B tools/tests/test_temas_v09.py -v
python -B tools/tests/test_transicao_trabalho.py -v
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/kit_transicao_trabalho.py --output .artifacts/v09-kit
python -B tools/validate_assistant.py --conferir-readme
```

A geração do kit é local ao runner e não usa credenciais Databricks.

## Failures preservados

### `34877035267` — FAILURE de oráculo textual da suíte V09

No head `17a95762b9f6dc19c13cf008ee581bc7c1041d26`, sete dos oito testes V09 passaram. O único failure foi `test_transition_checklist_names_theme_contract`: o checklist registra corretamente a chave real `manual_opt_in`, mas o teste procurava a expressão inexistente `manual/opt-in`. A implementação do contrato não foi alterada para acomodar o teste; o oráculo foi corrigido no commit seguinte. As etapas posteriores foram puladas porque a suíte específica já havia reprovado.

Esse run permanece **FAILURE**.

## Evidência pendente

Os resultados posteriores serão preenchidos a partir dos runs reais da branch. Nenhum resultado é declarado antecipadamente.

## O que PASS não prova

- importação real no workspace corporativo;
- render visual no navegador Databricks;
- acessibilidade ou UAT humano;
- ativação ou promoção de tema;
- permissão/ACL do destino;
- publicação Databricks.
