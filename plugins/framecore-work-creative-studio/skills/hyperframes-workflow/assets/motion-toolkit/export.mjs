import {Output, BufferTarget, CanvasSource, Mp4OutputFormat, WebMOutputFormat, canEncodeVideo, Quality} from 'mediabunny';
import {config} from './timeline.mjs';

export async function exportVideo(canvas, renderer, format, onProgress, signal) {
  if (!['mp4', 'webm'].includes(format)) throw new Error('Choose MP4 or WebM.');
  const codec = format === 'mp4' ? 'avc' : 'vp9';
  const quality = new Quality({bitrate: 2_000_000});
  if (!await canEncodeVideo(codec, {width: config.width, height: config.height, frameRate: config.fps, quality})) {
    throw new Error('This browser cannot encode the selected codec at the requested dimensions/FPS.');
  }
  const output = new Output({format: format === 'mp4' ? new Mp4OutputFormat() : new WebMOutputFormat(), target: new BufferTarget()});
  const source = new CanvasSource(canvas, {codec, quality});
  output.addVideoTrack(source, {frameRate: config.fps});
  try {
    await output.start();
    for (let frame = 0; frame < config.totalFrames; frame++) {
      if (signal?.aborted) throw new Error('Export cancelled.');
      await renderer.renderFrame(frame);
      await source.add(frame / config.fps, 1 / config.fps);
      onProgress(frame + 1, config.totalFrames);
      if (frame % 15 === 0) await new Promise(resolve => setTimeout(resolve, 0));
    }
    if (signal?.aborted) throw new Error('Export cancelled.');
    source.close(); await output.finalize();
    if (signal?.aborted) throw new Error('Export cancelled.');
    return new Blob([output.target.buffer], {type: format === 'mp4' ? 'video/mp4' : 'video/webm'});
  } catch (error) {
    if (output.state !== 'canceled' && output.state !== 'finalized') await output.cancel();
    throw error;
  }
}

export class InspectionMismatch extends Error {}

// Inspect the finalized bytes, independently of the submitted frame counter.
export async function inspectVideo(blob, signal) {
  const {Input, BlobSource, ALL_FORMATS, VideoSampleSink} = await import('mediabunny');
  const input = new Input({source: new BlobSource(blob), formats: ALL_FORMATS});
  try {
    const tracks = await input.getVideoTracks();
    if (tracks.length !== 1 || (await input.getAudioTracks()).length !== 0) throw new InspectionMismatch('Expected one video track and intentional silence.');
    const codec = await tracks[0].getCodec();
    const sink = new VideoSampleSink(tracks[0]);
    let count = 0, end = 0;
    for await (const sample of sink.samples()) {
      try {
        if (signal?.aborted) throw new Error('Inspection cancelled.');
        if (sample.displayWidth !== config.width || sample.displayHeight !== config.height) throw new InspectionMismatch('Decoded dimensions differ.');
        if (Math.abs(sample.timestamp - count / config.fps) > 0.002) throw new InspectionMismatch('Decoded frame timestamp differs at ' + count);
        end = sample.timestamp + sample.duration;
        count++;
      } finally {sample.close();}
    }
    if (count !== config.totalFrames || Math.abs(end - config.totalFrames / config.fps) > 0.002) throw new InspectionMismatch('Decoded frame count or duration differs.');
    return {codec, frames: count, duration: end, width: config.width, height: config.height, fps: config.fps, audioTracks: 0};
  } finally {input.dispose();}
}
