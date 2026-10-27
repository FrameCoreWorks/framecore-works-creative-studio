"""Openverse search (reference-pack-curator/scripts/openverse.py): offline parsing, licence filter, warnings,
failure classification (Cloudflare challenge, access, rate limit, server, timeout, invalid reply) and retries."""
import contextlib
import email.message
import importlib.util
import io
import json
import pathlib
import unittest
import urllib.error

TOOL = pathlib.Path(__file__).resolve().parent.parent / 'skills/reference-pack-curator/scripts/openverse.py'
spec = importlib.util.spec_from_file_location('openverse', TOOL)
ov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ov)

REPLY = {'result_count': 2, 'results': [
    {'title': 'Bakery', 'creator': 'InfoMofo', 'license': 'by-sa', 'license_version': '2.0', 'source': 'flickr',
     'url': 'https://example.org/a.jpg', 'attribution': '"Bakery" by InfoMofo is licensed under CC BY-SA 2.0.'},
    {'title': 'Bread', 'creator': None, 'license': 'cc0', 'url': 'https://example.org/b.jpg'}]}
CHALLENGE_PAGE = b'<!DOCTYPE html><title>Just a moment...</title>'


def headers(**fields):
    message = email.message.Message()
    for name, value in fields.items():
        message[name.replace('_', '-')] = value
    return message


class Reply(io.BytesIO):
    def __init__(self, body, status=200, **fields):
        super().__init__(body)
        self.status, self.headers = status, headers(**fields)


def opener_for(reply, seen):
    def opener(request, timeout):
        seen.append(request.full_url)
        return Reply(json.dumps(reply).encode(), Content_Type='application/json')
    return opener


def http_error(status, body=b'', **fields):
    return urllib.error.HTTPError('https://api.openverse.org/v1/images/', status, 'error', headers(**fields), io.BytesIO(body))


def run(argv, responses):
    """main() against a scripted series of replies or exceptions; returns exit code, printed JSON, calls and sleeps."""
    calls, sleeps, queue = [], [], list(responses)
    def opener(request, timeout):
        calls.append(request.full_url)
        item = queue.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item
    out = io.StringIO()
    original = ov.urllib.request.urlopen
    ov.urllib.request.urlopen = opener
    try:
        with contextlib.redirect_stdout(out):
            code = ov.main(argv, sleep=sleeps.append)
    finally:
        ov.urllib.request.urlopen = original
    return code, json.loads(out.getvalue()), calls, sleeps


def ok(reply):
    return Reply(json.dumps(reply).encode(), Content_Type='application/json')


class OpenverseTest(unittest.TestCase):
    def test_commercial_filter_and_warnings(self):
        seen = []
        found = ov.search('bakery', opener=opener_for(REPLY, seen))
        self.assertIn('/v1/images/', seen[0])
        self.assertIn('license_type=commercial%2Cmodification', seen[0])
        first, second = found['results']
        self.assertIn('share-alike', first['warnings'][0])
        self.assertEqual(first['attribution'], REPLY['results'][0]['attribution'])
        self.assertIn('creator unknown', second['warnings'][0])
        self.assertNotIn('creator', second)

    def test_audio_and_licence_options(self):
        seen = []
        ov.search('rain', media='audio', any_licence=True, opener=opener_for({'results': []}, seen))
        self.assertIn('/v1/audio/', seen[0])
        self.assertNotIn('license_type', seen[0])
        ov.search('door', media='audio', licence='cc0,by', opener=opener_for({'results': []}, seen))
        self.assertIn('license=cc0%2Cby', seen[1])

    def test_results_and_real_empty_results_keep_exit_codes(self):
        code, data, _, _ = run(['rain', '--media', 'audio'], [ok(REPLY)])
        self.assertEqual((code, len(data['results'])), (0, 2))
        code, data, _, _ = run(['zzz'], [ok({'result_count': 0, 'results': []})])
        self.assertEqual((code, data['results']), (1, []))
        self.assertNotIn('error', data)

    def test_cloudflare_challenge_is_classified_and_never_retried(self):
        error = http_error(403, CHALLENGE_PAGE, Content_Type='text/html; charset=UTF-8', CF_Mitigated='challenge', CF_Ray='a51115ddaab2381e-ORD')
        code, data, calls, sleeps = run(['sea', '--media', 'audio'], [error])
        self.assertEqual((code, data['error_type'], data['http_status'], data['cf_ray']), (3, 'cloudflare_challenge', 403, 'a51115ddaab2381e-ORD'))
        self.assertFalse(data['retryable'])
        self.assertEqual((len(calls), sleeps), (1, []))
        self.assertTrue(data['link'].startswith('https://openverse.org/search/audio?'))
        self.assertNotIn('Just a moment', json.dumps(data))

    def test_challenge_in_a_normal_response_and_lowercase_header(self):
        page = Reply(CHALLENGE_PAGE, 200, Content_Type='text/html')
        page.headers['cf-mitigated'] = 'Challenge'
        code, data, calls, _ = run(['sea'], [page])
        self.assertEqual((code, data['error_type'], len(calls)), (3, 'cloudflare_challenge', 1))

    def test_403_without_the_signature_is_not_cloudflare(self):
        code, data, calls, _ = run(['sea'], [http_error(403, b'{}', Content_Type='application/json')])
        self.assertEqual((code, data['error_type'], len(calls)), (3, 'access_denied', 1))

    def test_rate_limit_waits_for_a_short_retry_after_only(self):
        code, data, calls, sleeps = run(['sea'], [http_error(429, Retry_After='3'), ok(REPLY)])
        self.assertEqual((code, len(calls), sleeps), (0, 2, [3]))
        code, data, calls, sleeps = run(['sea'], [http_error(429, Retry_After='3600')])
        self.assertEqual((code, data['error_type'], data['retry_after'], len(calls), sleeps), (2, 'rate_limited', '3600', 1, []))

    def test_server_errors_and_timeouts_retry_within_the_budget(self):
        code, data, calls, sleeps = run(['sea'], [http_error(500), http_error(504), ok(REPLY)])
        self.assertEqual((code, len(calls), sleeps), (0, 3, [2, 5]))
        code, data, calls, sleeps = run(['sea'], [TimeoutError('slow')] * 3)
        self.assertEqual((code, data['error_type'], len(calls)), (3, 'timeout', ov.ATTEMPTS))
        code, data, calls, _ = run(['sea'], [urllib.error.URLError('refused')] * 3)
        self.assertEqual((code, data['error_type']), (3, 'connection_error'))

    def test_html_or_broken_json_without_a_challenge(self):
        code, data, calls, _ = run(['sea'], [Reply(b'<html>', 200, Content_Type='text/html')])
        self.assertEqual((code, data['error_type'], len(calls)), (3, 'invalid_response', 1))
        code, data, _, _ = run(['sea'], [Reply(b'[1, 2]', 200, Content_Type='application/json')])
        self.assertEqual(data['error_type'], 'invalid_response')

    def test_diagnostics_carry_no_secret_or_query(self):
        error = http_error(403, CHALLENGE_PAGE, CF_Mitigated='challenge', Set_Cookie='__cf_bm=secret', Authorization='Bearer x')
        _, data, _, _ = run(['private client name'], [error])
        text = json.dumps({k: v for k, v in data.items() if k != 'link'})
        for leak in ('secret', 'Bearer', 'private client name', '__cf_bm'):
            self.assertNotIn(leak, text)


if __name__ == '__main__':
    unittest.main()
