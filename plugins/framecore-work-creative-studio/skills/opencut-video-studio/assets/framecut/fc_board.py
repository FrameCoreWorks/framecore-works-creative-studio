"""Composition stills and complete structural storyboard coverage before video export."""
import os
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from fc_core import atomic_json, confined, event_start, file_hash, fingerprint, identifier, integer, keys, ratio, require, validate
from fc_jobs import checkpoint
from fc_picture import clip_frame, pillow


def composed_frame(project, root, plan, frame, timeout=600):
    from fc_media import ffmpeg
    Image = pillow()
    seq,d = plan['sequence'],plan['deliverable']
    fps = ratio(seq['fps'])
    integer(frame,'frame',0,seq['duration']-1)
    canvas = Image.new('RGBA',(d['width'],d['height']),seq.get('background','#000000'))
    active = [c for c in seq['clips'] if c['start'] <= frame < c['start']+c['duration']]
    for i,event in enumerate(active):
        picture = clip_frame(root,project['assets'][event['asset']],event,d,fps,frame-event['start'],timeout)
        overlap = event.get('transition',0)
        if overlap and frame < event['start']+overlap and i:
            canvas = Image.blend(canvas,picture,(frame-event['start'])/overlap)
        else:
            canvas = picture
    for event in seq.get('overlays',[]):
        start = event_start(event,seq)
        if not start <= frame < start+event['duration']:
            continue
        layer_d = dict(d)
        layer_d['width'] = max(2,round(d['width']*event['rect'][2]/2)*2)
        layer_d['height'] = max(2,round(d['height']*event['rect'][3]/2)*2)
        picture = clip_frame(root,project['assets'][event['asset']],event,layer_d,fps,frame-start,timeout,event.get('alpha')=='straight')
        canvas.alpha_composite(picture,(round(d['width']*event['rect'][0]),round(d['height']*event['rect'][1])))
    with tempfile.TemporaryDirectory(prefix='.framecut-type-',dir=root) as tmp:
        directory = Path(tmp)
        canvas.convert('RGB').save(directory/'picture.png')
        (directory/'captions.ass').write_text(plan['ass'],encoding='utf-8')
        # ASS sees the original timeline time, including entry/exit and keyed text.
        stamp = f'{float(Fraction(frame)/fps):.12f}'
        ffmpeg(['-i','picture.png','-vf',f'settb=AVTB,setpts={stamp}/TB,ass=filename=captions.ass,format=rgb24',
                '-frames:v','1','-threads','1','composite.png'],timeout,directory)
        with Image.open(directory/'composite.png') as output:
            return output.copy()


def preview_frame(project, root, deliverable_id, frame, out_relative, timeout=600):
    from fc_render import compile_project
    plan = compile_project(project,root,deliverable_id)
    output = confined(root,out_relative)
    require(output.suffix.lower()=='.png' and not output.exists(),'Use a new PNG output path')
    output.parent.mkdir(parents=True,exist_ok=True)
    image = composed_frame(project,root,plan,frame,timeout)
    with tempfile.TemporaryDirectory(prefix='.framecut-preview-',dir=output.parent) as tmp:
        candidate = Path(tmp)/'frame.png'
        image.save(candidate)
        checkpoint('publishing-preview')
        validate(project, root, True)
        os.link(candidate,output)
    return {'status':'preview_frame','path':out_relative,'frame':frame,'deliverable':deliverable_id,
            'project_revision':project['revision'],'project_hash':fingerprint(project),'sha256':file_hash(output),
            'warnings':plan['warnings'],'review':'Composition still; motion and audio are not reviewed by a still.'}


def panel_plan(plan, extra=None):
    seq = plan['sequence']
    points = {0:{'opening'},seq['duration']-1:{'ending'}}
    coverage = {}
    def add(n,label):
        if 0 <= n < seq['duration']:
            points.setdefault(n,set()).add(label)
    for lane in ('clips','overlays','texts','audio'):
        for event in seq.get(lane,[]):
            start,end = event_start(event,seq),event_start(event,seq)+event['duration']
            frames = [start,(start+end-1)//2,end-1]
            coverage[event['id']] = {'lane':lane,'interval':[start,end],'frames':frames}
            for n in frames: add(n,lane+':'+event['id'])
            for n in (start-1,end): add(n,'boundary:'+event['id'])
            for track in event.get('keyframes',{}).values():
                for key in track:
                    local = key['frame']-event.get('keyframe_offset',0)
                    if 0 <= local < event['duration']: add(start+local,'keyframe:'+event['id'])
            for key in event.get('speed_curve',[]): add(start+key['frame'],'speed:'+event['id'])
            for track in plan['deliverable'].get('framing',{}).get(event['id'],{}).get('keyframes',{}).values():
                for key in track:
                    local = key['frame']-event.get('keyframe_offset',0)
                    if 0 <= local < event['duration']: add(start+local,'framing:'+event['id'])
            if event.get('transition'):
                add(start+event['transition']//2,'transition:'+event['id'])
                add(start+event['transition']-1,'transition:'+event['id'])
    for group in plan['captions']['groups']:
        add(group[0]['start'],'caption'); add(group[-1]['end']-1,'caption')
    require(extra is None or isinstance(extra,list),'Panels must be a list')
    notes = {}
    for panel in extra or []:
        keys(panel,('frame','id','action','camera','audio','super'),('frame','id'))
        frame = integer(panel['frame'],'panel frame',0,seq['duration']-1)
        identifier(panel['id'])
        require(frame not in notes,'Duplicate authored panel frame')
        notes[frame] = panel
        add(frame,'authored:'+panel['id'])
    require(len(points)<=512,'Board exceeds 512 structural moments; split into explicit sequences, never silently drop panels','resource_limit')
    panels = []
    for frame,reasons in sorted(points.items()):
        text = [e['text'] for e in seq.get('texts',[]) if event_start(e,seq)<=frame<event_start(e,seq)+e['duration']]
        text += [' '.join(w['text'] for w in g) for g in plan['captions']['groups'] if g[0]['start']<=frame<g[-1]['end']]
        panels.append({'id':f'p-{frame:08d}','frame':frame,'reasons':sorted(reasons),'super':' | '.join(text),**notes.get(frame,{})})
    require(len({p['id'] for p in panels})==len(panels),'Duplicate panel ID')
    return panels,coverage


def storyboard(project, root, deliverable_id, out_relative, panels=None, timeout=600):
    from fc_render import compile_project
    from fc_media import run
    plan = compile_project(project,root,deliverable_id)
    entries,coverage = panel_plan(plan,panels)
    output = confined(root,out_relative)
    require(not output.exists(),'Storyboard output exists; choose a new board revision')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.framecut-board-',dir=output.parent) as tmp:
        directory=Path(tmp); (directory/'frames').mkdir()
        for i,panel in enumerate(entries):
            checkpoint('storyboard',frame=i,total=len(entries),force=True,unit='panels')
            image = composed_frame(project,root,plan,panel['frame'],timeout)
            panel['image']=f'frames/{panel["id"]}.png'
            image.save(directory/panel['image'])
            panel['sha256']=file_hash(directory/panel['image'])
            panel['time']=f'{float(Fraction(panel["frame"])/ratio(plan["sequence"]["fps"])):.3f}s'
        d=plan['deliverable']
        # Board layout is an existing Studio owner, reused here without duplicated typography.
        ratios={'16:9':16/9,'9:16':9/16,'1:1':1,'4:5':4/5,'2.39:1':2.39,'4:3':4/3}
        aspect=min(ratios,key=lambda k:abs(ratios[k]-d['width']/d['height']))
        board={'title':project['id']+' storyboard','subtitle':f'Revision {project["revision"]} | {deliverable_id} | for review',
               'frame':aspect,'columns':4 if d['width']>=d['height'] else 6,'page':'A4-landscape','fit':'cover' if abs(ratios[aspect]-d['width']/d['height'])<1e-6 else 'contain',
               'panels':entries,'notes':'All structural moments are represented. Review action, continuity and declared creative beats; stills do not establish motion/audio approval.'}
        atomic_json(directory/'board.json',board)
        script=Path(__file__).resolve().parents[3]/'storyboard-board-architect/scripts/board_compose.py'
        run([sys.executable,str(script),str(directory/'board.json'),'--out-dir',str(directory/'sheets')],timeout)
        receipt={'schema_version':1,'project_id':project['id'],'project_revision':project['revision'],'project_hash':fingerprint(project),
                 'deliverable':deliverable_id,'sequence':plan['sequence']['id'],'coverage':coverage,'panels':entries,
                 'status':'awaiting_user_review','warnings':plan['warnings'],'full_video_rendered':False,
                 'files':{p.relative_to(directory).as_posix():file_hash(p) for p in directory.rglob('*') if p.is_file()}}
        atomic_json(directory/'receipt.json',receipt)
        checkpoint('publishing-storyboard')
        validate(project, root, True)
        require(not output.exists(),'Storyboard output created concurrently')
        os.rename(directory,output)
    return {'status':'storyboard_ready','output':out_relative,'panels':len(entries),'receipt':out_relative+'/receipt.json',
            'sheets':[str(p.relative_to(root)) for p in sorted((output/'sheets').glob('*'))],
            'acceptance':'awaiting_user_review','project_hash':fingerprint(project)}
