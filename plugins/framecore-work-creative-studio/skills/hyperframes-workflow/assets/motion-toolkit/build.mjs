import {build} from 'esbuild';
import fs from 'node:fs';
await build({entryPoints: ['app.mjs'], bundle: true, format: 'esm', outdir: 'dist', sourcemap: true, target: 'es2022', legalComments: 'linked'});
fs.copyFileSync('index.html', 'dist/index.html');
console.log('Built local browser example in dist/.');
