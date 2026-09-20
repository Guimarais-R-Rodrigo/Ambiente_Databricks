"""Byte-level renderer regression; run explicitly in addition to SE07 FULL."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class RendererBytesTests(unittest.TestCase):
    def test_marker_lf_and_copies_are_idempotent(self):
        spec = importlib.util.spec_from_file_location("renderer_bytes", ROOT / "tools/render_simulado.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix="sef_renderer_bytes_") as raw:
            repo = Path(raw).resolve()
            (repo / "tools").mkdir()
            for name in ("render_simulado.py", "project_policy.py"):
                shutil.copyfile(ROOT / "tools" / name, repo / "tools" / name)
            source = repo / "ambiente_fonte"
            (source / ".assistant").mkdir(parents=True)
            copied = b"preserved bytes\r\nsecond line\r\n"
            (source / ".assistant_instructions.md").write_bytes(copied)
            (source / ".assistant/example.txt").write_bytes(copied)
            before = None
            for iteration in range(2):
                with self.subTest(iteration=iteration):
                    p = subprocess.run([sys.executable, "-B", "tools/render_simulado.py", "--write"],
                        cwd=repo, capture_output=True, timeout=15,
                        env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"})
                    self.assertEqual(0, p.returncode, p.stderr)
                    target = repo / "Novo_Ambiente_Simulado"
                    self.assertEqual(repo, target.resolve().parent)
                    marker = (target / "README_GERADO.md").read_bytes()
                    self.assertEqual(module.MARKER.encode("utf-8"), marker)
                    self.assertIn(b"\n", marker)
                    self.assertNotIn(b"\r\n", marker)
                    user = target / "Users" / module.DEFAULT_USERNAME
                    self.assertEqual(copied, (user / ".assistant_instructions.md").read_bytes())
                    self.assertEqual(copied, (user / ".assistant/example.txt").read_bytes())
                    snapshot = {p.relative_to(target).as_posix(): p.read_bytes()
                                for p in target.rglob("*") if p.is_file()}
                    if before is not None:
                        self.assertEqual(before, snapshot)
                    before = snapshot


if __name__ == "__main__":
    unittest.main()
