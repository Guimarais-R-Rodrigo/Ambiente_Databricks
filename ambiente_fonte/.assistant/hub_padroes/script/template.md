# Template — pasta de script

Um dos seis tipos do Hub. Um script atende uma tarefa explícita de inspeção, transformação ou governança. O exemplo `checar_base_campanha/` ensina forma; não é biblioteca de produção.

## Script ou snippet?

O papel distingue um utilitário de tarefa de uma peça reutilizável de cálculo. A assinatura depende do contrato: um script pode receber nome de tabela, arquivo, conteúdo ou objeto; não imponha DataFrame, nome de tabela ou um dicionário universal como regra. Declare entradas, retorno, permissões, custo, estado e efeitos reais, inclusive escrita quando houver.

## Estrutura da pasta

Idêntica à de snippet — README, fachada, implementação e notebook:

```text
hub_scripts/<nome_do_script>/
├── README.md                       # conceito, escolha e uso seguro
├── __init__.py                     # fachada pública do objeto
├── <nome_do_script>.py
└── exemplo_<nome_do_script>.py
```

Vale tudo que o [template de snippet](../snippet/template.md) exige de docstring,
validação de entrada e resolução de sessão Spark. O que muda é específico:

## Exemplo de saída de diagnóstico

O formato abaixo pertence ao exemplar; não define todas as APIs de scripts.

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

Registre custo de varreduras/coletas, tipos de falha e efeitos. Mostre casos de sucesso e limitação sem fabricar execução. Nunca corrija dados sem autorização explícita.

O exemplo preenchido está em
[`checar_base_campanha/checar_base_campanha.py`](checar_base_campanha/checar_base_campanha.py).

## README do objeto

Aplique o [molde de objeto](../readme/template_objeto.md); veja o
[exemplar](checar_base_campanha/README.md). Diferencie efeitos do script e do
notebook demonstrativo. Explique o retorno real de cada script: não imponha
as chaves deste exemplar a todos os utilitários preexistentes.
