# Erros de tema — significado e recuperação

Uma recusa não muda o tema global nem executa outro arquivo. `ThemeError` informa
`code`, `field` e `action`. O campo usa nomes conhecidos do contrato; nomes ou
valores arbitrários recebidos não são repetidos na mensagem.

| Código ou família | Causa | Ação segura |
|---|---|---|
| `JSON_INPUT_TYPE`, `JSON_VALUE_TYPE` | Entrada não é JSON simples | Forneça bytes UTF-8 ou dicionário; não use objetos Python, código ou paths como conteúdo. |
| `JSON_ENCODING`, `JSON_UNICODE` | Codificação inválida ou caractere isolado | Salve como UTF-8 sem BOM; confira a origem do arquivo. |
| `JSON_SYNTAX`, `JSON_DUPLICATE` | Pontuação inválida ou chave repetida | Corrija a cópia; não escolha arbitrariamente qual valor manter. |
| `JSON_SIZE`, `JSON_DEPTH`, `JSON_NODES`, `JSON_CYCLE` | Entrada excede limites ou é circular | Reduza a configuração; não aumente limites para aceitar dados desconhecidos. |
| `JSON_NONFINITE` | NaN/infinito ou número fora da representação finita | Informe um valor finito permitido pelo schema. |
| `SCHEMA_REQUIRED` | Campo obrigatório ausente | Complete o campo indicado; o núcleo não injeta defaults. |
| `SCHEMA_ADDITIONALPROPERTIES` | Campo não permitido | Remova typo, CSS, regra analítica, herança ou alegação de aprovação. |
| `SCHEMA_TYPE`, `SCHEMA_PATTERN`, `SCHEMA_CONST`, `SCHEMA_ENUM` | Tipo, formato ou opção incorretos | Consulte a referência; hexadecimal precisa ser #RRGGBB em maiúsculas. |
| `SCHEMA_MINIMUM`, `SCHEMA_MAXIMUM`, `SCHEMA_MINITEMS`, `SCHEMA_MAXITEMS`, `SCHEMA_MINLENGTH`, `SCHEMA_MAXLENGTH`, `SCHEMA_UNIQUEITEMS` | Valor, quantidade ou repetição fora do contrato | Use limites e opções documentados em TOKENS.md. |
| `ENGINE_VERSION` | Requisito de API incompatível | Use pacote/revisão compatível; não faça fallback silencioso. |
| `CONTEXT_EXPECTED`, `CONTEXT_MISMATCH` | Contexto inválido ou diferente do consumidor | Escolha notebook, readme ou presentation e a configuração correspondente. |
| `PALETTE_CENTER` | Paleta divergente sem centro definido | Use quantidade ímpar de cores. Isso não certifica qualidade perceptual. |
| `COLOR_FORMAT` | Ajuda de autoria recebeu cor ambígua | Use seis dígitos; não use nome, espaço, #RGB ou canal alpha. |
| `PATH_SCOPE`, `PATH_EXTENSION` | Caminho sai do escopo ou não é .json | Escolha raiz local explícita e nome relativo normalizado. |
| `PATH_SYMLINK`, `PATH_REGULAR`, `PATH_MISSING` | Atalho, arquivo especial ou ausente | Peça ao mantenedor o arquivo regular no pacote correto. |
| `PATH_READ`, `PATH_CHANGED` | Falta de permissão ou alteração durante leitura | Confirme acesso e revisão; não exponha a pasta nem desative proteção. |
| `HASH_FORMAT`, `HASH_MISMATCH` | Hash malformado ou revisão diferente | Compare com o recibo correto antes de prosseguir. |
| `RESOURCE_HASH`, `ASSET_HASH`, `ASSET_UNKNOWN` | Pacote ou recurso divergente | Restaure a versão compatível com o mantenedor; não altere hashes para esconder erro. |
| `DEPENDENCY_MISSING` | Validador indisponível | Mantenedor prepara requirements-temas.txt em ambiente autorizado; nada é instalado automaticamente. |
| `RESULT_TYPE`, `RESULT_INTEGRITY` | Objeto de saída incorreto ou adulterado | Gere novo resultado usando resolve_theme/load_theme; não monte a classe manualmente. |
| `SCHEMA_DIALECT`, `SCHEMA_INVALID`, `SCHEMA_REMOTE_REF`, `SCHEMA_LOCAL_REF`, `SCHEMA_NESTED_ID`, `SCHEMA_DYNAMIC_REF`, `SCHEMA_CYCLE` | Defeito do schema/pacote, não de uma escolha visual comum | Encaminhe ao mantenedor; nenhuma referência remota será consultada. |

Esta lista descreve códigos reais; não converte falha em aprovação. Falta de
compreensão do guia e falha de runtime são problemas diferentes e devem ser
registrados separadamente. [Voltar ao primeiro uso](GUIA_OPERACIONAL.md).
