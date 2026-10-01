import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {selectExamples, validateExampleBank, checkArtifact, evaluatePair, validateLesson} from '../scripts/quality-harness.mjs';
import {validateStudio} from '../scripts/validate-studio.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const bank = () => read('skills/commercial-video-campaign-director/assets/decision-examples.json');
const evidence = () => read('skills/output-critic-iteration/assets/quality-review.example.json');
const check = x => checkArtifact(x.contract, x.observation);
const pair = () => ({candidate_ids: ['base', 'candidate'], revisions: {base: 'r1', candidate: 'r2'}, criteria: ['specificity'], anchor_ids: ['STATIC-HIERARCHY'], required_hard_gates: ['copy', 'scope'], hard_gates: {base: {revision: 'r1', copy: 'PASS', scope: 'PASS'}, candidate: {revision: 'r2', copy: 'PASS', scope: 'PASS'}}, ab_verdict: {order: ['base', 'candidate'], winner: 'B', reason: 'Specific event relationship'}, ba_verdict: {order: ['candidate', 'base'], winner: 'A', reason: 'Same event relationship'}});
const lesson = () => ({schema_version: 1, id: 'synthetic-L1', status: 'proposed', scope: {type: 'project', id: 'synthetic-P1'}, domain: 'static', trigger: 'One exact glyph correction', error: 'Other approved text drifted', cause: 'Repair scope may have been broad', cause_status: 'hypothesis', correction: 'Bind original approved base and one word', test: {result: 'PASS', revision: 'synthetic-r2', evidence_id: 'synthetic-check-1'}, exclusions: ['Not a full redesign'], adoption: {explicit: false, owner: '', evidence_id: ''}, persistence: 'not_performed'});

test('retrieval filters domain, stage and hard locks before ranking, with a three-case ceiling', () => {
  const query = {domain: 'static', stage: 'review', problem_tags: ['scope', 'exact_copy', 'hierarchy'], required_locks: ['exact_copy']};
  const selected = selectExamples(bank(), query);
  assert.ok(selected.length && selected.length <= 3);
  assert.ok(selected.every(e => e.domain === 'static'));
  assert.equal(selectExamples(bank(), {...query, required_locks: ['layout']})[0].id, 'STATIC-LOCAL-EDIT');
  assert.deepEqual(selectExamples(bank(), {...query, problem_tags: ['unmatched']}), []);
  assert.throws(() => selectExamples(bank(), query, 4), /limit/);
});
test('malformed or duplicate anchors cannot enter retrieval', () => {
  const b = bank(); b.examples.push(b.examples[0]); assert.ok(validateExampleBank(b).length);
  b.examples[0].anchors.bad.hard_gates = 'PASS'; assert.match(validateExampleBank(b).join(';'), /anchor/);
});
test('exact copy rejects substring, spacing, punctuation and glyph drift', () => {
  for (const value of ['Wspólne nasiona!', 'Wspólne  nasiona', 'Wspolne nasiona', 'Dziś: Wspólne nasiona']) {
    const x = evidence(); x.observation.evidence[0].value = value; assert.equal(check(x).status, 'FAIL', value);
  }
});
test('plan PASS does not certify media, and authored text cannot certify a raster', () => {
  const x = evidence(); assert.equal(check(x).status, 'PASS'); assert.equal(check(x).certified_media, false);
  x.observation.kind = 'actual_media'; assert.equal(check(x).status, 'Unknown');
  x.observation.evidence[0].method = 'ocr'; assert.equal(check(x).checks[0].result, 'Unknown');
});
test('missing, stale and duplicate evidence do not pass', () => {
  const x = evidence(); x.observation.evidence = []; assert.equal(check(x).status, 'Unknown');
  const y = evidence(); y.observation.artifact_revision = 'old'; assert.equal(check(y).status, 'Unknown');
  const z = evidence(); z.observation.evidence[0].revision = 'old'; assert.equal(check(z).checks[0].result, 'Unknown');
  const d = evidence(); d.observation.evidence.push(d.observation.evidence[0]); assert.equal(check(d).status, 'FAIL');
});
test('dimension, number/unit, count and duration defects remain separate hard failures', () => {
  for (const index of [1, 2, 3]) {const x = evidence(); x.observation.evidence[index].value = 99; assert.equal(check(x).status, 'FAIL');}
  const x = evidence(); x.observation.evidence[2].unit = 'EUR'; assert.equal(check(x).status, 'FAIL');
  x.contract.duration_seconds = {min: 12, max: 12};
  x.observation.evidence.push({property: 'duration', value: 16, method: 'calculation', locator: 'synthetic intervals', revision: x.contract.revision});
  assert.equal(check(x).checks.find(c => c.property === 'duration').result, 'FAIL');
});
test('invalid contracts and unrequested copy cannot become a vacuous PASS', () => {
  for (const c of [null, {}, {revision: 'r', counts: null}, {revision: 'r', dimensions: {width: -1, height: 2}}]) assert.notEqual(checkArtifact(c, {kind: 'plan', evidence: []}).status, 'PASS');
  const x = evidence(); x.observation.evidence.push({property: 'copy', id: 'extra', value: 'New slogan'}); assert.equal(check(x).status, 'FAIL');
});
test('reversed pairwise verdicts map to candidates and never imply human calibration', () => {
  assert.equal(evaluatePair(pair()).decision, 'candidate'); assert.equal(evaluatePair(pair()).calibrated, false);
  const p = pair(); p.ba_verdict.winner = 'B'; assert.equal(evaluatePair(p).reason, 'order_disagreement');
  p.ab_verdict.winner = p.ba_verdict.winner = 'tie'; assert.equal(evaluatePair(p).decision, 'tie');
});
test('hard failure defeats beauty while Unknown and stale gates block acceptance', () => {
  const p = pair(); p.hard_gates.candidate.copy = 'FAIL'; assert.equal(evaluatePair(p).decision, 'base');
  p.hard_gates.candidate.copy = 'Unknown'; assert.equal(evaluatePair(p).decision, 'unresolved');
  p.hard_gates.candidate.copy = 'PASS'; p.hard_gates.candidate.revision = 'old'; assert.equal(evaluatePair(p).decision, 'unresolved');
  delete p.required_hard_gates; assert.equal(evaluatePair(p).decision, 'unresolved');
});
test('a tested Reflexion proposal needs separate explicit scoped adoption', () => {
  const l = lesson(); assert.equal(validateLesson(l).valid, true); assert.equal(validateLesson(l).reusable, false);
  l.status = 'adopted'; assert.equal(validateLesson(l).valid, false);
  l.adoption = {explicit: true, owner: 'synthetic-owner', evidence_id: 'synthetic-approval'};
  assert.equal(validateLesson(l).reusable, true); assert.equal(validateLesson(l).persistence, 'not_performed');
  l.status = 'retired'; assert.equal(validateLesson(l).reusable, false);
});
test('untested, unscoped or falsely confident lessons are rejected', () => {
  const l = lesson(); l.test.result = 'NOT_RUN'; assert.equal(validateLesson(l).valid, false);
  const s = lesson(); s.scope.type = 'everyone'; assert.equal(validateLesson(s).valid, false);
  const c = lesson(); c.cause_status = 'confirmed_by_test'; assert.equal(validateLesson(c).valid, false);
  assert.equal(validateLesson(read('skills/workflow-self-improvement/assets/reflexion-lesson.template.json')).reusable, false);
});
test('canonical checks catch removal of a quality guard and stale F03 owners', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'quality-guard-'));
  try {
    fs.cpSync(root, temp, {recursive: true});
    const file = path.join(temp, 'skills/pipeline-core/references/quality-improvement-methods.md');
    fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace('No method resets this budget', 'removed'));
    assert.ok(validateStudio(temp).canonical.errors.some(e => e.code === 'QUALITY_METHODS'));
    const f = path.join(temp, 'evals/studio-behavior-cases.json'), d = JSON.parse(fs.readFileSync(f, 'utf8'));
    d.cases.find(c => c.id === 'H01').expected_owners = ['humanizer']; fs.writeFileSync(f, JSON.stringify(d));
    assert.ok(validateStudio(temp).canonical.errors.some(e => e.detail.includes('Owner/evidence regression: H01')));
  } finally {fs.rmSync(temp, {recursive: true, force: true});}
});
