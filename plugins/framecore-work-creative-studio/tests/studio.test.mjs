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

test('canonical validation passes with explicit structural scope and no legacy execution', () => {
  const result = validateStudio(source);
  assert.equal(result.status, 'PASS', JSON.stringify(result.canonical?.errors));
  assert.match(result.canonical.scope, /not host behavior/);
  assert.equal(result.legacy.status, 'NOT_RUN');
  assert.equal(result.canonical.evaluations.executed, 0);
});

test('installed version directory and authoring slug accept both equivalent skills paths', () => {
  for (const name of ['framecore-work-creative-studio', currentVersion]) for (const discovery of ['./skills', './skills/']) withFixture(root => {
    editJson(root, '.codex-plugin/plugin.json', data => { data.skills = discovery; });
    assert.equal(validateStudio(root).status, 'PASS');
  }, name);
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

test('research link retained while mandatory is weakened still fails', () => withFixture(root => {
  edit(root, 'skills/humanizer/SKILL.md', text => text.replace(/mandatory/gi, 'optional'));
  assert.ok(codes(validateStudio(root)).includes('RESEARCH_MANDATORY'));
}));

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
  assert.equal(effective.learning_scenarios, 16);
  assert.equal(effective.cases.length, 183);
  const byId = new Map(effective.cases.map(item => [item.id, item]));
  assert.match(byId.get('S35').expected_branch, /geometry_unknown/);
  assert.match(byId.get('S35-CROP').expected_branch, /^feasible/);
  assert.match(byId.get('S35-PAD').expected_branch, /^feasible/);
  assert.match(byId.get('S35-CONFLICT').expected_branch, /conflict/);
  assert.equal(byId.get('S45').visual_label_resolution_contract.direction_permitted, true);
  assert.equal(byId.get('S45-FINAL').visual_label_resolution_contract.final_prompt_permitted, false);
  assert.equal(byId.get('S18').scenario_scope.requires_mock_capabilities, true);
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
