import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateStudio} from '../scripts/validate-studio.mjs';
import {loadEffectiveEvals} from '../scripts/load-effective-evals.mjs';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const currentVersion = JSON.parse(fs.readFileSync(path.join(source, 'plugin.json'), 'utf8')).version;
function fixture(name = currentVersion) {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-canonical-test-')), root = path.join(temp, name);
  fs.cpSync(source, root, {recursive: true});
  return {root, close: () => fs.rmSync(temp, {recursive: true, force: true})};
}
function withFixture(fn, name) { const f = fixture(name); try { return fn(f.root); } finally { f.close(); } }
function edit(root, relative, fn) { const p = path.join(root, relative); fs.writeFileSync(p, fn(fs.readFileSync(p, 'utf8'))); }
function editJson(root, relative, fn) { edit(root, relative, text => { const data = JSON.parse(text); fn(data); return JSON.stringify(data, null, 2) + '\n'; }); }
const codes = result => (result.canonical ?? result).errors.map(item => item.code);

test('skill descriptions stay valid YAML: an unquoted colon or a broken quote fails', () => {
  for (const [value, valid] of [
    ['Make motion graphics from code: kinetic type and titles.', false],
    ['"Make motion graphics from code: kinetic type and titles."', true],
    ["'Brand strategy: it''s quoted.'", true],
    ['"Broken "inner" quote."', false],
    ['Plain text with a # comment.', false],
    ['- starts with a dash', false],
    ['Plain text without indicators, commas allowed.', true],
  ]) withFixture(root => {
    edit(root, 'skills/hyperframes-workflow/SKILL.md', text => text.replace(/^description: .*$/m, 'description: ' + value));
    assert.equal(codes(validateStudio(root)).includes('SKILL_YAML'), !valid, value);
  });
});

test('every reference and template is linked from a skill; a "(moved)" pointer is exempt', () => {
  assert.ok(!codes(validateStudio(source)).includes('REFERENCE_REACH'));
  withFixture(root => {
    fs.writeFileSync(path.join(root, 'skills/ugc/references/unlinked-notes.md'), '# Unlinked notes\n\n' + 'Original guidance that no skill links. '.repeat(20) + '\n');
    assert.ok(codes(validateStudio(root)).includes('REFERENCE_REACH'));
  });
  withFixture(root => {
    edit(root, 'skills/storytelling/SKILL.md', text => text.replace('[short-form structures](references/short-form-structures.md)', 'short-form structures'));
    assert.ok(codes(validateStudio(root)).includes('REFERENCE_REACH'));
  });
  withFixture(root => {
    fs.writeFileSync(path.join(root, 'skills/ugc/references/old-notes.md'), '# Old notes (moved)\n\n' + 'This path stays because hosted updates cannot delete files; read the maintained reference instead. '.repeat(6) + '\n');
    assert.ok(!codes(validateStudio(root)).includes('REFERENCE_REACH'));
  });
});

test('the capability card names real tools and owners and is linked where capabilities are decided', () => {
  const card = JSON.parse(fs.readFileSync(path.join(source, 'skills/workflow-orchestrator/assets/capability-card.json'), 'utf8'));
  const byId = new Map(card.capabilities.map(item => [item.id, item]));
  for (const id of ['motion_render', 'motion_critique', 'motion_sound', 'motion_player']) assert.equal(byId.get(id).executed_by, 'studio', id);
  assert.deepEqual(byId.get('motion_sound').requires, ['python', 'numpy', 'ffmpeg']);
  assert.equal(byId.get('video_generation').executed_by, 'external');
  assert.ok(!codes(validateStudio(source)).includes('CAPABILITY_CARD'));
  const cardPath = 'skills/workflow-orchestrator/assets/capability-card.json';
  for (const [change, label] of [
    [data => { data.capabilities[0].tools = ['skills/hyperframes-workflow/assets/motion-render/missing.py']; }, 'missing tool'],
    [data => { data.capabilities[0].owner = 'imaginary-renderer'; }, 'unknown owner'],
    [data => { data.capabilities[0].requires.push('gpu'); }, 'unknown requirement'],
    [data => { data.capabilities[0].when_missing = ''; }, 'no fallback'],
  ]) withFixture(root => {
    editJson(root, cardPath, change);
    assert.ok(codes(validateStudio(root)).includes('CAPABILITY_CARD'), label);
  });
  withFixture(root => {
    edit(root, 'skills/pipeline-core/references/role-skill-map.md', text => text.replace('(../../workflow-orchestrator/assets/capability-card.json)', ''));
    assert.ok(codes(validateStudio(root)).includes('CAPABILITY_CARD'));
  });
});

test('general motion keeps its stable ID, neutral display name and requirement-led runtime policy', () => {
  const read = relative => fs.readFileSync(path.join(source, relative), 'utf8');
  const motion = read('skills/hyperframes-workflow/SKILL.md');
  assert.match(motion, /name: hyperframes-workflow\n/);
  assert.match(motion, /# Motion Graphics Workflow/);
  const selection = read('skills/hyperframes-workflow/references/code-based-motion-graphics.md');
  assert.match(selection, /does not select HyperFrames or any other engine/);
  assert.match(selection, /Remotion may be recommended/);
  assert.match(selection, /Preserve the user's explicit runtime choice and an established working project/);
  const entry = read('skills/workflow-orchestrator/references/startup-and-creative-menus.md');
  assert.match(entry, /Area `8` selects motion graphics from code, not an engine/);
  assert.doesNotMatch(entry, /owns an explicitly selected React/);
  withFixture(root => {
    edit(root, 'skills/hyperframes-workflow/agents/openai.yaml', text => text.replace('Motion Graphics Workflow', 'HyperFrames Workflow'));
    assert.ok(codes(validateStudio(root)).includes('SKILL_DISPLAY_NAME'));
  });
});

test('canonical validation passes with explicit structural scope and no legacy execution', () => {
  const result = validateStudio(source);
  assert.equal(result.status, 'PASS', JSON.stringify(result.canonical?.errors));
  assert.match(result.canonical.scope, /not host behavior/);
  assert.equal(result.legacy.status, 'NOT_RUN');
  assert.equal(result.canonical.evaluations.executed, 0);
});

test('entry package identity rejects stale, wrong, malformed, absent and duplicate evidence', () => {
  const block = /<!-- BEGIN PACKAGE IDENTITY -->\n[\s\S]*?\n<!-- END PACKAGE IDENTITY -->/;
  for (const mutation of [
    text => text.replace(block, ''),
    text => text.replace(block, value => value + '\n' + value),
    text => text.replace(block, value => value.replace(currentVersion, '0.0.0')),
    text => text.replace(block, value => value.replace('framecore-work-creative-studio', 'another-plugin')),
    text => text.replace(block, value => value.replace('{', '{broken')),
  ]) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', mutation);
    assert.ok(codes(validateStudio(root)).includes('PACKAGE_IDENTITY'));
  });
});

test('version identity must precede startup and preserve truthful source reporting', () => {
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => {
      const block = text.match(/<!-- BEGIN PACKAGE IDENTITY -->\n[\s\S]*?\n<!-- END PACKAGE IDENTITY -->/)[0];
      return text.replace(block, '') + '\n' + block + '\n';
    });
    assert.ok(codes(validateStudio(root)).includes('PACKAGE_IDENTITY_PLACEMENT'));
  });
  for (const phrase of ['plugin-version/installation-status request', 'Reread this entry through the active host', 'saved hosted release', 'current version cannot be confirmed', 'Never report a version from memory']) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replace(phrase, 'removed rule'));
    assert.ok(codes(validateStudio(root)).includes('VERSION_REPORTING_POLICY'));
  });
});

test('missing short descriptions fail for the entry owner and existing specialists', () => {
  for (const owner of ['workflow-orchestrator', 'pipeline-core', 'commercial-video-campaign-director']) withFixture(root => {
    edit(root, 'skills/' + owner + '/agents/openai.yaml', text => text.replace(/^  short_description:.*\n/m, ''));
    assert.ok(codes(validateStudio(root)).includes('SKILL_SHORT_DESCRIPTION'), owner);
  });
});

test('blank, non-string, malformed and duplicate interface descriptions fail closed', () => {
  for (const value of ['""', '"   "', 'null', 'true', '42', '[]', '{}', '"unterminated', '"Invalid \\q escape"']) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/agents/openai.yaml', text => text.replace(/^  short_description:.*$/m, '  short_description: ' + value));
    assert.ok(codes(validateStudio(root)).includes('SKILL_SHORT_DESCRIPTION'), value);
  });
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/agents/openai.yaml', text => text.replace(/^(  short_description:.*\n)/m, '$1$1'));
    assert.ok(codes(validateStudio(root)).includes('SKILL_SHORT_DESCRIPTION'));
  });
});

test('short descriptions must belong to interface and retain the authoring length range', () => {
  for (const replacement of ['short_description: "A top-level field cannot describe the interface."', 'metadata:\n  short_description: "Metadata is not the skill interface mapping."']) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/agents/openai.yaml', text => text.replace(/^  short_description:.*$/m, replacement));
    assert.ok(codes(validateStudio(root)).includes('SKILL_SHORT_DESCRIPTION'));
  });
  for (const length of [24, 65]) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/agents/openai.yaml', text => text.replace(/^  short_description:.*$/m, '  short_description: ' + JSON.stringify('x'.repeat(length))));
    assert.ok(codes(validateStudio(root)).includes('SKILL_SHORT_DESCRIPTION'), String(length));
  });
  for (const length of [25, 64]) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/agents/openai.yaml', text => text.replace(/^  short_description:.*$/m, '  short_description: ' + JSON.stringify('x'.repeat(length))));
    assert.equal(validateStudio(root).status, 'PASS', String(length));
  });
});

test('automatic output review cannot disappear from a directly invoked owner', () => {
  for (const owner of ['workflow-orchestrator', 'pipeline-core', 'static-graphic-design-creator', 'image-prompt-architect', 'commercial-video-campaign-director']) withFixture(root => {
    edit(root, 'skills/' + owner + '/SKILL.md', text => text.replace('automatically apply [output review]', 'optionally apply [output review]'));
    assert.ok(codes(validateStudio(root)).includes('OUTPUT_REVIEW_ENTRY'), owner);
  });
});

test('automatic output review retains its budget and uninspected-media boundary', () => {
  for (const phrase of ['at most three evaluation passes', 'media outcome uninspected', 'QA alone authorizes no generation']) withFixture(root => {
    edit(root, 'skills/pipeline-core/references/loop-protocol.md', text => text.replace(phrase, 'removed contract'));
    assert.ok(codes(validateStudio(root)).includes('OUTPUT_REVIEW_POLICY'), phrase);
  });
});

test('brand strategy, visual craft and guide delivery retain their shared profile', () => {
  for (const owner of ['marketing', 'static-graphic-design-creator', 'delivery-documentation']) withFixture(root => {
    edit(root, 'skills/' + owner + '/SKILL.md', text => text.replace('brand-identity-workflow.md', 'removed.md'));
    assert.ok(codes(validateStudio(root)).includes('BRAND_IDENTITY_SOURCE'), owner);
  });
});

test('brand profile cannot drop vector evidence or revision-aware delivery', () => {
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/references/brand-identity-workflow.md', text => text.replace('actual vector geometry', 'a filename'));
    assert.ok(codes(validateStudio(root)).includes('BRAND_IDENTITY_SOURCE'));
  });
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/assets/brand-identity.template.md', text => text.replace('source_revisions', 'removed'));
    assert.ok(codes(validateStudio(root)).includes('BRAND_IDENTITY_SOURCE'));
  });
});

test('installed version directory and authoring slug accept both equivalent skills paths', () => {
  for (const name of ['framecore-work-creative-studio', currentVersion]) for (const discovery of ['./skills', './skills/']) withFixture(root => {
    editJson(root, '.codex-plugin/plugin.json', data => { data.skills = discovery; });
    assert.equal(validateStudio(root).status, 'PASS');
  }, name);
});

test('compact entry keeps its budget and the moved rare-path rules', () => {
  const entry = fs.readFileSync(path.join(source, 'skills/workflow-orchestrator/SKILL.md'), 'utf8');
  assert.ok(Buffer.byteLength(entry) <= 32000);
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text + '\n' + 'x'.repeat(4000) + '\n');
    assert.ok(codes(validateStudio(root)).includes('ORCHESTRATOR_BUDGET'));
  });
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/references/routing-boundaries.md', text => text.replace('The sequence and board owners are distinct', 'Owners'));
    assert.ok(codes(validateStudio(root)).includes('ORCHESTRATOR_REFERENCE'));
  });
  withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replace('](references/version-reporting.md)', '](references/missing.md)'));
    assert.ok(codes(validateStudio(root)).includes('ORCHESTRATOR_REFERENCE'));
  });
});

test('overlapping owners name their neighbors and explicit-only owners stay explicit', () => {
  withFixture(root => {
    edit(root, 'skills/storytelling/SKILL.md', text => text.replace('Screenplay Story Architect', 'another owner'));
    assert.ok(codes(validateStudio(root)).includes('ROUTING_BOUNDARY'));
  });
  withFixture(root => {
    edit(root, 'skills/producer-ai-task-builder/agents/openai.yaml', text => text.replace('allow_implicit_invocation: false', 'allow_implicit_invocation: true'));
    assert.ok(codes(validateStudio(root)).includes('EXPLICIT_ONLY_POLICY'));
  });
  withFixture(root => {
    edit(root, 'skills/hipson-adapter/agents/openai.yaml', text => text.replace(/\npolicy:\n  allow_implicit_invocation: false\n?/, '\n'));
    assert.ok(codes(validateStudio(root)).includes('EXPLICIT_ONLY_POLICY'));
  });
});

test('every routed specialist appears in at least one orchestrator table route', () => {
  const registry = JSON.parse(fs.readFileSync(path.join(source, 'scripts/studio-contracts.json'), 'utf8'));
  assert.equal(registry.owners.length, 37);
  for (const owner of registry.owners.filter(item => item.route_required)) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.split('\n').filter(line => !(line.startsWith('|') && line.includes('(../' + owner.id + '/SKILL.md)'))).join('\n'));
    assert.ok(codes(validateStudio(root)).includes('OWNER_ROUTE'), owner.id);
  });
});

test('image reference, edit base and review target routes have distinct owners', () => {
  const registry = JSON.parse(fs.readFileSync(path.join(source, 'scripts/studio-contracts.json'), 'utf8'));
  assert.equal(registry.operation_routes.length, 3);
  for (const contract of registry.operation_routes) withFixture(root => {
    edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.split('\n').map(line => {
      if (line.startsWith('| ' + contract.need + ' |')) return line.replace(/\(\.\.\/[a-z0-9-]+\/SKILL\.md\)/g, '(../humanizer/SKILL.md)');
      return line;
    }).join('\n'));
    assert.ok(codes(validateStudio(root)).includes('OPERATION_ROUTE'), contract.need);
  });
});

test('complete pinned Static Graphic Design Creator bundle is byte-verified', () => {
  const provenance = JSON.parse(fs.readFileSync(path.join(source, 'skills/static-graphic-design-creator/source-provenance.json'), 'utf8'));
  assert.equal(provenance.immutable_source_commit, 'cbfc0160333d8605078c9a75508116b678f5af99');
  assert.equal(provenance.source_bundle_file_count, 34);
  assert.equal(provenance.files.length, 34);
  for (const item of provenance.files) {
    const bytes = fs.readFileSync(path.join(source, 'skills/static-graphic-design-creator', item.bundled_path));
    assert.equal(createHash('sha256').update(bytes).digest('hex'), item.sha256, item.bundled_path);
  }
  const alias = JSON.parse(fs.readFileSync(path.join(source, 'scripts/studio-contracts.json'), 'utf8')).owners.find(item => item.id === 'producer-ai-task-builder');
  assert.equal(alias.route_required, false);
  assert.match(fs.readFileSync(path.join(source, 'skills/producer-ai-task-builder/SKILL.md'), 'utf8'), /Audio Production Director/);
});

test('duplicate route and dropped registry owner cannot look valid', () => withFixture(root => {
  edit(root, 'skills/workflow-orchestrator/SKILL.md', text => {
    const row = text.split('\n').find(line => line.startsWith('|') && line.includes('(../humanizer/SKILL.md)'));
    return text.replace(row, row + '\n' + row);
  });
  assert.ok(codes(validateStudio(root)).includes('OWNER_ROUTE'));
  editJson(root, 'scripts/studio-contracts.json', data => { data.owners = data.owners.filter(owner => owner.id !== 'humanizer'); });
  assert.ok(codes(validateStudio(root)).includes('OWNER_ROSTER'));
}));

test('deleting privacy and untrusted-source paragraph fails the canonical gate', () => withFixture(root => {
  edit(root, 'skills/research-evidence/SKILL.md', text => text.split('\n').filter(line => !line.startsWith('Never send private briefs')).join('\n'));
  const result = validateStudio(root);
  assert.ok(result.canonical.errors.some(error => error.code === 'CRITICAL_CONTRACT' && error.detail.startsWith('research_privacy')));
  assert.ok(result.canonical.errors.some(error => error.code === 'CRITICAL_CONTRACT' && error.detail.startsWith('untrusted_sources')));
}));

test('research link retained while the conditional gate is removed or reverted still fails', () => {
  withFixture(root => {
    edit(root, 'skills/humanizer/SKILL.md', text => text.replace(/conditional/gi, 'optional'));
    assert.ok(codes(validateStudio(root)).includes('RESEARCH_CONDITIONAL'));
  });
  withFixture(root => {
    edit(root, 'skills/humanizer/SKILL.md', text => text.replace('Apply the conditional [public research gate]', 'Run the mandatory conditional [public research gate]'));
    assert.ok(codes(validateStudio(root)).includes('RESEARCH_CONDITIONAL'));
  });
});

test('research triggers, untriggered restraint and offline handling are protected', () => withFixture(root => {
  edit(root, 'skills/research-evidence/SKILL.md', text => text.replace('## Research triggers', '## Research lanes overview').replace('Do not search out of habit', 'Search freely'));
  const errors = validateStudio(root).canonical.errors;
  assert.ok(errors.some(error => error.code === 'CRITICAL_CONTRACT' && error.detail.startsWith('research_conditional_triggers')));
}));

test('planned research expectations require a named trigger or an untriggered reason', () => {
  const effective = loadEffectiveEvals(source).cases;
  assert.ok(effective.some(item => item.research_expectation === 'not_triggered'));
  for (const item of effective.filter(entry => entry.research_expectation === 'required')) assert.ok(item.research_trigger, item.id);
  assert.equal(effective.find(item => item.id === 'S10').research_trigger, 'named_tool_or_model');
  assert.equal(effective.find(item => item.id === 'H13').research_expectation, 'not_triggered');
  withFixture(root => {
    editJson(root, 'evals/video-cases.json', data => { delete data.cases.find(item => item.id === 'V02').research_trigger; });
    assert.ok(codes(validateStudio(root)).includes('EVAL_RESEARCH_TRIGGER'));
  });
  withFixture(root => {
    editJson(root, 'evals/video-cases.json', data => { const item = data.cases.find(entry => entry.id === 'V01'); item.research_trigger = 'named_tool_or_model'; });
    assert.ok(codes(validateStudio(root)).includes('EVAL_RESEARCH_TRIGGER'));
  });
  withFixture(root => {
    editJson(root, 'evals/studio-behavior-cases.json', data => { data.cases.find(item => item.id === 'H13').expected_owners.push('research-evidence'); });
    assert.ok(codes(validateStudio(root)).includes('EVAL_UNTRIGGERED_OWNER'));
  });
  withFixture(root => {
    editJson(root, 'evals/workflow-kit-cases.json', data => { data.cases = data.cases.filter(item => item.id !== 'WK13'); });
    assert.ok(codes(validateStudio(root)).includes('RESEARCH_CONDITIONAL_COVERAGE'));
  });
});

test('README and migration release drift is rejected independently', () => {
  for (const relative of ['README.md', 'docs/migration-status.md']) withFixture(root => {
    const version = JSON.parse(fs.readFileSync(path.join(root, 'plugin.json'), 'utf8')).version;
    edit(root, relative, text => text.replaceAll(version, '99.0.0'));
    assert.ok(codes(validateStudio(root)).includes('DOC_VERSION'), relative);
  });
});

test('manifest identity, keywords and strict semver mutations fail', () => {
  withFixture(root => { editJson(root, '.codex-plugin/plugin.json', data => { data.keywords = ['wrong']; }); assert.ok(codes(validateStudio(root)).includes('MANIFEST_IDENTITY')); });
  for (const version of ['01.0.0', '1.0.0-dev_27', '1.0.0-01', '1.0.0-dev..2']) withFixture(root => {
    for (const file of ['plugin.json', '.codex-plugin/plugin.json']) editJson(root, file, data => { data.version = version; });
    assert.ok(codes(validateStudio(root)).includes('VERSION'), version);
  });
});

test('escaping discovery paths, absolute paths and symlinks are blocked', () => {
  for (const discovery of ['../outside', '/tmp/skills', './skills/../../outside']) withFixture(root => {
    editJson(root, '.codex-plugin/plugin.json', data => { data.skills = discovery; });
    assert.ok(codes(validateStudio(root)).includes('SKILLS_PATH'));
  });
  withFixture(root => {
    fs.symlinkSync('/etc/passwd', path.join(root, 'malicious-reference.md'));
    assert.ok(codes(validateStudio(root)).includes('SYMLINK'));
  });
});

test('portable or fallback integrations cannot be silently added', () => {
  for (const file of ['mcp.json', '.mcp.json', 'hooks.json']) withFixture(root => { fs.writeFileSync(path.join(root, file), '{}'); assert.ok(codes(validateStudio(root)).includes('UNPLANNED_INTEGRATION')); });
  withFixture(root => { editJson(root, 'plugin.json', data => { data.extensions['com.openai'].apps = ['unplanned']; }); assert.ok(codes(validateStudio(root)).includes('UNPLANNED_INTEGRATION')); });
});

test('missing references, escaped Markdown links and missing fragments fail', () => {
  for (const [suffix, code] of [['[bad](missing.md)', 'BROKEN_LINK'], ['[bad](../../../../outside.md)', 'LINK_ESCAPE'], ['[bad](#nonexistent-test-anchor)', 'BROKEN_ANCHOR']]) withFixture(root => {
    edit(root, 'skills/humanizer/SKILL.md', text => text + '\n' + suffix + '\n');
    assert.ok(codes(validateStudio(root)).includes(code), suffix);
  });
});

test('effective loader preserves historical files and applies seven source-guarded overrides', () => {
  const effective = loadEffectiveEvals(source);
  assert.equal(effective.legacy_cases, 114);
  assert.deepEqual([...effective.overrides_applied].sort(), ['S01', 'S18', 'S32', 'S35', 'S45', 'S50', 'S51']);
  assert.equal(effective.additional_cases, 4);
  assert.equal(effective.host_scenarios, 25);
  assert.equal(effective.knowledge_scenarios, 12);
  assert.equal(effective.learning_scenarios, 24);
  assert.equal(effective.campaign_scenarios, 8);
  assert.equal(effective.cases.length, 201);
  const byId = new Map(effective.cases.map(item => [item.id, item]));
  assert.match(byId.get('S35').expected_branch, /geometry_unknown/);
  assert.match(byId.get('S35-CROP').expected_branch, /^feasible/);
  assert.match(byId.get('S35-PAD').expected_branch, /^feasible/);
  assert.match(byId.get('S35-CONFLICT').expected_branch, /conflict/);
  assert.equal(byId.get('S45').visual_label_resolution_contract.direction_permitted, true);
  assert.equal(byId.get('S45-FINAL').visual_label_resolution_contract.final_prompt_permitted, false);
  assert.equal(byId.get('S18').scenario_scope.requires_mock_capabilities, true);
});

test('campaign entry and static production keep the same reachable workflow', () => {
  for (const [file, phrase] of [
    ['skills/marketing/SKILL.md', 'website-to-campaign.md'],
    ['skills/static-graphic-design-creator/SKILL.md', 'campaign-production.md'],
    ['skills/ecommerce-campaign-strategy-director/SKILL.md', 'Do not bypass the integrated static owner'],
  ]) withFixture(root => {
    edit(root, file, text => text.replaceAll(phrase, 'removed-contract'));
    assert.ok(codes(validateStudio(root)).includes('CAMPAIGN_WORKFLOW'), file);
  });
});

test('campaign source guards reject lost claim, access and synthetic-person boundaries', () => {
  const prefix = 'skills/ecommerce-campaign-strategy-director/references/';
  for (const [file, phrase] of [
    ['website-to-campaign.md', 'Public website content does not establish conversion rate'],
    ['website-to-campaign.md', 'user approval of copy does not prove a claim'],
    ['campaign-production.md', 'A synthetic presenter is not a real customer'],
  ]) withFixture(root => {
    edit(root, prefix + file, text => text.replaceAll(phrase, 'removed-contract'));
    assert.ok(codes(validateStudio(root)).includes('CAMPAIGN_WORKFLOW'), phrase);
  });
});

test('campaign recovery and evaluation evidence fail closed on drift', () => {
  withFixture(root => {
    edit(root, 'skills/pipeline-core/templates/project-state.md', text => text.replace('- campaign_context:', '- lost_context:'));
    assert.ok(codes(validateStudio(root)).includes('CAMPAIGN_WORKFLOW'));
  });
  withFixture(root => {
    editJson(root, 'evals/campaign-workflow-cases.json', data => { data.cases[0].execution_status = 'passed'; data.cases[1].expected_owners = ['invented-campaign-agent']; });
    assert.ok(codes(validateStudio(root)).includes('CAMPAIGN_WORKFLOW'));
  });
});

test('override source mismatch fails closed instead of silently changing historical meaning', () => withFixture(root => {
  editJson(root, 'evals/effective-overrides.json', data => { data.overrides[0].source_record_sha256 = '0'.repeat(64); });
  assert.throws(() => loadEffectiveEvals(root), /Override source drift/);
  assert.ok(codes(validateStudio(root)).includes('EFFECTIVE_EVALS'));
}));

test('missing reviewed override and malformed registry fail closed', () => {
  withFixture(root => {
    editJson(root, 'evals/effective-overrides.json', data => { data.overrides = data.overrides.filter(item => item.id !== 'S35'); });
    assert.ok(codes(validateStudio(root)).includes('OVERRIDE_COVERAGE'));
  });
  withFixture(root => {
    editJson(root, 'scripts/studio-contracts.json', data => { data.owners = {}; data.critical_contracts = {}; });
    const found = codes(validateStudio(root)); assert.ok(found.includes('OWNER_ROSTER')); assert.ok(found.includes('CRITICAL_ROSTER'));
  });
});

test('PA05 preserves scoped user authorization while unavailable capabilities block execution', () => {
  const item = loadEffectiveEvals(source).cases.find(entry => entry.id === 'PA05');
  assert.equal(item.research_expectation, 'not_applicable');
  assert.equal(item.research_exemption_reason, 'unsupported_capability_status');
  assert.equal(item.tool_state.uploads_authorized, true);
  assert.equal(item.tool_state.upload_capability, 'not_available');
  assert.equal(item.tool_state.named_surface_execution_capability, 'not_available');
  assert.ok(item.context.authorization_scope.requested_operations_authorized.includes('upload resulting file to user Google Drive'));
  assert.equal(item.context.authorization_scope.paid_charges_authorized, false);
  assert.equal(item.context.authorization_scope.different_provider_or_route_authorized, false);
  assert.equal(item.context.authorization_scope.different_destination_authorized, false);
  assert.equal(item.status, 'planned');
});

test('research failure and evidence scenarios stay planned rather than claiming execution', () => {
  const suite = JSON.parse(fs.readFileSync(path.join(source, 'evals/studio-behavior-cases.json'), 'utf8'));
  assert.equal(new Set(suite.cases.map(item => item.family)).size, 25);
  for (const state of ['unavailable', 'timeout', 'error']) assert.ok(suite.cases.some(item => item.tool_state.web_search === state));
  withFixture(root => {
    editJson(root, 'evals/studio-behavior-cases.json', data => { data.cases[0].status = 'PASS'; data.cases[0].execution_status = 'passed'; });
    const found = codes(validateStudio(root)); assert.ok(found.includes('EVAL_EXECUTION_CLAIM')); assert.ok(found.includes('HOST_EVIDENCE_CONTRACT'));
  });
});

test('requested legacy diagnostics keep original errors and do not convert FAIL to PASS', () => {
  const result = validateStudio(source, {legacy: true});
  assert.notEqual(result.legacy.status, 'NOT_RUN');
  if (result.legacy.status !== 'PASS') {
    assert.equal(result.status, 'FAIL');
    assert.ok(result.legacy.report?.errors?.length || result.legacy.error || result.legacy.stderr || result.legacy.stdout);
  }
  assert.match(result.canonical.warnings.join(' '), /do not reproduce all historical/);
});

test('knowledge coverage cannot silently lose cases or claim executed outcomes', () => {
  withFixture(root => {
    editJson(root, 'evals/knowledge-practice-cases.json', data => { data.cases.pop(); });
    assert.ok(codes(validateStudio(root)).includes('KNOWLEDGE_COVERAGE'));
  });
  withFixture(root => {
    editJson(root, 'evals/knowledge-practice-cases.json', data => { data.cases[0].execution_status = 'passed'; });
    assert.ok(codes(validateStudio(root)).includes('KNOWLEDGE_EVIDENCE'));
  });
});
