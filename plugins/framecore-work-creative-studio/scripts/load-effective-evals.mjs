import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

export const legacyEvalFiles = ['static-cases.json', 'video-cases.json', 'campaign-cases.json', 'story-cases.json', 'storyboard-cases.json', 'producer-cases.json'];
export function canonicalJson(value) {
  if (Array.isArray(value)) return '[' + value.map(canonicalJson).join(',') + ']';
  if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonicalJson(value[key])).join(',') + '}';
  return JSON.stringify(value);
}
export const caseDigest = value => createHash('sha256').update(canonicalJson(value)).digest('hex');

// Read-only effective view. Historical files are never rewritten and never gain execution status.
export function loadEffectiveEvals(root) {
  const base = path.resolve(root);
  const read = relative => {
    const target = path.resolve(base, relative);
    if (!target.startsWith(base + path.sep)) throw new Error('Eval path escapes package: ' + relative);
    const real = fs.realpathSync(target);
    if (!real.startsWith(fs.realpathSync(base) + path.sep)) throw new Error('Eval symlink escapes package: ' + relative);
    return JSON.parse(fs.readFileSync(target, 'utf8'));
  };
  const sources = legacyEvalFiles.map(file => ({file, data: read('evals/' + file)}));
  const cases = sources.flatMap(({file, data}) => {
    if (!Array.isArray(data.cases)) throw new Error('Missing cases in ' + file);
    return data.cases.map(item => ({...item, provenance: {source_file: file, effective_override: false}}));
  });
  const overlay = read('evals/effective-overrides.json');
  if (overlay.schema_version !== 1 || !Array.isArray(overlay.overrides) || !Array.isArray(overlay.additional_cases)) throw new Error('Invalid effective override schema');
  const sourceIds = new Set(cases.map(item => item.id));
  if (sourceIds.size !== cases.length) throw new Error('Duplicate legacy eval ID');
  const applied = new Set();
  for (const override of overlay.overrides) {
    if (applied.has(override.id)) throw new Error('Duplicate override: ' + override.id);
    const index = cases.findIndex(item => item.id === override.id && item.provenance.source_file === override.source_file);
    if (index < 0) throw new Error('Override target missing: ' + override.id);
    const {provenance, ...original} = cases[index];
    if (caseDigest(original) !== override.source_record_sha256) throw new Error('Override source drift: ' + override.id + '; review source before rebasing overlay');
    if (override.replacement?.id !== override.id || override.replacement?.status !== 'planned' || !override.reason) throw new Error('Invalid planned override: ' + override.id);
    cases[index] = {...override.replacement, provenance: {...provenance, effective_override: true, source_record_sha256: override.source_record_sha256, reason: override.reason}};
    applied.add(override.id);
  }
  const newSuite = read('evals/studio-behavior-cases.json');
  if (newSuite.schema_version !== 1 || !Array.isArray(newSuite.cases)) throw new Error('Invalid Studio behavior schema');
  const practiceSuite = read('evals/knowledge-practice-cases.json');
  if (practiceSuite.schema_version !== 1 || !Array.isArray(practiceSuite.cases)) throw new Error('Invalid knowledge practice schema');
  const integrationSuite = read('evals/workflow-kit-cases.json');
  if (integrationSuite.schema_version !== 1 || !Array.isArray(integrationSuite.cases)) throw new Error('Invalid integration case schema');
  const learningSuite = read('evals/learning-mode-cases.json');
  if (learningSuite.schema_version !== 1 || !Array.isArray(learningSuite.cases)) throw new Error('Invalid learning case schema');
  const campaignSuite = read('evals/campaign-workflow-cases.json');
  if (campaignSuite.schema_version !== 1 || !Array.isArray(campaignSuite.cases)) throw new Error('Invalid campaign case schema');
  for (const [file, additions] of [['effective-overrides.json', overlay.additional_cases], ['studio-behavior-cases.json', newSuite.cases], ['knowledge-practice-cases.json', practiceSuite.cases], ['workflow-kit-cases.json', integrationSuite.cases], ['learning-mode-cases.json', learningSuite.cases], ['campaign-workflow-cases.json', campaignSuite.cases]]) {
    for (const item of additions) {
      if (!item.id || sourceIds.has(item.id)) throw new Error('Duplicate effective eval ID: ' + item.id);
      sourceIds.add(item.id);
      cases.push({...item, provenance: {source_file: file, effective_override: false}});
    }
  }
  return {
    scope: 'Planned specifications only; loading does not run a model, tools, or evaluate behavior.',
    legacy_cases: sources.reduce((n, source) => n + source.data.cases.length, 0),
    overrides_applied: [...applied], additional_cases: overlay.additional_cases.length,
    host_scenarios: newSuite.cases.length, knowledge_scenarios: practiceSuite.cases.length, integration_scenarios: integrationSuite.cases.length, learning_scenarios: learningSuite.cases.length, campaign_scenarios: campaignSuite.cases.length, cases,
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const root = process.argv[2] ?? path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
    console.log(JSON.stringify(loadEffectiveEvals(root), null, 2));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
