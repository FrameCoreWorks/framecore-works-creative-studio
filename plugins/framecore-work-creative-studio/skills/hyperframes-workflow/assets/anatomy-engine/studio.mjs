#!/usr/bin/env node
// A local workspace initializer and three executable integration fixtures.
// Production scenes import the complete kit; these fixtures are not creative templates.
import { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as iso from './kit/iso-kit.mjs';
import { turning } from './kit/turn-build.mjs';
import { glCamera } from './kit/gl.mjs';
import { glScript, turnScript } from './scripts/inline-kit.mjs';
import { createFrameBridge } from './frame-bridge.mjs';

const ROOT = dirname(fileURLToPath(import.meta.url));
const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const json = value => JSON.stringify(value).replace(/</g, '\\u003c');

export function checkNode(version = process.versions.node) {
  const [major, minor] = version.split('.').map(Number);
  if (!(major > 20 || (major === 20 && minor >= 10))) throw new Error('Anatomy needs Node.js >=20.10; browser helpers also need built-in WebSocket support');
}

export function buildPage({ mode = 'svg', width = 640, height = 480, fps = 30, seconds = 4, title = 'Anatomy integration fixture' } = {}) {
  if (!['svg', 'webgl', '3d'].includes(mode)) throw new Error('Mode must be svg, webgl or 3d');
  for (const n of [width, height]) if (!Number.isInteger(n) || n < 64 || n > 8192) throw new Error('Size must be an integer from 64 to 8192');
  createFrameBridge({ fps, seconds, draw() {} });
  const P = iso.fitProjection(iso.boxCorners({ x: -70, y: -70, w: 140, d: 140 }, -5, 70), width, height, { pad: 36, azimuth: 40, elevation: 30 });
  const body = iso.solidSvg(iso.slabOf({ x: -55, y: -40, w: 110, d: 80, r: 6 }, 0, 10, P), { tone: 'mid' });
  const surface = iso.figureSvg({ width, height, label: 'Isometric test geometry', body: [body] });
  let markup = surface, script = '', css = '';
  if (mode === 'svg') {
    const marker = `<circle id="marker" cx="${width / 2}" cy="${height / 2}" r="10" fill="#cb4e2f"/>`;
    markup = surface.replace('</svg>', marker + '</svg>');
    script = `const update = s => document.querySelector('#marker').setAttribute('cx', ${width} * (0.25 + 0.5 * s.progress));`;
  } else if (mode === 'webgl') {
    markup += '<canvas id="shader" aria-label="Procedural shader layer"></canvas><p id="fallback" role="status">SVG fallback: WebGL is unavailable.</p>';
    script = glScript() + `
      let layer = null;
      const canvas = document.querySelector('#shader');
      const fallback = document.querySelector('#fallback');
      const initGL = () => {
        layer = glLayer({ canvas, view: [${width}, ${height}], camera: ${json(glCamera(P))}, maxRatio: 1,
          fragment: 'void main(){vec2 p=gl_FragCoord.xy/uCanvas;float ring=1.-smoothstep(.015,.025,abs(length(p-vec2(.5))-(.15+.05*sin(uTime*2.))));gl_FragColor=vec4(.08,.42,.68,1.)*ring;}',
          onError: message => { window.__studioAnatomy.error = message; }
        });
        window.__studioAnatomy.webgl = Boolean(layer);
        fallback.hidden = Boolean(layer);
      };
      initGL();
      canvas.addEventListener('webglcontextlost', event => { event.preventDefault(); layer = null; fallback.hidden = false; window.__studioAnatomy.webgl = false; });
      canvas.addEventListener('webglcontextrestored', () => { initGL(); window.renderFrame(window.__studioAnatomy.time || 0); });
      const update = s => { if (layer) layer.draw({}, s.time); };
    `;
  } else {
    const T = turning(P);
    const group = T.group('rotor', { turn: { pivot: [0, 0] } });
    const layer = T.layer('parts');
    T.prism({ name: 'bar', group, layer, plan: { x: -45, y: -10, w: 90, d: 20, r: 2 }, z: 14, h: 24, material: 'steel' });
    const out = T.build({ verify: true, poses: () => [0, 45, 90, 180, 270, 360].map(rotor => ({ rotor })) });
    markup = surface + out.layerSvg('parts', { width, height });
    css = out.css;
    script = turnScript() + `
      window.__isoVerify = ${json(out.verify)};
      const controller = TURN.mount(document.querySelector('#stage'), ${json(out.data)});
      const update = s => controller.set({ rotor: s.time * 60 });
      window.__studioAnatomy.controller = controller;
    `;
  }
  const count = Math.round(fps * seconds);
  const runtime = `window.__studioAnatomy = { mode: ${json(mode)}, ready: false };\n` + script + `
    const bridge = (${createFrameBridge.toString()})({ fps: ${fps}, seconds: ${seconds}, target: window, draw: s => {
      update(s);
      document.querySelector('#scrub').value = s.frame;
      document.querySelector('#readout').textContent = s.time.toFixed(3) + ' s · frame ' + s.frame;
      window.__studioAnatomy.time = s.time;
      window.__studioAnatomy.frame = s.frame;
    }});
    document.querySelector('#scrub').addEventListener('input', e => bridge.renderIndex(Number(e.target.value)));
    window.addEventListener('resize', () => bridge.renderIndex(bridge.state.frame));
    window.__studioAnatomy.ready = true;
  `;
  const style = readFileSync(resolve(ROOT, 'kit/iso.css'), 'utf8');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><style>${style}\n${css}
    body{margin:0;background:#eef1ed;color:#252c2a;font-family:system-ui,sans-serif}main{max-width:${width}px;margin:auto}h1{font-size:18px;padding:0 16px}#stage{position:relative;aspect-ratio:${width}/${height};width:100%;overflow:hidden}#stage>svg,#shader{position:absolute;inset:0;width:100%;height:100%;margin:0}#fallback{position:absolute;bottom:0;left:16px;right:16px;font-size:13px}label,output{display:block;padding:8px 16px}input{width:100%}input:focus-visible{outline:3px solid #1767b2;outline-offset:4px}
    body[data-export] h1,body[data-export] label,body[data-export] output{display:none}body[data-export] main{max-width:none}body[data-export] #stage{width:100vw;height:100vh}
  </style></head><body class="iso" data-theme="light"><main><h1>${escapeHtml(title)}</h1><div id="stage" class="iso-stage" role="img" aria-label="${escapeHtml(title)}">${markup}</div><label>Frame<input id="scrub" type="range" min="0" max="${count - 1}" value="0" step="1"></label><output id="readout" for="scrub"></output></main><script>if(new URLSearchParams(location.search).has('export'))document.body.dataset.export='';\n${runtime}</script></body></html>`;
}

export function main(argv = process.argv.slice(2)) {
  checkNode();
  const [command, ...args] = argv;
  if (!command || command === '--help') {
    console.log('node studio.mjs init NEW_DIRECTORY\nnode studio.mjs build --mode svg|webgl|3d --out NEW.html [--width 640 --height 480 --fps 30 --seconds 4]\nnode studio.mjs preflight');
    return;
  }
  if (command === 'preflight') {
    console.log(JSON.stringify({ node: process.versions.node, source: true, browser: 'not_probed', webgl: 'not_probed', react: 'requires_existing_React_project', export: 'requires_Chrome_and_FFmpeg' }));
    return;
  }
  if (command === 'init') {
    if (args.length !== 1) throw new Error('init requires one new workspace directory');
    const dest = resolve(args[0]);
    const inside = relative(ROOT, dest);
    if (!inside || (!isAbsolute(inside) && inside !== '..' && !inside.startsWith('..' + sep))) throw new Error('Choose a destination outside the installed engine');
    if (existsSync(dest)) throw new Error('Destination already exists; no files overwritten');
    cpSync(ROOT, dest, { recursive: true, errorOnExist: true, force: false });
    console.log(dest);
    return;
  }
  if (command !== 'build') throw new Error('Unknown command');
  const options = {};
  const keys = new Set(['mode', 'out', 'width', 'height', 'fps', 'seconds']);
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    if (!args[i].startsWith('--') || !keys.has(key) || args[i + 1] === undefined || key in options) throw new Error('Invalid or duplicate option: ' + args[i]);
    options[key] = ['width', 'height', 'fps', 'seconds'].includes(key) ? Number(args[i + 1]) : args[i + 1];
  }
  if (!options.out) throw new Error('--out is required');
  const output = resolve(options.out);
  const page = buildPage(options);
  mkdirSync(dirname(output), { recursive: true });
  writeFileSync(output, page, { flag: 'wx' });
  console.log(output);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(); } catch (error) { console.error(error.message); process.exitCode = 1; }
}
