// Declarative motion scene engine for the FrameCore Works Creative Studio motion contract.
// Dependency-free and runtime-agnostic: buildScene() describes the elements of a scene once,
// sceneFrame() returns their styles (and changing text) for one frame. DOM and React
// renderers only apply the result, so every runtime shows the same picture for a frame.
// Values follow references/motion-craft.md. Keep copies of this file byte-identical.

const bezier = (x1, y1, x2, y2) => x => {
  if (x <= 0 || x >= 1) return Math.min(1, Math.max(0, x));
  let lo = 0, hi = 1, u = x;
  for (let i = 0; i < 30; i++) {
    u = (lo + hi) / 2;
    const bx = 3 * (1 - u) * (1 - u) * u * x1 + 3 * (1 - u) * u * u * x2 + u * u * u;
    if (bx < x) lo = u; else hi = u;
  }
  return 3 * (1 - u) * (1 - u) * u * y1 + 3 * (1 - u) * u * u * y2 + u * u * u;
};

export const easings = {
  easeOutCubic: bezier(0.33, 1, 0.68, 1),
  easeOutQuart: bezier(0.25, 1, 0.5, 1),
  easeOutExpo: bezier(0.16, 1, 0.3, 1),
  easeInOutCubic: bezier(0.65, 0, 0.35, 1),
  easeInCubic: bezier(0.32, 0, 0.67, 0),
  linear: x => Math.min(1, Math.max(0, x)),
};

/** Supported scene kinds and the params each one requires. */
export const sceneKinds = {
  'line-reveal': {required: ['lines'], copyParams: ['lines']},
  'item-stagger': {required: ['items'], copyParams: ['items']},
  'end-card': {required: ['text'], copyParams: ['text']},
  'counter': {required: ['to'], copyParams: ['label']},
  'quote': {required: ['quote'], copyParams: ['quote', 'attribution']},
  'logo-reveal': {required: ['asset'], copyParams: []},
};

/** Eased 0..1 progress of an interval starting at master frame `start` and lasting `duration` frames. */
export const progress = (frame, start, duration, easing = 'linear') => easings[easing]((frame - start) / duration);

// Sizes are authored for a 1080 px short side, so 16:9, 9:16 and 1:1 share one type scale.
const scale = score => Math.min(score.width, score.height) / 1080;
const px = (score, value) => Math.round(value * scale(score));
const motion = score => ({entryFrames: 15, exitFrames: 10, lineStaggerFrames: 6, itemStaggerFrames: 8, entryEasing: 'easeOutCubic', exitEasing: 'easeInCubic', resolveEasing: 'easeOutExpo', ...score.motion});
const margin = score => Math.round(score.width * (score.tokens?.marginRatio ?? 0.08));
const list = value => (Array.isArray(value) ? value : value === undefined ? [] : [value]);
const copy = (score, id) => score.copy?.[id] ?? '';
const isLast = (scene, score) => scene.end >= score.totalFrames;
// params.exit: true or 'lift' (fade and lift, the default except for the last scene), 'sweep' (fade and
// slide left while a vertical line sweeps across the frame) or false (no exit).
const exitMode = (scene, score) => {
  const exit = scene.params?.exit ?? !isLast(scene, score);
  return exit === false ? 'none' : exit === 'sweep' ? 'sweep' : 'lift';
};

// Optional tokens.safeArea {top, bottom} (fractions of the height) keeps content clear of platform UI.
// Take the values from the platform's current documentation or the user; the engine has no defaults.
const padding = score => {
  const area = score.tokens?.safeArea;
  if (!area) return `0 ${margin(score)}px`;
  return `${Math.round(score.height * (area.top ?? 0))}px ${margin(score)}px ${Math.round(score.height * (area.bottom ?? 0))}px`;
};
const column = (score, align = 'left') => ({
  position: 'absolute', inset: '0', display: 'flex', flexDirection: 'column', justifyContent: 'center',
  alignItems: align === 'center' ? 'center' : 'stretch', padding: padding(score), boxSizing: 'border-box',
});
// item-stagger direction: 'row', 'column' or 'auto' (a row only in clearly landscape frames).
const vertical = (scene, score) => {
  const direction = scene.params?.direction ?? 'auto';
  return direction === 'column' || (direction === 'auto' && score.width < score.height * 1.3);
};

/** The score in one output format: size, tokens and scene params of score.formats[id] merged over the base. */
export function resolveFormat(score, id) {
  if (id === undefined || id === null || id === '' || id === 'base') return score;
  const format = (score.formats ?? []).find(item => item.id === id);
  if (!format) throw new Error(`Unknown format: ${id}`);
  const params = format.params ?? {};
  return {...score, format: format.id, width: format.width, height: format.height, viewing: format.viewing ?? score.viewing,
    tokens: {...score.tokens, ...format.tokens},
    scenes: score.scenes.map(scene => (params[scene.id] ? {...scene, params: {...scene.params, ...params[scene.id]}} : scene))};
}

/** Describe the scene's elements. Each node: {key, type: 'box' | 'text' | 'image', text?, src?, style, children?}. */
export function buildScene(scene, score) {
  const content = buildContent(scene, score);
  if (exitMode(scene, score) !== 'sweep') return content;
  const p = scene.params ?? {}, t = score.tokens ?? {};
  return {key: 'scene', type: 'box', style: {position: 'absolute', inset: '0'}, children: [content,
    {key: 'sweep', type: 'box', style: {position: 'absolute', left: '0', top: '16%', bottom: '16%', width: `${px(score, 6)}px`, marginLeft: `-${px(score, 3)}px`, background: p.sweepColor ?? t.accent ?? t.foreground, opacity: '0'}}]};
}

function buildContent(scene, score) {
  const p = scene.params ?? {}, t = score.tokens ?? {};
  switch (scene.kind) {
    case 'line-reveal': {
      const sizes = p.sizes ?? [132, 96], weights = p.weights ?? [700, 400];
      return {key: 'container', type: 'box', style: column(score, p.align), children: list(p.lines).map((id, i) => ({
        key: `mask-${i}`, type: 'box', style: {overflow: 'hidden', lineHeight: '1.1'},
        children: [{key: `line-${i}`, type: 'text', text: copy(score, id), style: {fontSize: `${px(score, sizes[i] ?? sizes[sizes.length - 1])}px`, fontWeight: String(weights[i] ?? weights[weights.length - 1])}}],
      }))};
    }
    case 'item-stagger': {
      const items = list(p.items).map((id, i) => ({key: `item-${i}`, type: 'text', text: copy(score, id), style: {position: 'relative', padding: `${px(score, 12)}px ${px(score, 36)}px`, background: t.background, fontSize: `${px(score, p.size ?? 104)}px`, fontWeight: String(p.weight ?? 700)}}));
      const down = vertical(scene, score);
      const row = {key: 'row', type: 'box', children: items, style: down
        ? {position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: `${px(score, p.gap ?? 56)}px`}
        : {position: 'relative', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}};
      const line = down
        ? {position: 'absolute', top: '0', bottom: '0', left: `calc(50% - ${px(score, 3)}px)`, width: `${px(score, 6)}px`, background: t.accent, transformOrigin: 'center top'}
        : {position: 'absolute', left: '0', right: '0', top: '50%', height: `${px(score, 6)}px`, background: t.accent, transformOrigin: 'left center'};
      if (p.connector !== false) row.children = [{key: 'connector', type: 'box', style: line}, ...items];
      return {key: 'container', type: 'box', style: column(score), children: [row]};
    }
    case 'end-card':
      return {key: 'container', type: 'box', style: column(score, 'center'), children: [
        {key: 'text', type: 'text', text: copy(score, p.text), style: {fontSize: `${px(score, p.size ?? 120)}px`, fontWeight: String(p.weight ?? 700), textAlign: 'center'}},
        ...(p.rule === false ? [] : [{key: 'rule', type: 'box', style: {marginTop: `${px(score, 28)}px`, height: `${px(score, 6)}px`, width: `${px(score, 160)}px`, background: t.accent, transformOrigin: 'center'}}]),
      ]};
    case 'counter':
      return {key: 'container', type: 'box', style: column(score, p.align ?? 'center'), children: [
        {key: 'number', type: 'text', text: '', style: {fontSize: `${px(score, p.size ?? 220)}px`, fontWeight: '700', lineHeight: '1', fontVariantNumeric: 'tabular-nums'}},
        ...(p.label ? [{key: 'label', type: 'text', text: copy(score, p.label), style: {marginTop: `${px(score, 24)}px`, fontSize: `${px(score, p.labelSize ?? 48)}px`, color: t.muted ?? t.foreground}}] : []),
      ]};
    case 'quote':
      return {key: 'container', type: 'box', style: column(score, p.align ?? 'left'), children: [
        {key: 'quote', type: 'text', text: copy(score, p.quote), style: {maxWidth: '78%', fontSize: `${px(score, p.size ?? 72)}px`, lineHeight: '1.25', fontWeight: '400'}},
        ...(p.attribution ? [{key: 'attribution', type: 'text', text: copy(score, p.attribution), style: {marginTop: `${px(score, 36)}px`, fontSize: `${px(score, 40)}px`, color: t.muted ?? t.foreground}}] : []),
      ]};
    case 'logo-reveal': {
      const asset = (score.assets ?? []).find(item => item.id === p.asset);
      return {key: 'container', type: 'box', style: column(score, 'center'), children: [
        {key: 'logo', type: 'image', src: asset?.src ?? '', alt: asset?.alt ?? asset?.id ?? '', style: {width: `${px(score, p.width ?? 360)}px`, height: 'auto', display: 'block'}},
      ]};
    }
    default:
      throw new Error(`Unknown scene kind: ${scene.kind}`);
  }
}

/** Styles and changing text for one frame: {key: {style, text?}}. The scene is visible when start <= frame < end. */
export function sceneFrame(scene, score, frame) {
  const p = scene.params ?? {}, m = motion(score), out = {};
  const mode = exitMode(scene, score);
  // A sweep exit lasts sweepFrames: the content leaves during its first exitFrames, then the line finishes
  // crossing from margin to margin exactly at the scene end, so the next scene can enter behind it.
  const sweepFrames = p.sweepFrames ?? m.exitFrames + 12;
  const exitStart = mode === 'sweep' ? scene.end - sweepFrames : scene.end - m.exitFrames;
  const e = mode === 'none' ? 0 : progress(frame, exitStart, m.exitFrames, m.exitEasing);
  out.container = {style: {opacity: String(1 - e), transform: mode === 'sweep' ? `translateX(${-px(score, 150) * e}px)` : `translateY(${-px(score, 24) * e}px)`}};
  if (mode === 'sweep') {
    const k = progress(frame, exitStart, sweepFrames, 'easeInOutCubic'), from = margin(score), to = score.width - margin(score);
    out.sweep = {style: {opacity: k > 0 && k < 1 ? '1' : '0', transform: `translateX(${Math.round(from + (to - from) * k)}px)`}};
  }
  switch (scene.kind) {
    case 'line-reveal':
      list(p.lines).forEach((_, i) => {
        const k = progress(frame, scene.start + i * m.lineStaggerFrames, m.entryFrames, m.entryEasing);
        out[`line-${i}`] = {style: {transform: `translateY(${(1 - k) * 110}%)`}};
      });
      break;
    case 'item-stagger': {
      const n = list(p.items).length, lastEntryEnd = scene.start + (n - 1) * m.itemStaggerFrames + m.entryFrames;
      if (p.connector !== false) out.connector = {style: {transform: `${vertical(scene, score) ? 'scaleY' : 'scaleX'}(${progress(frame, scene.start + 6, lastEntryEnd - scene.start - 6, 'linear')})`}};
      for (let i = 0; i < n; i++) {
        const k = progress(frame, scene.start + i * m.itemStaggerFrames, m.entryFrames, m.entryEasing);
        out[`item-${i}`] = {style: {opacity: String(k), transform: `translateY(${(1 - k) * px(score, 32)}px)`}};
      }
      break;
    }
    case 'end-card': {
      const k = progress(frame, scene.start, p.duration ?? 30, m.resolveEasing);
      out.text = {style: {opacity: String(k), transform: `scale(${0.94 + 0.06 * k})`}};
      if (p.rule !== false) out.rule = {style: {transform: `scaleX(${k})`}};
      break;
    }
    case 'counter': {
      // The label and unit settle first; the number counts only once they are readable.
      const label = progress(frame, scene.start, m.entryFrames, m.entryEasing);
      const k = progress(frame, scene.start + m.entryFrames, p.duration ?? 45, p.easing ?? 'easeOutCubic');
      const value = (p.from ?? 0) + ((p.to ?? 0) - (p.from ?? 0)) * k;
      const format = new Intl.NumberFormat(p.locale ?? 'en-US', {minimumFractionDigits: p.decimals ?? 0, maximumFractionDigits: p.decimals ?? 0});
      out.number = {style: {opacity: String(label)}, text: `${p.prefix ?? ''}${format.format(value)}${p.suffix ?? ''}`};
      if (p.label) out.label = {style: {opacity: String(label), transform: `translateY(${(1 - label) * px(score, 16)}px)`}};
      break;
    }
    case 'quote': {
      // Whole-phrase reveal; the attribution follows once the quotation has settled.
      const k = progress(frame, scene.start, m.entryFrames + 5, m.entryEasing);
      out.quote = {style: {opacity: String(k), transform: `translateY(${(1 - k) * px(score, 24)}px)`}};
      if (p.attribution) out.attribution = {style: {opacity: String(progress(frame, scene.start + (p.attributionDelay ?? 30), m.entryFrames, m.entryEasing))}};
      break;
    }
    case 'logo-reveal': {
      // Reveal by clipping only: the mark is never scaled, skewed or recoloured.
      const k = progress(frame, scene.start, p.duration ?? 30, m.resolveEasing);
      out.logo = {style: {clipPath: p.reveal === 'wipe' ? `inset(0 ${(1 - k) * 100}% 0 0)` : `circle(${k * 75}% at 50% 50%)`}};
      break;
    }
    default:
      throw new Error(`Unknown scene kind: ${scene.kind}`);
  }
  return out;
}

/** Beat grid from score.music {bpm, offsetMs, beatsPerBar}: every beat inside the timeline as {beat, bar, beatInBar, frame}. */
export function beatFrames(score) {
  const music = score.music;
  if (!(music?.bpm > 0)) return [];
  const fps = score.fps.num / score.fps.den, perBar = music.beatsPerBar ?? 4, offset = (music.offsetMs ?? 0) / 1000, beats = [];
  // Each beat is computed from the master timeline, so rounding never accumulates.
  for (let beat = 0, frame = Math.round(offset * fps); frame < score.totalFrames; beat++, frame = Math.round((offset + beat * 60 / music.bpm) * fps)) {
    beats.push({beat, bar: Math.floor(beat / perBar) + 1, beatInBar: (beat % perBar) + 1, frame});
  }
  return beats;
}

/** Caption layer for score.captions [{id, start, end, copy}], drawn above the scenes; null without captions. */
export function buildCaptions(score) {
  if (!score.captions?.length) return null;
  const t = score.tokens ?? {}, c = t.captions ?? {};
  const bottom = Math.max(Math.round(score.height * (t.safeArea?.bottom ?? 0)), Math.round(score.height * (c.bottom ?? 0.08)));
  return {key: 'captions', type: 'box', style: {position: 'absolute', left: `${margin(score)}px`, right: `${margin(score)}px`, bottom: `${bottom}px`, display: 'flex', justifyContent: 'center'}, children: [
    {key: 'caption', type: 'text', text: '', style: {maxWidth: '100%', padding: `${px(score, 10)}px ${px(score, 22)}px`, background: c.background ?? 'rgba(0, 0, 0, 0.8)', color: c.color ?? '#FFFFFF', fontSize: `${px(score, c.size ?? 44)}px`, lineHeight: '1.3', fontWeight: String(c.weight ?? 500), textAlign: 'center', whiteSpace: 'pre-line', borderRadius: `${px(score, 6)}px`}},
  ]};
}

/** The caption shown at a frame: captions cut in and out on their exact frames, start <= frame < end. */
export function captionsFrame(score, frame) {
  const caption = (score.captions ?? []).find(item => frame >= item.start && frame < item.end);
  return {captions: {style: {visibility: caption ? 'visible' : 'hidden'}}, caption: {text: caption ? copy(score, caption.copy) : ''}};
}

/** Index a built scene tree by key. */
export function nodesByKey(node, map = {}) {
  map[node.key] = node;
  for (const child of node.children ?? []) nodesByKey(child, map);
  return map;
}
