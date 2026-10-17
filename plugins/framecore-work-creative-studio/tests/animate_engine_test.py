"""Tests for the bundled Animate engine: byte identity with the pinned source, no second skill, and a demo that builds."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest
import hashlib
import os
import sys

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ENGINE = PLUGIN / 'skills/hyperframes-workflow/assets/animate-engine'
MANIFEST = json.loads((PLUGIN / 'integrations/animate/source-manifest.json').read_text(encoding='utf-8'))
ADAPTER = PLUGIN / 'skills/hyperframes-workflow/assets/animate-export/export.mjs'


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


class Provenance(unittest.TestCase):
    def test_every_bundled_file_matches_the_pinned_source(self):
        listed = {item['path']: item['git_blob_sha'] for item in MANIFEST['bundled_files']}
        self.assertEqual(len(listed), 107)
        for path, blob in listed.items():
            self.assertEqual(git_blob(ENGINE / path), blob, path)
        added = {str(pathlib.Path(p).relative_to('skills/hyperframes-workflow/assets/animate-engine')) for p in MANIFEST['studio_added_files']}
        present = {str(p.relative_to(ENGINE)) for p in ENGINE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        self.assertEqual(present, set(listed) | added, 'only manifest files and the Studio-added pins are bundled')
        self.assertEqual(git_blob(PLUGIN / 'integrations/animate/LICENSE'), MANIFEST['retained_files'][0]['git_blob_sha'])

    def test_the_engine_is_not_a_second_skill(self):
        self.assertFalse(list(ENGINE.rglob('SKILL.md')), 'SKILL.md is bundled as ENGINE.md')
        self.assertTrue((ENGINE / 'ENGINE.md').read_text(encoding='utf-8').startswith('---\nname: animate\n'))

    def test_workspace_pin_and_lockfile_agree(self):
        package = json.loads((ENGINE / 'package.json').read_text(encoding='utf-8'))
        lock = json.loads((ENGINE / 'package-lock.json').read_text(encoding='utf-8'))
        self.assertEqual(package['dependencies'], {'playwright': '1.56.1'})
        self.assertEqual(lock['packages']['node_modules/playwright']['version'], '1.56.1')


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class Build(unittest.TestCase):
    def test_a_style_demo_builds_into_one_self_contained_file(self):
        with tempfile.TemporaryDirectory() as temp:
            piece = pathlib.Path(temp, 'pieces/riso-demo')
            shutil.copytree(ENGINE / 'styles/riso/demo', piece)
            done = subprocess.run(['node', str(ENGINE / 'tools/build.mjs'), str(piece)], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn('no external assets', done.stdout)
            html = (piece / 'index.html').read_text(encoding='utf-8')
            self.assertIn('<canvas', html)
            self.assertNotIn('Math.random()', html.replace('// never Math.random()', ''))


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class CaptionExport(unittest.TestCase):
    """Exercise the real pinned exporter with local browser/FFmpeg stand-ins; no media or network is needed."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='animate # captions ')
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.engine = self.root / 'engine'
        (self.engine / 'tools').mkdir(parents=True)
        for name in ('export.mjs', 'gpu.mjs'):
            shutil.copyfile(ENGINE / 'tools' / name, self.engine / 'tools' / name)
        self.original = (self.engine / 'tools/export.mjs').read_bytes()
        self.piece = self.root / 'piece'
        self.piece.mkdir()
        (self.piece / 'piece.json').write_text(json.dumps({'formats': ['9:16', '1:1']}))
        (self.piece / 'index.html').write_text('<!doctype html>')
        driver = self.engine / 'node_modules/playwright'
        driver.mkdir(parents=True)
        (driver / 'index.js').write_text("""
const page = () => ({
  url: '', on() {}, async goto(url) { this.url = url; }, async waitForFunction() {}, async close() {},
  async evaluate(fn) {
    if (String(fn).includes('const T = window.TIMELINE')) {
      const format = new URL(this.url).searchParams.get('format');
      return {frames: 2, fps: 30, width: 16, height: format === '1:1' ? 16 : 32,
        narration: process.env.STUDIO_TEST_NO_NARRATION ? null : [{t0: 0, t1: 0.06, text: 'Read this'}], gpu: false};
    }
    return 'cG5n';
  }
});
exports.chromium = {async launch() { return {newPage: async () => page(),
  newContext: async () => ({newPage: async () => page()}), async close() {}}; }};
""")
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.log = self.root / 'ffmpeg.jsonl'
        ffmpeg = self.bin / 'ffmpeg'
        ffmpeg.write_text(f'#!{sys.executable}\n' + """
import json, os, pathlib, sys
args = sys.argv[1:]
with open(os.environ['STUDIO_TEST_FFMPEG_LOG'], 'a') as out:
    out.write(json.dumps({'args': args, 'cwd': os.getcwd()}) + '\\n')
if '-vf' in args and not pathlib.Path(args[args.index('-i') + 1]).is_file():
    sys.exit(7)
pathlib.Path(args[-1]).write_text('stand-in export')
""")
        ffmpeg.chmod(0o755)

    def run_export(self, *args, upstream=False, narration=True, adapter=ADAPTER):
        env = dict(os.environ, PATH=str(self.bin), STUDIO_TEST_FFMPEG_LOG=str(self.log), TMPDIR=str(self.root))
        if narration:
            env.pop('STUDIO_TEST_NO_NARRATION', None)
        else:
            env['STUDIO_TEST_NO_NARRATION'] = '1'
        command = [shutil.which('node'), str(self.engine / 'tools/export.mjs' if upstream else adapter), str(self.piece)]
        if not upstream:
            command += ['--engine', str(self.engine)]
        done = subprocess.run(command + ['--no-audio', *args], capture_output=True, text=True, env=env, timeout=30)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []
        self.assertEqual((self.engine / 'tools/export.mjs').read_bytes(), self.original)
        self.assertFalse(list(self.root.glob('studio-animate-export-*')), 'temporary adapted source is removed')
        return done, calls

    def captions(self, calls):
        return [(pathlib.Path(call['args'][call['args'].index('-i') + 1]), pathlib.Path(call['args'][-1]))
                for call in calls if '-vf' in call['args']]

    def test_upstream_reproduces_the_wrong_input_for_an_alternate_format(self):
        done, calls = self.run_export('--format', '1:1', upstream=True)
        self.assertNotEqual(done.returncode, 0)
        self.assertEqual(self.captions(calls)[0][0], pathlib.Path('final.mp4'))

    def test_default_and_alternate_formats_use_the_actual_export(self):
        for options, name in (((), 'final'), (('--format', '1:1'), 'final-16x16')):
            with self.subTest(options=options):
                self.log.unlink(missing_ok=True)
                done, calls = self.run_export(*options)
                self.assertEqual(done.returncode, 0, done.stderr)
                renders = self.piece / 'renders'
                self.assertEqual(self.captions(calls), [(renders / (name + '.mp4'), renders / (name + '-captions.mp4'))])

    def test_custom_nested_name_and_spaces_are_preserved(self):
        done, calls = self.run_export('--format', '1:1', '--out', 'client files/my film.mp4')
        self.assertEqual(done.returncode, 0, done.stderr)
        renders = self.piece / 'renders/client files'
        self.assertEqual(self.captions(calls), [(renders / 'my film.mp4', renders / 'my film-captions.mp4')])

    def test_symlinked_adapter_path_runs_the_cli(self):
        link = self.root / 'adapter link.mjs'
        link.symlink_to(ADAPTER)
        done, calls = self.run_export(adapter=link)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(len(self.captions(calls)), 1, 'CLI must execute instead of silently returning success')

    def test_multiple_formats_keep_separate_videos_and_caption_outputs(self):
        for custom in (False, True):
            with self.subTest(custom=custom):
                self.log.unlink(missing_ok=True)
                args = ['--formats', '9:16,1:1'] + (['--out', 'client files/my film.mp4'] if custom else [])
                done, calls = self.run_export(*args)
                self.assertEqual(done.returncode, 0, done.stderr)
                renders = self.piece / 'renders' / ('client files' if custom else '')
                base = 'my film' if custom else 'final'
                self.assertEqual(self.captions(calls), [
                    (renders / (base + '.mp4'), renders / (base + '-captions.mp4')),
                    (renders / (base + '-16x16.mp4'), renders / (base + '-16x16-captions.mp4'))])

    def test_caption_opt_out_absent_narration_and_partial_exports_do_not_burn(self):
        for args, narration in ((['--no-captions'], True), ([], False), (['--no-mux'], True),
                                (['--from', '1'], True), (['--to', '0'], True)):
            with self.subTest(args=args, narration=narration):
                self.log.unlink(missing_ok=True)
                done, calls = self.run_export(*args, narration=narration)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(self.captions(calls), [])

    def test_an_unreviewed_exporter_fails_before_any_export(self):
        source = self.engine / 'tools/export.mjs'
        source.write_bytes(self.original + b'\n')
        self.original = source.read_bytes()
        done, calls = self.run_export()
        self.assertEqual(done.returncode, 2)
        self.assertIn('differs from the reviewed source', done.stderr)
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
