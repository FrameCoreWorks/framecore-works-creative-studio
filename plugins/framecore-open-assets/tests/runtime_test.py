"""Offline policy, transport, provenance and real decoder tests. No provider calls."""
import contextlib
import copy
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN / 'scripts'))
import core
import runtime


class Response(io.BytesIO):
    def __init__(self, body, status=200, headers=None):
        super().__init__(body)
        self.status, self.headers, self.url = status, headers or {}, 'https://sfxmint.com/api/v1/search?q=click'


class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
    def tearDown(self):
        self.tmp.cleanup()
    def client(self, provider='sfxmint'):
        return core.Client(provider, self.root / 'state', 'chatgpt_work', 'test-model')
    def fixture(self, name):
        return json.loads((PLUGIN / 'tests/fixtures' / (name + '.json')).read_text())

    def test_provider_lock_blocks_concurrency_and_survives_reuse(self):
        client = self.client()
        lock = client.state / 'sfxmint.lock'
        lock.write_text('old completed process')
        with patch('time.sleep'):
            with client.serial():
                with self.assertRaises(core.Refused) as raised:
                    with self.client().serial():
                        self.fail('Concurrent request acquired a held lock')
                self.assertEqual(raised.exception.kind, 'busy')
            with self.assertRaisesRegex(RuntimeError, 'interrupted'):
                with client.serial():
                    raise RuntimeError('interrupted')
            with self.client().serial():
                pass
        self.assertTrue(lock.exists())

    @unittest.skipIf(sys.platform == 'win32', 'POSIX abrupt-exit lock test; Windows branch not run here')
    def test_provider_lock_releases_when_process_exits_abruptly(self):
        import subprocess
        client = self.client()
        code = ('import sys,os; sys.path.insert(0,sys.argv[1]); import core; '
                'c=core.Client("sfxmint",sys.argv[2],"chatgpt_work","test"); '
                'lock=c.serial(); lock.__enter__(); os._exit(0)')
        run = subprocess.run([sys.executable, '-c', code, str(PLUGIN/'scripts'), str(client.state)],
                             capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        with patch('time.sleep'), client.serial():
            pass

    def test_licence_urls_fail_closed(self):
        for value in ('CC0', 'https://evil.test/licenses/by/4.0/', 'https://creativecommons.org.evil.test/publicdomain/zero/1.0/',
                      'https://creativecommons.org/licenses/by-nc/4.0/', 'https://creativecommons.org/licenses/by-nd/4.0/', '', None):
            self.assertEqual(core.license_policy(value)[1], 'blocked', value)
        self.assertEqual(core.license_policy(core.CC0), ('CC0', 'eligible'))
        self.assertEqual(core.license_policy('https://creativecommons.org/licenses/by-sa/4.0/')[1], 'review_sa')

    def test_unreviewed_hosts_and_credentials_are_refused(self):
        for url in ('http://sfxmint.com/a', 'https://sfxmint.com.evil.test/a', 'https://u:p@sfxmint.com/a',
                    'https://127.0.0.1/a', 'https://sfxmint.com:8080/a', 'https://sfxmint.com/a\nX: value'):
            with self.assertRaises(core.Refused):
                core.validate_url(url, ['sfxmint.com'])

    def test_policy_hold_prevents_network(self):
        with patch('urllib.request.build_opener') as network:
            with self.assertRaisesRegex(core.Refused, 'Terms'):
                self.client('finna')
            network.assert_not_called()

    def test_http_block_records_headers_and_does_not_retry(self):
        client = self.client()
        with patch('urllib.request.OpenerDirector.open', return_value=Response(b'<html>', 403, {'cf-mitigated':'challenge','cf-ray':'test'})) as call:
            with self.assertRaises(core.Refused) as raised:
                client.get('https://sfxmint.com/a', 'Test challenge classification')
        self.assertEqual(raised.exception.kind, 'cloudflare_challenge')
        self.assertEqual(call.call_count, 1)
        self.assertEqual(client.trace[0]['headers']['cf-ray'], 'test')

    def test_html_and_size_caps_refuse_false_media(self):
        for data, cap, headers in [(b'<html>oops</html>', 100, {}), (b'abcdef', 3, {}),
                                  (b'{}', 100, {'content-type':'text/html'})]:
            client = self.client()
            with patch.object(client, 'serial', contextlib.nullcontext), patch('urllib.request.OpenerDirector.open', return_value=Response(data, headers=headers)):
                with self.assertRaises(core.Refused):
                    client.get('https://sfxmint.com/a', 'Test bounded response validation', cap=cap)

    def test_cache_obeys_no_store_and_fresh_mode(self):
        for directive, calls in [('max-age=3600',1), ('no-store, max-age=3600',2), ('private, max-age=3600',2), ('no-cache',2)]:
            with tempfile.TemporaryDirectory() as state:
                client=core.Client('sfxmint',state,'chatgpt_work','test')
                with patch.object(client,'serial',contextlib.nullcontext), patch('urllib.request.OpenerDirector.open', side_effect=lambda *a,**k:Response(b'{"ok":true}',headers={'cache-control':directive})) as call:
                    client.json('https://sfxmint.com/a','Test cache first read')
                    client.json('https://sfxmint.com/a','Test cache second read')
                    self.assertEqual(call.call_count,calls)
                    client.fresh=True
                    client.json('https://sfxmint.com/a','Test explicit fresh read')
                    self.assertEqual(call.call_count,calls+1)

    def test_provenance_rejects_changed_rights_and_host(self):
        payload={'utc':core.utc(),'fingerprint':runtime.fingerprint(),'host':'chatgpt_work','items':[{'license':'Unknown'}]}
        signed=runtime.seal(payload,self.root)
        self.assertEqual(runtime.unseal(signed,self.root),payload)
        bad=copy.deepcopy(signed);bad['payload']['items'][0]['license']='CC0'
        with self.assertRaises(core.Refused):runtime.unseal(bad,self.root)
        bad=copy.deepcopy(signed);bad['payload']['host']='claude_code'
        with self.assertRaises(core.Refused):runtime.unseal(bad,self.root)

    def test_status_does_not_create_state_or_contact_network(self):
        state=self.root/'absent'
        with patch('urllib.request.build_opener') as network,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runtime.main(['--state',str(state),'status']),0)
        self.assertFalse(state.exists());network.assert_not_called()

    def test_local_decoder_rejects_playlist(self):
        p=self.root/'fake.mp3';p.write_text('#EXTM3U\nfile:///etc/passwd\n')
        with self.assertRaises(core.Refused):core.decode(p)

    def test_real_png_decode_and_sidecar(self):
        from PIL import Image
        image=io.BytesIO();Image.new('RGB',(12,8)).save(image,format='PNG')
        client=self.client()
        item=core.asset('sfxmint','test','Test','Author','https://sfxmint.com/sounds/test',
                        [core.variant('https://sfxmint.com/test.png')],core.CC0,'graphics')
        target=self.root/'image.png'
        with patch.object(client,'get',return_value=(image.getvalue(),{'content-type':'image/png'})):
            result=core.download(client,item,target)
            self.assertEqual(result['verification']['width'],12)
            self.assertTrue(Path(str(target)+'.asset.json').exists())
            with self.assertRaises(core.Refused):core.download(client,item,target)

    def test_rights_refusal_and_hash_mismatch_leave_no_media(self):
        client=self.client()
        item=core.asset('sfxmint','test','Test','Author','https://sfxmint.com/sounds/test',
                        [core.variant('https://sfxmint.com/test.wav',sha256='0'*64)],core.CC0,'sfx')
        target=self.root/'bad.wav'
        with patch.object(client,'get',return_value=(b'bad',{})) as network:
            item['rights_status']='blocked'
            with self.assertRaises(core.Refused):core.download(client,item,target,technical_only=True)
            network.assert_not_called()
            item['rights_status']='eligible'
            with self.assertRaises(core.Refused):core.download(client,item,target)
        self.assertFalse(target.exists())

    def test_all_ten_adapters_parse_observed_provider_shapes(self):
        fixtures={'met':['met-search-v1-1','met-metadata'],'commons':['commons-search'],
                  'cleveland':['cleveland-search'],'wellcome':['wellcome-search'],'ambientcg':['ambientcg-search'],
                  'polyhaven':['polyhaven-search','polyhaven-files'],'phylopic':['phylopic-search','phylopic-page','phylopic-image'],
                  'sfxmint':['sfxmint-search'],'librivox':['librivox-search'],'nasa':['nasa-search','nasa-manifest']}
        for provider,names in fixtures.items():
            with self.subTest(provider=provider):
                client=self.client(provider)
                category=core.REGISTRY[provider]['smoke_category']
                with patch.object(client,'json',side_effect=[self.fixture(n) for n in names]):
                    result=runtime.search_one(client,'test',category,1)
                self.assertEqual(len(result),1)
                self.assertTrue(result[0]['source_page'])
                self.assertTrue(result[0]['variants'])
                expected={'commons':'review_sa','nasa':'review_nasa','librivox':'review_jurisdiction'}.get(provider,'eligible')
                self.assertEqual(result[0]['rights_status'],expected)

    def test_met_metadata_is_not_blanket_image_clearance(self):
        client=self.client('met');obj=self.fixture('met-metadata');obj['isPublicDomain']=False
        with patch.object(client,'json',side_effect=[self.fixture('met-search-v1-1'),obj]):
            self.assertEqual(runtime.search_one(client,'test','graphics',1),[])

    def test_daily_limit_is_reserved_before_request(self):
        client=self.client();client.state.mkdir(exist_ok=True)
        (client.state/('sfxmint-'+core.utc()[:10]+'.json')).write_text(json.dumps([str(i) for i in range(20)]))
        item=core.asset('sfxmint','next','Next','Author','https://sfxmint.com/sounds/next',
                        [core.variant('https://sfxmint.com/next.wav')],core.CC0,'sfx')
        with patch.object(client,'get') as call:
            with self.assertRaises(core.Refused):core.download(client,item,self.root/'next.wav')
            call.assert_not_called()

    def test_texture_projects_are_retained_unexecuted_and_not_claimed_decoded(self):
        from PIL import Image
        import zipfile
        image=io.BytesIO();Image.new('RGB',(8,8)).save(image,format='PNG')
        archive=self.root/'texture.zip'
        with zipfile.ZipFile(archive,'w') as z:
            z.writestr('Color.png',image.getvalue());z.writestr('material.blend',b'not executed')
        result=core.decode(archive)
        self.assertEqual(result['decoded_images'],1)
        self.assertEqual(result['unverified_project_members'],['material.blend'])
        self.assertFalse(result['extracted']);self.assertTrue(result['crc_verified'])
        with zipfile.ZipFile(archive,'a') as z:z.writestr('run.py',b'print(1)')
        with self.assertRaises(core.Refused):core.decode(archive)

    def test_phylopic_page_uses_discovered_build(self):
        client=self.client('phylopic')
        with patch.object(client,'json',side_effect=[self.fixture('phylopic-search'),self.fixture('phylopic-page'),self.fixture('phylopic-image')]) as call:
            runtime.search_one(client,'felis catus','graphics',1)
        self.assertNotIn('page=',call.call_args_list[0].args[0])
        self.assertIn('build=560',call.call_args_list[1].args[0])

    def test_malformed_provider_shape_returns_structured_failure(self):
        output=io.StringIO()
        with patch.object(core.Client,'json',return_value=[]),contextlib.redirect_stdout(output):
            code=runtime.main(['--state',str(self.root/'state'),'search','--provider','met',
                               '--category','graphics','--query','sunflowers','--host','chatgpt_work',
                               '--model','test','--out',str(self.root/'result.json')])
        self.assertEqual(code,2)
        self.assertEqual(json.loads(output.getvalue())['status'],'FAIL')
        self.assertFalse((self.root/'result.json').exists())


if __name__=='__main__':unittest.main()
