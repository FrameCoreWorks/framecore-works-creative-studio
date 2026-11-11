"""Original analytic fixtures only; no AE/Blender or production renderer exercised."""
import json, math
from pathlib import Path
p = Path(__file__).resolve().parent
c, s = math.cos(math.pi/6), math.sin(math.pi/6)
def rs(v):
    x,y=v[0]*1.5,v[1]*.75
    return (c*x-s*y,s*x+c*y)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
A,P,Ap,point=(200,100),(960,540),(0,100),(400,100)
Pp=add(P,rs(sub(Ap,A)))
old=add(P,rs(sub(point,A)))
new=add(Pp,rs(sub(point,Ap)))
wrong=add(P,rs(sub(point,Ap)))
assert all(math.isclose(x,y,abs_tol=1e-9) for x,y in zip(old,new))
a=.25; fg=(.8,.2,.1); bg=(.1,.3,.5)
pm=tuple(a*x for x in fg)
correct=tuple(x+(1-a)*y for x,y in zip(pm,bg))
double=tuple(a*x+(1-a)*y for x,y in zip(pm,bg))
unassociated=tuple(x+(1-a)*y for x,y in zip(fg,bg))
assert all(math.isclose(x,y) for x,y in zip(correct,(.275,.275,.4)))
def encode(x):return 12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055
def decode(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
assert math.isclose(decode(encode(.5)),.5,abs_tol=1e-12)
def time_map(n):
    if n<30:return n
    if n<156:return 30+(n-30)*246/126
    return 276+(n-156)
assert [time_map(n) for n in (30,156,180)]==[30,276,300]
assert all(time_map(n+1)>time_map(n) for n in range(180))
assert 48-54<0
r={
 'evidence_scope':'Analytic calculations executed; no rendering or application interoperability tested.',
 'anchor':{'new_position':Pp,'old_point':old,'compensated_point':new,'uncompensated_point':wrong,'jump':sub(wrong,old)},
 'alpha':{'premultiplied':pm,'correct':correct,'double_multiplied':double,'straight_misread':unassociated},
 'srgb':{'encoded_linear_half':encode(.5),'eight_bit_nearest':round(255*encode(.5)),'decoded_encoded_half':decode(.5),'encoded_half_eight_bit':round(255*.5)},
 'shutter':{'duration_30':180/(360*30),'half_duration_30':1/120,'blur_30':900/60,'blur_24':900/48},
 'camera':{'width_near':1200*200/1000,'width_far':1200*200/1500,'shift_near':1200*100/1000,'shift_far':1200*100/1500},
 'revision':{'elastic_scale':126/246,'boundary_source_coordinates':[time_map(n) for n in (30,156,180)],'invalid_remaining_frames':48-54,'portrait_margin':1080*.05,'usable_width':1080*.9,'title_scale':972/1100}
}
out=p/'calculation-results.json'
assert not out.exists(), 'Refuse overwrite without a backup'
out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
