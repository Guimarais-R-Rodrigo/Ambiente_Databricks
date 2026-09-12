"""Gates da integração Concierge: referências e distribuição, não roteamento LLM."""
from __future__ import annotations

import ast
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from project_policy import EXPECTED_SKILL_NAMES
import validate_assistant
import publicar_free
import ci_local

HUB = ROOT / 'ambiente_fonte/.assistant'
SKILL = HUB / 'skills/hub-ml-concierge'


class ConciergeIntegrationTests(unittest.TestCase):
    def test_policy_and_discovery_folders_agree(self) -> None:
        problems: list[str] = []
        n = validate_assistant.check_skill_frontmatter(ROOT / 'ambiente_fonte', problems)
        self.assertIn('hub-ml-concierge', EXPECTED_SKILL_NAMES)
        self.assertEqual(problems, [])
        self.assertEqual(n, len(EXPECTED_SKILL_NAMES))

    def test_description_only_selects_discovery_contract(self) -> None:
        fields, error = validate_assistant._parse_frontmatter_subset(
            (SKILL / 'SKILL.md').read_text(encoding='utf-8'), SKILL / 'SKILL.md')
        self.assertIsNone(error)
        self.assertEqual(set(fields), {'name', 'description'})
        self.assertIn('descoberta', fields['description'])
        self.assertIn('Não substitui', fields['description'])
        self.assertLessEqual(len(fields['description']), 1024)
        # Presença de texto delimita o contrato; não prova seleção pelo modelo.

    def test_personal_instructions_have_optional_route(self) -> None:
        text = (ROOT / 'ambiente_fonte/.assistant_instructions.md').read_text(encoding='utf-8')
        self.assertIn('| Descobrir o que o Hub oferece, por onde começar ou como combinar recursos | `hub-ml-concierge` |', text)
        self.assertIn('Concierge é opcional', text)
        self.assertLessEqual(len(text), 20000)

    def test_manual_inventory_and_reading_copy(self) -> None:
        text = (HUB / 'MANUAL_TECNICO.md').read_text(encoding='utf-8')
        self.assertEqual((HUB / 'MANUAL_TECNICO.md').read_bytes(), (ROOT / 'MANUAL_TECNICO.md').read_bytes())
        self.assertEqual(text.count('| `hub-ml-concierge` |'), 1)
        self.assertIn('### 28.5. Concierge:', text)
        self.assertIn('publicação e testes conversacionais pendentes', text)

    def test_declared_helper_paths_exist_without_importing(self) -> None:
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        names = set(re.findall(r'`(hub_(?:snippets|scripts)\.[a-z0-9_.]+)`', text))
        self.assertGreaterEqual(len(names), 7)
        for name in names:
            with self.subTest(helper=name):
                folder = HUB.joinpath(*name.split('.'))
                self.assertTrue((folder / '__init__.py').is_file())
                self.assertTrue((folder / (folder.name + '.py')).is_file())
                self.assertTrue((folder / ('exemplo_' + folder.name + '.py')).is_file())
        # Leitura e presença não equivalem a execução nem adequação semântica.

    def test_example_public_symbols_are_exported(self) -> None:
        folder = HUB / 'hub_snippets/constants/format_br'
        exports: set[str] = set()
        for node in ast.walk(ast.parse((folder / '__init__.py').read_text(encoding='utf-8'))):
            if isinstance(node, ast.ImportFrom):
                exports.update(alias.asname or alias.name for alias in node.names)
        self.assertTrue({'fmt_brl', 'fmt_pct'} <= exports)
        tree = ast.parse((folder / 'format_br.py').read_text(encoding='utf-8'))
        definitions = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        self.assertTrue({'fmt_brl', 'fmt_pct'} <= definitions)

    def test_package_links_and_matrix_are_valid(self) -> None:
        file = SKILL / 'tests/validar_pacote.py'
        spec = importlib.util.spec_from_file_location('concierge_package_validator', file)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # importa só o validador conhecido, nunca helpers.
        self.assertEqual(module.validate(SKILL), [])

    def test_fixtures_never_claim_conversational_pass(self) -> None:
        matrix = json.loads((SKILL / 'tests/casos_aceite.json').read_text(encoding='utf-8'))
        self.assertTrue(matrix['cases'])
        self.assertTrue(all(c['execution_status'] == 'PENDENTE' for c in matrix['cases']))
        self.assertEqual({c['category'] for c in matrix['cases']}, {'positive', 'negative', 'mention', 'edge'})

    def test_rendered_skill_matches_source_bytes(self) -> None:
        target = ROOT / 'Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge'
        def inventory(root: Path) -> dict[str, bytes]:
            return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc', '.pyo'}}
        source = inventory(SKILL)
        self.assertTrue(source)
        self.assertEqual(source, inventory(target))

    def test_publisher_knows_skill_without_remote_calls(self) -> None:
        self.assertIn('hub-ml-concierge', publicar_free.EXPECTED_SKILL_NAMES)
        target = ROOT / 'Novo_Ambiente_Simulado/Users/usuario-free'
        self.assertEqual(publicar_free.conferir_fonte_espelho(target), [])

    def test_forward_cases_and_pending_state_are_documented(self) -> None:
        folder = ROOT / 'docs/testes/forward'
        plan = (folder / 'roteiro.md').read_text(encoding='utf-8')
        for marker in ('### 14P', '### 14N', '### 14M'):
            self.assertIn(marker, plan)
        status = (folder / 'README.md').read_text(encoding='utf-8')
        self.assertIn('PENDENTES', status)
        self.assertIn('não homologa o conjunto ampliado', status)

    def test_ci_includes_all_local_concierge_stages(self) -> None:
        stages = {name for name, _, _ in ci_local.ETAPAS}
        self.assertTrue({'concierge-pacote', 'concierge-regressoes', 'concierge-integracao'} <= stages)


if __name__ == '__main__':
    unittest.main()
