"""Compatibility contracts and mutants for deduplicated CI; not remote runs."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import ci_workflows as ci
import yaml


class CIWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="CI DAG with spaces ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / ".github/workflows", self.root / ".github/workflows")
        self.path = self.root / ".github/workflows/ci.yml"

    def test_generated_workflow_exact_and_every_old_check_preserved(self):
        ci.check(self.root)
        fixture = json.loads((TOOLS / "tests/fixtures/ci_recipe_contract.json").read_text())
        active = yaml.safe_load(self.path.read_text())["jobs"]
        for filename, contract in fixture["recipes"].items():
            workflow = yaml.safe_load((self.root / ".github/workflows" / filename).read_text())
            job = workflow["jobs"][contract["job_id"]]
            if contract["job_id"] in {p[0] for p in ci.CAMPAIGNS.values()}:
                job = active[contract["job_id"]]
            self.assertEqual(contract["check_name"], job.get("name", contract["job_id"]))
            for name, value in contract["env"].items():
                self.assertEqual(value, job.get("env", {}).get(name), (filename, name))
            self.assertEqual(contract["runner"], job["runs-on"], filename)
            for expected in contract["setup"]:
                actual = next(step for step in job["steps"] if step.get("uses") == expected["uses"])
                for key, value in expected.get("with", {}).items():
                    if key == "cache-dependency-path":
                        for path in value.splitlines(): self.assertIn(path, actual["with"][key])
                    else:
                        self.assertEqual(value, actual["with"][key], (filename, key))
            commands = [step.get("run") for step in job["steps"]]
            for command in contract["commands"]:
                self.assertIn(command, commands, (filename, command))
            artifacts = [step["with"] for step in job["steps"]
                         if step.get("uses", "").startswith("actions/upload-artifact@")]
            self.assertEqual(contract["artifacts"], artifacts, filename)

    def test_only_distinct_environments_discover_full_suite_automatically(self):
        work = yaml.safe_load(self.path.read_text())["jobs"]
        full = [(name, step["run"]) for name, job in work.items() for step in job["steps"]
                if ci.FULL_SUITE in step.get("run", "")]
        self.assertEqual({"temas-widgets", "temas-widgets-seeded", "temas-widgets-app", "temas-widgets-app-24"}, {name for name, _ in full})
        self.assertEqual(4, len(full))
        self.assertIn("python tools/ci_local.py", [s.get("run") for s in work["validar"]["steps"]])
        kit = yaml.safe_load((self.root / ".github/workflows/kit-transicao-trabalho.yml").read_text())
        text = str(kit)
        self.assertIn("3.11", text)
        self.assertIn("pyspark==4.0.1", text)
        self.assertIn("python tools/ci_local.py --verbose", text)
        self.assertEqual({0,4,5,6,7,8,9,10,11,12,13,14}, set(ci.CAMPAIGNS))
        for number,(check,upstream) in ci.CAMPAIGNS.items():
            expected = ("validar" if number in (0,4) else "temas-widgets" if number == 5
                        else "temas-widgets-seeded" if number < 10 else "temas-widgets-app" if number < 13
                        else "temas-widgets-app-24")
            self.assertEqual(expected,upstream)

    @unittest.skipUnless(shutil.which("bash"), "Linux CI shell is unavailable in this environment")
    def test_failure_cancelled_skipped_unknown_and_missing_never_green(self):
        for _,(_,upstream) in ci.CAMPAIGNS.items():
            gate=ci.failure_gate(upstream)
            for result in ("success", "failure", "cancelled", "skipped", "", "neutral", "unknown"):
                with self.subTest(upstream=upstream,result=result):
                    process=subprocess.run(["bash","-c",gate["run"]],env={**os.environ,"UPSTREAM_RESULT":result})
                    self.assertEqual(result=="success",process.returncode==0)

    def test_missing_dependency_mapping_failure_gate_and_exclusive_mutants(self):
        original=self.path.read_text()
        variants=(
            original.replace("needs:\n    - validar", "needs:\n    - temas-widgets",1),
            original.replace("if: ${{ always() }}", "if: ${{ success() }}",1),
            original.replace('test "$UPSTREAM_RESULT" = success', "echo success",1),
            original.replace("python -B tools/tests/test_temas_v05.py --require-ipywidgets -v", "echo disabled",1),
            original.replace("python -B tools/temas_v10_app.py --verify .artifacts/v10-app", "echo disabled",1),
        )
        for variant in variants:
            self.assertNotEqual(original,variant)
            self.path.write_text(variant)
            with self.assertRaises(ValueError):ci.check(self.root)
        self.path.write_text(original)

    def test_removed_shared_suite_or_optional_job_and_triggers_rejected(self):
        original=self.path.read_text()
        for old,new in (("python tools/ci_local.py","echo removed"),
                        ("codex/temas-v*","codex/only-one-branch"),
                        ("  pull_request: null","  pull_request:\n    paths: ['unrelated/**']")):
            self.path.write_text(original.replace(old,new,1))
            with self.assertRaises(ValueError):ci.check(self.root)
        self.path.write_text(original)
        recipe=self.root/".github/workflows/temas-v04-ci.yml"
        recipe.write_text(recipe.read_text().replace("  workflow_dispatch:","  push:"))
        with self.assertRaises(ValueError):ci.check(self.root)

    def test_permissions_cache_inputs_and_no_success_result_cache(self):
        for path in (self.root/".github/workflows").glob("*.yml"):
            data=yaml.safe_load(path.read_text())
            self.assertEqual({"contents":"read"},data["permissions"],path.name)
            for job in data["jobs"].values():
                self.assertFalse(job.get("continue-on-error",False),path.name)
                for step in job["steps"]:
                    if step.get("uses","").startswith("actions/setup-python@") and step.get("with",{}).get("cache")=="pip":
                        deps=step["with"]["cache-dependency-path"]
                        self.assertIn("tools/requirements-temas-dev.txt",deps)
                    self.assertFalse(step.get("continue-on-error",False),path.name)
                    self.assertNotIn("actions/cache",step.get("uses",""))


if __name__=="__main__": unittest.main()
