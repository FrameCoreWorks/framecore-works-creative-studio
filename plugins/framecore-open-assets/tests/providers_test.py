"""Regression cases from the 2026-10-28 Work validation; no network."""
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import core
import runtime

class Policies(unittest.TestCase):
    def test_proof_cannot_move_to_another_provider_or_category(self):
        with tempfile.TemporaryDirectory() as root:
            data={'utc':core.utc(),'fingerprint':runtime.fingerprint(),'host':'chatgpt_work',
                  'provider':'commons','category':'photos','status':'PASS'}
            signed=json.dumps(runtime.seal(data,root))
            for provider,category,expected in [('commons','photos',True),('met','graphics',False),('commons','video',False)]:
                runtime.proof_path(root,'chatgpt_work',provider,category).write_text(signed)
                self.assertEqual(runtime.proof_valid(root,'chatgpt_work',provider,category),expected)

    def test_provider_interval_above_five_seconds_is_honoured(self):
        with tempfile.TemporaryDirectory() as root:
            c=core.Client('loc',root,'chatgpt_work','test')
            (Path(root)/'loc.last').write_text('100')
            with patch('time.time',return_value=100),patch('time.sleep') as sleep,c.serial():pass
            sleep.assert_called_once_with(6.1)

    def test_finna_locale_suffix_does_not_change_rights(self):
        self.assertEqual(core.license_policy(core.CC0+'deed.fi'),('CC0','eligible'))
        self.assertEqual(core.license_policy('https://creativecommons.org/licenses/by-nc/4.0/deed.fi')[1],'blocked')

    def test_loc_rejects_negated_dedication_and_clippings(self):
        module=importlib.import_module('providers.loc')
        row={'id':'https://www.loc.gov/item/123/','original_format':['photo, print, drawing'],
             'image_url':['https://tile.loc.gov/test.jpg'],'title':'Portrait','contributor':['Gottlieb']}
        for text,count in [('This is not in the public domain; permission is required.',0),
                           ('Mr. Gottlieb has dedicated these works to the public domain, but rights of privacy and publicity may apply.',1)]:
            c=Mock();c.json.side_effect=[{'results':[row]},{'item':{'rights_advisory':[text]}}]
            self.assertEqual(len(module.search(c,'portrait','photos',1)),count)
        c=Mock();c.json.return_value={'results':[{**row,'original_format':['manuscript']}]}
        self.assertEqual(module.search(c,'jazz','photos',1),[])
        self.assertEqual(c.json.call_count,1)

    def test_rijks_does_not_apply_metadata_cc0_to_image_or_invent_by_credit(self):
        module=importlib.import_module('providers.rijks')
        for licence,expected in [(core.PDM,'eligible'),('https://creativecommons.org/licenses/by/4.0/','blocked'),('', 'blocked')]:
            c=Mock();c.json.side_effect=[{'orderedItems':[{'id':'https://id.rijksmuseum.nl/1'}]},
                {'id':'https://id.rijksmuseum.nl/1','referred_to_by':[{'content':core.CC0}],
                 'subject_of':[{'digitally_carried_by':[{'access_point':[{'id':'https://iiif.micr.io/1/full/max/0/default.jpg'}],
                                                        'referred_to_by':[{'content':licence}]}]}]}]
            self.assertEqual(module.search(c,'work','graphics',1)[0]['rights_status'],expected)

    def test_audio_cannot_be_delivered_as_a_photo(self):
        with tempfile.TemporaryDirectory() as root:
            c=core.Client('met',Path(root)/'state','chatgpt_work','test')
            c.get=Mock(return_value=(b'fake',{'content-type':'audio/wav'}))
            item=core.asset('met','1','work','artist','https://metmuseum.org/',[core.variant('https://images.metmuseum.org/a.jpg')],core.CC0,'photos')
            with patch('core.decode',return_value={'kind':'audio'}),self.assertRaises(core.Refused) as error:
                core.download(c,item,Path(root)/'photo.jpg')
            self.assertEqual(error.exception.kind,'wrong_media_type')
            self.assertFalse((Path(root)/'photo.jpg').exists())

if __name__=='__main__':unittest.main()
