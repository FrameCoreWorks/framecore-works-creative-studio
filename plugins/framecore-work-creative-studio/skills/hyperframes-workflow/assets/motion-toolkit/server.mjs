import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve('dist');
if (!fs.existsSync(path.join(root, 'index.html'))) throw new Error('Run npm run build first.');
const files = new Set(fs.readdirSync(root).filter(name => fs.statSync(path.join(root, name)).isFile()));
const server = http.createServer((req, res) => {
  const name = new URL(req.url, 'http://localhost').pathname.slice(1) || 'index.html';
  if (req.method !== 'GET' || !files.has(name)) {res.writeHead(404); res.end('Not found'); return;}
  const type = name.endsWith('.html') ? 'text/html' : name.endsWith('.js') ? 'text/javascript' : 'text/plain';
  res.writeHead(200, {'Content-Type': type + '; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'});
  fs.createReadStream(path.join(root, name)).pipe(res);
});
server.listen(8766, '127.0.0.1', () => console.log('Motion Toolkit: http://127.0.0.1:8766'));
