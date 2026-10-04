// Original synthetic fixture: time selects state; playback never accumulates it.
export const config = Object.freeze({width: 640, height: 360, fps: 30, totalFrames: 180});
export const colors = Object.freeze({paper: '#f3eee2', ink: '#182023', accent: '#b83a24'});
export const data = Object.freeze([
  Object.freeze({label: 'A', start: 24, end: 68}),
  Object.freeze({label: 'B', start: 52, end: 34}),
  Object.freeze({label: 'C', start: 38, end: 82}),
]);
export function assertFrame(frame) {
  if (!Number.isInteger(frame) || frame < 0 || frame >= config.totalFrames) {
    throw new RangeError('Frame must be an integer in [0, 180).');
  }
  return frame;
}
const clamp = value => Math.max(0, Math.min(1, value));
const smooth = value => {const t = clamp(value); return t * t * (3 - 2 * t);};
export function stateAtFrame(frame) {
  assertFrame(frame);
  const t = smooth((frame - 24) / 108);
  return {
    frame, progress: t, seconds: frame / config.fps,
    values: data.map(row => row.start + (row.end - row.start) * t),
    particles: Array.from({length: 48}, (_, i) => {
      const angle = i / 48 * Math.PI * 2 + t * Math.PI;
      const radius = 26 + (i % 8) * 10;
      return {x: 80 + i % 12 * 43 + t * (320 + Math.cos(angle) * radius - (80 + i % 12 * 43)),
        y: 128 + Math.floor(i / 12) * 38 + t * (198 + Math.sin(angle) * radius - (128 + Math.floor(i / 12) * 38)),
        rotation: t * (i % 4) * Math.PI / 2, size: 5 + i % 3};
    }),
  };
}
export function assetFrameAt(frame, {fps, start, end}) {
  assertFrame(frame);
  if (!Number.isFinite(fps) || fps <= 0 || !Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end <= start) {
    throw new RangeError('Asset needs positive FPS and a valid [start,end) frame range.');
  }
  return Math.min(end - 1, start + Math.floor(frame * fps / config.fps));
}
