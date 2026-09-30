import fs from 'node:fs';
import path from 'node:path';
import {isDeepStrictEqual as equal} from 'node:util';

export const learningDomainIds = ['static_graphics', 'typography_layout', 'story_screenplay', 'performance', 'character_reference', 'storyboard_sequence', 'cinematography', 'commercial_video', 'music_video', 'copy_voice', 'prompting', 'audio_music', 'editing_motion', 'campaign_workflow'];
export const learningCaseIds = Array.from({length: 16}, (_, i) => 'LM' + String(i + 1).padStart(2, '0'));

// Package-source checks only. This does not run the host, classify user messages,
// assess learner work, or establish that the model follows the teaching method.
export function validateLearningMode(root, packageFiles) {
  const errors = [];
  const fail = (code, detail) => errors.push({code, detail});
  const read = relative => {
    if (path.isAbsolute(relative) || relative.split('/').includes('..') || !packageFiles.includes(relative)) throw new Error('Missing or invalid learning resource: ' + relative);
    return fs.readFileSync(path.join(root, relative), 'utf8');
  };
  const need = (relative, patterns) => {
    const body = read(relative);
    for (const pattern of patterns) if (!pattern.test(body)) fail('LEARNING_INSTRUCTION', relative + ': ' + pattern);
  };
  const strings = values => Array.isArray(values) && values.length > 0 && values.every(v => typeof v === 'string' && v.trim());
  try {
    need('skills/workflow-orchestrator/SKILL.md', [/Tryb nauki/, /Tryb tworzenia/, /references\/learning-mode\.md/, /creation immediately/, /show this short choice and wait/, /Quick\/Deep are a separate pace/]);
    need('skills/pipeline-core/references/studio-integration-policy.md', [/direct specialist invocation/, /learning overlay/, /Creation keeps the established production route/]);
    need('skills/studio-workstyle-profile/SKILL.md', [/learning overlay/, /ordinary one-question rule/]);
    need('skills/pipeline-core/templates/project-state.md', [/interaction_mode/, /learning_context/, /learning-progress\.template\.md/]);
    need('skills/pipeline-core/references/project-recovery.md', [/learning_context/, /learning-progress\.template\.md/]);
    const method = 'skills/workflow-orchestrator/references/learning-mode.md';
    need(method, [/## Onboarding/, /at most six short questions/, /optional blanks do not block/, /## Personal plan/, /shared foundations/, /all requested supported specializations/, /begin the first lesson/, /plan-only/, /## Lesson cycle/, /Stop for the learner's attempt/, /one or two priority improvements/, /## Switching and project work/, /switches to creation immediately/, /## Progress and recovery/, /Do not mark a lesson completed merely because it was displayed/, /Do not promise persistent memory or cross-host sync/, /## Research, costs and limits/, /first offers a no-render alternative/, /Learning alone authorizes no generation/, /No free-use guarantee follows from a ChatGPT subscription/]);
    need('skills/workflow-orchestrator/assets/learning-plan.template.md', [/independent_outcome/, /domain_ids/, /sequence_reason/, /learner_action/, /assessment/, /tools_costs/, /no_render_alternative/, /estimated_effort/, /integrative_project/, /plan_only/]);
    need('skills/workflow-orchestrator/assets/learning-progress.template.md', [/level_by_domain/, /current_module/, /completed_lessons/, /skipped_lessons/, /strengths/, /practice_needs/, /next_action/, /persistence/]);
    const map = JSON.parse(read('skills/workflow-orchestrator/assets/learning-domains.json'));
    if (map.schema_version !== 1 || map.path_base !== 'plugin_root' || !Array.isArray(map.domains)) throw new Error('Invalid learning domain map');
    if (!equal(map.domains.map(d => d.id).sort(), [...learningDomainIds].sort())) fail('LEARNING_DOMAIN_COVERAGE', 'Expected the fourteen supported domain IDs once each');
    for (const domain of map.domains) {
      if (!strings([domain.title, domain.exercise_no_render, domain.support_boundary]) || !strings(domain.topics) || !strings(domain.assessment_criteria) || !strings(domain.owners) || !strings(domain.sources)) {
        fail('LEARNING_DOMAIN', String(domain.id));
        continue;
      }
      for (const owner of domain.owners) {
        if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(owner) || !domain.sources.includes('skills/' + owner + '/SKILL.md')) fail('LEARNING_OWNER', domain.id + ': ' + owner);
        else read('skills/' + owner + '/SKILL.md');
      }
      for (const source of domain.sources) read(source);
    }
    const suite = JSON.parse(read('evals/learning-mode-cases.json'));
    if (suite.schema_version !== 1 || !Array.isArray(suite.cases)) throw new Error('Invalid learning scenario suite');
    if (!equal(suite.cases.map(c => c.id).sort(), learningCaseIds)) fail('LEARNING_CASE_COVERAGE', 'Expected LM01 through LM16 once each');
    for (const item of suite.cases) {
      if (item.status !== 'planned' || item.execution_status !== 'not_run' || !strings(item.required_evidence) || !strings(item.expected_owners) || !strings(item.checks) || !['learning', 'creation', 'undecided'].includes(item.expected_interaction_mode)) fail('LEARNING_EVAL', String(item.id));
      for (const owner of item.expected_owners ?? []) if (!packageFiles.includes('skills/' + owner + '/SKILL.md')) fail('LEARNING_EVAL_OWNER', item.id + ': ' + owner);
      if (item.research_expectation === 'required' && !item.expected_owners?.includes('research-evidence')) fail('LEARNING_RESEARCH_OWNER', item.id);
      if (item.tool_state?.external_provider_authorized !== false || item.tool_state?.uploads_authorized !== false || item.tool_state?.image_generation !== 'not_available' || item.tool_state?.video_generation !== 'not_available' || item.tool_state?.audio_generation !== 'not_available') fail('LEARNING_EVAL_AUTHORITY', item.id);
    }
  } catch (error) { fail('LEARNING_PACKAGE', error.message); }
  return errors;
}
