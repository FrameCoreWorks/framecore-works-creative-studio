// Hairline kit: isometric line figures built from rounded solids, for seekable video (HyperFrames, capture-html, any frame-driven runtime).
// The drawing method follows hairline by Lucas Marques (MIT, see LICENSE.upstream); this code is Studio's own, written for video:
// every value is a pure function of the timeline time, so seeking to any frame draws exactly that frame.
(function (root) {
  const NS = 'http://www.w3.org/2000/svg';

  // +x runs down-right, +y down-left, +z up. 'iso' is the 30 degree view of the Iso Glow kit; 'dimetric' is the 2:1 view.
  function frame(OX, OY, scale = 1, view = 'iso') {
    const a = view === 'dimetric' ? Math.atan(0.5) : Math.PI / 6;
    const cx = Math.cos(a), sy = Math.sin(a);
    const P = (x, y, z = 0) => [(x - y) * cx * scale + OX, ((x + y) * sy - z) * scale + OY];
    return { P, scale, view };
  }

  function el(tag, attrs, parent) {
    const node = document.createElementNS(NS, tag);
    for (const key in attrs) node.setAttribute(key, attrs[key]);
    if (parent) parent.appendChild(node);
    return node;
  }

  // A rounded rectangle on the ground plane as a closed ring of points, counter-clockwise, `steps` points per corner arc.
  // r is clamped to half the shorter side, so r = w / 2 on a square gives a circle (a jar, a dial, a pillar).
  function rrect(x0, y0, x1, y1, r, steps = 6) {
    const w = x1 - x0, d = y1 - y0, rr = Math.max(0, Math.min(r, w / 2, d / 2)), pts = [];
    const corners = [[x1 - rr, y1 - rr, 0], [x0 + rr, y1 - rr, 0.5], [x0 + rr, y0 + rr, 1], [x1 - rr, y0 + rr, 1.5]];
    for (const [cx, cy, start] of corners)
      for (let k = 0; k <= steps; k++) {
        const t = (start + 0.5 * k / steps) * Math.PI;
        pts.push([cx + rr * Math.cos(t), cy + rr * Math.sin(t)]);
      }
    return pts;
  }

  const ringAt = (P, ring, z) => ring.map(([x, y]) => P(x, y, z));

  // Convex hull of screen points (monotone chain), clockwise on screen.
  function hull(points) {
    const pts = points.map(p => [+p[0].toFixed(3), +p[1].toFixed(3)]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    if (pts.length < 3) return pts;
    const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    const half = list => {
      const out = [];
      for (const p of list) {
        while (out.length >= 2 && cross(out[out.length - 2], out[out.length - 1], p) <= 0) out.pop();
        out.push(p);
      }
      out.pop();
      return out;
    };
    return half(pts).concat(half(pts.slice().reverse()));
  }

  const fmt = n => (Math.round(n * 100) / 100).toString();
  function path(points, closed = true) {
    if (!points.length) return '';
    return 'M' + points.map(p => fmt(p[0]) + ' ' + fmt(p[1])).join('L') + (closed ? 'Z' : '');
  }

  // The near run of a projected ring: from its leftmost to its rightmost screen point through the lowest one.
  // On a top face that is the edge the walls meet, which the hull does not draw: the crease.
  function nearRun(screen) {
    let lo = 0, hi = 0, low = 0;
    screen.forEach((p, i) => {
      if (p[0] < screen[lo][0]) lo = i;
      if (p[0] > screen[hi][0]) hi = i;
      if (p[1] > screen[low][1]) low = i;
    });
    const n = screen.length, run = i => { const out = []; for (let k = lo; ; k = (k + i + n) % n) { out.push(k); if (k === hi) break; } return out; };
    const a = run(1), b = run(-1);
    return (a.includes(low) ? a : b).map(k => screen[k]);
  }

  // A rounded solid: the silhouette is the hull of its foot ring and its top ring; the only inner line is one crease,
  // the near run of the top ring inset by `inset`. No vertical corner is ever drawn. Draw solids back to front:
  // smaller x + y first, lower z first. Returns the two path strings, to `put` into a group or to redraw on each frame.
  function solid(P, { x, y, w, d, z = 0, h, r = 2, inset = 1.4, top = null, steps = 6 }) {
    const foot = rrect(x, y, x + w, y + d, r, steps);
    const t = top || { x, y, w, d, r };
    const head = rrect(t.x, t.y, t.x + t.w, t.y + t.d, t.r, steps);
    const inner = rrect(t.x + inset, t.y + inset, t.x + t.w - inset, t.y + t.d - inset, Math.max(0, t.r - inset), steps);
    return {
      sil: path(hull(ringAt(P, foot, z).concat(ringAt(P, head, z + h)))),
      crease: path(nearRun(ringAt(P, inner, z + h)), false),
    };
  }

  // A group holding one solid's two paths. The silhouette keeps the plate fill so it hides what is behind it.
  function put(parent, shape, cls = {}) {
    const g = el('g', {}, parent);
    const sil = el('path', { class: cls.sil || 'hl-sil', d: shape.sil }, g);
    const crease = el('path', { class: cls.crease || 'hl-crease', d: shape.crease }, g);
    return { g, sil, crease, draw: s => { sil.setAttribute('d', s.sil); crease.setAttribute('d', s.crease); } };
  }

  // Motion: two clocks, both pure functions of time.
  // A choice (which part) gets a long ease-out, 0.7 s on cubic-bezier(.32, .72, 0, 1).
  function bezier(x1, y1, x2, y2) {
    const f = (a, b, s) => 3 * a * s * (1 - s) ** 2 + 3 * b * s * s * (1 - s) + s ** 3;
    return u => {
      if (u <= 0) return 0;
      if (u >= 1) return 1;
      let lo = 0, hi = 1;
      for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (f(x1, x2, m) < u) lo = m; else hi = m; }
      return f(y1, y2, (lo + hi) / 2);
    };
  }
  const easeOut = bezier(0.32, 0.72, 0, 1);

  // The value at time t of something that starts at v0 and is sent to `to` at each change [{ t, to }], each move
  // taking `dur` seconds from wherever the value was when the change came.
  function tweenAt(t, v0, changes, dur = 0.7, ease = easeOut) {
    let from = v0, target = v0, start = -Infinity;
    for (const c of changes) {
      if (c.t > t) break;
      from = start === -Infinity ? target : from + (target - from) * ease((c.t - start) / dur);
      target = c.to; start = c.t;
    }
    return start === -Infinity ? v0 : from + (target - from) * ease((t - start) / dur);
  }

  // A position (where) gets a spring, k 100, c 18, m 1. A spring at rest sent a step of 1 at time 0 is at
  // springStep(t); its target moving in steps is the sum of those responses, exactly, so no state is carried.
  function springStep(t, k = 100, c = 18, m = 1) {
    if (t <= 0) return 0;
    const w0 = Math.sqrt(k / m), z = c / (2 * Math.sqrt(k * m));
    if (z < 1) {
      const wd = w0 * Math.sqrt(1 - z * z);
      return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t));
    }
    if (z === 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
    const s = Math.sqrt(z * z - 1), r1 = -w0 * (z - s), r2 = -w0 * (z + s);
    return 1 + (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r1 - r2);
  }
  function springAt(t, v0, changes, k, c, m) {
    let v = v0, last = v0;
    for (const ch of changes) {
      if (ch.t > t) break;
      v += (ch.to - last) * springStep(t - ch.t, k, c, m);
      last = ch.to;
    }
    return v;
  }

  // Stagger by distance: the part `i` away from the chosen part `a` starts later, so the answer spreads out from it.
  const stagger = (i, a, step = 0.045) => Math.abs(i - a) * step;

  // Reach with a far end: 1 at the chosen part, easing down to a floor, never below it and never past 1.
  const falloff = (dist, radius, floor = 0.09) => Math.max(floor, Math.min(1, Math.exp(-(dist * dist) / (2 * radius * radius))));

  // A tour: the stops a hand would visit [{ t, at }] where `at` names the chosen part, or null for rest.
  // Returns which part is chosen at time t.
  function tourAt(t, stops) {
    let at = null;
    for (const s of stops) { if (s.t > t) break; at = s.at; }
    return at;
  }

  // Deterministic driver for a paused GSAP timeline (HyperFrames); capture-html calls window.renderFrame(t) instead.
  function drive(timeline, duration, update) {
    const proxy = { p: 0 };
    timeline.to(proxy, { p: 1, duration, ease: 'none', onUpdate: () => update(timeline.time()) }, 0);
    return timeline;
  }

  root.HairlineKit = { NS, frame, el, rrect, ringAt, hull, path, nearRun, solid, put, bezier, easeOut, tweenAt, springStep, springAt, stagger, falloff, tourAt, drive };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.HairlineKit;
})(typeof window !== 'undefined' ? window : globalThis);
