"""Regressões V02: dados hostis, isolamento, integridade e ausência de efeitos.

Sem dados corporativos. Os testes de filesystem usam exclusivamente pastas
sintéticas temporárias; resolver temas não publica nem aplica gráficos.
"""
from __future__ import annotations

import copy
from dataclasses import FrozenInstanceError, replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / 'ambiente_fonte/.assistant'
sys.path.insert(0, str(PRODUCT))
sys.path.insert(0, str(ROOT / 'tools'))
from hub_snippets.visual.tema import (
    ThemeError, ResolvedTheme, resolve_theme, load_theme, load_reference_theme,
    export_theme, normalize_color,
)
from hub_snippets.visual.tema import tema as engine
import temas_v01_contract as legacy


class _ThemeFixture:
    @classmethod
    def setUpClass(cls):
        cls.raw = (PRODUCT/'hub_padroes/identidade_visual/exemplos/legado_notebook.json').read_bytes()
        cls.reference = json.loads(cls.raw)

    def reject(self, code, callback, *args, **kwargs):
        with self.assertRaises(ThemeError) as exc:
            callback(*args, **kwargs)
        self.assertEqual(exc.exception.code, code)
        return exc.exception


class CoreTests(_ThemeFixture, unittest.TestCase):
    def test_reference_contexts(self):
        for ctx, count in [('notebook',48),('readme',32),('presentation',32)]:
            with self.subTest(context=ctx):
                r = load_reference_theme(ctx)
                self.assertEqual(r.to_dict()['context'],ctx)
                self.assertEqual(len(r.tokens),count)

    def test_raw_hash_tracks_original_bytes(self):
        self.assertEqual(resolve_theme(self.raw).raw_sha256,hashlib.sha256(self.raw).hexdigest())

    def test_canonical_hash_tracks_export(self):
        r=resolve_theme(self.raw)
        self.assertEqual(r.content_sha256,hashlib.sha256(export_theme(r)).hexdigest())

    def test_reordered_fields_same_fingerprint(self):
        a=resolve_theme(self.raw)
        b=resolve_theme(json.dumps(dict(reversed(list(self.reference.items())))).encode())
        self.assertEqual(a.fingerprint,b.fingerprint)
        self.assertNotEqual(a.raw_sha256,b.raw_sha256)

    def test_numeric_representation_same_fingerprint(self):
        v=copy.deepcopy(self.reference);v['tokens']['chart.width_px']=900.0
        self.assertEqual(resolve_theme(v).fingerprint,resolve_theme(self.raw).fingerprint)

    def test_change_token_changes_fingerprint(self):
        v=copy.deepcopy(self.reference);v['tokens']['brand.primary']='#112233'
        self.assertNotEqual(resolve_theme(v).fingerprint,resolve_theme(self.raw).fingerprint)

    def test_export_reimport_preserves_effective_values(self):
        a=resolve_theme(self.raw);b=resolve_theme(export_theme(a))
        self.assertEqual(a.to_dict(),b.to_dict());self.assertEqual(a.fingerprint,b.fingerprint)

    def test_no_approval_or_provenance_in_export(self):
        r=load_reference_theme();data=json.loads(export_theme(r))
        self.assertEqual(set(data),set(self.reference))
        self.assertNotIn('fingerprint',data);self.assertNotIn('source',data)
        self.assertIn('CONTRATO_VALIDADO_NAO_APROVADO',r.warnings)

    def test_nested_tokens_cannot_be_mutated(self):
        r=resolve_theme(self.raw)
        with self.assertRaises(TypeError):r.tokens['palette.categorical'][0]='#FFFFFF'
        with self.assertRaises(TypeError):r.tokens['brand.primary']='#FFFFFF'

    def test_input_mutation_does_not_contaminate(self):
        data=copy.deepcopy(self.reference);r=resolve_theme(data)
        data['tokens']['palette.categorical'][0]='#FFFFFF'
        self.assertEqual(r.tokens['palette.categorical'][0],'#005CA9')

    def test_output_copy_mutation_does_not_contaminate(self):
        r=resolve_theme(self.raw);data=r.to_dict();data['tokens']['palette.categorical'].clear()
        self.assertEqual(len(r.tokens['palette.categorical']),10)

    def test_two_instances_are_isolated(self):
        a=resolve_theme(self.raw);v=copy.deepcopy(self.reference);v['tokens']['brand.primary']='#000000';b=resolve_theme(v)
        self.assertEqual(a.tokens['brand.primary'],'#005CA9');self.assertEqual(b.tokens['brand.primary'],'#000000')

    def test_result_and_origins_are_frozen(self):
        r=resolve_theme(self.raw)
        with self.assertRaises(FrozenInstanceError):r.source='other'
        with self.assertRaises(TypeError):r.origins['brand.primary']='other'
        self.assertEqual(set(r.origins),set(r.tokens))

    def test_expected_context_match(self):
        self.assertEqual(resolve_theme(self.raw,expected_context='notebook').to_dict()['context'],'notebook')

    def test_expected_context_mismatch(self):
        self.reject('CONTEXT_MISMATCH',resolve_theme,self.raw,expected_context='readme')

    def test_invalid_expected_context(self):
        for ctx in ('app',{},1):self.reject('CONTEXT_EXPECTED',resolve_theme,self.raw,expected_context=ctx)

    def test_unknown_reference_context(self):self.reject('CONTEXT_EXPECTED',load_reference_theme,'app')
    def test_reference_context_unhashable(self):self.reject('CONTEXT_EXPECTED',load_reference_theme,{})
    def test_string_is_not_json_bytes(self):self.reject('JSON_INPUT_TYPE',resolve_theme,self.raw.decode())
    def test_programmatic_cycle(self):
        data={};data['self']=data;self.reject('JSON_CYCLE',resolve_theme,data)
    def test_programmatic_custom_objects(self):self.reject('JSON_VALUE_TYPE',resolve_theme,{'x':object()})
    def test_programmatic_nonstring_key(self):self.reject('JSON_VALUE_TYPE',resolve_theme,{1:'x'})
    def test_programmatic_nan(self):self.reject('JSON_NONFINITE',resolve_theme,{'x':float('nan')})
    def test_programmatic_depth(self):
        data={};v=data
        for _ in range(14):v['x']={};v=v['x']
        self.reject('JSON_DEPTH',resolve_theme,data)
    def test_programmatic_nodes_limit(self):self.reject('JSON_NODES',resolve_theme,{'x':[0]*8200})
    def test_programmatic_text_limit(self):self.reject('JSON_SIZE',resolve_theme,{'x':'a'*131073})
    def test_programmatic_integer_limit(self):self.reject('JSON_SIZE',resolve_theme,{'x':1<<4097})
    def test_duplicate_json_keys(self):self.reject('JSON_DUPLICATE',resolve_theme,b'{"x":1,"x":2}')
    def test_byte_limit(self):self.reject('JSON_SIZE',resolve_theme,b' '*131073)
    def test_json_depth_limit(self):self.reject('JSON_DEPTH',resolve_theme,b'['*13+b'0'+b']'*13)
    def test_json_encoding(self):self.reject('JSON_ENCODING',resolve_theme,b'\xff')
    def test_json_bom(self):self.reject('JSON_ENCODING',resolve_theme,b'\xef\xbb\xbf{}')
    def test_json_unicode_surrogate(self):self.reject('JSON_UNICODE',resolve_theme,b'{"a":"\\ud800"}')
    def test_json_infinite(self):self.reject('JSON_NONFINITE',resolve_theme,b'{"a":1e999}')
    def test_empty_bytes(self):self.reject('JSON_SYNTAX',resolve_theme,b'')

    def test_missing_field_does_not_fill_default(self):
        v=copy.deepcopy(self.reference);del v['tokens']['brand.primary']
        exc=self.reject('SCHEMA_REQUIRED',resolve_theme,v)
        self.assertEqual(exc.field,'$.tokens.brand.primary');self.assertNotIn('brand.primary',v['tokens'])

    def test_unknown_field_does_not_expose_value(self):
        v=copy.deepcopy(self.reference);v['confidential-marker']='secret-test'
        exc=self.reject('SCHEMA_ADDITIONALPROPERTIES',resolve_theme,v)
        self.assertNotIn('secret-test',str(exc));self.assertNotIn('confidential-marker',str(exc))
        self.assertTrue(exc.action)

    def test_no_publishing_flags(self):
        for name in ('approved','role','scope','permissions','css','extends'):
            with self.subTest(name=name):
                v=copy.deepcopy(self.reference);v[name]=True
                self.reject('SCHEMA_ADDITIONALPROPERTIES',resolve_theme,v)

    def test_no_analytic_parameters(self):
        v=copy.deepcopy(self.reference);v['tokens']['score.threshold']=.8
        self.reject('SCHEMA_ADDITIONALPROPERTIES',resolve_theme,v)

    def test_old_and_new_validation_share_functions(self):
        self.assertIs(legacy.strict_json,engine._strict_json)
        self.assertIs(legacy.validate_theme,engine._validate_theme)
        self.assertIs(legacy.ContractError,ThemeError)

    def test_engine_future_version(self):
        v=copy.deepcopy(self.reference);v['engine_compatibility']['minimum_version']='1.1.0'
        self.reject('ENGINE_VERSION',resolve_theme,v)

    def test_even_diverging_palette(self):
        v=copy.deepcopy(self.reference);v['tokens']['palette.diverging'].pop()
        self.reject('PALETTE_CENTER',resolve_theme,v)

    def test_normalize_color_explicit(self):self.assertEqual(normalize_color('#abcdef'),'#ABCDEF')
    def test_normalize_color_rejects_ambiguous_forms(self):
        for v in ('#fff','#FFFFFF00',' #FFFFFF','#FFFFFF\n','red',None,12):
            self.reject('COLOR_FORMAT',normalize_color,v)
    def test_lowercase_import_is_not_silently_fixed(self):
        v=copy.deepcopy(self.reference);v['tokens']['brand.primary']='#abcdef'
        self.reject('SCHEMA_PATTERN',resolve_theme,v)

    def test_no_socket_calls(self):
        with patch('socket.socket',side_effect=AssertionError('rede proibida')):
            self.assertEqual(len(resolve_theme(self.raw).tokens),48)

    def test_export_is_bytes_and_does_not_write(self):
        r=resolve_theme(self.raw)
        with patch.object(Path,'write_bytes',side_effect=AssertionError('escrita proibida')):
            raw=export_theme(r)
        self.assertIsInstance(raw,bytes);self.assertTrue(raw.endswith(b'\n'))

    def test_export_rejects_dictionary(self):self.reject('RESULT_TYPE',export_theme,self.reference)
    def test_export_checks_result_integrity(self):
        r=resolve_theme(self.raw);r=replace(r,fingerprint='0'*64)
        self.reject('RESULT_INTEGRITY',export_theme,r)

    def test_schema_resource_tampered(self):
        original=engine._read_bytes
        def reader(path,limit=engine._MAX_BYTES):
            if Path(path).name=='theme.schema.json':return b'{}'
            return original(path,limit)
        with patch.object(engine,'_read_bytes',reader):self.reject('RESOURCE_HASH',resolve_theme,self.raw)

    def test_asset_resource_tampered(self):
        original=engine._read_bytes
        def reader(path,limit=engine._MAX_BYTES):
            if Path(path).suffix=='.png':return b'changed'
            return original(path,limit)
        with patch.object(engine,'_read_bytes',reader):self.reject('ASSET_HASH',load_reference_theme,'readme')

    def test_no_global_cache_for_schema(self):
        first=resolve_theme(self.raw)
        with patch.object(engine,'_resource',side_effect=ThemeError('RESOURCE_HASH','changed')):
            self.reject('RESOURCE_HASH',resolve_theme,self.raw)
        self.assertEqual(resolve_theme(self.raw).fingerprint,first.fingerprint)

    def test_missing_dependencies_reported_without_install(self):
        code = "import sys;sys.path.insert(0,sys.argv[1]);from hub_snippets.visual.tema import load_reference_theme,ThemeError\ntry:load_reference_theme()\nexcept ThemeError as e:print(e.code)"
        p=subprocess.run([sys.executable,'-B','-S','-c',code,str(PRODUCT)],capture_output=True,text=True,timeout=15)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stdout.strip(),'DEPENDENCY_MISSING')

    def test_import_without_third_party_modules_or_platform(self):
        code="import sys;sys.path.insert(0,sys.argv[1]);from hub_snippets.visual.tema import normalize_color;print(normalize_color('#abc123'));assert not any(x in sys.modules for x in ['jsonschema','referencing','pyspark','plotly','pandas','mlflow','streamlit'])"
        p=subprocess.run([sys.executable,'-B','-S','-c',code,str(PRODUCT)],capture_output=True,text=True,timeout=15)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stdout.strip(),'#ABC123')

    def test_api_is_exhaustive(self):
        from api_publica import api_publica,conteudo_init
        base=PRODUCT/'hub_snippets/visual/tema'
        self.assertEqual((base/'__init__.py').read_text(),conteudo_init('tema',api_publica(base/'tema.py')))


class FileTests(_ThemeFixture, unittest.TestCase):
    def test_load_from_explicit_root(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'proposal.json';p.write_bytes(self.raw)
            r=load_theme(td,'proposal.json',expected_sha256=hashlib.sha256(self.raw).hexdigest())
            self.assertEqual(r.source,'proposal.json')
            self.assertEqual(set(r.origins.values()),{'proposal.json'})

    def test_expected_byte_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'proposal.json').write_bytes(self.raw)
            self.reject('HASH_MISMATCH',load_theme,td,'proposal.json',expected_sha256='0'*64)

    def test_hash_format(self):self.reject('HASH_FORMAT',load_theme,'.','x.json',expected_sha256='latest')
    def test_bad_root(self):self.reject('PATH_SCOPE',load_theme,None,'x.json')
    def test_path_traversal(self):self.reject('PATH_SCOPE',load_theme,'.','../x.json')
    def test_path_url(self):self.reject('PATH_SCOPE',load_theme,'.','https://example.invalid/x.json')
    def test_absolute_path(self):self.reject('PATH_SCOPE',load_theme,'.','/tmp/x.json')
    def test_windows_path(self):self.reject('PATH_SCOPE',load_theme,'.','C:\\x.json')
    def test_path_null(self):self.reject('PATH_SCOPE',load_theme,'.','x\x00.json')
    def test_path_repeated_separator(self):self.reject('PATH_SCOPE',load_theme,'.','a//b.json')
    def test_path_wrong_type(self):self.reject('PATH_SCOPE',load_theme,'.',{})
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as td:self.reject('PATH_MISSING',load_theme,td,'missing.json')
    def test_wrong_extension(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'x.txt').write_bytes(self.raw);self.reject('PATH_EXTENSION',load_theme,td,'x.txt')
    def test_symlink_file(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'real.json').write_bytes(self.raw);(Path(td)/'link.json').symlink_to(Path(td)/'real.json')
            self.reject('PATH_SYMLINK',load_theme,td,'link.json')
    def test_symlink_parent(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'real').mkdir();(root/'real/x.json').write_bytes(self.raw);(root/'link').symlink_to(root/'real',target_is_directory=True)
            self.reject('PATH_SYMLINK',load_theme,root,'link/x.json')
    def test_directory_is_not_configuration(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'x.json').mkdir();self.reject('PATH_MISSING',load_theme,td,'x.json')
    def test_fifo_is_not_configuration(self):
        if not hasattr(os,'mkfifo'):self.skipTest('FIFO não existe neste sistema')
        with tempfile.TemporaryDirectory() as td:
            os.mkfifo(Path(td)/'x.json');self.reject('PATH_MISSING',load_theme,td,'x.json')
    def test_no_stale_file_cache(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.json';p.write_bytes(self.raw);a=load_theme(td,'x.json')
            v=copy.deepcopy(self.reference);v['tokens']['brand.primary']='#000000';p.write_text(json.dumps(v))
            b=load_theme(td,'x.json');self.assertNotEqual(a.fingerprint,b.fingerprint)
    def test_oversized_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'x.json').write_bytes(b' '*131073);self.reject('JSON_SIZE',load_theme,td,'x.json')
    def test_permission_error_is_safe(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'x.json').write_bytes(self.raw)
            with patch.object(engine.os,'open',side_effect=PermissionError('private-path')):
                e=self.reject('PATH_READ',load_theme,td,'x.json')
            self.assertNotIn('private-path',str(e))



class LayoutTests(unittest.TestCase):
    def test_real_layout(self):
        from temas_v02_check import check_layout
        self.assertEqual(check_layout()['status'],'PASS_V02_LAYOUT')

    def test_empty_layout_rejected(self):
        from temas_v02_check import check_layout
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError,'V02_INCOMPLETE'):check_layout(Path(td))

    def test_missing_test_file_rejected(self):
        from temas_v02_check import check_layout
        original=Path.is_file
        def check(path):
            return False if path.name=='test_temas_v02.py' else original(path)
        with patch.object(Path,'is_file',check):
            with self.assertRaisesRegex(ValueError,'V02_INCOMPLETE'):check_layout()

    def test_duplicate_schema_rejected(self):
        from temas_v02_check import check_layout
        original=Path.exists
        def exists(path):
            if str(path).endswith('V01/theme.schema.json'):return True
            return original(path)
        with patch.object(Path,'exists',exists):
            with self.assertRaisesRegex(ValueError,'V02_DUPLICATE_SCHEMA'):check_layout()

    def test_derived_fixture_drift_rejected(self):
        from temas_v02_check import check_layout
        original=Path.read_bytes
        def read(path):
            if str(path).endswith('exemplos/legado_notebook.json'):return b'{}'
            return original(path)
        with patch.object(Path,'read_bytes',read):
            with self.assertRaisesRegex(ValueError,'V02_FIXTURE_DRIFT'):check_layout()

    def test_missing_temas_gate_rejected(self):
        import ci_local
        self.assertIn('temas',[s[0] for s in ci_local.ETAPAS])
        command=next(s[2] for s in ci_local.ETAPAS if s[0]=='temas')
        self.assertIn('test_temas*.py',command)



class AdditionalGuards(_ThemeFixture, unittest.TestCase):
    def test_internal_schema_reference_missing(self):
        schema=legacy.read_json(legacy.SCHEMA_PATH)
        schema['properties']['tokens']={'$ref':'#/$defs/absent'}
        self.reject('SCHEMA_LOCAL_REF',engine._schema_validator,schema)

    def test_internal_schema_reference_cycle(self):
        schema=legacy.read_json(legacy.SCHEMA_PATH)
        schema['$defs']['loop']={'$ref':'#/$defs/loop'}
        self.reject('SCHEMA_CYCLE',engine._schema_validator,schema)

    def test_schema_nested_id_rejected(self):
        schema=legacy.read_json(legacy.SCHEMA_PATH)
        schema['properties']['tokens']['$id']='urn:other'
        self.reject('SCHEMA_NESTED_ID',engine._schema_validator,schema)

    def test_schema_must_be_object(self):self.reject('SCHEMA_INVALID',engine._schema_validator,[])

    def test_asset_manifest_tampered(self):
        original=engine._read_bytes
        def reader(path,limit=engine._MAX_BYTES):
            return b'{}' if Path(path).name=='assets.json' else original(path,limit)
        with patch.object(engine,'_read_bytes',reader):self.reject('RESOURCE_HASH',resolve_theme,self.raw)

    def test_same_content_from_different_paths_same_fingerprint(self):
        with tempfile.TemporaryDirectory() as td:
            for name in ('one.json','two.json'):(Path(td)/name).write_bytes(self.raw)
            a=load_theme(td,'one.json');b=load_theme(td,'two.json')
            self.assertEqual(a.fingerprint,b.fingerprint);self.assertNotEqual(a.source,b.source)

    def test_file_replaced_during_open_is_rejected(self):
        from types import SimpleNamespace
        original=engine.os.fstat
        def fstat(fd):
            actual=original(fd)
            return SimpleNamespace(st_mode=actual.st_mode,st_dev=actual.st_dev,st_ino=actual.st_ino+1)
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'x.json').write_bytes(self.raw)
            with patch.object(engine.os,'fstat',fstat):self.reject('PATH_CHANGED',load_theme,td,'x.json')

    def test_layout_changed_dictionary(self):
        from temas_v02_check import check_layout
        original=Path.read_text
        def read(path,*args,**kwargs):
            return 'changed' if str(path).endswith('identidade_visual/TOKENS.md') else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            with self.assertRaisesRegex(ValueError,'V02_DICTIONARY'):check_layout()

    def test_layout_changed_api(self):
        from temas_v02_check import check_layout
        original=Path.read_text
        def read(path,*args,**kwargs):
            return '' if str(path).endswith('tema/__init__.py') else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            with self.assertRaisesRegex(ValueError,'V02_API'):check_layout()

    def test_layout_changed_manual(self):
        from temas_v02_check import check_layout
        original=Path.read_bytes
        def read(path):return b'changed' if path==ROOT/'MANUAL_TECNICO.md' else original(path)
        with patch.object(Path,'read_bytes',read):
            with self.assertRaisesRegex(ValueError,'V02_MANUAL'):check_layout()

    def test_layout_changed_schema(self):
        from temas_v02_check import check_layout
        original=Path.read_bytes
        def read(path):return b'{}' if str(path).endswith('identidade_visual/theme.schema.json') else original(path)
        with patch.object(Path,'read_bytes',read):
            with self.assertRaisesRegex(ValueError,'V02_SCHEMA_HASH'):check_layout()

    def test_layout_empty_test_content(self):
        from temas_v02_check import check_layout
        original=Path.read_text
        def read(path,*args,**kwargs):
            return '' if path.name=='test_temas_v02.py' else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            with self.assertRaisesRegex(ValueError,'V02_EMPTY_TESTS'):check_layout()

    def test_layout_parallel_validator(self):
        from temas_v02_check import check_layout
        with patch.object(legacy,'validate_theme',lambda *args:None):
            with self.assertRaisesRegex(ValueError,'V02_VALIDATOR'):check_layout()


class FurtherRegressions(_ThemeFixture, unittest.TestCase):
    def test_export_invalid_canonical_bytes_uses_safe_error(self):
        result=replace(resolve_theme(self.raw),_canonical=b'not-json')
        self.reject('JSON_SYNTAX',export_theme,result)

    def test_export_missing_canonical_uses_safe_error(self):
        result=replace(resolve_theme(self.raw),_canonical=None)
        self.reject('JSON_INPUT_TYPE',export_theme,result)

    def test_real_resolution_does_not_invoke_style_mutation(self):
        import plotly.io as pio
        before=pio.templates.default
        resolve_theme(self.raw)
        self.assertEqual(pio.templates.default,before)

    def test_no_current_directory_dependency(self):
        here=Path.cwd()
        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                self.assertEqual(load_reference_theme().context,'notebook')
            finally:os.chdir(here)

    def test_guard_rejects_missing_core_document(self):
        import temas_v02_check as guard
        real=Path.is_file
        with patch.object(Path,'is_file',lambda path: False if path.name=='ERROS.md' else real(path)):
            with self.assertRaisesRegex(ValueError,'V02_INCOMPLETE'):guard.check_layout()

    def test_guard_rejects_fixture_set_drift(self):
        import temas_v02_check as guard
        real=Path.glob
        with patch.object(Path,'glob',lambda path,pattern: iter(()) if path.name=='exemplos' else real(path,pattern)):
            with self.assertRaisesRegex(ValueError,'V02_FIXTURES'):guard.check_layout()

    def test_guard_rejects_asset_derivation_drift(self):
        import temas_v02_check as guard
        real=engine._read_json
        def read(path):
            data=real(path)
            if path.name=='assets.json':data['alterado']=True
            return data
        with patch.object(engine,'_read_json',side_effect=read):
            with self.assertRaisesRegex(ValueError,'V02_ASSETS'):guard.check_layout()

    def test_guard_rejects_fixture_content_drift(self):
        import temas_v02_check as guard
        real=Path.read_bytes
        with patch.object(Path,'read_bytes',lambda path: b'{}' if path.parent.name=='exemplos' and path.name=='legado_notebook.json' else real(path)):
            with self.assertRaisesRegex(ValueError,'V02_FIXTURE_DRIFT'):guard.check_layout()


class DeliveryTests(_ThemeFixture, unittest.TestCase):
    def test_concurrent_resolutions_do_not_share_tokens(self):
        from concurrent.futures import ThreadPoolExecutor
        def resolve(i):
            data=copy.deepcopy(self.reference)
            data['tokens']['brand.primary']=f'#{i:06X}'
            result=resolve_theme(data)
            return result.tokens['brand.primary'],result.fingerprint
        with ThreadPoolExecutor(max_workers=4) as pool:
            values=list(pool.map(resolve,range(12)))
        self.assertEqual([x[0] for x in values],[f'#{i:06X}' for i in range(12)])
        self.assertEqual(len({x[1] for x in values}),12)
        self.assertEqual(load_reference_theme().tokens['brand.primary'],'#005CA9')

    def test_packaged_runtime_has_no_dependency_on_docs_or_tools(self):
        import shutil
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'.assistant'
            for sub in ('hub_snippets/visual/tema','hub_padroes/identidade_visual'):
                shutil.copytree(PRODUCT/sub,root/sub,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            code="import sys;sys.path.insert(0,sys.argv[1]);from hub_snippets.visual.tema import load_reference_theme;print(load_reference_theme().context)"
            proc=subprocess.run([sys.executable,'-B','-c',code,str(root)],cwd=folder,capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertEqual(proc.stdout.strip(),'notebook')

    def test_notebook_and_runtime_modules_have_correct_databricks_types(self):
        import publicar_free
        obj=PRODUCT/'hub_snippets/visual/tema'
        self.assertFalse(publicar_free.eh_notebook(obj/'tema.py'))
        self.assertFalse(publicar_free.eh_notebook(obj/'__init__.py'))
        self.assertTrue(publicar_free.eh_notebook(obj/'exemplo_tema.py'))


if __name__=='__main__':unittest.main(verbosity=2)
