from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / "tools/readme_visuals/theme_bridge.py"
GENERATOR = ROOT / "tools/readme_visuals/theme_assets.mjs"
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
ASSETS_JSON = ASSISTANT / "hub_padroes/identidade_visual/assets.json"
THEME_ID = "hub-legado-editorial"
EPOCH = "1700000000"
OUT_A = ROOT / ".artifacts/v06-tests/a"
OUT_B = ROOT / ".artifacts/v06-tests/b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


class TemasV06Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shutil.rmtree(ROOT / ".artifacts/v06-tests", ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(ROOT / ".artifacts/v06-tests", ignore_errors=True)

    def bridge(self, theme_id=THEME_ID):
        return subprocess.run(
            [sys.executable, str(BRIDGE), "--theme-id", theme_id, "--context", "readme"],
            cwd=ROOT, text=True, capture_output=True,
        )

    def generate(self, out: Path):
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = EPOCH
        env["PYTHON"] = sys.executable
        return subprocess.run(
            ["node", str(GENERATOR), "--theme-id", THEME_ID, "--family", "all", "--output", out.relative_to(ROOT).as_posix()],
            cwd=ROOT, text=True, capture_output=True, env=env,
        )

    def verify(self, out: Path):
        env = os.environ.copy()
        env["PYTHON"] = sys.executable
        return subprocess.run(
            ["node", str(GENERATOR), "--theme-id", THEME_ID, "--output", out.relative_to(ROOT).as_posix(), "--verify"],
            cwd=ROOT, text=True, capture_output=True, env=env,
        )

    def frozen_hashes(self):
        contract = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
        result = {}
        for item in contract["sets"]["editorial-v2-congelado"]:
            path = ASSISTANT / item["path"]
            result[item["path"]] = digest(path)
            self.assertEqual(result[item["path"]], item["sha256"])
        return result

    def test_bridge_is_fail_closed_and_uses_resolved_theme(self):
        ok = self.bridge()
        self.assertEqual(ok.returncode, 0, ok.stderr)
        payload = json.loads(ok.stdout)
        self.assertEqual(payload["derivative_version"], 1)
        self.assertEqual(payload["theme_id"], THEME_ID)
        self.assertEqual(payload["context"], "readme")
        self.assertEqual(payload["asset_set_id"], "editorial-v2-congelado")
        self.assertRegex(payload["fingerprint"], r"^[0-9a-f]{64}$")
        self.assertIn("CONTRATO_VALIDADO_NAO_APROVADO", payload["warnings"])

        unknown = self.bridge("tema-inexistente-v06")
        self.assertNotEqual(unknown.returncode, 0)
        self.assertIn("THEME_ID_UNKNOWN", unknown.stderr)

    def test_generation_is_deterministic_preserves_frozen_bytes_and_verifies(self):
        before = self.frozen_hashes()
        first = self.generate(OUT_A)
        self.assertEqual(first.returncode, 0, first.stderr)
        result = json.loads(first.stdout)
        self.assertEqual(result["status"], "candidate_not_approved")
        self.assertEqual(result["theme_id"], THEME_ID)
        self.assertEqual(result["frozen_assets"], 12)
        self.assertGreater(result["assets"], 0)
        self.assertNotIn("variant_review_required", result["classifications"])
        self.assertGreater(result["classifications"].get("parametric_equivalent", 0), 0)
        self.assertGreater(result["classifications"].get("frozen_approved_signature", 0), 0)

        second = self.generate(OUT_B)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(tree_bytes(OUT_A), tree_bytes(OUT_B))
        self.assertEqual(before, self.frozen_hashes())

        verified = self.verify(OUT_A)
        self.assertEqual(verified.returncode, 0, verified.stderr)
        verification = json.loads(verified.stdout)
        self.assertTrue(verification["verified"])
        self.assertEqual(verification["frozen_assets"], 12)

    def test_verifier_detects_tampering(self):
        generated = self.generate(OUT_A)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        png = next(OUT_A.glob("readmes/*/png/*.png"))
        png.write_bytes(png.read_bytes() + b"tamper")
        checked = self.verify(OUT_A)
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("VERIFY_HASH", checked.stderr)

    def test_output_cannot_target_active_package(self):
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = EPOCH
        env["PYTHON"] = sys.executable
        target = "ambiente_fonte/.assistant/hub_readmes_visual_assets/v06-forbidden"
        run = subprocess.run(
            ["node", str(GENERATOR), "--theme-id", THEME_ID, "--output", target],
            cwd=ROOT, text=True, capture_output=True, env=env,
        )
        self.assertNotEqual(run.returncode, 0)
        self.assertTrue("OUTPUT_SCOPE" in run.stderr or "OUTPUT_ACTIVE_FORBIDDEN" in run.stderr)

    def test_generation_contract_is_mirrored(self):
        src = ASSISTANT / "hub_readmes_visual_assets/specs/theme_generation.yaml"
        sim = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_readmes_visual_assets/specs/theme_generation.yaml"
        self.assertEqual(src.read_bytes(), sim.read_bytes())
        text = src.read_text(encoding="utf-8")
        self.assertIn("ResolvedTheme", text)
        self.assertIn("variant_review_required", text)
        self.assertIn("não publica no Databricks", text)


if __name__ == "__main__":
    unittest.main()
