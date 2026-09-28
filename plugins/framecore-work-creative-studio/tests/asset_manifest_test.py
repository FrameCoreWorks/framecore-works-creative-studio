"""Tests for declared consistency; synthetic data is not media QA evidence."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/delivery-documentation/scripts/asset_manifest.py'
SPEC = importlib.util.spec_from_file_location('asset_manifest', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
EXAMPLE = ROOT / 'skills/delivery-documentation/assets/project-manifest.example.json'


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EXAMPLE.read_text())

    def codes(self):
        return {x['code'] for x in MODULE.validate(self.data)['errors']}

    def test_example_and_template(self):
        self.assertEqual(MODULE.validate(self.data)['status'], 'PASS')
        template = EXAMPLE.with_name('project-manifest.template.json')
        self.assertEqual(MODULE.validate(json.loads(template.read_text()))['status'], 'PASS')

    def test_transitive_impact_excludes_independent_artifact(self):
        report = MODULE.impact(self.data, ['product-front'])
        self.assertEqual(report['affected_assets'], ['portrait', 'poster'])
        self.assertEqual(report['changed_assets'], ['product-front'])

    def test_stale_source_propagates_and_blocks_final(self):
        self.data['assets'][0]['revision'] = 'r003'
        self.data['assets'][0]['review']['reviewed_revision'] = 'r003'
        report = MODULE.validate(self.data)
        self.assertEqual(report['stale_assets'], ['portrait', 'poster'])
        self.assertIn({'id': 'portrait', 'code': 'STALE_DEPENDENCY'}, report['delivery_errors'])

    def test_stale_draft_is_reported_without_final_block(self):
        self.data['assets'][0]['revision'] = 'r003'
        self.data['assets'][0]['review']['status'] = 'not_reviewed'
        self.data['deliverables'][0]['purpose'] = 'draft'
        report = MODULE.validate(self.data)
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual(report['stale_assets'], ['portrait', 'poster'])

    def test_move_does_not_change_dependencies(self):
        self.data['assets'][0]['locator'] = 'fictional-new-location.png'
        self.assertEqual(MODULE.validate(self.data)['stale_assets'], [])

    def test_old_review_cannot_accept_new_revision(self):
        self.data['assets'][1]['revision'] = 'r004'
        self.assertIn('REVIEW_REVISION', self.codes())

    def test_review_basis_cannot_be_relabelled_silently(self):
        self.data['assets'][1]['review']['basis'] = []
        self.assertIn('REVIEW_BASIS', self.codes())

    def test_missing_dependency(self):
        self.data['assets'][1]['depends_on'][0]['id'] = 'absent'
        self.data['assets'][1]['review']['status'] = 'not_reviewed'
        self.assertIn('MISSING_DEPENDENCY', self.codes())

    def test_cycle_is_invalid(self):
        self.data['assets'][0]['depends_on'] = [{'id': 'portrait', 'revision': 'r001'}]
        self.data['assets'][0]['review']['basis'] = copy.deepcopy(self.data['assets'][0]['depends_on'])
        self.assertIn('DEPENDENCY_CYCLE', self.codes())

    def test_duplicate_asset_and_dependency(self):
        self.data['assets'].append(copy.deepcopy(self.data['assets'][0]))
        self.assertIn('DUPLICATE_ID', self.codes())
        self.data['assets'].pop()
        self.data['assets'][1]['depends_on'].append(copy.deepcopy(self.data['assets'][1]['depends_on'][0]))
        self.assertIn('DUPLICATE_DEPENDENCY', self.codes())

    def test_declared_measurement_requires_method_and_evidence(self):
        self.data['assets'][0]['properties']['verified']['width'] = {'value': 1000}
        self.assertIn('VERIFIED_EVIDENCE', self.codes())

    def test_property_cannot_be_both_verified_and_unknown(self):
        props = self.data['assets'][0]['properties']
        props['verified']['width'] = {'value': 1000, 'method': 'fictional test', 'evidence': 'fictional test'}
        props['unknown'] = ['width']
        self.assertIn('PROPERTY_CONFLICT', self.codes())

    def test_present_requires_locator_and_digest_is_not_invented(self):
        self.data['assets'][0]['locator'] = None
        self.data['assets'][0]['sha256'] = 'unknown'
        self.assertTrue({'PRESENT_LOCATOR', 'DIGEST'} <= self.codes())

    def test_final_requires_acceptance(self):
        self.data['assets'][2]['review']['status'] = 'not_reviewed'
        self.assertIn({'id': 'portrait', 'code': 'NOT_ACCEPTED'}, MODULE.validate(self.data)['delivery_errors'])

    def test_planned_source_blocks_transitive_final(self):
        self.data['assets'][0].update(state='planned', locator=None, review={'status': 'not_reviewed'})
        report = MODULE.validate(self.data)
        self.assertEqual(report['unready_assets'], ['portrait', 'poster', 'product-front'])
        self.assertIn({'id': 'portrait', 'code': 'UNRESOLVED_INPUT'}, report['delivery_errors'])

    def test_upstream_changes_required_blocks_transitive_final(self):
        self.data['assets'][0]['review']['status'] = 'changes_required'
        self.assertIn({'id': 'portrait', 'code': 'UNRESOLVED_INPUT'}, MODULE.validate(self.data)['delivery_errors'])

    def test_missing_source_retains_historical_acceptance(self):
        self.data['assets'][0]['state'] = 'missing'
        self.assertEqual(MODULE.validate(self.data)['status'], 'PASS')
        self.data['deliverables'] = [{'id': 'product-front', 'purpose': 'final'}]
        self.assertIn({'id': 'product-front', 'code': 'NOT_PRESENT'}, MODULE.validate(self.data)['delivery_errors'])

    def test_planned_asset_cannot_claim_past_acceptance(self):
        self.data['assets'][0]['state'] = 'planned'
        self.assertIn('REVIEW_AVAILABILITY', self.codes())

    def test_conditional_prompt_can_be_final_without_future_execution_media(self):
        self.data['assets'] = [self.data['assets'][3]]
        self.data['assets'][0]['role'] = 'conditional-prompt-specification'
        self.data['assets'][0]['planned_inputs'] = ['Future accepted image required for execution, not used in authoring.']
        self.data['deliverables'] = [{'id': 'lyric', 'purpose': 'final'}]
        self.assertEqual(MODULE.validate(self.data)['status'], 'PASS')

    def test_malformed_inputs_fail_without_uncaught_type_errors(self):
        for item in [None, [], {}, {'schema_version': True, 'assets': [], 'deliverables': []}]:
            self.assertEqual(MODULE.validate(item)['status'], 'FAIL')
        for value in [None, 3, 'bad', [{'id': []}]]:
            self.data['assets'][0]['depends_on'] = value
            self.assertIn('DEPENDENCIES', self.codes())

    def test_unknown_change_id_fails(self):
        self.assertEqual(MODULE.impact(self.data, ['absent'])['status'], 'FAIL')

    def test_operations_do_not_mutate_input(self):
        before = copy.deepcopy(self.data)
        MODULE.validate(self.data)
        MODULE.impact(self.data, ['product-front'])
        self.assertEqual(before, self.data)

    def test_cli_reports_json_error_and_runs_without_media_files(self):
        good = subprocess.run([sys.executable, str(SCRIPT), 'check', str(EXAMPLE)], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)['status'], 'PASS')
        with tempfile.TemporaryDirectory() as folder:
            invalid = Path(folder) / 'invalid.json'
            invalid.write_text('{')
            bad = subprocess.run([sys.executable, str(SCRIPT), 'check', str(invalid)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertEqual(json.loads(bad.stdout)['errors'][0]['code'], 'INPUT')


if __name__ == '__main__':
    unittest.main()
