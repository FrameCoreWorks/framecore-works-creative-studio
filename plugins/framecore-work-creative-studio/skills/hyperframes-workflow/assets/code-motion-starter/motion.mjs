// Original synthetic teaching asset. No provider, DOM, clock or network dependency.
export const contract = {
  id: 'synthetic-code-motion', revision: 1, approval: 'example-not-client-approved',
  width: 640, height: 360, fps: 30, totalFrames: 180,
  colors: {background: '#f3eee2', ink: '#182023', accent: '#b83a24'},
  font: 'sans-serif', audio: 'intentional-silence',
  scenes: [
    {id: 'SC01', start: 0, end: 72, copy: 'PLAN', hold: [12, 60]},
    {id: 'SC02', start: 60, end: 144, copy: 'BUILD', hold: [72, 132]},
    {id: 'SC03', start: 132, end: 180, copy: 'REVIEW', hold: [144, 180]},
  ],
};
const clamp = (v) => Math.max(0, Math.min(1, v));
const ease = (v) => 1 - Math.pow(1 - clamp(v), 3);
const mix = (a, b, t) => a + (b - a) * t;
const number = (v) => Number(v.toFixed(4));
const escape = (text) => String(text).replace(/[&<>"']/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;',
})[c]);

export function stateAtFrame(frame) {
  if (!Number.isInteger(frame) || frame < 0 || frame >= contract.totalFrames) {
    throw new RangeError('Frame must be an integer in [0, totalFrames).');
  }
  const alignment = ease(frame / 45);
  const connection = clamp((frame - 72) / 48); // Deliberate constant velocity.
  const outline = ease((frame - 144) / 12);
  const initial = [[90, 90], [284, 150], [470, 70]];
  return {
    frame,
    blocks: initial.map(([x, y], i) => ({
      x: number(mix(x, 100 + i * 170, alignment)),
      y: number(mix(y, 104, alignment)),
    })),
    connection: number(connection),
    outline: number(outline),
    labels: contract.scenes.map((scene, i) => {
      const active = frame >= scene.start && frame < scene.end;
      const enter = i === 0 ? 1 : clamp((frame - scene.start) / 12);
      const exit = i === 2 ? 1 : clamp((scene.end - frame) / 12);
      return {id: scene.id, copy: scene.copy, opacity: active ? number(Math.min(enter, exit)) : 0};
    }),
  };
}

export function svgAtFrame(frame) {
  const state = stateAtFrame(frame);
  const {width, height, colors, font} = contract;
  const blocks = state.blocks.map(({x, y}) =>
    '<rect x="' + x + '" y="' + y + '" width="100" height="100" rx="2"/>').join('');
  const labels = state.labels.map(({copy, opacity}) =>
    '<text x="48" y="304" opacity="' + opacity + '">' + escape(copy) + '</text>').join('');
  return '<svg xmlns="http://www.w3.org/2000/svg" width="' + width + '" height="' + height +
    '" viewBox="0 0 ' + width + ' ' + height + '">' +
    '<rect width="' + width + '" height="' + height + '" fill="' + escape(colors.background) + '"/>' +
    '<path d="M 150 154 H ' + number(150 + 340 * state.connection) +
    '" stroke="' + escape(colors.accent) + '" stroke-width="8"/>' +
    '<g fill="' + escape(colors.ink) + '">' + blocks + '</g>' +
    '<rect x="86" y="90" width="468" height="128" rx="4" fill="none" stroke="' +
    escape(colors.accent) + '" stroke-width="3" opacity="' + state.outline + '"/>' +
    '<g fill="' + escape(colors.ink) + '" font-family="' + escape(font) +
    '" font-size="38" font-weight="700">' + labels + '</g></svg>';
}
