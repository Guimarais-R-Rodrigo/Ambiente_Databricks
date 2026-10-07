"""Validação estática do pacote integrado; não certifica Genie Code nem executa helpers."""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

NAME = "hub-ml-concierge"
ROUTES = {"DIRECT_ROUTE", "HELPER_ROUTE", "COMPOSITE_ROUTE", "BRIEFING_FIRST", "GAP", "ACCESS_BLOCKED"}
REQUIRED = (
    "SKILL.md", "README.md", "templates/recomendacao.md", "templates/handoff.md",
    "templates/registro_busca.md", "references/descoberta.md", "references/composicao.md",
    "references/exemplos.md", "docs/arquitetura_e_decisao.md",
    "docs/instalacao_testes_promocao.md", "docs/fontes.md", "tests/README.md",
    "tests/casos_aceite.json", "tests/RESULTADOS.md", "tests/test_validador.py",
    "tests/validar_pacote.py",
)
SECTIONS = (
    "## Quando esta skill se aplica", "## Fluxo", "## Usar helpers da biblioteca",
    "## O que nunca fazer", "## Formato de saída",
)


def validate(root: Path) -> list[str]:
    """Leia somente arquivos do pacote e devolva falhas; jamais importe o alvo."""
    if root.is_symlink():
        return ["Raiz simbólica não permitida."]
    root = root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        return ["Raiz do pacote inexistente."]
    if root.name != NAME:
        errors.append("Nome da pasta não corresponde à skill esperada.")
    # Recuse links simbólicos antes de ler: validação não deve escapar do pacote.
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Link simbólico não permitido: {path.relative_to(root)}")
    if errors and any("simbólico" in e for e in errors):
        return errors
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"Arquivo obrigatório ausente: {rel}")
    if not (root / "SKILL.md").is_file():
        return errors
    try:
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return errors + [f"Não foi possível ler SKILL.md: {type(exc).__name__}"]
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill, re.S)
    fields: dict[str, str] = {}
    if not match:
        errors.append("Frontmatter ausente ou inválido.")
    else:
        for line in match.group(1).splitlines():
            if not line or line != line.lstrip() or ": " not in line:
                errors.append("Frontmatter fora do subconjunto escalar de linha única.")
                continue
            key, value = line.split(": ", 1)
            if key not in {"name", "description"} or key in fields:
                errors.append(f"Campo não permitido ou duplicado: {key}")
            if not value.strip() or value[0] in "[{&*!|>'\"" or " #" in value or ": " in value:
                errors.append(f"Escalar vazio ou fora do subconjunto em {key}.")
            fields[key] = value
        if set(fields) != {"name", "description"}:
            errors.append("Frontmatter precisa conter somente name e description.")
        if fields.get("name") != NAME or fields.get("name") != root.name:
            errors.append("Campo name não corresponde ao nome da pasta.")
        if not 1 <= len(fields.get("description", "")) <= 1024:
            errors.append("Descrição fora do limite de 1 a 1024 caracteres.")
    if len(skill.splitlines()) >= 500:
        errors.append("SKILL.md deve ter menos de 500 linhas neste pacote.")
    for section in SECTIONS:
        if section not in skill.splitlines():
            errors.append(f"Seção obrigatória ausente: {section}")
    for route in ROUTES:
        if route not in skill:
            errors.append(f"Rota não documentada em SKILL.md: {route}")

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"Leitura inválida de {path.relative_to(root)}: {type(exc).__name__}")
            continue
        if path.suffix == ".py":
            try:
                ast.parse(text)
            except SyntaxError:
                errors.append(f"Sintaxe Python inválida: {path.relative_to(root)}")
            continue
        # Exemplos cercados por fences não são links navegáveis do documento.
        text = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", text):
            try:
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                destination = (path.parent / unquote(parsed.path)).resolve()
                if not destination.is_relative_to(root):
                    errors.append(f"Link fora do pacote: {path.relative_to(root)} -> {target}")
                elif not destination.exists():
                    errors.append(f"Link quebrado: {path.relative_to(root)} -> {target}")
            except ValueError:
                errors.append(f"Link malformado: {path.relative_to(root)}")

    matrix = root / "tests/casos_aceite.json"
    if matrix.is_file():
        try:
            document = json.loads(matrix.read_text(encoding="utf-8"))
            if not isinstance(document, dict) or document.get("schema_version") != 1:
                raise ValueError("schema_version inválido")
            cases = document.get("cases")
            if not isinstance(cases, list) or not cases:
                raise ValueError("matriz de casos vazia ou inválida")
            ids, categories, covered = set(), set(), set()
            for case in cases:
                if not isinstance(case, dict):
                    raise ValueError("caso precisa ser objeto")
                cid = case.get("id")
                if not isinstance(cid, str) or not re.fullmatch(r"[A-Z][0-9]{2}", cid) or cid in ids:
                    raise ValueError("id de caso inválido ou duplicado")
                ids.add(cid)
                category = case.get("category")
                if category not in {"positive", "negative", "mention", "edge"}:
                    raise ValueError("categoria inválida")
                categories.add(category)
                if case.get("activation") not in {"SELECT", "DO_NOT_SELECT", "PROVIDED_CONTEXT"}:
                    raise ValueError("ativação esperada inválida")
                expected_activation = {"positive": "SELECT", "mention": "SELECT", "negative": "DO_NOT_SELECT", "edge": "PROVIDED_CONTEXT"}[category]
                if case["activation"] != expected_activation:
                    raise ValueError("categoria e ativação esperada divergem")
                if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                    raise ValueError("prompt ausente")
                routes = case.get("allowed_routes")
                if not isinstance(routes, list) or any(not isinstance(r, str) or r not in ROUTES for r in routes):
                    raise ValueError("rota de aceite inválida")
                if category == "negative" and (routes or case["activation"] != "DO_NOT_SELECT"):
                    raise ValueError("negativo não pode exigir roteamento do Concierge")
                if category != "negative" and not routes:
                    raise ValueError("caso de seleção precisa declarar rota")
                covered.update(routes)
                for key in ("expected", "forbidden"):
                    value = case.get(key)
                    if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v.strip() for v in value):
                        raise ValueError(f"critérios inválidos: {key}")
                if case.get("execution_status") != "PENDENTE":
                    raise ValueError("expectativas não devem carregar resultados; registre execução separadamente")
            if categories != {"positive", "negative", "mention", "edge"} or covered != ROUTES:
                raise ValueError("cobertura estrutural insuficiente da matriz")
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            errors.append(f"Matriz de aceite inválida: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    problems = validate(args.root)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print("PASS: estrutura, frontmatter, links locais, sintaxe e matriz de aceite.")
    print("NAO VALIDADO: roteamento, recomendacoes reais, Databricks e permissoes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
