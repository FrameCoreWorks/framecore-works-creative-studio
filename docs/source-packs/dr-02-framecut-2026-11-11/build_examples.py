"""Own synthetic research fixtures. Does not import or execute downloaded FrameCut code."""
from pathlib import Path
import json
p=Path(__file__).parent

def write(name,obj):
 path=p/name
 if path.exists():
  from datetime import datetime
  import shutil
  backup=p/'backups'/datetime.now().strftime('%Y%m%dT%H%M%S%f')/name
  backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,backup)
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def op(kind,value,id='A'):
 d={'op':kind,'sequence':'main','value':value}
 if id is not None:d['id']=id
 return d
base_note='Independent case, not sequential. Hypothetical source probe: time_base=1/90000,start_pts=0,>=30 s; sequence main 25/1 fps. A start0,duration100,source_in90000; B start100,duration100,source_in450000. Native execution NOT_RUN.'
baseA={'id':'A','asset':'cameraA','start':0,'duration':100,'source_in':90000}
baseB={'id':'B','asset':'cameraB','start':100,'duration':100,'source_in':450000}
cases=[
 ('split',[op('split_clip',{'frame':50,'right_id':'A_right'})],'A_left0..50,A_right50..100; total fixed'),
 ('trim',[op('trim_clip',{'in':10,'out':90,'ripple':False})],'A10..90,source starts126000 ticks; B100..200'),
 ('ripple',[op('trim_clip',{'in':10,'out':90,'ripple':True})],'A0..80,B80..180; native shift changes sequence.duration200->180'),
 ('freeze',[op('freeze_frame',{'frame':50,'duration':25,'hold_id':'A_hold','right_id':'A_tail'})],'hold50..75,source at3 s; no speech during hold; downstream+25'),
 ('speed_curve',[op('set_speed_curve',[{'frame':0,'speed':{'num':1,'den':2}},{'frame':100,'speed':{'num':3,'den':2}}])],'100 timeline frames consume100 source-frame-equivalent; pitch follows native ramp'),
 ('transform_keyframes',[op('set_keyframes',{'scale':[{'frame':0,'value':1,'easing':'linear'},{'frame':99,'value':1.2,'easing':'hold'}],'x':[{'frame':0,'value':0,'easing':'smooth'},{'frame':99,'value':0.1,'easing':'hold'}]})],'fixed duration; scale1->1.2, x offset0->0.1 output width'),
 ('transition',[op('replace_clip',{**baseB,'start':90,'transition':10,'transition_style':'dissolve'},id='B')],'B90..190; trailing gap190..200 remains unless sequence explicitly shortened'),
 ('gain_ducking',[op('set_audio',[{'id':'music','asset':'music','start':0,'duration':200,'source_in':0,'gain_db':-12,'bus':'music','duck_db':-6}],None)],'replace full audio list; example requires music asset. Schedule ducking, not sidechain detector'),
 ('subtitles',[op('set_captions',{'enabled':True,'mode':'sentence','sources':['A','B'],'size':0.06,'bottom':0.12,'max_words':8},None)],'source timed transcript required; quality settings are proposed, not universal limits'),
 ('slip_candidate',[op('replace_clip',{**baseA,'source_in':126000})],'same placement/duration; manually composed candidate, no native slip op'),
 ('roll_candidate',[op('replace_clip',{**baseA,'duration':110}),op('replace_clip',{**baseB,'start':110,'duration':90,'source_in':486000},id='B')],'A0..110,B110..200; atomic final validation, handles and dependents checked')]
write('examples/native-operations.json',{'status':'NOT_RUN','notes':base_note,'base_sequence_fragment':{'id':'main','fps':{'num':25,'den':1},'duration':200,'clips':[baseA,baseB]},'cases':[{'id':n,'status':'NOT_RUN','operations':ops,'expected':ex} for n,ops,ex in cases]})
# External RFC envelope; never feed this document to framecut apply.
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:framecut-research:editorial-intent:0.1','title':'Proposed external editorial intent sidecar; NOT native FrameCut schema','type':'object','additionalProperties':False,'required':['schema_version','project_id','revision','request_id','timeline_owner','sequence','fps_num','fps_den','time_units','interval_convention','accepted_locks','provenance','operation'], 'properties':{}}
props=schema['properties']
for k in ['project_id','request_id','sequence']:props[k]={'type':'string','minLength':1}
props.update({'schema_version':{'const':'framecut-editorial-intent/0.1'},'revision':{'type':'integer','minimum':1},'timeline_owner':{'const':'FrameCut'},'fps_num':{'type':'integer','minimum':1},'fps_den':{'type':'integer','minimum':1},'time_units':{'const':'timeline_frames; source_pts_ticks; audio_samples'},'interval_convention':{'const':'[in,out)'},'accepted_locks':{'type':'array','items':{'type':'string'},'uniqueItems':True},'provenance':{'type':'object','required':['decision_id','evidence','classification'],'properties':{'decision_id':{'type':'string'},'evidence':{'type':'array','items':{'type':'string'}},'classification':{'enum':['SOURCED','DERIVED','PRACTITIONER','Unknown']}}},'operation':{'oneOf':[]}})
def obj(props,req=None):return {'type':'object','additionalProperties':False,'required':req or list(props),'properties':props}
integer={'type':'integer'};nonneg={'type':'integer','minimum':0};positive={'type':'integer','minimum':1};st={'type':'string'}
fields={
 'trim':{'clip':st,'in':nonneg,'out':positive,'ripple':{'type':'boolean'}},
 'split':{'clip':st,'frame':positive,'right_id':st},
 'insert':{'at':nonneg,'duration':positive,'asset_id':st,'source_in':integer,'affected_lanes':{'type':'array','items':st}},
 'overwrite':{'at':nonneg,'duration':positive,'asset_id':st,'source_in':integer,'affected_lanes':{'type':'array','items':st}},
 'ripple':{'clip':st,'in':nonneg,'out':positive,'affected_lanes':{'type':'array','items':st}},
 'roll':{'left':st,'right':st,'delta':integer},
 'slip':{'clip':st,'delta_source_frames':integer,'source_fps_num':positive,'source_fps_den':positive},
 'slide':{'left':st,'clip':st,'right':st,'delta':integer},
 'speed_curve':{'clip':st,'points':{'type':'array','minItems':2,'items':obj({'frame':nonneg,'speed_num':positive,'speed_den':positive})}},
 'freeze':{'clip':st,'frame':positive,'duration':positive,'hold_id':st,'right_id':st},
 'transform_keyframes':{'clip':st,'parameter':{'enum':['x','y','scale','rotation','opacity','zoom','pan_x','pan_y']},'points':{'type':'array','minItems':1,'items':obj({'frame':nonneg,'value':{'type':'number'},'easing':{'enum':['linear','smooth','hold']}})}},
 'transition':{'left':st,'right':st,'overlap':positive,'style':{'enum':['dissolve','dip_black','dip_white','wipe_left','slide_left']}},
 'gain_ducking':{'event_id':st,'gain_db':{'type':'number'},'duck_db':{'type':'number','maximum':0},'model':{'enum':['native_schedule','proposed_sidechain']}},
 'subtitles':{'source_events':{'type':'array','items':st},'timing':{'enum':['manual','aligned','asr_word','segment','unknown']},'language':st,'style_owner':{'const':'Caption Studio'}}}
for kind,fs in fields.items():props['operation']['oneOf'].append(obj({'kind':{'const':kind},'params':obj(fs)}))
write('editorial-intent.schema.json',schema)
params=[('trim',{'clip':'A','in':10,'out':90,'ripple':False}),('split',{'clip':'A','frame':50,'right_id':'A_right'}),('insert',{'at':50,'duration':25,'asset_id':'X','source_in':0,'affected_lanes':['clips','audio','overlays','texts']}),('overwrite',{'at':50,'duration':25,'asset_id':'X','source_in':0,'affected_lanes':['clips']}),('ripple',{'clip':'A','in':10,'out':90,'affected_lanes':['clips','audio','overlays','texts']}),('roll',{'left':'A','right':'B','delta':10}),('slip',{'clip':'A','delta_source_frames':10,'source_fps_num':25,'source_fps_den':1}),('slide',{'left':'A','clip':'B','right':'C','delta':10}),('speed_curve',{'clip':'A','points':[{'frame':0,'speed_num':1,'speed_den':2},{'frame':100,'speed_num':3,'speed_den':2}]}),('freeze',{'clip':'A','frame':50,'duration':25,'hold_id':'A_hold','right_id':'A_tail'}),('transform_keyframes',{'clip':'A','parameter':'scale','points':[{'frame':0,'value':1,'easing':'linear'},{'frame':99,'value':1.2,'easing':'hold'}]}),('transition',{'left':'A','right':'B','overlap':10,'style':'dissolve'}),('gain_ducking',{'event_id':'music','gain_db':-12,'duck_db':-6,'model':'native_schedule'}),('subtitles',{'source_events':['A','B'],'timing':'aligned','language':'pl','style_owner':'Caption Studio'})]
ints=[]
for i,(kind,values) in enumerate(params,1):
 ints.append({'schema_version':'framecut-editorial-intent/0.1','project_id':'synthetic_demo','revision':7,'request_id':f'request-{i:02}','timeline_owner':'FrameCut','sequence':'main','fps_num':25,'fps_den':1,'time_units':'timeline_frames; source_pts_ticks; audio_samples','interval_convention':'[in,out)','accepted_locks':[],'provenance':{'decision_id':f'decision-{i:02}','evidence':['synthetic-original-fixture'],'classification':'DERIVED'},'operation':{'kind':kind,'params':values}})
write('examples/editorial-intents.json',ints)
write('examples/motion-handoff-rfc.json',{'status':'PROPOSED_NOT_RUN','schema_version':'framecut-motion-envelope/0.1','project_id':'synthetic_demo','revision':7,'timeline_owner':'FrameCut','sequence_id':'main','event_id':'motion_product','asset_id':'motion_product_r1','hash':None,'hash_status':'UNBOUND_UNTIL_REAL_RENDER','fps_num':25,'fps_den':1,'time_units':{'timeline':'frames','source':'PTS ticks with time_base','audio':'samples'},'interval_convention':'[in,out)','timeline_time':{'in':1000,'out':1120},'source_time':{'in':12,'out':132,'unit':'render_frames','local_origin':0},'handles':{'head':12,'tail':12},'render_frames':144,'retiming':{'num':1,'den':1},'resolution':{'width':1920,'height':1080},'color_space':{'primaries':'bt709','transfer':'bt709','matrix':'bt709','range':'limited','management':'proposed SDR contract; verify actual render'},'alpha_mode':'straight','audio_sample_rate':48000,'fonts':[{'family':'client-approved','file_hash':None,'license':'UNBOUND'}],'seed':None,'provenance':{'decision_id':'motion-brief-1','source':'same Studio brief; no copy','render_engine':'Unknown'},'accepted_locks':[],'returns':['render','optional_editable_project','manifest','QA'],'incompatibility':'Current attach-motion requires its own generated request; this RFC handles-envelope is not accepted directly.'})
print('Wrote schema and 4 example files; no production execution')
