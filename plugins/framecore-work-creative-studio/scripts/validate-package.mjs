// Retired on 2026-10-10 by the owner's decision: this historical validator predated the conditional research policy and
// failed by design (134 known errors), so it no longer gated anything. The canonical check is validate-studio.mjs. The
// path stays because a hosted plugin update can add and overwrite files but never delete them.
export function validatePackage() {
  return {status: 'RETIRED', retired: '2026-10-10', errors: [], scope: 'Historical validator retired; run scripts/validate-studio.mjs'};
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].split('/').pop())) {
  console.log(JSON.stringify(validatePackage(), null, 2));
}
