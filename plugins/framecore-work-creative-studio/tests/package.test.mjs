// Retired on 2026-10-10 by the owner's decision: the historical 67-test suite asserted the old mandatory-research
// design and failed by design (20 known failures). Current behaviour is tested by the other files in this folder,
// run through scripts/check_all.sh. The path stays because a hosted plugin update cannot delete files.
import test from 'node:test';
import assert from 'node:assert/strict';
import {validatePackage} from '../scripts/validate-package.mjs';

test('the historical package suite is retired', () => {
  assert.equal(validatePackage().status, 'RETIRED');
});
