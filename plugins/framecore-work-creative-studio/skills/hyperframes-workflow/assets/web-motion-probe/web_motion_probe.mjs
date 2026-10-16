// How is this web animation built? Open a page in a local Chrome or Chromium and read what it exposes to any visitor,
// the same as the browser's developer tools: the motion libraries and their versions, each GSAP tween and
// ScrollTrigger (targets, duration, delay, ease, animated properties, scroll range), every CSS animation, transition
// and Web Animation with its timing and keyframes, Lottie files, canvases, videos and the fonts in use. Optional
// frames show the motion over time. Dependency-free (Node 20+); talks to the browser over its DevTools pipe.
//
//   node web_motion_probe.mjs https://example.com [--wait 3] [--scroll] [--width 1440 --height 900]
//        [--frames 12 --interval 100 --out frames/] [--json] [--browser /path/to/chrome]
//
// It downloads nothing into the project and never saves the site's code or assets; frames are screenshots for study.
// Exit code: 0 measured, 2 setup or page problem.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {devtools} from '../motion-export/export-video.mjs';
import {findBrowser} from '../motion-review/review-frames.mjs';

const LIMIT = 60;

// Runs inside the page. Everything it returns is plain data about what the page already loaded.
export const COLLECT = `(() => {
  const LIMIT = ${LIMIT};
  const name = el => {
    if (typeof el === 'function') return 'function';
    if (!el || !el.tagName) return typeof el === 'object' && el ? (el.constructor && el.constructor.name) || 'object' : String(el);
    let text = el.tagName.toLowerCase();
    if (el.id) text += '#' + el.id;
    const cls = typeof el.className === 'string' ? el.className.trim().split(/\\s+/).filter(Boolean).slice(0, 2) : [];
    return text + cls.map(c => '.' + c).join('');
  };
  const round = v => typeof v === 'number' ? Math.round(v * 1000) / 1000 : v;
  const version = v => v === undefined || v === null ? null : String(v);
  const g = window;
  const libraries = {
    gsap: g.gsap ? version(g.gsap.version) || 'present' : null,
    ScrollTrigger: g.ScrollTrigger ? 'present' : null,
    SplitText: g.SplitText ? 'present' : null,
    lottie: g.lottie || g.bodymovin ? version((g.lottie || g.bodymovin).version) || 'present' : null,
    three: g.THREE ? version(g.THREE.REVISION) || 'present' : null,
    pixi: g.PIXI ? version(g.PIXI.VERSION) || 'present' : null,
    anime: g.anime ? version(g.anime.version) || 'present' : null,
    motion: g.Motion ? 'present' : null,
    lenis: g.Lenis || g.lenis ? 'present' : null,
    d3: g.d3 ? version(g.d3.version) || 'present' : null,
    rive: g.rive ? 'present' : null,
    swiper: g.Swiper ? 'present' : null,
    p5: g.p5 ? 'present' : null
  };
  const CONTROL = new Set(['duration', 'delay', 'ease', 'repeat', 'yoyo', 'stagger', 'scrollTrigger', 'immediateRender', 'lazy',
    'overwrite', 'paused', 'reversed', 'inherit', 'data', 'id', 'callbackScope', 'runBackwards', 'startAt', 'parent', 'keyframes',
    'onStart', 'onUpdate', 'onComplete', 'onRepeat', 'onReverseComplete', 'onCompleteParams', 'onReverseCompleteParams',
    'onUpdateParams', 'onStartParams', 'totalProgress', 'smoothChildTiming', 'autoRemoveChildren', 'defaults', 'repeatDelay', 'repeatRefresh']);
  const easeName = e => typeof e === 'string' ? e : typeof e === 'function' ? 'custom function' : e === undefined ? 'default (power1.out)' : 'other';
  const trigger = st => st ? {trigger: name(st.trigger), start: round(st.start), end: round(st.end), scrub: st.vars ? st.vars.scrub ?? null : null, pin: !!(st.vars && st.vars.pin)} : null;
  let tweens = null, scrollTriggers = null;
  if (g.gsap && g.gsap.globalTimeline && g.gsap.globalTimeline.getChildren) {
    tweens = g.gsap.globalTimeline.getChildren(true, true, true).slice(0, LIMIT).map(t => {
      const vars = t.vars || {};
      const isTimeline = typeof t.targets !== 'function';
      const isCall = !isTimeline && t.targets().some(x => typeof x === 'function');
      return {
        kind: isTimeline ? 'timeline' : isCall ? 'call' : 'tween',
        targets: isTimeline ? [] : t.targets().slice(0, 5).map(name),
        start: round(t.startTime ? t.startTime() : 0), duration: round(t.duration ? t.duration() : 0), delay: round(t.delay ? t.delay() : 0),
        ease: isTimeline ? null : easeName(vars.ease), repeat: vars.repeat ?? 0, yoyo: !!vars.yoyo, stagger: vars.stagger ?? null,
        properties: Object.keys(vars).filter(k => !CONTROL.has(k)),
        from: !!vars.runBackwards, scroll: trigger(t.scrollTrigger)
      };
    });
  }
  if (g.ScrollTrigger && g.ScrollTrigger.getAll) scrollTriggers = g.ScrollTrigger.getAll().slice(0, LIMIT).map(trigger);
  const webAnimations = (document.getAnimations ? document.getAnimations() : []).slice(0, LIMIT).map(a => {
    const effect = a.effect, timing = effect && effect.getTiming ? effect.getTiming() : {};
    const kind = a.constructor ? a.constructor.name : 'Animation';
    const frames = effect && effect.getKeyframes ? effect.getKeyframes().slice(0, 8).map(f => {
      const out = {};
      for (const [k, v] of Object.entries(f)) if (!['computedOffset', 'composite'].includes(k)) out[k] = round(v);
      return out;
    }) : [];
    return {kind, name: a.animationName || a.transitionProperty || a.id || null, target: effect && effect.target ? name(effect.target) : null,
      duration: round(timing.duration), delay: round(timing.delay), easing: timing.easing === 'linear' && frames[0] && frames[0].easing ? frames[0].easing : timing.easing, iterations: timing.iterations === Infinity ? 'infinite' : timing.iterations,
      direction: timing.direction, fill: timing.fill, state: a.playState, keyframes: frames};
  });
  let lottieFiles = null;
  const lot = g.lottie || g.bodymovin;
  if (lot && lot.getRegisteredAnimations) lottieFiles = lot.getRegisteredAnimations().slice(0, LIMIT).map(a => ({
    name: a.name || null, renderer: a.renderer && a.renderer.rendererType || null, frames: round(a.totalFrames), fps: round(a.frameRate),
    width: a.animationData ? a.animationData.w : null, height: a.animationData ? a.animationData.h : null, loop: a.loop, path: a.path || null
  }));
  const canvases = [...document.querySelectorAll('canvas')].slice(0, 20).map(c => ({element: name(c), width: c.width, height: c.height}));
  const videos = [...document.querySelectorAll('video')].slice(0, 20).map(v => ({element: name(v), source: v.currentSrc || v.src || null, seconds: round(v.duration), loop: v.loop, autoplay: v.autoplay, muted: v.muted}));
  const fonts = [...new Set([...(document.fonts || [])].filter(f => f.status === 'loaded').map(f => [f.family.replace(/["']/g, ''), f.weight, f.style].join(' ')))].slice(0, 30);
  const scripts = [...document.scripts].slice(0, 80).map(s => s.src || 'inline');
  return {url: location.href, title: document.title, viewport: [innerWidth, innerHeight], page_height: document.documentElement.scrollHeight,
    reduced_motion: matchMedia('(prefers-reduced-motion: reduce)').matches,
    libraries: Object.fromEntries(Object.entries(libraries).filter(([, v]) => v)), gsap_tweens: tweens, scroll_triggers: scrollTriggers,
    web_animations: webAnimations, lottie: lottieFiles, canvases, videos, fonts, scripts};
})()`;

const KEEP_TWEENS = `(() => {
  let value;
  try {
    Object.defineProperty(window, 'gsap', {configurable: true, get: () => value, set: v => {
      value = v;
      try { if (v && v.globalTimeline) v.globalTimeline.autoRemoveChildren = false; } catch (e) {}
    }});
  } catch (e) {}
})()`;

function parseArgs(argv) {
  const options = {wait: 3, width: 1440, height: 900, frames: 0, interval: 100, scroll: false, json: false};
  const rest = [];
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const value = () => { if (i + 1 >= argv.length) throw new Error(`${arg} needs a value`); return argv[++i]; };
    if (arg === '--wait') options.wait = Number(value());
    else if (arg === '--width') options.width = Number(value());
    else if (arg === '--height') options.height = Number(value());
    else if (arg === '--frames') options.frames = Number(value());
    else if (arg === '--interval') options.interval = Number(value());
    else if (arg === '--out') options.out = value();
    else if (arg === '--browser') options.browser = value();
    else if (arg === '--scroll') options.scroll = true;
    else if (arg === '--json') options.json = true;
    else if (arg.startsWith('--')) throw new Error(`Unknown option ${arg}`);
    else rest.push(arg);
  }
  if (rest.length !== 1) throw new Error('Give one page: a URL or a local HTML file');
  options.page = rest[0];
  for (const key of ['wait', 'width', 'height', 'frames', 'interval']) if (!Number.isFinite(options[key]) || options[key] < 0) throw new Error(`--${key} must be a number of 0 or more`);
  if (options.frames > 300) throw new Error('--frames is limited to 300');
  if (options.frames && !options.out) throw new Error('Frames need a new folder with --out');
  return options;
}

export function pageUrl(page) {
  if (/^https?:\/\//i.test(page) || page.startsWith('file:')) return page;
  if (fs.existsSync(page)) return pathToFileURL(path.resolve(page)).href;
  throw new Error(`Not a URL and no such file: ${page}`);
}

const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

export async function probePage(page, options = {}) {
  const {wait = 3, width = 1440, height = 900, frames = 0, interval = 100, scroll = false, out, browser} = options;
  const url = pageUrl(page);
  if (frames) {
    if (fs.existsSync(out) && fs.readdirSync(out).length) throw new Error(`Frame folder is not empty: ${out}`);
    fs.mkdirSync(out, {recursive: true});
  }
  const chrome = findBrowser(browser);
  if (!chrome) throw new Error('No Chrome or Chromium found; pass --browser or set CHROME_PATH');
  const work = fs.mkdtempSync(path.join(os.tmpdir(), 'web-motion-probe-'));
  const args = ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--mute-audio', `--user-data-dir=${path.join(work, 'profile')}`, 'about:blank'];
  if (process.platform === 'linux' && process.getuid?.() === 0) args.unshift('--no-sandbox');
  const browserSession = devtools(chrome, args);
  try {
    const {targetId} = await browserSession.send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await browserSession.send('Target.attachToTarget', {targetId, flatten: true});
    const send = (method, params) => browserSession.send(method, params, sessionId);
    await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: 1, mobile: false});
    await send('Page.enable');
    // A global GSAP drops a finished tween from its timeline; keep them so an entrance animation is still readable.
    await send('Page.addScriptToEvaluateOnNewDocument', {source: KEEP_TWEENS});
    await send('Page.navigate', {url});
    const evaluate = async expression => {
      const {result, exceptionDetails} = await send('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true});
      if (exceptionDetails) throw new Error(`Page script failed: ${exceptionDetails.exception?.description || exceptionDetails.text}`);
      return result.value;
    };
    for (let i = 0; i < 300 && (await evaluate('document.readyState')) !== 'complete'; i += 1) await pause(100);
    const loaded = await evaluate('location.href');
    if (loaded.startsWith('chrome-error:')) throw new Error(`The page did not load in the browser: ${url} (network, proxy or certificate); open it in a browser that can reach it`);
    await pause(wait * 1000);
    const saved = [];
    const shoot = async label => {
      if (!frames || saved.length >= frames) return;
      const {data} = await send('Page.captureScreenshot', {format: 'png'});
      const file = path.join(out, `frame-${String(saved.length).padStart(3, '0')}${label ? `-${label}` : ''}.png`);
      fs.writeFileSync(file, Buffer.from(data, 'base64'));
      saved.push(path.basename(file));
    };
    const report = await evaluate(COLLECT);
    if (scroll) {
      // Walk down the page so scroll-driven animations play, then read again.
      const total = await evaluate('document.documentElement.scrollHeight - innerHeight');
      const steps = Math.max(1, frames || 10);
      for (let i = 1; i <= steps; i += 1) {
        await evaluate(`window.scrollTo(0, ${Math.round(total * i / steps)})`);
        await pause(interval);
        await shoot(`scroll${Math.round(100 * i / steps)}`);
      }
      report.after_scroll = await evaluate(COLLECT);
    } else {
      while (saved.length < frames) { await shoot(''); await pause(interval); }
    }
    report.frames = frames ? {folder: out, files: saved, interval_ms: interval} : null;
    report.note = 'Read from the live page as any visitor sees it. Values are what the page reports at that moment: finished tweens of a global GSAP are kept (a bundled GSAP may drop them), a custom ease shows as a function, and animation built in canvas or WebGL code is visible only in the frames.';
    return report;
  } finally {
    await browserSession.close();
    try { fs.rmSync(work, {recursive: true, force: true, maxRetries: 10, retryDelay: 300}); } catch (error) { console.warn(`WARN could not remove the temporary folder ${work}: ${error.message}`); }
  }
}

function summary(report) {
  const lines = [`${report.title || '(no title)'} — ${report.url}`];
  const libs = Object.entries(report.libraries).map(([k, v]) => v === 'present' ? k : `${k} ${v}`);
  lines.push(`  libraries: ${libs.length ? libs.join(', ') : 'none of the known motion libraries'}`);
  const pick = report.after_scroll || report;
  for (const t of pick.gsap_tweens || []) {
    if (t.kind !== 'tween' || !t.properties.length) continue;   // timelines, delayed calls and GSAP's own helper tweens
    lines.push(`  gsap ${t.from ? 'from' : 'tween'} ${t.targets.join(' ') || '?'}: ${t.properties.join(', ') || '-'}; ${t.duration}s at ${t.start}s, delay ${t.delay}s, ease ${t.ease}${t.stagger !== null ? `, stagger ${JSON.stringify(t.stagger)}` : ''}${t.repeat ? `, repeat ${t.repeat}${t.yoyo ? ' yoyo' : ''}` : ''}${t.scroll ? `, scroll ${t.scroll.start}-${t.scroll.end}px${t.scroll.scrub !== null ? ` scrub ${t.scroll.scrub}` : ''}${t.scroll.pin ? ' pinned' : ''}` : ''}`);
  }
  for (const a of pick.web_animations) {
    const props = [...new Set(a.keyframes.flatMap(f => Object.keys(f).filter(k => !['offset', 'easing'].includes(k))))];
    lines.push(`  ${a.kind} ${a.name || ''} on ${a.target}: ${props.join(', ') || '-'}; ${a.duration} ms, delay ${a.delay} ms, ${a.easing}, ${a.iterations} time(s), ${a.state}`);
  }
  for (const l of pick.lottie || []) lines.push(`  lottie ${l.name || l.path || ''}: ${l.width}x${l.height}, ${l.frames} frames at ${l.fps} fps, ${l.renderer}`);
  if (pick.canvases.length) lines.push(`  canvases: ${pick.canvases.map(c => `${c.element} ${c.width}x${c.height}`).join(', ')}`);
  if (pick.videos.length) lines.push(`  videos: ${pick.videos.map(v => `${v.element} ${v.seconds}s${v.loop ? ' loop' : ''}`).join(', ')}`);
  if (pick.fonts.length) lines.push(`  fonts: ${pick.fonts.join(', ')}`);
  if (report.frames) lines.push(`  frames: ${report.frames.files.length} in ${report.frames.folder}`);
  lines.push(`  note: ${report.note}`);
  return lines.join('\n');
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
  let options;
  try { options = parseArgs(process.argv.slice(2)); } catch (error) { console.error(`web_motion_probe: ${error.message}`); process.exit(2); }
  probePage(options.page, options).then(report => {
    console.log(options.json ? JSON.stringify(report, null, 2) : summary(report));
  }).catch(error => { console.error(`web_motion_probe: ${error.message}`); process.exit(2); });
}
