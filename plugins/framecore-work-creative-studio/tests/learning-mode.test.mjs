import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateStudio} from '../scripts/validate-studio.mjs';
import {loadEffectiveEvals, caseDigest} from '../scripts/load-effective-evals.mjs';
import {learningDomainIds, learningCaseIds, evaluateStartupReply} from '../scripts/validate-learning-mode.mjs';

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

test('grouped-menu example remains outside single-question learning onboarding', () => fixture(root => {
  edit(root, 'skills/workflow-orchestrator/references/startup-and-creative-menus.md', text => text.replace('when a production task calls for grouped choices', 'learning domains and learning pace'));
  assert.ok(codes(root).includes('LEARNING_INSTRUCTION'));
}));

test('a standalone progress card retains the unfinished onboarding state', () => {
  for (const phrase of ['onboarding_context', 'known/unknown/skipped answers', 'questions asked', 'six-question limit', 'at most one pending question', 'displayed token-to-option mapping', 'Remove answered/skipped/replaced pending questions']) fixture(root => {
    edit(root, 'skills/workflow-orchestrator/assets/learning-progress.template.md', text => text.replace(phrase, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), phrase);
  });
});

test('learning is integrated with the same 37 skills and unexecuted evidence scope', () => {
  const result = validateStudio(source);
  assert.equal(result.status, 'PASS', JSON.stringify(result.canonical.errors));
  assert.equal(result.canonical.owners, 37);
  assert.equal(result.canonical.evaluations.learning_scenarios, 24);
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
  const welcome = 'skills/workflow-orchestrator/assets/startup-welcome.pl.md';
  for (const [file, phrase] of [
    ...['## Complete welcome', 'copy verbatim the entire file', 'Repeat the identical complete welcome on every sent Studio-only invocation', '## Creative pace choice', '## Established work-area menu', '## Motion graphics in creative work', 'choose Creative Mode, Expanded Mode, then area `8`', 'Preserve a runtime explicitly supplied', '8. Motion graphics z kodu', 'Area `3` still selects storyboards', 'A `3` from the two-option startup menu asks for clarification without selecting motion', 'bare number only against a currently pending displayed choice group', 'concrete project request bypasses menus'].map(phrase => [startup, phrase]),
    ...['Jestem FrameCore Works Creative Studio.', 'Mogę pomóc Ci w:', '1. **Tryb kreatywny**', '2. **Tryb nauki**'].map(phrase => [welcome, phrase]),
    ['skills/workflow-orchestrator/SKILL.md', 'copy verbatim the entire file']
  ]) fixture(root => {
    edit(root, file, text => text.replaceAll(phrase, 'removed'));
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
  assert.deepEqual(start.follow_up_sequences.map(item => item.id), ['creative_quick', 'creative_deep', 'learning', 'direct_brief', 'invalid_startup_choice', 'motion_area', 'motion_learning']);
  assert.ok(start.follow_up_sequences.every(item => item.execution_status === 'not_run'));
});

test('the complete startup excerpt is available before general review instructions', () => {
  const entry = read('skills/workflow-orchestrator/SKILL.md');
  const begin = '<!-- BEGIN CANONICAL STARTUP RESPONSE -->\n';
  const end = '<!-- END CANONICAL STARTUP RESPONSE -->';
  const response = entry.slice(entry.indexOf(begin) + begin.length, entry.indexOf(end));
  assert.equal(response, read('skills/workflow-orchestrator/assets/startup-welcome.pl.md'));
  assert.ok(entry.indexOf(end) < entry.indexOf('Before final delivery'));
});

test('truncating the startup excerpt fails even when the canonical asset remains intact', () => fixture(root => {
  edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replace('Mogę pomóc Ci w:\n', ''));
  assert.ok(codes(root).includes('STARTUP_RESPONSE_PROJECTION'));
}));

test('a protected-word change fails even when the excerpt and asset are changed together', () => fixture(root => {
  for (const file of ['skills/workflow-orchestrator/SKILL.md', 'skills/workflow-orchestrator/assets/startup-welcome.pl.md']) edit(root, file, text => text.replace('Pomagam rozwijać pomysły', 'Pomagam rozwijać idee'));
  assert.ok(codes(root).includes('STARTUP_WELCOME_INTEGRITY'));
}));

test('moving the full welcome below general instructions fails startup placement', () => fixture(root => {
  edit(root, 'skills/workflow-orchestrator/SKILL.md', text => {
    const begin = text.indexOf('<!-- BEGIN CANONICAL STARTUP RESPONSE -->');
    const end = text.indexOf('<!-- END CANONICAL STARTUP RESPONSE -->') + '<!-- END CANONICAL STARTUP RESPONSE -->'.length;
    const block = text.slice(begin, end);
    return text.slice(0, begin) + text.slice(end) + '\n' + block + '\n';
  });
  assert.ok(codes(root).includes('STARTUP_RESPONSE_PLACEMENT'));
}));

test('supplied mode-only, shortened, paraphrased and prefixed startup replies fail', () => {
  const welcome = read('skills/workflow-orchestrator/assets/startup-welcome.pl.md');
  const replies = [
    '**Wybierz tryb pracy:**\n\n1. **Tryb kreatywny**\n2. **Tryb nauki**',
    welcome.slice(welcome.indexOf('**Wybierz, od czego zaczynamy:**')),
    welcome.replace(/- \*\*Grafice i materiałach reklamowych\*\*[^\n]+\n/, ''),
    welcome.replace('Pomagam rozwijać pomysły', 'Pomagam rozwijać idee'),
    'Cześć!\n\n' + welcome,
    '```markdown\n' + welcome + '```',
    welcome + '\nCo chcesz zrobić?'
  ];
  for (const reply of replies) assert.equal(evaluateStartupReply(reply, welcome).status, 'FAIL');
});

test('supplied full repeated replies pass; unavailable actual reply remains Unknown', () => {
  const welcome = read('skills/workflow-orchestrator/assets/startup-welcome.pl.md');
  for (const reply of [welcome, welcome.slice(0, -1), welcome]) assert.equal(evaluateStartupReply(reply, welcome).status, 'PASS');
  assert.equal(evaluateStartupReply(undefined, welcome).status, 'Unknown');
  assert.equal(evaluateStartupReply('', welcome).status, 'FAIL');
});

test('both full localized sources are early byte-matched excerpts', () => {
  const entry = read('skills/workflow-orchestrator/SKILL.md');
  for (const [locale, marker] of [['en', 'ENGLISH'], ['pl', 'CANONICAL']]) {
    const begin = '<!-- BEGIN ' + marker + ' STARTUP RESPONSE -->\n';
    const end = '<!-- END ' + marker + ' STARTUP RESPONSE -->';
    assert.equal(entry.slice(entry.indexOf(begin) + begin.length, entry.indexOf(end)), read('skills/workflow-orchestrator/assets/startup-welcome.' + locale + '.md'));
    assert.ok(entry.indexOf(end) < entry.indexOf('Before final delivery'));
  }
});

test('English truncation and synchronized English rewriting fail source guards', () => {
  fixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replace('I can help you with:\n', ''));
    assert.ok(codes(root).includes('STARTUP_RESPONSE_PROJECTION'));
  });
  fixture(root => {
    for (const file of ['skills/workflow-orchestrator/SKILL.md', 'skills/workflow-orchestrator/assets/startup-welcome.en.md']) edit(root, file, text => text.replace('I help develop ideas', 'I help develop concepts'));
    assert.ok(codes(root).includes('STARTUP_WELCOME_INTEGRITY'));
  });
});

test('language policy cannot drift between entry and reference or follow the excerpts', () => {
  fixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replace('most recent meaningful user conversation language', 'previous assistant response language'));
    assert.ok(codes(root).includes('STARTUP_LANGUAGE_PROJECTION'));
  });
  fixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => {
      const a = text.indexOf('<!-- BEGIN STARTUP LANGUAGE POLICY -->');
      const b = text.indexOf('<!-- END STARTUP LANGUAGE POLICY -->') + '<!-- END STARTUP LANGUAGE POLICY -->'.length;
      return text.slice(0, a) + text.slice(b) + '\n' + text.slice(a, b) + '\n';
    });
    assert.ok(codes(root).includes('STARTUP_LANGUAGE_PLACEMENT'));
  });
});

test('automatic language signals and full translation remain mandatory in both owners', () => {
  const resources = ['skills/workflow-orchestrator/SKILL.md', 'skills/workflow-orchestrator/references/startup-and-creative-menus.md'];
  for (const phrase of ['explicit response-language preference', 'current user-authored conversational text', "host's response/UI language only when actually supplied", 'most recent meaningful user conversation language', 'A user does not need to request translation', 'all six capability bullets', 'When the language changes, deliver the full welcome in the new language', 'Apply the same language selection to subsequent pace/area menus and learning onboarding']) fixture(root => {
    for (const file of resources) edit(root, file, text => text.replaceAll(phrase, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), phrase);
  });
});

test('reintroducing a fixed Polish default fails even beside the automatic language rule', () => fixture(root => {
  edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text + '\nPolish is the default for bare invocations.\n');
  assert.ok(codes(root).includes('STARTUP_FIXED_LANGUAGE'));
}));

test('supplied replies must match the complete selected-language source', () => {
  const en = read('skills/workflow-orchestrator/assets/startup-welcome.en.md');
  const pl = read('skills/workflow-orchestrator/assets/startup-welcome.pl.md');
  for (const expected of [en, pl]) {
    assert.equal(evaluateStartupReply(expected, expected).status, 'PASS');
    assert.equal(evaluateStartupReply(expected.slice(0, -1), expected).status, 'PASS');
    assert.equal(evaluateStartupReply(expected === en ? pl : en, expected).status, 'FAIL');
    assert.equal(evaluateStartupReply(expected.replace(/^- \*\*[^\n]+\n/m, ''), expected).status, 'FAIL');
    assert.equal(evaluateStartupReply(expected + '\nChoose your language.', expected).status, 'FAIL');
  }
});

test('lesson contract retains bounded onboarding, full plan, learner attempt and adaptive feedback', () => {
  for (const [file, phrase] of [
    ...['at most six short questions', 'Ask exactly one onboarding question per response and wait', 'Do not group onboarding questions', 'a natural-language answer', 'Do not ask an already answered question', 'Optional blanks do not block', 'all requested supported specializations', 'begin the first lesson', 'Stop for the learner\'s attempt', 'one or two priority improvements'].map(phrase => [method, phrase]),
    ...['skills/workflow-orchestrator/SKILL.md', 'skills/studio-workstyle-profile/SKILL.md', 'skills/pipeline-core/references/studio-integration-policy.md'].map(file => [file, 'Ask exactly one onboarding question per response and wait'])
  ]) fixture(root => {
    edit(root, file, text => text.replaceAll(phrase, 'removed'));
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
  assert.match(map.domains.find(d => d.id === 'commercial_video').support_boundary, /Webinar/);
  assert.match(map.domains.find(d => d.id === 'editing_motion').support_boundary, /VFX/);
  assert.match(map.domains.find(d => d.id === 'audio_music').support_boundary, /voice diagnosis/);
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

test('durable checkpoints and portable handoffs retain the same pending learning state', () => {
  const durable = 'skills/pipeline-core/assets/project-state.md';
  const handoff = 'skills/workflow-orchestrator/assets/cross-host-handoff.template.md';
  for (const field of ['interaction_mode', 'entry_context', 'learning_context']) fixture(root => {
    edit(root, durable, text => text.replace(field, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), field);
  });
  fixture(root => {
    edit(root, durable, text => text.replace('learning | creation | undecided', 'creation | undecided'));
    assert.ok(codes(root).includes('LEARNING_STATE_CONTRACT'));
  });
  fixture(root => {
    edit(root, handoff, text => text.replace('learning_context', 'removed'));
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

test('each teaching method retains its material safety and evidence boundary', () => {
  const boundaries = [
    'inside the first lesson, not in additional onboarding',
    'plan-only receives no diagnostic exercise',
    'Honor a request for a full explanation immediately',
    'Keep lesson completion, output quality and independence separate',
    'Keep learner-reported performance labelled separately',
    'at most one `pending_practice`',
    'A failed render alone proves no specific cause',
    'short new-context tasks'
  ];
  for (const boundary of boundaries) fixture(root => {
    edit(root, method, text => text.replaceAll(boundary, 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), boundary);
  });
});

test('practice evidence survives every existing state and handoff projection', () => {
  const views = ['skills/pipeline-core/templates/project-state.md', 'skills/pipeline-core/assets/project-state.md', 'skills/workflow-orchestrator/assets/cross-host-handoff.template.md', 'skills/workflow-orchestrator/assets/learning-progress.template.md'];
  for (const view of views) fixture(root => {
    edit(root, view, text => text.replaceAll('competency_evidence', 'removed'));
    assert.ok(codes(root).includes('LEARNING_INSTRUCTION'), view);
  });
});

test('new teaching scenarios preserve no-execution and unexecuted-outcome contracts', () => {
  const suite = JSON.parse(read(casesPath));
  const added = suite.cases.filter(c => Number(c.id.slice(2)) >= 17);
  assert.equal(added.length, 8);
  for (const family of ['diagnostic_practice', 'graduated_assistance', 'independence_evidence', 'transfer_practice', 'retrieval_resume', 'causal_diagnosis', 'evolving_project', 'requested_explanation']) assert.ok(added.some(c => c.family === family), family);
  assert.ok(added.every(c => c.execution_status === 'not_run' && c.tool_state.external_provider_authorized === false));
  assert.equal(added.find(c => c.id === 'LM21').research_expectation, 'prohibited_by_user');
  fixture(root => {
    editJSON(root, casesPath, suite => suite.cases.find(c => c.id === 'LM20').execution_status = 'passed');
    assert.ok(codes(root).includes('LEARNING_EVAL'));
  });
});
