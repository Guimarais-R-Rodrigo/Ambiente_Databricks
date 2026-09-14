"""V10 — Databricks App de gestão visual, persistência e guardas fail-closed."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "ambiente_fonte" / ".assistant"
APP = PRODUCT / "hub_padroes" / "identidade_visual" / "databricks_app"
MIRROR = ROOT / "Novo_Ambiente_Simulado" / "Users" / "usuario-free" / ".assistant" / "hub_padroes" / "identidade_visual" / "databricks_app"
sys.path.insert(0, str(PRODUCT))
sys.path.insert(0, str(APP))

from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_lab import ThemeLabError, create_theme_lab
from app_service import (
    ThemeAppError,
    list_own_sessions,
    load_config,
    publication_policy,
    reopen_own_session,
    resolve_user,
    retention_policy,
    save_own_session,
)


class IdentityTests(unittest.TestCase):
    def test_forwarded_identity_is_hashed_for_namespace(self):
        user = resolve_user({"X-Forwarded-User": "user-123", "X-Forwarded-Preferred-Username": "Pessoa Teste"}, env={})
        self.assertEqual(user.source, "databricks_forwarded_header")
        self.assertEqual(user.display_name, "Pessoa Teste")
        self.assertEqual(user.namespace, hashlib.sha256(b"user-123").hexdigest())
        self.assertNotIn("user-123", user.namespace)

    def test_missing_identity_fails_closed(self):
        with self.assertRaises(ThemeAppError) as cm:
            resolve_user({}, env={})
        self.assertEqual(cm.exception.code, "APP_IDENTITY_MISSING")

    def test_local_identity_requires_two_explicit_values(self):
        with self.assertRaises(ThemeAppError) as cm:
            resolve_user({}, env={"HUB_THEME_LOCAL_DEV": "true"})
        self.assertEqual(cm.exception.code, "APP_LOCAL_USER_MISSING")
        user = resolve_user({}, env={"HUB_THEME_LOCAL_DEV": "true", "HUB_THEME_LOCAL_USER_ID": "synthetic-user"})
        self.assertEqual(user.source, "explicit_local_dev")


class ConfigTests(unittest.TestCase):
    def test_production_requires_uc_volume_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ThemeAppError) as cm:
                load_config(env={"HUB_THEME_VOLUME": tmp, "HUB_THEME_APP_MODE": "authoring_only"})
            self.assertEqual(cm.exception.code, "APP_STORAGE_NOT_VOLUME")

    def test_local_mode_accepts_explicit_temp_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = load_config(env={
                "HUB_THEME_LOCAL_DEV": "true",
                "HUB_THEME_VOLUME": tmp,
                "HUB_THEME_APP_MODE": "authoring_only",
            })
            self.assertTrue(config.local_dev)
            self.assertEqual(config.storage_root, Path(tmp).absolute())

    def test_mode_cannot_enable_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ThemeAppError) as cm:
                load_config(env={
                    "HUB_THEME_LOCAL_DEV": "true",
                    "HUB_THEME_VOLUME": tmp,
                    "HUB_THEME_APP_MODE": "publish",
                })
            self.assertEqual(cm.exception.code, "APP_MODE_UNSUPPORTED")


class PersistenceTests(unittest.TestCase):
    def _context(self, root: str, subject: str):
        config = load_config(env={
            "HUB_THEME_LOCAL_DEV": "true",
            "HUB_THEME_VOLUME": root,
            "HUB_THEME_APP_MODE": "authoring_only",
        })
        user = resolve_user({"x-forwarded-user": subject}, env={})
        return config, user

    def test_roundtrip_uses_v05_session_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, user = self._context(tmp, "author-a")
            draft = create_theme_lab(load_reference_theme("notebook"))
            draft.set_token("brand.primary", "#0066cc")
            receipt = save_own_session(draft, config, user, "sessao-v10")
            self.assertEqual(receipt.session_name, "sessao-v10")
            listed = list_own_sessions(config, user)
            self.assertEqual([item.session_name for item in listed], ["sessao-v10"])
            reopened = reopen_own_session(config, user, "sessao-v10")
            self.assertEqual(reopened.current.content_sha256, draft.current.content_sha256)
            self.assertEqual(reopened.base.content_sha256, draft.base.content_sha256)

    def test_two_users_do_not_list_each_others_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, user_a = self._context(tmp, "author-a")
            _, user_b = self._context(tmp, "author-b")
            draft = create_theme_lab(load_reference_theme("notebook"))
            save_own_session(draft, config, user_a, "privada-a")
            self.assertEqual([item.session_name for item in list_own_sessions(config, user_a)], ["privada-a"])
            self.assertEqual(list_own_sessions(config, user_b), ())
            with self.assertRaises(ThemeAppError) as cm:
                reopen_own_session(config, user_b, "privada-a")
            self.assertEqual(cm.exception.code, "APP_SESSION_ROOT_MISSING")

    def test_existing_session_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, user = self._context(tmp, "author-a")
            draft = create_theme_lab(load_reference_theme("notebook"))
            save_own_session(draft, config, user, "mesmo-nome")
            with self.assertRaises(ThemeLabError):
                save_own_session(draft, config, user, "mesmo-nome")

    def test_tampered_session_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, user = self._context(tmp, "author-a")
            draft = create_theme_lab(load_reference_theme("notebook"))
            receipt = save_own_session(draft, config, user, "adulterada")
            proposal = Path(receipt.destination) / "proposal.json"
            proposal.write_text("{}", encoding="utf-8")
            with self.assertRaises(ThemeLabError):
                reopen_own_session(config, user, "adulterada")


class PolicyTests(unittest.TestCase):
    def test_retention_has_no_delete_or_history_rewrite(self):
        policy = retention_policy()
        self.assertFalse(policy["automatic_delete"])
        self.assertFalse(policy["user_delete_action"])
        self.assertFalse(policy["history_rewrite"])

    def test_publication_is_not_implemented(self):
        policy = publication_policy()
        self.assertFalse(policy["approve_implemented"])
        self.assertFalse(policy["publish_implemented"])
        self.assertFalse(policy["promote_implemented"])

    def test_v01_roles_are_preserved_in_v10_matrix(self):
        policy = json.loads((ROOT / "docs/sprints/sistema_temas/V01/politica_workflow.json").read_text(encoding="utf-8"))
        matrix = json.loads((ROOT / "docs/sprints/sistema_temas/V10/MATRIZ_PAPEIS.json").read_text(encoding="utf-8"))
        self.assertEqual(matrix["canonical_roles"], policy["roles"])
        self.assertEqual(matrix["role_source"], "docs/sprints/sistema_temas/V01/politica_workflow.json")
        self.assertEqual(matrix["v10_surface"], "authoring_only")


class PackagingTests(unittest.TestCase):
    def test_app_source_and_simulated_mirror_are_identical(self):
        names = {path.relative_to(APP).as_posix() for path in APP.rglob("*") if path.is_file()}
        mirror_names = {path.relative_to(MIRROR).as_posix() for path in MIRROR.rglob("*") if path.is_file()}
        self.assertEqual(names, mirror_names)
        for name in names:
            self.assertEqual((APP / name).read_bytes(), (MIRROR / name).read_bytes(), name)

    def test_app_yaml_uses_resource_reference_without_secret(self):
        text = (APP / "app.yaml").read_text(encoding="utf-8")
        self.assertIn("valueFrom: theme_storage", text)
        self.assertIn("authoring_only", text)
        for forbidden in ("DATABRICKS_TOKEN", "/Volumes/", "https://", "http://"):
            self.assertNotIn(forbidden, text)

    def test_streamlit_shell_has_no_publish_or_approve_action(self):
        text = (APP / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("WorkspaceClient", text)
        self.assertNotIn("databricks.sdk", text)
        self.assertNotIn("publish(", text)
        self.assertNotIn("approve(", text)
        self.assertIn("X-Forwarded", (APP / "README.md").read_text(encoding="utf-8"))

    def test_bundle_builder_creates_and_verifies_derived_app(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bundle"
            command = [sys.executable, "-B", str(ROOT / "tools/temas_v10_app.py"), "--output", str(output)]
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            manifest = json.loads((output / "V10_APP_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["publication"], "not_implemented")
            self.assertEqual(manifest["resource_key"], "theme_storage")
            self.assertTrue((output / "hub_snippets/visual/theme_lab/theme_lab.py").is_file())
            verify = subprocess.run(
                [sys.executable, "-B", str(ROOT / "tools/temas_v10_app.py"), "--verify", str(output)],
                cwd=ROOT, capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
