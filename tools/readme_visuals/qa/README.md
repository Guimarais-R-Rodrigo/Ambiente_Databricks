# Metadata e evidência de verificação visual

Conteúdo de manutenção fora do payload Databricks. Nem todo JSON desta pasta
representa execução atual: há metadata corrente e relatórios de campanhas anteriores.

| Entrada | Papel | Atualização |
|---|---|---|
| `figures/` | Medições, textos, dimensões e hashes das figuras | Renderer de produção; alguns predecessores têm preservação e sucessão explícitas |
| `validation.json` | Resultado completo da validação visual | `validate_production.mjs` após gerar/conferir os inputs da revisão escolhida |
| `sprint_*.json` | Relatórios por família/campanha | Conferir revisão e alcance; não transportar PASS histórico ao HEAD |
| `headers/` | Escalas de inspeção e evidência dos cabeçalhos | Receita de cabeçalhos e seus owners históricos |

Da raiz, `node tools/readme_visuals/validate_production.mjs` lê contratos,
confere assets/metadata e grava o relatório QA. `--family` restringe a cobertura;
`--figures-only` não comprova integração nos READMEs. O owner das flags está no
[guia visual](../README.md) e no código do validador.

Antes de retirar ou regenerar conteúdo, confira
[manifesto de realocação](../../tests/runtime/relocation_manifest.json),
[fronteira](../../package_boundary.py) e [sucessor visual](../../tests/runtime/visual_successor.json).
Não edite à mão metadata derivada nem declare resultado observado sem rodar o gate.
Preservação de bytes, QA e aceite visual humano são provas distintas.
