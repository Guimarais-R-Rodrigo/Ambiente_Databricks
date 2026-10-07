"""Regressões do kit e do núcleo; --spark habilita somente Spark local sintético."""
from __future__ import annotations
import ast
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import aceite_trabalho as core
import kit_transicao_trabalho as kit
from project_policy import EXPECTED_HUB_DIRS, EXPECTED_SKILL_NAMES

SPARK = "--spark" in sys.argv
if SPARK:
    sys.argv.remove("--spark")
COMMIT = "a" * 40


def manifest(entries=None, **kwargs):
    entries = entries or [{"path": x, "sha256": hashlib.sha256(b"ok").hexdigest(), "bytes": 2,
                         "object_type": "FILE"} for x in
                        (".assistant_instructions.md", ".assistant/README.md", ".assistant/MANUAL_TECNICO_V2.md")]
    data = {"schema_version": 2, "source_commit": COMMIT, "worktree_dirty": False, "files": entries, **kwargs}
    raw = json.dumps(data).encode()
    return raw, hashlib.sha256(raw).hexdigest()


class ManifestTests(unittest.TestCase):
    def check(self, raw, digest):
        return core.validate_manifest(raw, digest, COMMIT)

    def test_good_manifest(self):
        self.assertEqual(len(self.check(*manifest())["files"]), 3)

    def test_reject_digest_mismatch(self):
        raw, _ = manifest()
        with self.assertRaises(core.CheckError): self.check(raw, "0" * 64)

    def test_reject_commit_mismatch(self):
        with self.assertRaises(core.CheckError): self.check(*manifest(source_commit="b" * 40))

    def test_reject_dirty(self):
        with self.assertRaises(core.CheckError): self.check(*manifest(worktree_dirty=True))

    def test_reject_old_schema(self):
        with self.assertRaises(core.CheckError): self.check(*manifest(schema_version=1))

    def test_reject_duplicates(self):
        obj = self.check(*manifest()); obj["files"].append(obj["files"][0])
        with self.assertRaises(core.CheckError): self.check(*manifest(entries=obj["files"]))

    def test_reject_paths_outside_product(self):
        for name in ("../secret", ".assistant/../../secret", "/Users/private", ".assistant/./a",
                     ".assistant//a", ".assistant\\a", "README.md", "C:/secret"):
            with self.subTest(name=name):
                entries = self.check(*manifest())["files"]
                entries[0] = dict(entries[0], path=name)
                with self.assertRaises(core.CheckError): self.check(*manifest(entries))

    def test_reject_unknown_type(self):
        entries = self.check(*manifest())["files"]; entries[0]["object_type"] = "AUTO"
        with self.assertRaises(core.CheckError): self.check(*manifest(entries))

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/".assistant").mkdir(); (root/"other").mkdir()
            link=root/".assistant/x"
            try:
                link.symlink_to(root/"other", target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"filesystem sem symlink de diretório: {exc}")
            with self.assertRaises(core.CheckError): core.safe_payload_path(root, ".assistant/x")

    def test_check_exact_file_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);raw,sha=manifest();(root/"MANIFEST.json").write_bytes(raw)
            for e in json.loads(raw)["files"]:
                p=root/e["path"];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b"ok")
            obj=core.AcceptanceSession(root,root/"MANIFEST.json",sha,COMMIT)
            obj.check_manifest(); obj.check_files()
            (root/".assistant/README.md").write_bytes(b"NO")
            with self.assertRaises(core.CheckError): obj.check_files()

    def test_notebook_bytes_not_claimed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); raw,sha=manifest();entries=json.loads(raw)["files"]
            entries.append(dict(entries[0], path=".assistant/example.py", object_type="NOTEBOOK"))
            raw,sha=manifest(entries);(root/"MANIFEST.json").write_bytes(raw)
            for e in entries[:3]:
                p=root/e["path"];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b"ok")
            obj=core.AcceptanceSession(root,root/"MANIFEST.json",sha,COMMIT)
            obj.check_manifest();obj.check_files()
            self.assertEqual(obj.file_stats["notebooks_sem_hash_remoto"],1)


class VerdictTests(unittest.TestCase):
    def good(self): return {k:{"status":"PASS"} for k in core.CORE_IDS}
    def manual(self): return {k:"CONFIRMADO" for k in core.MANUAL_IDS}
    def test_empty_is_incomplete(self):
        self.assertEqual(core.summarize({}, {}, "final")["veredito"], "INCOMPLETO")
    def test_staging_is_not_activation(self):
        self.assertEqual(core.summarize(self.good(),self.manual(),"staging")["veredito"], "STAGING_TECNICO_APROVADO_NAO_ATIVADO")
    def test_human_pending(self):
        self.assertEqual(core.summarize(self.good(),{},"final")["veredito"], "TECNICO_APROVADO_ACEITE_HUMANO_PENDENTE")
    def test_ready_requires_all(self):
        self.assertEqual(core.summarize(self.good(),self.manual(),"final")["veredito"],"PRONTO_PARA_PILOTO_BASICO")
    def test_skip_is_not_pass(self):
        r=self.good();r["spark"]={"status":"NAO_TESTADO"}
        self.assertEqual(core.summarize(r,self.manual(),"final")["veredito"],"INCOMPLETO")
    def test_fail_blocks(self):
        r=self.good();r["pit"]={"status":"FAIL"}
        self.assertEqual(core.summarize(r,self.manual(),"final")["veredito"],"BLOQUEADO")
    def test_human_fail_blocks(self):
        r=self.manual();r["genie_eda"]="REPROVADO"
        self.assertEqual(core.summarize(self.good(),r,"final")["veredito"],"BLOQUEADO")
    def test_optional_fail_is_not_full_success(self):
        r=self.good();r["mlflow"]={"status":"FAIL"}
        self.assertEqual(core.summarize(r,self.manual(),"final")["veredito"],"BASE_OK_EXTENSAO_REPROVADA")
    def test_block_does_not_call_function(self):
        with tempfile.TemporaryDirectory() as d:
            s=core.AcceptanceSession(d,Path(d)/"x","0"*64,COMMIT)
            f=mock.Mock();s.run("x",f,("arquivos",));f.assert_not_called()
            self.assertEqual(s.results["x"]["status"],"PENDENTE")
            s.results["arquivos"]={"status":"FAIL"};s.run("x",f,("arquivos",));f.assert_not_called()
            self.assertEqual(s.results["x"]["status"],"BLOQUEADO")
    def test_raw_exception_not_exported(self):
        with tempfile.TemporaryDirectory() as d:
            s=core.AcceptanceSession(d,Path(d)/"x","0"*64,COMMIT)
            s.run("error",mock.Mock(side_effect=RuntimeError("secret-user-path")))
            receipt=json.dumps(s.receipt({}))
            self.assertNotIn("secret-user-path",receipt)
            self.assertIn("error",s.errors_local)


class NotebookKitTests(unittest.TestCase):
    def setUp(self):
        self.core=(TOOLS/"aceite_trabalho.py").read_text()
        self.nb=json.loads(kit.notebook(COMMIT,"0"*64,self.core))
    def test_all_code_cells_compile(self):
        for cell in self.nb["cells"]:
            if cell["cell_type"]=="code": ast.parse("".join(cell["source"]))

    def test_micromodelos_notebook_checks_commit_and_failure(self):
        nb = json.loads(kit.micromodelos_notebook(COMMIT, "b" * 64,
                                                  (TOOLS/"aceite_micromodelos_trabalho.py").read_text()))
        code = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
        ast.parse(code)
        self.assertIn("resultado.get('source_commit')", code)
        self.assertIn("resultado.get('status') != 'PASS'", code)
        self.assertIn("run(PACKAGE_ROOT, MANIFEST_PATH,", code)
        self.assertIn("expected_manifest_sha256='" + "b" * 64 + "'", code)
        self.assertIn("hub_staging_", code)
        self.assertNotIn("mm_staging_", code)
        self.assertNotIn("testar_mlflow=True", code)
        self.assertNotIn("testar_metadata=True", code)
    def test_no_saved_outputs(self):
        for cell in self.nb["cells"]:
            if cell["cell_type"]=="code":
                self.assertEqual(cell["outputs"],[]);self.assertIsNone(cell["execution_count"])
    def test_dangerous_options_off(self):
        text="\n".join("".join(c["source"]) for c in self.nb["cells"])
        for flag in ("EXECUTAR_SPARK", "TESTAR_MLFLOW", "TESTAR_LEITURA_UC", "CONSULTAR_TIPOS_VIA_API"):
            self.assertIn(flag+" = False",text)
        self.assertNotIn("subprocess.run(",text)
        self.assertNotIn("dbutils.fs.rm(",text)
    def test_core_embedded_exactly(self):
        self.assertIn(self.core,["".join(c["source"]) for c in self.nb["cells"]])
    def test_declared_skills_exist_in_offline_guide(self):
        text=(TOOLS.parent/"docs/playbooks/testes-genie-trabalho.md").read_text(encoding="utf-8")
        for n in EXPECTED_SKILL_NAMES:self.assertIn(n,text)
    def test_all_managed_directories_in_guide(self):
        text=(TOOLS.parent/"docs/playbooks/replicacao-trabalho.md").read_text(encoding="utf-8")
        for n in EXPECTED_HUB_DIRS:self.assertIn(n,text)
    def test_import_cache_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            s=core.AcceptanceSession(d,Path(d)/"x","0"*64,COMMIT)
            with mock.patch.dict(sys.modules,{"hub_snippets":mock.Mock()}):
                with self.assertRaises(core.CheckError):s.check_imports()
    def test_uc_identifier_rejected_before_sql(self):
        with tempfile.TemporaryDirectory() as d:
            s=core.AcceptanceSession(d,Path(d)/"x","0"*64,COMMIT);spark=mock.Mock()
            for name in ("foo;DROP TABLE x", "a.b", "a.b.c --", "a.b.c.d"):
                with self.assertRaises(core.CheckError):s.check_uc(spark,name)
            spark.sql.assert_not_called()


class MLflowSafetyTests(unittest.TestCase):
    def setUp(self):
        import types
        self.temp = tempfile.TemporaryDirectory()
        self.session = core.AcceptanceSession(self.temp.name, Path(self.temp.name)/"x", "0"*64, COMMIT)
        self.client = mock.Mock()
        self.client.get_experiment_by_name.return_value = types.SimpleNamespace(experiment_id="e1", lifecycle_stage="active")
        self.client.create_run.return_value = types.SimpleNamespace(info=types.SimpleNamespace(run_id="own-run"))
        self.client.get_run.side_effect = lambda _id: types.SimpleNamespace(
            data=types.SimpleNamespace(metrics={"test_metric":1.0}),
            info=types.SimpleNamespace(lifecycle_stage="deleted" if self.client.delete_run.called else "active"))
        mlflow = types.ModuleType("mlflow")
        mlflow.get_tracking_uri = lambda: "databricks"
        mlflow.MlflowClient = lambda: self.client
        sdk = types.ModuleType("databricks.sdk")
        sdk.WorkspaceClient = lambda: types.SimpleNamespace(config=types.SimpleNamespace(host="https://work.example.com"))
        self.modules = {"mlflow":mlflow, "databricks.sdk":sdk}
    def tearDown(self): self.temp.cleanup()
    def run_case(self, host="https://work.example.com"):
        with mock.patch.dict(sys.modules, self.modules):
            return self.session.check_mlflow("/Users/test/acceptance", host)
    def test_roundtrip_and_only_own_run_deleted(self):
        self.run_case(); self.client.delete_run.assert_called_once_with("own-run")
        self.client.create_experiment.assert_not_called()
        self.client.delete_experiment.assert_not_called()
    def test_wrong_host_refuses_creation(self):
        with self.assertRaises(core.CheckError): self.run_case("https://wrong.example.com")
        self.client.create_run.assert_not_called()
    def test_wrong_tracking_uri_refuses_creation(self):
        self.modules["mlflow"].get_tracking_uri = lambda: "https://remote.example.com"
        with self.assertRaises(core.CheckError): self.run_case()
        self.client.create_run.assert_not_called()
    def test_logging_failure_cleans_owned_run(self):
        self.client.log_metric.side_effect = RuntimeError("injected")
        with self.assertRaises(RuntimeError): self.run_case()
        self.client.delete_run.assert_called_once_with("own-run")
    def test_cleanup_failure_is_failure(self):
        self.client.delete_run.side_effect = RuntimeError("cleanup")
        with self.assertRaises(RuntimeError): self.run_case()
    def test_create_failure_does_not_delete_anything(self):
        self.client.create_run.side_effect = RuntimeError("create")
        with self.assertRaises(RuntimeError): self.run_case()
        self.client.delete_run.assert_not_called()
    def test_absent_experiment_is_not_created(self):
        self.client.get_experiment_by_name.return_value = None
        with self.assertRaises(core.CheckError): self.run_case()
        self.client.create_run.assert_not_called(); self.client.create_experiment.assert_not_called()


@unittest.skipUnless(SPARK,"Spark local desabilitado; usar --spark explicitamente")
class SparkContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.spark=SparkSession.builder.master("local[2]").appName("hub-acceptance-synthetic").config("spark.ui.enabled","false").config("spark.sql.shuffle.partitions","2").getOrCreate()
        cls.temp=tempfile.TemporaryDirectory()
        cls.session=core.AcceptanceSession(cls.temp.name,Path(cls.temp.name)/"x","0"*64,COMMIT)
        sys.path.insert(0,str(TOOLS.parent/"ambiente_databricks/.assistant"))
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop();cls.temp.cleanup()
    def test_spark(self):self.session.check_spark(self.spark)
    def test_dq_expected_warning(self):self.session.check_dq(self.spark)
    def test_dq_expected_failure(self):self.session.check_dq(self.spark,duplicate=True)
    def test_rfv_cutoff(self):self.session.check_rfv(self.spark)
    def test_pit_availability_and_duplicates(self):self.session.check_pit(self.spark)
    def test_psi_identity(self):self.session.check_psi(self.spark)
    def test_temp_view_cleanup_even_on_failure(self):
        names=[]
        def fail(name):
            names.append(name);raise RuntimeError("injected")
        with self.assertRaises(RuntimeError):self.session.with_view(self.spark,self.spark.range(1),fail)
        self.assertFalse(self.spark.catalog.tableExists(names[0]))


if __name__=="__main__":unittest.main()
