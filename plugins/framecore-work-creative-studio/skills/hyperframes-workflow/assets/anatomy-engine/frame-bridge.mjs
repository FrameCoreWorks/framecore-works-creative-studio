// Studio adapter: the same explicit frame drives SVG, WebGL and TURN.
export function createFrameBridge({ fps = 30, seconds = 4, draw, target = null }) {
  if (!Number.isFinite(fps) || fps <= 0 || !Number.isFinite(seconds) || seconds <= 0 || typeof draw !== 'function') {
    throw new TypeError('Positive finite fps and seconds and a draw function are required');
  }
  const count = Math.round(fps * seconds);
  if (!Number.isSafeInteger(count) || count < 1) throw new RangeError('Invalid frame count');
  let state;
  function renderIndex(index) {
    if (!Number.isInteger(index)) throw new TypeError('Frame index must be an integer');
    const frame = Math.max(0, Math.min(count - 1, index));
    const next = Object.freeze({ frame, time: frame / fps, progress: count > 1 ? frame / (count - 1) : 0, fps, count });
    draw(next);
    state = next;
    return state;
  }
  function renderFrame(time) {
    if (!Number.isFinite(time)) throw new TypeError('Time must be finite seconds');
    return renderIndex(Math.round(time * fps));
  }
  const api = { renderFrame, renderIndex, get state() { return state; } };
  if (target) target.renderFrame = renderFrame;
  renderIndex(0);
  return api;
}
