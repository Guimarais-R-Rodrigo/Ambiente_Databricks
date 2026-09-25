from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
G6 = Path(__file__).resolve().parent
QUALIFIED_SHA = "08c2a93c4c9dede1e759abe28c07242b4116f47e"
QUALIFIED_TREE = "a2b1b8c805044ff2e1898da3190414afab9140a7"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_UNAVAILABLE:" + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate() -> dict:
    issues = []
    external = _load_json(G6 / "external_manifest.json")
    genie = _load_json(G6 / "genie_manifest.json")
    auth = _load_json(
        ROOT / "docs/sprints/skill_enforcement_rollout/PARALELO/B1/G6/G6_AUTHORIZATION_REQUEST.json"
    )
    catalog = _load_json(
        ROOT / "docs/sprints/skill_enforcement_rollout/PARALELO/catalogos/CASOS.json"
    )
    catalog_rows = {
        row["case_id"]: row for row in catalog["cases"]
        if row.get("case_id") in {
            *(f"VF-G0{i}" for i in range(1, 9)),
            *(f"CE-G0{i}" for i in range(1, 9)),
        }
    }

    if external.get("schema_version") != "SER-B1-G6-EXTERNAL-MANIFEST-1":
        issues.append("EXTERNAL_SCHEMA")
    if external.get("qualified_candidate_sha") != QUALIFIED_SHA or external.get("qualified_candidate_tree") != QUALIFIED_TREE:
        issues.append("EXTERNAL_QUALIFIED_BINDING")
    if external.get("execution_authorized") is not False:
        issues.append("EXTERNAL_PREMATURE_AUTHORIZATION")
    for key in ("policy_change_authorized", "promotion_authorized", "ready_authorized", "merge_authorized"):
        if external.get(key) is not False:
            issues.append("EXTERNAL_AUTHORITY:" + key)
    if external.get("data_policy") != {"synthetic_only": True, "corporate_data_forbidden": True}:
        issues.append("EXTERNAL_DATA_POLICY")
    phases = {row["phase_id"]: row for row in external.get("external_phases", [])}
    if any(row.get("authorized") is not False for row in phases.values()):
        issues.append("EXTERNAL_PHASE_PREAUTHORIZED")
    if phases.get("G6.READ_ONLY_RECONCILE", {}).get("effect") != "NONE":
        issues.append("READ_ONLY_EFFECT")
    if phases.get("G6.PRODUCT_PUBLISH_IF_NEEDED", {}).get("effect") != "REMOTE_PACKAGE_WRITE":
        issues.append("PUBLISH_EFFECT_NOT_EXPLICIT")
    if phases.get("G6.PROBE_IMPORT", {}).get("effect") != "TEMPORARY_WORKSPACE_OBJECT_CREATE":
        issues.append("PROBE_IMPORT_EFFECT_NOT_EXPLICIT")

    if genie.get("schema_version") != "SER-B1-G6-GENIE-MANIFEST-1":
        issues.append("GENIE_SCHEMA")
    if genie.get("execution_authorized") is not False or genie.get("execution_status") != "NOT_RUN":
        issues.append("GENIE_PREMATURE_EXECUTION")
    skills = {row["skill"]: row for row in genie.get("skills", [])}
    expected = {
        "hub-ml-analise-safra": {f"VF-G0{i}" for i in range(1, 9)},
        "hub-ml-cross-eda-ml": {f"CE-G0{i}" for i in range(1, 9)},
    }
    for skill, ids in expected.items():
        row = skills.get(skill) or {}
        if set(row.get("canonical_case_ids", [])) != ids:
            issues.append("GENIE_CASE_SET:" + skill)
        variants = row.get("variants", [])
        if row.get("variant_count") != 10 or len(variants) != 10:
            issues.append("GENIE_VARIANT_COUNT:" + skill)
        g03 = [v for v in variants if v.get("case_id", "").endswith("-G03")]
        if len(g03) != 3:
            issues.append("GENIE_G03_NEIGHBORS:" + skill)
        for item in variants:
            cid = item.get("case_id")
            if item.get("catalog_basis") != catalog_rows.get(cid):
                issues.append("GENIE_CATALOG_BINDING:" + str(cid))
            if item.get("new_chat_required") is not True:
                issues.append("GENIE_CHAT_POLICY:" + str(cid))
            if item.get("expected_effect") != "NONE" or item.get("execution_status") != "NOT_RUN":
                issues.append("GENIE_EFFECT_STATE:" + str(cid))
            ev = item.get("evidence") or {}
            if ev.get("prompt_literal") != item.get("prompt_literal"):
                issues.append("GENIE_PROMPT_EVIDENCE_BINDING:" + str(cid))
            if ev.get("response_literal") is not None or ev.get("evidence_grade") != "NOT_OBSERVABLE" or ev.get("execution_status") != "NOT_RUN":
                issues.append("GENIE_PREPOPULATED_EVIDENCE:" + str(cid))
        auto = next((v for v in variants if v.get("case_id", "").endswith("-G01")), None)
        mention = next((v for v in variants if v.get("case_id", "").endswith("-G02")), None)
        if auto and "@" in auto.get("prompt_literal", ""):
            issues.append("GENIE_AUTOROUTE_HAS_MENTION:" + skill)
        if mention and ("@" + skill) not in mention.get("prompt_literal", ""):
            issues.append("GENIE_MENTION_MISSING:" + skill)

    if auth.get("document_kind") != "AUTHORIZATION_REQUEST_NOT_AUTHORIZATION":
        issues.append("AUTH_DOC_KIND")
    if auth.get("decision") is not None or auth.get("observed_user_authorization_ref") is not None or auth.get("execution_status") != "NOT_RUN":
        issues.append("AUTH_PREMATURE_DECISION")

    vf_cum = _load_json(ROOT / "tools/tests/fixtures/ser_b1/vf_cumulative.json")
    vf_evt = _load_json(ROOT / "tools/tests/fixtures/ser_b1/vf_events.json")
    ce_temp = _load_json(ROOT / "tools/tests/fixtures/ser_b1/ce_l2_temporal.json")
    ce_static = _load_json(ROOT / "tools/tests/fixtures/ser_b1/ce_l2_static.json")

    ser03 = _load_module(G6 / "ser03_free_probe.py", "_g6_validate_ser03")
    ser05 = _load_module(G6 / "ser05_l2_free_probe.py", "_g6_validate_ser05")
    if ser03.SER03_CASES["cumulative"]["request"] != vf_cum["request"] or ser03.SER03_CASES["cumulative"]["expected_table"] != vf_cum["expected_table"]:
        issues.append("SER03_CUMULATIVE_FIXTURE_DRIFT")
    if ser03.SER03_CASES["event"]["request"] != vf_evt["request"] or ser03.SER03_CASES["event"]["expected_table"] != vf_evt["expected_table"]:
        issues.append("SER03_EVENT_FIXTURE_DRIFT")
    if ser05.SER05_CONTEXTS["temporal"] != ce_temp["context"]:
        issues.append("SER05_TEMPORAL_FIXTURE_DRIFT")
    if ser05.SER05_CONTEXTS["static"] != ce_static["context"]:
        issues.append("SER05_STATIC_FIXTURE_DRIFT")

    for path in (G6 / "ser03_free_probe.py", G6 / "ser05_l2_free_probe.py"):
        source = path.read_text(encoding="utf-8")
        ast.parse(source)
        for forbidden in ("workspace import", "saveAsTable", ".write.format(", "dbutils.fs.rm", "dbutils.fs.put"):
            if forbidden in source:
                issues.append("FREE_PROBE_WRITE_SURFACE:" + path.name + ":" + forbidden)

    return {
        "schema_version": "SER-B1-G6-VALIDATION-1",
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "qualified_candidate_sha": QUALIFIED_SHA,
        "genie_case_count": 16,
        "genie_variant_count": sum(row.get("variant_count", 0) for row in genie.get("skills", [])),
        "free_probe_count": len(external.get("free_probes", [])),
        "execution_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    result = validate()
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
