import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Composition, cancelRender, continueRender, delayRender, registerRoot, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';

// Product turntable: an approved glTF/GLB model of the product turns on a frame clock under studio light, with a soft
// contact shadow and an optional title. Every transform is derived from useCurrentFrame(), so any frame renders alone.
export type TurntableProps = {
  model: string;          // file in public/, e.g. product.glb (the approved model of the real product)
  turns: number;          // full turns over the composition
  startAngle: number;     // degrees, the side shown on frame 0
  tilt: number;           // degrees the camera looks down
  background: string;
  floor: string;
  title: string;          // exact copy; empty for none
  subtitle: string;
  textColor: string;
  fontFamily: string;
  settleFrames: number;   // the model rises into place over these frames (0: still from frame 0); the title is there from frame 0
};

export const defaults: TurntableProps = {
  model: 'sample-product.glb', turns: 1, startAngle: -30, tilt: 14, background: '#efe9e1', floor: '#e2d9cc',
  title: 'Miód lipowy', subtitle: 'Pasieka Beskidy · 400 g', textColor: '#2b2118', fontFamily: 'Arial, Helvetica, sans-serif', settleFrames: 12,
};

// Load the model once, wait for it before any frame is captured, and fit it to a 2-unit height standing on y = 0.
const useModel = (file: string) => {
  const [scene, setScene] = useState<THREE.Group | null>(null);
  const [handle] = useState(() => delayRender(`Loading ${file}`));
  useEffect(() => {
    new GLTFLoader().load(staticFile(file), (gltf) => {
      const root = gltf.scene;
      const box = new THREE.Box3().setFromObject(root), size = box.getSize(new THREE.Vector3()), centre = box.getCenter(new THREE.Vector3());
      const fit = 2 / Math.max(size.y, size.x * 0.8, size.z * 0.8, 1e-6);
      root.position.set(-centre.x * fit, -box.min.y * fit, -centre.z * fit);
      root.scale.setScalar(fit);
      root.traverse((child) => { if ((child as THREE.Mesh).isMesh) { child.castShadow = true; child.receiveShadow = true; } });
      const holder = new THREE.Group();
      holder.add(root);
      setScene(holder);
      continueRender(handle);
    }, undefined, (error) => cancelRender(new Error(`Could not load public/${file}: ${String(error)}`)));
  }, [file, handle]);
  return scene;
};

export const Turntable: React.FC<TurntableProps> = (props) => {
  const frame = useCurrentFrame();
  const {width, height, durationInFrames} = useVideoConfig();
  const model = useModel(props.model);
  const angle = THREE.MathUtils.degToRad(props.startAngle) + (2 * Math.PI * props.turns * frame) / durationInFrames;
  const settle = props.settleFrames > 0 ? interpolate(frame, [0, props.settleFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}) : 1;
  // The camera looks a little above the model's middle, so the product sits in the lower part and the title has the top.
  const tilt = THREE.MathUtils.degToRad(props.tilt), distance = 7.4, portrait = height > width, aim = portrait ? 1.5 : 1.3;
  const camera = useMemo(() => ({position: [0, aim + Math.sin(tilt) * distance, Math.cos(tilt) * distance] as [number, number, number], fov: portrait ? 40 : 30}), [tilt, portrait, aim]);
  const titleSize = Math.round(Math.min(width, height) * 0.07);
  return (
    <AbsoluteFill style={{backgroundColor: props.background}}>
      <ThreeCanvas width={width} height={height} camera={camera} shadows onCreated={({camera: c}) => c.lookAt(0, aim, 0)}>
        <ambientLight intensity={0.55} />
        <hemisphereLight args={['#ffffff', props.floor, 0.6]} />
        <directionalLight position={[3.5, 6, 4]} intensity={2.6} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-3} shadow-camera-right={3} shadow-camera-top={3} shadow-camera-bottom={-3} />
        <directionalLight position={[-5, 3, -2]} intensity={0.9} />
        <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
          <circleGeometry args={[6, 64]} />
          <meshStandardMaterial color={props.floor} roughness={1} />
        </mesh>
        {model ? <group position={[0, (settle - 1) * 0.25, 0]} rotation={[0, angle, 0]} scale={0.96 + 0.04 * settle}><primitive object={model} /></group> : null}
      </ThreeCanvas>
      {props.title ? (
        <div style={{position: 'absolute', left: '7%', right: '7%', top: portrait ? '9%' : '8%', color: props.textColor, fontFamily: props.fontFamily}}>
          <div style={{fontSize: titleSize, fontWeight: 800, lineHeight: 1.1}}>{props.title}</div>
          {props.subtitle ? <div style={{fontSize: Math.round(titleSize * 0.45), marginTop: Math.round(titleSize * 0.25)}}>{props.subtitle}</div> : null}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const Root: React.FC = () => (
  <>
    <Composition id="ProductTurntable" component={Turntable} width={1080} height={1080} fps={30} durationInFrames={180} defaultProps={defaults} />
    <Composition id="ProductTurntableVertical" component={Turntable} width={1080} height={1920} fps={30} durationInFrames={240} defaultProps={defaults} />
  </>
);
registerRoot(Root);
