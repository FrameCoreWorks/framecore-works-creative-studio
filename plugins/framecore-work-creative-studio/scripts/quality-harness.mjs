// Read-only checks over declared records. No tool/media execution, persistence or adoption.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {isDeepStrictEqual} from 'node:util';

const object = v => !!v && typeof v === 'object' && !Array.isArray(v);
const text = v => typeof v === 'string' && !!v.trim() && !v.includes('REPLACE_WITH');
const strings = v => Array.isArray(v) && v.every(text);
const positive = v => Number.isFinite(v) && v > 0;

export function validateExampleBank(bank) {
  const errors = [], ids = new Set();
  if (bank?.schema_version !== 1 || !Array.isArray(bank?.examples) || !text(bank?.evidence_scope)) return ['Invalid example bank'];
  for (const item of bank.examples) {
    if (!text(item?.id) || ids.has(item.id)) errors.push('Missing or duplicate example ID');
    ids.add(item?.id);
    if (!['static', 'video', 'audio', 'copy'].includes(item?.domain) || !strings(item?.stages) || !item.stages.length || !strings(item?.problem_tags) || !item.problem_tags.length || !strings(item?.supported_locks)) errors.push('Invalid retrieval fields: ' + item?.id);
    for (const field of ['brief', 'decision', 'consequence']) if (!text(item?.[field])) errors.push('Missing ' + field + ': ' + item?.id);
    if (!strings(item?.exclusions) || !item.exclusions.length) errors.push('Missing exclusions: ' + item?.id);
    for (const label of ['good', 'bad', 'borderline']) {
      const anchor = item?.anchors?.[label];
      if (!text(anchor?.output) || !text(anchor?.criterion) || anchor?.hard_gates !== (label === 'bad' ? 'FAIL' : 'PASS')) errors.push('Invalid anchor: ' + item?.id + '/' + label);
    }
  }
  return errors;
}

export function selectExamples(bank, query, limit = 3) {
  const errors = validateExampleBank(bank);
  if (errors.length) throw new Error(errors.join('; '));
  if (!text(query?.domain) || !text(query?.stage) || !strings(query?.problem_tags) || !strings(query?.required_locks ?? []) || !Number.isInteger(limit) || limit < 1 || limit > 3) throw new Error('Invalid query or limit (1–3)');
  return bank.examples.filter(item => item.domain === query.domain && item.stages.includes(query.stage) && (query.required_locks ?? []).every(lock => item.supported_locks.includes(lock)))
    .map(item => ({item, matches: [...new Set(query.problem_tags)].filter(tag => item.problem_tags.includes(tag))}))
    .filter(result => result.matches.length)
    .sort((a, b) => b.matches.length - a.matches.length || a.item.id.localeCompare(b.item.id, 'en'))
    .slice(0, limit).map(({item, matches}) => ({...item, fit_reason: 'Matched domain/stage/locks and ' + matches.join(', ')}));
}

const methods = {
  plan: {copy: ['authored_text'], dimensions: ['document_spec'], duration: ['document_spec', 'calculation'], number: ['approved_source', 'calculation'], count: ['document_spec']},
  actual_media: {copy: ['visual_transcription'], dimensions: ['file_probe'], duration: ['file_probe'], number: ['approved_source', 'calculation', 'visual_transcription'], count: ['region_inspection', 'time_range_inspection']},
};

export function checkArtifact(contract, observation) {
  const checks = [], errors = [];
  const result = () => ({status: errors.length || checks.some(c => c.result === 'FAIL') ? 'FAIL' : checks.some(c => c.result === 'Unknown') || !checks.length ? 'Unknown' : 'PASS', evidence_scope: 'Declared evidence comparison only; evidence is not authenticated and media is not inspected by this helper.', kind: observation?.kind ?? 'Unknown', certified_media: false, checks, errors});
  if (!object(contract) || !text(contract.revision) || !object(observation) || !methods[observation.kind] || !Array.isArray(observation.evidence)) {errors.push('Invalid contract or observation'); return result();}
  const requirements = [];
  if (contract.copy !== undefined) {
    if (!Array.isArray(contract.copy)) errors.push('copy must be an array');
    else for (const item of contract.copy) {
      if (!text(item?.id) || typeof item?.text !== 'string') errors.push('Invalid copy lock');
      else requirements.push({property: 'copy', id: item.id, expected: item.text});
    }
  }
  if (contract.dimensions !== undefined) {
    if (!object(contract.dimensions) || !positive(contract.dimensions.width) || !positive(contract.dimensions.height)) errors.push('Invalid dimensions');
    else requirements.push({property: 'dimensions', expected: contract.dimensions});
  }
  if (contract.duration_seconds !== undefined) {
    const range = contract.duration_seconds;
    if (!object(range) || !positive(range.min) || !positive(range.max) || range.max < range.min) errors.push('Invalid duration range');
    else requirements.push({property: 'duration', expected: range});
  }
  if (contract.numbers !== undefined) {
    if (!Array.isArray(contract.numbers)) errors.push('numbers must be an array');
    else for (const item of contract.numbers) {
      if (!text(item?.id) || !Number.isFinite(item?.value) || !text(item?.unit)) errors.push('Invalid number lock');
      else requirements.push({property: 'number', id: item.id, expected: item.value, unit: item.unit});
    }
  }
  if (contract.counts !== undefined) {
    if (!object(contract.counts)) errors.push('counts must be an object');
    else for (const [id, expected] of Object.entries(contract.counts)) {
      if (!text(id) || !Number.isInteger(expected) || expected < 0) errors.push('Invalid count lock');
      else requirements.push({property: 'count', id, expected});
    }
  }
  const keys = requirements.map(r => r.property + ':' + (r.id ?? ''));
  if (new Set(keys).size !== keys.length) errors.push('Duplicate requirement');
  for (const req of requirements) {
    const records = observation.evidence.filter(e => e?.property === req.property && e?.id === req.id);
    let state = 'Unknown', reason = 'Missing current scoped evidence', record;
    if (records.length > 1) {state = 'FAIL'; reason = 'Ambiguous duplicate evidence';}
    else if (records.length === 1) {
      record = records[0];
      if (observation.artifact_revision === contract.revision && record.revision === contract.revision && text(record.locator) && methods[observation.kind][req.property]?.includes(record.method)) {
        let matches;
        if (req.property === 'duration') matches = positive(record.value) && record.value >= req.expected.min && record.value <= req.expected.max;
        else matches = isDeepStrictEqual(record.value, req.expected) && (req.unit === undefined || record.unit === req.unit);
        state = matches ? 'PASS' : 'FAIL'; reason = matches ? 'Declared evidence matches' : 'Observed value does not match lock';
      }
    }
    checks.push({...req, observed: record?.value ?? 'Unknown', method: record?.method ?? 'Unknown', locator: record?.locator ?? 'Unknown', result: state, reason});
  }
  if (contract.exact_copy_only === true) for (const e of observation.evidence) {
    if (e?.property === 'copy' && !requirements.some(r => r.property === 'copy' && r.id === e.id)) checks.push({property: 'copy', id: e.id, result: 'FAIL', reason: 'Unrequested extra copy in declared evidence'});
  }
  return result();
}

export function evaluatePair(record) {
  const blocked = reason => ({decision: 'unresolved', reason, calibrated: false, independent_review: false});
  if (!Array.isArray(record?.candidate_ids) || record.candidate_ids.length !== 2 || new Set(record.candidate_ids).size !== 2 || !record.candidate_ids.every(text) || !strings(record.criteria) || !record.criteria.length || !strings(record.required_hard_gates) || !record.required_hard_gates.length || !strings(record.anchor_ids) || !record.anchor_ids.length) return blocked('Invalid pair record');
  const ids = record.candidate_ids;
  for (const id of ids) if (!text(record.revisions?.[id]) || record.hard_gates?.[id]?.revision !== record.revisions[id]) return blocked('Missing or stale candidate revision');
  const states = ids.map(id => record.required_hard_gates.map(gate => record.hard_gates[id][gate]));
  if (states.some(values => values.some(v => !['PASS', 'FAIL', 'Unknown'].includes(v)))) return blocked('Missing or invalid hard gate');
  const eligible = states.map(values => !values.includes('FAIL') && !values.includes('Unknown'));
  if (!eligible.some(Boolean)) return blocked('No candidate passes all hard gates');
  const failed = states.map(values => values.includes('FAIL'));
  if (eligible[0] && failed[1]) return {decision: ids[0], reason: 'Other candidate fails a hard gate', calibrated: false, independent_review: false};
  if (eligible[1] && failed[0]) return {decision: ids[1], reason: 'Other candidate fails a hard gate', calibrated: false, independent_review: false};
  if (!eligible.every(Boolean)) return blocked('Unknown evidence blocks comparison acceptance');
  const map = (pass, order) => {
    if (!isDeepStrictEqual(pass?.order, order) || !text(pass?.reason) || !['A', 'B', 'tie'].includes(pass?.winner)) return undefined;
    return pass.winner === 'tie' ? 'tie' : order[pass.winner === 'A' ? 0 : 1];
  };
  const ab = map(record.ab_verdict, ids), ba = map(record.ba_verdict, [...ids].reverse());
  if (!ab || !ba) return blocked('Missing reversed-order verdicts');
  if (ab !== ba) return {...blocked('order_disagreement'), ab_candidate: ab, ba_candidate: ba};
  return {decision: ab, reason: 'Consistent declared order check', owner_decision: record.owner_decision ?? 'not_collected', calibrated: false, independent_review: false};
}

export function validateLesson(lesson) {
  const errors = [];
  if (!object(lesson)) return {valid: false, reusable: false, persistence: 'not_performed', errors: ['Invalid lesson']};
  for (const field of ['id', 'domain', 'trigger', 'error', 'cause', 'correction']) if (!text(lesson[field])) errors.push('Missing ' + field);
  if (lesson.schema_version !== 1 || !['proposed', 'adopted', 'retired'].includes(lesson.status)) errors.push('Invalid lesson version/status');
  if (!['user', 'client', 'project'].includes(lesson.scope?.type) || !text(lesson.scope?.id)) errors.push('Missing scoped authority');
  if (!['hypothesis', 'confirmed_by_test'].includes(lesson.cause_status) || (lesson.cause_status === 'confirmed_by_test' && !text(lesson.cause_evidence_id))) errors.push('Unsupported cause confidence');
  if (!strings(lesson.exclusions) || !lesson.exclusions.length) errors.push('Missing applicability exclusions');
  if (lesson.test?.result !== 'PASS' || !text(lesson.test?.evidence_id) || !text(lesson.test?.revision)) errors.push('Correction not successfully tested with evidence');
  if (lesson.status === 'adopted' && (lesson.adoption?.explicit !== true || !text(lesson.adoption?.owner) || !text(lesson.adoption?.evidence_id))) errors.push('No explicit scoped adoption');
  if (lesson.persistence !== 'not_performed') errors.push('This helper cannot establish persistence');
  return {valid: !errors.length, reusable: !errors.length && lesson.status === 'adopted', persistence: 'not_performed', errors};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const [action, filename] = process.argv.slice(2);
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const result = action === 'retrieve' ? selectExamples(data.bank, data.query, data.limit ?? 3) : action === 'check' ? checkArtifact(data.contract, data.observation) : action === 'pair' ? evaluatePair(data) : action === 'lesson' ? validateLesson(data) : (() => {throw new Error('Use retrieve|check|pair|lesson with a JSON file');})();
    console.log(JSON.stringify(result, null, 2));
    if (result.status === 'FAIL' || result.valid === false) process.exitCode = 1;
  } catch (error) {console.error(error.message); process.exitCode = 1;}
}
