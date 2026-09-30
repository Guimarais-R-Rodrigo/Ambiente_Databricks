"""Núcleo do notebook de aceite: verificações locais e testes sintéticos opt-in.

Não instala bibliotecas, publica o Hub ou grava tabelas. O gerador do kit embute
este código no notebook IPYNB para que não dependa de tools/ no workspace.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
import re
import sys
import time
import uuid
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath


class CheckError(Exception):
    """Erro com mensagem controlada, sem reproduzir paths ou dados do destino."""


CORE_IDS = ("manifesto", "arquivos", "imports", "python", "spark", "dq_aviso",
            "dq_falha", "rfv", "pit", "psi", "visual_objeto")
MANUAL_IDS = ("backup", "tipos_ui", "instrucoes_ui", "imagens_ui", "genie_eda",
              "genie_baseline", "genie_criar_objeto", "genie_contexto", "proveniencia")
MODULES = (
    "hub_snippets.constants.format_br", "hub_snippets.ml.split_temporal",
    "hub_scripts.data_quality_check", "hub_scripts.rfv_calculator",
    "hub_snippets.spark.pit_join", "hub_snippets.spark.psi_calculator",
    "hub_micromodelos.execucao", "hub_micromodelos.execucao.execucao",
)


def require(condition: bool, message: str) -> None:
    """Valida sem assert, para não desaparecer sob python -O."""
    if not condition:
        raise CheckError(message)


def safe_payload_path(root: Path, relative: str) -> Path:
    """Aceita somente paths relativos de produto, sem traversal ou symlink."""
    p = PurePosixPath(relative)
    require(isinstance(relative, str) and bool(relative), "Path vazio no manifesto.")
    require(not p.is_absolute() and "\\" not in relative and ":" not in relative,
            "Path inválido no manifesto.")
    require(all(x not in {"", ".", ".."} for x in relative.split("/")),
            "Navegação de diretórios recusada no manifesto.")
    require(relative == ".assistant_instructions.md" or relative.startswith(".assistant/"),
            "Manifesto contém arquivo fora do produto.")
    current = root
    for part in p.parts:
        current = current / part
        require(not current.is_symlink(), "Symlink recusado no produto sob teste.")
    require(current.resolve().is_relative_to(root.resolve()), "Arquivo escaparia da raiz autorizada.")
    return current


def validate_manifest(raw: bytes, expected_sha256: str, expected_commit: str) -> dict:
    """Confronta identidade fixa do kit, formato e escopo antes de ler o Hub."""
    require(hashlib.sha256(raw).hexdigest() == expected_sha256, "MANIFEST.json não corresponde ao kit.")
    obj = json.loads(raw)
    require(obj.get("schema_version") == 2, "Use manifesto v2 do kit de transição.")
    require(obj.get("source_commit") == expected_commit and bool(re.fullmatch(r"[a-f0-9]{40}", expected_commit)),
            "Commit do manifesto não corresponde ao notebook.")
    require(obj.get("worktree_dirty") is False, "Pacote de worktree não commitado recusado.")
    entries = obj.get("files")
    require(isinstance(entries, list) and len(entries) > 0, "Manifesto sem inventário.")
    seen = set()
    for entry in entries:
        path = entry.get("path", "")
        # Validação lexical independente do filesystem.
        require(isinstance(path, str) and path not in seen, "Path repetido ou inválido no manifesto.")
        require(not PurePosixPath(path).is_absolute() and "\\" not in path and ":" not in path
                and all(x not in {"", ".", ".."} for x in path.split("/")), "Path inseguro no manifesto.")
        require(path == ".assistant_instructions.md" or path.startswith(".assistant/"), "Escopo inválido.")
        require(entry.get("object_type") in {"FILE", "NOTEBOOK"}, "Tipo de objeto não declarado.")
        require(bool(re.fullmatch(r"[a-f0-9]{64}", entry.get("sha256", ""))), "SHA256 inválido.")
        require(type(entry.get("bytes")) is int and entry["bytes"] >= 0, "Tamanho inválido.")
        seen.add(path)
    require({".assistant_instructions.md", ".assistant/README.md", ".assistant/MANUAL_TECNICO.md"} <= seen,
            "Pacote não contém as três entradas escolhidas.")
    return obj


def summarize(results: dict, manual: dict, phase: str) -> dict:
    """Nunca transforma testes pulados ou declarações humanas em PASS automático."""
    ready = all(results.get(x, {}).get("status") == "PASS" for x in CORE_IDS)
    required_problem = any(results.get(x, {}).get("status") in {"FAIL", "BLOQUEADO"} for x in CORE_IDS)
    manual_ready = all(manual.get(x) == "CONFIRMADO" for x in MANUAL_IDS)
    manual_fail = any(manual.get(x) == "REPROVADO" for x in MANUAL_IDS)
    extra_fail = any(r.get("status") == "FAIL" for k, r in results.items() if k not in CORE_IDS)
    if required_problem or manual_fail:
        verdict = "BLOQUEADO"
    elif not ready:
        verdict = "INCOMPLETO"
    elif extra_fail:
        verdict = "BASE_OK_EXTENSAO_REPROVADA"
    elif phase == "staging":
        verdict = "STAGING_TECNICO_APROVADO_NAO_ATIVADO"
    elif not manual_ready:
        verdict = "TECNICO_APROVADO_ACEITE_HUMANO_PENDENTE"
    else:
        verdict = "PRONTO_PARA_PILOTO_BASICO"
    return {"veredito": verdict, "base_tecnica": "PASS" if ready else "NAO_APROVADA",
            "fase": phase, "confirmacoes_humanas": {x: manual.get(x, "PENDENTE") for x in MANUAL_IDS},
            "limites": ["Não certifica todos os helpers ou todos os notebooks didáticos.",
                        "Não mede segurança efetiva de ACLs nem custo/latência da Genie.",
                        "Não autoriza escrita produtiva, registro de modelo ou deploy."]}


class AcceptanceSession:
    """Acumula resultados sem parar a leitura; bloqueia dependentes de pré-requisitos."""
    def __init__(self, root, manifest_path, expected_sha256, expected_commit, phase="staging"):
        self.root = Path(root)
        self.manifest_path = Path(manifest_path)
        self.expected_sha256 = expected_sha256
        self.expected_commit = expected_commit
        self.phase = phase
        self.results = {}
        self.errors_local = {}
        self.manifest = None
        self.token = uuid.uuid4().hex[:12]
        self.mlflow_run_id = None
        require(phase in {"staging", "final"}, "Fase deve ser staging ou final.")
        require(self.root.is_absolute() and "<" not in str(self.root), "Preencha o diretório absoluto autorizado.")

    def run(self, key, fn, dependencies=()):
        """Guarda o diagnóstico público; detalhes completos ficam só na sessão."""
        missing = [x for x in dependencies if self.results.get(x, {}).get("status") != "PASS"]
        if missing:
            hard = any(self.results.get(x, {}).get("status") in {"FAIL", "BLOQUEADO"} for x in missing)
            self.results[key] = {"status": "BLOQUEADO" if hard else "PENDENTE", "detail": "Resolva primeiro: " + ", ".join(missing)}
        else:
            start = time.monotonic()
            try:
                detail = fn()
                self.results[key] = {"status": "PASS", "detail": str(detail or "Contrato conferido."),
                                     "seconds": round(time.monotonic()-start, 3)}
            except Exception as exc:
                self.errors_local[key] = exc  # não imprimir/repassar exceção corporativa bruta
                text = str(exc) if isinstance(exc, CheckError) else "Consulte a causa nesta sessão; não exporte o erro bruto."
                self.results[key] = {"status": "FAIL", "detail": text, "exception": type(exc).__name__}
            print(key, "->", self.results[key]["status"], "-", self.results[key]["detail"])
        return self.results[key]

    def skip(self, key, reason):
        self.results[key] = {"status": "NAO_TESTADO", "detail": reason}
        print(key, "→ NAO_TESTADO —", reason)

    def check_manifest(self):
        self.manifest = validate_manifest(self.manifest_path.read_bytes(), self.expected_sha256, self.expected_commit)
        return "Identidade do kit e manifesto v2 confirmados; nenhuma leitura de dados."

    def check_files(self):
        checked, notebooks, pngs = 0, 0, 0
        for entry in self.manifest["files"]:
            path = safe_payload_path(self.root, entry["path"])
            if entry["object_type"] == "NOTEBOOK":
                notebooks += 1
                continue  # SOURCE pode ser convertido; bytes de notebook exigem export dedicado
            require(path.is_file(), "FILE ausente/inacessível: " + entry["path"])
            raw = path.read_bytes()
            require(len(raw) == entry["bytes"] and hashlib.sha256(raw).hexdigest() == entry["sha256"],
                    "Conteúdo diverge do pacote: " + entry["path"])
            if path.suffix.lower() == ".png":
                require(raw.startswith(b"\x89PNG\r\n\x1a\n"), "PNG inválido no produto.")
                pngs += 1
            checked += 1
        self.file_stats = {"files_sha256": checked, "pngs": pngs, "notebooks_sem_hash_remoto": notebooks}
        return f"{checked} FILEs idênticos, incluindo {pngs} PNGs. {notebooks} NOTEBOOKs: tipo/UI, sem atestado de bytes."

    def check_notebook_types(self, expected_host):
        """API somente leitura; é opcional e não salva token nem mexe em ACL."""
        from databricks.sdk import WorkspaceClient
        from databricks.sdk.errors import NotFound
        client = WorkspaceClient()
        require(isinstance(expected_host, str) and expected_host.startswith("https://")
                and client.config.host.rstrip("/") == expected_host.rstrip("/"),
                "Host do SDK difere da URL de workspace explicitamente conferida.")
        count = 0
        for entry in self.manifest["files"]:
            if entry["object_type"] != "NOTEBOOK":
                continue
            path = safe_payload_path(self.root, entry["path"])
            remote = str(path)
            if remote.startswith("/Workspace/"):
                remote = remote[len("/Workspace"):]
            try:
                info = client.workspace.get_status(remote)
            except NotFound:
                # UI pode omitir extensão de notebooks SOURCE; nunca aplicar a módulo FILE.
                info = client.workspace.get_status(str(PurePosixPath(remote).with_suffix("")))
            kind = getattr(info.object_type, "value", info.object_type)
            require(kind == "NOTEBOOK", "Exemplo não foi reconhecido como NOTEBOOK: " + entry["path"])
            count += 1
        return f"{count} NOTEBOOKs confirmados por metadata da API; não é comparação de células/conteúdo."

    def check_imports(self):
        root = (self.root / ".assistant").resolve()
        # Sessão fresca evita falso PASS com módulo de versão anterior em sys.modules.
        contamination = [name for name in sys.modules if name in {"hub_scripts", "hub_snippets", "hub_micromodelos"}
                         or name.startswith(("hub_scripts.", "hub_snippets.", "hub_micromodelos."))]
        require(not contamination, "Há módulos Hub em cache: reinicie Python e rode desde o início.")
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        importlib.invalidate_caches()
        for name in MODULES:
            mod = importlib.import_module(name)
            require(Path(mod.__file__).resolve().is_relative_to(root), "Import resolvido fora da instalação sob teste.")
        self.loaded_modules = MODULES
        return f"{len(MODULES)} módulos importados da instalação verificada; nenhum exemplo didático executado."

    def check_python(self):
        from hub_snippets.constants.format_br import fmt_brl, fmt_pct
        require(fmt_brl(1250000.5) == "R$ 1.250.000,50", "Formato monetário divergente.")
        require(fmt_pct(0.154) == "15,4%", "Formato percentual divergente.")
        return "R$ 1.250.000,50 e 15,4%: retornos reais conferidos."

    def check_spark(self, spark):
        require(spark is not None, "Conecte o notebook ao compute autorizado e recomece.")
        row = spark.range(20).selectExpr("count(*) as n", "sum(id) as total").first()
        require(row.n == 20 and row.total == 190, "Ação Spark sintética com retorno divergente.")
        self.spark_version = spark.version
        return "Ação Spark concluída: N=20, soma=190; não acessa tabela corporativa."

    def with_view(self, spark, df, action):
        name = "hub_aceite_" + uuid.uuid4().hex
        df.createTempView(name)  # sem replace: nunca substituir recurso preexistente
        try:
            return action(name)
        finally:
            spark.catalog.dropTempView(name)  # exclusivamente a view criada nesta função

    def check_dq(self, spark, duplicate=False):
        from hub_scripts.data_quality_check import data_quality_check
        if duplicate:
            df = spark.createDataFrame([(1, "email"), (1, "email")], "event_id long, canal string")
        else:
            df = spark.createDataFrame([(i, None if i == 0 else "email") for i in range(20)],
                                       "event_id long, canal string")
        r = self.with_view(spark, df, lambda name: data_quality_check(
            table_name=name, pk_columns=["event_id"], date_column=None,
            thresholds={"null_warn": 5.0, "null_fail": 20.0}))
        require(set(r) == {"status", "score", "thresholds", "checks", "alerts"}, "Contrato DQ divergente.")
        if duplicate:
            require(r["status"] == "fail" and r["checks"]["pk_uniqueness"]["duplicate_rows"] == 1,
                    "Duplicidade não sinalizada como esperado.")
            return "PASS do teste negativo: helper devolveu fail para uma duplicidade, como deveria."
        require(r["status"] == "warn" and r["score"] == 95 and r["checks"]["row_count"] == 20
                and r["checks"]["nulls"]["canal"]["pct"] == 5.0 and "freshness" not in r["checks"],
                "Oráculo DQ (20 linhas, 5% nulos, score95) divergiu.")
        return "PASS: diagnóstico warn esperado, N=20, nulos=5%, score=95; independente do calendário."

    def check_rfv(self, spark):
        from hub_scripts.rfv_calculator import rfv_calculator
        df = spark.createDataFrame([("A", "2026-06-01", 10.0), ("A", "2026-06-05", 20.0),
                                    ("A", "2026-07-01", 999.0)], "cliente string, data string, valor double")
        r = self.with_view(spark, df, lambda name: rfv_calculator(
            table_name=name, col_cliente="cliente", col_data="data", col_valor="valor",
            dt_referencia="2026-06-10", periodos=[30]).collect())
        require(len(r) == 1 and r[0].valor_total == 30.0 and r[0].frequencia_total == 2 and r[0].recencia == 5,
                "RFV não respeitou o corte temporal do teste.")
        return "Valor=30, frequência=2, recência=5; evento futuro de 999 excluído."

    def check_pit(self, spark):
        from hub_snippets.spark.pit_join import pit_join
        facts = spark.createDataFrame([("A", date(2026, 6, 10)), ("A", date(2026, 6, 10))],
                                      "cliente string, decisao date")
        feats = spark.createDataFrame([("A", date(2026, 6, 1), 10.0), ("A", date(2026, 6, 9), 99.0)],
                                      "cliente string, referencia date, valor double")
        output, diagnostics = pit_join(facts, feats, chave="cliente", ts_decisao="decisao",
            ts_feature="referencia", atraso_publicacao_dias=2, colunas_feature=["valor"])
        rows = output.select("valor").collect()
        require(len(rows) == 2 and all(x.valor == 10.0 for x in rows) and isinstance(diagnostics, dict),
                "PIT não preservou linhas/atraso de publicação.")
        return "Duas linhas preservadas; valor10 disponível, valor99 ainda indisponível."

    def check_psi(self, spark):
        from hub_snippets.spark.psi_calculator import calcular_psi
        df = spark.createDataFrame([(float(i),) for i in range(20)], "valor double")
        value = calcular_psi(df, df, col="valor", n_bins=4)
        require(abs(value) < 1e-8, "PSI de distribuições idênticas deve ser zero.")
        return "PSI=0 para distribuições idênticas; não calibra thresholds de negócio."

    def check_visual_object(self):
        import plotly.graph_objects as go
        self.figure = go.Figure(go.Bar(x=["A", "B"], y=[10, 20]))
        require(list(self.figure.data[0].y) == [10, 20], "Objeto Plotly divergente.")
        return "Objeto Plotly construído. A aparência e os READMEs exigem conferência humana."

    def check_uc(self, spark, table):
        # Opt-in: única tabela selecionada; nenhuma enumeração de catálogos ou valores no output.
        require(bool(re.fullmatch(r"[A-Za-z_][\w]*\.[A-Za-z_][\w]*\.[A-Za-z_][\w]*", table)),
                "Informe nome catalog.schema.table simples e autorizado, somente no destino.")
        quoted = ".".join("`" + x + "`" for x in table.split("."))
        rows = spark.sql("SELECT 1 AS acesso FROM " + quoted + " LIMIT 1").collect()
        require(len(rows) <= 1, "Consulta de acesso excedeu o limite.")
        return "Consulta SELECT limitada concluída na tabela autorizada; nenhum valor corporativo exibido."

    def check_mlflow(self, experiment_path, expected_host):
        # Somente tracking em experimento existente. Não cria experimento, treina ou registra modelo.
        import mlflow
        from mlflow import MlflowClient
        require(mlflow.get_tracking_uri() == "databricks", "Tracking URI não é o workspace atual; não será alterado.")
        require(experiment_path.startswith("/Users/") and "<" not in experiment_path,
                "Informe experimento pessoal temporário existente, aprovado no destino.")
        from databricks.sdk import WorkspaceClient
        sdk = WorkspaceClient()
        require(isinstance(expected_host, str) and expected_host.startswith("https://")
                and sdk.config.host.rstrip("/") == expected_host.rstrip("/"),
                "Host da autenticação difere do workspace explicitamente conferido.")
        client = MlflowClient()
        exp = client.get_experiment_by_name(experiment_path)
        require(exp is not None and exp.lifecycle_stage == "active", "Experimento temporário ausente/inativo.")
        run = client.create_run(exp.experiment_id, tags={"hub_acceptance": self.expected_commit,
                                                       "purpose": "synthetic_migration_test"})
        self.mlflow_run_id = run.info.run_id
        try:
            client.log_param(self.mlflow_run_id, "fixture", "synthetic")
            client.log_metric(self.mlflow_run_id, "test_metric", 1.0)
            observed = client.get_run(self.mlflow_run_id)
            require(observed.data.metrics.get("test_metric") == 1.0, "Métrica gravada não foi confirmada.")
        finally:
            # Só toca no run que esta chamada criou; falha de limpeza reprova o caso.
            try:
                client.set_terminated(self.mlflow_run_id)
            finally:
                client.delete_run(self.mlflow_run_id)
            require(client.get_run(self.mlflow_run_id).info.lifecycle_stage == "deleted",
                    "Run de teste não está excluído; inspecione a limpeza no destino.")
        return "Parâmetro/métrica lidos de volta; run próprio excluído logicamente. Experimento preservado; modelo não testado."

    def dependency_inventory(self):
        packages = ("numpy", "pandas", "pyspark", "plotly", "scikit-learn", "mlflow", "lightgbm",
                    "xgboost", "catboost", "optuna", "shap", "umap-learn", "lifelines", "prophet", "torch")
        result = {}
        for name in packages:
            try:
                result[name] = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                result[name] = "NAO_INSTALADO"
        return result  # instalado não equivale a importável ou funcional

    def receipt(self, manual):
        data = summarize(self.results, manual, self.phase)
        data.update(source_commit=self.expected_commit, manifest_sha256=self.expected_sha256,
                    generated_at_utc=datetime.now(timezone.utc).isoformat(),
                    execution_scope="workspace_do_trabalho_a_confirmar_pelo_operador",
                    results=self.results, file_stats=getattr(self, "file_stats", {}))
        return data
