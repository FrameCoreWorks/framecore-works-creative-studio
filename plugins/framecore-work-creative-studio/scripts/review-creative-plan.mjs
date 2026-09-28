import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const object = v => v !== null && typeof v === 'object' && !Array.isArray(v);
const nonempty = v => typeof v === 'string' && v.trim().length > 0;
const known = v => nonempty(v) && !['unknown','unverified'].includes(v.trim().toLowerCase());
const finite = v => typeof v === 'number' && Number.isFinite(v);
const positive = v => finite(v) && v > 0;
const scope = 'Declared planning data only; no media inspection, taste inference, permissions or provider execution.';

export function reviewSequence(plan) {
  const errors=[], blockers=[], review=[];
  const result=()=>({status:errors.length?'invalid_plan':'structurally_valid_plan',execution_readiness:errors.length||blockers.length?'blocked':'unverified',observed_quality:'uninspected',errors,blockers,human_review:review,evidence_scope:scope});
  if (!object(plan) || !Array.isArray(plan.shots) || !plan.shots.length || !Array.isArray(plan.bridges)) {errors.push('A nonempty shot list and a bridge list are required.');return result();}
  if (!positive(plan.target_duration_s)) errors.push('Target duration must be a positive number of seconds.');
  const ids=new Set();
  for (const shot of plan.shots) {
    if (!object(shot)) {errors.push('Every shot must be an object.');continue;}
    if (!known(shot.id) || ids.has(shot.id)) errors.push('Shot IDs must be known and unique.');ids.add(shot.id);
    if (!finite(shot.start_s) || shot.start_s<0 || !finite(shot.end_s) || shot.end_s<=shot.start_s) errors.push(`${shot.id}: invalid edit interval.`);
    if (!['proposed','user_supplied','measured'].includes(shot.timing_basis)) errors.push(`${shot.id}: timing basis is required.`);
    if (shot.timing_basis==='measured' && !known(shot.timing_evidence)) errors.push(`${shot.id}: measured timing requires observed evidence.`);
    if (!known(shot.action) || !known(shot.entry_state) || !known(shot.exit_state)) errors.push(`${shot.id}: describe an action and entry/exit states.`);
    for (const key of ['primary_actions','camera_moves']) if (!Number.isInteger(shot[key]) || shot[key]<0) errors.push(`${shot.id}: ${key} must be a nonnegative integer.`);
    if ((shot.primary_actions>1 || shot.camera_moves>1) && !known(shot.complexity_reason)) review.push(`${shot.id}: simplify the action/camera or document why the complexity is readable.`);
    if (!['strict','approximate'].includes(shot.continuity_requirement)) errors.push(`${shot.id}: preserve an explicit continuity requirement.`);
    if (!Array.isArray(shot.required_refs) || !Array.isArray(shot.bound_refs)) {errors.push(`${shot.id}: reference inventories are required, even when empty.`);continue;}
    if (shot.required_refs.some(r=>!known(r)) || new Set(shot.required_refs).size!==shot.required_refs.length) errors.push(`${shot.id}: required reference aliases must be known and unique.`);
    if (shot.bound_refs.some(r=>!known(r))) errors.push(`${shot.id}: bound reference aliases must be known.`);
    const missing=shot.required_refs.filter(ref=>!shot.bound_refs.includes(ref));
    if (missing.length) blockers.push(`${shot.id}: unresolved required references: ${missing.join(', ')}. Requirement remains ${shot.continuity_requirement}.`);
    if (shot.continuity_requirement==='strict' && !shot.required_refs.length) blockers.push(`${shot.id}: strict requirement lacks a declared source carrier.`);
    if ('generation_duration_s' in shot && !positive(shot.generation_duration_s)) errors.push(`${shot.id}: source clip duration, when supplied, must be positive.`);
    if (positive(shot.generation_duration_s) && finite(shot.start_s) && finite(shot.end_s) && shot.end_s-shot.start_s>shot.generation_duration_s) errors.push(`${shot.id}: edit interval exceeds declared source clip duration.`);
  }
  const first=plan.shots[0],last=plan.shots.at(-1);
  if (first?.start_s!==0) errors.push('Timeline must start at zero.');
  if (!finite(last?.end_s) || Math.abs(last.end_s-plan.target_duration_s)>0.000001) errors.push('Timeline end must equal target duration.');
  const allowed=new Set(['cut','action_match','graphic_match','occlusion','sound_bridge','dissolve']);
  const pairs=new Set();
  for (const bridge of plan.bridges) {
    if (!object(bridge)) {errors.push('Every bridge must be an object.');continue;}
    const index=plan.shots.findIndex(shot=>shot?.id===bridge.from);
    if (index<0 || plan.shots[index+1]?.id!==bridge.to) errors.push('A bridge must join adjacent shot IDs.');
    const key=JSON.stringify([bridge.from,bridge.to]);if (pairs.has(key)) errors.push('Duplicate bridge.');pairs.add(key);
    if (!allowed.has(bridge.type)) errors.push(`${key}: unsupported bridge type.`);
    if (!finite(bridge.overlap_s) || bridge.overlap_s<0) errors.push(`${key}: overlap must be a nonnegative number.`);
    if (bridge.type!=='dissolve' && bridge.overlap_s!==0) errors.push(`${key}: this template permits picture overlap only for a dissolve; audio bridges do not overlap picture intervals.`);
    if (!known(bridge.relationship) || !Array.isArray(bridge.review_checks) || !bridge.review_checks.length || bridge.review_checks.some(c=>!known(c))) errors.push(`${key}: state the relationship and observable review checks.`);
  }
  for (let i=0;i<plan.shots.length-1;i++) {
    const a=plan.shots[i],b=plan.shots[i+1];if(!object(a)||!object(b))continue;
    const bridge=plan.bridges.find(v=>v?.from===a.id&&v?.to===b.id);
    if (!bridge) {errors.push(`${a.id} to ${b.id}: missing bridge.`);continue;}
    if (finite(a.end_s) && finite(b.start_s) && finite(bridge.overlap_s) && Math.abs(a.end_s-b.start_s-bridge.overlap_s)>0.000001) errors.push(`${a.id} to ${b.id}: timeline gap or overlap differs from the declared bridge.`);
    if (finite(bridge.overlap_s) && (bridge.overlap_s>=a.end_s-a.start_s || bridge.overlap_s>=b.end_s-b.start_s)) errors.push(`${a.id} to ${b.id}: overlap consumes an entire shot.`);
  }
  if (plan.bridges.length!==Math.max(0,plan.shots.length-1)) errors.push('Exactly one picture bridge per adjacent pair is required.');
  review.push('Inspect actual outgoing/incoming media for action phase, screen direction, product state, colour and sound.');
  return result();
}

export function reviewTaste(profile) {
  const errors=[];
  if (!object(profile) || !Array.isArray(profile.records)) return {status:'invalid_profile',errors:['Expected records array.'],evidence_scope:scope};
  const ids=new Set();
  for (const record of profile.records) {
    if (!object(record)) {errors.push('Every preference record must be an object.');continue;}
    if (!known(record.id)||ids.has(record.id)) errors.push('Preference IDs must be known and unique.');ids.add(record.id);
    if (!['user','client','project'].includes(record.scope)||!known(record.scope_id)) errors.push(`${record.id}: scope and scope ID required.`);
    if (!known(record.preference)||!known(record.medium)||!known(record.source_decision)) errors.push(`${record.id}: preference, medium and source decision required.`);
    if (!['explicit','observed'].includes(record.evidence_type)||!Number.isInteger(record.evidence_count)||record.evidence_count<1) errors.push(`${record.id}: invalid evidence declaration.`);
    if (!['tentative','confirmed'].includes(record.confidence)||!['active','retired','unresolved'].includes(record.status)) errors.push(`${record.id}: invalid confidence/status.`);
    if (record.confidence==='confirmed'&&record.evidence_type!=='explicit') errors.push(`${record.id}: an inferred preference cannot be labelled confirmed.`);
    if (record.evidence_type==='observed'&&record.evidence_count<2) errors.push(`${record.id}: one implicit observation is not a reusable taste pattern.`);
    if (!['accepted','rejected','mixed','stated_preference'].includes(record.decision)) errors.push(`${record.id}: invalid decision.`);
    if (!nonempty(record.stated_reason)) errors.push(`${record.id}: reason must be supplied or explicitly Unknown.`);
  }
  return {status:errors.length?'invalid_profile':'structurally_valid_profile',errors,persistence:'not_performed',evidence_scope:scope};
}

if (process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {
    const [kind,file,...extra]=process.argv.slice(2);
    if (!['sequence','taste'].includes(kind)||!file||extra.length) throw new Error('Usage: node review-creative-plan.mjs sequence|taste <JSON-file>');
    const input=JSON.parse(fs.readFileSync(file,'utf8'));
    const result=kind==='sequence'?reviewSequence(input):reviewTaste(input);
    console.log(JSON.stringify(result,null,2));
    if(result.errors.length)process.exitCode=1;
  } catch(error) {console.error(error.message);process.exitCode=2;}
}
