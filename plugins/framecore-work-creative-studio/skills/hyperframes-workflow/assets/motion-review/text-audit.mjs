// Visible-text audit for any HTML motion composition (Studio preview, HyperFrames, GSAP or hand-written HTML),
// in a local Chrome or Chromium. Dependency-free (Node 20+). At each sample time it seeks the composition, waits
// for fonts, and checks that every visible word is complete inside the frame and every clipping ancestor
// (text-audit.browser.js). A clipped word in a readable hold is an error; during a transition it is reported as
// transitional. Holds come from --holds, from a Studio contract, or are inferred: a sample whose text geometry is
// unchanged 0.2 s later counts as held. Exit code: 0 no errors, 1 errors, 2 setup problem.
//
//   node text-audit.mjs composition.html --out audit-out --times 1,4.5,9 [--holds 0.6-3,3.4-7.6] [--fps 30]
//        [--width 1080 --height 1920] [--root '#root'] [--seek 'window.__timelines.main.seek(T, false)'] [--browser path]
//   node text-audit.mjs motion-score.json --out audit-out          (Studio contract: its review frames and holds)
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {findBrowser, previewFor, selectFrames} from './review-frames.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export const auditScript = () => fs.readFileSync(path.join(here, 'text-audit.browser.js'), 'utf8');
const STEP = 0.2;

// Seeking: Studio's preview (seekFrame), HyperFrames (window.__timelines plus data-start/data-duration clips),
// a page-wide GSAP timeline, or a caller expression with T (seconds) and F (frame).
const seeker = expression => `
async function __studioSeek(T, F) {
  ${expression ? `${expression};` : `
  if (typeof window.seekFrame === 'function') { window.seekFrame(F); return 'studio-preview'; }
  const timelines = window.__timelines && Object.values(window.__timelines).filter(t => t && typeof t.seek === 'function');
  if (timelines && timelines.length) {
    for (const t of timelines) { if (t.pause) t.pause(); t.seek(T, false); }
    for (const clip of document.querySelectorAll('[data-start]')) {
      if (clip.matches('[data-composition-id]')) continue;
      const start = Number(clip.getAttribute('data-start')), length = Number(clip.getAttribute('data-duration'));
      if (Number.isFinite(start)) clip.style.visibility = T >= start && (!Number.isFinite(length) || T < start + length) ? '' : 'hidden';
    }
    return 'hyperframes-timelines';
  }
  if (window.gsap && window.gsap.globalTimeline) { window.gsap.globalTimeline.pause(); window.gsap.globalTimeline.seek(T, false); return 'gsap-global'; }
  for (const a of document.getAnimations ? document.getAnimations() : []) { a.pause(); a.currentTime = T * 1000; }
  return document.getAnimations && document.getAnimations().length ? 'web-animations' : 'static';`}
  return 'expression';
}`;

const runner = options => `
<script>
${auditScript()}
${seeker(options.seek)}
(async () => {
  const query = new URLSearchParams(location.search), T = Number(query.get('t')), F = Number(query.get('f'));
  const out = document.createElement('script'); out.type = 'application/json'; out.id = 'text-audit-report';
  try {
    if (document.readyState !== 'complete') await new Promise(r => window.addEventListener('load', r, {once: true}));
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    const mode = await __studioSeek(T, F);
    void document.body.offsetHeight; // style and layout are flushed synchronously before measuring
    out.textContent = JSON.stringify({t: T, seek: mode, ...window.__studioTextAudit(${JSON.stringify({root: options.root, width: options.width, height: options.height})})});
  } catch (error) {
    out.textContent = JSON.stringify({t: T, error: String(error && error.message || error)});
  }
  document.body.append(out);
})();
</script>`;

export function parseRanges(text) {
  if (!text) return null;
  return text.split(',').map(part => part.trim()).filter(Boolean).map(part => {
    const [a, b] = part.split('-').map(Number);
    if (!(b > a)) throw new Error(`Bad range ${part}; use start-end in seconds`);
    return [a, b];
  });
}

/** The composition page to audit and its sampling plan: a Studio contract becomes its preview, frames and holds. */
export function plan(input, {times, holds, fps, width, height, root, seek} = {}) {
  if (input.endsWith('.json')) {
    const {html, score} = previewFor(input);
    const rate = score.fps.num / score.fps.den;
    const frames = times ? times.map(t => Math.round(t * rate)) : selectFrames(score);
    const known = score.scenes.flatMap(s => (s.holds ?? []).map(([a, b]) => [a / rate, b / rate]));
    return {html, base: null, fps: rate, width: score.width, height: score.height, root: root ?? '#stage', seek,
      samples: frames.map(f => ({t: f / rate, f})), holds: known, holdsFrom: 'contract'};
  }
  const html = fs.readFileSync(input, 'utf8');
  const rootSize = html.match(/data-width="(\d+)"[^>]*data-height="(\d+)"/);
  const rate = fps ?? 30;
  if (!times?.length) throw new Error('Give --times for an HTML composition (seconds, comma separated)');
  return {html, base: path.dirname(path.resolve(input)), fps: rate, width: width ?? (rootSize ? Number(rootSize[1]) : undefined),
    height: height ?? (rootSize ? Number(rootSize[2]) : undefined), root, seek, samples: times.map(t => ({t, f: Math.round(t * rate)})),
    holds: holds ?? null, holdsFrom: holds ? 'given' : 'inferred'};
}

function inject(html, options, base) {
  const head = base ? `<base href="${pathToFileURL(base).href}/">` : '';
  const withBase = head ? html.replace(/<head([^>]*)>/i, m => m + head) : html;
  const script = runner(options);
  return /<\/body>/i.test(withBase) ? withBase.replace(/<\/body>(?![\s\S]*<\/body>)/i, script + '</body>') : withBase + script;
}

const geometry = report => JSON.stringify((report.texts ?? []).map(t => [t.key, t.box, t.visible, t.cutWords.map(w => w.visible)]));

const esc = value => String(value).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'})[c]);

/** Contact sheet: every sample at phone scale (360 px wide) with cut words outlined, linked to the full-size image. */
export function auditSheet(result) {
  const k = 360 / (result.width || 360);
  const card = s => {
    const boxes = s.texts.flatMap(text => text.cutWords.map(word => word.box)).map(b =>
      `<i style="left:${b.left * k}px;top:${b.top * k}px;width:${(b.right - b.left) * k}px;height:${(b.bottom - b.top) * k}px"></i>`).join('');
    const lines = s.issues.map(i => `<br><b>${esc(i.severity)}</b> ${esc(i.check)} "${esc(i.text)}": ${esc(i.detail)}`).join('');
    return `<figure class="${s.issues.some(i => i.severity === 'error') ? 'error' : ''}"><a href="${esc(s.image)}"><div class="shot" style="width:360px;height:${(result.height || 640) * k}px">${s.image ? `<img src="${esc(s.image)}" width="360" alt="${s.t} s">` : ''}${boxes}</div></a>` +
      `<figcaption>${s.t} s${s.hold ? ' (readable hold)' : ' (transition)'} - ${s.texts.filter(t => t.visible !== 'hidden').length} visible texts${lines}${s.exceptions.map(e => `<br><b>exception</b> "${esc(e.text)}": ${esc(e.reason)}`).join('')}</figcaption></figure>`;
  };
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Text audit: ${esc(result.input)}</title><style>
body{margin:16px;font:14px system-ui,sans-serif;background:#f4f4f4;color:#111}main{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;width:360px;background:#fff;border:2px solid #ddd}figure.error{border-color:#c62828}
.shot{position:relative;overflow:hidden;background:#000}.shot img{display:block}.shot i{position:absolute;outline:3px solid #e0007a}figcaption{padding:8px;line-height:1.4}</style></head><body>
<h1>Text audit: ${esc(result.input)} - ${esc(result.verdict.toUpperCase())}</h1>
<p>${result.summary.errors} errors, ${result.summary.transitional} transitional, ${result.summary.exceptions} declared exceptions in ${result.summary.samples} samples. Images are shown at phone scale (360 px wide); open one for full size. Magenta outlines mark cut words. This sheet is evidence of these instants only.</p>
<main>${result.samples.map(card).join('\n')}</main></body></html>
`;
}

export function runAudit(input, {out, browser, screenshots = true, ...options} = {}) {
  if (!out) throw new Error('Choose a new output directory with --out');
  if (fs.existsSync(out)) throw new Error(`Output directory already exists: ${out}`);
  const chrome = findBrowser(browser);
  if (!chrome) throw new Error('No Chrome or Chromium found; pass --browser or set CHROME_PATH');
  const p = plan(input, options);
  fs.mkdirSync(out, {recursive: true});
  const page = path.join(out, 'audit.html');
  fs.writeFileSync(page, inject(p.html, p, p.base));
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'text-audit-'));
  const flags = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`, '--virtual-time-budget=5000'];
  if (process.platform === 'linux' && process.getuid?.() === 0) flags.push('--no-sandbox');
  if (p.width && p.height) {
    // As in review-frames: new headless Chrome gives the page less height than the window, so measure and add it.
    const probe = path.join(out, 'viewport-probe.html');
    fs.writeFileSync(probe, '<!doctype html><title></title><script>document.title = innerHeight</script>');
    const probed = spawnSync(chrome, [...flags, `--window-size=${p.width},${p.height}`, '--dump-dom', pathToFileURL(probe).href], {encoding: 'utf8', timeout: 60000});
    fs.rmSync(probe, {force: true});
    const inner = Number(probed.stdout?.match(/<title>(\d+)<\/title>/)?.[1]);
    flags.push(`--window-size=${p.width},${p.height + (inner > 0 && inner < p.height ? p.height - inner : 0)}`);
  }
  const urlFor = (t, f) => `${pathToFileURL(path.resolve(page)).href}?t=${t}&f=${f}${input.endsWith('.json') ? `&frame=${f}&review=1` : ''}`;
  const measure = (t, f) => {
    const url = urlFor(t, f);
    const dump = spawnSync(chrome, [...flags, '--dump-dom', url], {encoding: 'utf8', timeout: 90000, maxBuffer: 64 * 1024 * 1024});
    const json = dump.stdout?.match(/<script type="application\/json" id="text-audit-report">([\s\S]*?)<\/script>/)?.[1];
    if (!json) throw new Error(`No text audit for ${t} s: ${dump.stderr?.slice(0, 300) ?? dump.error}`);
    return JSON.parse(json);
  };
  const samples = [];
  try {
    for (const {t, f} of p.samples) {
      const report = measure(t, f);
      let hold;
      if (p.holds) hold = p.holds.some(([a, b]) => t >= a - 1e-9 && t < b - 1e-9);
      else {
        const later = measure(t + STEP, Math.round((t + STEP) * p.fps));
        hold = !report.error && !later.error && geometry(report) === geometry(later);
      }
      const issues = (report.issues ?? []).map(issue => ({...issue,
        severity: issue.severity === 'error' && ['text-cut', 'text-hidden'].includes(issue.check) && !hold ? 'transitional' : issue.severity}));
      if (report.error) issues.push({severity: 'error', check: 'audit-failed', element: '', text: '', detail: report.error});
      let image = '';
      if (screenshots && p.width && p.height) {
        image = `sample-${String(samples.length).padStart(3, '0')}-${t}s.png`;
        spawnSync(chrome, [...flags, `--screenshot=${path.resolve(out, image)}`, urlFor(t, f)], {encoding: 'utf8', timeout: 90000});
        if (!fs.existsSync(path.join(out, image))) image = '';
      }
      samples.push({t, frame: f, hold, seek: report.seek, fontsStatus: report.fontsStatus, image, issues, exceptions: report.exceptions ?? [], texts: report.texts ?? []});
    }
  } finally {
    fs.rmSync(profile, {recursive: true, force: true});
  }
  const all = samples.flatMap(s => s.issues);
  const seekModes = [...new Set(samples.map(s => s.seek).filter(Boolean))];
  const result = {input: path.basename(input), browser: path.basename(chrome), width: p.width, height: p.height, holdsFrom: p.holdsFrom, seek: seekModes,
    summary: {errors: all.filter(i => i.severity === 'error').length, warnings: all.filter(i => i.severity === 'warning').length,
      transitional: all.filter(i => i.severity === 'transitional').length, exceptions: samples.reduce((n, s) => n + s.exceptions.length, 0),
      samples: samples.length, heldSamples: samples.filter(s => s.hold).length,
      textsChecked: samples.reduce((n, s) => n + s.texts.filter(t => t.visible !== 'hidden').length, 0)},
    verdict: all.some(i => i.severity === 'error') ? 'fail' : seekModes.includes('static') && samples.length > 1 ? 'not_verified' : 'pass',
    samples,
    boundary: 'Geometry of every visible text at the sampled times after fonts loaded, in this browser. Not a review of motion, rhythm, image quality or the encoded export; a mask or non-inset clip-path is noted for pixel review, not measured.'};
  if (result.verdict === 'not_verified') result.reason = 'the page did not expose a timeline to seek, so every sample shows the same state';
  fs.writeFileSync(path.join(out, 'text-audit.json'), JSON.stringify(result, null, 2) + '\n');
  fs.writeFileSync(path.join(out, 'text-audit.html'), auditSheet(result));
  return result;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), option = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const valued = ['--out', '--browser', '--times', '--holds', '--fps', '--width', '--height', '--root', '--seek'];
  const input = args.find((arg, i) => !arg.startsWith('--') && !valued.includes(args[i - 1]));
  try {
    if (!input) throw new Error('Usage: node text-audit.mjs <composition.html | motion-score.json> --out <new-dir> [--times 1,2.5] [--holds 0.5-3] [--fps 30] [--width W --height H] [--root sel] [--seek expr] [--browser path]');
    const number = name => option(name) === undefined ? undefined : Number(option(name));
    const result = runAudit(input, {out: option('--out'), browser: option('--browser'), times: option('--times')?.split(',').map(Number),
      holds: parseRanges(option('--holds')), fps: number('--fps'), width: number('--width'), height: number('--height'), root: option('--root'), seek: option('--seek')});
    for (const s of result.samples) for (const i of s.issues) console.log(`${i.severity.toUpperCase()} ${s.t}s${s.hold ? ' hold' : ''} ${i.check} ${i.element} "${i.text}": ${i.detail}`);
    for (const s of result.samples) for (const e of s.exceptions) console.log(`EXCEPTION ${s.t}s ${e.element} "${e.text}": ${e.reason} (${e.review})`);
    console.log(`${result.verdict.toUpperCase()}: ${result.summary.errors} errors, ${result.summary.warnings} warnings, ${result.summary.transitional} transitional, ${result.summary.textsChecked} visible texts in ${result.summary.samples} samples (${result.summary.heldSamples} held; holds ${result.holdsFrom}).`);
    process.exitCode = result.summary.errors ? 1 : 0;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
