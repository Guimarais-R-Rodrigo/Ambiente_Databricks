"""Testes focados dos guardrails do publicador visual alvo-fechado."""

from __future__ import annotations

import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


VISUAL_TOOLS = Path(__file__).resolve().parents[1]
if str(VISUAL_TOOLS) not in sys.path:
    sys.path.insert(0, str(VISUAL_TOOLS))

import publish_production as publisher  # noqa: E402


class VisualReleaseFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / ".assistant"
        for relative in publisher.ACTIVE_READMES:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {relative}\n", encoding="utf-8", newline="\n")
        asset = self.root / publisher.ASSET_REL
        (asset / "qa").mkdir(parents=True)
        (asset / "qa" / "validation.json").write_text(
            json.dumps({"status": "passed", "scope": "all"}) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (asset / "manifest.yaml").write_text(
            "version: 2\nassets: []\n", encoding="utf-8", newline="\n"
        )
        (asset / "readmes" / "demo" / "png").mkdir(parents=True)
        (asset / "readmes" / "demo" / "png" / "figure.png").write_bytes(
            b"\x89PNG\r\n\x1a\nfixture"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def records(self) -> dict[str, publisher.LocalFile]:
        return publisher.collect_local_files(self.root)

    def exact_snapshot(
        self, records: dict[str, publisher.LocalFile]
    ) -> publisher.RemoteSnapshot:
        return publisher.RemoteSnapshot(
            files={
                relative: publisher.RemoteFile(relative, "FILE", record.content)
                for relative, record in records.items()
            },
            directories=frozenset(publisher._expected_asset_directories(records)),
        )


class ScopeTests(VisualReleaseFixture):
    def test_noncanonical_paths_are_rejected(self) -> None:
        for value in ("", ".", "..", "../README.md", "/README.md", "a//b", "a/./b", "C:/x", "a\\b"):
            with self.subTest(value=value), self.assertRaises(publisher.PublicationError):
                publisher._safe_relative(value)

    def test_programmatic_payload_cannot_broaden_scope(self) -> None:
        for relative in ("hub_scripts/runtime.py", "../README.md", "hub_readmes_visual_assets_old/a"):
            records = {relative: publisher.LocalFile(relative, self.root / "README.md", b"x")}
            with self.subTest(relative=relative), self.assertRaises(publisher.PublicationError):
                publisher.stage_payload(records, Path(self.temp.name) / "run")

    def test_allowlist_is_five_readmes_plus_entire_asset_tree(self) -> None:
        records = self.records()
        self.assertEqual(
            {relative for relative in records if relative in publisher.ACTIVE_READMES},
            set(publisher.ACTIVE_READMES),
        )
        self.assertTrue(
            all(
                relative in publisher.ACTIVE_READMES
                or relative.startswith(publisher.ASSET_REL + "/")
                for relative in records
            )
        )
        self.assertNotIn("../README.md", records)
        self.assertIn(
            f"{publisher.ASSET_REL}/readmes/demo/png/figure.png", records
        )

    def test_local_legacy_file_blocks_release(self) -> None:
        legacy = self.root / publisher.LEGACY_ASSET_PATHS[0]
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_bytes(b"old")
        with self.assertRaisesRegex(publisher.PublicationError, "legados"):
            self.records()

    def test_incomplete_visual_qa_blocks_release(self) -> None:
        report = self.root / publisher.ASSET_REL / "qa" / "validation.json"
        report.write_text(
            json.dumps({"status": "failed", "scope": "all"}), encoding="utf-8"
        )
        with self.assertRaisesRegex(publisher.PublicationError, "QA visual"):
            self.records()


class PreflightTests(VisualReleaseFixture):
    def test_crlf_inside_png_is_not_normalized(self) -> None:
        relative = "hub_readmes_visual_assets/readmes/demo/png/figure.png"
        self.assertFalse(
            publisher._equivalent_for_preflight(b"PNG\r\nbytes", b"PNG\nbytes", relative)
        )

    def test_notebook_with_same_bytes_is_not_reported_as_verified_file(self) -> None:
        records = self.records()
        snapshot = self.exact_snapshot(records)
        files = dict(snapshot.files)
        relative = publisher.ACTIVE_READMES[0]
        files[relative] = publisher.RemoteFile(relative, "NOTEBOOK", records[relative].content)
        problems, evidence = publisher.verify_snapshot(
            publisher.RemoteSnapshot(files, snapshot.directories), records
        )
        self.assertTrue(any("tipo remoto" in item for item in problems))
        self.assertNotIn(relative, {item["path"] for item in evidence})

    def test_text_line_endings_are_equivalent_only_during_preflight(self) -> None:
        records = self.records()
        relative = publisher.ACTIVE_READMES[0]
        remote_files = {
            key: publisher.RemoteFile(key, "FILE", record.content)
            for key, record in records.items()
        }
        remote_files[relative] = publisher.RemoteFile(
            relative,
            "FILE",
            records[relative].content.replace(b"\n", b"\r\n"),
        )
        snapshot = publisher.RemoteSnapshot(
            files=remote_files,
            directories=frozenset(publisher._expected_asset_directories(records)),
        )
        baseline = {key: value.content for key, value in records.items()}
        assessment = publisher.assess_preflight(
            snapshot, records, baseline, allow_legacy_retirement=False
        )
        self.assertEqual(assessment.conflicts, ())
        self.assertIn(relative, assessment.uploads)

        problems, _evidence = publisher.verify_snapshot(snapshot, records)
        self.assertIn(f"bytes remotos divergentes: {relative}", problems)

    def test_binary_change_is_never_normalized(self) -> None:
        records = self.records()
        relative = f"{publisher.ASSET_REL}/readmes/demo/png/figure.png"
        snapshot = self.exact_snapshot(records)
        changed = dict(snapshot.files)
        changed[relative] = publisher.RemoteFile(relative, "FILE", b"different")
        assessment = publisher.assess_preflight(
            publisher.RemoteSnapshot(changed, snapshot.directories),
            records,
            {key: value.content for key, value in records.items()},
            allow_legacy_retirement=False,
        )
        self.assertTrue(any(relative in item for item in assessment.conflicts))

    def test_unexpected_remote_file_and_directory_fail_closed(self) -> None:
        records = self.records()
        snapshot = self.exact_snapshot(records)
        files = dict(snapshot.files)
        extra = f"{publisher.ASSET_REL}/manual.txt"
        files[extra] = publisher.RemoteFile(extra, "FILE", b"manual")
        directories = set(snapshot.directories)
        directories.add(f"{publisher.ASSET_REL}/manual")
        assessment = publisher.assess_preflight(
            publisher.RemoteSnapshot(files, frozenset(directories)),
            records,
            {key: value.content for key, value in records.items()},
            allow_legacy_retirement=True,
        )
        self.assertTrue(any("arquivo remoto inesperado" in x for x in assessment.conflicts))
        self.assertTrue(any("diretório remoto inesperado" in x for x in assessment.conflicts))

    def test_legacy_requires_flag_and_exact_baseline_bytes(self) -> None:
        records = self.records()
        snapshot = self.exact_snapshot(records)
        legacy = publisher.LEGACY_ASSET_PATHS[0]
        files = dict(snapshot.files)
        files[legacy] = publisher.RemoteFile(legacy, "FILE", b"known-old")
        with_legacy = publisher.RemoteSnapshot(files, snapshot.directories)
        baseline = {key: value.content for key, value in records.items()}
        baseline[legacy] = b"known-old"

        denied = publisher.assess_preflight(
            with_legacy, records, baseline, allow_legacy_retirement=False
        )
        self.assertTrue(any("--retire-legacy" in x for x in denied.conflicts))
        allowed = publisher.assess_preflight(
            with_legacy, records, baseline, allow_legacy_retirement=True
        )
        self.assertEqual(allowed.conflicts, ())
        self.assertEqual(allowed.legacy_present, (legacy,))

        files[legacy] = publisher.RemoteFile(legacy, "FILE", b"modified-old")
        changed = publisher.assess_preflight(
            publisher.RemoteSnapshot(files, snapshot.directories),
            records,
            baseline,
            allow_legacy_retirement=True,
        )
        self.assertTrue(any("baseline" in x for x in changed.conflicts))


class BackupAndExecutionTests(VisualReleaseFixture):
    def test_backup_corruption_blocks_before_any_write(self) -> None:
        snapshot = self.exact_snapshot(self.records())
        run = Path(self.temp.name) / "corrupt-run"
        record = next(iter(snapshot.files.values()))
        blob = run / "remote-backup" / "blobs" / f"{record.sha256}.bin"
        blob.parent.mkdir(parents=True)
        blob.write_bytes(b"corrupted")
        with self.assertRaisesRegex(publisher.PublicationError, "backup remoto corrompido"):
            publisher.backup_snapshot(snapshot, run)

    def test_full_mocked_release_backs_up_uploads_and_retires_exact_allowlist(self) -> None:
        records = self.records()
        relative = publisher.ACTIVE_READMES[0]
        current = {key: record.content for key, record in records.items()}
        current[relative] = b"old README"
        current.update({key: b"old legacy" for key in publisher.LEGACY_ASSET_PATHS})
        baseline = dict(current)
        remote_prefix = "/Users/test/.assistant/"
        old = publisher.RemoteSnapshot(
            {key: publisher.RemoteFile(key, "FILE", value) for key, value in current.items()},
            frozenset(publisher._expected_asset_directories(records)),
        )
        final = self.exact_snapshot(records)
        run = Path(self.temp.name) / "complete-run"
        client = mock.Mock()

        def status(path: str) -> dict[str, str] | None:
            return {"object_type": "FILE"} if path.removeprefix(remote_prefix) in current else None

        def upload(path: str, payload: Path) -> None:
            backup = run / "remote-backup" / "manifest.json"
            self.assertTrue(backup.is_file(), "backup must exist before first mutation")
            self.assertEqual(len(json.loads(backup.read_text(encoding="utf-8"))["files"]), len(old.files))
            current[path.removeprefix(remote_prefix)] = payload.read_bytes()

        client.get_status_optional.side_effect = status
        client.export.side_effect = lambda path, _type: current[path.removeprefix(remote_prefix)]
        client.import_raw.side_effect = upload
        client.delete_file.side_effect = lambda path: current.pop(path.removeprefix(remote_prefix))
        with mock.patch.object(publisher, "capture_remote_snapshot", side_effect=[old, old, final]):
            receipt_path = publisher.execute_release(
                client, "/Users/test", records, "a" * 40, baseline,
                {"source_commit": "b" * 40, "scope_dirty": True},
                retire_legacy=True, run_directory=run, assistant_root=self.root,
            )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["status"], "verified")
        self.assertEqual(receipt["uploaded"], [relative])
        self.assertEqual(set(receipt["deleted_legacy"]), set(publisher.LEGACY_ASSET_PATHS))
        self.assertEqual(len(client.delete_file.call_args_list), 12)
        self.assertEqual(current, {key: value.content for key, value in records.items()})

    def test_backup_contains_every_existing_file_as_content_addressed_blob(self) -> None:
        records = self.records()
        snapshot = self.exact_snapshot(records)
        run = Path(self.temp.name) / "run"
        manifest = publisher.backup_snapshot(snapshot, run)
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(len(payload["files"]), len(snapshot.files))
        self.assertTrue(all(item["path"].startswith("$USER_ROOT/") for item in payload["files"]))
        for item in payload["files"]:
            blob = run / item["blob"]
            self.assertTrue(blob.is_file())
            self.assertEqual(publisher._sha(blob.read_bytes()), item["raw_sha256"])

    def test_remote_change_between_preflight_and_write_aborts_without_mutation(self) -> None:
        records = self.records()
        first = publisher.RemoteSnapshot(files={}, directories=frozenset())
        second = publisher.RemoteSnapshot(
            files={
                f"{publisher.ASSET_REL}/intruder.txt": publisher.RemoteFile(
                    f"{publisher.ASSET_REL}/intruder.txt", "FILE", b"changed"
                )
            },
            directories=frozenset({publisher.ASSET_REL}),
        )
        client = mock.Mock()
        with mock.patch.object(
            publisher, "capture_remote_snapshot", side_effect=[first, second]
        ), mock.patch.object(publisher, "collect_local_files", return_value=records):
            with self.assertRaisesRegex(publisher.PublicationError, "mudou durante"):
                publisher.execute_release(
                    client,
                    "/Users/test",
                    records,
                    "a" * 40,
                    {},
                    {"source_commit": "b" * 40, "scope_dirty": False},
                    retire_legacy=False,
                    run_directory=Path(self.temp.name) / "execute",
                    assistant_root=self.root,
                )
        client.mkdirs.assert_not_called()
        client.import_raw.assert_not_called()
        client.delete_file.assert_not_called()

    def test_cli_commands_use_raw_and_never_recursive_delete(self) -> None:
        client = publisher.DatabricksClient("free")
        client.json = mock.Mock(return_value={})  # type: ignore[method-assign]
        client.import_raw("/Users/test/a", Path("payload.png"))
        client.delete_file("/Users/test/old.png")
        self.assertEqual(
            client.json.call_args_list[0].args,
            (
                "workspace",
                "import",
                "/Users/test/a",
                "--file",
                "payload.png",
                "--format",
                "RAW",
                "--overwrite",
            ),
        )
        self.assertEqual(
            client.json.call_args_list[1].args,
            ("workspace", "delete", "/Users/test/old.png"),
        )
        self.assertNotIn("--recursive", client.json.call_args_list[1].args)

    def test_each_overwrite_rechecks_remote_bytes(self) -> None:
        previous = publisher.RemoteFile("README.md", "FILE", b"old")
        client = mock.Mock()
        client.get_status_optional.return_value = {"object_type": "FILE"}
        client.export.return_value = b"changed-after-snapshot"
        with self.assertRaisesRegex(publisher.PublicationError, "mudou antes"):
            publisher._assert_target_unchanged(
                client, "/Users/test", "README.md", previous
            )
        client.import_raw.assert_not_called()

    def test_listing_error_is_fail_closed(self) -> None:
        client = mock.Mock()
        client.get_status_optional.side_effect = [
            {"object_type": "DIRECTORY"},
        ]
        client.list_directory.side_effect = publisher.PublicationError("list failed")
        with self.assertRaisesRegex(publisher.PublicationError, "list failed"):
            publisher.capture_remote_snapshot(client, "/Users/test")


class RetryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.payload = Path(self.temp.name) / "figure.png"
        self.payload.write_bytes(b"new PNG\r\nbytes")
        self.client = mock.Mock()
        self.client.import_raw.side_effect = publisher.PublicationError("ambiguous timeout")
        self.client.get_status_optional.return_value = {"object_type": "FILE"}
        self.previous = publisher.RemoteFile("README.md", "FILE", b"old")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_ambiguous_success_does_not_upload_twice(self) -> None:
        self.client.export.return_value = self.payload.read_bytes()
        with mock.patch.object(publisher.time, "sleep"):
            publisher._upload_with_retry(
                self.client, "/Users/test/figure.png", self.payload, previous=self.previous
            )
        self.assertEqual(self.client.import_raw.call_count, 1)

    def test_concurrent_edit_blocks_retry(self) -> None:
        self.client.export.return_value = b"independent edit"
        with mock.patch.object(publisher.time, "sleep"), self.assertRaisesRegex(
            publisher.PublicationError, "retry bloqueado"
        ):
            publisher._upload_with_retry(
                self.client, "/Users/test/figure.png", self.payload, previous=self.previous
            )
        self.assertEqual(self.client.import_raw.call_count, 1)

    def test_known_previous_bytes_allow_bounded_retry(self) -> None:
        self.client.export.return_value = self.previous.content
        self.client.import_raw.side_effect = [publisher.PublicationError("timeout"), None]
        with mock.patch.object(publisher.time, "sleep"):
            publisher._upload_with_retry(
                self.client, "/Users/test/figure.png", self.payload, previous=self.previous
            )
        self.assertEqual(self.client.import_raw.call_count, 2)


class DestinationAndGateTests(VisualReleaseFixture):
    def test_exact_cli_missing_path_message_is_accepted(self) -> None:
        client = publisher.DatabricksClient("free")
        remote = "/Users/test/.assistant/hub_readmes_visual_assets/headers"
        client._raw = mock.Mock(return_value=(1, "", f"Error: Path ({remote}) doesn't exist.\n"))
        self.assertIsNone(client.get_status_optional(remote))

    def test_missing_path_message_must_match_target_and_empty_stdout(self) -> None:
        client = publisher.DatabricksClient("free")
        remote = "/Users/test/.assistant/hub_readmes_visual_assets/headers"
        responses = (
            (1, "", "Error: Path (/Users/another/path) doesn't exist.\n"),
            (1, '{"partial": true}', f"Error: Path ({remote}) doesn't exist.\n"),
            (1, "", f"Error: Permission denied. Path ({remote}) doesn't exist.\n"),
            (1, "", f"Error: Path ({remote}) doesn't exist.\nAnother error"),
        )
        for response in responses:
            with self.subTest(response=response), self.assertRaises(publisher.PublicationError):
                client._raw = mock.Mock(return_value=response)
                client.get_status_optional(remote)

    def test_resolve_destination_reuses_canonical_gate_and_restores_globals(self) -> None:
        client = publisher.DatabricksClient("free")
        previous_profile = publisher.full_publisher.CLI_PROFILE
        previous_cli = publisher.full_publisher.databricks
        with mock.patch.object(publisher.full_publisher, "resolve_home", return_value=(
            "/Users/test", "test", "https://example.cloud.databricks.com", "free"
        )) as resolve:
            self.assertEqual(
                publisher.resolve_destination(client, "free", "https://example.cloud.databricks.com"),
                ("/Users/test", "https://example.cloud.databricks.com"),
            )
        resolve.assert_called_once_with(
            expected_host="https://example.cloud.databricks.com", require_explicit_target=True
        )
        self.assertIs(publisher.full_publisher.databricks, previous_cli)
        self.assertEqual(publisher.full_publisher.CLI_PROFILE, previous_profile)

    def test_different_profile_and_unsafe_user_block(self) -> None:
        client = publisher.DatabricksClient("free")
        for user, profile in (("test", "other"), ("..", "free"), ("", "free"), ("a/b", "free")):
            with self.subTest(user=user, profile=profile), mock.patch.object(
                publisher.full_publisher, "resolve_home",
                return_value=(f"/Users/{user}", user, "https://example.cloud.databricks.com", profile),
            ), self.assertRaises(publisher.PublicationError):
                publisher.resolve_destination(client, "free", "https://example.cloud.databricks.com")

    def test_partial_listing_is_not_accepted(self) -> None:
        client = publisher.DatabricksClient("free")
        client.json = mock.Mock(return_value={"objects": [], "next_page_token": "next"})
        with self.assertRaisesRegex(publisher.PublicationError, "parcial"):
            client.list_directory("/Users/test/.assistant/hub_readmes_visual_assets")

    def test_mirror_requires_exact_png_bytes_even_if_canonical_gate_normalizes(self) -> None:
        records = self.records()
        relative = "hub_readmes_visual_assets/readmes/demo/png/figure.png"
        (self.root / relative).write_bytes(records[relative].content.replace(b"\r\n", b"\n"))
        with mock.patch.object(
            publisher.full_publisher, "local_tree", return_value=(self.root.parent, [])
        ), mock.patch.object(publisher.full_publisher, "conferir_fonte_espelho", return_value=[]), self.assertRaisesRegex(
            publisher.PublicationError, "bytes brutos divergentes"
        ):
            publisher.assert_mirror_is_current(records)

    def test_failed_current_visual_gate_blocks(self) -> None:
        with mock.patch.object(publisher.subprocess, "run", return_value=mock.Mock(returncode=1)), self.assertRaisesRegex(
            publisher.PublicationError, "QA visual local reprovado"
        ):
            publisher.assert_visual_qa_is_current()

    def test_plan_is_local_and_rechecks_qa_and_mirror(self) -> None:
        records = self.records()
        with mock.patch.object(publisher, "assert_visual_qa_is_current") as qa, mock.patch.object(
            publisher, "collect_local_files", return_value=records
        ), mock.patch.object(publisher, "assert_mirror_is_current") as mirror, mock.patch.object(
            publisher, "load_baseline", return_value=("a" * 40, {})
        ), mock.patch.object(publisher, "source_provenance", return_value={}), mock.patch.object(
            publisher, "DatabricksClient"
        ) as client, mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(publisher.main([]), 0)
        qa.assert_called_once_with()
        mirror.assert_called_once_with(records)
        client.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())["remote_calls"], 0)


if __name__ == "__main__":
    unittest.main()
