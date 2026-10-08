import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateStudio} from '../scripts/validate-studio.mjs';
import {presentationPolicy, presentationCases} from '../scripts/validate-presentation.mjs';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (relative, root = source) => fs.readFileSync(path.join(root, relative), 'utf8');
function fixture(run) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-presentation-test-'));
  try { fs.cpSync(source, root, {recursive: true}); return run(root); }
  finally { fs.rmSync(root, {recursive: true, force: true}); }
}
function edit(root, relative, change) {
  const before = read(relative, root), after = change(before);
  assert.notEqual(after, before, 'Mutation must apply: ' + relative);
  fs.writeFileSync(path.join(root, relative), after);
}
const editCases = (root, change) => edit(root, presentationCases, text => { const value = JSON.parse(text); change(value.cases); return JSON.stringify(value); });
const codes = root => (validateStudio(root).canonical?.errors ?? []).map(item => item.code);

test('the shared presentation policy and its planned cases pass canonical validation', () => {
  assert.equal(validateStudio(source).canonical.status, 'PASS');
});

test('every installed skill has exactly one coverage row', () => {
  const rows = read(presentationPolicy).split('## Module coverage')[1].split('\n').filter(line => /^\| [a-z0-9-]+ \|/.test(line)).map(line => line.split('|')[1].trim()).sort();
  const skills = fs.readdirSync(path.join(source, 'skills')).filter(id => fs.existsSync(path.join(source, 'skills', id, 'SKILL.md'))).sort();
  assert.deepEqual(rows, skills);
});

test('a module without coverage, or with an empty text path, fails', () => fixture(root => {
  edit(root, presentationPolicy, text => text.replace(/^\| caption-studio \|.*\n/m, '').replace(/^(\| humanizer \| [^|]+\|)[^|]+\|/m, '$1 |'));
  const errors = validateStudio(root).canonical.errors.filter(error => error.code === 'PRESENTATION_COVERAGE').map(error => error.detail).join('\n');
  assert.match(errors, /missing caption-studio/);
  assert.match(errors, /humanizer: every module needs/);
}));

test('a domain source that loses its route to its adaptation fails', () => fixture(root => {
  edit(root, 'skills/workflow-orchestrator/references/learning-mode.md', text => text.replace('presentation-and-interaction.md#learning)', 'presentation-and-interaction.md)'));
  edit(root, 'skills/pipeline-core/references/prompt-format-and-continuity.md', text => text.replace('presentation-and-interaction.md#prompts-and-references)', 'studio-integration-policy.md)'));
  assert.equal(codes(root).filter(code => code === 'PRESENTATION_ROUTE').length, 2);
}));

test('a skill that stops reading the integration authority loses the policy and fails', () => fixture(root => {
  edit(root, 'skills/humanizer/SKILL.md', text => text.replace('(../pipeline-core/references/studio-integration-policy.md)', '(../pipeline-core/references/loop-protocol.md)'));
  assert.ok(codes(root).includes('PRESENTATION_REACH'));
}));

test('a planned case cannot claim a host result or drop its text path', () => fixture(root => {
  editCases(root, cases => { cases[2].execution_status = 'passed'; cases[4].text_path = ''; });
  const found = codes(root);
  assert.ok(found.includes('PRESENTATION_EVIDENCE'));
  assert.ok(found.includes('PRESENTATION_TEXT_PATH'));
}));

test('a host without native elements must expect the text path', () => fixture(root => {
  editCases(root, cases => { cases.find(item => item.family === 'no_native_host_text_equivalent').expected_presentation = 'native_or_text_equivalent'; });
  assert.ok(validateStudio(root).canonical.errors.some(error => error.code === 'PRESENTATION_CASES' && /expects text/.test(error.detail)));
}));

test('dropping a required scenario family fails', () => fixture(root => {
  editCases(root, cases => { cases.find(item => item.family === 'stale_view_vs_revision').family = 'other'; });
  assert.ok(validateStudio(root).canonical.errors.some(error => error.code === 'PRESENTATION_CASES' && /distinct and complete/.test(error.detail)));
}));

test('the host basis accepts only dated official sources with an Unknown list', () => fixture(root => {
  edit(root, presentationPolicy, text => text.replace('(https://help.openai.com/en/articles/20001598-intelligent-ui-in-chatgpt)', '(https://example.com/intelligent-ui)').replace(/^Unknown:/m, 'Open:'));
  const details = validateStudio(root).canonical.errors.filter(error => error.code === 'PRESENTATION_SOURCES').map(error => error.detail).join('\n');
  assert.match(details, /official OpenAI sources/);
  assert.match(details, /Unknown list/);
}));

test('the startup welcome stays byte-checked after the presentation change', () => fixture(root => {
  edit(root, 'skills/workflow-orchestrator/SKILL.md', text => text.replace('1. **Creative mode**', '1. **Creative**'));
  assert.notEqual(validateStudio(root).canonical.status, 'PASS');
}));
