// Types for the shared motion contract (motion-score.json). Easing and scene
// behaviour live in the shared scene engine, motion-scenes.mjs.
export type Scene = {
  id: string;
  start: number;
  end: number;
  purpose: string;
  kind: 'line-reveal' | 'item-stagger' | 'end-card' | 'counter' | 'quote' | 'logo-reveal';
  params: Record<string, unknown>;
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
  motion: Record<string, unknown>;
  copy: Record<string, string>;
  assets?: {id: string; src: string; alt?: string}[];
  scenes: Scene[];
};
