"""Shared AI/general link scanner regressions for integrated audit AI-GAP-03."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_controls as ai
import validate_assistant as validator
from markdown_links import markdown_destinations, local_destination_path


class MarkdownDestinationTests(unittest.TestCase):
    def test_inline_images_angles_titles_parentheses_and_escapes(self):
        text = r'''[basic](guide.md) ![image](image.png)
[space](<guide with space.md> "a title")
[title](guide.md 'single title') [title](guide.md (parenthesized title))
[nested [label]](guide_(one).md) [escaped](guide\(one\).md)
[entity](guide&amp;one.md)'''
        self.assertEqual(list(markdown_destinations(text)), [
            'guide.md', 'image.png', 'guide with space.md', 'guide.md', 'guide.md',
            'guide_(one).md', 'guide(one).md', 'guide&one.md'])

    def test_references_full_collapsed_shortcut_and_case_fold(self):
        text = '''[full][Some Label] ![image][some label] [collapsed][] [shortcut]

[some   LABEL]: <some guide.md> "title"
[collapsed]: collapsed.md
[shortcut]: shortcut.md
'''
        self.assertEqual(list(markdown_destinations(text)), [
            'some guide.md', 'some guide.md', 'collapsed.md', 'shortcut.md'])

    def test_reference_destination_on_next_line_and_first_definition_wins(self):
        text = '[link][ref]\n\n[ref]:\n  <first guide.md>\n[ref]: ignored.md\n'
        self.assertEqual(list(markdown_destinations(text)), ['first guide.md'])

    def test_fences_inline_code_html_comments_and_escaped_markup_not_links(self):
        text = '''```md
[code](missing.md)
```
~~~md
[code][ref]
[ref]: missing.md
~~~
`[inline](missing.md)` <!-- [hidden](missing.md) -->
\\[escaped](missing.md)
[visible](good.md)
'''
        self.assertEqual(list(markdown_destinations(text)), ['good.md'])

    def test_plain_undefined_reference_and_unused_definition_not_links(self):
        self.assertEqual(list(markdown_destinations('[plain] [plain][undefined]\n\n[unused]: absent.md\n')), [])

    def test_linked_image_inline_and_reference_destinations_are_both_visible(self):
        text = '[![inline](inner.png)](outer.md) [![ref][image]][page]\n\n[image]: inner2.png\n[page]: outer2.md\n'
        self.assertEqual(list(markdown_destinations(text)), ['inner.png', 'outer.md', 'inner2.png', 'outer2.md'])

    def test_blockquote_and_list_reference_definitions_resolve(self):
        for text in ('> [text][ref]\n>\n> [ref]: target.md\n',
                     '- [text][ref]\n\n  [ref]: target.md\n',
                     '> - [text][ref]\n>\n>   [ref]: target.md\n',
                     '1. [text][ref]\n\n   [ref]: target.md\n',
                     '[text][ref]\n\n- > [ref]: target.md\n'):
            with self.subTest(text=text):
                self.assertEqual(list(markdown_destinations(text)), ['target.md'])

    def test_nested_normal_link_keeps_inner_link_and_outer_literal(self):
        text = '[outer [inner](inner.md)](literal.md)'
        self.assertEqual(list(markdown_destinations(text)), ['inner.md'])

    def test_quoted_and_list_fenced_examples_stay_masked(self):
        for prefix, continuation in (('> ', '> '), ('- ', '  ')):
            text = prefix + '```md\n' + continuation + '[example](missing.md)\n' + continuation + '```\n[real](present.md)\n'
            self.assertEqual(list(markdown_destinations(text)), ['present.md'])

    def test_url_parts_decoded_after_query_and_fragment_split(self):
        self.assertEqual(local_destination_path('file%23name%3F.md?raw=1#section'), 'file#name?.md')
        self.assertEqual(local_destination_path('with%20space.md'), 'with space.md')
        for raw in ('HTTPS://example.org/page', 'mailto:test@example.org', '//example.org/page', '#anchor'):
            self.assertIsNone(local_destination_path(raw))


class SharedLinkGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='markdown links with spaces ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.origin = self.root / 'README.md'
        for name in ('Present.md', 'with space.md', 'file#name?.md', 'paren(one).md'):
            (self.root / name).write_text('# Existing anchor\n', encoding='utf-8')

    def ai_errors(self, text):
        errors = []
        for target in markdown_destinations(text):
            try:
                ai.check_link(self.root, 'README.md', target)
            except ai.ContractError as exc:
                errors.append(str(exc))
        return errors

    def validator_errors(self, text):
        self.origin.write_text(text, encoding='utf-8')
        errors = []
        validator.check_markdown(self.root, errors)
        return errors

    def test_reference_angle_encoded_and_case_mutants_fail_both_entrypoints(self):
        for text in ('[required][ref]\n\n[ref]: missing.md\n',
                     '[required](<missing space.md>)', '[required](missing%20space.md)',
                     '[required][ref]\n\n[ref]: present.md\n', '[required](<present.md>)'):
            with self.subTest(text=text):
                self.assertTrue(self.ai_errors(text))
                self.assertTrue(self.validator_errors(text))

    def test_valid_reference_angle_encoded_escape_and_case_pass_both(self):
        text = r'''[reference][ref] [angle](<with space.md>)
[encoded](with%20space.md) [case](Present.md)
[punctuation](file%23name%3F.md) [parens](paren\(one\).md)

[ref]: Present.md#existing-anchor
'''
        self.assertEqual([], self.ai_errors(text))
        self.assertEqual([], self.validator_errors(text))

    def test_fenced_examples_do_not_mask_real_missing_target(self):
        text = '```md\n[example](absent-example.md)\n```\n[actual](actual-missing.md)\n'
        for errors in (self.ai_errors(text), self.validator_errors(text)):
            self.assertEqual(len(errors), 1)
            self.assertIn('actual-missing.md', errors[0])

    def test_nested_image_resource_and_container_reference_mutants(self):
        for text in ('[![image](missing.png)](Present.md)',
                     '> [link][ref]\n>\n> [ref]: missing.md\n',
                     '- [link][ref]\n\n  [ref]: missing.md\n',
                     '[link][ref]\n\n- > [ref]: missing.md\n',
                     '[outer [inner](missing.md)](Present.md)'):
            with self.subTest(text=text):
                self.assertTrue(self.ai_errors(text))
                self.assertTrue(self.validator_errors(text))
        valid = '[![image](Present.md)](Present.md)\n> [link][ref]\n>\n> [ref]: Present.md\n[outer [inner](Present.md)](not-an-active-target.md)\n'
        self.assertEqual([], self.ai_errors(valid))
        self.assertEqual([], self.validator_errors(valid))

    def test_reference_anchor_checked_by_ai_and_path_by_general_validator(self):
        text = '[link][ref]\n\n[ref]: Present.md#missing-anchor\n'
        self.assertIn('ANCHOR_MISSING', self.ai_errors(text)[0])
        # The general validator preserves its path-only contract.
        self.assertEqual([], self.validator_errors(text))

    def test_angle_traversal_and_symlink_still_rejected_by_ai(self):
        self.assertIn('LINK_OUTSIDE_ROOT', self.ai_errors('[escape](<../outside.md>)')[0])
        (self.root / 'link.md').symlink_to(self.root / 'Present.md')
        self.assertIn('SYMLINK', self.ai_errors('[link](<link.md>)')[0])

    def test_repo_and_untracked_scanners_use_shared_reference_parser(self):
        self.origin.write_text('[required][ref]\n\n[ref]: missing.md\n', encoding='utf-8')
        with patch.object(validator, 'REPO_ROOT', self.root), patch.object(validator, 'iter_repo_files', return_value=[self.origin]):
            errors = []
            self.assertEqual(validator.check_repo_links(self.root / 'product', errors), 1)
            self.assertEqual(len(errors), 1)
        with patch.object(validator, 'REPO_ROOT', self.root), patch.object(validator, 'git_paths', return_value=[self.origin]):
            errors = []
            validator.check_worktree_hygiene(errors)
            self.assertEqual(len(errors), 1)
            self.assertIn('missing.md', errors[0])

    def test_notebook_multiline_reference_and_code_examples(self):
        notebook = self.root / 'example.py'
        notebook.write_text('''# Databricks notebook source
# MAGIC %md
# MAGIC [valid][ref]
# MAGIC [ref]: Present.md
# MAGIC ```md
# MAGIC [example](absent-example.md)
# MAGIC ```
# MAGIC [actual](actual-missing.md)
print("[python literal](not-markdown.md)")
''', encoding='utf-8')
        errors = []
        count, links = validator.check_notebook_links(self.root, errors)
        self.assertEqual((count, links), (1, 2))
        self.assertEqual(len(errors), 1)
        self.assertIn('actual-missing.md', errors[0])


if __name__ == '__main__':
    unittest.main()
