import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame} from 'remotion';
import type {CSSProperties} from 'react';
import {buildCaptions, buildScene, captionsFrame, sceneFrame} from './motion-scenes.mjs';
import type {MotionScore, Scene} from './motion';

type Node = {key: string; type: 'box' | 'text' | 'image'; text?: string; src?: string; alt?: string; style?: CSSProperties; children?: Node[]};
type FrameStyles = Record<string, {style?: CSSProperties; text?: string}>;

// Generic renderer for declarative scene kinds. The shared scene engine describes the
// elements and their per-frame styles; this component only applies them.
export const KineticType: React.FC<{score: MotionScore}> = ({score}) => {
  const frame = useCurrentFrame();
  const {tokens} = score;
  // Captions and audio files come from the contract; audio files live in public/ (see README).
  const captions = buildCaptions(score) as unknown as Node | null;
  return (
    <AbsoluteFill style={{backgroundColor: tokens.background, fontFamily: tokens.fontFamily, color: tokens.foreground}}>
      {score.scenes.filter(scene => frame >= scene.start && frame < scene.end).map(scene => (
        <SceneView key={scene.id} scene={scene} score={score} frame={frame} />
      ))}
      {captions ? <NodeView node={captions} styles={captionsFrame(score, frame) as unknown as FrameStyles} /> : null}
      {score.music?.src ? <Audio src={staticFile(score.music.src)} volume={score.music.volume ?? 1} /> : null}
      {score.voiceover?.src ? <Audio src={staticFile(score.voiceover.src)} volume={score.voiceover.volume ?? 1} /> : null}
    </AbsoluteFill>
  );
};

const SceneView: React.FC<{scene: Scene; score: MotionScore; frame: number}> = ({scene, score, frame}) => {
  // The engine is plain JavaScript; its result shapes are documented by these local types.
  const tree = buildScene(scene, score) as unknown as Node;
  const styles = sceneFrame(scene, score, frame) as unknown as FrameStyles;
  return <NodeView node={tree} styles={styles} />;
};

const NodeView: React.FC<{node: Node; styles: FrameStyles}> = ({node, styles}) => {
  const style = {...node.style, ...styles[node.key]?.style};
  if (node.type === 'image') return <Img src={node.src ?? ''} alt={node.alt ?? ''} style={style} />;
  const text = styles[node.key]?.text ?? node.text;
  return (
    <div style={style}>
      {node.type === 'text' ? text : node.children?.map(child => <NodeView key={child.key} node={child} styles={styles} />)}
    </div>
  );
};
