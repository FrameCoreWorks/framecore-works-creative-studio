import fs from 'node:fs';
import path from 'node:path';
import {validateExampleBank, checkArtifact} from './quality-harness.mjs';

// Source/asset validation only. Never invokes a model or marks host fixtures executed.
export function validateQualityMethods(root) {
  const errors = [], read = file => fs.readFileSync(path.join(root, file), 'utf8');
  const fail = detail => errors.push({code: 'QUALITY_METHODS', detail});
  const requireText = (file, phrases) => {
    try {const body = read(file); for (const phrase of phrases) if (!body.includes(phrase)) fail(file + ': missing ' + phrase);}
    catch (error) {fail(error.message);}
  };
  const profile = 'skills/pipeline-core/references/quality-improvement-methods.md';
  requireText(profile, ['## Relevant examples', '## Tool-backed verification (CRITIC-inspired)', '## Calibrated pairwise evaluation', '## Controlled Reflexion lessons', '## Offline GEPA pilot', 'No method resets this budget', 'Passing work stops unchanged', 'order_disagreement', 'No automatic adoption', 'not media certification', 'never raw reasoning traces']);
  requireText('skills/pipeline-core/references/inference-reasoning-methods.md', ['quality-improvement-methods.md']);
  requireText('skills/static-graphic-design-creator/SKILL.md', ['After an unexplained rejection', 'Apply an already explained correction directly']);
  requireText('skills/commercial-visual-campaign-director/SKILL.md', ['Hand a selected direction for static execution to [Static Graphic Design Creator]']);
  requireText('skills/commercial-video-campaign-director/references/creative-decision-library.md', ['decision-examples.json', 'one to three examples']);
  requireText('skills/output-critic-iteration/SKILL.md', ['quality-improvement-methods.md#tool-backed-verification-critic-inspired', 'quality-improvement-methods.md#calibrated-pairwise-evaluation']);
  requireText('skills/workflow-self-improvement/SKILL.md', ['quality-improvement-methods.md#controlled-reflexion-lessons', 'assets/reflexion-lesson.template.json']);
  try {
    const bank = JSON.parse(read('skills/commercial-video-campaign-director/assets/decision-examples.json'));
    for (const error of validateExampleBank(bank)) fail(error);
    if (bank.examples?.length !== 8 || bank.examples.filter(e => e.domain === 'static').length !== 4) fail('Expected eight teaching cases, four static anchors');
    const example = JSON.parse(read('skills/output-critic-iteration/assets/quality-review.example.json'));
    if (checkArtifact(example.contract, example.observation).status !== 'PASS' || example.observation.kind !== 'plan') fail('Synthetic plan evidence example must pass its declared scope');
    const template = JSON.parse(read('skills/workflow-self-improvement/assets/reflexion-lesson.template.json'));
    if (template.status !== 'proposed' || template.test?.result !== 'NOT_RUN' || template.adoption?.explicit !== false || template.persistence !== 'not_performed') fail('Blank lesson must not imply testing/adoption/persistence');
    const host = JSON.parse(read('evals/studio-behavior-cases.json')).cases;
    const practice = JSON.parse(read('evals/knowledge-practice-cases.json')).cases;
    for (const [id, owners] of [['H01', ['copy-voice']], ['H02', ['static-graphic-design-creator']], ['KP02', ['commercial-visual-campaign-director', 'static-graphic-design-creator']]]) {
      const item = [...host, ...practice].find(c => c.id === id);
      if (JSON.stringify(item?.expected_owners) !== JSON.stringify(owners) || item?.execution_status !== 'not_run' || item?.status !== 'planned') fail('Owner/evidence regression: ' + id);
    }
  } catch (error) {fail(error.message);}
  return errors;
}
