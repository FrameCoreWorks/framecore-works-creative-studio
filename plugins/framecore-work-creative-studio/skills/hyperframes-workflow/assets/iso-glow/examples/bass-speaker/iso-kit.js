// Iso Glow kit: isometric hairline drawing with glow lighting for seekable video (HyperFrames, GSAP, any frame-driven runtime).
// Projection kernel after iso-figure by Tolga Cohce; glow vocabulary after iso-glow by April Zhu. Both MIT, see LICENSE.upstream.
// Everything is drawn on flat face planes and mapped with one isometric matrix, so ordinary rects, circles and text land on a face.
(function (root) {
  const NS = 'http://www.w3.org/2000/svg';
  const C = Math.cos(Math.PI / 6), S = Math.sin(Math.PI / 6);

  // +x runs down-right, +y down-left, +z up. (OX, OY) is where the origin lands on screen; scale is pixels per unit.
  function frame(OX, OY, scale = 1) {
    const P = (x, y, z) => [(x - y) * C * scale + OX, ((x + y) * S - z) * scale + OY];
    const D = (x, y, z) => [(x - y) * C * scale, ((x + y) * S - z) * scale];
    const plane = (O, U, V) => { const o = P(...O), u = D(...U), v = D(...V); return `matrix(${u[0]} ${u[1]} ${v[0]} ${v[1]} ${o[0]} ${o[1]})`; };
    // Each takes the face's top-left corner: local u grows along the face, local v grows downward.
    const TOP = (x, y, z) => plane([x, y, z], [1, 0, 0], [0, 1, 0]);
    const FRONT = (x, y, z) => plane([x, y, z], [1, 0, 0], [0, 0, -1]);   // the y = max face, lower left
    const SIDE = (x, y, z) => plane([x, y, z], [0, -1, 0], [0, 0, -1]);   // the x = max face, lower right
    return { P, D, plane, TOP, FRONT, SIDE, scale };
  }

  function el(tag, attrs, parent) {
    const node = document.createElementNS(NS, tag);
    for (const key in attrs) node.setAttribute(key, attrs[key]);
    if (parent) parent.appendChild(node);
    return node;
  }

  // One shared glow filter. userSpaceOnUse keeps perfectly straight lines (a zero-height box) from vanishing.
  function defs(svg, { blur = 5, spread = 16 } = {}) {
    const d = el('defs', {}, svg);
    const f = el('filter', { id: 'iso-glow', filterUnits: 'userSpaceOnUse', x: -200, y: -200, width: 4000, height: 4000 }, d);
    el('feGaussianBlur', { in: 'SourceGraphic', stdDeviation: blur, result: 'near' }, f);
    el('feGaussianBlur', { in: 'SourceGraphic', stdDeviation: spread, result: 'far' }, f);
    const m = el('feMerge', {}, f);
    ['far', 'near', 'SourceGraphic'].forEach(n => el('feMergeNode', { in: n }, m));
    return d;
  }

  // A box is its three visible faces with opaque fills; draw boxes back to front (smaller x + y first, lower z first).
  function box(K, parent, x, y, z, w, d, h, cls = {}) {
    const g = el('g', {}, parent);
    const face = (transform, fw, fh, fill) => {
      const f = el('g', { transform }, g);
      el('rect', { class: fill, x: 0, y: 0, width: fw, height: fh }, f);
      el('rect', { class: cls.line || 'iso-line', x: 0, y: 0, width: fw, height: fh }, f);
      return f;
    };
    return {
      g,
      side: face(K.SIDE(x + w, y + d, z + h), d, h, cls.side || 'iso-side'),
      front: face(K.FRONT(x, y + d, z + h), w, h, cls.front || 'iso-front'),
      top: face(K.TOP(x, y, z + h), w, d, cls.top || 'iso-top'),
    };
  }

  // A part that lights up: `draw(group, cls)` runs twice, once in hairline grey and once in the accent inside the
  // glow filter. Animate `.lit` opacity (0 = off, 1 = fully lit); the grey copy keeps the drawing readable when off.
  function lit(parent, draw) {
    const base = el('g', {}, parent);
    const glow = el('g', { opacity: 0, filter: 'url(#iso-glow)' }, parent);
    draw(base, 'iso-line');
    draw(glow, 'iso-lit');
    return { base, lit: glow, set: v => glow.setAttribute('opacity', Math.max(0, Math.min(1, v)).toFixed(3)) };
  }

  // Parallel hairlines on a face plane (window grids, ribs, grilles): from a0 to a1 every step, each spanning b0 to b1.
  function slits(parent, a0, a1, step, b0, b1, vertical = true, cls = 'iso-detail') {
    for (let a = a0; a <= a1 + 1e-6; a += step)
      el('line', vertical ? { class: cls, x1: a, y1: b0, x2: a, y2: b1 } : { class: cls, x1: b0, y1: a, x2: b1, y2: a }, parent);
  }

  // The envelope value at time t (seconds), linearly interpolated between frames; ENVELOPE comes from audio_envelope.py.
  function envAt(envelope, t) {
    const list = envelope.env, f = Math.max(0, t * envelope.fps), i = Math.floor(f);
    const a = list[Math.min(i, list.length - 1)] || 0, b = list[Math.min(i + 1, list.length - 1)] || 0;
    return a + (b - a) * (f - i);
  }

  // Deterministic driver: `update(t)` runs whenever the paused timeline is rendered at time t, including on seek,
  // so a frame-by-frame capture shows exactly the state for that frame. Never use requestAnimationFrame in a video.
  function drive(timeline, duration, update) {
    const proxy = { p: 0 };
    timeline.to(proxy, { p: 1, duration, ease: 'none', onUpdate: () => update(timeline.time()) }, 0);
    return timeline;
  }

  // A deterministic stand-in envelope at a tempo, for drafting before the real track is analysed.
  function demoEnvelope(duration, fps = 30, bpm = 120, first = 0) {
    const env = [], kicks = [], beat = 60 / bpm;
    for (let t = first; t < duration; t += beat) kicks.push(Math.round(t * 1000) / 1000);
    for (let i = 0; i < Math.round(duration * fps); i++) {
      const t = i / fps, since = ((t - first) % beat + beat) % beat;
      env.push(Math.round((0.15 + 0.85 * Math.exp(-since * 7)) * 1000) / 1000);
    }
    return { fps, start: 0, duration, band: 'demo', env, kicks };
  }

  root.IsoKit = { NS, frame, el, defs, box, lit, slits, envAt, drive, demoEnvelope };
})(typeof window !== 'undefined' ? window : globalThis);
