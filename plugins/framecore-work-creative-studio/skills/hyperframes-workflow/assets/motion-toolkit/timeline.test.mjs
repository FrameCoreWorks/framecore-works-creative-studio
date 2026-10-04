import test from 'node:test';
import assert from 'node:assert/strict';
import {config, data, stateAtFrame, assetFrameAt} from './timeline.mjs';

test('one 180-frame timeline contains exact opening and closing data with a final hold', () => {
  assert.equal(config.totalFrames / config.fps, 6);
  assert.deepEqual(stateAtFrame(0).values, data.map(row => row.start));
  assert.deepEqual(stateAtFrame(179).values, data.map(row => row.end));
  assert.deepEqual(stateAtFrame(150).particles, stateAtFrame(179).particles);
});
test('backward/direct/replayed state does not depend on history', () => {
  const original = stateAtFrame(81);
  for (const frame of [0, 179, 20, 150, 81]) stateAtFrame(frame);
  assert.deepEqual(stateAtFrame(81), original);
  assert.notEqual(stateAtFrame(0).progress, stateAtFrame(90).progress);
});
test('all frames are finite and reject invalid and endpoint indices', () => {
  for (let f = 0; f < config.totalFrames; f++) {
    const s = stateAtFrame(f);
    assert.ok(s.values.every(Number.isFinite));
    assert.ok(s.particles.every(p => [p.x, p.y, p.rotation, p.size].every(Number.isFinite)));
  }
  for (const f of [-1, 180, 0.5, NaN, Infinity, '0']) assert.throws(() => stateAtFrame(f), RangeError);
});
test('asset rates are mapped separately, with an exclusive end and no implicit loop', () => {
  assert.equal(assetFrameAt(30, {fps: 24, start: 10, end: 100}), 34);
  assert.equal(assetFrameAt(179, {fps: 60, start: 0, end: 120}), 119);
  for (const fps of [0, -1, NaN]) assert.throws(() => assetFrameAt(0, {fps, start: 0, end: 120}));
});
