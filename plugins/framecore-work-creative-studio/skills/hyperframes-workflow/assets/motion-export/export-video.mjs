// Export a motion contract to a video file with a local Chrome or Chromium, through the same browser
// export as the single-file preview's Export video button. Dependency-free (Node 20+); it talks to the
// browser over the DevTools pipe and writes MP4 (H.264) when the browser can encode it, otherwise WebM.
// Video only. Exit code: 0 written, 2 setup or export problem.
//
//   node export-video.mjs motion-score.json --out film.mp4 [--format 9x16] [--container mp4|webm] [--browser /path/to/chrome]
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {previewFor, findBrowser} from '../motion-review/review-frames.mjs';

/** Minimal DevTools protocol client over --remote-debugging-pipe (fd 3 in, fd 4 out, NUL-separated JSON). */
function devtools(chrome, args) {
  const child = spawn(chrome, [...args, '--remote-debugging-pipe'], {stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe']});
  const waiting = new Map();
  let next = 1, buffer = '', stderr = '';
  child.stderr.on('data', data => { stderr = (stderr + data).slice(-2000); });
  child.stdio[4].on('data', data => {
    buffer += data;
    let end;
    while ((end = buffer.indexOf('\0')) >= 0) {
      const message = JSON.parse(buffer.slice(0, end)); buffer = buffer.slice(end + 1);
      const pending = waiting.get(message.id);
      if (!pending) continue;
      waiting.delete(message.id);
      if (message.error) pending.reject(new Error(message.error.message)); else pending.resolve(message.result);
    }
  });
  const failAll = reason => { for (const pending of waiting.values()) pending.reject(new Error(`${reason}${stderr ? `: ${stderr.trim().slice(-300)}` : ''}`)); waiting.clear(); };
  child.on('exit', () => failAll('The browser exited'));
  child.on('error', error => failAll(error.message));
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const id = next++;
    waiting.set(id, {resolve, reject});
    child.stdio[3].write(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})}) + '\0');
  });
  const exited = new Promise(resolve => child.once('exit', resolve));
  return {send, close: () => { child.kill(); return Promise.race([exited, new Promise(resolve => setTimeout(resolve, 5000))]); }};
}

export async function exportFile(input, {out, format, container, browser} = {}) {
  if (!out) throw new Error('Choose a new output file with --out');
  const chrome = findBrowser(browser);
  if (!chrome) throw new Error('No Chrome or Chromium found; pass --browser or set CHROME_PATH');
  const {html} = previewFor(input);
  const work = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-export-'));
  const page = path.join(work, 'preview.html');
  fs.writeFileSync(page, html);
  const args = ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${path.join(work, 'profile')}`, 'about:blank'];
  if (process.platform === 'linux' && process.getuid?.() === 0) args.unshift('--no-sandbox');
  const browserSession = devtools(chrome, args);
  try {
    const {targetId} = await browserSession.send('Target.createTarget', {url: `${pathToFileURL(page).href}${format && format !== 'base' ? `?format=${encodeURIComponent(format)}` : ''}`});
    const {sessionId} = await browserSession.send('Target.attachToTarget', {targetId, flatten: true});
    const evaluate = async expression => {
      const {result, exceptionDetails} = await browserSession.send('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true}, sessionId);
      if (exceptionDetails) throw new Error(exceptionDetails.exception?.description?.split('\n')[0] ?? exceptionDetails.text);
      return result.value;
    };
    for (let i = 0; i < 300 && (await evaluate("document.documentElement.dataset.ready || ''")) !== 'true'; i++) await new Promise(resolve => setTimeout(resolve, 100));
    const result = await evaluate(`window.exportVideoBase64(${JSON.stringify({container})})`);
    let target = out;
    if (path.extname(out) && path.extname(out).slice(1).toLowerCase() !== result.extension) {
      target = out.slice(0, -path.extname(out).length) + '.' + result.extension;
      console.warn(`WARN this browser produced ${result.extension.toUpperCase()}; writing ${target}`);
    } else if (!path.extname(out)) target = `${out}.${result.extension}`;
    if (fs.existsSync(target)) throw new Error(`Output file already exists: ${target}`);
    const bytes = Buffer.from(result.base64, 'base64');
    fs.writeFileSync(target, bytes);
    return {file: target, container: result.container, codec: result.codec, frames: result.frames, bytes: bytes.length, ms: result.ms, browser: path.basename(chrome)};
  } finally {
    await browserSession.close();
    fs.rmSync(work, {recursive: true, force: true, maxRetries: 5, retryDelay: 200});
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), valued = ['--out', '--format', '--container', '--browser'];
  const option = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const input = args.find((arg, i) => !arg.startsWith('--') && !valued.includes(args[i - 1]));
  try {
    if (!input) throw new Error('Usage: node export-video.mjs <motion-score.json | motion-preview.html> --out <new file> [--format <id>] [--container mp4|webm] [--browser <path>]');
    const result = await exportFile(input, {out: option('--out'), format: option('--format'), container: option('--container'), browser: option('--browser')});
    console.log(`Wrote ${result.file}: ${result.frames} frames, ${result.codec} in ${result.container.toUpperCase()}, ${(result.bytes / 1048576).toFixed(1)} MB, video only, encoded in ${(result.ms / 1000).toFixed(1)} s.`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
