"""Regressões de staging/destino, links, argumentos e assets dos rascunhos."""
from __future__ import annotations
import sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import markdown_contract as md
import review_readmes as review
import validate_assistant as validator

class MarkdownTests(unittest.TestCase):
    def test_fenced_links_are_not_navigation(self):
        text='[real](README.md)\n```markdown\n![exemplo](nao-publicado.png)\n```\n'
        self.assertEqual([m[1] for m in md.markdown_links(text)], ['README.md'])
    def test_inline_code_is_not_navigation(self):
        self.assertEqual(list(md.markdown_links('`[exemplo](fantasma.md)`')), [])
    def test_tilde_fence(self):
        self.assertEqual(list(md.markdown_links('~~~text\n[x](no.md)\n~~~\n')), [])
    def test_fence_closes_only_with_correct_marker(self):
        self.assertEqual(list(md.markdown_links('````text\n```\n[x](no.md)\n````\n')), [])
    def test_offsets_survive_masking(self):
        text='`ignore`\n[x](abc.md#alvo)';m=next(md.markdown_links(text))
        self.assertEqual(text[m.start(1):m.end(1)], 'abc.md#alvo')
    def test_explicit_anchor(self):
        self.assertIn('alvo',md.anchors('<a id="alvo"></a>\n## Nome'))
    def test_heading_in_code_is_not_anchor(self):
        self.assertNotIn('fake',md.anchors('```markdown\n## Fake\n```'))
    def test_missing_link_detected(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'README.md').write_text('# Hello')
            errors,_,_=review.check_links('[x](missing.md)',r/'README.md',r,{})
            self.assertTrue(errors)
    def test_missing_anchor_detected(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'README.md').write_text('# Hello')
            errors,_,_=review.check_links('[x](#missing)',r/'README.md',r,{})
            self.assertTrue(errors)
    def test_validator_still_rejects_real_broken_link(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'README.md').write_text('```markdown\n[x](example.md)\n```\n[x](broken.md)')
            errors=[];validator.check_markdown(r,errors)
            self.assertEqual(len(errors),1)
            self.assertIn('broken.md',errors[0])

class ReviewTests(unittest.TestCase):
    def test_actual_candidate_static_gate(self):
        result=review.audit()
        self.assertEqual(result['errors'],[])
        self.assertEqual(result['documents'],10)
        self.assertEqual(result['unique_images'],23)
    def test_mapping_targets_unique(self):
        docs=review.load_mapping();self.assertEqual(len({d['target'] for d in docs}),10)
    def test_rebase_keeps_fenced_examples(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d)
            text='[x](README.md)\n```markdown\n[x](README.md)\n```'
            out=review.translated(text,r/'draft/a.md',r/'prod/a.md',{},r)
            self.assertIn('[x](../draft/README.md)',out)
            self.assertIn('```markdown\n[x](README.md)',out)
    def test_virtual_link_uses_candidate_target(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);virtual={(r/'README.md').resolve():'# Novo'}
            e,_,_=review.check_links('[x](README.md#novo)',r/'a.md',r,virtual)
            self.assertEqual(e,[])
    def test_export_cannot_overwrite_product(self):
        with self.assertRaises(ValueError):review.export(review.ROOT, review.ROOT/'ambiente_fonte')
    def test_confined_rejects_traversal(self):
        with self.assertRaises(ValueError):review.confined(review.ROOT,'../segredo')
    def test_confined_rejects_absolute(self):
        with self.assertRaises(ValueError):review.confined(review.ROOT,'/tmp/fora')
    def test_contract_rejects_bad_parameter(self):
        text='```python\nfrom hub_scripts.data_quality_check import data_quality_check\ndata_quality_check("t", ["id"], primary_keys=["id"])\n```'
        e,n=review.import_contracts(text,review.ROOT)
        self.assertTrue(any('primary_keys' in x for x in e));self.assertEqual(n,1)
    def test_contract_rejects_missing_argument(self):
        text='```python\nfrom hub_scripts.data_quality_check import data_quality_check\ndata_quality_check("t")\n```'
        e,_=review.import_contracts(text,review.ROOT);self.assertTrue(any('pk_columns' in x for x in e))
    def test_png_rejects_non_png(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.png';p.write_bytes(b'not-an-image')
            with self.assertRaises(ValueError):review.png_contract(p)

if __name__=='__main__':unittest.main(verbosity=2)
