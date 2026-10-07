"""Compile compatibility checks into a single DAG, preserving their identities.

The campaign YAMLs remain runnable manual recipes. Only their equivalent full
suite is shared in the automatic DAG; every exclusive command/environment stays.
--check is read-only; --write refreshes the generated suffix of ci.yml.
"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
MARKER = "  # BEGIN GENERATED CAMPAIGN JOBS: tools/ci_workflows.py\n"
FULL_SUITE = "python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v"
CAMPAIGNS = {
    0: ("testar-v00", "validar"),
    4: ("html-v04", "validar"),
    5: ("visual-lab-v05", "temas-widgets"),
    6: ("assets-v06", "temas-widgets-seeded"),
    7: ("consumidores-v07", "temas-widgets-seeded"),
    8: ("transversal-v08", "temas-widgets-seeded"),
    9: ("kit-temas-v09", "temas-widgets-seeded"),
    10: ("databricks-app-v10", "temas-widgets-app"),
    11: ("aibi-v11", "temas-widgets-app"),
    12: ("homologacao-v12", "temas-widgets-app"),
    13: ("contrato-operacional-v13", "temas-widgets-app-24"),
    14: ("readiness-v14", "temas-widgets-app-24"),
}

# Shared jobs are executable recipes, not bags of command substrings. Keep
# environment dimensions and ordered steps explicit; labels alone are editorial.
APP_REQUIREMENTS = "ambiente_databricks/.assistant/hub_padroes/identidade_visual/databricks_app/requirements.txt"
NODE_INSTALL = "npm install --global pnpm@10.34.5\npnpm --dir tools/readme_visuals install --frozen-lockfile\n"
PREPARE_DERIVED = ("python -B tools/validate_assistant.py --conferir-readme\n"
                   "python -B tools/render_simulado.py --write\n"
                   "python -B tools/render_simulado.py --check\n")
SHARED_PROFILES = {
    # runner, deterministic seed, widgets, App
    "validar": ("ubuntu-latest", None, False, False),
    "temas-widgets": ("ubuntu-latest", None, True, False),
    "temas-widgets-seeded": ("ubuntu-latest", "1700000000", True, False),
    "temas-widgets-app": ("ubuntu-latest", "1700000000", True, True),
    "temas-widgets-app-24": ("ubuntu-24.04", "1700000000", True, True),
}


def shared_contract(key: str) -> dict:
    """The exact executable shape of one maintained shared environment."""
    runner, seed, widgets, app = SHARED_PROFILES[key]
    env = {"PYTHONDONTWRITEBYTECODE": "1"}
    cache_inputs = "tools/requirements-dev.txt\ntools/requirements-temas-dev.txt\n"
    if widgets:
        env["PYTHONUTF8"] = "1"
        cache_inputs += APP_REQUIREMENTS + "\n"
    if seed is not None:
        env["SOURCE_DATE_EPOCH"] = seed
    steps = [
        {"uses": "actions/checkout@v4", "with": {"persist-credentials": False, "fetch-depth": 0}},
        {"uses": "actions/setup-python@v5", "with": {
            "python-version": "3.12", "cache": "pip", "cache-dependency-path": cache_inputs}},
        {"uses": "actions/setup-node@v4", "with": {"node-version": "22"}},
    ]
    install = "python -m pip install -r tools/requirements-dev.txt"
    if widgets:
        steps.append({"run": install + " 'ipywidgets>=8,<9'\n" + NODE_INSTALL})
    else:
        steps.extend([{"run": install}, {"run": NODE_INSTALL}])
    if app:
        steps.append({"run": "python -m pip install -r " + APP_REQUIREMENTS})
    steps.extend([{"run": PREPARE_DERIVED},
                  {"run": FULL_SUITE if widgets else "python tools/ci_local.py"}])
    return {"runs-on": runner, "timeout-minutes": 25, "env": env, "steps": steps}


def check_shared_profile(key: str, job: dict) -> None:
    """Reject missing, repeated, reordered, conditional or masked execution.

    Only names may differ. Exact equality also protects shell, working directory,
    per-step environments and defaults from silently changing the recipe.
    """
    if job.get("name", key) != key:
        raise ValueError(f"SHARED_CHECK_NAME_CHANGED: {key}")
    actual = {field: value for field, value in job.items() if field != "name"}
    steps = job.get("steps")
    if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
        raise ValueError(f"SHARED_STEPS_INVALID: {key}")
    actual["steps"] = [{field: value for field, value in step.items() if field != "name"}
                       for step in steps]
    if actual != shared_contract(key):
        raise ValueError(f"SHARED_EXECUTION_CONTRACT_CHANGED: {key}")


def failure_gate(upstream: str) -> dict:
    return {
        "name": "Exigir sucesso da suíte cumulativa correspondente",
        "shell": "bash",
        "env": {"UPSTREAM_RESULT": "${{ needs." + upstream + ".result }}"},
        "run": 'test "$UPSTREAM_RESULT" = success',
    }


def compiled_jobs(root: Path) -> dict:
    jobs = {}
    for campaign, (job_id, upstream) in CAMPAIGNS.items():
        path = root / f".github/workflows/temas-v{campaign:02d}-ci.yml"
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        job = copy.deepcopy(workflow["jobs"][job_id])
        if job.get("name", job_id) != job_id:
            raise ValueError(f"check name changed: {job_id}")
        job["name"] = job_id
        job["needs"] = [upstream]
        job["if"] = "${{ always() }}"
        steps = []
        removed = 0
        for step in job["steps"]:
            command = step.get("run", "")
            if command in (FULL_SUITE, "python -B tools/ci_local.py --verbose"):
                removed += 1
                continue
            steps.append(step)
        if removed != 1:
            raise ValueError(f"expected exactly one cumulative recipe in {path.name}; got {removed}")
        job["steps"] = [failure_gate(upstream), *steps]
        jobs[job_id] = job
    return jobs


def render(root: Path) -> str:
    path = root / ".github/workflows/ci.yml"
    prefix = path.read_text(encoding="utf-8").split(MARKER)[0].rstrip() + "\n\n"
    generated = yaml.safe_dump({"jobs": compiled_jobs(root)}, sort_keys=False,
                              allow_unicode=True, width=1000).split("\n", 1)[1]
    return prefix + MARKER + generated


def check(root: Path) -> None:
    path = root / ".github/workflows/ci.yml"
    if path.read_text(encoding="utf-8") != render(root):
        raise ValueError("CI_DAG_DRIFT: regenerate with python tools/ci_workflows.py --write")
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    if "defaults" in workflow or "env" in workflow:
        raise ValueError("SHARED_WORKFLOW_EXECUTION_OVERRIDE")
    # PyYAML's YAML 1.1 loader treats 'on' as True; do not rewrite event keys.
    events = workflow.get("on", workflow.get(True, {}))
    if "pull_request" not in events or events["pull_request"] is not None:
        raise ValueError("COMMON_PR_FILTERED")
    if events.get("push", {}).get("branches") != ["main", "codex/temas-v*"]:
        raise ValueError("COMMON_BRANCH_COVERAGE")
    jobs = workflow["jobs"]
    for key in SHARED_PROFILES:
        check_shared_profile(key, jobs[key])
    for campaign, (job_id, upstream) in CAMPAIGNS.items():
        job = jobs[job_id]
        if job.get("needs") != [upstream] or job.get("if") != "${{ always() }}":
            raise ValueError(f"MISSING_FAIL_CLOSED_DEPENDENCY: {job_id}")
        if job["steps"][0] != failure_gate(upstream):
            raise ValueError(f"FAILURE_PROPAGATION_CHANGED: {job_id}")
        shared = jobs[upstream]
        if job["runs-on"] != shared["runs-on"]:
            raise ValueError(f"RUNNER_PROFILE_MISMATCH: {job_id}")
        if job.get("env", {}).get("SOURCE_DATE_EPOCH") != shared.get("env", {}).get("SOURCE_DATE_EPOCH"):
            raise ValueError(f"SEED_PROFILE_MISMATCH: {job_id}")
        recipe = yaml.safe_load((root / f".github/workflows/temas-v{campaign:02d}-ci.yml").read_text())
        if recipe.get("on", recipe.get(True)) != {"workflow_dispatch": None}:
            raise ValueError(f"DUPLICATED_AUTOMATIC_TRIGGER: {job_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            (ROOT / ".github/workflows/ci.yml").write_text(render(ROOT), encoding="utf-8", newline="\n")
        check(ROOT)
    except (ValueError, KeyError) as exc:
        print(f"FAIL {exc}")
        return 1
    print("OK: same check names, exclusive recipes and fail-closed DAG dependencies")
    return 0


if __name__ == "__main__":
    sys.exit(main())
