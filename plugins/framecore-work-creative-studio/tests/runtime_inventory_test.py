"""Regressions for the owner-requested installation and update inventory."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'skills/workflow-orchestrator/assets/environment-check'
spec = importlib.util.spec_from_file_location('audit_tools', FOLDER / 'audit_tools.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
CATALOG = audit.load(FOLDER / 'runtime-tools.json')
TOOLS = {t['id']: t for t in CATALOG['tools']}


def args(**changes):
    values = dict(workspace='/absent/workspace', project='/absent/project', browser=None,
                  python_env=[], node_root=[], update=False)
    values.update(changes)
    return argparse.Namespace(**values)


class Inventory(unittest.TestCase):
    def test_every_requested_component_has_its_own_probe_and_reference(self):
        expected = set('hyperframes remotion animate_engine manim blender ffmpeg ffprobe imageio_ffmpeg ffmpeg_fallback scenedetect opencv autoeditor librosa whisper whisper_tiny deepfilter imagemagick inkscape cairosvg pillow numpy matplotlib fonttools tesseract pytesseract ocr_pol react react_dom gsap three react_three_fiber pixi d3_scale lottie mediabunny remotion_cli remotion_renderer remotion_three cairo pango manimpango pycairo latex dvisvgm typst lxml python python_manim python_blender node npm npx typescript esbuild uv micromamba playwright browser_animate browser'.split())
        self.assertEqual(set(TOOLS), expected)
        self.assertEqual(len(CATALOG['tools']), 59)
        self.assertEqual(TOOLS['python_blender']['reported_version'], '3.13.16')
        self.assertEqual(TOOLS['browser_animate']['reported_version'], '141.0.7390.37')
        for tool in TOOLS.values():
            self.assertEqual(set(tool['host_evidence']), set(audit.HOSTS))
            self.assertNotIn('latest', tool)
            self.assertTrue(tool['install']['rule'])

    def test_distribution_without_successful_import_is_broken(self):
        env = {'requested_path':'/venv/bin/python','prefix':'/venv','modules':{'blender':{'present':True,'version':'5.2.2','import_ok':False,'error':'missing shared library'}}}
        result = audit.probe_python(TOOLS['blender'], [env])
        self.assertEqual(result['status'], 'broken')
        self.assertIn('shared library', result['note'])

    def test_other_python_role_is_not_inferred_from_active_version(self):
        env = {'requested_path':'/active/python','prefix':'/active','python':'3.12.14','modules':{}}
        self.assertEqual(audit.probe(TOOLS['python_blender'],args(),[env],[],{})['status'],'missing')
        env['modules']['blender']={'import_ok':True}
        self.assertEqual(audit.probe(TOOLS['python_blender'],args(),[env],[],{})['version'],'3.12.14')

    def test_import_failure_does_not_hide_a_working_isolated_environment(self):
        bad={'requested_path':'/system/python','modules':{'manim':{'present':True,'import_ok':False,'error':'ABI'}}}
        good={'requested_path':'/isolated/python','prefix':'/isolated','modules':{'manim':{'present':True,'import_ok':True,'version':'0.22.0','path':'/isolated/manim/__init__.py'}}}
        result=audit.probe_python(TOOLS['manim'],[bad,good])
        self.assertEqual(result['status'],'ok');self.assertEqual(result['interpreter'],'/isolated/python')

    def test_interpreter_timeout_is_unknown_not_confirmed_absence(self):
        self.assertEqual(audit.probe_python(TOOLS['manim'],[{'error':'timeout'}])['status'],'unknown')

    def test_npm_manifest_only_does_not_confirm_installation(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=root/'react';p.mkdir()
            (p/'package.json').write_text(json.dumps({'name':'react','version':'19.2.0'}))
            self.assertEqual(audit.probe_npm(TOOLS['react'],[root])['status'],'broken')
            (p/'index.js').write_text('module.exports = {};')
            result=audit.probe_npm(TOOLS['react'],[root])
            self.assertEqual(result['status'],'ok');self.assertIn('NOT_RUN',result['runtime_test'])

    def test_model_is_separate_from_wrapper_and_wrong_model_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'ggml-tiny.bin';p.write_bytes(b'fixture model')
            tool=dict(TOOLS['whisper_tiny'],sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            with mock.patch.dict(os.environ,{'FRAMECORE_WHISPER_MODEL':str(p)}):
                self.assertEqual(audit.probe_model(tool,[])['status'],'ok')
                p.write_bytes(b'other model')
                self.assertEqual(audit.probe_model(tool,[])['status'],'unknown')
                self.assertEqual(p.read_bytes(),b'other model')

    def test_installed_different_versions_are_not_added_to_install_plan(self):
        self.assertEqual(audit.installation_plan([{'status':'ok','version':'24.20.0'}],[TOOLS['node']]),[])
        plan=audit.installation_plan([{'status':'missing'}],[TOOLS['node']])
        self.assertEqual(plan[0]['action'],'install')
        self.assertEqual(plan[0]['state'],'planned; not executed')

    def test_unknown_is_a_verification_step_not_silent_install(self):
        plan=audit.installation_plan([{'status':'unknown','note':'hash differs'}],[TOOLS['ocr_pol']])
        self.assertEqual(plan[0]['action'],'verify')

    def test_failed_binary_does_not_count_as_installed(self):
        with mock.patch.object(audit,'execute',return_value={'exit_code':127,'stdout':'','stderr':'missing shared library'}):
            self.assertEqual(audit.probe_binary(TOOLS['ffmpeg'],['/fixture/ffmpeg'])['status'],'broken')

    def test_windows_convert_is_not_imagemagick(self):
        with mock.patch.object(audit,'execute',return_value={'exit_code':0,'stdout':'Windows filesystem converter 10.0','stderr':''}):
            self.assertEqual(audit.probe_binary(TOOLS['imagemagick'],['convert.exe'])['status'],'broken')

    def test_unavailable_host_does_not_become_a_pass(self):
        with mock.patch.object(audit,'python_paths',return_value=[]),mock.patch.object(audit,'node_roots',return_value=[]),mock.patch.object(audit,'probe',return_value=audit.absent()):
            data=audit.report(args(),None,'no trace')
        self.assertEqual(data['final']['verdict'],'unknown_host')
        self.assertEqual(len(data['tools']),59)
        self.assertFalse(data['network_used'])

    def test_work_is_measured_and_not_excluded_by_old_host_assumptions(self):
        def measured(tool,*unused):return audit.installed(tool['reported_version'],'/fixture','fixture')
        with mock.patch.object(audit,'python_paths',return_value=[]),mock.patch.object(audit,'node_roots',return_value=[]),mock.patch.object(audit,'probe',side_effect=measured):
            data=audit.report(args(update=True),'chatgpt_work','given')
        self.assertEqual(data['final']['verdict'],'pass')
        self.assertEqual(data['mode'],'update')
        self.assertFalse(data['installation_plan'])

    def test_limited_work_report_says_tools_install_per_conversation(self):
        with mock.patch.object(audit,'python_paths',return_value=[]),mock.patch.object(audit,'node_roots',return_value=[]),mock.patch.object(audit,'probe',return_value=audit.absent()):
            data=audit.report(args(update=True),'chatgpt_work','given')
        self.assertEqual(data['final']['verdict'],'limited')
        self.assertIn('installs them for the current conversation when a task needs them',audit.text(data))
        self.assertTrue(data['installs_nothing'])

    def test_remotion_family_drift_requires_review_without_upgrading(self):
        def measured(tool,*unused):return audit.installed('4.0.530' if tool['id']=='remotion_three' else tool['reported_version'],'/fixture','fixture')
        with mock.patch.object(audit,'python_paths',return_value=[]),mock.patch.object(audit,'node_roots',return_value=[]),mock.patch.object(audit,'probe',side_effect=measured):
            data=audit.report(args(),'codex','given')
        self.assertEqual(data['final']['verdict'],'fail')
        self.assertEqual(data['compatibility'][0]['id'],'remotion_family')
        self.assertEqual(data['installation_plan'],[])

    def test_real_python_probe_executes_without_installer_or_model(self):
        result=audit.python_probe(Path(sys.executable),[])
        self.assertEqual(result['python'],'.'.join(map(str,sys.version_info[:3])))
        self.assertEqual(result['modules'],{})

    def test_timeout_has_bounded_failure_evidence(self):
        with mock.patch.object(audit.subprocess,'run',side_effect=subprocess.TimeoutExpired('probe',20)):
            self.assertIsNone(audit.execute(['/fixture/probe'])['exit_code'])

    def test_unrelated_js_cannot_replace_missing_npm_entry(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=root/'hyperframes';p.mkdir()
            (p/'package.json').write_text(json.dumps({'name':'hyperframes','version':'0.8.181','main':'missing.js','bin':'missing-cli.js'}))
            (p/'example.js').write_text('')
            self.assertEqual(audit.probe_npm(TOOLS['hyperframes'],[root])['status'],'broken')
            (p/'missing.js').write_text('')
            self.assertEqual(audit.probe_npm(TOOLS['hyperframes'],[root])['status'],'broken')

    def test_auto_editor_import_without_executable_is_not_installed(self):
        env={'requested_path':'/env/python','prefix':'/env','modules':{'autoeditor':{'import_ok':True,'version':'29.3.1'}}}
        with mock.patch.object(audit,'binary_paths',return_value=[]):
            self.assertEqual(audit.probe(TOOLS['autoeditor'],args(),[env],[],{})['status'],'missing')

    def test_explicit_project_and_direct_media_environments_are_inspected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);project=root/'project';media=root/'media'
            for path in (project/'.venv/bin/python',media/'bin/python'):
                path.parent.mkdir(parents=True);path.touch()
            missing=root/'missing/bin/python'
            with mock.patch.dict(os.environ,{'FRAMECORE_MEDIA_HOME':str(media)},clear=True):
                paths=audit.python_paths(args(project=str(project),python_env=[str(missing)]))
            self.assertIn(project/'.venv/bin/python',paths)
            self.assertIn(media/'bin/python',paths)
            self.assertIn(missing,paths)

    def test_failed_interpreter_keeps_library_and_model_absence_unknown(self):
        env={'requested_path':'/absent/python','error':'failed','modules':{},'libraries':{}}
        self.assertEqual(audit.probe(TOOLS['cairo'],args(),[env],[],{})['status'],'unknown')
        with mock.patch.object(Path,'is_file',return_value=False):
            self.assertEqual(audit.probe_model(TOOLS['whisper_tiny'],[env])['status'],'unknown')

    def test_bundled_ffmpeg_checks_second_environment_after_first_fails(self):
        envs=[{'modules':{'imageio_ffmpeg':{'ffmpeg_path':p}}} for p in ('/broken/ffmpeg','/working/ffmpeg')]
        results=[{'exit_code':1,'stdout':'','stderr':'broken'}, {'exit_code':0,'stdout':'ffmpeg version 7.0.2','stderr':''}]
        with mock.patch.object(audit,'execute',side_effect=results) as execute:
            result=audit.probe(TOOLS['ffmpeg_fallback'],args(),envs,[],{})
        self.assertEqual(result['status'],'ok');self.assertEqual(execute.call_count,2)


if __name__=='__main__':unittest.main()
