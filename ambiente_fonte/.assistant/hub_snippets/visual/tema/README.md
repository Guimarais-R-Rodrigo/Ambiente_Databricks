# `tema` — carregar e validar um tema sem mudar o visual

Use este helper quando outro componente precisar receber uma configuração visual validada. **Ele não aplica cores por conta própria.**

## Em linguagem simples

Pense nele como a portaria do Sistema de Temas. Antes de um gráfico ou cabeçalho usar uma configuração, a portaria confere se o arquivo está no formato permitido, se não há campos desconhecidos, se a versão é compatível e se regras básicas do contrato foram respeitadas.

Se você não escolher tema algum, `resolver_tema(None)` devolve `None`. Isso é intencional: os helpers atuais continuam usando o comportamento antigo até que V03/V04 os adaptem explicitamente.

## API pública

```python
from hub_snippets.visual.tema import carregar_tema, resolver_tema, ErroTema
```

- `carregar_tema(caminho_ou_bytes)`: lê JSON local, valida e devolve `TemaResolvido`.
- `resolver_tema(None)`: preserva a rota legada.
- `resolver_tema(tema_resolvido)`: reutiliza o objeto já validado sem mutar sessão.
- `TemaResolvido.token("brand.primary")`: devolve uma cópia do token solicitado.
- `TemaResolvido.como_dict()`: devolve cópia independente do documento.

## O que é conferido

UTF-8 sem BOM, tamanho máximo, profundidade, chaves duplicadas, NaN/infinito, Unicode inválido, campos/tipos/limites do schema, contexto, asset set, versão do engine, unicidade de paletas e centro ímpar da paleta divergente.

O núcleo usa somente a biblioteca padrão do Python. `jsonschema` continua como dependência de manutenção para testes diferenciais, não como requisito do notebook que apenas importa o helper.

## O que ele não faz

Não busca tema na internet, não interpreta herança, não registra template global, não publica configuração, não verifica permissão do usuário, não aplica CSS, não recolore PNG e não decide se um indicador de negócio é positivo ou negativo.

## Erros

`ErroTema` expõe `codigo`, `campo` e `orientacao`. A mensagem evita incluir o valor recebido. Corrija a proposta; não remova a validação para fazê-la passar.

## Exemplo operacional

Veja `exemplo_tema.py`. Enquanto V05 não existir, o caminho do JSON é informado explicitamente pelo código chamador. Para um usuário não técnico, nenhuma mudança de rotina é exigida nesta sprint.
