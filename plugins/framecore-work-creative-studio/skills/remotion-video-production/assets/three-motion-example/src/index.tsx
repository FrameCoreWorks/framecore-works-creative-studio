import React from 'react';
import {AbsoluteFill, Composition, registerRoot, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {ThreeCanvas} from '@remotion/three';

// Original geometric study. No product, imported model, texture, remote font or audio.
export const ThreeMotion: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const phase = interpolate(frame, [24, 132], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const t = phase * phase * (3 - 2 * phase);
  return <AbsoluteFill style={{backgroundColor: '#f3eee2'}}>
    <ThreeCanvas width={width} height={height} camera={{position: [0, 0, 7], fov: 40}}>
      <ambientLight intensity={1.4}/>
      <directionalLight position={[3, 4, 5]} intensity={3}/>
      <directionalLight position={[-4, -1, 2]} intensity={0.8}/>
      <group position={[0, -0.15, 0]} rotation={[0.2 + t * 0.25, -0.6 + t * 1.2, 0]}>
        {[-1, 0, 1].map((i) => <mesh key={i}
          position={[i * (0.88 + (1 - t) * 0.25), (1 - t) * i * 0.55, (1 - t) * Math.abs(i) * -0.6]}
          rotation={[0, (1 - t) * i * 0.5, 0]}>
          <boxGeometry args={[0.72, 1.55, 0.72]}/>
          <meshStandardMaterial color={i === 0 ? '#b83a24' : '#182023'} roughness={0.32} metalness={0.15}/>
        </mesh>)}
      </group>
    </ThreeCanvas>
    <div style={{position: 'absolute', left: 36, top: 26, color: '#182023', fontFamily: 'Arial, sans-serif'}}>
      <div style={{fontSize: 28, fontWeight: 700}}>FORM / ALIGNMENT</div>
      <div style={{fontSize: 14, marginTop: 8}}>Three.js · one frame clock · original geometry</div>
    </div>
    <div style={{position: 'absolute', left: 36, bottom: 26, fontFamily: 'Arial, sans-serif', fontSize: 13, color: '#182023'}}>
      {frame < 132 ? 'Three parts become one composition.' : 'A stable final hold.'}
    </div>
  </AbsoluteFill>;
};

const Root: React.FC = () => <Composition id="FrameCoreThree" component={ThreeMotion}
  width={640} height={360} fps={30} durationInFrames={180}/>;
registerRoot(Root);
