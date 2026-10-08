// Automated frame review for a motion contract, using the single-file preview and a local
// Chrome or Chromium. Dependency-free (Node 20+). For every review frame chosen from the contract
// (first and last frame, both sides of each scene boundary, hold start/middle/end, uniform samples)
// it captures a screenshot and the preview's in-page review report, then writes review.json and a
// review.html contact sheet. A contract with formats is reviewed in every format by default
// ('base' is the score's own size). Exit code: 0 no errors, 1 errors found, 2 setup problem.
//
//   node review-frames.mjs motion-score.json --out review-out [--browser /path/to/chrome] [--samples 12] [--format all|base|9x16]
//   node review-frames.mjs motion-preview.html --out review-out
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const templatePath = path.join(here, '..', 'single-file-preview', 'motion-preview.html');
const scoreBlock = /(<script type="application\/json" id="motion-score">\n)([\s\S]*?)(\n<\/script>)/;

/** Review frames: same selection rules as reviewFrames() in motion-quality/score.mjs. */
export function selectFrames(score, samples = 12) {
  const n = score.totalFrames, frames = new Set([0, n - 1]);
  const add = f => { if (Number.isInteger(f) && f >= 0 && f < n) frames.add(f); };
  for (let i = 0; i < samples; i++) add(Math.round(i * (n - 1) / (samples - 1)));
  for (const s of score.scenes) {
    for (const boundary of [s.start, s.end]) for (const offset of [-1, 0, 1]) add(boundary + offset);
    for (const [a, b] of s.holds ?? []) { add(a); add(Math.floor((a + b - 1) / 2)); add(b - 1); }
  }
  for (const c of score.cues ?? []) for (const offset of [-1, 0, 1]) add(c.frame + offset);
  for (const c of score.captions ?? []) { add(c.start); add(Math.floor((c.start + c.end - 1) / 2)); add(c.end - 1); }
  return [...frames].sort((a, b) => a - b);
}

/** Put a score into the preview template, or read the score already embedded in a preview. */
export function previewFor(input) {
  const text = fs.readFileSync(input, 'utf8');
  if (input.endsWith('.html')) {
    const match = text.match(scoreBlock);
    if (!match) throw new Error('No embedded motion-score block found in the preview');
    return {html: text, score: JSON.parse(match[2])};
  }
  const score = JSON.parse(text);
  const template = fs.readFileSync(templatePath, 'utf8');
  // Every '<' is written as \u003c, so copy such as '</script>' can never end the script element; JSON.parse restores it.
  return {html: template.replace(scoreBlock, (_, open, __, close) => open + JSON.stringify(score, null, 2).replace(/</g, '\\u003c') + close), score};
}

export function findBrowser(explicit) {
  const candidates = [explicit, process.env.CHROME_PATH,
    ...['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome'].flatMap(name => (process.env.PATH ?? '').split(path.delimiter).map(dir => path.join(dir, name))),
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'];
  return candidates.find(candidate => candidate && fs.existsSync(candidate));
}

/** Format IDs to review: 'all' (default) is the base size plus every entry in score.formats. */
export function formatsFor(score, format = 'all') {
  const ids = ['base', ...(score.formats ?? []).map(item => item.id)];
  if (format === 'all') return ids;
  if (!ids.includes(format)) throw new Error(`Unknown format ${format}; use all or one of ${ids.join(', ')}`);
  return [format];
}

const escapeHtml = value => String(value).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'})[c]);

export function contactSheet(review) {
  const card = f => `<figure class="${f.issues.some(i => i.severity === 'error') ? 'error' : f.issues.length ? 'warning' : ''}"><img src="${escapeHtml(f.image)}" alt="frame ${f.frame}" loading="lazy"${f.width && f.height ? ` style="aspect-ratio:${f.width}/${f.height}"` : ''}><figcaption>frame ${f.frame} - ${escapeHtml(f.scenes.join(', ') || 'no scene')}${f.checked ? '' : ' - not in a hold (not checked)'}${f.issues.map(i => `<br><b>${i.severity}</b> ${escapeHtml(i.check)} ${escapeHtml(i.scene)}/${escapeHtml(i.element)}: ${escapeHtml(i.detail)}`).join('')}</figcaption></figure>`;
  const formats = [...new Set(review.frames.map(f => f.format ?? 'base'))];
  const cards = formats.map(format => `${formats.length > 1 || format !== 'base' ? `<h2>Format ${escapeHtml(format)}</h2>\n` : ''}<main>
${review.frames.filter(f => (f.format ?? 'base') === format).map(card).join('\n')}
</main>`).join('\n');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Frame review: ${escapeHtml(review.id)}</title><style>
body{margin:16px;font:14px system-ui,sans-serif;background:#f4f4f4;color:#111}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}
h2{margin:20px 0 8px}figure{margin:0;background:#fff;border:2px solid #ddd;border-radius:6px;overflow:hidden}figure.warning{border-color:#d9a400}figure.error{border-color:#c62828}
img{width:100%;display:block;background:#000;object-fit:cover;object-position:top}figcaption{padding:8px;line-height:1.4}</style></head><body>
<h1>Frame review: ${escapeHtml(review.id)}, revision ${escapeHtml(review.revision)}</h1>
<p>${review.summary.errors} errors, ${review.summary.warnings} warnings; ${review.summary.checkedFrames} of ${review.frames.length} frames fall in readable holds and were measured. Screenshots are evidence of these frames only, not of motion, rhythm or sound; watch the full sequence before accepting it.</p>
${cards}
</body></html>
`;
}

export function runReview(input, {out, browser, samples = 12, format = 'all'} = {}) {
  if (!out) throw new Error('Choose a new output directory with --out');
  if (fs.existsSync(out)) throw new Error(`Output directory already exists: ${out}`);
  const chrome = findBrowser(browser);
  if (!chrome) throw new Error('No Chrome or Chromium found; pass --browser or set CHROME_PATH');
  const {html, score} = previewFor(input);
  const formats = formatsFor(score, format), nested = Boolean(score.formats?.length);
  fs.mkdirSync(path.join(out, 'frames'), {recursive: true});
  const previewPath = path.join(out, 'preview.html');
  fs.writeFileSync(previewPath, html);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-review-'));
  const flags = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`, '--virtual-time-budget=3000'];
  if (process.platform === 'linux' && process.getuid?.() === 0) flags.push('--no-sandbox');
  const frames = [];
  try {
    for (const id of formats) {
      const size = id === 'base' ? score : score.formats.find(item => item.id === id);
      // New headless Chrome gives the page less height than --window-size (browser chrome) and fills the rest
      // of a screenshot with the page background, so measure the difference and enlarge the window by it.
      const probe = path.join(out, 'viewport-probe.html');
      fs.writeFileSync(probe, '<!doctype html><title></title><script>document.title = innerHeight</script>');
      const probed = spawnSync(chrome, [...flags, `--window-size=${size.width},${size.height}`, '--dump-dom', pathToFileURL(probe).href], {encoding: 'utf8', timeout: 60000});
      fs.rmSync(probe, {force: true});
      const inner = Number(probed.stdout?.match(/<title>(\d+)<\/title>/)?.[1]);
      const extra = inner > 0 && inner < size.height ? size.height - inner : 0;
      const base = [...flags, `--window-size=${size.width},${size.height + extra}`];
      if (nested) fs.mkdirSync(path.join(out, 'frames', id), {recursive: true});
      for (const frame of selectFrames(score, samples)) {
        const url = `${pathToFileURL(path.resolve(previewPath)).href}?frame=${frame}&review=1${id === 'base' ? '' : `&format=${encodeURIComponent(id)}`}`;
        const dump = spawnSync(chrome, [...base, '--dump-dom', url], {encoding: 'utf8', timeout: 60000, maxBuffer: 64 * 1024 * 1024});
        const report = dump.stdout?.match(/<script type="application\/json" id="review-report">([\s\S]*?)<\/script>/)?.[1];
        if (!report) throw new Error(`No review report for frame ${frame}: ${dump.stderr?.slice(0, 300) ?? dump.error}`);
        const image = `frames/${nested ? `${id}/` : ''}frame-${String(frame).padStart(5, '0')}.png`;
        spawnSync(chrome, [...base, `--screenshot=${path.resolve(out, image)}`, url], {encoding: 'utf8', timeout: 60000});
        const parsed = JSON.parse(report);
        frames.push({format: id, width: size.width, height: size.height, frame, image: fs.existsSync(path.join(out, image)) ? image : '', scenes: score.scenes.filter(s => frame >= s.start && frame < s.end).map(s => s.id), checked: parsed.checked, issues: parsed.issues});
      }
    }
  } finally {
    fs.rmSync(profile, {recursive: true, force: true});
  }
  const issues = frames.flatMap(f => f.issues);
  const review = {id: score.id, revision: score.revision, browser: path.basename(chrome), formats, frames,
    summary: {errors: issues.filter(i => i.severity === 'error').length, warnings: issues.filter(i => i.severity === 'warning').length, checkedFrames: frames.filter(f => f.checked).length},
    boundary: 'Automated layout checks on review frames in readable holds. Not a review of motion, rhythm, audio or the encoded export.'};
  fs.writeFileSync(path.join(out, 'review.json'), JSON.stringify(review, null, 2) + '\n');
  fs.writeFileSync(path.join(out, 'review.html'), contactSheet(review));
  return review;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), option = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const input = args.find((arg, i) => !arg.startsWith('--') && !['--out', '--browser', '--samples', '--format'].includes(args[i - 1]));
  try {
    if (!input) throw new Error('Usage: node review-frames.mjs <motion-score.json | motion-preview.html> --out <new-dir> [--browser <path>] [--samples 12] [--format all|base|<id>]');
    const review = runReview(input, {out: option('--out'), browser: option('--browser'), samples: Number(option('--samples') ?? 12), format: option('--format') ?? 'all'});
    for (const f of review.frames) for (const i of f.issues) console.log(`${i.severity.toUpperCase()} ${f.format} frame ${f.frame} ${i.check} ${i.scene}/${i.element}: ${i.detail}`);
    console.log(`${review.summary.errors} errors, ${review.summary.warnings} warnings, ${review.summary.checkedFrames}/${review.frames.length} frames measured. Contact sheet: ${path.join(option('--out'), 'review.html')}`);
    process.exitCode = review.summary.errors ? 1 : 0;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
