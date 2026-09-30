# Execução SER04 — KS de duas amostras independentes

Este é um perfil **candidato local** de uma única comparação bicaudal com
amostras numéricas contínuas, independentes e sem empates. A independência e
seleção i.i.d. são declarações do autor do estudo; o runner não as infere.
O request é fechado e sintético no piloto. O preflight rejeita inteiros cuja conversão
para float64 perca precisão e empates após a conversão, antes do helper.

Execute a partir da raiz publicada da `.assistant`, com Python que tenha
`numpy`, `pandas` e `scipy`:

```text
python skills/hub-ml-validacao-estatistica/scripts/preflight.py --request request.json
python skills/hub-ml-validacao-estatistica/scripts/run.py --request request.json --run-id SER04-EXAMPLE-1 > run.json
python skills/hub-ml-validacao-estatistica/scripts/verify.py --payload run.json --request request.json --run-id SER04-EXAMPLE-1 --expected-statistic 1 --expected-p-value 0.02857142857142857
```

Use arquivos e `run_id` únicos por tentativa para não sobrescrever evidência.
Interrompa a sequência se preflight ou run devolver código diferente de zero.
O runner imprime o payload JSON em stdout; ele **não** cria `run.json` sozinho.
O redirecionamento acima preserva esse payload para o verificador. A CLI de
`verify.py` exige o payload, o request e um oráculo independente; imprime um
JSON com `valid`, `status` e `issues` e retorna código zero somente quando
`valid=true`. Guarde esse output. Ausência de erro ou stdout vazio não prova
verificação. Os valores esperados devem vir de fonte confiável externa ao
payload, nunca do próprio resultado sob teste.

O JSON sintético em `fixtures/ks_separated_request.json` possui
`reference=[1,2,3,4]` e `comparison=[5,6,7,8]`: oráculo independente
`D=1`; sob H0 e oito postos sem empates, apenas duas das
`binomial(8,4)=70` rotulações extremas dão `D=1`, portanto
`p=1/35`. O método do helper é `scipy.stats.ks_2samp` com
`method=auto`; esta fixture pequena usa a rota exata da versão de SciPy
testada localmente. Outros tamanhos não ganham promessa de p exato.

`verify.py::verify` deve receber o request e run_id esperados de fonte
confiável, mais `expected_statistic=1` e `expected_p_value=1/35`.
Não extraia esses argumentos do payload testado. O Receipt prova vínculo
da execução e integridade da release; o oráculo confere o número. O
resultado não contém IC, equivalência, causalidade ou decisão de negócio.
Não persiste arquivo, tabela ou modelo.
