# Concierge — recuperação do protótipo retirado

Para usar ou manter o Concierge, abra a
[versão canônica do produto](../../ambiente_databricks/.assistant/skills/hub-ml-concierge/README.md).
A integração segue o [ADR-0011](../decisions/ADR-0011-concierge-hub.md); descoberta
opcional não executa helpers nem comprova homologação conversacional.

## Retirada autorizada em 07/10/2026

A pasta `novas_funcionalidades/` foi removida da árvore atual: sua implementação
já foi incorporada ao produto. O protótipo não é rota de instalação ou manutenção.
Os registros datados de decisões e auditorias conservam os nomes antigos como
contexto da época; não são caminhos vivos do checkout atual.

O [manifesto original](concierge-manifest.json) permanece intacto e fixa os 19
arquivos, tamanhos e hashes no commit
`126a2e125cca2251527f187a58696243414c6859`. O campo `disposition` descreve a
retenção de 06/10/2026; a situação atual é retirada com recuperação pelo Git.
O README original daquela base também é verificável, inclusive seus bytes
anteriores à adaptação da navegação.

## Conferir recuperação

Na raiz de um clone com histórico completo:

```powershell
python -B tools/verify_concierge_history.py
```

O [verificador](../../tools/verify_concierge_history.py) lê cada blob do commit
fixado, exige todas as identidades do manifesto e compara tamanho e SHA-256.
Não restaura arquivos, importa o protótipo ou consulta a rede. Ausência de histórico
ou divergência reprova: obtenha o histórico completo antes de repetir a prova.
A suíte `test_ai_history.py` protege recuperação, hashes, inventário não vazio,
identidades únicas, paths seguros e rejeição de blob ausente.

Para consultar um arquivo sem recolocar o protótipo na árvore:

```powershell
git show 126a2e125cca2251527f187a58696243414c6859:novas_funcionalidades/README.md
```

Uma reversão integral pode usar o mesmo commit com `git restore --source` somente
para `novas_funcionalidades/`, após conferir conflitos locais e autorizar a reversão.
Exportar somente o produto ou um ZIP sem `.git` não conserva essa recuperabilidade;
use o clone completo para a memória histórica de manutenção.

[Voltar ao histórico](README.md)
