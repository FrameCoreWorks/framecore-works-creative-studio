// Browser video export for the motion contract. Each frame of the preview stage is drawn into a canvas
// through an SVG foreignObject image, encoded with WebCodecs and written as MP4 (H.264) when the browser
// can encode it, otherwise WebM (VP9 or VP8). Video only. Dependency-free: the muxers are pure functions
// that also run in Node. The single-file preview embeds this file; keep copies identical.

/** Candidate encodings in order of preference; isConfigSupported() decides what the browser offers. */
export const videoCandidates = [
  {container: 'mp4', codec: 'avc1.640028', mime: 'video/mp4', extension: 'mp4', maxMacroblocks: 8192},
  {container: 'mp4', codec: 'avc1.4d0028', mime: 'video/mp4', extension: 'mp4', maxMacroblocks: 8192},
  {container: 'mp4', codec: 'avc1.640033', mime: 'video/mp4', extension: 'mp4', maxMacroblocks: 36864},
  {container: 'webm', codec: 'vp09.00.40.08', mime: 'video/webm', extension: 'webm'},
  {container: 'webm', codec: 'vp8', mime: 'video/webm', extension: 'webm'},
];

const rate = fps => fps.num / fps.den;
const macroblocks = (width, height) => Math.ceil(width / 16) * Math.ceil(height / 16);

/** The first supported encoding, preferring `container` ('mp4' or 'webm') when given; null when none. */
export async function chooseVideoEncoding(width, height, fps, {container} = {}) {
  if (typeof VideoEncoder === 'undefined') return null;
  const ordered = [...videoCandidates].sort((a, b) => (b.container === container) - (a.container === container));
  for (const candidate of ordered) {
    if (candidate.maxMacroblocks && macroblocks(width, height) > candidate.maxMacroblocks) continue;
    const config = {codec: candidate.codec, width, height, framerate: rate(fps),
      bitrate: Math.round(8e6 * (width * height) / (1920 * 1080) * Math.min(rate(fps), 60) / 30),
      ...(candidate.container === 'mp4' ? {avc: {format: 'avc'}} : {})};
    try { if ((await VideoEncoder.isConfigSupported(config)).supported) return {...candidate, config}; } catch { /* try the next one */ }
  }
  return null;
}

/** Draw the stage element at its true size into a 2D context, through an SVG foreignObject image. */
export async function drawStage(stage, score, context) {
  const clone = stage.cloneNode(true);
  Object.assign(clone.style, {position: 'relative', left: '0', top: '0', transform: 'none'});
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${score.width}" height="${score.height}"><foreignObject x="0" y="0" width="${score.width}" height="${score.height}">${new XMLSerializer().serializeToString(clone)}</foreignObject></svg>`;
  const image = new Image();
  image.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  await image.decode();
  context.fillStyle = score.tokens?.background ?? '#000';
  context.fillRect(0, 0, score.width, score.height);
  context.drawImage(image, 0, 0);
}

const bytesOf = data => (ArrayBuffer.isView(data) ? new Uint8Array(data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength)) : new Uint8Array(data.slice(0)));

/** Render every frame through seekFrame(), encode and mux. Returns {blob, bytes, container, codec, extension, frames, ms}. */
export async function exportVideo({stage, score, seekFrame, container, onProgress = () => {}}) {
  const encoding = await chooseVideoEncoding(score.width, score.height, score.fps, {container});
  if (!encoding) throw new Error('This browser cannot encode video here (WebCodecs is missing or offers no suitable codec). Use a current Chrome or Edge, or render with the Remotion starter.');
  const canvas = document.createElement('canvas');
  canvas.width = score.width; canvas.height = score.height;
  const context = canvas.getContext('2d');
  const chunks = [], started = performance.now(), keyEvery = Math.max(1, Math.round(rate(score.fps) * 2));
  let description = null, failure = null;
  const encoder = new VideoEncoder({
    output: (chunk, metadata) => {
      const data = new Uint8Array(chunk.byteLength); chunk.copyTo(data);
      chunks.push({timestamp: chunk.timestamp, key: chunk.type === 'key', data});
      if (metadata?.decoderConfig?.description) description = bytesOf(metadata.decoderConfig.description);
    },
    error: error => { failure = error; },
  });
  encoder.configure(encoding.config);
  try {
    for (let frame = 0; frame < score.totalFrames; frame++) {
      seekFrame(frame);
      await drawStage(stage, score, context);
      if (frame === 0) {
        try { context.getImageData(0, 0, 1, 1); } catch { throw new Error('This browser does not allow reading the drawn frames back (the canvas is tainted). Use a current Chrome or Edge, or render with the Remotion starter.'); }
      }
      const image = new VideoFrame(canvas, {timestamp: Math.round(frame * 1e6 * score.fps.den / score.fps.num), duration: Math.round(1e6 * score.fps.den / score.fps.num)});
      encoder.encode(image, {keyFrame: frame % keyEvery === 0});
      image.close();
      while (encoder.encodeQueueSize > 4 && !failure) await new Promise(resolve => setTimeout(resolve, 1));
      if (failure) throw failure;
      onProgress(frame + 1, score.totalFrames);
    }
    await encoder.flush();
    if (failure) throw failure;
  } finally {
    if (encoder.state !== 'closed') encoder.close();
  }
  const meta = {width: score.width, height: score.height, fps: score.fps, codec: encoding.codec, chunks};
  const bytes = encoding.container === 'mp4' ? muxMP4({...meta, description}) : muxWebM(meta);
  return {blob: new Blob([bytes], {type: encoding.mime}), bytes, container: encoding.container, codec: encoding.codec, extension: encoding.extension, frames: chunks.length, ms: Math.round(performance.now() - started)};
}

const concat = parts => {
  const out = new Uint8Array(parts.reduce((sum, part) => sum + part.length, 0));
  let offset = 0;
  for (const part of parts) { out.set(part, offset); offset += part.length; }
  return out;
};
const ascii = text => new Uint8Array([...text].map(c => c.charCodeAt(0)));
const uint = (value, length) => { const out = new Uint8Array(length); for (let i = length - 1; i >= 0; i--) { out[i] = value % 256; value = Math.floor(value / 256); } return out; };

/** WebM (Matroska) file from encoded VP8/VP9 chunks {timestamp (µs), key, data}: millisecond timecodes, a cluster per keyframe. */
export function muxWebM({width, height, fps, codec, chunks}) {
  const id = hex => new Uint8Array(hex.match(/../g).map(byte => parseInt(byte, 16)));
  const size = length => { const out = uint(length, 8); out[0] = 1; return out; }; // 8-byte EBML size
  const el = (hex, ...body) => { const data = concat(body); return concat([id(hex), size(data.length), data]); };
  const num = value => { let length = 1; while (value >= 256 ** length) length++; return uint(value, length); };
  const float = value => { const out = new Uint8Array(8); new DataView(out.buffer).setFloat64(0, value); return out; };
  const header = el('1A45DFA3', el('4286', num(1)), el('42F7', num(1)), el('42F2', num(4)), el('42F3', num(8)), el('4282', ascii('webm')), el('4287', num(2)), el('4285', num(2)));
  const app = ascii('FrameCore Works Creative Studio');
  const info = el('1549A966', el('2AD7B1', num(1000000)), el('4D80', app), el('5741', app), el('4489', float(chunks.length * 1000 * fps.den / fps.num)));
  const tracks = el('1654AE6B', el('AE', el('D7', num(1)), el('73C5', num(1)), el('83', num(1)), el('86', ascii(codec === 'vp8' ? 'V_VP8' : 'V_VP9')),
    el('23E383', num(Math.round(1e9 * fps.den / fps.num))), el('E0', el('B0', num(width)), el('BA', num(height)))));
  const clusters = [];
  let cluster = null;
  for (const chunk of chunks) {
    const time = Math.round(chunk.timestamp / 1000);
    if (!cluster || chunk.key || time - cluster.time > 32000) { cluster = {time, blocks: []}; clusters.push(cluster); }
    const relative = time - cluster.time, block = new Uint8Array(4 + chunk.data.length);
    block[0] = 0x81; block[1] = (relative >> 8) & 255; block[2] = relative & 255; block[3] = chunk.key ? 0x80 : 0;
    block.set(chunk.data, 4);
    cluster.blocks.push(el('A3', block));
  }
  return concat([header, el('18538067', info, tracks, ...clusters.map(c => el('1F43B675', el('E7', num(c.time)), ...c.blocks)))]);
}

/** MP4 file from encoded H.264 chunks in AVCC format and the avcC decoder configuration; moov before mdat. */
export function muxMP4({width, height, fps, codec, description, chunks}) {
  if (!codec.startsWith('avc1')) throw new Error(`MP4 export supports H.264 only, not ${codec}`);
  if (!description?.length) throw new Error('The H.264 decoder configuration (avcC) is missing');
  const box = (type, ...body) => { const data = concat(body); return concat([uint(data.length + 8, 4), ascii(type), data]); };
  const full = (type, version, flags, ...body) => box(type, uint(version, 1), uint(flags, 3), ...body);
  const u16 = value => uint(value, 2), u32 = value => uint(value, 4), zeros = length => new Uint8Array(length);
  const matrix = concat([0x00010000, 0, 0, 0, 0x00010000, 0, 0, 0, 0x40000000].map(u32));
  const timescale = fps.num, delta = fps.den, count = chunks.length, duration = count * delta;
  if (chunks.reduce((sum, c) => sum + c.data.length, 0) > 0xFFFFFFFF - 1e6) throw new Error('Video too large for this MP4 writer');
  // Composition offsets only when the encoder reordered frames; otherwise presentation equals decode order.
  const offsets = chunks.map((chunk, i) => Math.round(chunk.timestamp * timescale / 1e6) - i * delta);
  const keys = chunks.flatMap((chunk, i) => (chunk.key ? [i + 1] : []));
  const moov = dataOffset => box('moov',
    full('mvhd', 0, 0, u32(0), u32(0), u32(timescale), u32(duration), u32(0x00010000), u16(0x0100), zeros(10), matrix, zeros(24), u32(2)),
    box('trak',
      full('tkhd', 0, 3, u32(0), u32(0), u32(1), u32(0), u32(duration), zeros(8), u16(0), u16(0), u16(0), u16(0), matrix, u32(width * 65536), u32(height * 65536)),
      box('mdia',
        full('mdhd', 0, 0, u32(0), u32(0), u32(timescale), u32(duration), u16(0x55C4), u16(0)),
        full('hdlr', 0, 0, u32(0), ascii('vide'), zeros(12), ascii('VideoHandler'), zeros(1)),
        box('minf',
          full('vmhd', 0, 1, zeros(8)),
          box('dinf', full('dref', 0, 0, u32(1), full('url ', 0, 1))),
          box('stbl',
            full('stsd', 0, 0, u32(1), box('avc1', zeros(6), u16(1), zeros(16), u16(width), u16(height), u32(0x00480000), u32(0x00480000), u32(0), u16(1), zeros(32), u16(0x18), u16(0xFFFF), box('avcC', description))),
            full('stts', 0, 0, u32(1), u32(count), u32(delta)),
            ...(offsets.some(Boolean) ? [full('ctts', 1, 0, u32(count), ...offsets.map(o => u32(o >>> 0)))] : []),
            full('stss', 0, 0, u32(keys.length), ...keys.map(u32)),
            full('stsc', 0, 0, u32(1), u32(1), u32(count), u32(1)),
            full('stsz', 0, 0, u32(0), u32(count), ...chunks.map(c => u32(c.data.length))),
            full('stco', 0, 0, u32(1), u32(dataOffset)))))));
  const ftyp = box('ftyp', ascii('isom'), u32(512), ascii('isom'), ascii('iso2'), ascii('avc1'), ascii('mp41'));
  const offset = ftyp.length + moov(0).length + 8;
  return concat([ftyp, moov(offset), box('mdat', ...chunks.map(c => c.data))]);
}
