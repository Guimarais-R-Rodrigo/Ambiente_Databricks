from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: esperado 1 match, encontrado {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


contract = ROOT / "tools" / "micromodelo_mm01_contract.py"
replace_once(
    contract,
    "import argparse\nimport json\nimport re\nimport unicodedata\n",
    "import argparse\nimport json\nimport math\nimport re\nimport unicodedata\n",
    "import math",
)
replace_once(
    contract,
    '''def load_document(path: str | Path) -> dict[str, Any]:\n    file_path = Path(path)\n    text = file_path.read_text(encoding="utf-8")\n    if file_path.suffix.lower() == ".json":\n        loaded = json.loads(text, object_pairs_hook=_pairs_without_duplicates)\n    else:\n        loaded = _load_yaml_without_duplicate_keys(text)\n''',
    '''def _reject_nonfinite_json_constant(value: str) -> Any:\n    raise ValueError(f"constante JSON não finita recusada: {value}")\n\n\ndef load_document(path: str | Path) -> dict[str, Any]:\n    file_path = Path(path)\n    text = file_path.read_text(encoding="utf-8")\n    if file_path.suffix.lower() == ".json":\n        loaded = json.loads(\n            text,\n            object_pairs_hook=_pairs_without_duplicates,\n            parse_constant=_reject_nonfinite_json_constant,\n        )\n    else:\n        loaded = _load_yaml_without_duplicate_keys(text)\n''',
    "json strict loader",
)
replace_once(
    contract,
    '''    loaded = json.loads(\n        Path(path).read_text(encoding="utf-8"),\n        object_pairs_hook=_pairs_without_duplicates,\n    )\n''',
    '''    loaded = json.loads(\n        Path(path).read_text(encoding="utf-8"),\n        object_pairs_hook=_pairs_without_duplicates,\n        parse_constant=_reject_nonfinite_json_constant,\n    )\n''',
    "schema strict loader",
)
replace_once(
    contract,
    '''def _normalize_semantic_text(value: str) -> str:\n    decomposed = unicodedata.normalize("NFKD", value).casefold()\n    without_accents = "".join(\n        char for char in decomposed if not unicodedata.combining(char)\n    )\n    words_only = re.sub(r"[\\W_]+", " ", without_accents, flags=re.UNICODE)\n    return " ".join(words_only.split())\n''',
    '''def _is_semantic_default_ignorable(char: str) -> bool:\n    codepoint = ord(char)\n    return (\n        unicodedata.category(char) == "Cf"\n        or 0xFE00 <= codepoint <= 0xFE0F\n        or 0xE0100 <= codepoint <= 0xE01EF\n    )\n\n\ndef _normalize_semantic_text(value: str) -> str:\n    decomposed = unicodedata.normalize("NFKD", value).casefold()\n    normalized = "".join(\n        char\n        for char in decomposed\n        if not unicodedata.combining(char)\n        and not _is_semantic_default_ignorable(char)\n    )\n    words_only = re.sub(r"[\\W_]+", " ", normalized, flags=re.UNICODE)\n    return " ".join(words_only.split())\n''',
    "semantic default ignorables",
)
replace_once(
    contract,
    '''@MATERIAL_FORMAT_CHECKER.checks("material-text")\ndef _check_material_text_format(value: Any) -> bool:\n    """Implementa no schema a mesma política Unicode usada pelos gates semânticos."""\n    if not isinstance(value, str):\n        return True\n    return _has_material_text(value)\n''',
    '''@MATERIAL_FORMAT_CHECKER.checks("material-text")\ndef _check_material_text_format(value: Any) -> bool:\n    """Implementa no schema a mesma política Unicode usada pelos gates semânticos."""\n    if not isinstance(value, str):\n        return True\n    return _has_material_text(value)\n\n\n@MATERIAL_FORMAT_CHECKER.checks("finite-number")\ndef _check_finite_number_format(value: Any) -> bool:\n    """Recusa NaN e infinitos em números materiais do contrato."""\n    if isinstance(value, bool) or not isinstance(value, (int, float)):\n        return True\n    return math.isfinite(value)\n''',
    "finite number format",
)

schema_path = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
schema = json.loads(schema_path.read_text(encoding="utf-8"))
schema["properties"]["classificacao"]["properties"]["limiares"]["items"]["properties"]["valor"]["format"] = "finite-number"
schema["properties"]["score"]["properties"]["componentes"]["items"]["properties"]["peso"]["format"] = "finite-number"
schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

tests = ROOT / "tools" / "tests" / "test_micromodelo_mm01.py"
replace_once(
    tests,
    '''                if node.get("type") == "string" and "minLength" in node:\n                    if node.get("format") != "material-text":\n                        violations.append(".".join(path))\n''',
    '''                node_type = node.get("type")\n                accepts_string = node_type == "string" or (\n                    isinstance(node_type, list) and "string" in node_type\n                )\n                if accepts_string and "minLength" in node:\n                    if node.get("format") != "material-text":\n                        violations.append(".".join(path))\n''',
    "string type array guard",
)
insert_marker = '''    def test_schema_patterns_are_exact_structural_allowlist(self) -> None:\n'''
new_tests = '''    def test_semantic_equivalence_rejects_default_ignorable_infix(self) -> None:\n        base = self.valid["classificacao"]["semantica"]["quando_indeterminado"]\n        self.assertIn("disponível", base)\n        invisibles = [\n            "\\u200b",\n            "\\u200c",\n            "\\u200d",\n            "\\u2060",\n            "\\u2063",\n            "\\ufe0f",\n            "\\U000e0100",\n        ]\n        for invisible in invisibles:\n            with self.subTest(invisible=hex(ord(invisible))):\n                document = copy.deepcopy(self.valid)\n                disguised = base.replace("disponível", f"dispo{invisible}nível", 1)\n                self.assertEqual(\n                    module._normalize_semantic_text(base),\n                    module._normalize_semantic_text(disguised),\n                )\n                document["classificacao"]["semantica"]["quando_false"] = disguised\n                self.assertIn("AMBIGUOUS_BINARY_SEMANTICS", self.codes(document))\n\n    def test_required_minlength_guard_handles_string_type_arrays(self) -> None:\n        for node_type in (["string"], ["string", "null"]):\n            with self.subTest(node_type=node_type):\n                mutated = copy.deepcopy(self.schema)\n                mutated["$defs"]["synthetic_type_array_escape"] = {\n                    "type": node_type,\n                    "minLength": 3,\n                }\n                self.assertIn(\n                    "$defs.synthetic_type_array_escape",\n                    self._required_minlength_without_material_text(mutated),\n                )\n\n        nested = copy.deepcopy(self.schema)\n        nested["$defs"]["synthetic_nested_escape"] = {\n            "allOf": [{"type": ["string", "null"], "minLength": 3}]\n        }\n        self.assertIn(\n            "$defs.synthetic_nested_escape.allOf.0",\n            self._required_minlength_without_material_text(nested),\n        )\n\n    def test_nonfinite_material_numbers_and_json_constants_are_rejected(self) -> None:\n        values = [float("nan"), float("inf"), float("-inf")]\n        mutations = [\n            (\n                "classificacao.limiares.valor",\n                lambda d, v: d["classificacao"]["limiares"][0].__setitem__("valor", v),\n            ),\n            (\n                "score.componentes.peso",\n                lambda d, v: d["score"]["componentes"][0].__setitem__("peso", v),\n            ),\n        ]\n        for field, mutate in mutations:\n            for value in values:\n                with self.subTest(field=field, value=repr(value)):\n                    document = copy.deepcopy(self.valid)\n                    mutate(document, value)\n                    self.assertIn("SCHEMA", self.codes(document))\n\n        with tempfile.TemporaryDirectory() as tmp:\n            import yaml\n\n            yaml_document = copy.deepcopy(self.valid)\n            yaml_document["classificacao"]["limiares"][0]["valor"] = float("nan")\n            yaml_path = Path(tmp) / "nonfinite.yaml"\n            yaml_path.write_text(\n                yaml.safe_dump(yaml_document, allow_unicode=True, sort_keys=False),\n                encoding="utf-8",\n            )\n            loaded_yaml = module.load_document(yaml_path)\n            self.assertIn("SCHEMA", self.codes(loaded_yaml))\n\n            for token in ("NaN", "Infinity", "-Infinity"):\n                with self.subTest(json_token=token):\n                    json_path = Path(tmp) / "nonfinite.json"\n                    json_path.write_text(f'{{"valor": {token}}}', encoding="utf-8")\n                    with self.assertRaisesRegex(ValueError, "não finita"):\n                        module.load_document(json_path)\n\n'''
replace_once(tests, insert_marker, new_tests + insert_marker, "insert seventh A1 regressions")

root_readme = ROOT / "README.md"
replace_once(
    root_readme,
    "repo (identidade)  : 1428 arquivos varridos no repositório editável/derivado",
    "repo (identidade)  : 1429 arquivos varridos no repositório editável/derivado",
    "root identity metric",
)

print("Correções técnicas da sétima A1 aplicadas.")
