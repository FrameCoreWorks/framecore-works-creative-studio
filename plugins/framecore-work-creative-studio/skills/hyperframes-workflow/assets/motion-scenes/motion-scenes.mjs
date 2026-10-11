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
  easeOutBack: bezier(0.34, 1.56, 0.64, 1),
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
  'device': {required: ['screens'], copyParams: ['caption', 'url']},
  'lower-third': {required: ['name'], copyParams: ['name', 'title']},
  'bar-chart': {required: ['bars'], copyParams: []},
  'line-chart': {required: ['points'], copyParams: []},
  'photo-hero': {required: ['asset'], copyParams: ['lines']},
};

/** Eased 0..1 progress of an interval starting at master frame `start` and lasting `duration` frames. */
export const progress = (frame, start, duration, easing = 'linear') => easings[easing]((frame - start) / duration);

// Sizes are authored for a 1080 px short side, so 16:9, 9:16 and 1:1 share one type scale; tokens.contentScale
// enlarges everything in a format (1.25 fills a 9:16 frame better than the short-side scale alone).
const scale = score => Math.min(score.width, score.height) / 1080 * (score.tokens?.contentScale ?? 1);
const px = (score, value) => Math.round(value * scale(score));
const motion = score => ({entryFrames: 15, exitFrames: 10, lineStaggerFrames: 6, itemStaggerFrames: 8, entryEasing: 'easeOutCubic', exitEasing: 'easeInCubic', resolveEasing: 'easeOutExpo', ...score.motion});
const margin = score => Math.round(score.width * (score.tokens?.marginRatio ?? 0.08));
const list = value => (Array.isArray(value) ? value : value === undefined ? [] : [value]);
// Typography both renderers share: a one-letter word (Polish a, i, o, u, w, z) never ends a line, and a number stays
// with its unit ("90 zł", "10 kg", "50 %"); the space becomes a no-break space.
const UNIT = '(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|[gmlhs])(?!\\p{L})|%';
export const keepTogether = (text) => String(text)
  .replace(/(?<!\S)(\p{L}) +(?=\S)/gu, '$1\u00A0')
  .replace(/(\d) (?=\d{3}(?!\d))/gu, '$1\u00A0')
  .replace(new RegExp(`(\\d) (?=${UNIT})`, 'gu'), '$1\u00A0');
const copy = (score, id) => keepTogether(score.copy?.[id] ?? '');
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

// device: approved screenshots inside a drawn phone or window. Every size is computed here in whole
// pixels, so all renderers place the device, its screen and the caption identically.
export function deviceLayout(scene, score) {
  const p = scene.params ?? {}, W = score.width, H = score.height, m = margin(score);
  const area = score.tokens?.safeArea ?? {};
  const top = Math.round(H * (area.top ?? 0)), bottom = H - Math.round(H * (area.bottom ?? 0));
  const phone = (p.frame ?? 'phone') === 'phone', browser = p.frame === 'browser';
  const first = (score.assets ?? []).find(item => item.id === list(p.screens)[0]?.asset) ?? {};
  const aspect = first.width > 0 && first.height > 0 ? first.width / first.height : phone ? 9 / 19.5 : 16 / 10;
  const hasCaption = list(p.caption).length > 0, portrait = H > W, gap = px(score, 24);
  let box = {x: m, y: top, w: W - 2 * m, h: bottom - top}, caption = null;
  if (hasCaption && portrait) {
    const ch = Math.round((bottom - top) * 0.28);
    caption = {x: m, y: top, w: W - 2 * m, h: ch};
    box = {x: m, y: top + ch, w: W - 2 * m, h: bottom - top - ch};
  } else if (hasCaption) {
    const half = Math.round(W / 2);
    const left = {x: m, y: top, w: half - gap - m, h: bottom - top}, right = {x: half + gap, y: top, w: W - m - half - gap, h: bottom - top};
    [caption, box] = (p.side ?? 'left') === 'left' ? [left, right] : [right, left];
  }
  const bezel = phone ? px(score, 14) : 0, bar = phone ? 0 : px(score, browser ? 58 : 40);
  let sw, sh;
  if (phone) {
    sh = Math.round(box.h * 0.84); sw = Math.round(sh * aspect);
    if (sw + 2 * bezel > box.w * 0.9) { sw = Math.round(box.w * 0.9 - 2 * bezel); sh = Math.round(sw / aspect); }
  } else {
    sw = Math.round(box.w * 0.92); sh = Math.round(sw / aspect);
    if (sh + bar > box.h * 0.84) { sh = Math.round(box.h * 0.84 - bar); sw = Math.round(sh * aspect); }
  }
  const dw = sw + 2 * bezel, dh = sh + 2 * bezel + bar;
  const radius = phone ? Math.round(sw * 0.14) : px(score, 14);
  const field = px(score, 34);
  return {phone, browser, portrait, caption, bezel, bar, sw, sh, dw, dh, radius,
    address: browser ? {x: px(score, 96), y: Math.round((bar - field) / 2), w: dw - px(score, 96) - px(score, 20), h: field} : null,
    tap: px(score, 28),
    dx: Math.round(box.x + (box.w - dw) / 2), dy: Math.round(box.y + (box.h - dh) / 2),
    island: phone ? {x: Math.round((dw - sw * 0.3) / 2), y: bezel + px(score, 14), w: Math.round(sw * 0.3), h: px(score, 30)} : null};
}

// lower-third: a name and an optional title above the bottom edge or the safe area, with an accent bar at the
// left (none when centred). Every size is a whole pixel computed here, so all renderers place it identically.
export function lowerThirdLayout(scene, score) {
  const p = scene.params ?? {}, m = margin(score), area = score.tokens?.safeArea ?? {}, center = p.align === 'center';
  const nameSize = px(score, p.nameSize ?? 64), titleSize = px(score, p.titleSize ?? 40);
  const nameH = Math.round(nameSize * 1.2), titleH = list(p.title).length ? Math.round(titleSize * 1.3) : 0;
  const bar = center ? 0 : px(score, 8), gap = center ? 0 : px(score, 24);
  const bottom = score.height - Math.max(Math.round(score.height * (area.bottom ?? 0)), m);
  return {x: m, top: bottom - nameH - titleH, nameSize, titleSize, nameH, titleH, bar, center,
    textX: m + bar + gap, textW: score.width - 2 * m - bar - gap};
}

// bar-chart: one row per bar, its label above a bar that grows from the left and the value riding at the bar's
// end. The bars share one scale (params.max or the largest value) and leave room for the value at the right.
export function barChartLayout(scene, score) {
  const p = scene.params ?? {}, m = margin(score), area = score.tokens?.safeArea ?? {}, bars = list(p.bars);
  const max = p.max ?? Math.max(0, ...bars.map(bar => bar?.value ?? 0));
  const labelSize = px(score, p.size ?? 44), valueSize = px(score, p.valueSize ?? p.size ?? 44);
  const labelH = Math.round(labelSize * 1.2), valueH = Math.round(valueSize * 1.2), thickness = px(score, p.thickness ?? 36);
  const labelGap = px(score, 12), gap = px(score, p.gap ?? 40), valueGap = px(score, 16);
  const reserve = Math.round(valueSize * (p.valueWidth ?? 4.5)), full = score.width - 2 * m - reserve - valueGap;
  const row = labelH + labelGap + thickness, total = bars.length * row + Math.max(0, bars.length - 1) * gap;
  const top = Math.round(score.height * (area.top ?? 0)), bottom = score.height - Math.round(score.height * (area.bottom ?? 0));
  const y0 = Math.round(top + (bottom - top - total) / 2);
  return {x: m, labelSize, valueSize, labelH, valueH, thickness, valueGap, reserve, full, labelW: score.width - 2 * m,
    rows: bars.map((bar, i) => {
      const labelTop = y0 + i * (row + gap), barTop = labelTop + labelH + labelGap;
      return {labelTop, barTop, valueTop: barTop + Math.round((thickness - valueH) / 2), width: max > 0 ? Math.round(full * Math.max(0, bar?.value ?? 0) / max) : 0};
    })};
}

// line-chart: values on one scale, joined by a line drawn from the first point to the last; each point's dot and value
// appear when the line reaches it. Positions, lengths and angles are computed here, so every renderer draws the same line.
export function lineChartLayout(scene, score) {
  const p = scene.params ?? {}, m = margin(score), area = score.tokens?.safeArea ?? {}, values = list(p.points).map(point => point?.value ?? 0);
  const lo = p.min ?? Math.min(0, ...values), hi = p.max ?? Math.max(lo, ...values), span = hi > lo ? hi - lo : 1;
  const labelSize = px(score, p.size ?? 36), valueSize = px(score, p.valueSize ?? 40), labelH = Math.round(labelSize * 1.2), valueH = Math.round(valueSize * 1.2);
  const thickness = px(score, p.thickness ?? 8), dot = px(score, p.dot ?? 12), ring = px(score, 4), gap = px(score, 14), valueW = Math.round(valueSize * (p.valueWidth ?? 4));
  const top = Math.round(score.height * (area.top ?? 0)), bottom = score.height - Math.round(score.height * (area.bottom ?? 0));
  const height = Math.round((bottom - top) * (p.height ?? 0.6)), y0 = top + Math.round((bottom - top - height) / 2);
  const x0 = m + Math.round(valueW / 2), x1 = score.width - m - Math.round(valueW / 2), n = values.length;
  const plotTop = y0 + valueH + gap + dot, plotBottom = y0 + height - labelH - gap;
  const points = values.map((value, i) => ({x: n > 1 ? x0 + Math.round((x1 - x0) * i / (n - 1)) : x0, y: plotBottom - Math.round((value - lo) / span * (plotBottom - plotTop))}));
  const segments = points.slice(1).map((b, i) => {
    const a = points[i], dx = b.x - a.x, dy = b.y - a.y;
    return {x: a.x, y: a.y, length: Math.round(Math.sqrt(dx * dx + dy * dy)), angle: Math.round(Math.atan2(dy, dx) * 180 / Math.PI * 1000) / 1000};
  });
  const cum = [0];
  segments.forEach(s => cum.push(cum[cum.length - 1] + s.length));
  return {x0, x1, y0, height, plotTop, plotBottom, labelSize, valueSize, labelH, valueH, thickness, dot, ring, gap, valueW,
    labelW: n > 1 ? Math.round((x1 - x0) / (n - 1)) : x1 - x0, labelTop: plotBottom + gap, axisY: plotBottom + Math.round(gap / 3), axisH: Math.max(1, px(score, 2)),
    points, segments, cum, total: cum[cum.length - 1]};
}
/** The first frame at which the drawn line reaches each point of a line-chart scene. */
export function lineChartReach(scene, score, L = lineChartLayout(scene, score)) {
  const p = scene.params ?? {}, begin = scene.start + motion(score).entryFrames, duration = p.duration ?? 48, easing = p.easing ?? 'easeInOutCubic';
  return L.cum.map(d => {
    for (let f = begin; f < begin + duration; f++) if (progress(f, begin, duration, easing) * L.total >= d - 0.5) return f;
    return begin + duration;
  });
}
// Word-by-word entries (line-reveal params.entry 'words'): the Polish typesetting rules keep a one-letter word with the
// next and a number with its unit, and the gap between words is a fixed share of the type size in every renderer.
export const lineWords = (score, id) => captionItems(score.copy?.[id] ?? '').map(item => item.text);
const wordGap = size => Math.round(size * 0.28);

/** Describe the scene's elements. Each node: {key, type: 'box' | 'text' | 'image', text?, src?, style, children?}. */
export function buildScene(scene, score) {
  const content = buildContent(scene, score);
  const p = scene.params ?? {}, t = score.tokens ?? {}, sweep = exitMode(scene, score) === 'sweep';
  if (!sweep && !p.background) return content;
  // params.background: the scene's own canvas colour, optionally wiped in (params.backgroundWipe).
  const style = p.background ? {position: 'absolute', inset: '0', background: p.background} : {position: 'absolute', inset: '0'};
  return {key: 'scene', type: 'box', style, children: [content, ...(sweep ? [
    {key: 'sweep', type: 'box', style: {position: 'absolute', left: '0', top: '16%', bottom: '16%', width: `${px(score, 6)}px`, marginLeft: `-${px(score, 3)}px`, background: p.sweepColor ?? t.accent ?? t.foreground, opacity: '0'}}] : [])]};
}

/** The scene canvas wipe as CSS inset() lengths [top, right, bottom, left] in whole pixels, or null. */
export function backgroundWipe(scene, score, frame) {
  const p = scene.params ?? {}, side = p.backgroundWipe ?? 'none';
  if (!p.background || side === 'none') return null;
  const k = progress(frame, scene.start, p.backgroundFrames ?? 12, 'easeInOutCubic');
  const x = Math.round((1 - k) * score.width), y = Math.round((1 - k) * score.height);
  return {left: [0, x, 0, 0], right: [0, 0, 0, x], up: [y, 0, 0, 0], down: [0, 0, y, 0]}[side];
}

function buildContent(scene, score) {
  const p = scene.params ?? {}, t = score.tokens ?? {};
  switch (scene.kind) {
    case 'line-reveal': {
      const sizes = p.sizes ?? [132, 96], weights = p.weights ?? [700, 400];
      if (p.entry === 'words') return {key: 'container', type: 'box', style: column(score, p.align), children: list(p.lines).map((id, i) => {
        const size = px(score, sizes[i] ?? sizes[sizes.length - 1]), weight = String(weights[i] ?? weights[weights.length - 1]);
        return {key: `mask-${i}`, type: 'box', style: {display: 'flex', flexWrap: 'wrap', justifyContent: p.align === 'center' ? 'center' : 'flex-start', columnGap: `${wordGap(size)}px`, lineHeight: '1.1'},
          children: lineWords(score, id).map((word, j) => ({key: `word-mask-${i}-${j}`, type: 'box', style: {overflow: p.wordMotion === 'pop' ? 'visible' : 'hidden'},
            children: [{key: `word-${i}-${j}`, type: 'text', text: word, style: {display: 'block', fontSize: `${size}px`, fontWeight: weight, whiteSpace: 'nowrap', transformOrigin: '50% 100%'}}]}))};
      })};
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
    case 'device': {
      const d = deviceLayout(scene, score), body = p.deviceColor ?? (d.phone ? '#111214' : '#E9E9EC');
      const screens = list(p.screens).map((shot, i) => {
        const asset = (score.assets ?? []).find(item => item.id === shot.asset);
        return {key: `screen-${i}`, type: 'image', src: asset?.src ?? '', alt: asset?.alt ?? asset?.id ?? '', style: {position: 'absolute', left: '0', top: '0', width: `${d.sw}px`, height: `${d.sh}px`, objectFit: 'cover', opacity: '0'}};
      });
      const r = d.tap, ring = px(score, 3), accent = score.tokens?.accent ?? '#FFFFFF';
      list(p.taps).forEach((tap, i) => {
        const at = {position: 'absolute', left: `${Math.round((tap.x ?? 0.5) * d.sw) - r}px`, top: `${Math.round((tap.y ?? 0.5) * d.sh) - r}px`, width: `${2 * r}px`, height: `${2 * r}px`, borderRadius: `${r}px`, boxSizing: 'border-box', opacity: '0'};
        screens.push({key: `ripple-${i}`, type: 'box', style: {...at, border: `${ring}px solid ${accent}`}});
        screens.push({key: `tap-${i}`, type: 'box', style: {...at, border: `${ring}px solid rgba(0, 0, 0, 0.35)`, background: 'rgba(255, 255, 255, 0.75)', backgroundClip: 'padding-box'}});
      });
      const screen = {key: 'screen', type: 'box', children: screens, style: {position: 'absolute', left: `${d.bezel}px`, top: `${d.bezel + d.bar}px`, width: `${d.sw}px`, height: `${d.sh}px`, overflow: 'hidden', background: '#000', borderRadius: d.phone ? `${d.radius}px` : '0'}};
      const parts = d.phone
        ? [screen, {key: 'island', type: 'box', style: {position: 'absolute', left: `${d.island.x}px`, top: `${d.island.y}px`, width: `${d.island.w}px`, height: `${d.island.h}px`, borderRadius: `${Math.round(d.island.h / 2)}px`, background: body}}]
        : [screen, ...['#FF5F57', '#FEBC2E', '#28C840'].map((dot, i) => ({key: `dot-${i}`, type: 'box', style: {position: 'absolute', left: `${px(score, 20) + i * px(score, 22)}px`, top: `${Math.round((d.bar - px(score, 14)) / 2)}px`, width: `${px(score, 14)}px`, height: `${px(score, 14)}px`, borderRadius: `${px(score, 7)}px`, background: dot}})),
          ...(d.browser ? [{key: 'address', type: 'box', style: {position: 'absolute', left: `${d.address.x}px`, top: `${d.address.y}px`, width: `${d.address.w}px`, height: `${d.address.h}px`, borderRadius: `${Math.round(d.address.h / 2)}px`, background: '#FFFFFF', overflow: 'hidden'},
            children: [{key: 'url', type: 'text', text: copy(score, p.url), style: {position: 'absolute', left: `${px(score, 14)}px`, top: '0', height: `${d.address.h}px`, lineHeight: `${d.address.h}px`, fontSize: `${px(score, 20)}px`, fontWeight: '400', color: '#5F6368', whiteSpace: 'nowrap'}}]}] : [])];
      const device = {key: 'device', type: 'box', style: {position: 'absolute', left: `${d.dx}px`, top: `${d.dy}px`, width: `${d.dw}px`, height: `${d.dh}px`, transformOrigin: '0 0'}, children: [
        {key: 'body', type: 'box', children: parts, style: {position: 'absolute', inset: '0', overflow: 'hidden', borderRadius: `${d.phone ? d.radius + d.bezel : d.radius}px`, background: body}}]};
      const children = [device];
      if (d.caption) {
        const sizes = p.captionSizes ?? [72, 40], weights = p.captionWeights ?? [700, 400];
        children.push({key: 'caption', type: 'box', style: {position: 'absolute', left: `${d.caption.x}px`, top: `${d.caption.y}px`, width: `${d.caption.w}px`, height: `${d.caption.h}px`, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: d.portrait ? 'center' : 'stretch', textAlign: d.portrait ? 'center' : 'left'},
          children: list(p.caption).map((id, i) => ({key: `caption-mask-${i}`, type: 'box', style: {overflow: 'hidden', lineHeight: '1.2'},
            children: [{key: `caption-${i}`, type: 'text', text: copy(score, id), style: {fontSize: `${px(score, sizes[i] ?? sizes[sizes.length - 1])}px`, fontWeight: String(weights[i] ?? weights[weights.length - 1])}}]}))});
      }
      return {key: 'container', type: 'box', style: {position: 'absolute', inset: '0'}, children};
    }
    case 'lower-third': {
      const L = lowerThirdLayout(scene, score), align = L.center ? 'center' : 'left';
      const mask = (top, h) => ({position: 'absolute', left: `${L.textX}px`, top: `${top}px`, width: `${L.textW}px`, height: `${h}px`, overflow: 'hidden'});
      const line = (h, size, weight) => ({position: 'absolute', left: '0', top: '0', width: '100%', height: `${h}px`, lineHeight: `${h}px`, fontSize: `${size}px`, fontWeight: String(weight), whiteSpace: 'nowrap', textAlign: align});
      const children = [];
      if (L.bar) children.push({key: 'bar', type: 'box', style: {position: 'absolute', left: `${L.x}px`, top: `${L.top}px`, width: `${L.bar}px`, height: `${L.nameH + L.titleH}px`, background: p.barColor ?? t.accent ?? t.foreground, transformOrigin: 'center bottom'}});
      children.push({key: 'name-mask', type: 'box', style: mask(L.top, L.nameH), children: [{key: 'name', type: 'text', text: copy(score, p.name), style: line(L.nameH, L.nameSize, p.nameWeight ?? 700)}]});
      if (L.titleH) children.push({key: 'title-mask', type: 'box', style: mask(L.top + L.nameH, L.titleH), children: [{key: 'title', type: 'text', text: copy(score, p.title), style: {...line(L.titleH, L.titleSize, p.titleWeight ?? 400), color: t.muted ?? t.foreground}}]});
      return {key: 'container', type: 'box', style: {position: 'absolute', inset: '0'}, children};
    }
    case 'bar-chart': {
      const B = barChartLayout(scene, score), colour = p.barColor ?? t.accent ?? t.foreground, children = [];
      list(p.bars).forEach((bar, i) => {
        const r = B.rows[i];
        children.push({key: `label-${i}`, type: 'text', text: copy(score, bar?.label), style: {position: 'absolute', left: `${B.x}px`, top: `${r.labelTop}px`, width: `${B.labelW}px`, height: `${B.labelH}px`, lineHeight: `${B.labelH}px`, fontSize: `${B.labelSize}px`, fontWeight: String(p.labelWeight ?? 500), whiteSpace: 'nowrap'}});
        children.push({key: `bar-${i}`, type: 'box', style: {position: 'absolute', left: `${B.x}px`, top: `${r.barTop}px`, width: `${r.width}px`, height: `${B.thickness}px`, background: colour, transformOrigin: 'left center'}});
        children.push({key: `value-${i}`, type: 'text', text: '', style: {position: 'absolute', left: `${B.x + B.valueGap}px`, top: `${r.valueTop}px`, height: `${B.valueH}px`, lineHeight: `${B.valueH}px`, fontSize: `${B.valueSize}px`, fontWeight: '700', fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap'}});
      });
      return {key: 'container', type: 'box', style: {position: 'absolute', inset: '0'}, children};
    }
    case 'line-chart': {
      const L = lineChartLayout(scene, score), colour = p.lineColor ?? t.accent ?? t.foreground, muted = t.muted ?? t.foreground, children = [];
      const format = new Intl.NumberFormat(p.locale ?? 'en-US', {minimumFractionDigits: p.decimals ?? 0, maximumFractionDigits: p.decimals ?? 0});
      children.push({key: 'axis', type: 'box', style: {position: 'absolute', left: `${L.x0}px`, top: `${L.axisY}px`, width: `${L.x1 - L.x0}px`, height: `${L.axisH}px`, background: muted, transformOrigin: 'left center'}});
      list(p.points).forEach((point, i) => {
        if (point?.label) children.push({key: `label-${i}`, type: 'text', text: copy(score, point.label), style: {position: 'absolute', left: `${L.points[i].x - Math.round(L.labelW / 2)}px`, top: `${L.labelTop}px`, width: `${L.labelW}px`, height: `${L.labelH}px`, lineHeight: `${L.labelH}px`, fontSize: `${L.labelSize}px`, fontWeight: String(p.labelWeight ?? 500), textAlign: 'center', whiteSpace: 'nowrap', color: muted}});
      });
      L.segments.forEach((s, i) => children.push({key: `segment-${i}`, type: 'box', style: {position: 'absolute', left: `${s.x}px`, top: `${s.y - Math.round(L.thickness / 2)}px`, width: `${s.length}px`, height: `${L.thickness}px`, background: colour, transformOrigin: `0 ${Math.round(L.thickness / 2)}px`, transform: `rotate(${s.angle}deg) scaleX(0)`}}));
      list(p.points).forEach((point, i) => {
        const {x, y} = L.points[i];
        children.push({key: `dot-${i}`, type: 'box', style: {position: 'absolute', left: `${x - L.dot}px`, top: `${y - L.dot}px`, width: `${2 * L.dot}px`, height: `${2 * L.dot}px`, borderRadius: `${L.dot}px`, boxSizing: 'border-box', border: `${L.ring}px solid ${t.background ?? '#000000'}`, background: colour, backgroundClip: 'padding-box', opacity: '0'}});
        if ((p.values ?? 'last') === 'all' || ((p.values ?? 'last') === 'last' && i === L.points.length - 1)) children.push({key: `value-${i}`, type: 'text', text: `${p.prefix ?? ''}${format.format(point?.value ?? 0)}${p.suffix ?? ''}`, style: {position: 'absolute', left: `${x - Math.round(L.valueW / 2)}px`, top: `${y - L.dot - L.gap - L.valueH}px`, width: `${L.valueW}px`, height: `${L.valueH}px`, lineHeight: `${L.valueH}px`, fontSize: `${L.valueSize}px`, fontWeight: '700', textAlign: 'center', whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums', opacity: '0'}});
      });
      return {key: 'container', type: 'box', style: {position: 'absolute', inset: '0'}, children};
    }
    case 'photo-hero': {
      // The photo covers the frame around params.focus; a shade keeps the lines at the bottom readable.
      const asset = (score.assets ?? []).find(item => item.id === p.asset), f = p.focus ?? {}, at = `${(f.x ?? 0.5) * 100}% ${(f.y ?? 0.5) * 100}%`;
      const sizes = p.sizes ?? [96, 48], weights = p.weights ?? [700, 400], area = t.safeArea ?? {};
      const bottom = Math.max(Math.round(score.height * (area.bottom ?? 0)), margin(score)), top = Math.round(score.height * (area.top ?? 0));
      return {key: 'container', type: 'box', style: {position: 'absolute', inset: '0', overflow: 'hidden'}, children: [
        {key: 'photo', type: 'image', src: asset?.src ?? '', alt: asset?.alt ?? asset?.id ?? '', style: {position: 'absolute', left: '0', top: '0', width: `${score.width}px`, height: `${score.height}px`, objectFit: 'cover', objectPosition: at, transformOrigin: at, display: 'block'}},
        ...(p.shade === 0 ? [] : [{key: 'shade', type: 'box', style: {position: 'absolute', left: '0', right: '0', bottom: '0', height: `${Math.round(score.height * 0.6)}px`, background: `linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, ${p.shade ?? 0.6}))`}}]),
        {key: 'text', type: 'box', style: {position: 'absolute', inset: '0', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', alignItems: p.align === 'center' ? 'center' : 'stretch', padding: `${top}px ${margin(score)}px ${bottom}px`, boxSizing: 'border-box', color: p.color ?? '#FFFFFF'},
          children: list(p.lines).map((id, i) => ({key: `mask-${i}`, type: 'box', style: {overflow: 'hidden', lineHeight: '1.1'}, children: [
            {key: `line-${i}`, type: 'text', text: copy(score, id), style: {fontSize: `${px(score, sizes[i] ?? sizes[sizes.length - 1])}px`, fontWeight: String(weights[i] ?? weights[weights.length - 1])}}]}))},
      ]};
    }
    default:
      throw new Error(`Unknown scene kind: ${scene.kind}`);
  }
}

/** Device state at a frame: entry, camera focus {s, x, y} and each screen's offset and opacity. */
export function deviceFrame(scene, score, frame) {
  const p = scene.params ?? {}, m = motion(score), d = deviceLayout(scene, score);
  const entry = progress(frame, scene.start, m.entryFrames + 10, m.resolveEasing);
  // Camera focus: each key eases from the previous state to {scale, x, y} (fractions of the screen).
  let focus = {s: 1, x: 0.5, y: 0.5};
  for (const key of list(p.focus)) {
    const k = progress(frame, scene.start + (key.at ?? 0), key.frames ?? 24, 'easeInOutCubic');
    if (k <= 0) break;
    const to = {s: key.scale ?? 1, x: key.x ?? 0.5, y: key.y ?? 0.5};
    focus = {s: focus.s + (to.s - focus.s) * k, x: focus.x + (to.x - focus.x) * k, y: focus.y + (to.y - focus.y) * k};
  }
  const shots = list(p.screens), mode = p.transition ?? 'push', tf = p.transitionFrames ?? 12;
  let current = 0;
  shots.forEach((shot, i) => { if (frame >= scene.start + (shot.at ?? 0)) current = i; });
  const k = current === 0 || mode === 'cut' ? 1 : progress(frame, scene.start + (shots[current].at ?? 0), tf, 'easeInOutCubic');
  const screens = shots.map((_, i) => {
    if (i === current) return {opacity: 1, x: mode === 'push' ? Math.round((1 - k) * d.sw) : 0, alpha: mode === 'fade' ? k : 1};
    if (i === current - 1 && k < 1) return {opacity: 1, x: mode === 'push' ? -Math.round(k * d.sw) : 0, alpha: 1};
    return {opacity: 0, x: 0, alpha: 1};
  });
  // A tap: the marker arrives 4 frames before `at`, presses on `at`, a ring spreads, then the marker leaves.
  const taps = list(p.taps).map(tap => {
    const at = scene.start + (tap.at ?? 0);
    const arrive = progress(frame, at - 4, 4, 'easeOutCubic'), press = progress(frame, at, 3, 'easeInCubic') - progress(frame, at + 3, 5, 'easeOutCubic');
    const spread = progress(frame, at, 14, 'easeOutCubic');
    return {opacity: arrive * (1 - progress(frame, at + 8, 6, 'linear')), scale: (1.3 - 0.3 * arrive) * (1 - 0.15 * press),
      ripple: frame >= at ? 1 - spread : 0, rippleScale: 1 + spread};
  });
  const px0 = d.bezel + focus.x * d.sw, py0 = d.bezel + d.bar + focus.y * d.sh;
  return {layout: d, entry, focus, screens, taps, tx: px0 * (1 - focus.s), ty: py0 * (1 - focus.s) + (1 - entry) * px(score, 60)};
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
  const wipe = backgroundWipe(scene, score, frame);
  if (wipe) out.scene = {style: {clipPath: `inset(${wipe.map(v => `${v}px`).join(' ')})`}};
  // A full-frame photo fades without the lift, so the frame edge never shows.
  out.container = {style: {opacity: String(1 - e), transform: mode === 'sweep' ? `translateX(${-px(score, 150) * e}px)` : `translateY(${-(scene.kind === 'photo-hero' ? 0 : px(score, 24)) * e}px)`}};
  if (mode === 'sweep') {
    const k = progress(frame, exitStart, sweepFrames, 'easeInOutCubic'), from = margin(score), to = score.width - margin(score);
    out.sweep = {style: {opacity: k > 0 && k < 1 ? '1' : '0', transform: `translateX(${Math.round(from + (to - from) * k)}px)`}};
  }
  switch (scene.kind) {
    case 'line-reveal':
      if (p.entry === 'words') {
        // Word by word through all lines: each word rises from its mask ('rise') or springs up from 60 % ('pop').
        let n = 0;
        list(p.lines).forEach((id, i) => lineWords(score, id).forEach((_, j) => {
          const begin = scene.start + n++ * (p.wordStaggerFrames ?? 3);
          if (p.wordMotion === 'pop') {
            const k = progress(frame, begin, m.entryFrames, p.wordEasing ?? 'easeOutBack');
            out[`word-${i}-${j}`] = {style: {opacity: String(progress(frame, begin, Math.max(1, Math.round(m.entryFrames / 2)), 'linear')), transform: `scale(${0.6 + 0.4 * k})`}};
          } else {
            const k = progress(frame, begin, m.entryFrames, p.wordEasing ?? m.entryEasing);
            out[`word-${i}-${j}`] = {style: {transform: `translateY(${(1 - k) * 110}%)`}};
          }
        }));
        break;
      }
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
    case 'device': {
      const f = deviceFrame(scene, score, frame);
      out.device = {style: {opacity: String(f.entry), transform: `translate(${f.tx}px, ${f.ty}px) scale(${f.focus.s})`}};
      f.screens.forEach((state, i) => { out[`screen-${i}`] = {style: {opacity: String(state.opacity * state.alpha), transform: `translateX(${state.x}px)`}}; });
      f.taps.forEach((tap, i) => {
        out[`tap-${i}`] = {style: {opacity: String(tap.opacity), transform: `scale(${tap.scale})`}};
        out[`ripple-${i}`] = {style: {opacity: String(tap.ripple), transform: `scale(${tap.rippleScale})`}};
      });
      list(p.caption).forEach((_, i) => {
        const c = progress(frame, scene.start + 10 + i * m.lineStaggerFrames, m.entryFrames, m.entryEasing);
        out[`caption-${i}`] = {style: {transform: `translateY(${(1 - c) * 110}%)`}};
      });
      break;
    }
    case 'lower-third': {
      // The bar rises first, then the name and the title slide up inside their masks.
      if (lowerThirdLayout(scene, score).bar) out.bar = {style: {transform: `scaleY(${progress(frame, scene.start, m.entryFrames, m.entryEasing)})`}};
      out.name = {style: {transform: `translateY(${(1 - progress(frame, scene.start + 4, m.entryFrames, m.entryEasing)) * 110}%)`}};
      if (list(p.title).length) out.title = {style: {transform: `translateY(${(1 - progress(frame, scene.start + 4 + m.lineStaggerFrames, m.entryFrames, m.entryEasing)) * 110}%)`}};
      break;
    }
    case 'bar-chart': {
      // Each row in turn: the label settles, then the bar grows and its value counts up at the bar's end.
      const B = barChartLayout(scene, score);
      const format = new Intl.NumberFormat(p.locale ?? 'en-US', {minimumFractionDigits: p.decimals ?? 0, maximumFractionDigits: p.decimals ?? 0});
      list(p.bars).forEach((bar, i) => {
        const begin = scene.start + i * m.itemStaggerFrames;
        const label = progress(frame, begin, m.entryFrames, m.entryEasing);
        const k = progress(frame, begin + 6, p.duration ?? 36, p.easing ?? m.resolveEasing);
        out[`label-${i}`] = {style: {opacity: String(label), transform: `translateY(${(1 - label) * px(score, 16)}px)`}};
        out[`bar-${i}`] = {style: {transform: `scaleX(${k})`}};
        out[`value-${i}`] = {style: {opacity: String(label), transform: `translateX(${Math.round(B.rows[i].width * k)}px)`}, text: `${p.prefix ?? ''}${format.format((bar?.value ?? 0) * k)}${p.suffix ?? ''}`};
      });
      break;
    }
    case 'line-chart': {
      // The axis and labels settle, then the line draws from the first point; each dot and value appear on arrival.
      const L = lineChartLayout(scene, score), reach = lineChartReach(scene, score, L), shown = p.values ?? 'last';
      const drawn = progress(frame, scene.start + m.entryFrames, p.duration ?? 48, p.easing ?? 'easeInOutCubic') * L.total;
      const axis = progress(frame, scene.start, m.entryFrames, m.entryEasing);
      out.axis = {style: {transform: `scaleX(${axis})`}};
      L.segments.forEach((s, i) => { out[`segment-${i}`] = {style: {transform: `rotate(${s.angle}deg) scaleX(${s.length ? Math.min(1, Math.max(0, (drawn - L.cum[i]) / s.length)) : 1})`}}; });
      list(p.points).forEach((point, i) => {
        if (point?.label) out[`label-${i}`] = {style: {opacity: String(axis), transform: `translateY(${(1 - axis) * px(score, 16)}px)`}};
        out[`dot-${i}`] = {style: {opacity: String(progress(frame, reach[i], 6, 'easeOutCubic'))}};
        if (shown === 'all' || (shown === 'last' && i === L.points.length - 1)) out[`value-${i}`] = {style: {opacity: String(progress(frame, reach[i], m.entryFrames, m.entryEasing))}};
      });
      break;
    }
    case 'photo-hero': {
      // The photo pushes in from zoom[0] to zoom[1] and drifts up by params.parallax px over the whole scene, while the
      // lines rise from their masks over it.
      const zoom = p.zoom ?? [1, 1.08], length = scene.end - scene.start;
      const s = zoom[0] + (zoom[1] - zoom[0]) * progress(frame, scene.start, length, p.zoomEasing ?? 'linear');
      const drift = px(score, p.parallax ?? 0) * progress(frame, scene.start, length, 'linear');
      out.photo = {style: {opacity: String(p.fadeFrames ? progress(frame, scene.start, p.fadeFrames, 'linear') : 1), transform: `translateY(${-drift}px) scale(${s})`}};
      list(p.lines).forEach((_, i) => {
        const k = progress(frame, scene.start + (p.textDelay ?? 8) + i * m.lineStaggerFrames, m.entryFrames, m.entryEasing);
        out[`line-${i}`] = {style: {transform: `translateY(${(1 - k) * 110}%)`}};
      });
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

// Caption words as flex items for the active-word preset: the Polish typesetting rules decide which words stay
// together (a one-letter word with the next, a number with its unit), and each item lists the indexes of the words
// it holds, so caption.words timings select it.
export function captionItems(text) {
  let index = 0;
  return keepTogether(String(text).split(/\s+/).filter(Boolean).join(' ')).split(' ').filter(Boolean).map(part => {
    const words = part.split('\u00A0').map(() => index++);
    return {text: part, words};
  });
}
const activeWordStyle = (score, c) => ({size: px(score, c.size ?? 64), pad: px(score, 12), radius: px(score, 10), gap: px(score, 10),
  line: Math.round(px(score, c.size ?? 64) * 1.3), rowGap: px(score, 8)});

// Caption layer for score.captions [{id, start, end, copy, words?}].
function captionLayer(score) {
  if (!score.captions?.length) return null;
  const t = score.tokens ?? {}, c = t.captions ?? {};
  if (c.preset === 'active-word') {
    // Every word in its own box; the spoken word lights up (captionsFrame). Rows wrap and centre above `bottom`.
    const bottom = Math.max(Math.round(score.height * (t.safeArea?.bottom ?? 0)), Math.round(score.height * (c.bottom ?? 0.2)));
    const a = activeWordStyle(score, c);
    return {key: 'captions', type: 'box', style: {position: 'absolute', left: `${margin(score)}px`, right: `${margin(score)}px`, bottom: `${bottom}px`, height: '0'}, children: score.captions.map((caption, i) => ({
      key: `caption-${i}`, type: 'box', style: {position: 'absolute', left: '0', right: '0', bottom: '0', display: 'flex', flexWrap: 'wrap', justifyContent: 'center', columnGap: `${a.gap}px`, rowGap: `${a.rowGap}px`, visibility: 'hidden'},
      children: captionItems(score.copy?.[caption.copy] ?? '').map((item, j) => ({key: `caption-${i}-${j}`, type: 'text', text: c.uppercase ? item.text.toUpperCase() : item.text,
        style: {padding: `0 ${a.pad}px`, height: `${a.line}px`, lineHeight: `${a.line}px`, fontSize: `${a.size}px`, fontWeight: String(c.weight ?? 800), color: c.color ?? '#FFFFFF', background: c.wordBackground ?? 'rgba(0, 0, 0, 0.6)', borderRadius: `${a.radius}px`, whiteSpace: 'nowrap'}})),
    }))};
  }
  const bottom = Math.max(Math.round(score.height * (t.safeArea?.bottom ?? 0)), Math.round(score.height * (c.bottom ?? 0.08)));
  return {key: 'captions', type: 'box', style: {position: 'absolute', left: `${margin(score)}px`, right: `${margin(score)}px`, bottom: `${bottom}px`, display: 'flex', justifyContent: 'center'}, children: [
    {key: 'caption', type: 'text', text: '', style: {maxWidth: '100%', padding: `${px(score, 10)}px ${px(score, 22)}px`, background: c.background ?? 'rgba(0, 0, 0, 0.8)', color: c.color ?? '#FFFFFF', fontSize: `${px(score, c.size ?? 44)}px`, lineHeight: '1.3', fontWeight: String(c.weight ?? 500), textAlign: 'center', whiteSpace: 'pre-line', borderRadius: `${px(score, 6)}px`}},
  ]};
}

// The caption shown at a frame: captions cut in and out on their exact frames, start <= frame < end.
function captionLayerFrame(score, frame) {
  const t = score.tokens ?? {}, c = t.captions ?? {};
  if (c.preset === 'active-word') {
    const out = {};
    (score.captions ?? []).forEach((caption, i) => {
      const shown = frame >= caption.start && frame < caption.end;
      out[`caption-${i}`] = {style: {visibility: shown ? 'visible' : 'hidden'}};
      if (!shown) return;
      captionItems(score.copy?.[caption.copy] ?? '').forEach((item, j) => {
        const active = item.words.some(w => { const span = caption.words?.[w]; return Array.isArray(span) && frame >= span[0] && frame < span[1]; });
        out[`caption-${i}-${j}`] = {style: {background: active ? c.activeColor ?? t.accent ?? '#FFD400' : c.wordBackground ?? 'rgba(0, 0, 0, 0.6)', color: active ? c.activeText ?? '#111111' : c.color ?? '#FFFFFF'}};
      });
    });
    return out;
  }
  const caption = (score.captions ?? []).find(item => frame >= item.start && frame < item.end);
  return {captions: {style: {visibility: caption ? 'visible' : 'hidden'}}, caption: {text: caption ? copy(score, caption.copy) : ''}};
}

// Persistent elements stay on screen across scenes (a logo in a corner, a price tag, a web address):
// score.persistent [{id, asset | copy, position, from, to, ...}], inside the side margin and the safe area or margin.
const persistentAt = (score, item) => {
  const area = score.tokens?.safeArea ?? {}, m = margin(score), [v, h] = String(item.position ?? 'top-right').split('-');
  return {[v]: `${Math.max(Math.round(score.height * (area[v] ?? 0)), m)}px`, [h]: `${m}px`};
};
export function buildPersistent(score) {
  const t = score.tokens ?? {};
  return list(score.persistent).map(item => {
    const at = {position: 'absolute', ...persistentAt(score, item), opacity: '0', visibility: 'hidden'};
    if (item.asset) {
      const asset = (score.assets ?? []).find(a => a.id === item.asset);
      return {key: `persistent-${item.id}`, type: 'image', src: asset?.src ?? '', alt: asset?.alt ?? asset?.id ?? '', style: {...at, width: `${px(score, item.width ?? 160)}px`, height: 'auto', display: 'block'}};
    }
    const size = px(score, item.size ?? 36), line = Math.round(size * 1.3), filled = item.background !== 'none';
    return {key: `persistent-${item.id}`, type: 'text', text: copy(score, item.copy), style: {...at, padding: `0 ${filled ? px(score, 16) : 0}px`, height: `${line}px`, lineHeight: `${line}px`, fontSize: `${size}px`, fontWeight: String(item.weight ?? 700), whiteSpace: 'nowrap',
      color: item.color ?? (filled ? t.background : t.foreground) ?? '#FFFFFF', background: filled ? item.background ?? t.accent ?? '#000000' : 'transparent', borderRadius: `${px(score, item.radius ?? 8)}px`}};
  });
}
/** Persistent element styles at a frame: shown for from <= frame < to, fading in and out unless at the timeline's ends. */
export function persistentFrame(score, frame) {
  const m = motion(score), out = {};
  for (const item of list(score.persistent)) {
    const from = item.from ?? 0, to = item.to ?? score.totalFrames, shown = frame >= from && frame < to;
    const k = from === 0 ? 1 : progress(frame, from, m.entryFrames, m.entryEasing), e = to >= score.totalFrames ? 0 : progress(frame, to - m.exitFrames, m.exitFrames, m.exitEasing);
    out[`persistent-${item.id}`] = {style: {opacity: String(shown ? k * (1 - e) : 0), visibility: shown ? 'visible' : 'hidden'}};
  }
  return out;
}

/** Overlay above the scenes: persistent elements, then the captions; null when the contract has neither. */
export function buildCaptions(score) {
  const layer = captionLayer(score), persistent = buildPersistent(score);
  if (!persistent.length) return layer;
  return {key: 'overlay', type: 'box', style: {position: 'absolute', inset: '0', pointerEvents: 'none'}, children: layer ? [...persistent, layer] : persistent};
}
/** Overlay styles at a frame: persistent elements and the caption shown, start <= frame < end. */
export function captionsFrame(score, frame) {
  return {...persistentFrame(score, frame), ...(score.captions?.length ? captionLayerFrame(score, frame) : {})};
}

/** Index a built scene tree by key. */
export function nodesByKey(node, map = {}) {
  map[node.key] = node;
  for (const child of node.children ?? []) nodesByKey(child, map);
  return map;
}
