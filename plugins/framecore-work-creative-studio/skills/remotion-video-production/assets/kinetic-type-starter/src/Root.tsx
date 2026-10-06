import {Composition} from 'remotion';
import {KineticType} from './KineticType';
import {resolveFormat} from './motion-scenes.mjs';
import score from '../motion-score.json';
import type {MotionScore} from './motion';

// check-score.mjs validates this JSON before rendering; TypeScript cannot infer tuple holds from JSON.
const contract = score as unknown as MotionScore;

// One composition per output format: KineticType for the base size, KineticType-<id> for each entry
// in formats. Settings come from the shared motion score so code and contract cannot drift.
const variants = [
  {id: 'KineticType', score: contract},
  ...(contract.formats ?? []).map(format => ({id: `KineticType-${format.id}`, score: resolveFormat(contract, format.id) as unknown as MotionScore})),
];

export const Root: React.FC = () => (
  <>
    {variants.map(variant => (
      <Composition
        key={variant.id}
        id={variant.id}
        component={KineticType}
        durationInFrames={variant.score.totalFrames}
        fps={variant.score.fps.num / variant.score.fps.den}
        width={variant.score.width}
        height={variant.score.height}
        defaultProps={{score: variant.score}}
      />
    ))}
  </>
);
