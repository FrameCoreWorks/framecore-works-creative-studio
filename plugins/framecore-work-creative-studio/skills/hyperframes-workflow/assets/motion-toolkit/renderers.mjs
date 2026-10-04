// Pixi's official CSP-safe polyfills replace generated eval functions.
import 'pixi.js/unsafe-eval';
import {scaleBand, scaleLinear} from 'd3-scale';
import {Application, Graphics, BlurFilter} from 'pixi.js';
import lottie from 'lottie-web/build/player/lottie_canvas.js';
import {config, colors, data, stateAtFrame, assetFrameAt} from './timeline.mjs';
import {animationData} from './lottie-fixture.mjs';

function background(ctx, title, subtitle) {
  ctx.fillStyle = colors.paper; ctx.fillRect(0, 0, config.width, config.height);
  ctx.fillStyle = colors.ink; ctx.font = '700 28px Arial, sans-serif';
  ctx.fillText(title, 36, 52);
  ctx.font = '14px Arial, sans-serif'; ctx.fillText(subtitle, 36, 78);
}

export async function createRenderer(kind, canvas) {
  canvas.width = config.width; canvas.height = config.height;
  const ctx = canvas.getContext('2d', {willReadFrequently: true});
  if (!ctx) throw new Error('Canvas 2D is unavailable.');
  await document.fonts.ready;
  if (kind === 'data') {
    const x = scaleBand().domain(data.map(row => row.label)).range([76, 580]).padding(0.28);
    const y = scaleLinear().domain([0, 100]).range([300, 112]);
    return {renderFrame(frame) {
      const state = stateAtFrame(frame);
      background(ctx, 'DATA IN MOTION', 'Fixed scale. Exact data. One frame clock.');
      ctx.lineWidth = 1;
      for (const value of [0, 25, 50, 75, 100]) {
        ctx.strokeStyle = '#d4cec2'; ctx.beginPath(); ctx.moveTo(66, y(value)); ctx.lineTo(590, y(value)); ctx.stroke();
        ctx.fillStyle = colors.ink; ctx.font = '11px Arial, sans-serif'; ctx.fillText(String(value), 36, y(value) + 4);
      }
      state.values.forEach((value, i) => {
        ctx.fillStyle = i === 2 ? colors.accent : colors.ink;
        ctx.fillRect(x(data[i].label), y(value), x.bandwidth(), 300 - y(value));
        ctx.textAlign = 'center'; ctx.font = '700 18px Arial, sans-serif';
        ctx.fillText(value.toFixed(1), x(data[i].label) + x.bandwidth() / 2, y(value) - 10);
        ctx.font = '14px Arial, sans-serif'; ctx.fillText(data[i].label, x(data[i].label) + x.bandwidth() / 2, 326);
        ctx.textAlign = 'left';
      });
    }, destroy() {}};
  }
  if (kind === 'particles') {
    const app = new Application();
    await app.init({width: config.width, height: config.height, autoStart: false, sharedTicker: false,
      backgroundAlpha: 0, antialias: true, resolution: 1, preference: 'webgl', preserveDrawingBuffer: true});
    app.stop();
    const ring = new Graphics().circle(320, 198, 108).stroke({width: 2, color: 0xb83a24, alpha: 0.2});
    app.stage.addChild(ring);
    const halo = new Graphics().circle(320, 198, 40).fill({color: 0xb83a24, alpha: 0.18});
    halo.filters = [new BlurFilter({strength: 12, quality: 3})]; app.stage.addChild(halo);
    const particles = stateAtFrame(0).particles.map((p, i) => {
      const shape = new Graphics().rect(-p.size, -p.size, p.size * 2, p.size * 2).fill(i % 5 === 0 ? 0xb83a24 : 0x182023);
      app.stage.addChild(shape); return shape;
    });
    return {renderFrame(frame) {
      const state = stateAtFrame(frame);
      state.particles.forEach((p, i) => {particles[i].position.set(p.x, p.y); particles[i].rotation = p.rotation;});
      ring.alpha = state.progress; halo.alpha = state.progress; app.render();
      background(ctx, 'ORDER FROM MOTION', '48 particles. One repeatable transformation.');
      ctx.drawImage(app.canvas, 0, 0);
    }, destroy() {app.destroy(true, {children: true, texture: true, textureSource: true});}};
  }
  if (kind === 'lottie') {
    const layer = document.createElement('canvas'); layer.width = config.width; layer.height = config.height;
    const animation = lottie.loadAnimation({renderer: 'canvas', autoplay: false, loop: false,
      animationData: structuredClone(animationData), rendererSettings: {context: layer.getContext('2d'), clearCanvas: true}});
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('Lottie asset did not become ready.')), 10000);
      animation.addEventListener('DOMLoaded', () => {clearTimeout(timeout); resolve();});
      animation.addEventListener('data_failed', () => {clearTimeout(timeout); reject(new Error('Invalid Lottie data.'));});
      if (animation.isLoaded) {clearTimeout(timeout); resolve();}
    });
    return {renderFrame(frame) {
      const sourceFrame = assetFrameAt(frame, {fps: animationData.fr, start: animationData.ip, end: animationData.op});
      animation.goToAndStop(sourceFrame - animationData.ip, true);
      background(ctx, 'VECTOR REUSE', 'Original Lottie JSON. Explicit frame selection.');
      ctx.drawImage(layer, 0, 0);
    }, destroy() {animation.destroy();}};
  }
  throw new Error('Unknown renderer: ' + kind);
}
