// Build a link that opens the motion player with a contract already loaded: the contract is carried in
// the address fragment (#contract=<base64url of the UTF-8 JSON, no padding>), which browsers never send
// to a server. Dependency-free (Node 20+). Exit code: 0 printed, 2 setup problem.
//
//   node player-link.mjs motion-score.json [--player https://example.org/player.html]
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export const playerUrl = 'https://framecoreworks.github.io/framecore-works-creative-studio/';

/** The player link for a contract object. Matches the player's own encoding of an opened contract. */
export function playerLink(contract, player = playerUrl) {
  return `${player}#contract=${Buffer.from(JSON.stringify(contract), 'utf8').toString('base64url')}`;
}

/** The contract carried by a player link. */
export function contractFromLink(link) {
  const value = new URLSearchParams(new URL(link).hash.slice(1)).get('contract');
  if (!value) throw new Error('The link carries no #contract= fragment');
  return JSON.parse(Buffer.from(value, 'base64url').toString('utf8'));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), i = args.indexOf('--player');
  const file = args.find((arg, k) => !arg.startsWith('--') && args[k - 1] !== '--player');
  try {
    if (!file) throw new Error('Usage: node player-link.mjs <motion-score.json> [--player <url>]');
    console.log(playerLink(JSON.parse(fs.readFileSync(file, 'utf8')), i >= 0 ? args[i + 1] : undefined));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
