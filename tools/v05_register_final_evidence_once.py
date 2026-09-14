"""Registra evidências finais V05 sem alterar produto, links ou métricas do Hub."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs/sprints/sistema_temas/V05/CHECKPOINT_V05.md"
TESTES = ROOT / "docs/sprints/sistema_temas/V05/TESTES.md"
CHANGELOG = ROOT / "CHANGELOG.md"

EXPECTED = {
    CHECKPOINT: "d349664c48282cf1f2d920434dd24b7203475a9a",
    TESTES: "7a87684bd534167fb973797be5265ea2eaad4863",
    CHANGELOG: "10a0768604b3ffbd9654205f955001b6e11a99c9",
}
ALLOWED = {
    "docs/sprints/sistema_temas/V05/CHECKPOINT_V05.md",
    "docs/sprints/sistema_temas/V05/TESTES.md",
    "CHANGELOG.md",
}


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def require_sha() -> None:
    for path, expected in EXPECTED.items():
        if path.is_symlink() or blob_sha(path) != expected:
            raise RuntimeError(f"arquivo mudou antes do registro final: {path}")


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1, encontrado {count}")


def patch_checkpoint() -> None:
    text = CHECKPOINT.read_text(encoding="utf-8")
    old = '''### Próximas ações de fechamento

- completar o inventário de `hub_snippets.visual.theme_lab` no Manual Técnico canônico;
- sincronizar Manual raiz e derivado sem substituir a redação D05/R13;
- atualizar README do Hub, `CLAUDE.md` e índices com o estado V05 candidato;
- registrar a rodada no CHANGELOG, preservando D05 e histórico anterior;
- executar renderer/conferências disponíveis e recalcular as métricas do README somente na árvore final;
- abrir uma nova PR **draft** contra `main`, executar CI geral/permanente e corrigir qualquer falha;
- parar antes de merge e solicitar aceite explícito.
'''
    require_once(text, old, "bloco de próximas ações")
    new = '''### Fechamento técnico e PR final

O Manual canônico, a cópia raiz e o derivado foram sincronizados sem substituir a redação D05/R13. O README do Hub e seu derivado, `CLAUDE.md`, índices e CHANGELOG também foram reconciliados. As métricas do README raiz foram medidas no run `34831939535` e atualizadas sem estimativa manual.

No head limpo `efb9dd3270ac0f5240612cf3b7e9e39111e51c46`, o workflow V05 `34832202757` terminou com **success** em todas as etapas. A PR final **#37** foi aberta em draft contra a `main` `24ffce298ed543755eb15d5d7c553d02ce15e73e`. Os checks disparados pela PR também concluíram com **success**: CI geral `34832408423`, V00 `34832408496`, V01 `34832408407`, V02 `34832408460` e V05 `34832408426`.

Os workflows V03/V04 isolados não foram disparados pela PR porque seus filtros de caminho não abrangem os arquivos V05. Isso não remove suas regressões da bateria: o workflow V05 executa a descoberta `test_temas*.py`, que inclui V01–V05 e passou com 359 casos no head técnico validado.

Após este registro documental, a própria PR deve repetir os checks no novo head. Permanecem como próximas ações somente: confirmar o CI do head documental final, revisar o diff final, manter a PR em draft e parar antes de qualquer merge para aceite explícito. Nenhuma dessas etapas autoriza publicação Databricks ou início da V06.
'''
    CHECKPOINT.write_text(text.replace(old, new), encoding="utf-8")


def patch_testes() -> None:
    text = TESTES.read_text(encoding="utf-8")
    marker = "## Fechamento pós-D05/R13 — 14/09/2026\n"
    require_once(text, marker, "marcador de fechamento pós-D05")
    section = '''## Fechamento técnico pré-registro final — PR #37

No head limpo `efb9dd3270ac0f5240612cf3b7e9e39111e51c46`, o run V05 `34832202757` concluiu com **success** em todas as etapas: 31/31 testes específicos V05, 14/14 testes de sessões, 359/359 regressões `test_temas*.py`, 12/12 regressões visuais V00, validação estrutural/documental e gate de escopo.

A PR final #37 foi aberta em draft contra a `main` pós-D05 `24ffce298ed543755eb15d5d7c553d02ce15e73e`. Os checks iniciais da PR concluíram com **success**:

| Execução | Workflow | Resultado |
|---|---|---|
| 34832408423 | CI local reproduzível | success |
| 34832408496 | Regressões da instrumentação V00 | success |
| 34832408407 | Contrato de temas V01 | success |
| 34832408460 | Núcleo de temas V02 | success |
| 34832408426 | Visual Lab notebook V05 | success |

V03 e V04 possuem workflows com filtros de caminho próprios e não foram disparados por esta PR. Seus testes continuam dentro da regressão `test_temas*.py` executada pelo workflow V05. O run `34831939535`, imediatamente anterior à atualização numérica, mediu as contagens finais do README raiz; a única reprovação naquele head eram as 14 linhas ainda antigas, posteriormente substituídas pelos valores medidos.

Este registro não transforma PASS de GitHub Actions em homologação Databricks. Browser/runtime, frontend de widgets, acessibilidade, p95, ACL real, reinício e UAT continuam fora do alcance automatizado descrito aqui. A alteração documental deste registro requer seus próprios checks no head subsequente da PR.

'''
    TESTES.write_text(text.replace(marker, section + marker), encoding="utf-8")


def patch_changelog() -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    old = "- (Codex) Métricas finais do README, CI geral e PR final ainda dependem da árvore de fechamento; nenhum sucesso é antecipado nesta entrada.\n"
    require_once(text, old, "nota pendente do CHANGELOG")
    new = (
        "- (Codex) As métricas finais do README foram medidas no run `34831939535`; depois da atualização numérica, o head limpo `efb9dd32` obteve `success` no workflow V05 `34832202757`, incluindo validação documental e escopo.\n"
        "- (Codex) A PR #37 foi aberta em draft contra a `main` pós-D05; os checks iniciais da PR concluíram com `success` no CI geral `34832408423`, V00 `34832408496`, V01 `34832408407`, V02 `34832408460` e V05 `34832408426`. O registro final continua sem autorizar merge.\n"
    )
    CHANGELOG.write_text(text.replace(old, new), encoding="utf-8")


def changed_paths() -> set[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    return {line[3:] for line in raw.splitlines()}


def main() -> int:
    require_sha()
    patch_checkpoint()
    patch_testes()
    patch_changelog()
    changed = changed_paths()
    if changed != ALLOWED:
        raise RuntimeError(f"escopo inesperado: {sorted(changed)}")
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("OK: evidências finais registradas somente em CHECKPOINT, TESTES e CHANGELOG.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
