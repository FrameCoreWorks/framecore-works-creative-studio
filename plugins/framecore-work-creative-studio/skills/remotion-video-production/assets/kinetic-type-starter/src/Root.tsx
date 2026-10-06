import {Composition} from 'remotion';
import {KineticType} from './KineticType';
import score from '../motion-score.json';
import type {MotionScore} from './motion';

// check-score.mjs validates this JSON before rendering; TypeScript cannot infer tuple holds from JSON.
const contract = score as unknown as MotionScore;

// Composition settings come from the shared motion score so code and contract cannot drift.
export const Root: React.FC = () => (
  <Composition
    id="KineticType"
    component={KineticType}
    durationInFrames={contract.totalFrames}
    fps={contract.fps.num / contract.fps.den}
    width={contract.width}
    height={contract.height}
    defaultProps={{score: contract}}
  />
);
