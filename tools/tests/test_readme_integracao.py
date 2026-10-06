"""Regressões de convivência READMEs/Concierge, sem executar helpers ou conversas.

A integração R02-I encontrou duas implementações válidas de ci_local.py que,
se substituídas uma pela outra, descartariam gates. Confere o conjunto real e
mutantes, a unicidade de ADRs e as rotas complementares; não certifica pedagogia.
"""
from __future__ import annotations

import fnmatch
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import ci_local

REQUIRED = {
    'validacao', 'biblioteca', 'ferramentas', 'transicao', 'readmes',
    'concierge-pacote', 'concierge-regressoes', 'concierge-integracao',
}


def stage_errors(stages: list) -> list[str]:
    """Recusa perda/duplicação de etapa e descoberta que exclua regressões antigas."""
    names = [name for name, _description, _command in stages]
    errors = [f'etapa ausente: {name}' for name in sorted(REQUIRED - set(names))]
    if len(names) != len(set(names)):
        errors.append('etapa duplicada')
    commands = {name: command for name, _description, command in stages}
    validation = commands.get('validacao', [])
    if '--conferir-readme' not in validation:
        errors.append('conferência do README removida')
    command = commands.get('readmes', [])
    try:
        pattern = command[command.index('-p') + 1]
        folder = command[command.index('-s') + 1]
    except (ValueError, IndexError):
        errors.append('descoberta de regressões READMEs ausente')
    else:
        if 'unittest' not in command or 'discover' not in command or folder != 'tools/tests':
            errors.append('executor READMEs divergente')
        for filename in ('test_readme_objeto_contract.py', 'test_readme_integracao.py'):
            if not fnmatch.fnmatchcase(filename, pattern):
                errors.append(f'regressão fora da descoberta: {filename}')
    return errors


def duplicate_adrs(names: list[str]) -> set[str]:
    """Só arquivos decisórios entram; texto histórico não é um novo ADR."""
    seen: set[str] = set()
    duplicates: set[str] = set()
    for name in names:
        match = re.fullmatch(r'ADR-(\d{4})-.+\.md', name)
        if match:
            number = match[1]
            if number in seen:
                duplicates.add(number)
            seen.add(number)
    return duplicates


class ReadmeConciergeIntegrationTests(unittest.TestCase):
    def test_actual_stage_union_is_valid(self) -> None:
        self.assertEqual(stage_errors(ci_local.ETAPAS), [])

    def test_each_missing_stage_is_rejected(self) -> None:
        for name in REQUIRED:
            with self.subTest(stage=name):
                mutant = [s for s in ci_local.ETAPAS if s[0] != name]
                self.assertIn(f'etapa ausente: {name}', stage_errors(mutant))

    def test_duplicate_stage_is_rejected(self) -> None:
        self.assertIn('etapa duplicada', stage_errors(ci_local.ETAPAS + [ci_local.ETAPAS[0]]))

    def test_weakened_readme_validation_is_rejected(self) -> None:
        mutant = [(n, d, [x for x in c if x != '--conferir-readme'])
                  if n == 'validacao' else (n, d, c) for n, d, c in ci_local.ETAPAS]
        self.assertIn('conferência do README removida', stage_errors(mutant))

    def test_discovery_cannot_omit_original_readme_tests(self) -> None:
        mutant = [(n, d, [x.replace('test_readme*.py', 'test_readme_integracao.py') for x in c])
                  if n == 'readmes' else (n, d, c) for n, d, c in ci_local.ETAPAS]
        self.assertIn('regressão fora da descoberta: test_readme_objeto_contract.py', stage_errors(mutant))

    def test_actual_adr_numbers_are_unique(self) -> None:
        names = [p.name for p in (ROOT / 'docs/decisions').glob('ADR-*.md')]
        self.assertTrue(names)
        self.assertEqual(duplicate_adrs(names), set())

    def test_duplicate_adr_number_is_rejected(self) -> None:
        self.assertEqual(duplicate_adrs(['ADR-0011-concierge-hub.md', 'ADR-0011-readmes-de-objeto.md']), {'0011'})

    def test_proposal_and_concierge_have_distinct_routes(self) -> None:
        index = (ROOT / 'docs/decisions/README.md').read_text(encoding='utf-8')
        self.assertIn('(ADR-0011-concierge-hub.md)', index)
        self.assertIn('(ADR-0012-readmes-de-objeto.md)', index)
        self.assertNotIn('(ADR-0011-readmes-de-objeto.md)', index)
        self.assertTrue((ROOT / 'docs/decisions/ADR-0012-readmes-de-objeto.md').is_file())
        self.assertFalse((ROOT / 'docs/decisions/ADR-0011-readmes-de-objeto.md').exists())

    def test_instructions_preserve_both_optional_discovery_and_readme_contract(self) -> None:
        text = (ROOT / 'ambiente_fonte/.assistant_instructions.md').read_text(encoding='utf-8')
        self.assertIn('Concierge é opcional', text)
        self.assertIn('hub-ml-concierge', text)
        self.assertIn('README', text)
        self.assertIn('README não executa helper', text)
        self.assertLessEqual(len(text), 20_000)

    def test_manual_and_instructions_mirrors_match(self) -> None:
        source = ROOT / 'ambiente_fonte'
        target = ROOT / '.artifacts/simulado/Users/usuario-free'
        for rel in ('.assistant_instructions.md', '.assistant/MANUAL_TECNICO.md'):
            with self.subTest(path=rel):
                self.assertEqual((source / rel).read_bytes(), (target / rel).read_bytes())
        self.assertEqual((ROOT / 'MANUAL_TECNICO.md').read_bytes(), (source / '.assistant/MANUAL_TECNICO.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
