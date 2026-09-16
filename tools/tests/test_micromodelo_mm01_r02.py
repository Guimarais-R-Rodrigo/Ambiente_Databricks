from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "tools" / "micromodelo_mm01_contract.py"
SCHEMA = REPO / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
FIXTURE = REPO / "tools" / "tests" / "fixtures" / "micromodelos_mm01" / "valido_validado.json"

spec = importlib.util.spec_from_file_location("micromodelo_mm01_contract_r02", CONTRACT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MicromodeloMM01R02RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = module.load_schema(SCHEMA)
        cls.valid = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def codes(self, document: dict) -> set[str]:
        return {issue.code for issue in module.validate_spec(document, self.schema)}

    def test_terminal_editorial_punctuation_remains_equivalent(self) -> None:
        self.assertEqual(
            module._normalize_editorial_text("Resultado positivo"),
            module._normalize_editorial_text("  RESULTADO   POSITIVO?!…  "),
        )

        document = copy.deepcopy(self.valid)
        original = document["classificacao"]["semantica"]["quando_true"]
        document["classificacao"]["semantica"]["quando_false"] = (
            f"  {original.upper()}?!…  "
        )
        self.assertIn("AMBIGUOUS_BINARY_SEMANTICS", self.codes(document))

    def test_initial_punctuation_is_not_canonicalized_away(self) -> None:
        base = module._normalize_editorial_text("Resultado positivo")
        self.assertNotEqual(
            base,
            module._normalize_editorial_text("?Resultado positivo"),
        )
        self.assertNotEqual(
            base,
            module._normalize_editorial_text("…Resultado positivo"),
        )
        self.assertEqual(
            "?resultado positivo",
            module._normalize_editorial_text("  ?RESULTADO   POSITIVO  "),
        )
        self.assertEqual(
            "…resultado positivo",
            module._normalize_editorial_text("  …RESULTADO   POSITIVO  "),
        )

    def test_initial_punctuation_does_not_create_false_ambiguity(self) -> None:
        for prefix in ("?", "…"):
            with self.subTest(prefix=prefix):
                document = copy.deepcopy(self.valid)
                original = document["classificacao"]["semantica"]["quando_true"]
                document["classificacao"]["semantica"]["quando_false"] = (
                    f"{prefix}{original}"
                )
                self.assertNotIn(
                    "AMBIGUOUS_BINARY_SEMANTICS",
                    self.codes(document),
                )


if __name__ == "__main__":
    unittest.main()
