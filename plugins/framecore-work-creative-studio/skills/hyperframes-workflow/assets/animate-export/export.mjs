#!/usr/bin/env node
// Studio's caption-path fix for the pinned Animate exporter. The upstream files stay byte-identical.
// Run a guarded temporary copy so format recursion, rendering and audio retain upstream behavior.
// Usage: node export.mjs pieces/<name> --engine <installed-animate-engine> [upstream export options]
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';

// integrations/animate/source-manifest.json: tools/export.mjs at the reviewed 7e5eb56 commit.
const EXPORT_BLOB = '1338167bd20a0253b2f18c8629d2b33dcbd7720c';

export function adaptedExporter(engine) {
  const exporter = path.resolve(engine, 'tools/export.mjs');
  const bytes = fs.readFileSync(exporter);
  const blob = createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex');
  if (blob !== EXPORT_BLOB) throw new Error('Animate exporter differs from the reviewed source; use the pinned Studio workspace copy.');
  let source = bytes.toString('utf8');
  const replace = (before, after) => {
    if (source.split(before).length !== 2) throw new Error('Animate exporter adapter does not match its pinned source.');
    source = source.replace(before, () => after);
  };
  // A temporary module still resolves the engine's own driver and GPU helper, without copying its dependencies.
  replace("from './gpu.mjs'", `from ${JSON.stringify(pathToFileURL(path.resolve(engine, 'tools/gpu.mjs')).href)}`);
  replace('createRequire(import.meta.url)', `createRequire(${JSON.stringify(pathToFileURL(exporter).href)})`);
  replace("[process.argv[1], argv[0], ...rest, '--format', f]",
    "[process.argv[1], argv[0], ...rest, '--format', f, '--studio-format-output']");
  replace("  const out = path.join(RENDERS, opt('out', `final${SUFFIX}.mp4`));", `  const requested = opt('out');
  const named = requested && flag('studio-format-output') && SUFFIX
    ? path.join(path.dirname(requested), path.parse(requested).name + SUFFIX + path.extname(requested)) : requested;
  const out = path.join(RENDERS, named || \`final\${SUFFIX}.mp4\`);
  fs.mkdirSync(path.dirname(out), {recursive: true});
  const captionOut = path.join(path.dirname(out), path.parse(out).name + '-captions.mp4');`);
  replace("'-i', 'final.mp4',", "'-i', out,");
  replace("'-c:a', 'copy', 'final-captions.mp4'", "'-c:a', 'copy', captionOut");
  replace("path.join(RENDERS, 'final-captions.mp4'), '(narration preview)'", "captionOut, '(narration preview)'");
  return source;
}

export function main(argv = process.argv.slice(2)) {
  const args = [...argv];
  const engineOption = args.indexOf('--engine');
  if (engineOption < 0 || !args[engineOption + 1] || args[engineOption + 1].startsWith('--')) {
    throw new Error('Usage: node export.mjs <piece> --engine <installed-animate-engine> [export options]');
  }
  const engine = path.resolve(args[engineOption + 1]);
  args.splice(engineOption, 2);
  if (!args[0] || args[0].startsWith('--')) throw new Error('Give the piece directory before export options.');
  const source = adaptedExporter(engine);
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-animate-export-'));
  try {
    const executable = path.join(temporary, 'export.mjs');
    fs.writeFileSync(executable, source);
    const done = spawnSync(process.execPath, [executable, ...args], {stdio: 'inherit'});
    if (done.error) throw done.error;
    return done.status ?? 1;
  } finally {
    fs.rmSync(temporary, {recursive: true, force: true});
  }
}

if (process.argv[1] && fs.existsSync(process.argv[1]) && fs.realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { process.exitCode = main(); }
  catch (error) { console.error(error.message); process.exitCode = 2; }
}
