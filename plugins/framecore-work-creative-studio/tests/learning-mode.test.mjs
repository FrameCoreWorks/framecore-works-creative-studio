import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateStudio} from '../scripts/validate-studio.mjs';
import {loadEffectiveEvals, caseDigest} from '../scripts/load-effective-evals.mjs';
import {learningDomainIds, learningCaseIds} from '../scripts/validate-learning-mode.mjs';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const method = 'skills/workflow-orchestrator/references/learning-mode.md';
const domainMap = 'skills/workflow-orchestrator/assets/learning-domains.json';
const casesPath = 'evals/learning-mode-cases.json';
const read = (relative, root = source) => fs.readFileSync(path.join(root, relative), 'utf8');
function fixture(run) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-learning-test-'));
  try { fs.cpSync(source, root, {recursive: true}); return run(root); }
  finally { fs.rmSync(root, {recursive: true, force: true}); }
}
function edit(root, relative, change) {
  const before = read(relative, root), after = change(before);
  assert.notEqual(after, before, 'Mutation must apply: ' + relative);
  fs.writeFileSync(path.join(root, relative), after);
}
const editJSON = (root, relative, change) => edit(root, relative, text => {
  const value = JSON.parse(text); change(value); return JSON.stringify(value);
});
const codes = root => (validateStudio(root).canonical?.errors ?? []).map(item => item.code);

test('learning is integrated with the same 37 skills and unexecuted evidence scope', () => {
  const result = validateStudio(source);
  assert.equal(result.status, 'PASS', JSON.stringify(result.canonical.errors));
  assert.equal(result.canonical.owners, 37);
  assert.equal(result.canonical.evaluations.learning_scenarios, 16);
  assert.equal(result.canonical.evaluations.executed, 0);
});

test('historical greeting is preserved with a guarded effective mode-menu override', () => {
  const original = JSON.parse(read('evals/static-cases.json')).cases.find(c => c.id === 'S01');
  assert.ok(original.checks.some(c => c.includes('Non-exhaustive menu')));
  const override = JSON.parse(read('evals/effective-overrides.json')).overrides.find(c => c.id === 'S01');
  assert.equal(override.source_record_sha256, caseDigest(original));
  const effective = loadEffectiveEvals(source);
  assert.equal(effective.cases.find(c => c.id === 'S01').expected_branch, 'learning_or_creation_menu');
  const production = effective.cases.find(c => c.id === 'S02');
  assert.equal(production.expected_branch, 'complete_prompt_no_generation');
  assert.ok(production.checks.includes('Concrete prompt request bypasses onboarding menu'));
});

test('both intent labels and immediate production entry remain discoverable', () => {
  for (const phrase of ['Tryb nauki', 'Tryb tworzenia', 'creation immediately']) fixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replaceAll(phrase, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), phrase);
  });
});

test('startup cannot lose its welcome, creative pace step or displayed-menu number binding', () => {
  const startup = 'skills/workflow-orchestrator/references/startup-and-creative-menus.md';
  for (const phrase of ['## Complete welcome', '1. **Tryb kreatywny**', '2. **Tryb nauki**', '## Creative pace choice', '## Established work-area menu', 'bare number only against a currently pending displayed choice group', 'concrete project request bypasses menus']) fixture(root => {
    edit(root, startup, text => text.replaceAll(phrase, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), phrase);
  });
});

test('orchestrator and shared intake cannot bypass the creative pace transition', () => {
  for (const [path, phrase] of [
    ['skills/workflow-orchestrator/SKILL.md', 'After a mode-only creative choice'],
    ['skills/workflow-orchestrator/references/intake-and-reference-authority.md', 'mode-only creative choice gets Quick/Deep pace selection'],
    ['skills/pipeline-core/templates/project-state.md', 'last menu actually shown']
  ]) fixture(root => {
    edit(root, path, text => text.replaceAll(phrase, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), path);
  });
  const start = loadEffectiveEvals(source).cases.find(c => c.id === 'LM01');
  assert.deepEqual(start.follow_up_sequences.map(item => item.id), ['creative_quick', 'creative_deep', 'learning', 'direct_brief']);
  assert.ok(start.follow_up_sequences.every(item => item.execution_status === 'not_run'));
});

test('lesson contract retains bounded onboarding, full plan, learner attempt and adaptive feedback', () => {
  for (const phrase of ['at most six short questions', 'optional blanks do not block', 'all requested supported specializations', 'begin the first lesson', 'Stop for the learner\'s attempt', 'one or two priority improvements']) fixture(root => {
    edit(root, method, text => text.replaceAll(phrase, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), phrase);
  });
});

test('learning permission boundary cannot silently lose the no-execution rule', () => fixture(root => {
  edit(root, method, text => text.replace('Learning alone authorizes no generation', 'Learning automatically generates'));
  assert.ok(codes(root).includes('LEARNING_INSTRUCTION'));
}));

test('domain coverage includes broad creative competence and no-render exercises', () => {
  const map = JSON.parse(read(domainMap));
  assert.deepEqual(map.domains.map(d => d.id), learningDomainIds);
  for (const domain of map.domains) {
    assert.ok(domain.exercise_no_render.trim());
    assert.ok(domain.assessment_criteria.length >= 2);
    assert.ok(domain.support_boundary.trim());
    for (const owner of domain.owners) assert.ok(fs.existsSync(path.join(source, 'skills', owner, 'SKILL.md')));
  }
  assert.match(map.domains.find(d => d.id === 'commercial_video').support_boundary, /Webinary/);
  assert.match(map.domains.find(d => d.id === 'editing_motion').support_boundary, /VFX/);
  assert.match(map.domains.find(d => d.id === 'audio_music').support_boundary, /diagnozy głosu/);
});

test('lost domain, exercise or owner is rejected', () => {
  fixture(root => { editJSON(root, domainMap, d => d.domains.pop()); assert.ok(codes(root).includes('LEARNING_DOMAIN_COVERAGE')); });
  fixture(root => { editJSON(root, domainMap, d => d.domains[0].exercise_no_render = ''); assert.ok(codes(root).includes('LEARNING_DOMAIN')); });
  fixture(root => { editJSON(root, domainMap, d => d.domains[0].owners = ['imaginary-teacher']); assert.ok(codes(root).includes('LEARNING_OWNER')); });
});

test('domain sources cannot point outside the package or to a missing file', () => {
  for (const target of ['../outside.md', 'skills/missing/SKILL.md']) fixture(root => {
    editJSON(root, domainMap, d => d.domains[0].sources.push(target));
    assert.ok(codes(root).includes('LEARNING_PACKAGE'));
  });
});

test('progress and mode switching preserve one Project State without claimed automatic completion', () => {
  assert.match(read(method), /switches to creation immediately/);
  assert.match(read(method), /Do not mark a lesson completed merely because it was displayed/);
  fixture(root => {
    edit(root, 'skills/pipeline-core/templates/project-state.md', text => text.replace('learning_context', 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'));
  });
});

test('scenario inventory covers learning, creation, resume, plan-only and provider boundaries', () => {
  const cases = loadEffectiveEvals(source).cases.filter(c => c.provenance.source_file === 'learning-mode-cases.json');
  assert.deepEqual(cases.map(c => c.id), learningCaseIds);
  for (const family of ['start_menu', 'direct_creation', 'learning_onboarding', 'complete_brief_plan_lesson', 'domain_choice', 'broad_curriculum', 'learner_participation', 'adaptive_feedback', 'switch_to_creation', 'switch_to_learning', 'production_regression', 'no_execution', 'progress_resume', 'no_browse_unknown_tools', 'plan_only', 'support_boundaries']) {
    assert.ok(cases.some(c => c.family === family), family);
  }
  assert.ok(cases.every(c => c.execution_status === 'not_run'));
});

test('missing cases and fabricated executed outcomes fail closed', () => {
  fixture(root => { editJSON(root, casesPath, d => d.cases.pop()); assert.ok(codes(root).includes('LEARNING_CASE_COVERAGE')); });
  fixture(root => { editJSON(root, casesPath, d => d.cases[0].execution_status = 'passed'); assert.ok(codes(root).includes('LEARNING_EVAL')); });
});

test('learning fixtures cannot imply generation or omit required research', () => {
  fixture(root => { editJSON(root, casesPath, d => d.cases[0].tool_state.external_provider_authorized = true); assert.ok(codes(root).includes('LEARNING_EVAL_AUTHORITY')); });
  fixture(root => { editJSON(root, casesPath, d => { const c = d.cases.find(c => c.research_expectation === 'required'); c.expected_owners = c.expected_owners.filter(o => o !== 'research-evidence'); }); assert.ok(codes(root).includes('LEARNING_RESEARCH_OWNER')); });
});
