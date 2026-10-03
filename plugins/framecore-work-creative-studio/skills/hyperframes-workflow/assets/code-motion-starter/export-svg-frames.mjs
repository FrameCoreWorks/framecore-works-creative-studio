// Exports deterministic SVG source frames, not raster frames or encoded video.
import {mkdir, writeFile} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {contract, svgAtFrame} from './motion.mjs';

const destination = process.argv[2];
if (!destination || process.argv.length !== 3) {
  console.error('Usage: node export-svg-frames.mjs <new-output-directory>');
  process.exitCode = 1;
} else {
  const output = resolve(destination);
  await mkdir(dirname(output), {recursive: true});
  await mkdir(output); // Refuse an existing destination; preserve previous exports.
  try {
    for (let frame = 0; frame < contract.totalFrames; frame++) {
      const name = 'frame-' + String(frame).padStart(5, '0') + '.svg';
      await writeFile(resolve(output, name), svgAtFrame(frame), {flag: 'wx'});
    }
    await writeFile(resolve(output, 'manifest.json'), JSON.stringify({
      contract, durationSeconds: contract.totalFrames / contract.fps,
      framePattern: 'frame-%05d.svg', range: [0, contract.totalFrames],
      format: 'SVG source sequence', encodedVideo: false,
      temporalReview: 'NOT VERIFIED', fontPortability: 'environment-dependent',
    }, null, 2) + '\n', {flag: 'wx'});
    console.log(JSON.stringify({output, frames: contract.totalFrames, encodedVideo: false}));
  } catch (error) {
    console.error('Export interrupted; partial output may remain in the new destination.');
    throw error;
  }
}
