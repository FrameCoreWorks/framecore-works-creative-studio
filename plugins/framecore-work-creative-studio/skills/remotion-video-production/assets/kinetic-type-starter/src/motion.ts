import {Easing, interpolate} from 'remotion';

export type Scene = {
  id: string;
  start: number;
  end: number;
  purpose: string;
  copy: string[];
  holds: [number, number][];
};

export type MotionScore = {
  id: string;
  revision: number;
  fps: {num: number; den: number};
  totalFrames: number;
  width: number;
  height: number;
  tokens: {
    background: string;
    foreground: string;
    muted: string;
    accent: string;
    fontFamily: string;
    marginRatio: number;
  };
  motion: {
    entryFrames: number;
    exitFrames: number;
    lineStaggerFrames: number;
    itemStaggerFrames: number;
    entryEasing: EasingName;
    exitEasing: EasingName;
    resolveEasing: EasingName;
  };
  copy: Record<string, string>;
  scenes: Scene[];
};

// Presets match references/motion-craft.md in the Motion Graphics Workflow skill.
export const easings = {
  easeOutCubic: Easing.bezier(0.33, 1, 0.68, 1),
  easeOutQuart: Easing.bezier(0.25, 1, 0.5, 1),
  easeOutExpo: Easing.bezier(0.16, 1, 0.3, 1),
  easeInOutCubic: Easing.bezier(0.65, 0, 0.35, 1),
  easeInCubic: Easing.bezier(0.32, 0, 0.67, 0),
  linear: Easing.linear,
};
export type EasingName = keyof typeof easings;

/** Eased 0..1 progress of an interval that starts at `start` (master frame) and lasts `duration` frames. */
export const progress = (frame: number, start: number, duration: number, easing: EasingName) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    easing: easings[easing],
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

/** Scene opacity and lift for the exit that ends exactly at the scene's exclusive end. */
export const exitState = (frame: number, scene: Scene, score: MotionScore) => {
  const t = progress(frame, scene.end - score.motion.exitFrames, score.motion.exitFrames, score.motion.exitEasing);
  return {opacity: 1 - t, lift: -24 * t};
};

export const isActive = (frame: number, scene: Scene) => frame >= scene.start && frame < scene.end;
