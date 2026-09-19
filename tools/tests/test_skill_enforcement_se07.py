#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ASSISTANT=ROOT/"ambiente_fonte"/".assistant"
POLICY=ASSISTANT/"hub_padroes"/"skill_enforcement"/"policy.json"

def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module); return module

class SE07PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool=_load("se07_policy_test_tool",ROOT/"tools"/"skill_enforcement"/"se07_policy.py")
        cls.runtime=_load("se07_runtime_policy",ASSISTANT/"hub_scripts"/"skill_execution"/"policy.py")
        cls.raw=json.loads(POLICY.read_text(encoding="utf-8")); cls.by={i["skill"]:i for i in cls.raw["skills"]}
    def test_registry_validates_and_covers_catalog(self):
        self.assertEqual([],self.tool.validate_policy_registry(POLICY)); self.assertEqual(14,len(self.tool.discover_skills())); self.assertEqual(self.tool.discover_skills(),set(self.by))
    def test_current_level_is_evidence_based(self):
        self.assertEqual("L4",self.by["hub-ml-eda-profissional"]["current_level"])
        for skill,p in self.by.items():
            if skill!="hub-ml-eda-profissional": self.assertEqual("L0",p["current_level"],skill)
    def test_target_classification(self):
        expected={"hub-ml-analise-safra":"L3","hub-ml-auditoria-skills":"L3","hub-ml-baseline-ml":"L4","hub-ml-comentar-notebook":"L1","hub-ml-concierge":"L1","hub-ml-criar-objeto":"L3","hub-ml-cross-eda-ml":"L4","hub-ml-eda-profissional":"L4","hub-ml-explainability":"L3","hub-ml-feature-engineering":"L4","hub-ml-monitoramento-modelo":"L4","hub-ml-pipeline-builder":"L4","hub-ml-tutor-databricks":"L0","hub-ml-validacao-estatistica":"L3"}
        self.assertEqual(expected,{k:v["target_level"] for k,v in self.by.items()})
    def test_audit_debt_and_ladder(self):
        self.assertEqual({"AUDIT_FALSE_REASSURANCE","AUDIT_STATE_LADDER","AUDIT_CONDITIONAL_APPLICABILITY"},set(self.by["hub-ml-auditoria-skills"]["known_debt"]))
        text=(ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"SKILL.md").read_text(encoding="utf-8")
        for token in ("citado","localizado","lido","importado","chamado","concluído","NOT_OBSERVABLE","get_skill_enforcement_policy","verify_finalized"): self.assertIn(token,text)
    def test_pipeline_authorization(self):
        self.assertIn("authorization",{x["evidence"] for x in self.by["hub-ml-pipeline-builder"]["protected_surfaces"]})
    def test_tutor_remains_l0(self):
        p=self.by["hub-ml-tutor-databricks"]; self.assertEqual(("L0","L0","guidance"),(p["current_level"],p["target_level"],p["rollout_mode"]))
    def test_runtime_resolver(self):
        p=self.runtime.get_skill_enforcement_policy("hub-ml-auditoria-skills",assistant_root=ASSISTANT); self.assertEqual(("L0","L3"),(p.current_level,p.target_level)); self.assertIn("AUDIT_FALSE_REASSURANCE",p.known_debt)
    def test_unknown_fails_closed(self):
        with self.assertRaises(self.runtime.EnforcementPolicyError): self.runtime.get_skill_enforcement_policy("hub-ml-nao-existe",assistant_root=ASSISTANT)
if __name__=="__main__": unittest.main()
