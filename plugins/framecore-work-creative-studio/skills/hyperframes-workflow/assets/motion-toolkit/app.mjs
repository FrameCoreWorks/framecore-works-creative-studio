import {config} from './timeline.mjs';
import {createRenderer} from './renderers.mjs';
import {exportVideo, inspectVideo, InspectionMismatch} from './export.mjs';
const canvas = document.querySelector('canvas');
const select = document.querySelector('#scene');
const slider = document.querySelector('#frame');
const status = document.querySelector('#status');
const play = document.querySelector('#play');
const links = document.querySelector('#downloads');
let renderer, playing = false, frame = 0, previousTime, accumulator = 0, busy = false, cancellation;
const urls = [];
function report(message) {status.textContent = message;}
function stop() {playing = false; play.textContent = 'Play'; previousTime = undefined; accumulator = 0;}
function render(value) {
  frame = value; renderer.renderFrame(frame); slider.value = frame;
  document.querySelector('#frame-label').textContent = 'Frame ' + frame + ' / ' + (config.totalFrames - 1);
}
function lock(value) {
  busy = value;
  for (const element of document.querySelectorAll('button, select, input')) element.disabled = value;
  document.querySelector('#cancel').disabled = !value || !cancellation;
}
async function loadScene() {
  stop(); lock(true);
  try {renderer?.destroy(); renderer = undefined; renderer = await createRenderer(select.value, canvas); render(0); report('Ready. Preview and export share the same frame renderer.');}
  catch (error) {report('Unavailable: ' + error.message);}
  finally {lock(false); if (!renderer) for (const control of document.querySelectorAll('button, #frame')) control.disabled = true;}
}
async function runSeekCheck() {
  stop(); lock(true);
  try {
    const ctx = canvas.getContext('2d');
    const signature = async f => {render(f); return new Uint8Array(await crypto.subtle.digest('SHA-256', ctx.getImageData(0, 0, config.width, config.height).data));};
    const same = (a, b) => a.every((value, i) => value === b[i]);
    const probes = [0, 24, 81, 132, 179];
    const direct = new Map();
    for (const f of probes) direct.set(f, await signature(f));
    for (let f = 0; f < config.totalFrames; f++) {
      render(f);
      if (direct.has(f) && !same(direct.get(f), await signature(f))) throw new Error('Forward/direct mismatch at ' + f);
    }
    for (const f of [...probes].reverse()) if (!same(direct.get(f), await signature(f))) throw new Error('Backward/direct mismatch at ' + f);
    if (same(direct.get(0), direct.get(81))) throw new Error('Expected motion was not observed.');
    render(179); report('PASS: direct, forward and backward pixels match at frames ' + probes.join(', ') + '. Motion detected. This is a local pixel check, not creative QA.');
  } catch (error) {report('FAIL: ' + error.message);}
  finally {lock(false);}
}
select.addEventListener('change', loadScene);
slider.addEventListener('input', () => {stop(); render(Number(slider.value));});
play.addEventListener('click', () => {if (playing) stop(); else {if (frame === config.totalFrames - 1) render(0); playing = true; play.textContent = 'Pause';}});
document.querySelector('#replay').addEventListener('click', () => {stop(); render(0); playing = true; play.textContent = 'Pause';});
document.querySelector('#check').addEventListener('click', runSeekCheck);
document.querySelector('#cancel').addEventListener('click', () => cancellation?.abort());
document.querySelector('#export').addEventListener('click', async () => {
  stop(); cancellation = new AbortController(); lock(true);
  const kind = select.value, format = document.querySelector('#format').value;
  try {
    const blob = await exportVideo(canvas, renderer, format, (n, total) => report('Encoding ' + n + ' / ' + total), cancellation.signal);
    document.querySelector('#cancel').disabled = true;
    const url = URL.createObjectURL(blob); urls.push(url);
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'motion-' + kind + '.' + format;
    anchor.textContent = 'Download ' + kind + ' ' + format.toUpperCase() + ' (' + blob.size + ' bytes)'; links.append(anchor);
    const video = document.createElement('video'); video.src = url; video.controls = true; video.preload = 'metadata';
    video.width = config.width; video.style.maxWidth = '100%'; video.setAttribute('aria-label', 'Encoded ' + kind + ' ' + format + ' preview');
    links.append(video);
    report('Encoded. Inspecting finalized video bytes...');
    try {
      const check = await inspectVideo(blob, cancellation.signal);
      report('Decoded PASS: ' + check.frames + ' frames, ' + check.width + ' × ' + check.height + ', ' + check.fps + ' FPS timestamps, ' + check.duration.toFixed(3) + ' seconds, ' + check.codec + ', no audio. Watch the encoded preview before accepting it.');
    } catch (error) {report(error instanceof InspectionMismatch ? 'Decoded FAIL: ' + error.message : 'Encoded; decoded inspection NOT VERIFIED: ' + error.message + ' Use an available local media inspector.');}
  } catch (error) {report('Export not completed: ' + error.message);}
  finally {cancellation = undefined; lock(false); render(frame);}
});
function tick(now) {
  if (playing && !busy && renderer) {
    if (previousTime !== undefined) accumulator += now - previousTime;
    previousTime = now;
    const steps = Math.floor(accumulator / (1000 / config.fps));
    if (steps) {accumulator -= steps * (1000 / config.fps); render(Math.min(config.totalFrames - 1, frame + steps)); if (frame === config.totalFrames - 1) stop();}
  }
  requestAnimationFrame(tick);
}
window.addEventListener('pagehide', () => {cancellation?.abort(); stop(); renderer?.destroy(); urls.forEach(url => URL.revokeObjectURL(url));});
await loadScene(); requestAnimationFrame(tick);
