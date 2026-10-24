"""Concat-inspired FrameCut capabilities: original contracts and decoded-media checks."""
import copy
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from fractions import Fraction
from pathlib import Path

RUNTIME=Path(__file__).resolve().parents[1]/'skills/opencut-video-studio/assets/framecut'
sys.path.insert(0,str(RUNTIME))
from fc_core import FrameCutError, apply_operations, atomic_json, commit_revision, fingerprint, read_json, validate, ratio, span_seconds
from fc_time import parameters, source_offset, timeline_offset, trim_time
from fc_edit import timeline_read, change_impact
from fc_effects import check_fixtures, picture
from fc_media import ffmpeg, ingest
from fc_render import compile_project, render
from fc_board import panel_plan, preview_frame, storyboard
from framecut import project_init


def project():
    return {'schema_version':1,'id':'test','revision':1,'assets':{'a':{'path':'a.mp4','sha256':'a'*64,'kind':'video',
            'probe':{'time_base':'1/1000','clock':{'num':1,'den':1000},'start_pts':0,'duration':20,'has_audio':True}}},
            'analyses':{},'sequences':[{'id':'main','fps':{'num':30,'den':1},'duration':120,'clips':[
                {'id':'one','asset':'a','start':0,'duration':60,'source_in':0},
                {'id':'two','asset':'a','start':60,'duration':60,'source_in':2000}]}],
            'deliverables':[{'id':'wide','sequence':'main','width':160,'height':90}],'locks':[]}


class Contracts(unittest.TestCase):
    def test_split_preserves_source_fraction_and_animation_clock(self):
        p=project();c=p['sequences'][0]['clips'][0]
        c['speed_curve']=[{'frame':0,'speed':{'num':1,'den':2}},{'frame':60,'speed':{'num':2,'den':1}}]
        c['keyframes']={'x':[{'frame':0,'value':-.2,'easing':'smooth'},{'frame':60,'value':.2}]}
        result,_=apply_operations(p,[{'op':'split_clip','sequence':'main','id':'one','value':{'frame':23,'right_id':'right'}}])
        left,right=result['sequences'][0]['clips'][:2]
        source,_=span_seconds(p['assets']['a'],right,Fraction(30))
        self.assertEqual(source,source_offset(c,23,Fraction(30)))
        for n in range(right['duration']):
            self.assertEqual(parameters(c,n+23),parameters(right,n))
            self.assertEqual(source+source_offset(right,n,Fraction(30)),source_offset(c,n+23,Fraction(30)))
        self.assertEqual(c['duration'],60)

    def test_inverse_curve_projects_real_words(self):
        from fc_captions import project_captions
        p=project();seq=p['sequences'][0];c=seq['clips'][0]
        c['speed_curve']=[{'frame':0,'speed':{'num':1,'den':1}},{'frame':60,'speed':{'num':2,'den':1}}]
        p['analyses']={'a':{'timing':'manual','words':[{'id':'w','start':1,'end':1.2,'text':'word'}]}}
        seq['clips']=[c]
        words=project_captions(p,seq)['words']
        expected=round(30*(-2+math.sqrt(8)))
        self.assertEqual(words[0]['start'],expected)
        for n in (0,12,30,59,60):
            self.assertAlmostEqual(float(timeline_offset(c,source_offset(c,n,Fraction(30)),Fraction(30))),n,places=10)

    def test_ripple_trim_moves_all_lanes_and_keeps_anchor(self):
        p=project();s=p['sequences'][0]
        s['texts']=[{'id':'later','start':70,'duration':15,'text':'later'}, {'id':'inside','anchor':{'clip':'one','offset':20},'duration':5,'text':'inside'}]
        out,_=apply_operations(p,[{'op':'trim_clip','sequence':'main','id':'one','value':{'in':10,'out':50,'ripple':True}}])
        s=out['sequences'][0]
        self.assertEqual((s['duration'],s['clips'][1]['start'],s['texts'][0]['start']),(100,40,50))
        self.assertEqual(s['texts'][1]['anchor']['offset'],10)

    def test_conflicting_ripple_is_atomic(self):
        p=project();p['sequences'][0]['texts']=[{'id':'cross','start':50,'duration':20,'text':'cross'}]
        before=fingerprint(p)
        with self.assertRaises(FrameCutError):
            apply_operations(p,[{'op':'remove_clip','sequence':'main','id':'one','value':{'ripple':True}}])
        self.assertEqual(before,fingerprint(p))

    def test_move_locked_clip_and_unknown_ids_fail(self):
        for id_,locks in [('one',['one']),('missing',[])]:
            p=project();p['locks']=locks
            with self.assertRaises(FrameCutError):
                apply_operations(p,[{'op':'move_clip','sequence':'main','id':id_,'value':{'start':65}}])

    def test_remove_anchor_policy_and_caption_sources(self):
        p=project();s=p['sequences'][0];s['texts']=[{'id':'caption','anchor':{'clip':'one','offset':0},'duration':20,'text':'x'}]
        s['captions']={'sources':['one','two']}
        with self.assertRaises(FrameCutError):apply_operations(p,[{'op':'remove_clip','sequence':'main','id':'one','value':{}}])
        out,_=apply_operations(p,[{'op':'remove_clip','sequence':'main','id':'one','value':{'dependents':'remove','ripple':True}}])
        self.assertEqual(out['sequences'][0]['texts'],[])
        self.assertEqual(out['sequences'][0]['captions']['sources'],['two'])

    def test_freeze_inserts_hold_and_shifts_tail(self):
        p=project()
        p['deliverables'][0]['framing']={'one':{'keyframes':{'zoom':[{'frame':0,'value':1},{'frame':60,'value':2}]}}}
        out,_=apply_operations(p,[{'op':'freeze_frame','sequence':'main','id':'one','value':{'frame':30,'duration':15,'hold_id':'hold','right_id':'tail'}}])
        s=out['sequences'][0]
        self.assertEqual([c['start'] for c in s['clips']],[0,30,45,75])
        self.assertEqual(s['duration'],135)
        self.assertTrue(s['clips'][1]['freeze']);self.assertTrue(s['clips'][1]['mute'])
        self.assertEqual(source_offset(s['clips'][1],10,Fraction(30)),0)
        from fc_picture import effective_event
        held=effective_event(s['clips'][1],out['deliverables'][0])
        self.assertEqual(parameters(held,0)['zoom'],1.5)
        self.assertEqual(parameters(held,14)['zoom'],1.5)

    def test_curve_and_effect_validation(self):
        variants=[{'speed_curve':[{'frame':0,'speed':{'num':1,'den':1}},{'frame':60,'speed':{'num':0,'den':1}}]},
                  {'effects':[{'id':'missing','version':1}]}, {'keyframes':{'x':[{'frame':0,'value':9}]}},
                  {'keyframes':{'x':[{'frame':1,'value':0},{'frame':1,'value':.1}]}},
                  {'freeze':True,'speed_curve':[{'frame':0,'speed':{'num':1,'den':1}},{'frame':60,'speed':{'num':2,'den':1}}]}]
        for data in variants:
            p=project();p['sequences'][0]['clips'][0].update(data)
            with self.assertRaises(FrameCutError):validate(p)

    def test_framing_and_compact_timeline_are_scoped(self):
        p=project()
        out,_=apply_operations(p,[{'op':'set_framing','sequence':'main','value':{'deliverable':'wide','framing':{'one':{'crop':[.25,0,.5,1]}}}}])
        self.assertNotIn('framing',p['deliverables'][0])
        self.assertEqual(timeline_read(out)['sequences'][0]['lanes']['clips'][0]['id'],'one')
        out['deliverables'][0]['framing']['unknown']={}
        with self.assertRaises(FrameCutError):validate(out)

    def test_effects_change_pixels_and_preserve_alpha(self):
        from PIL import Image
        self.assertEqual(check_fixtures()['status'],'PASS')
        a=Image.new('RGBA',(8,8),(40,80,120,127))
        b=picture(a,[{'id':'brightness','version':1,'params':{'amount':2}}])
        self.assertEqual(b.getpixel((3,3)),(80,160,240,127))
        with self.assertRaises(FrameCutError):picture(a,[{'id':'brightness','version':9}])


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg unavailable')
class Media(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared=tempfile.TemporaryDirectory();cls.source=Path(cls.shared.name)/'source.mp4'
        ffmpeg(['-f','lavfi','-i','testsrc2=s=160x90:r=30:d=5','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=5',
                '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(cls.source)])

    @classmethod
    def tearDownClass(cls):cls.shared.cleanup()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        shutil.copy2(self.source,self.root/'source.mp4')
        self.p=project_init(self.root/'project.json','test')
        self.p['assets']['a']=ingest(self.root,'source.mp4','a')
        self.p['sequences']=[{'id':'main','fps':{'num':30,'den':1},'duration':45,'clips':[{'id':'clip','asset':'a','start':0,'duration':45,'source_in':0}]}]
        self.p['deliverables']=[{'id':'wide','sequence':'main','width':160,'height':90}]
        self.p['authorization']='Synthetic local regression render'

    def tearDown(self):self.tmp.cleanup()

    def test_decoder_preserves_count_and_selected_pixels_on_supported_ffmpeg(self):
        from fc_picture import decode_command
        from PIL import Image
        asset = self.p['assets']['a']
        for fps, extra in ((Fraction(30), {}), (Fraction(30000, 1001), {}), (Fraction(30), {'freeze': True}),
                           (Fraction(30), {'speed': {'num': 2, 'den': 1}})):
            with self.subTest(fps=str(fps), extra=extra):
                event = dict(self.p['sequences'][0]['clips'][0], duration=12, **extra)
                full = subprocess.run(decode_command(self.root, asset, event, fps), capture_output=True)
                self.assertEqual(full.returncode, 0, full.stderr.decode())
                size = 160 * 90 * 4
                self.assertEqual(len(full.stdout), 12 * size)
                selected = subprocess.run(decode_command(self.root, asset, event, fps, frame=7), capture_output=True)
                self.assertEqual(selected.returncode, 0, selected.stderr.decode())
                self.assertEqual(selected.stdout, full.stdout[7 * size:8 * size])
                if extra.get('freeze'):
                    self.assertEqual(full.stdout[:size], selected.stdout)
                else:
                    self.assertNotEqual(full.stdout[:size], selected.stdout)
                path = self.root / 'selected.png'
                if path.exists(): path.unlink()
                still = subprocess.run(decode_command(self.root, asset, event, fps, frame=7, output=path), capture_output=True)
                self.assertEqual(still.returncode, 0, still.stderr.decode())
                with Image.open(path) as image:
                    self.assertEqual(image.convert('RGBA').tobytes(), selected.stdout)

    def test_keyframes_variant_effect_preview_matches_decoded_video(self):
        from PIL import Image,ImageChops,ImageStat
        c=self.p['sequences'][0]['clips'][0]
        c['keyframes']={'rotation':[{'frame':0,'value':0},{'frame':44,'value':12}], 'opacity':[{'frame':0,'value':.6},{'frame':44,'value':1}]}
        c['effects']=[{'id':'brightness','version':1,'params':{'amount':1.1}}]
        self.p['deliverables'][0]['framing']={'clip':{'keyframes':{'zoom':[{'frame':0,'value':1},{'frame':44,'value':1.4}]}}}
        render(self.p,self.root,'wide','movie')
        preview_frame(self.p,self.root,'wide',20,'still.png')
        ffmpeg(['-i',str(self.root/'movie/video.mp4'),'-vf',"select='eq(n,20)'",'-frames:v','1',str(self.root/'decoded.png')])
        with Image.open(self.root/'still.png') as a,Image.open(self.root/'decoded.png') as b:
            # H.264 4:2:0 loses high-frequency chroma: compare luma and half-resolution colour separately.
            luma=ImageStat.Stat(ImageChops.difference(a.convert('L'),b.convert('L'))).mean[0]
            colour=sum(ImageStat.Stat(ImageChops.difference(a.convert('RGB').resize((80,45)),b.convert('RGB').resize((80,45)))).mean)/3
        self.assertLess(luma,5)
        self.assertLess(colour,6)

    def test_transition_alpha_overlay_and_keyed_text_match_still(self):
        from PIL import Image, ImageChops, ImageStat
        Image.new('RGBA',(40,30),(230,60,20,128)).save(self.root/'overlay.png')
        self.p['assets']['overlay']=ingest(self.root,'overlay.png','overlay')
        s=self.p['sequences'][0]
        s['clips']=[{'id':'clip','asset':'a','start':0,'duration':30,'source_in':0},
                    {'id':'next','asset':'a','start':15,'duration':30,'source_in':15360,'transition':15}]
        s['overlays']=[{'id':'badge','asset':'overlay','start':10,'duration':25,'rect':[.2,.2,.5,.5],'alpha':'straight'}]
        s['texts']=[{'id':'title','start':10,'duration':25,'text':'TEST','keyframes':{'x':[{'frame':0,'value':-.1},{'frame':24,'value':.1}]}}]
        render(self.p,self.root,'wide','composite')
        preview_frame(self.p,self.root,'wide',22,'still.png')
        ffmpeg(['-i',str(self.root/'composite/video.mp4'),'-vf',"select='eq(n,22)'",'-frames:v','1',str(self.root/'decoded.png')])
        with Image.open(self.root/'still.png') as a,Image.open(self.root/'decoded.png') as b:
            luma=ImageStat.Stat(ImageChops.difference(a.convert('L'),b.convert('L'))).mean[0]
            colour=sum(ImageStat.Stat(ImageChops.difference(a.convert('RGB').resize((80,45)),b.convert('RGB').resize((80,45)))).mean)/3
        self.assertLess(luma,5)
        self.assertLess(colour,6)

    def test_speed_ramp_renders_audio_and_maps_captions(self):
        c=self.p['sequences'][0]['clips'][0]
        c['speed_curve']=[{'frame':0,'speed':{'num':1,'den':2}},{'frame':45,'speed':{'num':2,'den':1}}]
        self.p['analyses']['a']={'source_hash':self.p['assets']['a']['sha256'],'timing':'manual','words':[{'id':'w','start':.2,'end':.4,'text':'test'}]}
        self.p['sequences'][0]['captions']={'enabled':True,'mode':'kinetic'}
        result=render(self.p,self.root,'wide','ramp',mode='final')
        receipt=read_json(self.root/'ramp/receipt.json')
        self.assertEqual(receipt['technical']['decoded_frames'],45)
        self.assertIn('varispeed',result['cache_built'])
        self.assertNotEqual(receipt['technical']['loudness']['input_i'],'-inf')
        self.assertIsNotNone(read_json(self.root/'ramp/source-map.json')[0]['speed_curve'])

    def test_freeze_decoded_frames_are_held(self):
        from PIL import Image,ImageChops,ImageStat
        self.p,_=apply_operations(self.p,[{'op':'freeze_frame','sequence':'main','id':'clip','value':{'frame':15,'duration':12,'hold_id':'hold','right_id':'tail'}}])
        render(self.p,self.root,'wide','frozen')
        for n in (16,25):ffmpeg(['-i',str(self.root/'frozen/video.mp4'),'-vf',f"select='eq(n,{n})'",'-frames:v','1',str(self.root/f'{n}.png')])
        with Image.open(self.root/'16.png') as a,Image.open(self.root/'25.png') as b:
            self.assertLess(sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3,1)

    def test_storyboard_covers_end_all_events_and_authored_moments(self):
        self.p['sequences'][0]['texts']=[{'id':'title','start':6,'duration':12,'text':'Exact copy','animation':'none'}]
        result=storyboard(self.p,self.root,'wide','board',[{'id':'beat','frame':11,'action':'Authored moment'}])
        receipt=read_json(self.root/'board/receipt.json')
        self.assertEqual(receipt['status'],'awaiting_user_review')
        self.assertFalse(receipt['full_video_rendered'])
        self.assertIn('title',receipt['coverage'])
        self.assertEqual(receipt['panels'][-1]['frame'],44)
        self.assertTrue(any(p['id']=='beat' for p in receipt['panels']))
        self.assertTrue(any(x.endswith('.pdf') for x in result['sheets']))
        self.assertEqual(list((self.root/'board').rglob('*.mp4')),[])

    def test_job_cancel_resume_and_completed_state_survive_processes(self):
        from fc_jobs import start,cancel,status,resume
        self.p=commit_revision(self.root/'project.json',self.p,1,'fixture')
        job=start(self.root/'project.json',{'kind':'render','deliverable':'wide','out':'job-output','mode':'preview'})
        cancel(self.root,'test',job['id'])
        deadline=time.monotonic()+20
        while time.monotonic()<deadline:
            state=status(self.root,'test',job['id'])
            if state['status'] not in ('queued','running'):break
            time.sleep(.1)
        self.assertEqual(state['status'],'cancelled',state)
        self.assertFalse((self.root/'job-output').exists())
        resumed=resume(self.root/'project.json',job['id'])
        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            state=status(self.root,'test',resumed['id'])
            if state['status'] not in ('queued','running'):break
            time.sleep(.1)
        self.assertEqual(state['status'],'completed',state)
        self.assertEqual(state['resumes'],job['id'])
        self.assertTrue((self.root/'job-output/receipt.json').exists())

    def test_split_ramp_preserves_decoded_picture(self):
        from PIL import Image, ImageChops, ImageStat
        c=self.p['sequences'][0]['clips'][0]
        c['speed_curve']=[{'frame':0,'speed':{'num':1,'den':2}},{'frame':45,'speed':{'num':2,'den':1}}]
        c['mute']=True
        original=copy.deepcopy(self.p)
        split_project,_=apply_operations(self.p,[{'op':'split_clip','sequence':'main','id':'clip','value':{'frame':23,'right_id':'tail'}}])
        preview_frame(original,self.root,'wide',23,'before.png')
        preview_frame(split_project,self.root,'wide',23,'after.png')
        with Image.open(self.root/'before.png') as a,Image.open(self.root/'after.png') as b:
            self.assertLess(sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3,1)

    def test_audio_effects_and_gain_envelope_reach_actual_mix(self):
        self.p['sequences'][0]['clips'][0]['mute']=True
        self.p['sequences'][0]['audio']=[{'id':'voice','asset':'a','start':0,'duration':45,
            'effects':[{'id':'highpass','version':1,'params':{'amount':100}}],
            'keyframes':{'gain_db':[{'frame':0,'value':-60},{'frame':44,'value':0}]}}]
        render(self.p,self.root,'wide','gain')
        import array
        ffmpeg(['-i',str(self.root/'gain/video.mp4'),'-vn','-ac','1','-ar','48000','-f','s16le',str(self.root/'audio.pcm')])
        samples=array.array('h',(self.root/'audio.pcm').read_bytes())
        rms=lambda values:math.sqrt(sum(v*v for v in values)/len(values))
        self.assertGreater(rms(samples[-10000:]),rms(samples[:10000])*10)

    def test_interrupted_job_recovery_is_guarded_by_snapshot(self):
        from fc_jobs import start,status,resume,folder
        self.p=commit_revision(self.root/'project.json',self.p,1,'fixture')
        job='job-dead';directory=folder(self.root,'test',job);directory.mkdir(parents=True)
        state={'id':job,'status':'running','pid':2147483647,'process_token':'absent','host':__import__('socket').gethostname(),
               'project_hash':fingerprint(self.p),'request':{'kind':'render','deliverable':'wide','out':'resumed'}}
        atomic_json(directory/'state.json',state)
        self.assertEqual(status(self.root,'test',job)['status'],'interrupted')
        changed=copy.deepcopy(self.p);changed['brief']={'changed':True}
        commit_revision(self.root/'project.json',changed,2,'change')
        with self.assertRaises(FrameCutError):resume(self.root/'project.json',job)

    def test_dry_run_does_not_create_revision(self):
        self.p=commit_revision(self.root/'project.json',self.p,1,'fixture')
        atomic_json(self.root/'ops.json',[{'op':'split_clip','sequence':'main','id':'clip','value':{'frame':15,'right_id':'tail'}}])
        before=(self.root/'project.json').read_bytes()
        result=subprocess.run([sys.executable,str(RUNTIME/'framecut.py'),'apply',str(self.root/'project.json'),'--base-revision','2','--reason','fixture','--ops',str(self.root/'ops.json'),'--dry-run'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'],'dry_run')
        self.assertEqual((self.root/'project.json').read_bytes(),before)

if __name__=='__main__':unittest.main(verbosity=2)
