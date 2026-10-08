import fs from 'node:fs';
import path from 'node:path';

export const presentationPolicy = 'skills/pipeline-core/references/presentation-and-interaction.md';
export const presentationCases = 'evals/presentation-cases.json';
export const presentationFamilies = ['copyable_prompt_text', 'concept_comparison_choice', 'interactive_lesson_waits', 'full_learning_brief', 'quiz_after_expired_menu', 'scene_time_and_copy_fix', 'stale_view_vs_revision', 'no_native_host_text_equivalent', 'no_renderer_no_export', 'explicit_plain_text', 'campaign_matrix_no_invented_metrics', 'qa_status_from_evidence', 'audio_timeline_not_listen', 'direct_specialist_invocation', 'selection_to_prompt_handoff', 'startup_with_native_host', 'route_comparison_not_authorization'];
const sections = ['host-basis', 'choosing-the-form', 'equivalent-text-path', 'interaction-state-and-actions', 'domain-adaptations', 'learning', 'concepts', 'storyboard-and-motion', 'prompts-and-references', 'campaigns-and-qa', 'other-modules', 'module-coverage'];
// Each domain source must route to its own adaptation, not only to the shared file.
const domainRoutes = [
  ['skills/pipeline-core/references/studio-integration-policy.md', 'presentation-and-interaction.md'],
  ['skills/workflow-orchestrator/SKILL.md', '../pipeline-core/references/presentation-and-interaction.md'],
  ['skills/workflow-orchestrator/references/startup-and-creative-menus.md', 'presentation-and-interaction.md#interaction-state-and-actions'],
  ['skills/workflow-orchestrator/references/learning-mode.md', 'presentation-and-interaction.md#learning'],
  ['skills/workflow-orchestrator/references/studio-contract.md', 'presentation-and-interaction.md#concepts'],
  ['skills/hyperframes-workflow/SKILL.md', 'presentation-and-interaction.md#storyboard-and-motion'],
  ['skills/storyboard-sequence-architect/SKILL.md', 'presentation-and-interaction.md#storyboard-and-motion'],
  ['skills/pipeline-core/references/prompt-format-and-continuity.md', 'presentation-and-interaction.md#prompts-and-references'],
  ['skills/output-critic-iteration/references/review-and-repair.md', 'presentation-and-interaction.md#campaigns-and-qa'],
  ['skills/ecommerce-campaign-strategy-director/SKILL.md', 'presentation-and-interaction.md#campaigns-and-qa'],
  ['skills/audio-production-director/SKILL.md', 'presentation-and-interaction.md#other-modules'],
];
const officialHosts = new Set(['openai.com', 'help.openai.com', 'developers.openai.com', 'platform.openai.com', 'learn.chatgpt.com']);
const slug = heading => heading.trim().toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, '').replace(/\s+/g, '-');

// Structure and planned-evidence checks only: no model is run and no host UI is observed.
export function validatePresentation(root, packageFiles, ownerIds) {
  const errors = [], fail = (code, detail) => errors.push({code, detail});
  const read = relative => {
    if (!packageFiles.includes(relative)) throw new Error('Missing presentation resource: ' + relative);
    return fs.readFileSync(path.join(root, relative), 'utf8');
  };
  try {
    const body = read(presentationPolicy);
    const anchors = new Set([...body.matchAll(/^#{2,3} (.+)$/gm)].map(match => slug(match[1])));
    for (const section of sections) if (!anchors.has(section)) fail('PRESENTATION_SECTION', section);
    const basis = body.split('## Host basis')[1]?.split('\n## ')[0] ?? '';
    const sources = [...basis.matchAll(/\]\((https?:[^)]+)\)/g)].map(match => new URL(match[1]));
    if (!sources.length || sources.some(url => url.protocol !== 'https:' || !officialHosts.has(url.hostname))) fail('PRESENTATION_SOURCES', 'Host basis must cite official OpenAI sources only');
    if (!/^Checked \d{4}-\d{2}-\d{2}/m.test(basis) || !/^Unknown:/m.test(basis)) fail('PRESENTATION_SOURCES', 'Host basis needs a check date and an explicit Unknown list');
    const coverage = body.split('## Module coverage')[1] ?? '';
    const rows = coverage.split('\n').filter(line => /^\| [a-z0-9-]+ \|/.test(line)).map(line => line.split('|').slice(1, -1).map(cell => cell.trim()));
    const covered = rows.map(row => row[0]);
    if (new Set(covered).size !== covered.length) fail('PRESENTATION_COVERAGE', 'Duplicate module row');
    const missing = ownerIds.filter(id => !covered.includes(id)), extra = covered.filter(id => !ownerIds.includes(id));
    if (missing.length || extra.length) fail('PRESENTATION_COVERAGE', 'Rows must match the owner roster; missing ' + missing.join(', ') + '; unknown ' + extra.join(', '));
    for (const row of rows) if (row.length !== 4 || row.some(cell => !cell)) fail('PRESENTATION_COVERAGE', row[0] + ': every module needs a form, a text path and its state');
  } catch (error) { fail('PRESENTATION_SECTION', error.message); }
  for (const [relative, link] of domainRoutes) {
    try { if (!read(relative).includes(link + ')')) fail('PRESENTATION_ROUTE', relative + ' -> ' + link); }
    catch (error) { fail('PRESENTATION_ROUTE', error.message); }
  }
  // Every entrypoint reaches the policy through the integration authority it already reads.
  for (const id of ownerIds) {
    const relative = 'skills/' + id + '/SKILL.md';
    try { if (!read(relative).includes('studio-integration-policy.md)')) fail('PRESENTATION_REACH', relative); }
    catch (error) { fail('PRESENTATION_REACH', error.message); }
  }
  try {
    const suite = JSON.parse(read(presentationCases));
    const cases = Array.isArray(suite.cases) ? suite.cases : [];
    if (suite.schema_version !== 1 || cases.length !== presentationFamilies.length) fail('PRESENTATION_CASES', 'Expected one planned case per presentation family');
    const families = cases.map(item => item.family);
    if (families.length !== new Set(families).size || presentationFamilies.some(family => !families.includes(family))) fail('PRESENTATION_CASES', 'Families must be distinct and complete');
    cases.forEach((item, index) => {
      const id = 'PI' + String(index + 1).padStart(2, '0'), host = item.host_profile?.native_interactive_elements;
      if (item.id !== id || item.status !== 'planned' || item.execution_status !== 'not_run') fail('PRESENTATION_EVIDENCE', (item.id ?? id) + ': planned cases stay not_run until a recorded host run');
      if (!['offered', 'not_offered', 'unknown'].includes(host) || !['text', 'native_or_text_equivalent'].includes(item.expected_presentation)) fail('PRESENTATION_CASES', id + ': host profile and expected presentation');
      if (host === 'not_offered' && item.expected_presentation !== 'text') fail('PRESENTATION_CASES', id + ': a host without native elements expects text');
      if (typeof item.text_path !== 'string' || !item.text_path.trim()) fail('PRESENTATION_TEXT_PATH', id);
      for (const field of ['checks', 'forbidden', 'required_evidence']) if (!Array.isArray(item[field]) || !item[field].length) fail('PRESENTATION_CASES', id + ': ' + field);
      if (!Array.isArray(item.expected_owners) || !item.expected_owners.length || item.expected_owners.some(owner => !ownerIds.includes(owner))) fail('PRESENTATION_CASES', id + ': owners');
    });
  } catch (error) { fail('PRESENTATION_CASES', error.message); }
  return errors;
}
