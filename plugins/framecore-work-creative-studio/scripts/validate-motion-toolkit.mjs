import fs from 'node:fs';
import path from 'node:path';
import {isDeepStrictEqual} from 'node:util';

const canvas = 'skills/hyperframes-workflow/assets/motion-toolkit';
const three = 'skills/remotion-video-production/assets/three-motion-example';
const kinetic = 'skills/remotion-video-production/assets/kinetic-type-starter';
const gsapStarter = 'skills/hyperframes-workflow/assets/gsap-motion-starter';
export function validateMotionToolkit(root) {
  const errors = [];
  const fail = detail => errors.push({code: 'MOTION_TOOLKIT', detail});
  const read = relative => fs.readFileSync(path.join(root, relative), 'utf8');
  const required = [
    ...['README.md','package.json','package-lock.json','index.html','app.mjs','build.mjs','server.mjs','timeline.mjs','timeline.test.mjs','renderers.mjs','lottie-fixture.mjs','export.mjs'].map(name => `${canvas}/${name}`),
    ...['README.md','package.json','package-lock.json','tsconfig.json','remotion.config.ts','src/index.tsx'].map(name => `${three}/${name}`),
    ...['README.md','package.json','package-lock.json','tsconfig.json','remotion.config.ts','check-score.mjs','motion-score.json','src/index.ts','src/Root.tsx','src/motion.ts','src/KineticType.tsx'].map(name => `${kinetic}/${name}`),
    ...['README.md','package.json','package-lock.json','index.html','main.mjs','check-score.mjs','motion-score.json'].map(name => `${gsapStarter}/${name}`),
    'skills/hyperframes-workflow/references/motion-craft.md',
    ...['motion-toolkit-routing.md','motion-toolkit-runtime-cards.md','motion-toolkit-sources.md'].map(name => `skills/hyperframes-workflow/references/${name}`),
    'skills/hyperframes-workflow/templates/motion-toolkit-acceptance.md',
    'skills/hyperframes-workflow/assets/manim-motion-example.py'
  ];
  for (const relative of required) {
    try {if (!read(relative).trim()) fail(`Empty: ${relative}`);} catch {fail(`Missing: ${relative}`);}
  }
  for (const directory of [canvas, three, kinetic, gsapStarter]) {
    try {
      const pkg = JSON.parse(read(`${directory}/package.json`));
      const lock = JSON.parse(read(`${directory}/package-lock.json`));
      if (pkg.private !== true || lock.lockfileVersion !== 3) fail(`${directory}: private example and lockfile v3 required`);
      for (const group of ['dependencies', 'devDependencies']) {
        if (!isDeepStrictEqual(pkg[group], lock.packages[''][group])) fail(`${directory}: ${group} lock mismatch`);
        for (const [name, version] of Object.entries(pkg[group] ?? {})) {
          if (!/^\d+\.\d+\.\d+$/.test(version)) fail(`${directory}: ${name} needs an exact version`);
          if (lock.packages[`node_modules/${name}`]?.version !== version) fail(`${directory}: ${name} resolved version mismatch`);
        }
      }
      const remotion = Object.entries(pkg.dependencies ?? {}).filter(([name]) => name === 'remotion' || name.startsWith('@remotion/'));
      if (new Set(remotion.map(([, version]) => version)).size > 1) fail(`${directory}: Remotion versions differ`);
      for (const unwanted of ['node_modules','dist','out']) if (fs.existsSync(path.join(root,directory,unwanted))) fail(`${directory}: ${unwanted} must stay outside the installed package`);
    } catch (error) {fail(`${directory}: ${error.message}`);}
  }
  // Both starters must share one contract and one checker so runtimes stay comparable.
  for (const file of ['motion-score.json', 'check-score.mjs']) {
    try { if (read(`${kinetic}/${file}`) !== read(`${gsapStarter}/${file}`)) fail(`Starter ${file} differs between runtimes`); } catch {}
  }
  return errors;
}
