// Original helpers. Caller supplies the approved project score and installed libraries.
export function validateScore(score) {
  if (!score || !Number.isSafeInteger(score.totalFrames) || score.totalFrames < 1) throw new RangeError('Positive integer totalFrames required');
  const {num, den} = score.fps || {};
  if (!Number.isSafeInteger(num) || !Number.isSafeInteger(den) || num <= 0 || den <= 0) throw new RangeError('FPS requires positive integer num/den');
  if (!Array.isArray(score.scenes) || !score.scenes.length) throw new TypeError('Scenes required');
  const ids = new Set(), n = score.totalFrames;
  let coverage = 0;
  for (const s of [...score.scenes].sort((a,b)=>a.start-b.start)) {
    if (!s.id || ids.has(s.id)) throw new Error('Unique scene IDs required');
    ids.add(s.id);
    if (![s.start,s.end].every(Number.isSafeInteger) || s.start < 0 || s.end > n || s.end <= s.start) throw new RangeError('Invalid scene interval');
    if (s.start > coverage) throw new Error('Uncovered scene frames');
    coverage = Math.max(coverage,s.end);
    for (const h of s.holds || []) if (!Array.isArray(h) || h.length !== 2 || !h.every(Number.isSafeInteger) || h[0] < s.start || h[1] > s.end || h[1] <= h[0]) throw new RangeError('Invalid readable hold');
  }
  if (coverage !== n) throw new Error('Scene coverage must reach totalFrames');
  const cues = new Set();
  for (const c of score.cues || []) {
    if (!c.id || cues.has(c.id)) throw new Error('Unique cue IDs required');
    cues.add(c.id);
    if (![c.frame,c.durationFrames].every(Number.isSafeInteger) || c.frame < 0 || c.durationFrames < 1 || c.frame+c.durationFrames > n) throw new RangeError('Cue including tail must fit output');
    if (!Number.isFinite(c.frequency) || c.frequency < 20 || c.frequency > 20000) throw new RangeError('Cue frequency must be 20..20000 Hz');
    if (!Number.isFinite(c.gainDb) || c.gainDb > 0 || c.gainDb < -96) throw new RangeError('Cue gainDb must be -96..0');
  }
  return score;
}
export function secondsAtFrame(frame, score) {
  if (!Number.isSafeInteger(frame) || frame < 0 || frame >= score.totalFrames) throw new RangeError('Frame outside output');
  const {num,den}=score.fps || {};
  if (!Number.isSafeInteger(num) || !Number.isSafeInteger(den) || num <= 0 || den <= 0) throw new RangeError('Invalid FPS');
  return frame * den / num;
}
export function reviewFrames(score, uniformSamples=12) {
  validateScore(score);
  if (!Number.isInteger(uniformSamples) || uniformSamples < 2 || uniformSamples > 120) throw new RangeError('Use 2..120 uniform samples');
  const frames = new Set([0,score.totalFrames-1]);
  const add = f => {if (f >= 0 && f < score.totalFrames) frames.add(f);};
  for (let i=0;i<uniformSamples;i++) add(Math.round(i*(score.totalFrames-1)/(uniformSamples-1)));
  for (const s of score.scenes) {
    for (const boundary of [s.start,s.end]) for (const offset of [-1,0,1]) add(boundary+offset);
    for (const [a,b] of s.holds || []) {add(a);add(Math.floor((a+b-1)/2));add(b-1);}
  }
  for (const c of score.cues || []) for (const offset of [-1,0,1]) add(c.frame+offset);
  return [...frames].sort((a,b)=>a-b);
}
export function cueTimes(score) {
  validateScore(score);
  return (score.cues || []).map(c=>({...c,timeSeconds:secondsAtFrame(c.frame,score),durationSeconds:c.durationFrames*score.fps.den/score.fps.num}));
}
export function renderPaperFrame(shaderMount,frame,score) {
  if (typeof shaderMount?.setSpeed !== 'function' || typeof shaderMount?.setFrame !== 'function') throw new TypeError('Initialized Paper ShaderMount required');
  const milliseconds=secondsAtFrame(frame,score)*1000;
  shaderMount.setSpeed(0);
  shaderMount.setFrame(milliseconds);
  // Capture only after the host confirms draw completion; this return is time, not render proof.
  return milliseconds;
}
export async function renderToneCues(Tone,score,{sampleRate=48000}={}) {
  const cues=cueTimes(score);
  if (!Number.isInteger(sampleRate) || sampleRate < 8000 || sampleRate > 192000) throw new RangeError('Unsupported sample rate');
  if (typeof Tone?.Offline !== 'function' || typeof Tone?.Synth !== 'function') throw new TypeError('Installed Tone Offline and Synth required');
  if (cues.some(c=>c.frequency >= sampleRate/2)) throw new RangeError('Cue frequency must be below Nyquist');
  const voices=[];
  try {
    return await Tone.Offline(()=>{
      for (const c of cues) {
        // Each declared duration includes the release tail. No runtime clock or Transport.
        const release=Math.min(0.05,c.durationSeconds/4);
        const voice=new Tone.Synth({oscillator:{type:'sine'},envelope:{attack:Math.min(0.005,c.durationSeconds/8),decay:0,sustain:0.7,release},volume:c.gainDb}).toDestination();
        voices.push(voice);
        voice.triggerAttackRelease(c.frequency,c.durationSeconds-release,c.timeSeconds);
      }
    },score.totalFrames*score.fps.den/score.fps.num,2,sampleRate);
  } finally {for (const voice of voices) voice.dispose();}
}
