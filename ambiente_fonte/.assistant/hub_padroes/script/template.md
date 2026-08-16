# Template — pasta de script

Use quando o objeto for **diagnóstico**: algo que se aponta a uma tabela do
workspace e que devolve um veredito legível, tipicamente antes de alguém confiar
naquele objeto.

## Script ou snippet?

A diferença é de papel, não de tamanho, e ela decide a assinatura da função:

| | Snippet | Script |
|---|---|---|
| Papel | peça de cálculo dentro de um fluxo | diagnóstico que roda sozinho |
| Entrada | `DataFrame` | **nome de tabela** (`catalogo.schema.tabela`) |
| Saída | `DataFrame` | dicionário com `status`, `checagens` e `alertas` |
| Quem chama | outro código, ou o notebook do analista | uma pessoa, antes de decidir |

Script recebe nome de tabela porque existe para ser apontado a algo que já está
publicado. Snippet recebe DataFrame porque entra no meio de uma transformação.

## Estrutura da pasta

Idêntica à de snippet — mesmos três arquivos, mesmos nomes:

```text
hub_scripts/<nome_do_script>/
├── __init__.py                     # gerado por tools/api_publica.py
├── <nome_do_script>.py
└── exemplo_<nome_do_script>.py
```

Vale tudo que o [template de snippet](../snippet/template.md) exige de docstring,
validação de entrada e resolução de sessão Spark. O que muda é específico:

## O contrato de saída

```python
{
    "tabela": "catalogo.schema.tabela",
    "status": "pass" | "warn" | "fail",
    "limites": {...},        # a política aplicada, explícita
    "checagens": {...},      # os números crus, para quem quiser recontar
    "alertas": [             # um por problema, nunca uma lista de strings
        {"checagem": "grao", "severidade": "fail", "mensagem": "..."}
    ],
}
```

Quatro regras que o contrato carrega:

1. **`status: "fail"` não significa dado ruim.** Significa que algo precisa de
   decisão humana antes de a medição valer. Diga isso na docstring, porque o
   leitor vai supor o contrário.
2. **A política aparece na saída.** O limite aplicado vai em `limites`, para que
   quem lê o resultado saiba contra o que foi comparado sem abrir o código.
3. **A mensagem do alerta diz o que fazer**, não só o que houve. "`id_cliente`
   não é único: 48.161 linhas para 45.868 chaves. A taxa passa a pesar quem
   aparece mais vezes."
4. **Nunca filtre nem corrija sozinho.** Helper que remove a linha problemática
   produz relatório limpo e conclusão errada.

## Antes de dar por pronto

```text
[ ] a função recebe nome de tabela, não DataFrame
[ ] não escreve nada, e a docstring diz isso
[ ] a docstring diz quantas varreduras faz, para quem avalia custo
[ ] o notebook demonstra um caso pass/warn E um caso fail
[ ] __init__.py saiu da ferramenta
[ ] o README da seção lista este script
```

O exemplo preenchido está em
[`exemplo/checar_base_campanha.py`](exemplo/checar_base_campanha.py).
