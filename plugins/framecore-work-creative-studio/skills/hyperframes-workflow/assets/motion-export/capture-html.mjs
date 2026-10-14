// Render any hand-written HTML composition (canvas, GSAP, DOM) to MP4 with a local Chrome or Chromium and FFmpeg,
// frame by frame from the frame number, without npm. The route for a shell host where the npm registry is
// unreachable, so `npx hyperframes` cannot run. Dependency-free (Node 20+); talks to the browser over its DevTools pipe.
//
//   node capture-html.mjs outro.html --out outro-9x16.mp4 --width 1080 --height 1920 --seconds 6 [--fps 30 | 30000/1001]
//        [--query fmt=9x16] [--audio mix.wav] [--browser /path/to/chrome]
//
// Page contract: `window.ready` (optional) is a promise that resolves when fonts and images are loaded, and
// `window.renderFrame(t)` draws the state at t seconds from t alone (it may return a promise). No wall clock,
// no unseeded randomness, so frame 120 renders the same whether or not frames 0 to 119 were drawn.
// Exit code: 0 written, 2 setup or capture problem.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn, spawnSync} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {devtools} from './export-video.mjs';
import {findBrowser} from '../motion-review/review-frames.mjs';

/** A Chrome or Chromium: the explicit path, CHROME_PATH, HYPERFRAMES_BROWSER_PATH, the usual names, Playwright's folders. */
export function locateBrowser(explicit) {
  return findBrowser(explicit);
}

/** Frame rate as a fraction: "30", "29.97" is refused, "30000/1001". */
export function parseFps(value = '30') {
  const [num, den = '1'] = String(value).split('/');
  if (!/^\d+$/.test(num) || !/^\d+$/.test(den) || Number(num) === 0 || Number(den) === 0) throw new Error(`Frame rate must be an integer or N/D, got ${value}`);
  return {num: Number(num), den: Number(den)};
}

/** Frame count for a duration: the frames whose start lies before the end, from absolute time. */
export function frameCount(seconds, fps) {
  return Math.round(seconds * fps.num / fps.den);
}

/** Frames actually written to the file (ffprobe), or null when ffprobe is not installed. */
export function encodedFrames(file) {
  const probe = spawnSync('ffprobe', ['-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', file], {encoding: 'utf8'});
  if (probe.error) return null;
  const frames = parseInt(probe.stdout, 10);
  return Number.isFinite(frames) ? frames : null;
}

/** The FFmpeg arguments for the frame pipe and optional audio. The picture sets the length: shorter audio is padded
 * with silence and longer audio is cut at the last frame (-shortest would end the film with a short voice-over). */
export function encoderArgs({out, rate, total, audio, crf = 16}) {
  const args = ['-hide_banner', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', `${rate.num}/${rate.den}`, '-i', '-'];
  const length = (total * rate.den / rate.num).toFixed(6);
  if (audio) args.push('-i', audio, '-map', '0:v:0', '-map', '1:a:0', '-af', 'apad', '-c:a', 'aac', '-b:a', '192k', '-t', length);
  args.push('-c:v', 'libx264', '-crf', String(crf), '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out);
  return args;
}

export async function captureFile(input, {out, width, height, seconds, frames, fps = '30', query, audio, browser, crf = 16} = {}) {
  if (!out) throw new Error('Choose a new output file with --out');
  if (fs.existsSync(out)) throw new Error(`Output file already exists: ${out}`);
  if (!input || !fs.existsSync(input)) throw new Error(`Page not found: ${input}`);
  if (!width || !height) throw new Error('Give --width and --height in pixels');
  if (width % 2 || height % 2) throw new Error('H.264 with yuv420p needs an even width and height');
  const rate = parseFps(fps);
  const total = frames ? Number(frames) : frameCount(Number(seconds), rate);
  if (!Number.isInteger(total) || total < 1) throw new Error('Give --seconds or --frames');
  const chrome = locateBrowser(browser);
  if (!chrome) throw new Error('No Chrome or Chromium found; pass --browser or set CHROME_PATH or HYPERFRAMES_BROWSER_PATH');
  const work = fs.mkdtempSync(path.join(os.tmpdir(), 'capture-html-'));
  const args = ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--disable-background-networking', '--disable-component-update',
    '--force-device-scale-factor=1', `--user-data-dir=${path.join(work, 'profile')}`, 'about:blank'];
  if (process.platform === 'linux' && process.getuid?.() === 0) args.unshift('--no-sandbox');
  const session = devtools(chrome, args);
  const ffmpegArgs = encoderArgs({out, rate, total, audio, crf});
  const encoder = spawn('ffmpeg', ffmpegArgs, {stdio: ['pipe', 'ignore', 'pipe']});
  let encoderError = '';
  encoder.stderr.on('data', data => { encoderError = (encoderError + data).slice(-2000); });
  const encoded = new Promise((resolve, reject) => {
    encoder.on('error', error => reject(new Error(`FFmpeg could not start: ${error.message}`)));
    encoder.on('exit', code => code === 0 ? resolve() : reject(new Error(`FFmpeg failed: ${encoderError.trim().slice(-300)}`)));
  });
  encoded.catch(() => {});   // a failure is reported once, from the frame loop or from awaiting it below
  const started = Date.now();
  try {
    const url = pathToFileURL(path.resolve(input)).href + (query ? `?${query}` : '');
    const {targetId} = await session.send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await session.send('Target.attachToTarget', {targetId, flatten: true});
    const send = (method, params) => session.send(method, params, sessionId);
    await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: 1, mobile: false});
    await send('Page.enable');
    await send('Page.navigate', {url});
    const evaluate = async expression => {
      const {result, exceptionDetails} = await send('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true});
      if (exceptionDetails) throw new Error(exceptionDetails.exception?.description?.split('\n')[0] ?? exceptionDetails.text);
      return result.value;
    };
    let ready = false;
    for (let i = 0; i < 300 && !ready; i++) {
      ready = await evaluate("document.readyState === 'complete' && typeof window.renderFrame === 'function'").catch(() => false);
      if (!ready) await new Promise(resolve => setTimeout(resolve, 100));
    }
    if (!ready) throw new Error('The page did not define window.renderFrame(t) within 30 seconds');
    await evaluate('Promise.resolve(window.ready).then(() => document.fonts ? document.fonts.ready : null).then(() => true)');
    for (let frame = 0; frame < total; frame++) {
      await evaluate(`Promise.resolve(window.renderFrame(${frame * rate.den / rate.num})).then(() => new Promise(r => requestAnimationFrame(() => r(true))))`);
      const {data} = await send('Page.captureScreenshot', {format: 'png', clip: {x: 0, y: 0, width, height, scale: 1}});
      if (!encoder.stdin.write(Buffer.from(data, 'base64'))) await new Promise(resolve => encoder.stdin.once('drain', resolve));
    }
    encoder.stdin.end();
    await encoded;
    const written = encodedFrames(out);
    if (written !== null && written !== total) throw new Error(`The encoded file has ${written} frames, not ${total}`);
    return {file: out, frames: total, fps: `${rate.num}/${rate.den}`, width, height, audio: Boolean(audio), ms: Date.now() - started, browser: path.basename(chrome)};
  } catch (error) {
    encoder.stdin.destroy();
    encoder.kill();
    try { fs.rmSync(out, {force: true}); } catch {}
    throw error;
  } finally {
    await session.close();
    try { fs.rmSync(work, {recursive: true, force: true, maxRetries: 10, retryDelay: 300}); } catch (error) { console.warn(`WARN could not remove the temporary folder ${work}: ${error.message}`); }
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const valued = ['--out', '--width', '--height', '--seconds', '--frames', '--fps', '--query', '--audio', '--browser', '--crf'];
  const option = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const input = args.find((arg, i) => !arg.startsWith('--') && !valued.includes(args[i - 1]));
  try {
    if (!input) throw new Error('Usage: node capture-html.mjs <page.html> --out <new.mp4> --width <px> --height <px> --seconds <s> [--fps 30|N/D] [--query k=v] [--audio file] [--browser path]');
    const result = await captureFile(input, {out: option('--out'), width: Number(option('--width')), height: Number(option('--height')),
      seconds: option('--seconds'), frames: option('--frames'), fps: option('--fps'), query: option('--query'), audio: option('--audio'),
      browser: option('--browser'), crf: option('--crf') ?? 16});
    console.log(`Wrote ${result.file}: ${result.frames} frames at ${result.fps} fps, ${result.width} x ${result.height}, H.264${result.audio ? ' with audio' : ', video only'}, in ${(result.ms / 1000).toFixed(1)} s.`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
