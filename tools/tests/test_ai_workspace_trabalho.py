"""Fixtures sintéticas: destinos, isolamento Git e payload sem configuração."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.trabalho import workspace as w


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'config').mkdir()
        (self.root / '.gitignore').write_text('*.local.json\n', encoding='utf-8')
        self.data = {'schema_version': 1, 'profile': 'synthetic',
                     'expected_host': 'https://workspace.example.test',
                     'development_root': '/Users/synthetic/dev',
                     'installation_root': '/Users/synthetic/hub'}
        self.file = self.root / 'config/workspace.local.json'
        self.profiles = self.root / 'profiles.fixture'
        self.profiles.write_text('[synthetic]\nhost = https://workspace.example.test\n', encoding='utf-8')
        self.save()

    def save(self):
        self.file.write_text(json.dumps(self.data), encoding='utf-8')

    def test_valid_local_profile(self):
        self.assertEqual(w.load(self.root, self.profiles), self.data)

    def test_missing_config(self):
        self.file.unlink()
        with self.assertRaisesRegex(w.ConfigError, 'CONFIG_MISSING'):
            w.load(self.root, self.profiles)

    def test_duplicate_field_rejected(self):
        self.file.write_text('{"schema_version": 1, "schema_version": 2}', encoding='utf-8')
        with self.assertRaisesRegex(w.ConfigError, 'CONFIG_DUPLICATE_FIELD'):
            w.load(self.root, self.profiles)

    def test_host_mismatch_without_value_leak(self):
        self.profiles.write_text('[synthetic]\nhost=https://different.example.test\n', encoding='utf-8')
        with self.assertRaisesRegex(w.ConfigError, '^PROFILE_HOST_MISMATCH$'):
            w.load(self.root, self.profiles)

    def test_environment_host_mismatch_rejected(self):
        with patch.dict('os.environ', {'DATABRICKS_HOST': 'https://different.example.test'}):
            with self.assertRaisesRegex(w.ConfigError, '^ENV_HOST_MISMATCH$'):
                w.load(self.root, self.profiles)

    def test_unknown_fields_and_secrets_rejected(self):
        for key in ('token', 'password', 'unexpected'):
            with self.subTest(key=key):
                with self.assertRaisesRegex(w.ConfigError, 'CONFIG_SCHEMA'):
                    w.validate(dict(self.data, **{key: 'synthetic'}))

    def test_unsafe_roots_rejected(self):
        for path in ('/Users', '/Users/synthetic', '/Shared/hub', '/Users/synthetic/../shared',
                     '/Users/synthetic//hub', '/Users/USUARIO_EXEMPLO/hub', '/Users/synthetic/hub/'):
            with self.subTest(path=path), self.assertRaises(w.ConfigError):
                w.validate(dict(self.data, installation_root=path))

    def test_overlap_and_different_owner_rejected(self):
        for path in ('/Users/synthetic/dev', '/Users/synthetic/dev/hub', '/Users/other/hub'):
            with self.subTest(path=path), self.assertRaises(w.ConfigError):
                w.validate(dict(self.data, installation_root=path))

    def test_host_auth_query_path_and_example_rejected(self):
        for url in ('http://workspace.example.test', 'https://u:p@workspace.example.test',
                    'https://workspace.example.test?token=synthetic', 'https://workspace.example.test/path',
                    'https://workspace.example.invalid', 'https://workspace.example.test:bad'):
            with self.subTest(url=url), self.assertRaises(w.ConfigError):
                w.validate(dict(self.data, expected_host=url))

    def test_force_tracked_local_config_rejected(self):
        subprocess.run(['git', 'add', '-f', 'config/workspace.local.json'], cwd=self.root, check=True)
        with self.assertRaisesRegex(w.ConfigError, 'CONFIG_MUST_BE_IGNORED'):
            w.load(self.root, self.profiles)

    def test_ignored_config_not_in_git_inventory(self):
        output = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=self.root)
        self.assertNotIn(b'workspace.local.json', output)

    def test_plan_payload_and_two_users(self):
        source = self.root / 'ambiente_databricks'
        (source / '.assistant').mkdir(parents=True)
        (source / '.assistant_instructions.md').write_text('synthetic', encoding='utf-8')
        (source / '.assistant/test.txt').write_text('synthetic', encoding='utf-8')
        subprocess.run(['git', 'add', '.gitignore', 'ambiente_databricks'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.test',
                        'commit', '-qm', 'fixture'], cwd=self.root, check=True)
        first = w.plan(self.root, self.data)
        self.assertEqual(len(first['files']), 2)
        self.assertFalse(any('destination' in f for f in first['files']))
        self.assertNotIn('/Users/', json.dumps(first))
        a = w.plan(self.root, self.data, True)
        b = w.plan(self.root, dict(self.data, development_root='/Users/other/dev', installation_root='/Users/other/hub'), True)
        self.assertEqual([f['sha256'] for f in a['files']], [f['sha256'] for f in b['files']])
        self.assertNotEqual(a['files'][0]['destination'], b['files'][0]['destination'])


if __name__ == '__main__':
    unittest.main()
