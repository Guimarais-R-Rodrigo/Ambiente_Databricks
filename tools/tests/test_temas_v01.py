"""Regressões e mutantes do CONTRATO V01; não homologam runtime ou pessoas."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import temas_v01_contract as c


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema=c.read_json(c.SCHEMA_PATH)
        cls.valid=c.read_json(c.PACKAGE/'fixtures/legado_notebook.json')
        cls.policy=c.read_json(c.PACKAGE/'politica_workflow.json')
        cls.assets=c.read_json(c.PACKAGE/'referencias_assets.json')
    def setUp(self):
        self.theme=copy.deepcopy(self.valid)
    def reject(self,code,callback,*args):
        with self.assertRaises(c.ContractError) as caught: callback(*args)
        self.assertEqual(caught.exception.code,code)
    def validate(self): c.validate_theme(self.theme,self.schema)
    def test_package_complete(self):
        result=c.check_package();self.assertEqual(result['status'],'PASS_CONTRATO_LOCAL')
        self.assertEqual(result['runtime'],'NAO_IMPLEMENTADO_V01')
    def test_all_four_context_fixtures_valid(self):
        for path in (c.PACKAGE/'fixtures').glob('*.json'):
            with self.subTest(path=path.name): c.validate_theme(c.read_json(path),self.schema)
    def test_validation_does_not_mutate_or_fill_defaults(self):
        before=copy.deepcopy(self.theme);self.validate();self.assertEqual(before,self.theme)
    def test_missing_root_field(self):
        del self.theme['mode'];self.reject('SCHEMA_REQUIRED',self.validate)
    def test_missing_token_no_default_injection(self):
        del self.theme['tokens']['brand.primary'];self.reject('SCHEMA_REQUIRED',self.validate)
        self.assertNotIn('brand.primary',self.theme['tokens'])
    def test_unknown_root_key(self):
        self.theme['modee']='dark';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_unknown_token(self):
        self.theme['tokens']['brand.primry']='#005CA9';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_approved_flag_forbidden(self):
        self.theme['approved']=True;self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_role_forgery_forbidden(self):
        self.theme['role']='publicador';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_scope_not_from_theme(self):
        self.theme['scope']='compartilhado';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_arbitrary_css_forbidden(self):
        self.theme['css']='body{display:none}';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_analytic_parameters_forbidden(self):
        self.theme['tokens']['score.threshold']=.8;self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_invalid_hex_digit(self):
        self.theme['tokens']['brand.primary']='#00XCA9';self.reject('SCHEMA_PATTERN',self.validate)
    def test_short_hex_rejected(self):
        self.theme['tokens']['brand.primary']='#FFF';self.reject('SCHEMA_PATTERN',self.validate)
    def test_alpha_hex_rejected(self):
        self.theme['tokens']['brand.primary']='#005CA9FF';self.reject('SCHEMA_PATTERN',self.validate)
    def test_lowercase_requires_ui_normalization(self):
        self.theme['tokens']['brand.primary']='#005ca9';self.reject('SCHEMA_PATTERN',self.validate)
    def test_whitespace_requires_explicit_ui_normalization(self):
        self.theme['tokens']['brand.primary']=' #005CA9 ';self.reject('SCHEMA_PATTERN',self.validate)
    def test_color_injection_rejected(self):
        self.theme['tokens']['brand.primary']='#005CA9;display:none';self.reject('SCHEMA_PATTERN',self.validate)
    def test_numeric_string_rejected(self):
        self.theme['tokens']['chart.width_px']='900';self.reject('SCHEMA_TYPE',self.validate)
    def test_boolean_is_not_dimension(self):
        self.theme['tokens']['chart.width_px']=True;self.reject('SCHEMA_TYPE',self.validate)
    def test_negative_dimension(self):
        self.theme['tokens']['chart.width_px']=-1;self.reject('SCHEMA_MINIMUM',self.validate)
    def test_excessive_dimension(self):
        self.theme['tokens']['chart.width_px']=99999;self.reject('SCHEMA_MAXIMUM',self.validate)
    def test_noninteger_dimension(self):
        self.theme['tokens']['chart.width_px']=900.5;self.reject('SCHEMA_TYPE',self.validate)
    def test_wrong_unit(self):
        self.theme['tokens']['chart.width_px']='900pt';self.reject('SCHEMA_TYPE',self.validate)
    def test_empty_palette(self):
        self.theme['tokens']['palette.categorical']=[];self.reject('SCHEMA_MINITEMS',self.validate)
    def test_duplicate_palette_color(self):
        self.theme['tokens']['palette.categorical']=['#005CA9','#005CA9'];self.reject('SCHEMA_UNIQUEITEMS',self.validate)
    def test_palette_no_endpoints(self):
        self.theme['tokens']['palette.sequential']=['#005CA9'];self.reject('SCHEMA_MINITEMS',self.validate)
    def test_palette_even_diverging(self):
        self.theme['tokens']['palette.diverging']=['#000000','#111111','#222222','#FFFFFF'];self.reject('PALETTE_CENTER',self.validate)
    def test_palette_too_large(self):
        self.theme['tokens']['palette.categorical']=[f'#{i:06X}' for i in range(21)];self.reject('SCHEMA_MAXITEMS',self.validate)
    def test_schema_future_version(self):
        self.theme['schema_version']='99.0.0';self.reject('SCHEMA_CONST',self.validate)
    def test_engine_major_future(self):
        self.theme['engine_compatibility']['api_major']=99;self.reject('SCHEMA_CONST',self.validate)
    def test_engine_minimum_future(self):
        self.theme['engine_compatibility']['minimum_version']='1.9.0';self.reject('ENGINE_VERSION',self.validate)
    def test_engine_minimum_wrong_major(self):
        self.theme['engine_compatibility']['minimum_version']='0.9.0';self.reject('ENGINE_VERSION',self.validate)
    def test_version_leading_zero(self):
        self.theme['theme_version']='01.0.0';self.reject('SCHEMA_PATTERN',self.validate)
    def test_inheritance_forbidden_no_cycle(self):
        self.theme['extends']=self.theme['theme_id'];self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_external_ref_in_theme(self):
        self.theme['$ref']='https://example.invalid/theme';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_wrong_context_rejected(self):
        self.theme['context']='readme';self.theme['asset_set_id']='editorial-v2-congelado';self.reject('SCHEMA_ADDITIONALPROPERTIES',self.validate)
    def test_apps_reserved_not_supported(self):
        self.theme['context']='app';self.reject('SCHEMA_ENUM',self.validate)
    def test_unknown_font(self):
        self.theme['tokens']['font.family']='https://example.invalid/font.woff';self.reject('SCHEMA_ENUM',self.validate)
    def test_asset_free_path_forbidden(self):
        self.theme['asset_set_id']='../../private';self.reject('SCHEMA_ENUM',self.validate)
    def test_asset_unknown_registry(self):
        self.theme['asset_set_id']='desconhecido';self.reject('ASSET_UNKNOWN',c.check_assets,self.theme,self.assets)
    def test_asset_hash_tampered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'image.png').write_bytes(b'actual')
            reg={'sets':{'fixture':[{'path':'image.png','sha256':'0'*64}]}}
            self.theme['asset_set_id']='fixture';self.reject('ASSET_HASH',c.check_assets,self.theme,reg,root)
    def test_empty_asset_manifest(self):
        self.theme['asset_set_id']='editorial-v2-congelado';self.reject('ASSET_EMPTY',c.check_assets,self.theme,{'sets':{'editorial-v2-congelado':[]}})
    def test_duplicate_asset_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'img').write_bytes(b'ok');entry={'path':'img','sha256':hashlib.sha256(b'ok').hexdigest()}
            self.theme['asset_set_id']='fixture';self.reject('ASSET_DUPLICATE',c.check_assets,self.theme,{'sets':{'fixture':[entry,entry]}},root)
    def test_real_baseline_assets_match(self):
        theme=c.read_json(c.PACKAGE/'fixtures/legado_editorial.json');self.assertEqual(c.check_assets(theme,self.assets),12)
    def test_label_markup_forbidden(self):
        self.theme['display_name']='<script>alert(1)</script>';self.reject('SCHEMA_PATTERN',self.validate)
    def test_label_accented_text_allowed(self):
        self.theme['display_name']='Análise executiva — revisão 2';self.validate()
    def test_label_excessive(self):
        self.theme['display_name']='a'*81;self.reject('SCHEMA_MAXLENGTH',self.validate)
    def test_theme_id_not_path(self):
        self.theme['theme_id']='../tema';self.reject('SCHEMA_PATTERN',self.validate)
    def test_legacy_curves_six_colors_preserved(self):
        self.assertEqual(len(self.theme['tokens']['palette.curves_legacy']),6)
        self.assertEqual(len(self.theme['tokens']['palette.categorical']),10)
    def test_source_constants_default_values(self):
        p=ROOT/'ambiente_databricks/.assistant/hub_snippets/constants/colors/colors.py'
        spec=importlib.util.spec_from_file_location('v01_colors_fixture',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        for token,name in {'brand.primary':'AZUL_CAIXA','text.secondary':'TEXTO_SECUNDARIO','palette.categorical':'PALETA_CATEGORICA','palette.sequential':'PALETA_SEQUENCIAL','palette.diverging':'PALETA_DIVERGENTE'}.items():
            self.assertEqual(self.theme['tokens'][token],getattr(m,name))
    def test_token_documentation_derived_exactly(self):
        self.assertEqual((c.PACKAGE/'TOKENS.md').read_text(),c.dictionary(self.schema))
    def test_required_tokens_equal_documented_tokens(self):
        for key in ('notebookTokens','editorialTokens'):
            block=self.schema['$defs'][key];self.assertEqual(set(block['required']),set(block['properties']))
    def test_every_token_has_existing_integration_point(self):
        for key in ('notebookTokens','editorialTokens'):
            for spec in self.schema['$defs'][key]['properties'].values():
                for consumer in spec['x-hub']['consumers']: self.assertTrue(c.safe_file(ROOT,consumer).is_file())
    def test_no_external_schema_resolution(self):
        schema=copy.deepcopy(self.schema);schema['properties']['tokens']['$ref']='https://example.invalid/schema'
        self.reject('SCHEMA_REMOTE_REF',c.schema_validator,schema)
    def test_no_dynamic_schema_ref(self):
        schema=copy.deepcopy(self.schema);schema['$dynamicRef']='#root';self.reject('SCHEMA_DYNAMIC_REF',c.schema_validator,schema)
    def test_invalid_metaschema(self):
        schema=copy.deepcopy(self.schema);schema['type']='invalid';self.reject('SCHEMA_INVALID',c.schema_validator,schema)
    def test_unknown_schema_dialect(self):
        schema=copy.deepcopy(self.schema);schema['$schema']='https://example.invalid/schema';self.reject('SCHEMA_DIALECT',c.schema_validator,schema)
    def test_parser_duplicate_root(self): self.reject('JSON_DUPLICATE',c.strict_json,b'{"a":1,"a":2}')
    def test_parser_duplicate_nested(self): self.reject('JSON_DUPLICATE',c.strict_json,b'{"a":{"b":1,"b":2}}')
    def test_parser_nan(self): self.reject('JSON_NONFINITE',c.strict_json,b'{"a":NaN}')
    def test_parser_infinity(self): self.reject('JSON_NONFINITE',c.strict_json,b'{"a":Infinity}')
    def test_parser_exponent_overflow(self): self.reject('JSON_NONFINITE',c.strict_json,b'{"a":1e999}')
    def test_parser_invalid_utf8(self): self.reject('JSON_ENCODING',c.strict_json,b'\xff')
    def test_parser_bom_rejected(self): self.reject('JSON_ENCODING',c.strict_json,b'\xef\xbb\xbf{}')
    def test_parser_surrogate_rejected(self): self.reject('JSON_UNICODE',c.strict_json,b'{"a":"\\ud800"}')
    def test_parser_too_large(self): self.reject('JSON_SIZE',c.strict_json,b' '*(c.MAX_BYTES+1))
    def test_parser_too_deep(self): self.reject('JSON_DEPTH',c.strict_json,b'['*13+b'0'+b']'*13)
    def test_parser_brackets_inside_escaped_string(self):
        text='[[["\\'*20;self.assertEqual(c.strict_json(json.dumps({'a':text}).encode()),{'a':text})
    def test_parser_invalid_syntax(self): self.reject('JSON_SYNTAX',c.strict_json,b'{')
    def test_parser_string_not_bytes(self): self.reject('JSON_INPUT_TYPE',c.strict_json,'{}')
    def test_parser_no_sensitive_echo(self):
        try:c.strict_json(b'{"secret-test":NaN}')
        except c.ContractError as exc:self.assertNotIn('secret-test',str(exc))
    def test_path_traversal(self): self.reject('PATH_SCOPE',c.safe_file,ROOT,'../README.md')
    def test_path_absolute(self): self.reject('PATH_SCOPE',c.safe_file,ROOT,'/README.md')
    def test_path_windows_drive(self): self.reject('PATH_SCOPE',c.safe_file,ROOT,'C:/README.md')
    def test_path_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'x').write_text('ok')
            try:
                (root/'s').symlink_to(root/'x')
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f'filesystem sem symlink de arquivo: {exc}')
            self.reject('PATH_SYMLINK',c.safe_file,root,'s')
    def test_parent_symlink_on_json_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'a').mkdir();(root/'a/x.json').write_text('{}')
            link=root/'b'
            try:
                link.symlink_to(root/'a',target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f'filesystem sem symlink de diretório: {exc}')
            self.reject('PATH_SYMLINK',c.read_json,root/'b/x.json')
    def test_theme_id_trailing_newline_rejected(self):
        self.theme['theme_id']='tema\n';self.reject('SCHEMA_PATTERN',self.validate)
    def test_version_trailing_newline_rejected(self):
        self.theme['theme_version']='0.1.0\n';self.reject('SCHEMA_PATTERN',self.validate)
    def test_label_trailing_control_rejected(self):
        self.theme['display_name']='Tema\n';self.reject('SCHEMA_PATTERN',self.validate)
    def test_policy_no_owner_check_mutant(self):
        p=copy.deepcopy(self.policy);next(t for t in p['transitions'] if t['action']=='editar')['guards'].remove('owner');self.reject('POLICY_GUARD',c.validate_policy,p)
    def test_policy_scope_widening_mutant(self):
        p=copy.deepcopy(self.policy);next(t for t in p['transitions'] if t['action']=='editar')['scopes'].append('compartilhado');self.reject('POLICY_GUARD',c.validate_policy,p)
    def test_policy_approval_not_bound_to_dependencies(self):
        p=copy.deepcopy(self.policy);p['trusted_revision_components'].remove('asset_manifest_sha256');self.reject('POLICY_REVISION',c.validate_policy,p)
    def test_policy_trusts_json_identity_mutant(self):
        p=copy.deepcopy(self.policy);p['permissions_source']='json';self.reject('POLICY_IDENTITY',c.validate_policy,p)
    def test_policy_reader_can_export_mutant(self):
        p=copy.deepcopy(self.policy);p['read_actions'][-1]['roles'].append('leitor');self.reject('POLICY_READ',c.validate_policy,p)
    def test_policy_published_editable_mutant(self):
        p=copy.deepcopy(self.policy);p['new_revision_required_for'].remove('editar_publicado');self.reject('POLICY_IMMUTABLE',c.validate_policy,p)
    def test_file_root_parent_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'actual/sub').mkdir(parents=True);(root/'actual/sub/x').write_text('x')
            alias=root/'alias'
            try:
                alias.symlink_to(root/'actual',target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f'filesystem sem symlink de diretório: {exc}')
            self.reject('PATH_SYMLINK',c.safe_file,root/'alias/sub','x')
    def test_document_local_links_resolve(self):
        self.assertGreater(c.check_links(),20)
    def test_policy_valid(self): c.validate_policy(self.policy)
    def test_policy_default_allow_mutant(self):
        p=copy.deepcopy(self.policy);p['default']='allow';self.reject('POLICY_DEFAULT',c.validate_policy,p)
    def test_policy_self_asserted_operational_status(self):
        p=copy.deepcopy(self.policy);p['status']='PRODUCAO_APROVADA';self.reject('POLICY_STATUS',c.validate_policy,p)
    def test_policy_publish_reader_mutant(self):
        p=copy.deepcopy(self.policy);next(t for t in p['transitions'] if t['action']=='publicar')['roles'].append('leitor');self.reject('POLICY_GUARD',c.validate_policy,p)
    def test_policy_removed_hash_check(self):
        p=copy.deepcopy(self.policy);next(t for t in p['transitions'] if t['action']=='publicar')['guards'].remove('revision_match');self.reject('POLICY_GUARD',c.validate_policy,p)
    def test_policy_duplicate_action(self):
        p=copy.deepcopy(self.policy);p['transitions'].append(p['transitions'][0]);self.reject('POLICY_DUPLICATE',c.validate_policy,p)
    def test_policy_unreviewed_transition(self):
        p=copy.deepcopy(self.policy);p['transitions'].append({'action':'force_publish'});self.reject('POLICY_ACTIONS',c.validate_policy,p)
    def test_model_all_defined_transitions(self):
        for t in self.policy['transitions']:
            for role in t['roles']:
                for scope in t['scopes']:
                    with self.subTest(action=t['action'],role=role,scope=scope):
                        result=c.model_transition(self.policy,t['action'],t['from'],role,scope,{g:True for g in t['guards']});self.assertEqual(result,t['to'])
    def test_model_denies_every_other_role(self):
        for t in self.policy['transitions']:
            for role in set(self.policy['roles'])-set(t['roles']):
                with self.subTest(action=t['action'],role=role):self.reject('MODEL_DENY',c.model_transition,self.policy,t['action'],t['from'],role,t['scopes'][0],{g:True for g in t['guards']})
    def test_model_denies_each_missing_guard(self):
        for t in self.policy['transitions']:
            for guard in t['guards']:
                checks={g:True for g in t['guards']};checks.pop(guard)
                with self.subTest(action=t['action'],guard=guard):self.reject('MODEL_DENY',c.model_transition,self.policy,t['action'],t['from'],t['roles'][0],t['scopes'][0],checks)
    def test_model_no_self_approval(self):
        t=next(t for t in self.policy['transitions'] if t['action']=='aprovar');checks={g:True for g in t['guards']};checks['not_author']=False
        self.reject('MODEL_DENY',c.model_transition,self.policy,'aprovar','em_revisao','aprovador','projeto',checks)
    def test_model_no_publish_draft(self):
        self.reject('MODEL_DENY',c.model_transition,self.policy,'publicar','rascunho','publicador','projeto',{})
    def test_model_stale_revision_denied(self):
        t=next(t for t in self.policy['transitions'] if t['action']=='publicar');checks={g:True for g in t['guards']};checks['revision_match']=False
        self.reject('MODEL_DENY',c.model_transition,self.policy,'publicar','aprovado','publicador','projeto',checks)
    def test_model_integer_one_is_not_verified_true(self):
        self.reject('MODEL_DENY',c.model_transition,self.policy,'editar','rascunho','proponente','pessoal',{'owner':1,'schema_valid':True})
    def test_contrast_known_black_white(self): self.assertEqual(c.contrast('#000000','#FFFFFF'),21.0)
    def test_contrast_same_color(self): self.assertEqual(c.contrast('#005CA9','#005CA9'),1.0)
    def test_contrast_symmetry(self): self.assertEqual(c.contrast('#005CA9','#FFFFFF'),c.contrast('#FFFFFF','#005CA9'))
    def test_legacy_debt_not_masked(self):
        self.assertLess(c.contrast(self.theme['tokens']['semantic.positive'],'#FFFFFF'),4.5)
        self.assertLess(c.contrast(self.theme['tokens']['semantic.warning'],'#FFFFFF'),4.5)
    def test_contrast_not_rounded_to_pass(self): self.assertLess(c.contrast('#777777','#FFFFFF'),4.5)
    def test_contrast_candidate_pairs(self):
        t=c.read_json(c.PACKAGE/'fixtures/executivo_claro_exemplo.json')['tokens']
        for fg,bg in [('brand.primary','surface.section'),('text.secondary','surface.section'),('text.primary','surface.card'),('status.ok_text','status.ok_bg'),('status.warn_text','status.warn_bg'),('status.fail_text','status.fail_bg'),('table.header_text','brand.primary')]:
            with self.subTest(fg=fg,bg=bg):self.assertGreaterEqual(c.contrast(t[fg],t[bg]),4.5)
    def test_no_network_needed(self):
        with patch('socket.socket',side_effect=AssertionError('Rede não permitida')): self.validate()
    def test_cli_no_side_effect_files(self):
        before={p.relative_to(c.PACKAGE):hashlib.sha256(p.read_bytes()).hexdigest() for p in c.PACKAGE.rglob('*') if p.is_file()}
        result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/temas_v01_contract.py')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        after={p.relative_to(c.PACKAGE):hashlib.sha256(p.read_bytes()).hexdigest() for p in c.PACKAGE.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
    def test_readme_distinguishes_current_and_future(self):
        text=(c.PACKAGE/'README.md').read_text()
        for term in ['não está instalado','GUIA_PRIMEIRO_USO.md','CONTRATO_TEMAS.md','PENDENTE']:
            self.assertIn(term,text)
    def test_all_contract_cases_have_oracles(self):
        matrix=c.read_json(c.PACKAGE/'matriz_testes.json')
        ids={case['id'] for case in matrix['cases']}
        self.assertTrue({f'CON-{i:02}' for i in range(1,13)}<=ids)
        for case in matrix['cases']:
            self.assertTrue(case['procedure']);self.assertTrue(case['oracle']);self.assertTrue(case['evidence_required'])
    def test_human_cases_not_forged_pass(self):
        matrix=c.read_json(c.PACKAGE/'matriz_testes.json')
        for case in matrix['cases']:
            if case['human_required']:
                self.assertEqual(case['human_status'],'PENDENTE');self.assertIsNone(case['participant']);self.assertIsNone(case['observed_seconds'])
    def test_runtime_and_documentation_do_not_claim_installation(self):
        self.assertTrue(self.schema['x-hub-policy']['candidate'])
        for fixture in (c.PACKAGE/'fixtures').glob('*.json'):
            data=c.read_json(fixture);self.assertNotIn('approved',data);self.assertNotIn('published',data)

if __name__=='__main__': unittest.main(verbosity=2)
