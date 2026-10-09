// Visible-text audit, run inside a page by text-audit.mjs and review-frames.mjs. It finds EVERY visible text
// node under the composition root (copy, labels, decoration), measures each word's glyph boxes after
// transforms, and intersects them with the frame and every clipping ancestor (overflow hidden/clip/scroll/
// auto on either axis, clip-path inset). A word that is partly visible, or a word or line that is hidden while
// other words of the same element show, is reported. Audit flags such as data-layout-ignore never exempt
// visible text; only data-text-clip-ok="<reason>" on the element itself records a narrow, reviewed exception.
// The result is plain JSON; whether a finding blocks delivery depends on whether the sample is a readable hold,
// which the caller decides.
(function () {
  const IGNORE_FLAGS = ['data-layout-ignore', 'data-layout-allow-overflow', 'data-layout-allow-occlusion', 'data-layout-allow-overlap'];
  const MIN_REASON = 12;
  const round = value => Math.round(value * 10) / 10;
  const clips = value => ['hidden', 'clip', 'scroll', 'auto'].includes(value);

  function opacityOf(element, root) {
    let opacity = 1;
    for (let node = element; node; node = node.parentElement) {
      opacity *= Number(getComputedStyle(node).opacity);
      if (node === root) break;
    }
    return opacity;
  }

  function insetClip(element, style) {
    // clip-path: inset(top right bottom left) in px or %; other shapes cannot be measured from geometry.
    const value = style.clipPath;
    if (!value || value === 'none') return null;
    const match = value.match(/^inset\(([^)]*)\)/);
    const box = element.getBoundingClientRect();
    if (!match) return {left: box.left, top: box.top, right: box.right, bottom: box.bottom, unmeasured: value};
    const parts = match[1].split(/\s+round\s+/)[0].trim().split(/\s+/);
    // CSS shorthand: one value for all sides, two for vertical/horizontal, three for top/horizontal/bottom.
    const [t, r = t, b = t, l = r] = parts;
    const length = (token, size) => token.endsWith('%') ? parseFloat(token) / 100 * size : parseFloat(token) || 0;
    return {left: box.left + length(l, box.width), top: box.top + length(t, box.height),
      right: box.right - length(r, box.width), bottom: box.bottom - length(b, box.height)};
  }

  function clipRect(element, root, frame) {
    // The visible region for the element's content: the frame, narrowed by every clipping ancestor up to the root.
    let rect = {...frame};
    const notes = [];
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node), box = node.getBoundingClientRect();
      const x = clips(style.overflowX), y = clips(style.overflowY);
      if (x) { rect.left = Math.max(rect.left, box.left); rect.right = Math.min(rect.right, box.right); }
      if (y) { rect.top = Math.max(rect.top, box.top); rect.bottom = Math.min(rect.bottom, box.bottom); }
      const inset = insetClip(node, style);
      if (inset) {
        rect = {left: Math.max(rect.left, inset.left), top: Math.max(rect.top, inset.top), right: Math.min(rect.right, inset.right), bottom: Math.min(rect.bottom, inset.bottom)};
        if (inset.unmeasured) notes.push('clip-path ' + inset.unmeasured);
      }
      const mask = style.maskImage || style.webkitMaskImage;
      if (mask && mask !== 'none') notes.push('mask ' + mask.slice(0, 60));
      if (node === root) break;
    }
    return {rect, notes};
  }

  function visibleFraction(box, rect) {
    const w = Math.max(0, Math.min(box.right, rect.right) - Math.max(box.left, rect.left));
    const h = Math.max(0, Math.min(box.bottom, rect.bottom) - Math.max(box.top, rect.top));
    const area = Math.max(1e-6, (box.right - box.left) * (box.bottom - box.top));
    return (w * h) / area;
  }

  function wordsOf(node) {
    const out = [], pattern = /\S+/g, text = node.data;
    let match;
    while ((match = pattern.exec(text))) {
      const range = document.createRange();
      range.setStart(node, match.index);
      range.setEnd(node, match.index + match[0].length);
      const rects = [...range.getClientRects()].filter(q => q.width > 0 && q.height > 0);
      if (rects.length) out.push({word: match[0], rects});
    }
    return out;
  }

  function fontState(style) {
    const family = style.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
    const faces = [...document.fonts].filter(face => face.family.replace(/^["']|["']$/g, '') === family);
    if (!faces.length) return {family, state: 'system'};
    if (faces.some(face => face.status === 'loaded')) return {family, state: 'loaded'};
    return {family, state: faces.some(face => face.status === 'error') ? 'error' : 'not_loaded'};
  }

  window.__studioTextAudit = function (options = {}) {
    const root = (options.root && document.querySelector(options.root)) || document.querySelector('[data-composition-id]') || document.body;
    const rootBox = root.getBoundingClientRect();
    const width = options.width || Number(root.getAttribute('data-width')) || rootBox.width;
    const height = options.height || Number(root.getAttribute('data-height')) || rootBox.height;
    // The frame is the composition's own canvas: the root's box, or the requested size from its top-left corner.
    const scale = rootBox.width && width ? rootBox.width / width : 1;
    const frame = {left: rootBox.left, top: rootBox.top, right: rootBox.left + width * scale, bottom: rootBox.top + height * scale};
    const texts = [], issues = [], exceptions = [];
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: n => n.data.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT});
    const byElement = new Map();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const element = node.parentElement;
      if (!element || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'TITLE'].includes(element.tagName)) continue;
      const style = getComputedStyle(element);
      if (style.visibility !== 'visible' || style.display === 'none') continue;
      const colour = (style.webkitTextFillColor && style.webkitTextFillColor !== style.color ? style.webkitTextFillColor : style.color).match(/[\d.]+/g) || [];
      if (colour.length >= 4 && Number(colour[3]) === 0 && !(style.webkitTextStrokeWidth && parseFloat(style.webkitTextStrokeWidth) > 0)) continue;
      const opacity = opacityOf(element, root);
      if (opacity < 0.02) continue;
      const words = wordsOf(node);
      if (!words.length) continue;
      if (!byElement.has(element)) byElement.set(element, {style, opacity, words: []});
      byElement.get(element).words.push(...words);
    }
    let index = 0;
    for (const [element, {style, opacity, words}] of byElement) {
      const {rect, notes} = clipRect(element, root, frame);
      const key = element.id ? '#' + element.id : element.className && typeof element.className === 'string' ? element.tagName.toLowerCase() + '.' + element.className.trim().split(/\s+/).join('.') : element.tagName.toLowerCase() + ':' + index;
      index += 1;
      // A glyph box spans the font's whole ascent and descent; with a tight line-height that box is taller than the
      // line, and the part beyond the line box is empty space, not ink. Only that excess is tolerated vertically.
      const lineHeight = parseFloat(style.lineHeight);
      const trim = r => {
        const excess = Number.isFinite(lineHeight) ? Math.max(0, (r.height - lineHeight) / 2) : 0;
        return {left: r.left, right: r.right, width: r.width, top: r.top + excess, bottom: r.bottom - excess};
      };
      const measured = words.map(({word, rects: raw}) => {
        const rects = raw.map(trim);
        const fractions = rects.map(r => visibleFraction(r, rect));
        const fraction = fractions.reduce((sum, f, i) => sum + f * rects[i].width, 0) / rects.reduce((sum, r) => sum + r.width, 0);
        return {word, fraction, box: {left: round(Math.min(...rects.map(r => r.left)) - frame.left), top: round(Math.min(...rects.map(r => r.top)) - frame.top),
          right: round(Math.max(...rects.map(r => r.right)) - frame.left), bottom: round(Math.max(...rects.map(r => r.bottom)) - frame.top)}};
      });
      const text = words.map(w => w.word).join(' ');
      const shown = measured.filter(w => w.fraction > 0.02);
      const cut = measured.filter(w => w.fraction > 0.02 && w.fraction < 0.98);
      const hidden = measured.filter(w => w.fraction <= 0.02);
      const font = fontState(style);
      const flags = IGNORE_FLAGS.filter(flag => element.closest('[' + flag + ']'));
      const exception = element.getAttribute('data-text-clip-ok');
      const entry = {key, text, fontSize: parseFloat(style.fontSize), opacity: round(opacity), font, flags,
        visible: shown.length ? (cut.length || hidden.length ? 'partial' : 'complete') : 'hidden',
        cutWords: cut.map(w => ({word: w.word, visible: round(w.fraction * 100) + '%', box: w.box})), hiddenWords: shown.length ? hidden.map(w => w.word) : [],
        box: shown.length ? {left: Math.min(...shown.map(w => w.box.left)), top: Math.min(...shown.map(w => w.box.top)), right: Math.max(...shown.map(w => w.box.right)), bottom: Math.max(...shown.map(w => w.box.bottom))} : null,
        clipNotes: notes};
      texts.push(entry);
      if (!shown.length) continue;
      const add = (severity, check, detail) => issues.push({severity, check, element: key, text, detail});
      if (entry.visible === 'partial') {
        const detail = (cut.length ? 'cut: ' + cut.map(w => `${w.word} (${round(w.fraction * 100)}% visible)`).join(', ') : '') +
          (hidden.length ? (cut.length ? '; ' : '') + 'not visible: ' + hidden.map(w => w.word).join(' ') : '');
        if (exception && exception.trim().length >= MIN_REASON) exceptions.push({element: key, text, reason: exception.trim(), detail, review: 'pixel review required'});
        else add('error', hidden.length && !cut.length ? 'text-hidden' : 'text-cut', detail + (exception ? ' (data-text-clip-ok needs a reason of at least ' + MIN_REASON + ' characters)' : ''));
      }
      if (flags.length) add('warning', 'ignore-flag', flags.join(', ') + ' hides this visible text from other layout audits; Studio audits it anyway');
      if (font.state === 'not_loaded' || font.state === 'error') add('error', 'font-not-loaded', `font ${font.family} is ${font.state.replace('_', ' ')}`);
      if (notes.length) add('note', 'unmeasured-clip', notes.join('; ') + ': inspect the pixels');
    }
    return {width, height, fontsStatus: document.fonts.status, texts, issues, exceptions};
  };
})();
