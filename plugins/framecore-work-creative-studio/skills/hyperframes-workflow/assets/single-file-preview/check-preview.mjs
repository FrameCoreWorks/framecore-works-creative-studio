// Check a delivered single-file preview against the template: everything except the embedded motion
// contract must be unchanged, and the contract must pass check-score.mjs with a scene kind on every scene.
// Dependency-free (Node 20+). Exit code: 0 pass, 1 findings, 2 setup problem.
//
//   node check-preview.mjs delivered-preview.html
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {checkScore} from '../gsap-motion-starter/check-score.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const scoreBlock = /(<script type="application\/json" id="motion-score">\n)([\s\S]*?)(\n<\/script>)/;
const regions = [
  ['scene engine', '// BEGIN motion-scenes engine', '// END motion-scenes engine'],
  ['video export', '// BEGIN video export', '// END video export'],
];

/** Compare a preview with the template. Returns {errors, warnings, unchanged, regions}. */
export function checkPreview(html, template = fs.readFileSync(path.join(here, 'motion-preview.html'), 'utf8')) {
  const errors = [], warnings = [];
  const match = html.match(scoreBlock);
  if (!match) return {errors: ['No embedded motion contract (<script type="application/json" id="motion-score">) found; deliver the template with only the contract replaced'], warnings, unchanged: false, regions: {}};
  const outside = text => text.replace(scoreBlock, '$1$3');
  const unchanged = outside(html) === outside(template);
  const state = {};
  for (const [name, begin, end] of regions) {
    const pick = text => (text.includes(begin) && text.includes(end) ? text.slice(text.indexOf(begin), text.indexOf(end)) : null);
    const delivered = pick(html);
    state[name] = delivered === null ? 'missing' : delivered === pick(template) ? 'identical' : 'changed';
    if (state[name] !== 'identical') errors.push(`The ${name} is ${state[name]}; copy it from the template byte for byte`);
  }
  if (!unchanged && !errors.length) errors.push('The player outside the contract differs from the template; replace only the motion contract');
  let score;
  try { score = JSON.parse(match[2]); } catch (error) { errors.push(`The motion contract is not valid JSON: ${error.message}`); }
  if (score) {
    const result = checkScore(score);
    errors.push(...result.errors.map(error => `Contract: ${error}`));
    warnings.push(...result.warnings.map(warning => `Contract: ${warning}`));
    for (const scene of score.scenes ?? []) if (!scene.kind) errors.push(`Contract: scene ${scene.id} declares no kind, so the template cannot draw it`);
  }
  return {errors, warnings, unchanged, regions: state};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const file = process.argv[2];
  try {
    if (!file) throw new Error('Usage: node check-preview.mjs <delivered-preview.html>');
    const {errors, warnings, unchanged} = checkPreview(fs.readFileSync(file, 'utf8'));
    for (const warning of warnings) console.warn('WARN ' + warning);
    for (const error of errors) console.error('FAIL ' + error);
    console.log(errors.length ? 'FAIL' : `PASS${unchanged ? ': template unchanged except the motion contract' : ''}`);
    process.exitCode = errors.length ? 1 : 0;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
