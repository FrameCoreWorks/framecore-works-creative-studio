import fs from 'node:fs';
import path from 'node:path';
import {isDeepStrictEqual as equal} from 'node:util';
import {createHash} from 'node:crypto';

export const learningDomainIds = ['static_graphics', 'typography_layout', 'story_screenplay', 'performance', 'character_reference', 'storyboard_sequence', 'cinematography', 'commercial_video', 'music_video', 'copy_voice', 'prompting', 'audio_music', 'editing_motion', 'campaign_workflow'];
export const learningCaseIds = Array.from({length: 24}, (_, i) => 'LM' + String(i + 1).padStart(2, '0'));
export const canonicalWelcomeSha256 = '509afb18477debb7c4bf97be9d67d2dc086175b89a77755e9eed54072d5545b0';
export const englishWelcomeSha256 = 'e926662229b03b447bde8eebfe5024b9a07a1dadc8990a91b3765a9b87d3c378';

// Checks caller-supplied response text only. This does not invoke or observe a host.
// A single file-terminal LF is optional in a conversation response; nothing else
// is normalized, omitted or rewritten.
export function evaluateStartupReply(reply, expectedWelcome) {
  if (typeof expectedWelcome !== 'string' || !expectedWelcome.endsWith('\n') || !expectedWelcome.trim()) throw new Error('A complete canonical welcome file is required');
  if (typeof reply !== 'string') return {status: 'Unknown', scope: 'supplied_response_text', reason: 'No observed response text supplied'};
  const matches = reply === expectedWelcome || reply + '\n' === expectedWelcome;
  return {status: matches ? 'PASS' : 'FAIL', scope: 'supplied_response_text', matches_full_welcome: matches};
}

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
    need('skills/workflow-orchestrator/SKILL.md', [/Tryb nauki/, /Tryb tworzenia/, /references\/learning-mode\.md/, /creation immediately/, /never deliver the menu by itself/, /Quick\/Deep are a separate pace/]);
    need('skills/workflow-orchestrator/SKILL.md', [/references\/startup-and-creative-menus\.md/, /complete welcome/, /After a mode-only creative choice/, /After a pace-only choice/, /bare number only against a currently pending displayed choice group/]);
    need('skills/workflow-orchestrator/SKILL.md', [/assets\/startup-welcome\.en\.md/, /assets\/startup-welcome\.pl\.md/, /copy verbatim the entire file/, /Repeat the identical complete welcome on every sent Studio-only invocation/]);
    need('skills/workflow-orchestrator/assets/startup-welcome.pl.md', [/^Jestem FrameCore Works Creative Studio\./, /Mogę pomóc Ci w:/, /możesz dodać je teraz albo później/, /1\. \*\*Tryb kreatywny\*\*/, /2\. \*\*Tryb nauki\*\*/, /3\. \*\*Motion graphics z kodu\*\*/, /HTML\/SVG, GSAP, HyperFrames lub Remotion/, /podgląd i eksport zależą od narzędzi/, /Wpisz \*\*1\*\*, \*\*2\*\* albo \*\*3\*\*\.\s*$/]);
    const welcome = read('skills/workflow-orchestrator/assets/startup-welcome.pl.md');
    if (createHash('sha256').update(welcome).digest('hex') !== canonicalWelcomeSha256) fail('STARTUP_WELCOME_INTEGRITY', 'The protected Polish welcome has changed');
    const english = read('skills/workflow-orchestrator/assets/startup-welcome.en.md');
    if (createHash('sha256').update(english).digest('hex') !== englishWelcomeSha256) fail('STARTUP_WELCOME_INTEGRITY', 'The protected English welcome has changed');
    need('skills/workflow-orchestrator/assets/startup-welcome.en.md', [/^I am FrameCore Works Creative Studio\./, /I can help you with:/, /you can add them now or later/, /1\. \*\*Creative mode\*\*/, /2\. \*\*Learning mode\*\*/, /3\. \*\*Code-based motion graphics\*\*/, /HTML\/SVG, GSAP, HyperFrames or Remotion/, /preview and export depend on tools/, /Enter \*\*1\*\*, \*\*2\*\* or \*\*3\*\*\.\s*$/]);
    const entry = read('skills/workflow-orchestrator/SKILL.md');
    const begin = '<!-- BEGIN CANONICAL STARTUP RESPONSE -->\n';
    const end = '<!-- END CANONICAL STARTUP RESPONSE -->';
    const beginAt = entry.indexOf(begin), endAt = entry.indexOf(end);
    if (beginAt < 0 || endAt < beginAt || entry.indexOf(begin, beginAt + begin.length) >= 0 || entry.indexOf(end, endAt + end.length) >= 0 || entry.slice(beginAt + begin.length, endAt) !== welcome) fail('STARTUP_RESPONSE_PROJECTION', 'The complete startup excerpt must equal the canonical asset exactly');
    if (endAt < 0 || endAt >= entry.indexOf('Before final delivery') || endAt >= entry.indexOf('## Entry response first')) fail('STARTUP_RESPONSE_PLACEMENT', 'The full startup response must precede general review and routing instructions');
    const englishBegin = '<!-- BEGIN ENGLISH STARTUP RESPONSE -->\n';
    const englishEnd = '<!-- END ENGLISH STARTUP RESPONSE -->';
    const englishAt = entry.indexOf(englishBegin), englishEndAt = entry.indexOf(englishEnd);
    if (englishAt < 0 || englishEndAt < englishAt || entry.indexOf(englishBegin, englishAt + englishBegin.length) >= 0 || entry.indexOf(englishEnd, englishEndAt + englishEnd.length) >= 0 || entry.slice(englishAt + englishBegin.length, englishEndAt) !== english) fail('STARTUP_RESPONSE_PROJECTION', 'The complete English excerpt must equal its source exactly');
    if (englishEndAt < 0 || englishEndAt >= entry.indexOf('Before final delivery') || englishEndAt >= entry.indexOf('## Entry response first')) fail('STARTUP_RESPONSE_PLACEMENT', 'The English startup response must precede general review and routing instructions');
    const languageReference = 'skills/workflow-orchestrator/references/startup-and-creative-menus.md';
    const reference = read(languageReference);
    const policyBegin = '<!-- BEGIN STARTUP LANGUAGE POLICY -->';
    const policyEnd = '<!-- END STARTUP LANGUAGE POLICY -->';
    const policy = body => {
      const a = body.indexOf(policyBegin), b = body.indexOf(policyEnd);
      if (a < 0 || b < a || body.indexOf(policyBegin, a + policyBegin.length) >= 0 || body.indexOf(policyEnd, b + policyEnd.length) >= 0) return null;
      return body.slice(a, b + policyEnd.length);
    };
    if (!policy(entry) || policy(entry) !== policy(reference)) fail('STARTUP_LANGUAGE_PROJECTION', 'The early language policy must exactly match the reference');
    if (entry.indexOf(policyEnd) < 0 || entry.indexOf(policyEnd) >= englishAt || entry.indexOf(policyEnd) >= beginAt) fail('STARTUP_LANGUAGE_PLACEMENT', 'Select language before choosing a welcome');
    const languageRules = [/Select the response language before choosing or translating the welcome/, /explicit response-language preference/, /current user-authored conversational text/, /Ignore quoted material/, /host's response\/UI language only when actually supplied/, /most recent meaningful user conversation language/, /every signal is unavailable, use English as a provisional fallback/, /Never infer language from country/, /A user does not need to request translation/, /For any other language, translate the complete English welcome automatically/, /all six capability bullets/, /When the language changes, deliver the full welcome in the new language/, /Apply the same language selection to subsequent pace\/area menus and learning onboarding/, /preserving option order, reply tokens and their active state mapping/];
    for (const relative of ['skills/workflow-orchestrator/SKILL.md', languageReference]) {
      need(relative, languageRules);
      if (/Polish (?:is|remains) the default|Follow the\s+orchestrator's explicit-language rule/i.test(read(relative))) fail('STARTUP_FIXED_LANGUAGE', relative + ': fixed Polish default is superseded');
    }
    need('skills/workflow-orchestrator/SKILL.md', [/@FrameCore Works Creative Studio/, /never return only the two-mode choice/, /A two-option menu alone is a failed startup response/, /Concrete tasks and actual resume requests bypass this startup response/]);
    need('skills/workflow-orchestrator/references/startup-and-creative-menus.md', [/## Complete welcome/, /assets\/startup-welcome\.pl\.md/, /copy verbatim the entire file/, /Repeat the identical complete welcome on every sent Studio-only invocation/, /## Creative pace choice/, /1\. \*\*Tryb szybki\*\*/, /2\. \*\*Tryb rozbudowany\*\*/, /## Established work-area menu/, /1\. Grafika statyczna/, /2\. Wideo i prompty/, /7\. Analiza dostarczonej/, /bare number only against a currently pending displayed choice group/, /older 1\.2\.0 order/, /concrete project request bypasses menus/, /neither a concrete task nor a pace is supplied/]);
    need('skills/workflow-orchestrator/references/startup-and-creative-menus.md', [/## Motion graphics shortcut/, /not a third interaction mode/, /keep motion selected and skip the area menu/, /Preserve a runtime explicitly supplied/, /explicit request to learn motion graphics follows Learning Mode/, /8\. Motion graphics z kodu/, /Area `3` still selects storyboards/, /older still-pending two-option startup menu/, /Selecting the shortcut authorizes no installation/]);
    need('skills/workflow-orchestrator/SKILL.md', [/Motion shortcut answer/, /eight numbered work areas/, /If the motion shortcut already selected the area/, /motion shortcut.*references\/startup-and-creative-menus\.md#motion-graphics-shortcut/]);
    need('skills/workflow-orchestrator/references/intake-and-reference-authority.md', [/startup-and-creative-menus\.md/, /mode-only creative choice gets Quick\/Deep pace selection/]);
    need('skills/pipeline-core/references/studio-integration-policy.md', [/direct specialist invocation/, /learning overlay/, /Creation keeps the established production route/, /Ask exactly one onboarding question per response and wait/]);
    need('skills/studio-workstyle-profile/SKILL.md', [/learning overlay/, /ordinary one-question rule/, /Ask exactly one onboarding question per response and wait/]);
    need('skills/workflow-orchestrator/SKILL.md', [/Ask exactly one onboarding question per response and wait/]);
    need('skills/pipeline-core/templates/project-state.md', [/interaction_mode/, /learning_context/, /learning-progress\.template\.md/, /entry_context/, /last menu actually shown/]);
    const stateViews = ['skills/pipeline-core/templates/project-state.md', 'skills/pipeline-core/assets/project-state.md'];
    const stateFields = ['interaction_mode', 'pace', 'entry_context', 'learning_context'];
    for (const view of stateViews) need(view, [/checkpoint_id/, /checkpoint_status/, /updated_utc/, /interaction_mode/, /pace/, /entry_context/, /learning_context/, /pending_choice_groups/, /one pending question/, /learning-progress\.template\.md/]);
    for (const field of stateFields) {
      const pattern = new RegExp('^- ' + field + ':.*$', 'm');
      const values = stateViews.map(view => read(view).match(pattern)?.[0]);
      if (!values[0] || values[0] !== values[1]) fail('LEARNING_STATE_CONTRACT', field + ': portable and durable state fields differ');
    }
    need('skills/workflow-orchestrator/assets/cross-host-handoff.template.md', [/interaction_mode/, /pace/, /entry_context/, /learning_context/, /pending_choice_groups/, /at most one pending question/, /learning-progress\.template\.md/, /never reactivate completed menus/]);
    need('skills/pipeline-core/references/project-recovery.md', [/learning_context/, /learning-progress\.template\.md/]);
    const method = 'skills/workflow-orchestrator/references/learning-mode.md';
    need(method, [/## Onboarding/, /at most six short questions/, /Ask exactly one onboarding question per response and wait/, /Do not group onboarding questions/, /a natural-language answer/, /Do not ask an already answered question/, /optional blanks do not block/i, /## Personal plan/, /shared foundations/, /all requested supported specializations/, /begin the first lesson/, /plan-only/, /## Lesson cycle/, /Stop for the learner's attempt/, /one or two priority improvements/, /## Switching and project work/, /switches to creation immediately/, /## Progress and recovery/, /Do not mark a lesson completed merely because it was displayed/, /Do not promise persistent memory or cross-host sync/, /## Research, costs and limits/, /first offers a no-render alternative/, /Learning alone authorizes no generation/, /No free-use guarantee follows from a ChatGPT subscription/]);
    need('skills/workflow-orchestrator/assets/learning-plan.template.md', [/independent_outcome/, /domain_ids/, /sequence_reason/, /learner_action/, /assessment/, /tools_costs/, /no_render_alternative/, /estimated_effort/, /integrative_project/, /plan_only/]);
    need('skills/workflow-orchestrator/assets/learning-progress.template.md', [/level_by_domain/, /current_module/, /completed_lessons/, /skipped_lessons/, /strengths/, /practice_needs/, /next_action/, /persistence/, /onboarding_context/, /known\/unknown\/skipped answers/, /questions asked/, /six-question limit/, /at most one pending question/, /displayed token-to-option mapping/, /Remove answered\/skipped\/replaced pending questions/]);
    need('skills/workflow-orchestrator/SKILL.md', [/learning-mode\.md#diagnostic-first-attempt/, /at most one pending learner exercise/]);
    need(method, [/## Diagnostic first attempt/, /inside the first lesson, not in additional onboarding/, /plan-only receives no diagnostic exercise/, /Reuse a relevant supplied attempt/, /keep the unobserved skill Unknown/, /## Graduated assistance/, /Honor a request for a full explanation immediately/, /Fade assistance after successful attempts/, /strongest solution-bearing help/, /## Evidence of independence/, /independent_familiar/, /independent_transfer/, /Keep learner-reported performance labelled separately/, /Keep lesson completion, output quality and independence separate/, /## Retrieval and transfer/, /at most one `pending_practice`/, /before revealing the answer/, /not a reminder/, /## Feedback and causal diagnosis/, /cause_category/, /A failed render alone proves no specific cause/, /## One evolving learning project/, /short new-context tasks/, /Missing or older fields|missing or older fields/]);
    const practiceFields = ['diagnostic_attempt', 'competency_evidence', 'assistance_used', 'review_queue', 'pending_practice', 'feedback_diagnosis', 'learning_project'];
    for (const view of [...stateViews, 'skills/workflow-orchestrator/assets/cross-host-handoff.template.md', 'skills/workflow-orchestrator/assets/learning-progress.template.md']) need(view, practiceFields.map(field => new RegExp(field)));
    need('skills/workflow-orchestrator/assets/learning-plan.template.md', [/diagnostic_attempt/, /assistance_plan/, /learning_project/, /review_queue/, /competency_evidence/]);
    need('skills/workflow-orchestrator/references/startup-and-creative-menus.md', [/when a production task calls for grouped choices/, /Learning onboarding still asks exactly one question at a time/]);
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
    if (!equal(suite.cases.map(c => c.id).sort(), learningCaseIds)) fail('LEARNING_CASE_COVERAGE', 'Expected LM01 through LM24 once each');
    for (const item of suite.cases) {
      if (item.status !== 'planned' || item.execution_status !== 'not_run' || !strings(item.required_evidence) || !strings(item.expected_owners) || !strings(item.checks) || !['learning', 'creation', 'undecided'].includes(item.expected_interaction_mode)) fail('LEARNING_EVAL', String(item.id));
      for (const owner of item.expected_owners ?? []) if (!packageFiles.includes('skills/' + owner + '/SKILL.md')) fail('LEARNING_EVAL_OWNER', item.id + ': ' + owner);
      if (item.research_expectation === 'required' && !item.expected_owners?.includes('research-evidence')) fail('LEARNING_RESEARCH_OWNER', item.id);
      if (item.tool_state?.external_provider_authorized !== false || item.tool_state?.uploads_authorized !== false || item.tool_state?.image_generation !== 'not_available' || item.tool_state?.video_generation !== 'not_available' || item.tool_state?.audio_generation !== 'not_available') fail('LEARNING_EVAL_AUTHORITY', item.id);
    }
  } catch (error) { fail('LEARNING_PACKAGE', error.message); }
  return errors;
}
