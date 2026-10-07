"""Run the frozen core cases and require every expected ID to succeed once.

The existing versioned AST fingerprint still owns method semantics. This is a
separate execution guard: ordinary unittest success also permits skips, empty
discovery and load_tests filtering. None counts as full core execution here.
No core methods, assertions or frozen fingerprints are rewritten by this gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stdout
import importlib.util
import json
from pathlib import Path
import sys
import unittest

try:
    from . import package_boundary as boundary
except ImportError:
    import package_boundary as boundary

ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "_maintained_core_tests"


def expected_ids(root: Path) -> set[str]:
    """Derive IDs only after validating their immutable semantic contract."""
    directory = root / "tools/tests/runtime"
    contract = json.loads((directory / "package_contract.json").read_text(encoding="utf-8"),
                          object_pairs_hook=boundary._unique_object)
    manifest = json.loads((directory / "relocation_manifest.json").read_text(encoding="utf-8"),
                          object_pairs_hook=boundary._unique_object)
    fingerprint = boundary.validate_fingerprint(contract, manifest)
    path = root / boundary.CORE_PATH
    cases = boundary.core_cases(path)
    if boundary.core_signature(path) != fingerprint["sha256"]:
        raise ValueError("CORE_CASES_OR_ASSERTIONS_CHANGED")
    ids = {f"{MODULE_NAME}.{cls}.{method}" for cls, methods in cases.items() for method in methods}
    if len(ids) != contract["core_case_count"]:
        raise ValueError("CORE_CASE_COUNT_CHANGED")
    return ids


class ExecutionResult(unittest.TextTestResult):
    """Record callbacks instead of confusing discovery or testsRun with success."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started_ids: list[str] = []
        self.completed_ids: list[str] = []
        self.successful_ids: list[str] = []

    def startTest(self, test):
        self.started_ids.append(test.id())
        super().startTest(test)

    def stopTest(self, test):
        self.completed_ids.append(test.id())
        super().stopTest(test)

    def addSuccess(self, test):
        self.successful_ids.append(test.id())
        super().addSuccess(test)


def run_suite(suite, required_ids: set[str], *, stream=None, verbosity=1) -> dict:
    """Require exact started/completed/successful ID multisets and zero skips."""
    result = unittest.TextTestRunner(stream=stream, verbosity=verbosity,
                                     resultclass=ExecutionResult).run(suite)
    required = Counter({case_id: 1 for case_id in required_ids})
    observed = [Counter(ids) for ids in (result.started_ids, result.completed_ids, result.successful_ids)]
    skipped = [{"id": test.id(), "reason": reason} for test, reason in result.skipped]
    passed = bool(required) and result.wasSuccessful() and not skipped and all(
        counts == required for counts in observed)
    return {
        "status": "PASS" if passed else "FAIL",
        "expected_ids": sorted(required_ids),
        "started_ids": result.started_ids,
        "completed_ids": result.completed_ids,
        "successful_ids": result.successful_ids,
        "missing_ids": sorted(required_ids - set(result.successful_ids)),
        "unexpected_ids": sorted(set().union(*(set(counts) for counts in observed)) - required_ids),
        "duplicate_ids": sorted({case_id for counts in observed for case_id, count in counts.items() if count > 1}),
        "skipped": skipped,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "expected_failures": len(result.expectedFailures),
        "unexpected_successes": len(result.unexpectedSuccesses),
    }


def run_core(root: Path = ROOT, *, stream=None, verbosity=1) -> dict:
    required = expected_ids(root)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, root / boundary.CORE_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("CORE_MODULE_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(MODULE_NAME)
    original_path = sys.path[:]
    try:
        sys.modules[MODULE_NAME] = module
        # Runtime helpers may print diagnostics; reserve CLI stdout for the
        # complete, machine-readable ID report rather than mixing JSON and logs.
        with redirect_stdout(stream if stream is not None else sys.stderr):
            spec.loader.exec_module(module)
            suite = unittest.TestLoader().loadTestsFromModule(module)
            return run_suite(suite, required, stream=stream, verbosity=verbosity)
    finally:
        sys.path[:] = original_path
        if previous is None:
            sys.modules.pop(MODULE_NAME, None)
        else:
            sys.modules[MODULE_NAME] = previous


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="complete checkout or isolated fixture")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = run_core(args.root.resolve(), verbosity=2 if args.verbose else 1)
    except (Exception, SystemExit) as exc:
        report = {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return int(report["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
