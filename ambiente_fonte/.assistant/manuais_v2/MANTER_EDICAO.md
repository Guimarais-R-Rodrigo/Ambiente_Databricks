# Manutenção desta edição dos manuais

## Qual arquivo editar

Os arquivos `MANUAL_TECNICO_V2.md` e `MANUAL_DO_USUARIO.md`, na raiz de `.assistant`, são as referências publicadas desta edição. A pasta `manuais_v2/partes/` oferece cópias menores para leitura no GitHub. Essas partes são derivadas: uma correção não deve existir somente nelas. Os JSONs de `manuais_v2/mapas/` são mapas técnicos de consulta, com exemplos, campos e vínculos de fonte; não são configurações executáveis nem registros de aprovação de um ambiente.

O `MANUAL_TECNICO.md` anterior permanece disponível. A presença dos dois livros novos não revoga sua autoridade editorial prevista no ADR-0010, promove skills ou homologa o Databricks. Uma adoção operacional diferente requer decisão própria.

## Como atualizar sem criar duas versões divergentes

1. Identifique o contrato ou trecho que mudou e a fonte técnica que sustenta a correção. O código, schema e policy aplicáveis continuam sendo autoridades sobre o comportamento do produto.
2. Corrija primeiro o livro completo correspondente. Preserve os IDs explícitos das seções quando a intenção continuar a mesma; renomeá-los exige revisar todos os links recebidos.
3. Reproduza a correção na parte de leitura indicada pelo índice. Preserve explicações, tabelas e código; adapte somente a navegação relativa ao destino da parte. Se mudar um mapa técnico, atualize seus campos, exemplos, referências e consumidores afetados.
4. Confira os links entre livros, partes, fontes e mapas. Compare chamadas, defaults, retornos, exceções e efeitos com a mesma versão da fonte. Uma revisão por amostra não justifica declarar todo o livro novamente auditado.
5. Registre a revisão da edição e gere novos hashes somente depois de conferir a correspondência. Não altere apenas o manifesto para ocultar uma divergência. Não reescreva um resultado histórico como se fosse uma execução atual.

## Conferência de integridade, sem dependências adicionais

O `MANIFESTO.json` desta pasta identifica cada arquivo entregue por caminho relativo à raiz `.assistant`, tamanho e SHA-256. Ele não inclui o próprio hash, evitando uma referência circular. Execute o Python abaixo com o diretório de trabalho posicionado na `.assistant` que contém os dois livros. O código somente lê arquivos e imprime divergências; não altera conteúdo, instala dependências ou acessa rede.

```python
from pathlib import Path
import hashlib
import json
import sys

root = Path.cwd().resolve()
manifest_path = root / "manuais_v2" / "MANIFESTO.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
failures = []
for item in manifest["files"]:
    path = (root / item["path"]).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        failures.append((item["path"], "caminho fora da raiz"))
        continue
    if not path.is_file():
        failures.append((item["path"], "arquivo ausente"))
        continue
    data = path.read_bytes()
    if len(data) != item["bytes"]:
        failures.append((item["path"], "tamanho diferente"))
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        failures.append((item["path"], "SHA-256 diferente"))
for path, reason in failures:
    print(path, reason)
print("ARQUIVOS_CONFERIDOS", len(manifest["files"]))
print("DIVERGENCIAS", len(failures))
sys.exit(1 if failures else 0)
```

Zero divergências comprova correspondência com os bytes listados no manifesto examinado. Não comprova a origem confiável do manifesto, verdade do conteúdo, qualidade didática, execução dos exemplos ou aprovação de publicação. Para rever a semântica após uma mudança, repita as verificações pertinentes ao trecho alterado e aos seus consumidores.

## Leitura de arquivos grandes

Os dois livros completos preservam o conteúdo integral. Se a prévia do GitHub não renderizar um arquivo grande, use a leitura por partes ou baixe o Markdown completo para um leitor compatível. As partes não são resumos; os índices permitem voltar ao livro e acompanhar a sequência.
