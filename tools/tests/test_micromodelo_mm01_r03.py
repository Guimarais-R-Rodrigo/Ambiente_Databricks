from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "tools" / "micromodelo_mm01_contract.py"
SCHEMA = REPO / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
FIXTURE = REPO / "tools" / "tests" / "fixtures" / "micromodelos_mm01" / "valido_validado.json"

spec = importlib.util.spec_from_file_location("micromodelo_mm01_contract_r03", CONTRACT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MicromodeloMM01R03RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = module.load_schema(SCHEMA)
        cls.valid = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_numpy_float64_is_rejected_as_external_numeric_type(self) -> None:
        value = np.float64(1.5)
        self.assertFalse(module._check_finite_number_format(value))

        threshold = copy.deepcopy(self.valid)
        threshold["classificacao"]["limiares"][0]["valor"] = value
        threshold_codes = {issue.code for issue in module.validate_spec(threshold, self.schema)}
        self.assertIn("SCHEMA", threshold_codes)

        weight = copy.deepcopy(self.valid)
        weight["score"]["componentes"][0]["peso"] = value
        weight_codes = {issue.code for issue in module.validate_spec(weight, self.schema)}
        self.assertIn("SCHEMA", weight_codes)


if __name__ == "__main__":
    unittest.main()
