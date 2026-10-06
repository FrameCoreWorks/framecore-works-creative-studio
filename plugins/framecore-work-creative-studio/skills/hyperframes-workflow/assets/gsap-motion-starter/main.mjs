// Seekable GSAP preview driven by the shared motion score.
// The timeline is always paused; play only chooses which frame to seek, so
// preview, scrubbing and frame capture all derive state from the same frame.
import {gsap} from 'gsap';

const eases = {
  easeOutCubic: 'power2.out', easeOutQuart: 'power3.out', easeOutExpo: 'expo.out',
  easeInOutCubic: 'power2.inOut', easeInCubic: 'power2.in', linear: 'none',
};

const score = await (await fetch('motion-score.json')).json();
const fps = score.fps.num / score.fps.den, N = score.totalFrames, m = score.motion, t = score.tokens;
const at = frame => frame / fps;
const stage = document.getElementById('stage');
Object.assign(stage.style, {width: score.width + 'px', height: score.height + 'px', background: t.background, color: t.foreground, fontFamily: t.fontFamily});
const margin = Math.round(score.width * t.marginRatio);
const tl = gsap.timeline({paused: true});

const scene = s => {
  const el = document.createElement('div');
  el.className = 'scene';
  el.style.padding = `0 ${margin}px`;
  stage.append(el);
  tl.set(el, {visibility: 'visible'}, at(s.start)).set(el, {visibility: 'hidden'}, at(s.end));
  return el;
};
const exit = (el, s) => tl.to(el, {opacity: 0, y: -24, duration: at(m.exitFrames), ease: eases[m.exitEasing]}, at(s.end - m.exitFrames));
const [title, steps, end] = score.scenes;

// Title: line mask reveal.
{
  const el = scene(title);
  title.copy.forEach((id, i) => {
    const mask = document.createElement('div'), line = document.createElement('div');
    mask.className = 'mask';
    Object.assign(line.style, {fontSize: i === 0 ? '132px' : '96px', fontWeight: i === 0 ? 700 : 400});
    line.textContent = score.copy[id];
    mask.append(line);
    el.append(mask);
    tl.fromTo(line, {yPercent: 110}, {yPercent: 0, duration: at(m.entryFrames), ease: eases[m.entryEasing]}, at(title.start + i * m.lineStaggerFrames));
  });
  exit(el, title);
}

// Steps: item stagger and a connector that grows at constant speed.
{
  const el = scene(steps);
  const row = document.createElement('div'), line = document.createElement('div');
  Object.assign(row.style, {position: 'relative', display: 'flex', justifyContent: 'space-between', alignItems: 'center'});
  Object.assign(line.style, {position: 'absolute', left: 0, right: 0, top: '50%', height: '6px', background: t.accent, transformOrigin: 'left center'});
  row.append(line);
  el.append(row);
  const lastEntryEnd = steps.start + (steps.copy.length - 1) * m.itemStaggerFrames + m.entryFrames;
  tl.fromTo(line, {scaleX: 0}, {scaleX: 1, duration: at(lastEntryEnd - steps.start - 6), ease: 'none'}, at(steps.start + 6));
  steps.copy.forEach((id, i) => {
    const item = document.createElement('div');
    Object.assign(item.style, {position: 'relative', padding: '12px 36px', background: t.background, fontSize: '104px', fontWeight: 700});
    item.textContent = score.copy[id];
    row.append(item);
    tl.fromTo(item, {opacity: 0, y: 32}, {opacity: 1, y: 0, duration: at(m.entryFrames), ease: eases[m.entryEasing]}, at(steps.start + i * m.itemStaggerFrames));
  });
  exit(el, steps);
}

// End card: slow-settling resolve, no exit, stable final frame.
{
  const el = scene(end);
  el.style.alignItems = 'center';
  const word = document.createElement('div'), rule = document.createElement('div');
  Object.assign(word.style, {fontSize: '120px', fontWeight: 700});
  Object.assign(rule.style, {marginTop: '28px', height: '6px', width: '160px', background: t.accent, transformOrigin: 'center'});
  word.textContent = score.copy[end.copy[0]];
  el.append(word, rule);
  tl.fromTo(word, {opacity: 0, scale: 0.94}, {opacity: 1, scale: 1, duration: at(30), ease: eases[m.resolveEasing]}, at(end.start));
  tl.fromTo(rule, {scaleX: 0}, {scaleX: 1, duration: at(30), ease: eases[m.resolveEasing]}, at(end.start));
}

// Keep the timeline exactly N frames long so the last valid frame is N - 1.
tl.set({}, {}, at(N));

const scrub = document.getElementById('scrub'), readout = document.getElementById('readout'), play = document.getElementById('play');
scrub.max = String(N - 1);
let current = 0, playing = false, startedAt = 0, startFrame = 0;

/** Render exactly one frame. Resolves after fonts are ready, for capture tools. */
async function seekFrame(frame) {
  current = Math.min(N - 1, Math.max(0, Math.round(frame)));
  tl.seek(at(current), false);
  scrub.value = String(current);
  readout.textContent = `frame ${current}`;
  await document.fonts.ready;
  return current;
}
window.seekFrame = seekFrame;
window.motionScore = score;

function tick(now) {
  if (!playing) return;
  const frame = startFrame + Math.floor((now - startedAt) / 1000 * fps);
  seekFrame(frame);
  if (frame >= N - 1) { playing = false; play.textContent = 'Play'; return; }
  requestAnimationFrame(tick);
}
play.onclick = () => {
  playing = !playing;
  play.textContent = playing ? 'Pause' : 'Play';
  if (playing) { startFrame = current >= N - 1 ? 0 : current; startedAt = performance.now(); requestAnimationFrame(tick); }
};
document.getElementById('replay').onclick = () => { playing = false; seekFrame(0); play.click(); };
scrub.oninput = () => { playing = false; play.textContent = 'Play'; seekFrame(Number(scrub.value)); };

const fit = () => {
  const viewport = document.getElementById('viewport');
  stage.style.transform = `scale(${Math.min(viewport.clientWidth / score.width, viewport.clientHeight / score.height)})`;
};
addEventListener('resize', fit);
fit();
// ?frame=140 seeks once; ?frames=299,0,140 replays a seek sequence to compare
// direct, forward and backward seeks of the same frame during review.
const query = new URLSearchParams(location.search);
for (const frame of (query.get('frames') ?? query.get('frame') ?? '0').split(',')) await seekFrame(Number(frame));
document.documentElement.dataset.ready = 'true';
