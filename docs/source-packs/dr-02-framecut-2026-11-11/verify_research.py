"""Verify research artifacts and original synthetic arithmetic only.
Does not execute inspected third-party code or media/NLE tests.
No claim to implement the full JSON Schema standard.
"""
from pathlib import Path
from fractions import Fraction
import json,re,sys,hashlib
P=Path(__file__).resolve().parent
errors=[];checks=[]
def check(ok,msg):
 (checks if ok else errors).append(msg)

check(hashlib.sha256((P/'PROMPT.md').read_bytes()).hexdigest()=='8b00ad1f655ffefbf27a626d3f00d762042b06fe546c5d60c79400a25a1f2a7d','original prompt unchanged')
required=['PROMPT.md','SCOPE-CLARIFICATION.md','PLAN.md','README.md','COMPREHENSIVE-REPORT.md','CODE-AND-CONTRACTS.md','IMPLEMENTATION_HANDOFF.md','COVERAGE-MATRIX.md','REVIEW.md','VERIFICATION.md','SOURCE-LEDGER.json','SOURCE-LEDGER.csv','LINK-CHECK.json','editorial-intent.schema.json','specialists/craft/CRAFT.md','specialists/craft/GLOSSARY.md','specialists/craft/RECIPES.md','specialists/nle/NLE-WORKFLOWS.md','specialists/nle/QA-BENCHMARKS.md','specialists/repo/CURRENT-STUDIO.md','specialists/repo/CONTRACT-FINDINGS.md','specialists/repo/REPOSITORIES.md']
for f in required:check((P/f).is_file(),f+' exists')
if errors:
 print(json.dumps({'status':'FAIL','errors':errors},ensure_ascii=False,indent=2));sys.exit(1)
ledger=json.loads((P/'SOURCE-LEDGER.json').read_text())
if isinstance(ledger,dict):ledger=ledger['sources']
ids=[s['id'] for s in ledger]
check(len(ids)==len(set(ids)),'source IDs unique')
for s in ledger:
 for field in ['id','title','url','author','accessed','locator','inspection','evidence_class','claims','decision','counterexample','test','rights','limitations']:
  check(field in s,f"{s['id']} field {field}")
 check(s.get('accessed')=='2026-11-11',f"{s['id']} access date")
 check(bool(s.get('claims')),f"{s['id']} has claims")
files=[p for p in P.rglob('*.md') if 'backups' not in p.parts and 'evidence' not in p.parts and p.name!='PROMPT.md']
text='\n'.join(p.read_text() for p in files)
used=set(re.findall(r'\[((?:C|N|R|F)\d{2,3})\]',text))
check(not(used-set(ids)),'no undefined source citations: '+str(sorted(used-set(ids))))
check(not(set(ids)-used),'all ledger sources cited in authored documents: '+str(sorted(set(ids)-used)))
g=(P/'specialists/craft/GLOSSARY.md').read_text();terms=set(re.findall(r'\bG\d{3}\b',g))
check(95<=len(terms)<=110,'glossary approximately100: '+str(len(terms)))
r=(P/'specialists/craft/RECIPES.md').read_text();recipe_ids=set(re.findall(r'(?m)^##\s+(?:R|RC)?(?:0?)(\d{1,2})[. —–:]',r))
# Author can use a different unambiguous heading prefix; require 15–20 actual recipe-level headings.
if not recipe_ids:recipe_ids=set(re.findall(r'(?m)^##\s+((?:R|RC)\d{2})',r))
check(15<=len(recipe_ids)<=20,'15–20 recipe headings: '+str(len(recipe_ids)))
# Restricted structural validator for this deliberately bounded RFC schema.
def valid(x,s):
 if 'oneOf' in s:return sum(valid(x,a) for a in s['oneOf'])==1
 if 'const' in s and x!=s['const']:return False
 if 'enum' in s and x not in s['enum']:return False
 t=s.get('type')
 good={'object':lambda:isinstance(x,dict),'array':lambda:isinstance(x,list),'integer':lambda:type(x)is int,'number':lambda:type(x)in(int,float),'string':lambda:isinstance(x,str),'boolean':lambda:type(x)is bool}
 if t and not good[t]():return False
 if t=='object':
  if any(k not in x for k in s.get('required',[])):return False
  props=s.get('properties',{})
  if s.get('additionalProperties') is False and set(x)-set(props):return False
  return all(valid(v,props[k]) for k,v in x.items() if k in props)
 if t=='array':
  if len(x)<s.get('minItems',0):return False
  if s.get('uniqueItems') and len({json.dumps(v,sort_keys=True) for v in x})!=len(x):return False
  return all(valid(v,s.get('items',{})) for v in x)
 if t=='string' and len(x)<s.get('minLength',0):return False
 if t in ('integer','number'):
  if 'minimum' in s and x<s['minimum']:return False
  if 'maximum' in s and x>s['maximum']:return False
 return True
schema=json.loads((P/'editorial-intent.schema.json').read_text());intents=json.loads((P/'examples/editorial-intents.json').read_text())
kinds={'trim','split','insert','overwrite','ripple','roll','slip','slide','speed_curve','freeze','transform_keyframes','transition','gain_ducking','subtitles'}
check({x['operation']['kind'] for x in intents}==kinds,'14 required intent families')
for x in intents:check(valid(x,schema),'restricted schema check '+x['operation']['kind'])
bad=dict(intents[0]);bad.pop('revision');check(not valid(bad,schema),'negative: missing revision rejected')
bad={**intents[0],'unexpected':1};check(not valid(bad,schema),'negative: unknown top-level field rejected')
bad={**intents[0],'fps_den':0};check(not valid(bad,schema),'negative: zero rate denominator rejected')
native=json.loads((P/'examples/native-operations.json').read_text())
check(native['status']=='NOT_RUN' and all(c['status']=='NOT_RUN' for c in native['cases']),'native examples remain NOT_RUN')
allowed={'split_clip','trim_clip','move_clip','remove_clip','freeze_frame','set_keyframes','set_speed_curve','set_effects','set_framing','set_sequence','replace_clip','set_captions','set_audio','set_overlays','set_texts','add_sequence','set_deliverables','set_brief','set_authorization','set_locks'}
for c in native['cases']:
 for op in c['operations']:
  check(op['op'] in allowed and not(set(op)-{'op','sequence','id','value'}),'native envelope '+c['id'])
# Own exact arithmetic, NOT validation through the third-party runtime.
check(Fraction(1800*1001,30000)==Fraction(6006,100),'1800 frames at30000/1001 =60.06s')
check(Fraction(48000*1001,30000)==Fraction(8008,5),'1601.6 samples/frame')
check(1602*100000-160160000==40000,'per-frame rounding drift40000 samples')
check(Fraction(40000,48000)==Fraction(5,6),'drift5/6s')
check(Fraction(100,25)*(Fraction(1,2)+Fraction(3,2))/2==4,'ramp trapezoid source consumption4s')
check(120+12+12==144 and 132-12==120,'motion body+handles')
check(90000+Fraction(10,25)*90000==126000,'10-frame slip maps source PTS126000')
check(450000+Fraction(10,25)*90000==486000,'roll B source PTS486000')
check(sum([50,25,50,100])==225,'insert extends200→225')
check(sum([50,25,25,100])==200,'overwrite retains200')
check(sum([80,100])==180 and sum([110,90])==200,'ripple/roll durations')
check(sum([110,100,90])==300,'slide preserves total')
check(Fraction(180000*1001,30000)==6006,'B5 duration6006s')
check(Fraction(180090*1001,30000)*48000==288432144,'B5 after ripple sample count288432144')
check(Fraction(90*1001,30000)*48000==144144,'B5 insert delta144144 samples')
check(Fraction(126000-90000,90000)*25==10 and Fraction(162000-90000,90000)*25==20,'subtitle before10..20')
check(Fraction(126000-126000,90000)*25==0 and Fraction(162000-126000,90000)*25==10,'subtitle after0..10')
for path in files:
 for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',path.read_text()):
  link=link.split('#')[0]
  if not link or re.match(r'\w+://',link) or link.startswith('mailto:'):continue
  # File links only; ignore prose code examples with templated paths.
  if '<' in link or '`' in link:continue
  check((path.parent/link).exists(),f'local link {path.relative_to(P)} -> {link}')
check('NOT_RUN' in (P/'specialists/nle/QA-BENCHMARKS.md').read_text(),'media benchmarks marked NOT_RUN')
check('NATIVE_TESTS: NOT_RUN' in (P/'VERIFICATION.md').read_text(),'verification preserves native boundary')
check(bool(re.search(r'REVIEW_STATUS: PASS(?:_WITH_LIMITATIONS)?\b',(P/'REVIEW.md').read_text())),'independent review passed within declared research scope')
for p in P.rglob('*'):
 if p.is_file():check(p.stat().st_size<16*1024*1024,'artifact below Hipson16MiB '+str(p.relative_to(P)))
print(json.dumps({'status':'PASS' if not errors else 'FAIL','scope':'research structure/references/restricted RFC checks/original arithmetic only; no native/NLE/media execution','passed_checks':len(checks),'source_records':len(ids),'cited_source_ids':len(used),'glossary_terms':len(terms),'recipe_count':len(recipe_ids),'intent_examples':len(intents),'native_examples':len(native['cases']),'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
