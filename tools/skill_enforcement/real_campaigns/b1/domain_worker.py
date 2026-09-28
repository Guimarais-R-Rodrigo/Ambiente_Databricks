from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT_ROOT = ROOT / "ambiente_fonte/.assistant"
FIXTURES = ROOT / "tools/tests/fixtures/ser_b1"
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_UNAVAILABLE:" + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _digest(value) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def ser03_execute_verify() -> dict:
    skill = ASSISTANT_ROOT / "skills/hub-ml-analise-safra/scripts"
    runner = _load(skill / "run.py", "_b1p2_ser03_runner")
    verifier = _load(skill / "verify.py", "_b1p2_ser03_verifier")
    rows = []
    for filename in ("vf_cumulative.json", "vf_events.json"):
        fixture = _fixture(filename)
        run_id = "B1P2-" + fixture["fixture_id"]
        payload = runner.run(fixture["request"], run_id=run_id)
        if payload.get("status") != "PASS":
            raise RuntimeError("SER03_RUN_NOT_PASS:" + filename)
        verification = verifier.verify(
            payload,
            expected_request=fixture["request"],
            expected_run_id=run_id,
            expected_table=fixture["expected_table"],
        )
        if verification.get("valid") is not True:
            raise RuntimeError("SER03_VERIFY_NOT_VALID:" + filename + ":" + ",".join(verification.get("issues", [])))
        replay = copy.deepcopy(fixture["request"])
        replay["population_id"] = replay["population_id"] + "-replay"
        if verifier.verify(
            payload, expected_request=replay, expected_run_id=run_id,
            expected_table=fixture["expected_table"]
        ).get("valid") is True:
            raise RuntimeError("SER03_REPLAY_ACCEPTED:" + filename)
        tampered = copy.deepcopy(payload)
        tampered["result"]["table"][0]["taxa"] = 0.999999
        if verifier.verify(
            tampered, expected_request=fixture["request"], expected_run_id=run_id,
            expected_table=fixture["expected_table"]
        ).get("valid") is True:
            raise RuntimeError("SER03_TAMPER_ACCEPTED:" + filename)
        rows.append({
            "fixture_id": fixture["fixture_id"],
            "run_id": run_id,
            "request_sha256": _digest(fixture["request"]),
            "result_sha256": _digest(payload["result"]),
            "receipt_present": payload.get("receipt") is not None,
            "verification": "VALID",
            "replay_rejected": True,
            "tamper_rejected": True,
            "promotion_authorized": payload["result"].get("promotion_authorized"),
        })
    return {"status": "PASS", "skill": "hub-ml-analise-safra", "rows": rows, "effect": "NONE"}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "ser03-execute-verify":
        print(json.dumps({"status": "FAIL", "issue": "ACTION_NOT_ALLOWLISTED"}, sort_keys=True))
        return 2
    try:
        result = ser03_execute_verify()
    except Exception as exc:
        result = {"status": "FAIL", "issue": type(exc).__name__ + ":" + str(exc)}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
