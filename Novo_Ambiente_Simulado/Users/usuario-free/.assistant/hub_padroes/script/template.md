# Template — pasta de script

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Se o seu objeto
> recebe **DataFrame** e devolve dado para o fluxo seguir, ele é snippet e não
> script — veja [`../snippet/template.md`](../snippet/template.md). O que estiver
> em `checar_base_campanha/` é referência de forma, **não biblioteca**.

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

Idêntica à de snippet — README, fachada, implementação e notebook:

```text
hub_scripts/<nome_do_script>/
├── README.md                       # conceito, escolha e uso seguro
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

O checklist é **um só para os seis tipos**, e mora em
[`skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
Ele separa o que um terceiro consegue conferir do que é juízo de quem escreveu, e
tem um bloco específico para script.

A lista abaixo era a antiga, preservada porque um item dela não estava no
canônico — os demais foram absorvidos:

```text
[ ] a função recebe nome de tabela, não DataFrame
[ ] não escreve nada, e a docstring diz isso
[ ] a docstring diz quantas varreduras faz, para quem avalia custo
[ ] o notebook demonstra um caso pass/warn E um caso fail
[ ] __init__.py saiu da ferramenta
[ ] o README da seção lista este script
```

O exemplo preenchido está em
[`checar_base_campanha/checar_base_campanha.py`](checar_base_campanha/checar_base_campanha.py).

## README do objeto

Aplique o [molde de objeto](../readme/template_objeto.md); veja o
[exemplar](checar_base_campanha/README.md). Diferencie efeitos do script e do
notebook demonstrativo. Explique o retorno real de cada script: não imponha
as chaves deste exemplar a todos os utilitários preexistentes.
