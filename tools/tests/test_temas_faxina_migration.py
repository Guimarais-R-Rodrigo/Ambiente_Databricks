"""The directory migration must not change theme validation semantics."""
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
BASE = "8dd8da57de89122241890b8b6b059fd2f9be25d0"


class MigrationTests(unittest.TestCase):
    def test_schema_only_changes_declared_source_metadata_namespace(self):
        relative = ".assistant/hub_padroes/identidade_visual/theme.schema.json"
        original = subprocess.check_output(["git", "show", f"{BASE}:ambiente_fonte/{relative}"], cwd=ROOT)
        actual = (ROOT / "ambiente_databricks" / relative).read_bytes()
        self.assertEqual(actual, original.replace(b"ambiente_fonte/", b"ambiente_databricks/"))
        from temas_v02_check import tema
        self.assertEqual(hashlib.sha256(actual).hexdigest(), tema._SCHEMA_SHA)

    def test_one_source_and_one_technical_edition(self):
        self.assertTrue((ROOT / "ambiente_databricks/.assistant/MANUAL_TECNICO_V2.md").is_file())
        for old in ("ambiente_fonte", "novas_funcionalidades", "MANUAL_TECNICO.md",
                    "ambiente_databricks/.assistant/MANUAL_TECNICO.md"):
            with self.subTest(old=old):
                self.assertFalse((ROOT / old).exists())


if __name__ == "__main__":
    unittest.main()
