"""A source handoff keeps byte identity and never promotes rejected rights."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import wave
S=Path(__file__).resolve().parents[1]/'skills/earshot/real-sound/scripts'
sys.path.insert(0,str(S))
import import_open_assets as bridge

class Import(unittest.TestCase):
    def test_handoff_and_rejections(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);audio=root/'sound.wav'
            with wave.open(str(audio),'wb') as f:
                f.setparams((1,2,8000,0,'NONE','not compressed'));f.writeframes(b'\x00\x00'*800)
            row={'technical_test_only':False,'rights_status':'eligible','category':'sfx','verification':{'kind':'audio'},
                 'license':'CC0','provider':'test','id':'1','title':'Click','creator':'Author','source_page':'https://example.org/1',
                 'license_url':'https://creativecommons.org/publicdomain/zero/1.0/','attribution':'Click — Author, CC0',
                 'selected_variant':{'url':'https://example.org/1.wav'},'saved_path':str(audio),
                 'sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'bytes':audio.stat().st_size}
            sidecar=root/'sound.asset.json';sidecar.write_text(json.dumps(row))
            entry,studio=bridge.prepare(sidecar,root,'click')
            self.assertEqual(entry['sha256'],studio['assets'][0]['sha256'])
            self.assertEqual(studio['assets'][0]['review']['status'],'not_reviewed')
            self.assertEqual(entry['attribution'],row['attribution'])
            for change in ({'technical_test_only':True},{'rights_status':'review_nasa'},{'license':'CC BY-SA 4.0'},
                           {'sha256':'0'*64},{'bytes':10},{'category':'photos'},{'license_url':'https://example.org/cc0'}):
                sidecar.write_text(json.dumps({**row,**change}))
                with self.assertRaises(ValueError):bridge.prepare(sidecar,root,'click')
            sidecar.write_text(json.dumps({**row,'license':'PDM','license_url':'https://creativecommons.org/publicdomain/mark/1.0/'}))
            self.assertEqual(bridge.prepare(sidecar,root,'click')[0]['license'],'Public Domain Mark 1.0')
            sidecar.write_text(json.dumps(row));audio.write_bytes(b'changed')
            with self.assertRaises(ValueError):bridge.prepare(sidecar,root,'click')
            row.update(sha256=hashlib.sha256(audio.read_bytes()).hexdigest(),bytes=audio.stat().st_size)
            sidecar.write_text(json.dumps(row))
            with self.assertRaises(ValueError):bridge.prepare(sidecar,root,'click')

if __name__=='__main__':unittest.main()
