"""Regressões do verificador em cópias temporárias; não são forward tests."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validar_pacote import validate

PACKAGE = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "hub-ml-concierge"
        shutil.copytree(PACKAGE, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    def append(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")

    def matrix(self) -> tuple[Path, dict]:
        path = self.root / "tests/casos_aceite.json"
        return path, json.loads(path.read_text(encoding="utf-8"))

    def test_valid_package(self) -> None:
        self.assertEqual(validate(self.root), [])

    def test_missing_template(self) -> None:
        (self.root / "templates/handoff.md").unlink()
        self.assertTrue(any("obrigatório ausente" in e for e in validate(self.root)))

    def test_extra_frontmatter_field(self) -> None:
        path = self.root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("name: hub-ml-concierge", "name: hub-ml-concierge\npriority: 1"), encoding="utf-8")
        self.assertTrue(any("Campo não permitido" in e for e in validate(self.root)))

    def test_duplicate_frontmatter(self) -> None:
        path = self.root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("name: hub-ml-concierge", "name: hub-ml-concierge\nname: hub-ml-concierge"), encoding="utf-8")
        self.assertTrue(any("duplicado" in e for e in validate(self.root)))

    def test_broken_link(self) -> None:
        self.append("README.md", "\n[Ausente](nao_existe.md)\n")
        self.assertTrue(any("Link quebrado" in e for e in validate(self.root)))

    def test_link_outside_package(self) -> None:
        self.append("README.md", "\n[Fora](../../fora.md)\n")
        self.assertTrue(any("Link fora do pacote" in e for e in validate(self.root)))

    def test_invalid_route(self) -> None:
        path, matrix = self.matrix()
        matrix["cases"][0]["allowed_routes"] = ["INVENTED_ROUTE"]
        path.write_text(json.dumps(matrix), encoding="utf-8")
        self.assertTrue(any("rota de aceite inválida" in e for e in validate(self.root)))

    def test_duplicate_case(self) -> None:
        path, matrix = self.matrix()
        matrix["cases"].append(matrix["cases"][0])
        path.write_text(json.dumps(matrix), encoding="utf-8")
        self.assertTrue(any("id de caso inválido ou duplicado" in e for e in validate(self.root)))

    def test_claimed_human_pass(self) -> None:
        path, matrix = self.matrix()
        matrix["cases"][0]["execution_status"] = "PASS"
        path.write_text(json.dumps(matrix), encoding="utf-8")
        self.assertTrue(any("expectativas não devem carregar resultados" in e for e in validate(self.root)))

    def test_negative_cannot_take_over(self) -> None:
        path, matrix = self.matrix()
        case = next(c for c in matrix["cases"] if c["category"] == "negative")
        case["allowed_routes"] = ["DIRECT_ROUTE"]
        path.write_text(json.dumps(matrix), encoding="utf-8")
        self.assertTrue(any("negativo não pode exigir" in e for e in validate(self.root)))

    def test_python_syntax_error(self) -> None:
        self.append("tests/test_validador.py", "\ndef broken(:\n")
        self.assertTrue(any("Sintaxe Python inválida" in e for e in validate(self.root)))

    def test_symlink_rejected(self) -> None:
        target = Path(self.tmp.name) / "outside.txt"
        target.write_text("outside", encoding="utf-8")
        try:
            (self.root / "outside-link.txt").symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Sistema não permite criar symlink; não é evidência de aprovação.")
        self.assertTrue(any("simbólico não permitido" in e for e in validate(self.root)))

    def test_root_symlink_rejected(self) -> None:
        link = Path(self.tmp.name) / "root-link"
        try:
            link.symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Sistema não permite criar symlink.")
        self.assertIn("Raiz simbólica não permitida.", validate(link))

    def test_positive_activation_must_select(self) -> None:
        path, matrix = self.matrix()
        matrix["cases"][0]["activation"] = "DO_NOT_SELECT"
        path.write_text(json.dumps(matrix), encoding="utf-8")
        self.assertTrue(any("categoria e ativação" in e for e in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
