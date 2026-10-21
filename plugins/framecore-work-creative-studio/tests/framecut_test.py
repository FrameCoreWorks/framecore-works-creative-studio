"""Behavioral contract and decoded-media regressions for FrameCut; no external assets/models."""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / 'skills/opencut-video-studio/assets/framecut'
sys.path.insert(0, str(RUNTIME))
from fc_core import (FrameCutError, apply_operations, atomic_json, commit_revision, confined, file_hash, fingerprint,
                     ratio, read_json, round_boundary, validate)
from fc_media import ffmpeg, ingest, probe, run, transcript_import
from fc_captions import project_captions, sidecars
from fc_render import bind_motion, compile_project, delivery_readiness, motion_request, render, validate_review, verify_delivery
from framecut import project_init, export_edit, propose


def base_project(root):
    return project_init(root / 'project.json', 'test')


def sequence(fps=None):
    return {'id': 'main', 'fps': fps or {'num': 30, 'den': 1}, 'duration': 60,
            'clips': [], 'texts': [{'id': 'title', 'start': 0, 'duration': 45, 'text': 'Zażółć gęślą', 'position': 'top'}]}


class Contract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.p = base_project(self.root)
        self.p['sequences'] = [sequence()]
        self.p['deliverables'] = [{'id': 'wide', 'sequence': 'main', 'width': 320, 'height': 180}]

    def tearDown(self): self.tmp.cleanup()

    def test_motion_request_bounds(self):
        for event in ({'id':'m','start':50,'duration':11}, {'id':'m','start':-1,'duration':1}, {'id':'m','start':0,'duration':True}):
            with self.assertRaises(FrameCutError): motion_request(self.p,self.p['sequences'][0],event,self.p['deliverables'][0])

    def test_review_readiness_never_promotes_partial_or_failed_review(self):
        e={'reviewer':'fixture','scope':'all frames','observations':'synthetic test','outcome':'pass','picture_watched':True,'audio_heard':True}
        self.assertEqual(delivery_readiness({'status':'NOT_RUN'})['status'],'REVIEW_REQUIRED')
        self.assertEqual(delivery_readiness(e)['status'],'REVIEW_REQUIRED')
        e['coverage']='full';self.assertEqual(delivery_readiness(e)['status'],'READY')
        e['audio_heard']=False;self.assertEqual(delivery_readiness(e)['status'],'REVIEW_REQUIRED')
        e['audio_intentionally_silent']=True;self.assertEqual(delivery_readiness(e)['status'],'READY')
        e['outcome']='needs_revision';self.assertEqual(delivery_readiness(e)['status'],'BLOCKED')
        for k,v in [('reviewer',True),('scope',[]),('audio_heard','yes'),('coverage','almost')]:
            bad=copy.deepcopy(e);bad[k]=v
            with self.assertRaises(FrameCutError):validate_review(bad)

    def test_exact_rational_clock_and_sample_boundary(self):
        fps = ratio({'num': 30000, 'den': 1001})
        self.assertEqual(Fraction(18000)/fps, Fraction(3003,5))
        self.assertEqual(round_boundary(Fraction(18000)/fps*48000), 28828800)
        self.assertEqual(round_boundary(Fraction(1,2)), 1)
        self.assertEqual(round_boundary(Fraction(-1,2)), -1)

    def test_bool_and_nonfinite_not_numbers(self):
        for value in (True, float('nan'), float('inf'), -2, 0):
            p = copy.deepcopy(self.p); p['sequences'][0]['duration'] = value
            with self.assertRaises((FrameCutError, ValueError)): validate(p)

    def test_unknown_schema_and_fields(self):
        for value in (True, '1', 0, 2):
            p = copy.deepcopy(self.p); p['schema_version'] = value
            with self.assertRaises(FrameCutError): validate(p)
        p = copy.deepcopy(self.p); p['shell'] = 'echo unsafe'
        with self.assertRaises(FrameCutError): validate(p)

    def test_duplicate_json_key_rejected(self):
        f = self.root / 'bad.json'; f.write_text('{"id":1,"id":2}')
        with self.assertRaises(FrameCutError): read_json(f)

    def test_traversal_absolute_and_symlink(self):
        for v in ('../outside', '/tmp/outside', 'a/../b', 'a//b', 'a\\b'):
            with self.assertRaises(FrameCutError): confined(self.root, v)
        (self.root/'link').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(FrameCutError): confined(self.root, 'link/output')

    def test_unicode_and_spaces(self):
        f = confined(self.root, "materiał ' Łódź [1], #/wynik.json")
        atomic_json(f, {'text': 'żółć'})
        self.assertEqual(read_json(f)['text'], 'żółć')

    def test_outputs_are_not_overwritten(self):
        f = self.root/'protected.json'; atomic_json(f, {'a': 1})
        with self.assertRaises(FrameCutError): atomic_json(f, {'a': 2})
        self.assertEqual(read_json(f), {'a': 1})

    def test_stale_revision_and_immutable_history(self):
        first = commit_revision(self.root/'project.json', self.p, 1, 'assemble')
        with self.assertRaises(FrameCutError) as error: commit_revision(self.root/'project.json', first, 1, 'stale')
        self.assertEqual(error.exception.code, 'stale_revision')
        original = read_json(self.root/'.framecut/test/history/r1.json')
        self.assertEqual(original['sequences'], [])
        self.assertEqual(first['revision'], 2)

    def test_unknown_operation_does_not_mutate(self):
        before = fingerprint(self.p)
        with self.assertRaises(FrameCutError): apply_operations(self.p, [{'op':'execute','sequence':'main','value':'touch x'}])
        self.assertEqual(before, fingerprint(self.p))

    def test_caption_revision_keeps_analysis(self):
        revised, invalid = apply_operations(self.p, [{'op':'set_captions','sequence':'main','value':{'enabled':False,'size':.08}}])
        self.assertEqual(revised['analyses'], self.p['analyses'])
        self.assertNotIn('mix', invalid)
        self.assertNotIn('picture', invalid)

    def test_orphan_anchor_rejected(self):
        self.p['sequences'][0]['texts'][0].pop('start')
        self.p['sequences'][0]['texts'][0]['anchor'] = {'clip':'gone','offset':0}
        with self.assertRaises(FrameCutError) as e: validate(self.p)
        self.assertEqual(e.exception.code,'missing_anchor')

    def test_invalid_locks_cannot_corrupt_project(self):
        for bad in (None, 'take', ['missing'], [True]):
            with self.assertRaises(FrameCutError):
                apply_operations(self.p, [{'op':'set_locks','value':bad}])
        self.assertEqual(read_json(self.root/'project.json')['locks'], [])

    def test_no_speech_does_not_invent_transcript(self):
        self.p['assets']['still'] = {'sha256':'a'*64}
        result = propose(self.p, 'still')
        self.assertEqual(result['candidates'], [])
        self.assertEqual(result['status'], 'needs_editorial_analysis')

    def test_caption_projection_and_owner_sidecars(self):
        p = self.p
        p['assets']['a'] = {'probe':{'time_base':'1/1000','start_pts':5000}}
        p['analyses']['a'] = {'timing':'manual','words':[{'id':'w','text':'Żółć','start':10.4,'end':10.8}]}
        seq = p['sequences'][0]; seq['duration']=240
        seq['clips'] = [{'id':'c','asset':'a','start':120,'duration':120,'source_in':15000}]
        projection = project_captions(p,seq)
        self.assertEqual((projection['words'][0]['start'],projection['words'][0]['end']),(132,144))
        files = sidecars(projection,'pl')
        self.assertIn('00:00:04,400 --> 00:00:04,800', files['srt'])
        self.assertIn('Żółć',files['vtt'])

    def test_independent_narration_caption_source_and_anchor(self):
        p=self.p;p['assets']['a']={'probe':{'time_base':'1/1000','start_pts':0}}
        p['analyses']['a']={'timing':'manual','words':[{'id':'w','text':'narration','start':.2,'end':.6}]}
        seq=p['sequences'][0];seq['clips']=[{'id':'picture','asset':'a','start':15,'duration':30}]
        seq['audio']=[{'id':'voice','asset':'a','anchor':{'clip':'picture','offset':3},'duration':30}]
        seq['captions']={'sources':['voice']}
        result=project_captions(p,seq)
        self.assertEqual(result['words'][0]['start'],24)
        self.assertEqual(result['words'][0]['clip'],'voice')

    def test_half_source_tick_quantization_is_not_a_clipped_word(self):
        p=self.p;p['assets']['a']={'probe':{'time_base':'1/15360','start_pts':0}}
        p['analyses']['a']={'words':[{'id':'w','text':'word','start':3.28,'end':3.5}]}
        seq=p['sequences'][0];seq['clips']=[{'id':'c','asset':'a','start':0,'duration':30,'source_in':50381}]
        result=project_captions(p,seq)
        self.assertEqual(result['warnings'],[])
        self.assertEqual(result['words'][0]['start'],0)

    def test_cut_word_and_segment_are_flagged(self):
        p=self.p; p['assets']['a']={'probe':{'time_base':'1/1000','start_pts':0}}
        seq=p['sequences'][0]; seq['clips']=[{'id':'c','asset':'a','start':0,'duration':30,'source_in':500}]
        for key,code in [('words','clipped_word'),('segments','partial_segment')]:
            p['analyses']['a']={key:[{'id':'w','text':'not safe','start':0.4,'end':0.8}]}
            self.assertEqual(project_captions(p,seq)['warnings'][0]['code'],code)

    def test_unknown_word_time_never_becomes_zero(self):
        p=self.p; p['assets']['a']={'probe':{'time_base':'1/1000','start_pts':0}}
        p['analyses']['a']={'words':[{'id':'w','text':'unknown','start':None,'end':None}]}
        seq=p['sequences'][0]; seq['clips']=[{'id':'c','asset':'a','start':0,'duration':30,'source_in':0}]
        result=project_captions(p,seq)
        self.assertEqual(result['words'],[]); self.assertEqual(result['warnings'][0]['code'],'unknown_timing')

    def test_child_timeout_is_bounded(self):
        with self.assertRaises(FrameCutError) as e: run([sys.executable,'-c','import time; time.sleep(5)'], .05)
        self.assertEqual(e.exception.code,'resource_limit')

    def test_missing_capability_is_specific(self):
        with self.assertRaises(FrameCutError) as e: run(['framecut-no-such-executable'],1)
        self.assertEqual(e.exception.code,'missing_capability')


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg/FFprobe not installed')
class Media(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = tempfile.TemporaryDirectory(); cls.source = Path(cls.fixtures.name)/'source.mp4'
        ffmpeg(['-f','lavfi','-i','color=red:s=320x180:r=30:d=3','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3',
                '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(cls.source)])

    @classmethod
    def tearDownClass(cls): cls.fixtures.cleanup()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        shutil.copy2(self.source,self.root/'source.mp4')
        self.p=base_project(self.root); self.p['assets']['a']=ingest(self.root,'source.mp4','a')
        self.p['sequences']=[sequence()]; self.p['sequences'][0]['clips']=[{'id':'c1','asset':'a','start':0,'duration':60,'source_in':0}]
        self.p['deliverables']=[{'id':'wide','sequence':'main','width':320,'height':180}]
        self.p['authorization']='Authorized synthetic test render'

    def tearDown(self): self.tmp.cleanup()

    def motion_fixture(self):
        seq=self.p['sequences'][0];seq['duration']=90;seq['clips'][0]['duration']=90
        self.p=commit_revision(self.root/'project.json',self.p,1,'request fixture')
        atomic_json(self.root/'motion.json',{'renderer':'synthetic FFmpeg fixture'})
        return motion_request(self.p,self.p['sequences'][0],self.p['sequences'][0]['clips'][0],self.p['deliverables'][0])

    def test_motion_return_survives_ingest_revision_and_rejects_moved_placement(self):
        request=self.motion_fixture()
        self.p['assets']['new']=ingest(self.root,'source.mp4','new')
        self.p=commit_revision(self.root/'project.json',self.p,2,'ingest return')
        self.p['assets']['a']['motion_contract']=bind_motion(self.p,self.root,'a','motion.json',Fraction(30),request)
        self.p=commit_revision(self.root/'project.json',self.p,3,'bind return')
        compile_project(self.p,self.root,'wide')
        self.p['sequences'][0]['duration']=120;self.p['sequences'][0]['clips'][0]['start']=30
        with self.assertRaises(FrameCutError) as e:compile_project(self.p,self.root,'wide')
        self.assertEqual(e.exception.code,'stale_revision')

    def test_motion_rejects_changed_context_and_wrong_project(self):
        request=self.motion_fixture()
        for change in ('brief','sequence','delivery','project'):
            p=copy.deepcopy(self.p);r=copy.deepcopy(request)
            if change=='brief':p['brief']['style']='changed'
            elif change=='sequence':p['sequences'][0]['duration']=91
            elif change=='delivery':p['deliverables'][0]['width']=640
            else:r['project_id']='other'
            if change!='project':p=commit_revision(self.root/'project.json',p,p['revision'],'changed context');self.p=p
            with self.assertRaises(FrameCutError) as e:bind_motion(p,self.root,'a','motion.json',Fraction(30),r)
            self.assertEqual(e.exception.code,'stale_revision')

    def test_motion_media_duration_fps_dimensions_and_alpha_are_checked(self):
        request=self.motion_fixture()
        for field,value in [('duration_frames',60),('alpha','straight')]:
            r=copy.deepcopy(request);r[field]=value
            with self.assertRaises(FrameCutError) as e:bind_motion(self.p,self.root,'a','motion.json',Fraction(30),r)
            self.assertEqual(e.exception.code,'qa_failed')
        with self.assertRaises(FrameCutError):bind_motion(self.p,self.root,'a','motion.json',Fraction(24),request)
        ffmpeg(['-f','lavfi','-i','color=blue:s=160x90:r=30:d=3','-c:v','libx264',str(self.root/'small.mp4')])
        self.p['assets']['small']=ingest(self.root,'small.mp4','small')
        self.p=commit_revision(self.root/'project.json',self.p,2,'ingest wrong size')
        with self.assertRaises(FrameCutError) as e:bind_motion(self.p,self.root,'small','motion.json',Fraction(30),request)
        self.assertEqual(e.exception.code,'qa_failed')

    def test_legacy_motion_binding_is_preview_only(self):
        atomic_json(self.root/'motion.json',{'renderer':'legacy'})
        self.p['assets']['a']['motion_contract']={'path':'motion.json','sha256':file_hash(self.root/'motion.json'),'fps':{'num':30,'den':1}}
        self.assertIn('unbound_motion',[w['code'] for w in compile_project(self.p,self.root,'wide')['warnings']])
        with self.assertRaises(FrameCutError) as e:render(self.p,self.root,'wide','blocked',mode='final',max_disk_mb=128)
        self.assertEqual(e.exception.code,'qa_failed');self.assertFalse((self.root/'blocked').exists())

    def test_review_cli_records_partial_then_full_without_losing_previous_evidence(self):
        self.p=commit_revision(self.root/'project.json',self.p,1,'assemble')
        render(self.p,self.root,'wide','reviewed',max_disk_mb=128)
        self.assertEqual(verify_delivery(self.p,self.root,'reviewed')['delivery_readiness']['status'],'REVIEW_REQUIRED')
        e={'reviewer':'synthetic test only','scope':'fixture','observations':'tests recording, not a real media review','outcome':'pass','picture_watched':True,'audio_heard':True,'coverage':'sampled'}
        for coverage,expected in [('sampled','REVIEW_REQUIRED'),('full','READY')]:
            e['coverage']=coverage;(self.root/'evidence.json').write_text(json.dumps(e))
            run([sys.executable,str(RUNTIME/'framecut.py'),'review',str(self.root/'project.json'),'--bundle','reviewed','--evidence',str(self.root/'evidence.json')])
            self.assertEqual(verify_delivery(self.p,self.root,'reviewed')['delivery_readiness']['status'],expected)
        self.assertEqual(len(list((self.root/'reviewed/review/history').glob('*.json'))),1)

    def test_changed_source_rejected_before_render(self):
        with (self.root/'source.mp4').open('ab') as f: f.write(b'changed')
        with self.assertRaises(FrameCutError) as e: compile_project(self.p,self.root,'wide')
        self.assertEqual(e.exception.code,'stale_source')

    def test_insufficient_handles_and_overlap(self):
        self.p['sequences'][0]['clips'][0]['source_in']=15360*2
        with self.assertRaises(FrameCutError) as e: validate(self.p,self.root)
        self.assertEqual(e.exception.code,'insufficient_handles')
        self.p['sequences'][0]['clips'][0]['source_in']=0
        self.p['sequences'][0]['clips'].append({'id':'c2','asset':'a','start':30,'duration':30})
        with self.assertRaises(FrameCutError): validate(self.p)

    def test_transition_cannot_overrun_short_previous_clip(self):
        seq=self.p['sequences'][0];seq['duration']=90
        seq['clips']=[{'id':'first','asset':'a','start':0,'duration':45}, {'id':'short','asset':'a','start':45,'duration':15},
                      {'id':'third','asset':'a','start':30,'duration':60,'transition':30}]
        with self.assertRaises(FrameCutError): validate(self.p)

    def test_final_frame_count_sources_and_audio_unchanged_by_title_revision(self):
        original=file_hash(self.root/'source.mp4')
        render(self.p,self.root,'wide','first','final',max_disk_mb=128)
        first=read_json(self.root/'first/receipt.json')
        self.assertEqual(first['technical']['decoded_frames'],60)
        self.assertEqual(verify_delivery(self.p,self.root,'first')['status'],'PASS')
        self.p['revision']+=1; self.p['sequences'][0]['texts'][0]['size']=.1
        result=render(self.p,self.root,'wide','second','final',max_disk_mb=128)
        self.assertIn('mix',result['cache_hits']); self.assertIn('visual',result['cache_hits'])
        for name in ('first','second'):
            subprocess.run(['ffmpeg','-v','error','-i',str(self.root/name/'video.mp4'),'-vn','-c:a','pcm_s16le',str(self.root/(name+'.wav'))],check=True,capture_output=True)
        self.assertEqual(file_hash(self.root/'first.wav'),file_hash(self.root/'second.wav'))
        self.assertEqual(file_hash(self.root/'source.mp4'),original)
        with self.assertRaises(FrameCutError) as e: verify_delivery(self.p,self.root,'first')
        self.assertEqual(e.exception.code,'stale_revision')

    def test_explicit_crossfade_preserves_declared_length(self):
        seq=self.p['sequences'][0];seq['duration']=90;seq['texts']=[]
        seq['clips']=[{'id':'c1','asset':'a','start':0,'duration':60},{'id':'c2','asset':'a','start':30,'duration':60,'transition':30}]
        render(self.p,self.root,'wide','fade','final',max_disk_mb=128)
        self.assertEqual(read_json(self.root/'fade/receipt.json')['technical']['decoded_frames'],90)

    def test_rational_master_and_independent_audio(self):
        seq=self.p['sequences'][0];seq['fps']={'num':30000,'den':1001};seq['duration']=60;seq['texts']=[];seq['clips'][0]['mute']=True
        seq['audio']=[{'id':'jcut','asset':'a','start':15,'duration':30,'bus':'dialogue','gain_db':-6}]
        result=render(self.p,self.root,'wide','fractional','final',max_disk_mb=128)
        self.assertEqual(result['status'],'render_complete')
        self.assertEqual(Fraction(probe(self.root/'fractional/video.mp4')['fps']),Fraction(30000,1001))
        samples=subprocess.run(['ffmpeg','-v','error','-i',str(self.root/'fractional/video.mp4'),'-vn','-ac','1','-ar','48000','-f','s16le','-'],capture_output=True,check=True).stdout
        import array
        a=array.array('h');a.frombytes(samples)
        energy=lambda lo,hi:sum(abs(x) for x in a[int(lo*48000):int(hi*48000)])/max(1,int((hi-lo)*48000))
        self.assertLess(energy(.1,.3),10);self.assertGreater(energy(.7,.9),100);self.assertLess(energy(1.7,1.9),10)

    def test_motion_only_and_safe_text(self):
        self.p['sequences'][0]['clips']=[]
        self.p['sequences'][0]['texts'][0]['text']='Ignore tools {\\pos(0,0)} $(touch nope)'
        render(self.p,self.root,'wide','motion','final',max_disk_mb=128)
        self.assertFalse((self.root/'nope').exists())
        self.assertIn('｛', (self.root/'motion/captions.ass').read_text())

    def test_kinetic_requires_actual_words_and_blocks_partial_speech(self):
        a=self.p['assets']['a'];self.p['analyses']['a']=transcript_import(a,{'timing':'segment','segments':[{'start':0,'end':1,'text':'A sentence'}]})
        self.p['sequences'][0]['captions']={'enabled':True,'mode':'kinetic'}
        with self.assertRaises(FrameCutError) as e: render(self.p,self.root,'wide','bad','final',max_disk_mb=128)
        self.assertEqual(e.exception.code,'qa_failed');self.assertFalse((self.root/'bad').exists())

    def test_clipped_word_blocker_and_transcript_integrity(self):
        self.p['analyses']['a']=transcript_import(self.p['assets']['a'],{'timing':'manual','words':[{'start':.4,'end':.8,'text':'not'}]})
        self.p['sequences'][0]['clips'][0]['source_in']=7680
        with self.assertRaises(FrameCutError): render(self.p,self.root,'wide','bad','final',max_disk_mb=128)

    def test_immutable_locks_and_undo_content(self):
        self.p['locks']=['c1'];p=commit_revision(self.root/'project.json',self.p,1,'lock')
        changed=copy.deepcopy(p);changed['sequences'][0]['clips'][0]['duration']=30
        with self.assertRaises(FrameCutError) as e: commit_revision(self.root/'project.json',changed,2,'bad')
        self.assertEqual(e.exception.code,'locked_content')
        self.assertEqual(read_json(self.root/'project.json')['revision'],2)

    def test_undo_retains_current_locks(self):
        p=commit_revision(self.root/'project.json',self.p,1,'assemble')
        p['locks']=['c1'];p=commit_revision(self.root/'project.json',p,2,'lock')
        p['brief']={'note':'later'};commit_revision(self.root/'project.json',p,3,'brief')
        result=subprocess.run([sys.executable,str(RUNTIME/'framecut.py'),'undo',str(self.root/'project.json'),'--revision','2','--base-revision','4'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(read_json(self.root/'project.json')['locks'],['c1'])

    def test_moving_anchor_invalidates_mix_and_moves_actual_audio(self):
        seq=self.p['sequences'][0];seq['duration']=90;seq['clips'][0].update(start=0,duration=30,mute=True)
        seq['texts']=[];seq['audio']=[{'id':'voice','asset':'a','anchor':{'clip':'c1','offset':0},'duration':30}]
        render(self.p,self.root,'wide','before',max_disk_mb=128)
        seq['clips'][0]['start']=30;self.p['revision']+=1
        result=render(self.p,self.root,'wide','after',max_disk_mb=128)
        self.assertIn('mix',result['cache_built']);self.assertNotIn('mix',result['cache_hits'])
        samples=subprocess.run(['ffmpeg','-v','error','-i',str(self.root/'after/video.mp4'),'-vn','-ac','1','-ar','48000','-f','s16le','-'],capture_output=True,check=True).stdout
        import array
        a=array.array('h');a.frombytes(samples)
        self.assertLess(sum(abs(x) for x in a[12000:24000])/12000,10)
        self.assertGreater(sum(abs(x) for x in a[60000:72000])/12000,100)

    def test_hdr_is_not_silently_washed_out(self):
        self.p['assets']['a']['probe']['color_transfer']='smpte2084'
        with self.assertRaises(FrameCutError) as e: compile_project(self.p,self.root,'wide')
        self.assertEqual(e.exception.code,'unsupported_operation')

    def test_disk_budget_and_timeout_do_not_publish(self):
        with self.assertRaises(FrameCutError) as e: render(self.p,self.root,'wide','bad',max_disk_mb=1)
        self.assertEqual(e.exception.code,'resource_limit');self.assertFalse((self.root/'bad').exists())

    def test_export_is_honest_and_legacy_preserved(self):
        result=export_edit(self.p,self.root,'main','export')
        self.assertTrue((self.root/'export/picture.edl').exists())
        self.assertEqual(result['editor_import'],'NOT_RUN')
        self.assertTrue(any('Motion' in s for s in result['losses']))
        self.assertTrue((RUNTIME.parents[1]/'scripts/edit_export.py').exists())

    def test_corrupted_delivery_is_rejected(self):
        render(self.p,self.root,'wide','good',max_disk_mb=128)
        (self.root/'good/video.mp4').write_bytes(b'not a video')
        with self.assertRaises(FrameCutError) as e: verify_delivery(self.p,self.root,'good')
        self.assertEqual(e.exception.code,'qa_failed')


if __name__ == '__main__': unittest.main(verbosity=2)
