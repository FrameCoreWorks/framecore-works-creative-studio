"""Guard branches of scripts/publish_github_release.py: ambiguous release, foreign tag, partial upload."""
import hashlib
import importlib.util
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('publish_github_release', ROOT / 'scripts/publish_github_release.py')
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

SHA = 'a' * 40
OTHER = 'b' * 40
VERSION = '9.9.9'
TAG = 'v' + VERSION
NAMES = (
    f'framecore-work-creative-studio-{VERSION}.zip',
    f'framecore-work-creative-studio-{VERSION}.zip.inventory.json',
    f'framecore-works-creative-studio-{VERSION}-repository.zip',
    f'framecore-works-creative-studio-{VERSION}-repository.zip.inventory.json',
    f'framecore-motion-player-{VERSION}.html',
    'SHA256SUMS.txt',
)


class FakeGitHub:
    """Answers the script's `api` calls from in-memory releases and tags."""

    def __init__(self, releases, tag_sha=None):
        self.releases = releases
        self.tag_sha = tag_sha
        self.writes = []

    def __call__(self, path, payload=None, method='POST', missing_ok=False):
        if payload is not None:
            self.writes.append((method, path, payload))
            if path == 'releases':
                release = {'id': 1, 'tag_name': TAG, 'target_commitish': payload['target_commitish'],
                           'draft': True, 'assets': [], 'published_at': None, 'html_url': 'u'}
                self.releases.append(release)
                return release
            release = self.releases[0]
            release.update(draft=payload['draft'], published_at='now')
            return release
        if path.startswith('releases?'):
            return self.releases
        if path.startswith('git/ref/tags/'):
            if self.tag_sha is None:
                if missing_ok:
                    return None
                raise RuntimeError('HTTP 404')
            return {'object': {'type': 'commit', 'sha': self.tag_sha}}
        return self.releases[0]


class PublishGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        manifest = root / 'plugins/framecore-work-creative-studio/plugin.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({'version': VERSION}))
        (root / 'RELEASE_NOTES.md').write_text('notes\n')
        (root / 'dist').mkdir()
        self.digests = {}
        for name in NAMES:
            data = name.encode()
            (root / 'dist' / name).write_bytes(data)
            self.digests[name] = 'sha256:' + hashlib.sha256(data).hexdigest()
        patches = [
            mock.patch.object(pub, 'ROOT', root),
            mock.patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'GITHUB_REPOSITORY': pub.REPO,
                                         'GITHUB_SHA': SHA}),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.upload = mock.patch.object(pub.subprocess, 'run').start()
        self.addCleanup(mock.patch.stopall)

    def tearDown(self):
        self.tmp.cleanup()

    def asset(self, name):
        return {'name': name, 'state': 'uploaded', 'digest': self.digests[name]}

    def release(self, draft=True, commit=SHA, assets=()):
        return {'id': 1, 'tag_name': TAG, 'target_commitish': commit, 'draft': draft,
                'assets': [self.asset(n) for n in assets], 'published_at': None if draft else 'then',
                'html_url': 'u'}

    def run_with(self, fake):
        with mock.patch.object(pub, 'api', fake):
            pub.main()

    def test_two_releases_for_one_tag_stop_before_any_write(self):
        fake = FakeGitHub([self.release(), self.release()])
        with self.assertRaisesRegex(RuntimeError, 'Ambiguous release state'):
            self.run_with(fake)
        self.assertEqual(fake.writes, [])
        self.upload.assert_not_called()

    def test_tag_on_another_commit_is_never_replaced(self):
        fake = FakeGitHub([], tag_sha=OTHER)
        with self.assertRaisesRegex(RuntimeError, 'another commit'):
            self.run_with(fake)
        self.assertEqual(fake.writes, [])
        self.upload.assert_not_called()

    def test_release_from_another_source_is_left_for_inspection(self):
        fake = FakeGitHub([self.release(commit=OTHER)], tag_sha=SHA)
        with self.assertRaisesRegex(RuntimeError, 'different source'):
            self.run_with(fake)
        self.assertEqual(fake.writes, [])

    def test_partial_upload_on_published_release_is_not_patched(self):
        fake = FakeGitHub([self.release(draft=False, assets=NAMES[:3])], tag_sha=SHA)
        with self.assertRaisesRegex(RuntimeError, 'incomplete'):
            self.run_with(fake)
        self.upload.assert_not_called()

    def test_partial_upload_on_draft_resumes_only_missing_assets(self):
        fake = FakeGitHub([self.release(assets=NAMES[:3])], tag_sha=SHA)

        def finish_upload(cmd, **kwargs):
            fake.releases[0]['assets'].append(self.asset(pathlib.Path(cmd[4]).name))
        self.upload.side_effect = finish_upload
        self.run_with(fake)
        uploaded = [pathlib.Path(c.args[0][4]).name for c in self.upload.call_args_list]
        self.assertEqual(uploaded, list(NAMES[3:]))
        self.assertEqual(fake.writes[-1][0], 'PATCH')
        self.assertFalse(fake.releases[0]['draft'])

    def test_changed_existing_asset_blocks_publication(self):
        release = self.release(assets=NAMES[:1])
        release['assets'][0]['digest'] = 'sha256:' + '0' * 64
        fake = FakeGitHub([release], tag_sha=SHA)
        with self.assertRaisesRegex(RuntimeError, 'Existing asset differs'):
            self.run_with(fake)
        self.upload.assert_not_called()

    def test_unexpected_asset_is_preserved(self):
        release = self.release()
        release['assets'].append({'name': 'extra.zip', 'state': 'uploaded', 'digest': 'x'})
        fake = FakeGitHub([release], tag_sha=SHA)
        with self.assertRaisesRegex(RuntimeError, 'Unexpected release assets'):
            self.run_with(fake)


if __name__ == '__main__':
    unittest.main()
