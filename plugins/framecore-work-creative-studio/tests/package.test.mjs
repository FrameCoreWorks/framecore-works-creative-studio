import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validatePackage} from '../scripts/validate-package.mjs';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const researchEntrypoints = [
  'workflow-orchestrator', 'creative-music-video-director', 'producer-ai-task-builder', 'commercial-video-campaign-director',
  'commercial-visual-campaign-director', 'humanizer',
  'image-prompt-architect', 'video-prompt-architect', 'screenplay-story-architect',
  'storyboard-sequence-architect', 'storyboard-board-architect',
  'output-critic-iteration', 'delivery-documentation',
];
function hasMandatoryResearchRoute(text) {
  const researchLink = '../research-evidence/SKILL.md';
  const linkPosition = text.indexOf(researchLink);
  if (linkPosition < 0) return false;
  const routeContext = text.slice(Math.max(0, linkPosition - 220), linkPosition + researchLink.length);
  return /\bmandatory\b/i.test(routeContext) && /public research preflight/i.test(routeContext);
}
function fixture() {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'framecore-studio-test-'));
  const root = path.join(temporary, path.basename(source));
  fs.cpSync(source, root, {recursive: true});
  return {root, close() { fs.rmSync(temporary, {recursive: true, force: true}); }};
}
test('candidate has valid local structure', () => {
  assert.deepEqual(validatePackage(source).errors, []);
});
test('greeting instructions and planned onboarding case expose the approved non-exhaustive menu', () => {
  const orchestrator = fs.readFileSync(path.join(source, 'skills/workflow-orchestrator/SKILL.md'), 'utf8');
  const intake = fs.readFileSync(path.join(source, 'skills/workflow-orchestrator/references/intake-and-reference-authority.md'), 'utf8');
  const welcome = orchestrator.split('## Begin at the user\'s actual point')[1]?.split('## Choose a short route')[0] ?? '';
  assert.ok(welcome.startsWith('\n\nA greeting-only response'));
  assert.match(welcome, /> Jestem FrameCore Works Creative Studio\./);
  assert.match(welcome, /Do not begin the welcome with “Cześć”/);
  for (const item of ['**Szybki**', '**Rozbudowany**', 'Grafika statyczna', 'Wideo i prompty', 'Storyboardy', 'Kampanie reklamowe', 'Teksty i scenariusze', 'Teledyski i zadania muzyczne', 'Analiza dostarczonej grafiki', 'logo, zdjęcia, grafiki, przykłady lub dokumenty']) {
    assert.ok(welcome.includes(item), 'welcome must include ' + item);
  }
  assert.match(intake, /When the user has given a concrete task, act on it instead of repeating onboarding/);
  assert.match(intake, /not an automatic message sent merely because a host enabled or selected the plugin/);

  const staticCases = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8')).cases;
  const onboarding = staticCases.find(item => item.id === 'S01');
  assert.equal(onboarding.status, 'planned');
  for (const check of ['Quick and expanded are presented as work modes, not separate capabilities', 'Optional uploads', 'Does not begin Polish welcome with Cześć', 'No claim of completed or host-tested modules']) {
    assert.ok(onboarding.checks.includes(check), 'S01 must specify ' + check);
  }
  assert.ok(staticCases.find(item => item.id === 'S02').checks.includes('Concrete prompt request bypasses onboarding menu'));

  const manifests = [
    JSON.parse(fs.readFileSync(path.join(source, 'plugin.json'), 'utf8')).extensions['com.openai'].interface,
    JSON.parse(fs.readFileSync(path.join(source, '.codex-plugin/plugin.json'), 'utf8')).interface,
  ];
  for (const manifest of manifests) {
    assert.equal(manifest.defaultPrompt.length, 3);
    assert.ok(manifest.defaultPrompt.some(prompt => prompt.startsWith('Pokaż menu startowe')));
    assert.ok(manifest.defaultPrompt.every(prompt => prompt.length <= 128));
  }
});
test('all substantive creative entrypoints route through mandatory public research', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  for (const name of researchEntrypoints) {
    const text = fs.readFileSync(path.join(source, 'skills', name, 'SKILL.md'), 'utf8');
    assert.ok(hasMandatoryResearchRoute(text), name + ' must mark its research preflight mandatory');
  }
  const research = fs.readFileSync(path.join(source, 'skills/research-evidence/SKILL.md'), 'utf8');
  assert.ok(research.includes('Every new substantive creative task MUST use an active web search'));
});
test('planned fixtures distinguish research policy from tool availability', () => {
  const files = ['static-cases.json', 'story-cases.json', 'storyboard-cases.json', 'video-cases.json', 'campaign-cases.json', 'producer-cases.json'];
  const cases = new Map();
  for (const file of files) {
    const data = JSON.parse(fs.readFileSync(path.join(source, 'evals', file), 'utf8'));
    for (const item of data.cases) {
      assert.ok(['required', 'not_applicable', 'prohibited_by_user'].includes(item.research_expectation), item.id);
      assert.ok(['available_read_only', 'prohibited_by_user'].includes(item.tool_state.web_search), item.id);
      assert.ok(['textual_fixture_no_execution', 'planned_fixture_only'].includes(item.tool_state.mode), item.id);
      if (item.research_expectation === 'not_applicable') assert.ok(item.research_exemption_reason, item.id);
      cases.set(item.id, item);
    }
  }
  for (const id of ['S02', 'S03', 'S10', 'S17', 'S19', 'SC01', 'SC05', 'SC06', 'SC10', 'SB01', 'SB06', 'SB14', 'V01', 'V02', 'V14', 'V15', 'MV01', 'MV02', 'MV03', 'MV04', 'PA01', 'PA02', 'PA05', 'PA06', 'PA07']) {
    assert.equal(cases.get(id)?.research_expectation, 'required', id);
  }
  for (const id of ['S01', 'S05', 'S07', 'S38', 'SC08', 'SB05', 'SB13', 'V08']) {
    assert.equal(cases.get(id)?.research_expectation, 'not_applicable', id);
  }
  for (const id of ['S11', 'V03']) {
    assert.equal(cases.get(id)?.research_expectation, 'prohibited_by_user', id);
  }
  assert.equal(cases.get('PA03')?.research_expectation, 'not_applicable', 'missing required producer-task input');
  assert.equal(cases.get('PA04')?.research_expectation, 'prohibited_by_user', 'user-prohibited current product research');
  assert.equal(cases.get('SC05').research_expectation, 'required', 'user-supplied copy does not verify a claim');
});
test('image model snapshot has dated, surface-aware family cards and a scoped watchlist', () => {
  const filename = path.join(source, 'skills/research-evidence/references/image-generator-snapshot.md');
  const text = fs.readFileSync(filename, 'utf8');
  const names = [...text.matchAll(/^### Family: (.+)$/gm)].map(match => match[1]);
  assert.equal(text.includes('Snapshot date: 2026-09-24.'), true);
  assert.equal(names.length, 19);
  assert.equal(new Set(names).size, 19);
  assert.ok(text.includes('## Watchlist and evidence gaps'));
  assert.ok(text.includes('## Dated practitioner evidence register'));
  for (const name of names) {
    const start = text.indexOf('### Family: ' + name);
    const following = text.indexOf('\n### Family:', start + 1);
    const watchlist = text.indexOf('\n## Watchlist and evidence gaps', start + 1);
    const endCandidates = [following, watchlist].filter(index => index >= 0);
    const section = text.slice(start, endCandidates.length ? Math.min(...endCandidates) : text.length);
    for (const field of ['**Variants:**', '**Surface and operations:**', '**Prompt guidance:**', '**Practitioner evidence:**', '**Unknowns:**', '**Sources:**']) {
      assert.ok(section.includes(field), name + ' must include ' + field);
    }
    assert.match(section, /https:\/\//, name + ' must cite a direct source');
  }
  const researchSkill = fs.readFileSync(path.join(source, 'skills/research-evidence/SKILL.md'), 'utf8');
  const sourceRegister = fs.readFileSync(path.join(source, 'skills/research-evidence/references/initial-source-register.md'), 'utf8');
  assert.ok(researchSkill.includes(`finite ${names.length}-family map`));
  assert.ok(sourceRegister.includes(`${names.length} family cards plus a watchlist`));
});
test('image snapshot count drift in either research entrypoint fails validation', () => {
  const mismatches = [
    {
      path: 'skills/research-evidence/SKILL.md',
      from: 'finite 19-family map',
      to: 'finite 17-family map',
    },
    {
      path: 'skills/research-evidence/references/initial-source-register.md',
      from: '19 family cards plus a watchlist',
      to: '17 family cards plus a watchlist',
    },
  ];
  for (const mutation of mismatches) {
    const f = fixture();
    try {
      const filename = path.join(f.root, mutation.path);
      const original = fs.readFileSync(filename, 'utf8');
      fs.writeFileSync(filename, original.replace(mutation.from, mutation.to));
      assert.ok(validatePackage(f.root).errors.includes(`Image snapshot count mismatch: ${mutation.path}`));
    } finally { f.close(); }
  }
});
test('named image-model mapping remains planned, version-specific, evidence-bounded, and non-executing', () => {
  const cases = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8')).cases;
  const item = cases.find(fixture => fixture.id === 'S53');
  assert.ok(item);
  assert.equal(item.status, 'planned');
  assert.equal(item.research_expectation, 'required');
  assert.equal(item.context.requested_version, '3.0');
  assert.equal(item.context.requested_surface, 'not_named; consumer-facing product is the default');
  assert.equal(item.tool_state.external_provider_authorized, false);
  assert.equal(item.tool_state.image_generation, 'not_available');
  assert.equal(item.tool_state.uploads_authorized, false);

  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases.find(testCase => testCase.id === 'S53').tool_state.external_provider_authorized = true;
    fs.writeFileSync(filename, JSON.stringify(data, null, 2) + '\n');
    assert.ok(validatePackage(f.root).errors.includes('S53 must not authorize provider calls, uploads, or generation'));
  } finally { f.close(); }
});
test('commercial campaign fixtures cover routing, truth, research and anti-generic gates without declaring behavior PASS', () => {
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/campaign-cases.json'), 'utf8'));
  assert.deepEqual(data.cases.map(item => item.id), Array.from({length: 10}, (_, index) => 'M' + String(index + 1).padStart(2, '0')));
  assert.ok(data.cases.every(item => item.status === 'planned'));
  assert.equal(data.cases.find(item => item.id === 'M01').context.asset_family_requested, true);
  assert.equal(data.cases.find(item => item.id === 'M06').context.current_specification_requested, true);
  assert.equal(data.cases.find(item => item.id === 'M07').research_expectation, 'prohibited_by_user');
  assert.equal(data.cases.find(item => item.id === 'M08').expected_branch, 'route_to_music_video_direction_without_commercial_misroute');
  assert.ok(data.cases.find(item => item.id === 'M08').checks.includes('Routes the song-centered brief to the dedicated music-video direction owner'));
  assert.ok(data.cases.find(item => item.id === 'M02').checks.includes('Does not promise or imply viral reach or sales performance'));
  assert.ok(data.cases.find(item => item.id === 'M10').checks.includes('Repairs one primary issue and names an observable retest before a final handoff'));
  assert.ok(data.cases.find(item => item.id === 'M10').checks.includes('Withholds final direction and handoff until all material gate items pass'));
});
test('campaign direction has exactly one orchestrator route', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'skills/workflow-orchestrator/SKILL.md');
    const text = fs.readFileSync(filename, 'utf8');
    const target = '[commercial-video-campaign-director](../commercial-video-campaign-director/SKILL.md)';
    const route = text.split(/\r?\n/).find(line => line.startsWith('|') && line.includes(target));
    assert.ok(route, 'fixture must contain the canonical campaign route row');

    fs.writeFileSync(filename, text.replace(route + '\n', ''));
    assert.ok(validatePackage(f.root).errors.includes('Commercial video campaign direction must have exactly one orchestrator route; found 0'));

    fs.writeFileSync(filename, text.replace(route, route + '\n' + route));
    assert.ok(validatePackage(f.root).errors.includes('Commercial video campaign direction must have exactly one orchestrator route; found 2'));
  } finally { f.close(); }
});
test('music-video direction has exactly one orchestrator route', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'skills/workflow-orchestrator/SKILL.md');
    const text = fs.readFileSync(filename, 'utf8');
    const target = '[creative-music-video-director](../creative-music-video-director/SKILL.md)';
    const route = text.split(/\r?\n/).find(line => line.startsWith('|') && line.includes(target));
    assert.ok(route, 'fixture must contain the canonical music-video route row');

    fs.writeFileSync(filename, text.replace(route + '\n', ''));
    assert.ok(validatePackage(f.root).errors.includes('Music-video direction must have exactly one orchestrator route; found 0'));

    fs.writeFileSync(filename, text.replace(route, route + '\n' + route));
    assert.ok(validatePackage(f.root).errors.includes('Music-video direction must have exactly one orchestrator route; found 2'));
  } finally { f.close(); }
});
test('music-video cases protect evidence, sustained form, handoffs and focused revision', () => {
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/video-cases.json'), 'utf8'));
  const cases = data.cases.filter(item => item.id.startsWith('MV'));
  assert.deepEqual(cases.map(item => item.id), ['MV01', 'MV02', 'MV03', 'MV04']);
  assert.ok(cases.every(item => item.status === 'planned' && item.research_expectation === 'required'));
  const byId = Object.fromEntries(cases.map(item => [item.id, item]));
  assert.equal(byId.MV01.tool_state.web_search, 'available_read_only');
  assert.ok(byId.MV01.checks.includes('Does not claim to have listened to or analysed unattached audio'));
  assert.ok(byId.MV02.checks.includes('Preserves the user\'s deliberate sustained or hypnotic form'));
  assert.ok(byId.MV03.checks.includes('Routes song/persona direction before requested sequence and generator-aware prompting'));
  assert.ok(byId.MV04.checks.includes('Preserves explicit accepted persona/reference locks'));
});
test('producer cases cover task preparation, currentness, missing input, provider boundary and owner routing', () => {
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/producer-cases.json'), 'utf8'));
  assert.deepEqual(data.cases.map(item => item.id), ['PA01', 'PA02', 'PA03', 'PA04', 'PA05', 'PA06', 'PA07']);
  assert.ok(data.cases.every(item => item.status === 'planned'));
  assert.equal(data.cases.filter(item => item.research_expectation === 'required').length, 5);
  assert.equal(data.cases.filter(item => item.research_expectation === 'not_applicable').length, 1);
  assert.equal(data.cases.filter(item => item.research_expectation === 'prohibited_by_user').length, 1);
  const byId = Object.fromEntries(data.cases.map(item => [item.id, item]));
  assert.equal(byId.PA02.context.current_model_id, 'unknown until verified');
  assert.equal(byId.PA03.research_exemption_reason, 'missing_required_input');
  assert.equal(byId.PA04.tool_state.web_search, 'prohibited_by_user');
  assert.equal(byId.PA05.tool_state.external_provider_authorized, false);
  assert.equal(byId.PA05.tool_state.uploads_authorized, false);
  assert.equal(byId.PA06.context.requested_artifact, 'music-video direction only');
  assert.ok(byId.PA07.checks.includes('Preserves the user-approved lyric wording verbatim in its own labeled block'));
  assert.ok(byId.PA07.checks.includes('Treats user-declared lyric authorship as supplied context rather than legal clearance and does not invent rights or consent'));
  assert.ok(byId.PA07.checks.includes('Distinguishes visible singing from exact phoneme-level synchronization and does not promise exact lip sync'));
  assert.equal(byId.PA07.context.exact_sync_requirement, 'hard_requirement');
  assert.equal(byId.PA07.context.exact_sync_capability, 'unknown_not_verified');
  assert.ok(byId.PA07.expected_branch.includes('block_exact_sync_prompt_until_matching_capability_is_verified'));
  assert.ok(byId.PA07.checks.includes('Withholds an exact-sync prompt until a matching capability is verified and offers a best-effort alternative only after the user accepts a downgrade'));
  assert.ok(byId.PA07.checks.includes('Does not claim to have analysed audio/video when no result is attached and no analysis capability is available'));
  assert.ok(byId.PA07.checks.includes('Provides one bounded repair change and one retest for a future actual render without diagnosing an absent output'));
});
test('producer task preparation has exactly one orchestrator route', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'skills/workflow-orchestrator/SKILL.md');
    const text = fs.readFileSync(filename, 'utf8');
    const target = '[producer-ai-task-builder](../producer-ai-task-builder/SKILL.md)';
    const route = text.split(/\r?\n/).find(line => line.startsWith('|') && line.includes(target));
    assert.ok(route, 'fixture must contain the canonical producer-task route row');
    fs.writeFileSync(filename, text.replace(route + '\n', ''));
    assert.ok(validatePackage(f.root).errors.includes('Producer task preparation must have exactly one orchestrator route; found 0'));
    fs.writeFileSync(filename, text.replace(route, route + '\n' + route));
    assert.ok(validatePackage(f.root).errors.includes('Producer task preparation must have exactly one orchestrator route; found 2'));
  } finally { f.close(); }
});
test('producer validator rejects missing coverage, weakened evidence/sync/repair checks, and generation or provider authorization', () => {
  const mutations = [
    data => { data.cases = data.cases.filter(item => item.id !== 'PA06'); },
    data => { data.cases.find(item => item.id === 'PA02').checks = data.cases.find(item => item.id === 'PA02').checks.filter(check => !check.includes('exact video model unknown')); },
    data => { data.cases.find(item => item.id === 'PA05').tool_state.external_provider_authorized = true; },
    data => { data.cases.find(item => item.id === 'PA05').tool_state.video_generation = 'available'; },
    data => { data.cases.find(item => item.id === 'PA05').tool_state.audio_analysis = 'available'; },
    data => { data.cases.find(item => item.id === 'PA07').checks = data.cases.find(item => item.id === 'PA07').checks.filter(check => !check.includes('exact phoneme-level synchronization')); },
    data => { data.cases.find(item => item.id === 'PA07').checks = data.cases.find(item => item.id === 'PA07').checks.filter(check => !check.includes('bounded repair change')); },
    data => { data.cases.find(item => item.id === 'PA07').checks = data.cases.find(item => item.id === 'PA07').checks.filter(check => !check.includes('wording verbatim')); },
    data => { data.cases.find(item => item.id === 'PA07').checks = data.cases.find(item => item.id === 'PA07').checks.filter(check => !check.includes('rather than legal clearance')); },
    data => { data.cases.find(item => item.id === 'PA07').checks = data.cases.find(item => item.id === 'PA07').checks.filter(check => !check.includes('no result is attached')); },
    data => { data.cases.find(item => item.id === 'PA07').checks = data.cases.find(item => item.id === 'PA07').checks.filter(check => !check.includes('Withholds an exact-sync prompt')); },
    data => { data.cases.find(item => item.id === 'PA07').context.exact_sync_requirement = 'best_effort'; },
    data => { data.cases.find(item => item.id === 'PA07').context.exact_sync_capability = 'verified_available'; },
    data => { data.cases.find(item => item.id === 'PA07').expected_branch = 'provide_best_effort_prompt_by_default'; },
  ];
  const expected = [
    'Producer task fixtures must contain exactly PA01-PA07',
    'Producer fixture missing required check: PA02 -> Marks the exact video model unknown if official current evidence does not resolve it',
    'Producer fixture must not authorize an external provider: PA05',
    'Producer fixture cannot claim video-generation availability: PA05',
    'Producer fixture cannot claim audio-analysis availability: PA05',
    'Producer fixture missing required check: PA07 -> Distinguishes visible singing from exact phoneme-level synchronization and does not promise exact lip sync',
    'Producer fixture missing required check: PA07 -> Provides one bounded repair change and one retest for a future actual render without diagnosing an absent output',
    'Producer fixture missing required check: PA07 -> Preserves the user-approved lyric wording verbatim in its own labeled block',
    'Producer fixture missing required check: PA07 -> Treats user-declared lyric authorship as supplied context rather than legal clearance and does not invent rights or consent',
    'Producer fixture missing required check: PA07 -> Does not claim to have analysed audio/video when no result is attached and no analysis capability is available',
    'Producer fixture missing required check: PA07 -> Withholds an exact-sync prompt until a matching capability is verified and offers a best-effort alternative only after the user accepts a downgrade',
    'Producer PA07 must preserve exact synchronization as a hard requirement when requested',
    'Producer PA07 must not treat the unverified exact-sync capability as available',
    'Producer PA07 must block exact-sync prompt until its required capability is verified',
  ];
  for (let i = 0; i < mutations.length; i++) {
    const f = fixture();
    try {
      const filename = path.join(f.root, 'evals/producer-cases.json');
      const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
      mutations[i](data);
      fs.writeFileSync(filename, JSON.stringify(data, null, 2) + '\n');
      assert.ok(validatePackage(f.root).errors.includes(expected[i]));
    } finally { f.close(); }
  }
});
test('validator rejects missing music-video direction evaluation coverage', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/video-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases = data.cases.filter(item => item.id !== 'MV04');
    fs.writeFileSync(filename, JSON.stringify(data, null, 2) + '\n');
    assert.ok(validatePackage(f.root).errors.includes('Music-video direction fixtures must contain MV01-MV04'));
  } finally { f.close(); }
});
test('validator rejects a music-video fixture with a weakened required acceptance check', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/video-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const item = data.cases.find(entry => entry.id === 'MV04');
    item.checks = item.checks.filter(check => check !== 'Preserves explicit accepted persona/reference locks');
    fs.writeFileSync(filename, JSON.stringify(data, null, 2) + '\n');
    assert.ok(validatePackage(f.root).errors.includes('Music-video fixture missing required check: MV04 -> Preserves explicit accepted persona/reference locks'));
  } finally { f.close(); }
});
test('campaign fixtures guard against viral promises and premature handoff after anti-generic failure', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/campaign-cases.json');
    const originalText = fs.readFileSync(filename, 'utf8');
    const requirements = [
      {id: 'M02', check: 'Does not promise or imply viral reach or sales performance', error: 'Campaign M02 must explicitly guard against viral reach and sales performance promises'},
      {id: 'M08', check: 'Routes the song-centered brief to the dedicated music-video direction owner', error: 'Campaign M08 must route a song-centered video to the dedicated music-video owner'},
      {id: 'M10', check: 'Repairs one primary issue and names an observable retest before a final handoff', error: 'Campaign M10 must require one primary repair and an observable retest'},
      {id: 'M10', check: 'Withholds final direction and handoff until all material gate items pass', error: 'Campaign M10 must withhold final direction and handoff until material gates pass'},
    ];
    for (const requirement of requirements) {
      const data = JSON.parse(originalText);
      const item = data.cases.find(entry => entry.id === requirement.id);
      item.checks = item.checks.filter(check => check !== requirement.check);
      fs.writeFileSync(filename, JSON.stringify(data, null, 2) + '\n');
      assert.ok(validatePackage(f.root).errors.includes(requirement.error), requirement.id + ': ' + requirement.error);
    }
  } finally { f.close(); }
});
test('rejects a planned fixture that omits or misclassifies research expectation', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    delete data.cases.find(item => item.id === 'S02').research_expectation;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing or invalid research expectation: S02.research_expectation')));
  } finally { f.close(); }
});
test('rejects campaign fixture coverage missing an anti-generic dimension', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/campaign-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    for (const item of data.cases) {
      if (item.dimensions) item.dimensions = item.dimensions.filter(dimension => dimension !== 'anti_generic_rework');
    }
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing campaign fixture coverage: anti_generic_rework')));
  } finally { f.close(); }
});
test('rejects campaign fixture that claims completed behavior', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/campaign-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases.find(item => item.id === 'M01').status = 'PASS';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Campaign fixture must not predeclare behavior PASS: M01')));
  } finally { f.close(); }
});
test('rejects a direct entrypoint that keeps the link but weakens research to optional', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'skills/image-prompt-architect/SKILL.md');
    const text = fs.readFileSync(filename, 'utf8');
    const weakened = text.replace('Run the mandatory [public research preflight]', 'Run the [public research preflight]');
    assert.notEqual(weakened, text, 'fixture must target the current mandatory wording');
    fs.writeFileSync(filename, weakened);
    assert.ok(fs.readFileSync(filename, 'utf8').includes('../research-evidence/SKILL.md'), 'link should remain present');
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Research preflight route must be marked mandatory: image-prompt-architect')));
  } finally { f.close(); }
});
test('rejects a creative entrypoint that bypasses mandatory research routing', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'skills/image-prompt-architect/SKILL.md');
    const text = fs.readFileSync(filename, 'utf8').replace('../research-evidence/SKILL.md', '../missing/SKILL.md');
    fs.writeFileSync(filename, text);
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing mandatory research preflight route: image-prompt-architect')));
  } finally { f.close(); }
});
test('detects identity drift between manifests', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'plugin.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.version = '9.9.9';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('identity mismatch')));
  } finally { f.close(); }
});
test('detects missing reference', () => {
  const f = fixture();
  try {
    fs.renameSync(path.join(f.root, 'skills/humanizer/references/copy-and-voice.md'), path.join(f.root, 'missing-copy.md'));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Broken link')));
  } finally { f.close(); }
});
test('detects unresolved local Markdown fragments', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'skills/commercial-visual-campaign-director/SKILL.md');
    fs.appendFileSync(filename, '\n[missing section](references/direction-and-composition.md#not-a-real-section)\n');
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Broken link fragment: skills/commercial-visual-campaign-director/SKILL.md -> references/direction-and-composition.md#not-a-real-section')));
  } finally { f.close(); }
});
test('detects unresolved same-file Markdown fragments', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'README.md');
    fs.appendFileSync(filename, '\n[missing section](#not-a-real-heading)\n');
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Broken link fragment: README.md -> #not-a-real-heading')));
  } finally { f.close(); }
});
test('detects resource links outside package', () => {
  const f = fixture();
  try {
    fs.appendFileSync(path.join(f.root, 'README.md'), '\n[escape](../../outside.md)\n');
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('escapes package')));
  } finally { f.close(); }
});
test('detects unplanned external integration', () => {
  const f = fixture();
  try {
    fs.writeFileSync(path.join(f.root, '.mcp.json'), '{}');
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('external integration')));
  } finally { f.close(); }
});
test('detects fake executed status in planned fixtures', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases[0].status = 'PASS';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('predeclare')));
  } finally { f.close(); }
});
test('detects a fixture without supplied context', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    delete data.cases.find(item => item.id === 'S12').context;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing eval context/state: S12.context')));
  } finally { f.close(); }
});
test('detects a fixture without an expected decision branch', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    delete data.cases.find(item => item.id === 'S17').expected_branch;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing eval expected branch: S17')));
  } finally { f.close(); }
});
test('detects mismatch in portable OpenAI presentation metadata', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'plugin.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.extensions['com.openai'].interface.shortDescription = 'Different portable copy';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('OpenAI interface differs')));
  } finally { f.close(); }
});
test('detects an unexecuted video fixture falsely marked PASS', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/video-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases[0].status = 'PASS';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Video fixture must not predeclare behavior PASS')));
  } finally { f.close(); }
});
test('requires focused video anti-slop correction-loop fixtures', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/video-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases = data.cases.filter(item => !['V14', 'V15'].includes(item.id));
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('anti-slop correction-loop')));
  } finally { f.close(); }
});
test('requires the static pre-prompt anti-slop fixture matrix', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const required = new Map([
    ['S13', 'pass'],
    ['S27', 'rework'],
    ['S28', 'rework'],
    ['S29', 'rework'],
    ['S30', 'pass'],
    ['S31', 'pass'],
    ['S32', 'blocked'],
  ]);
  for (const [id, decision] of required) {
    const item = data.cases.find(testCase => testCase.id === id);
    assert.ok(item, 'missing static anti-slop fixture ' + id);
    assert.equal(item.status, 'planned', id);
    assert.equal(item.anti_slop_gate?.decision, decision, id);
    assert.equal(item.anti_slop_gate?.final_prompt_permitted, decision === 'pass', id);
  }
});
test('requires planned concept selection, adaptation, and conflict fixtures', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const required = new Map([
    ['S33', ['needs_selection', 'request_one_route_selection']],
    ['S34', ['locked', 'adapt_layout_within_locked_mechanism']],
    ['S35', ['locked', 'ask_one_format_constraint_tradeoff']],
  ]);
  for (const [id, [status, action]] of required) {
    const item = data.cases.find(testCase => testCase.id === id);
    assert.ok(item, 'missing concept-state fixture ' + id);
    assert.equal(item.status, 'planned', id);
    assert.equal(item.context?.concept_state?.status, status, id);
    assert.equal(item.concept_action, action, id);
  }
});
test('rejects malformed concept-state fixture and does not accept a false lock', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases.find(item => item.id === 'S34').context.concept_state.status = 'needs_selection';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Unexpected concept-state status: S34')));
  } finally { f.close(); }
});
test('requires planned business-card and civic-source-truth profile fixtures', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const card = data.cases.find(item => item.id === 'S36');
  assert.equal(card?.status, 'planned');
  assert.equal(card?.research_expectation, 'required');
  assert.equal(card?.context?.deliverable_profile, 'business_membership_card');
  assert.equal(card?.context?.production_intent, 'concept_raster_only');
  assert.equal(card?.profile_action, 'create_card_concept_without_print_claim');
  const civic = data.cases.find(item => item.id === 'S37');
  assert.equal(civic?.status, 'planned');
  assert.equal(civic?.research_expectation, 'required');
  assert.equal(civic?.context?.deliverable_profile, 'civic_social_political');
  assert.equal(civic?.source_gate?.decision, 'blocked');
  assert.equal(civic?.source_gate?.final_prompt_permitted, false);
  assert.equal(civic?.expected_branch, 'request_claim_source_and_speaker_before_final_prompt');
});
test('requires the planned staged identity-view validation fixture', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const item = data.cases.find(testCase => testCase.id === 'S38');
  assert.equal(item?.status, 'planned');
  assert.equal(item?.research_expectation, 'not_applicable');
  assert.equal(item?.research_exemption_reason, 'missing_continuity_carrier');
  assert.equal(item?.identity_validation?.source_status, 'user_designated_master_not_attached');
  assert.equal(item?.identity_validation?.candidate_status, 'user_reported_drift_not_visually_reviewed');
  assert.equal(item?.identity_validation?.initial_major_change_axis_limit, 1);
  assert.equal(item?.identity_validation?.anchor_promotion_requires, 'actual_render_visually_reviewed_and_accepted_for_stated_use');
  assert.equal(item?.identity_validation?.failed_view_action, 'return_to_last_accepted_master');
  assert.equal(item?.expected_branch, 'plan_staged_validation_and_request_identity_assets_before_final_pack');
});
test('rejects identity fixture that promotes the unreviewed profile or weakens the staged gate', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const item = data.cases.find(testCase => testCase.id === 'S38');
    item.identity_validation.anchor_promotion_requires = 'trust_user_description';
    item.identity_validation.failed_view_action = 'use_drifted_profile_as_master';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Identity fixture must withhold the unreviewed profile and preserve staged validation: S38')));
  } finally { f.close(); }
});
test('requires the planned camera-reframing conflict fixture and its evidence limits', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const item = data.cases.find(testCase => testCase.id === 'S39');
  assert.equal(item?.status, 'planned');
  assert.equal(item?.research_exemption_reason, 'missing_required_input');
  assert.equal(item?.context?.source_image_attached, false);
  assert.equal(item?.context?.requested_camera_change?.axis, 'viewpoint_angle');
  assert.equal(item?.context?.user_requested_pixel_identical_background, true);
  assert.equal(item?.context?.newly_visible_surface_evidence, 'unknown; no source image or alternate view is available');
  assert.equal(item?.reframing_contract?.camera_change_kind, 'viewpoint_change_not_crop');
  assert.equal(item?.reframing_contract?.pixel_identical_background_guaranteed_by_prompt, false);
  assert.equal(item?.reframing_contract?.unknown_surface_may_be_invented_as_fact, false);
  assert.equal(item?.reframing_contract?.final_prompt_permitted, false);
  assert.equal(item?.expected_branch, 'surface_viewpoint_and_pixel_continuity_conflict_then_request_source_or_bounded_alternative');
});
test('rejects a reframe fixture that promises pixel identity or invents a hidden surface', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const item = data.cases.find(testCase => testCase.id === 'S39');
    item.reframing_contract.pixel_identical_background_guaranteed_by_prompt = true;
    item.reframing_contract.unknown_surface_may_be_invented_as_fact = true;
    item.reframing_contract.final_prompt_permitted = true;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Camera-reframing fixture must surface unknown geometry and withhold the source-bound prompt: S39')));
  } finally { f.close(); }
});
test('requires planned independent still-series fixture with standalone prompts and approximate continuity', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const item = data.cases.find(testCase => testCase.id === 'S40');
  assert.equal(item?.status, 'planned');
  assert.equal(item?.research_expectation, 'required');
  assert.equal(item?.context?.requested_artifact, 'three_separate_still_image_files');
  assert.equal(item?.series_contract?.output_count, 3);
  assert.deepEqual(item?.series_contract?.roles, ['hero', 'product_detail', 'in_use_editorial']);
  assert.equal(item?.series_contract?.coverage_or_progression, 'coverage');
  assert.equal(item?.series_contract?.standalone_prompt_count, 3);
  assert.equal(item?.series_contract?.each_prompt_self_contained, true);
  assert.deepEqual(item?.series_contract?.attached_reference_count_per_unit, [0, 0, 0]);
  assert.equal(item?.series_contract?.strict_continuity_claim, false);
  assert.equal(item?.expected_branch, 'produce_three_standalone_approximate_continuity_prompts');
});
test('rejects a series fixture that collapses separate outputs into a board or changes the requested count', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const series = data.cases.find(item => item.id === 'S40').series_contract;
    series.grid_or_board = true;
    series.output_count = 4;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Independent still-series fixture must preserve exact separate outputs, distinct roles, standalone prompts, and honest continuity: S40')));
  } finally { f.close(); }
});
test('rejects a series fixture that reuses prior prompts or overstates strict continuity', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const series = data.cases.find(item => item.id === 'S40').series_contract;
    series.each_prompt_self_contained = false;
    series.prompt_may_depend_on_prior_unit = true;
    series.strict_continuity_claim = true;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Independent still-series fixture must preserve exact separate outputs, distinct roles, standalone prompts, and honest continuity: S40')));
  } finally { f.close(); }
});
test('rejects a series fixture without distinct variation and anti-duplicate intent', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const series = data.cases.find(item => item.id === 'S40').series_contract;
    series.allowed_variation = [];
    series.anti_duplicate_required = false;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Independent still-series fixture must preserve exact separate outputs, distinct roles, standalone prompts, and honest continuity: S40')));
  } finally { f.close(); }
});
test('requires planned positive and conflict fixtures for bounded background replacement', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const positive = data.cases.find(item => item.id === 'S41');
  const conflict = data.cases.find(item => item.id === 'S42');
  assert.equal(positive?.status, 'planned');
  assert.equal(positive?.background_replacement_contract?.final_prompt_permitted, true);
  assert.ok(positive?.background_replacement_contract?.preserve_exactly.includes('focus'));
  assert.ok(positive?.background_replacement_contract?.allowed_secondary_changes.includes('new_environment_reflections_and_transmission'));
  assert.equal(positive?.context?.source_image_status, 'synthetic_asset_supplied_in_fixture_scenario_only_not_reviewed_in_this_execution');
  assert.equal(conflict?.status, 'planned');
  assert.equal(conflict?.background_replacement_contract?.contradictory_lock, true);
  assert.equal(conflict?.background_replacement_contract?.final_prompt_permitted, false);
  assert.equal(conflict?.background_replacement_contract?.next_action, 'ask_one_tradeoff_or_offer_keep_original_environment');
  assert.equal(conflict?.expected_branch, 'ask_one_tradeoff_before_final_background_replacement_prompt');
});
test('rejects background-replacement fixtures that widen secondary effects or drop protected focus', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const positive = data.cases.find(item => item.id === 'S41').background_replacement_contract;
    positive.preserve_exactly = positive.preserve_exactly.filter(item => item !== 'focus');
    positive.allowed_secondary_changes.push('product_geometry');
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Background-replacement fixture must preserve source truth and narrowly bound physical secondary changes: S41')));
  } finally { f.close(); }
});
test('rejects a contradictory background fixture that permits final prompt release', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const conflict = data.cases.find(item => item.id === 'S42').background_replacement_contract;
    conflict.final_prompt_permitted = true;
    conflict.next_action = 'compile_prompt_and_preserve_old_pixels';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Conflicting background locks must block the final prompt until the user resolves a bounded trade-off: S42')));
  } finally { f.close(); }
});
test('requires a planned sequential separate-asset fixture with exact selection and no-output guards', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const item = data.cases.find(entry => entry.id === 'S43');
  assert.equal(item?.status, 'planned');
  assert.equal(item?.research_expectation, 'required');
  assert.equal(item?.separate_asset_review_contract?.selected_version_while_candidate_pending, 'background-v001');
  assert.equal(item?.separate_asset_review_contract?.pending_candidate_version, 'background-v002');
  assert.equal(item?.separate_asset_review_contract?.actual_image_returned, false);
  assert.equal(item?.separate_asset_review_contract?.ask_keep_or_change_before_actual_image, false);
  assert.equal(item?.separate_asset_review_contract?.advance_to_next_asset, false);
  assert.equal(item?.tool_state?.image_generation, 'not_available');
  assert.equal(item?.expected_branch, 'hold_current_asset_without_fabricating_output_or_advancing');
});
test('rejects missing or weakened sequential separate-asset fixture guards', () => {
  const mutations = [
    {
      label: 'missing S43',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S43'); },
      error: 'Missing sequential separate-asset review fixture: S43',
    },
    {
      label: 'promotes the pending candidate over the previously accepted version',
      apply: data => { data.cases.find(item => item.id === 'S43').separate_asset_review_contract.selected_version_while_candidate_pending = 'background-v002'; },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'asks for image acceptance before an actual image exists',
      apply: data => { data.cases.find(item => item.id === 'S43').separate_asset_review_contract.ask_keep_or_change_before_actual_image = true; },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'misclassifies required research',
      apply: data => {
        const item = data.cases.find(entry => entry.id === 'S43');
        item.research_expectation = 'not_applicable';
        item.research_exemption_reason = 'test mutation';
      },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'authorizes an unexecuted external provider',
      apply: data => { data.cases.find(item => item.id === 'S43').tool_state.external_provider_authorized = true; },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'enables unavailable image generation',
      apply: data => { data.cases.find(item => item.id === 'S43').tool_state.image_generation = 'available'; },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'removes read-only web-search availability state',
      apply: data => { data.cases.find(item => item.id === 'S43').tool_state.web_search = 'not_available'; },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'authorizes uploads outside the no-upload harness',
      apply: data => { data.cases.find(item => item.id === 'S43').tool_state.uploads_authorized = true; },
      error: 'Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43',
    },
    {
      label: 'falsely declares behavior PASS',
      apply: data => { data.cases.find(item => item.id === 'S43').status = 'PASS'; },
      error: 'Fixture must not predeclare behavior PASS: S43',
    },
  ];
  for (const mutation of mutations) {
    const f = fixture();
    try {
      const filename = path.join(f.root, 'evals/static-cases.json');
      const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
      mutation.apply(data);
      fs.writeFileSync(filename, JSON.stringify(data));
      assert.ok(validatePackage(f.root).errors.includes(mutation.error), mutation.label);
    } finally { f.close(); }
  }
});
test('requires two planned approved-dependency reassessment fixtures with user decision and preservation boundaries', () => {
  assert.deepEqual(validatePackage(source).errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const ids = ['S48', 'S49'];
  const byId = Object.fromEntries(data.cases.filter(item => ids.includes(item.id)).map(item => [item.id, item]));
  assert.deepEqual(Object.keys(byId).sort(), ids);
  for (const id of ids) {
    assert.equal(byId[id].status, 'planned');
    assert.equal(byId[id].research_expectation, 'required');
    assert.equal(byId[id].dependency_reassessment_contract.dependency_is_edit_permission, false);
    assert.equal(byId[id].dependency_reassessment_contract.ask_or_obtain_explicit_decision_before_dependent_candidate, true);
    assert.equal(byId[id].dependency_reassessment_contract.automatic_dependent_edit, false);
    assert.equal(byId[id].dependency_reassessment_contract.relationship_assessed, false);
    assert.equal(byId[id].tool_state.image_generation, 'not_available');
    assert.deepEqual(byId[id].available_assets, []);
  }
  assert.equal(byId.S48.dependency_reassessment_contract.dependent_selected_version_while_pending, 'shadow-v001');
  assert.deepEqual(byId.S48.dependency_reassessment_contract.preserve_independent_asset_ids, ['poster_background']);
  assert.equal(byId.S48.context.selected_versions.poster_background, 'background-v001');
  assert.equal(byId.S49.dependency_reassessment_contract.dependent_selected_version_while_pending, 'reflection-v001');
  assert.deepEqual(byId.S49.dependency_reassessment_contract.preserve_independent_asset_ids, ['poster_title']);
  assert.equal(byId.S49.context.selected_versions.poster_title, 'title-v003');
});
test('rejects weakened approved-dependency permission, request, relationship, and preservation guards', () => {
  const mutations = [
    {
      label: 'missing S48 figure-to-shadow reassessment case',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S48'); },
      id: 'S48',
      error: 'Missing approved-dependent-asset reassessment fixture: S48',
    },
    {
      label: 'drops the figure-to-shadow dependency edge',
      apply: data => { data.cases.find(item => item.id === 'S48').context.dependency_edges = []; },
      id: 'S48',
    },
    {
      label: 'contradicts the no-shadow-edit user instruction',
      apply: data => { data.cases.find(item => item.id === 'S48').user_request = 'Pracujemy na jawnie oddzielonych assetach. Zmień poster_figure oraz shadow_v001 automatycznie, bez pytania i bez osobnego uzgodnienia. Zachowaj background_v001. Przygotuj kierunek bez promptu.'; },
      id: 'S48',
    },
    {
      label: 'rejects added explicit shadow consent that contradicts the retained no-consent phrase',
      apply: data => { data.cases.find(item => item.id === 'S48').user_request += ' Wyrażam zgodę na zmianę shadow-v001 bez dalszego uzgodnienia.'; },
      id: 'S48',
    },
    {
      label: 'treats dependency as permission for an automatic shadow edit',
      apply: data => { data.cases.find(item => item.id === 'S48').dependency_reassessment_contract.automatic_dependent_edit = true; },
      id: 'S48',
    },
    {
      label: 'drops the independent approved background preservation',
      apply: data => { data.cases.find(item => item.id === 'S48').dependency_reassessment_contract.preserve_independent_asset_ids = []; },
      id: 'S48',
    },
    {
      label: 'does not preserve the exact selected independent background version',
      apply: data => { data.cases.find(item => item.id === 'S48').context.selected_versions.poster_background = 'background-v002'; },
      id: 'S48',
    },
    {
      label: 'missing S49 background-to-reflection reassessment case',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S49'); },
      id: 'S49',
      error: 'Missing approved-dependent-asset reassessment fixture: S49',
    },
    {
      label: 'changes the user request to authorize a reflection edit while contract remains unapproved',
      apply: data => { data.cases.find(item => item.id === 'S49').user_request = 'To osobne warstwy. Zmień poster_background i automatycznie zmień floor_reflection_v001 bez pytania. Zachowaj tytuł. Kierunek bez promptu.'; },
      id: 'S49',
    },
    {
      label: 'rejects added explicit reflection consent that contradicts the retained prior-approval request',
      apply: data => { data.cases.find(item => item.id === 'S49').user_request += ' Wyrażam zgodę na zmianę floor_reflection_v001 bez dalszego uzgodnienia.'; },
      id: 'S49',
    },
    {
      label: 'promotes an unapproved reflection version',
      apply: data => { data.cases.find(item => item.id === 'S49').context.selected_versions.floor_reflection = 'reflection-v002'; },
      id: 'S49',
    },
    {
      label: 'does not preserve the exact selected independent title version',
      apply: data => { data.cases.find(item => item.id === 'S49').context.selected_versions.poster_title = 'title-v004'; },
      id: 'S49',
    },
    {
      label: 'claims the unavailable background-reflection relationship was assessed',
      apply: data => { data.cases.find(item => item.id === 'S49').dependency_reassessment_contract.relationship_assessed = true; },
      id: 'S49',
    },
  ];
  for (const mutation of mutations) {
    const f = fixture();
    try {
      const filename = path.join(f.root, 'evals/static-cases.json');
      const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
      mutation.apply(data);
      fs.writeFileSync(filename, JSON.stringify(data));
      const expectedError = mutation.error ??
        'Approved-dependent-asset fixture must bind request, dependency, approval, preservation and no-edit rules: ' + mutation.id;
      assert.ok(validatePackage(f.root).errors.includes(expectedError), mutation.label);
    } finally { f.close(); }
  }
});
test('requires planned commercial-copy cases for distinct routes, unsupported-claim fallback and exact-copy lock', () => {
  assert.deepEqual(validatePackage(source).errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const ids = ['S50', 'S51', 'S52'];
  const byId = Object.fromEntries(data.cases.filter(item => ids.includes(item.id)).map(item => [item.id, item]));
  assert.deepEqual(Object.keys(byId).sort(), ids);
  assert.ok(ids.every(id => byId[id].status === 'planned'));

  assert.equal(byId.S50.research_expectation, 'required');
  assert.deepEqual(byId.S50.commercial_copy_contract.route_mechanisms, [
    'plain_offer', 'supported_objection_answer', 'tactile_scene',
  ]);
  assert.equal(byId.S50.commercial_copy_contract.candidate_count, 3);
  assert.equal(byId.S50.commercial_copy_contract.selection_status, 'all_unselected_drafts');
  assert.equal(byId.S50.commercial_copy_contract.framework_required, false);
  assert.equal(byId.S50.commercial_copy_contract.unsupported_claims_allowed, false);

  assert.equal(byId.S51.research_expectation, 'required');
  assert.equal(byId.S51.commercial_copy_contract.evidence_available, false);
  assert.equal(byId.S51.commercial_copy_contract.final_copy_permitted, false);
  assert.equal(byId.S51.commercial_copy_contract.final_prompt_permitted, false);
  assert.equal(byId.S51.commercial_copy_contract.invented_replacement_claim_permitted, false);

  assert.equal(byId.S52.research_expectation, 'not_applicable');
  assert.equal(byId.S52.commercial_copy_contract.exact_locked_text, 'Sobota z gliną');
  assert.equal(byId.S52.commercial_copy_contract.may_rewrite, false);
  assert.equal(byId.S52.commercial_copy_contract.alternatives_permitted, false);
});
test('rejects commercial-copy fixture mutations that weaken route, proof or exact-copy boundaries', () => {
  const mutations = [
    {
      label: 'missing distinct-route case S50',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S50'); },
      error: 'Missing commercial-copy strategy and selection fixture: S50',
    },
    {
      label: 'collapses strategic routes into synonym variants',
      apply: data => { data.cases.find(item => item.id === 'S50').commercial_copy_contract.route_mechanisms = ['plain_offer', 'plain_offer', 'plain_offer']; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S50',
    },
    {
      label: 'makes a sales framework compulsory',
      apply: data => { data.cases.find(item => item.id === 'S50').commercial_copy_contract.framework_required = true; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S50',
    },
    {
      label: 'permits unsupported claims',
      apply: data => { data.cases.find(item => item.id === 'S50').commercial_copy_contract.unsupported_claims_allowed = true; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S50',
    },
    {
      label: 'missing unsupported-claim case S51',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S51'); },
      error: 'Missing commercial-copy strategy and selection fixture: S51',
    },
    {
      label: 'claims evidence exists without supplied substantiation',
      apply: data => { data.cases.find(item => item.id === 'S51').commercial_copy_contract.evidence_available = true; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S51',
    },
    {
      label: 'permits final copy before unsupported claims are resolved',
      apply: data => { data.cases.find(item => item.id === 'S51').commercial_copy_contract.final_copy_permitted = true; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S51',
    },
    {
      label: 'missing exact-copy case S52',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S52'); },
      error: 'Missing commercial-copy strategy and selection fixture: S52',
    },
    {
      label: 'rewrites the user-final exact copy',
      apply: data => { data.cases.find(item => item.id === 'S52').commercial_copy_contract.may_rewrite = true; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S52',
    },
    {
      label: 'floods a single locked-line request with alternatives',
      apply: data => { data.cases.find(item => item.id === 'S52').commercial_copy_contract.alternatives_permitted = true; },
      error: 'Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: S52',
    },
  ];
  for (const mutation of mutations) {
    const f = fixture();
    try {
      const filename = path.join(f.root, 'evals/static-cases.json');
      const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
      mutation.apply(data);
      fs.writeFileSync(filename, JSON.stringify(data, null, 2) + '\n');
      assert.ok(validatePackage(f.root).errors.includes(mutation.error), mutation.label);
    } finally { f.close(); }
  }
});
test('requires the four planned ambiguous-label and coherent-hybrid decision fixtures', () => {
  assert.deepEqual(validatePackage(source).errors, []);
  const data = JSON.parse(fs.readFileSync(path.join(source, 'evals/static-cases.json'), 'utf8'));
  const ids = ['S44', 'S45', 'S46', 'S47'];
  const byId = Object.fromEntries(data.cases.filter(item => ids.includes(item.id)).map(item => [item.id, item]));
  assert.deepEqual(Object.keys(byId).sort(), ids);
  assert.ok(ids.every(id => byId[id].status === 'planned' && byId[id].research_expectation === 'required'));
  assert.equal(byId.S44.visual_label_resolution_contract.resolution, 'reversible_assumption');
  assert.equal(byId.S44.visual_label_resolution_contract.question_required, false);
  assert.equal(byId.S44.visual_label_resolution_contract.project_lock_created, false);
  assert.equal(byId.S45.visual_label_resolution_contract.resolution, 'ask_single_material_question');
  assert.equal(byId.S45.visual_label_resolution_contract.final_prompt_permitted, false);
  assert.equal(byId.S46.visual_label_resolution_contract.resolution, 'preserve_coherent_user_requested_hybrid');
  assert.deepEqual(byId.S46.visual_label_resolution_contract.components.map(item => item.role), [
    'organize_title_date_and_event_facts', 'central_image',
  ]);
  assert.equal(byId.S47.visual_label_resolution_contract.resolution, 'ask_one_organizing_question');
  assert.equal(byId.S47.visual_label_resolution_contract.direction_permitted, false);
});
test('rejects missing or weakened visual-label decision fixtures', () => {
  const mutations = [
    {
      label: 'missing reversible-choice fixture S44',
      apply: data => { data.cases = data.cases.filter(item => item.id !== 'S44'); },
      id: 'S44',
      error: 'Missing ambiguous-label and hybrid-resolution fixture: S44',
    },
    {
      label: 'forces a ceremonial question despite an authorized reversible choice',
      apply: data => { data.cases.find(item => item.id === 'S44').visual_label_resolution_contract.question_required = true; },
      id: 'S44',
    },
    {
      label: 'context no longer authorizes a reversible choice',
      apply: data => { data.cases.find(item => item.id === 'S44').context.user_authorized_provisional_interpretation = false; },
      id: 'S44',
    },
    {
      label: 'user request no longer permits an assumption or rules out a prompt',
      apply: data => {
        const item = data.cases.find(entry => entry.id === 'S44');
        item.user_request = item.user_request.replace('Możesz zaproponować roboczą interpretację bez dodatkowych pytań', 'Nie wybieraj kierunku bez wcześniejszego pytania');
      },
      id: 'S44',
    },
    {
      label: 'permits a final direction before material period ambiguity is resolved',
      apply: data => { data.cases.find(item => item.id === 'S45').visual_label_resolution_contract.direction_permitted = true; },
      id: 'S45',
    },
    {
      label: 'permits a final prompt before the period choice',
      apply: data => { data.cases.find(item => item.id === 'S45').visual_label_resolution_contract.final_prompt_permitted = true; },
      id: 'S45',
    },
    {
      label: 'context already selects a period but fixture still requires clarification',
      apply: data => { data.cases.find(item => item.id === 'S45').context.selected_period = '1970s'; },
      id: 'S45',
    },
    {
      label: 'request no longer presents two unselected periods',
      apply: data => {
        const item = data.cases.find(entry => entry.id === 'S45');
        item.user_request = item.user_request.replace('lat 70. albo 90., ale jeszcze nie wybrałem', 'lat 70., które wybrałem');
      },
      id: 'S45',
    },
    {
      label: 'rejects the user-requested hybrid as inherently incompatible',
      apply: data => { data.cases.find(item => item.id === 'S46').visual_label_resolution_contract.hybrid_rejected_as_incompatible = true; },
      id: 'S46',
    },
    {
      label: 'drops the distinct roles in the coherent hybrid',
      apply: data => { data.cases.find(item => item.id === 'S46').visual_label_resolution_contract.components[0].role = 'central_image'; },
      id: 'S46',
    },
    {
      label: 'request no longer contains the linocut image treatment',
      apply: data => {
        const item = data.cases.find(entry => entry.id === 'S46');
        item.user_request = item.user_request.replace('ilustracja wycięta w linoleum', 'fotograficzny packshot');
      },
      id: 'S46',
    },
    {
      label: 'silently resolves an unassigned equal-priority label stack',
      apply: data => { data.cases.find(item => item.id === 'S47').visual_label_resolution_contract.direction_permitted = true; },
      id: 'S47',
    },
    {
      label: 'adds an unsupported fixed style cap',
      apply: data => { data.cases.find(item => item.id === 'S47').visual_label_resolution_contract.fixed_style_cap_added = true; },
      id: 'S47',
    },
    {
      label: 'context assigns roles to the stack while fixture still claims roles are absent',
      apply: data => { data.cases.find(item => item.id === 'S47').context.component_roles = ['primary', 'secondary']; },
      id: 'S47',
    },
    {
      label: 'marks an unexecuted fixture as behavior PASS',
      apply: data => { data.cases.find(item => item.id === 'S44').status = 'PASS'; },
      id: 'S44',
    },
  ];
  for (const mutation of mutations) {
    const f = fixture();
    try {
      const filename = path.join(f.root, 'evals/static-cases.json');
      const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
      mutation.apply(data);
      fs.writeFileSync(filename, JSON.stringify(data));
      const expectedError = mutation.error ?? 'Visual-label fixture must enforce its planned reversible-choice, material-question, or coherent-hybrid contract: ' + mutation.id;
      assert.ok(validatePackage(f.root).errors.includes(expectedError), mutation.label);
    } finally { f.close(); }
  }
});
test('rejects changes to exact business-card copy and anti-invention checks', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const card = data.cases.find(item => item.id === 'S36');
    card.context.approved_copy[3] = '+48 600 000 000';
    card.checks = card.checks.filter(check => !check.includes('Do not invent a logo'));
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Business-card fixture must separate concept raster, exact copy and print production: S36')));
  } finally { f.close(); }
});
test('rejects civic fixture that drops claim-source, speaker, or no-legal-advice guards', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const civic = data.cases.find(item => item.id === 'S37');
    civic.source_gate.missing_evidence = ['authorized speaker or organization'];
    civic.checks = civic.checks.filter(check => !check.includes('legal-compliance'));
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Civic fixture must block an unsupported claim and unknown speaker: S37')));
  } finally { f.close(); }
});
test('rejects final-prompt release for an unsupported civic claim and unknown speaker', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases.find(item => item.id === 'S37').source_gate.final_prompt_permitted = true;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Civic fixture must block an unsupported claim and unknown speaker: S37')));
  } finally { f.close(); }
});
test('rejects missing static anti-slop pre-prompt coverage', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases = data.cases.filter(item => item.id !== 'S27');
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing static anti-slop gate fixture coverage: S27')));
  } finally { f.close(); }
});
test('rejects a static anti-slop rework fixture that permits final prompt release', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/static-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases.find(item => item.id === 'S27').anti_slop_gate.final_prompt_permitted = true;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Static anti-slop gate result conflicts with prompt release: S27')));
  } finally { f.close(); }
});
test('rejects unexecuted screenplay fixture marked as behavior PASS', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/story-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases[0].status = 'PASS';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Story fixture must not predeclare behavior PASS')));
  } finally { f.close(); }
});
test('requires the exact planned SB01-SB15 storyboard fixture set', () => {
  const result = validatePackage(source);
  assert.deepEqual(result.errors, []);
  assert.equal(result.storyboard_fixtures, 15);
});
test('rejects a storyboard fixture falsely marked as behavior PASS', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/storyboard-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases[0].status = 'PASS';
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Storyboard fixture must not predeclare behavior PASS: SB01')));
  } finally { f.close(); }
});
test('rejects missing high-priority storyboard regression coverage', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/storyboard-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    data.cases.find(item => item.id === 'SB13').dimensions = ['continuity'];
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing storyboard fixture coverage: board_not_carrier')));
  } finally { f.close(); }
});
test('rejects storyboard fixture with missing source and tool context', () => {
  const f = fixture();
  try {
    const filename = path.join(f.root, 'evals/storyboard-cases.json');
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    delete data.cases.find(item => item.id === 'SB03').available_assets;
    fs.writeFileSync(filename, JSON.stringify(data));
    assert.ok(validatePackage(f.root).errors.some(e => e.includes('Missing storyboard eval asset inventory: SB03')));
  } finally { f.close(); }
});
