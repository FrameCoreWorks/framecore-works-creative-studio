import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {exitState, isActive, progress, type MotionScore, type Scene} from './motion';

type Props = {score: MotionScore};

// Every visual state is derived from the master frame; scenes receive it explicitly.
export const KineticType: React.FC<Props> = ({score}) => {
  const frame = useCurrentFrame();
  const {tokens} = score;
  const margin = Math.round(score.width * tokens.marginRatio);
  const [title, steps, end] = score.scenes;
  return (
    <AbsoluteFill style={{backgroundColor: tokens.background, fontFamily: tokens.fontFamily, color: tokens.foreground}}>
      {isActive(frame, title) && <TitleScene frame={frame} scene={title} score={score} margin={margin} />}
      {isActive(frame, steps) && <StepsScene frame={frame} scene={steps} score={score} margin={margin} />}
      {isActive(frame, end) && <EndScene frame={frame} scene={end} score={score} />}
    </AbsoluteFill>
  );
};

type SceneProps = {frame: number; scene: Scene; score: MotionScore; margin?: number};

// Line mask reveal: each line rises inside its own clipping box.
const TitleScene: React.FC<SceneProps> = ({frame, scene, score, margin}) => {
  const exit = exitState(frame, scene, score);
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: margin, opacity: exit.opacity, transform: `translateY(${exit.lift}px)`}}>
      {scene.copy.map((id, index) => {
        const t = progress(frame, scene.start + index * score.motion.lineStaggerFrames, score.motion.entryFrames, score.motion.entryEasing);
        return (
          <div key={id} style={{overflow: 'hidden', lineHeight: 1.1}}>
            <div style={{fontSize: index === 0 ? 132 : 96, fontWeight: index === 0 ? 700 : 400, transform: `translateY(${(1 - t) * 110}%)`}}>
              {score.copy[id]}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Item stagger plus a connector that grows at constant speed, because it shows a continuing process.
const StepsScene: React.FC<SceneProps> = ({frame, scene, score, margin = 0}) => {
  const exit = exitState(frame, scene, score);
  const lastEntryEnd = scene.start + (scene.copy.length - 1) * score.motion.itemStaggerFrames + score.motion.entryFrames;
  const connector = progress(frame, scene.start + 6, lastEntryEnd - scene.start, 'linear');
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: margin, paddingRight: margin, opacity: exit.opacity, transform: `translateY(${exit.lift}px)`}}>
      <div style={{position: 'relative', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: '50%', height: 6, background: score.tokens.accent, transformOrigin: 'left center', transform: `scaleX(${connector})`}} />
        {scene.copy.map((id, index) => {
          const t = progress(frame, scene.start + index * score.motion.itemStaggerFrames, score.motion.entryFrames, score.motion.entryEasing);
          return (
            <div key={id} style={{position: 'relative', padding: '12px 36px', background: score.tokens.background, fontSize: 104, fontWeight: 700, opacity: t, transform: `translateY(${(1 - t) * 32}px)`}}>
              {score.copy[id]}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Resolve with a slow-settling scale; no exit, so the final frame stays stable.
const EndScene: React.FC<SceneProps> = ({frame, scene, score}) => {
  const t = progress(frame, scene.start, 30, score.motion.resolveEasing);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontSize: 120, fontWeight: 700, opacity: t, transform: `scale(${0.94 + 0.06 * t})`}}>{score.copy[scene.copy[0]]}</div>
      <div style={{marginTop: 28, width: 160 * t, height: 6, background: score.tokens.accent}} />
    </AbsoluteFill>
  );
};
