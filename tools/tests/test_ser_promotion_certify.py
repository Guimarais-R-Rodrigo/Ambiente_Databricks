from __future__ import annotations
import copy, importlib.util, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("promotion",ROOT/"tools/skill_enforcement/ser_promotion_certify.py")
m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)

class PromotionCertifierTests(unittest.TestCase):
    def test_identity_is_distinct(self):
        self.assertEqual("SER-PROMOTION-CERT-1",m.VERSION)
        self.assertEqual("ser01-object-validation-post-promotion",m.PROFILE)
    def test_historical_classifier_accepts_only_exact_temporal_failure(self):
        out="FAIL: test_runtime_resolver (x)\nFAIL: test_current_level_is_evidence_based (x)\n"
        r=m._historical_result("se07",1,out,{"test_runtime_resolver","test_current_level_is_evidence_based"})
        self.assertEqual("EXPECTED_TEMPORAL_FAIL",r["status"])
        r=m._historical_result("se07",1,out+"FAIL: test_other (x)\n",{"test_runtime_resolver","test_current_level_is_evidence_based"})
        self.assertEqual("UNEXPECTED_RESULT",r["status"])
    def test_pre_promotion_tree_is_not_yet_promotion_ready(self):
        r=m._promotion_gate()
        self.assertEqual("FAIL",r["status"])
        self.assertIn("POLICY_LEVEL_NOT_L3",r["issues"])
        self.assertIn("POLICY_STATUS_NOT_IMPLEMENTED",r["issues"])

if __name__=="__main__": unittest.main()
