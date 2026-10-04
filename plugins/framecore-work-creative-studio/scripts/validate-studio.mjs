import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {isDeepStrictEqual} from 'node:util';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {validateMotionToolkit} from './validate-motion-toolkit.mjs';
import {validateWorkflowKit} from './validate-workflow-kit.mjs';
import {loadEffectiveEvals} from './load-effective-evals.mjs';
import {validateLearningMode} from './validate-learning-mode.mjs';
import {validateQualityMethods} from './validate-quality-methods.mjs';
import {validateCampaignWorkflow} from './validate-campaign-workflow.mjs';

const expectedOwnerCount = 37;
const criticalIds = ['research_privacy', 'untrusted_sources', 'research_not_execution', 'research_failure_honesty', 'prompt_only', 'handoff_locks', 'actual_output_review', 'host_model_honesty'];
const webStates = new Set(['available_read_only', 'prohibited_by_user', 'unavailable', 'blocked', 'timeout', 'error']);

function anchors(text) {
  const out = new Set(), occurrences = new Map();
  let fence;
  for (const line of text.split(/\r?\n/)) {
    const token = line.match(/^\s*(`{3,}|~{3,})/)?.[1];
    if (token) { if (!fence) fence = token[0]; else if (fence === token[0]) fence = undefined; continue; }
    if (fence) continue;
    const heading = line.match(/^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$/)?.[1];
    if (!heading) continue;
    const slug = heading.replace(/<[^>]*>/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
    const count = occurrences.get(slug) ?? 0; occurrences.set(slug, count + 1); out.add(count ? slug + '-' + count : slug);
  }
  return out;
}

export function validateStudio(root, {legacy = false} = {}) {
  const base = path.resolve(root), errors = [], warnings = [], files = [], texts = new Map();
  const fail = (code, detail) => errors.push({code, detail});
  const within = target => target === base || target.startsWith(base + path.sep);
  const result = () => ({status: errors.length ? 'FAIL' : 'PASS', scope: 'Structural and planned-contract checks only; not host behavior, media QA, or legacy test equivalence.', errors, warnings});
  // Reject symlinks before reading any package content. No source module is executed by canonical validation.
  function walk(directory) {
    for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
      const target = path.join(directory, entry.name), rel = path.relative(base, target);
      if (entry.isSymbolicLink()) { fail('SYMLINK', rel); continue; }
      if (entry.name.startsWith('._')) fail('SIDECAR', rel);
      if (entry.isDirectory()) walk(target); else if (entry.isFile()) files.push(rel);
    }
  }
  try {
    if (fs.lstatSync(base).isSymbolicLink()) throw new Error('Package root must not be a symlink');
    walk(base);
  } catch (error) { fail('PACKAGE_ACCESS', error.message); return result(); }
  if (errors.some(error => error.code === 'SYMLINK')) return result();
  const read = relative => {
    const target = path.resolve(base, relative);
    if (!within(target) || target === base) throw new Error('Path outside package: ' + relative);
    return fs.readFileSync(target, 'utf8');
  };
  const json = relative => {
    try { const data = JSON.parse(read(relative)); if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error('Expected a JSON object'); return data; }
    catch (error) { fail('JSON', relative + ': ' + error.message); return {}; }
  };
  errors.push(...validateMotionToolkit(base));
  errors.push(...validateWorkflowKit(base, files));
  errors.push(...validateLearningMode(base, files));
  errors.push(...validateQualityMethods(base));
  errors.push(...validateCampaignWorkflow(base, files));
  // Contract reachability and evidence boundaries; this does not execute model QA.
  const loopProfile = 'skills/pipeline-core/references/loop-protocol.md';
  try {
    const body = read(loopProfile);
    for (const pattern of [/## Automatic output review/, /automatically run one/, /Do not wait for\s+the user to request QA/, /at most three evaluation passes/, /Honor a stricter domain budget/, /deliver the result unchanged/, /QA alone authorizes no generation/, /media outcome uninspected/, /do not stack a second loop/]) {
      if (!pattern.test(body)) fail('OUTPUT_REVIEW_POLICY', loopProfile + ': ' + pattern);
    }
  } catch (error) { fail('OUTPUT_REVIEW_POLICY', error.message); }
  for (const relative of files.filter(file => /^skills\/[^/]+\/SKILL\.md$/.test(file))) {
    const link = relative === 'skills/pipeline-core/SKILL.md' ? 'references/loop-protocol.md#automatic-output-review' : '../pipeline-core/references/loop-protocol.md#automatic-output-review';
    if (!read(relative).includes('automatically apply [output review](' + link + ')')) fail('OUTPUT_REVIEW_ENTRY', relative);
  }
  // Guard the shared method contract; these checks do not execute model reasoning.
  const reasoningPolicy = 'skills/pipeline-core/references/inference-reasoning-methods.md';
  try {
    const body = read(reasoningPolicy);
    for (const pattern of [/CQoT means \*\*Critical-Questions-of-Thought\*\*/, /## One review, conditional methods/, /up to three critical questions per pass/, /CoVe is claim verification/, /leave missing evidence Unknown/, /No method\s+or handoff resets this budget/, /Passing work stops unchanged/, /actual delegation capability and task\s+authorization exist/, /do not require a model to reveal or narrate hidden reasoning/, /do not exceed 4 distinct variants/]) {
      if (!pattern.test(body)) fail('REASONING_METHOD_POLICY', reasoningPolicy + ': ' + pattern);
    }
    if (/Concise Quality (?:Of|of) Thought/.test(body)) fail('REASONING_METHOD_POLICY', 'Conflicting CQoT expansion');
    for (const relative of ['skills/pipeline-core/SKILL.md', 'skills/workflow-orchestrator/SKILL.md', 'skills/workflow-orchestrator/kit/method.md', 'skills/output-critic-iteration/SKILL.md', 'skills/research-evidence/SKILL.md', loopProfile]) {
      if (!read(relative).includes('inference-reasoning-methods.md#one-review-conditional-methods')) fail('REASONING_METHOD_ROUTE', relative);
    }
  } catch (error) { fail('REASONING_METHOD_POLICY', error.message); }
  // Brand-profile checks guard packaged contracts, not host design or file QA.
  const brandProfile = 'skills/workflow-orchestrator/references/brand-identity-workflow.md';
  const brandPack = 'skills/workflow-orchestrator/assets/brand-identity.template.md';
  const needBrand = (relative, patterns) => {
    try {
      const body = read(relative);
      for (const pattern of patterns) if (!pattern.test(body)) fail('BRAND_IDENTITY_SOURCE', relative + ': ' + pattern);
    } catch (error) { fail('BRAND_IDENTITY_SOURCE', relative + ': ' + error.message); }
  };
  needBrand(brandProfile, [/Ask exactly one missing question per response and wait/, /Keep one Project State/, /logo-only request stays logo-only/, /\.\.\/\.\.\/marketing\/SKILL\.md/, /\.\.\/\.\.\/static-graphic-design-creator\/SKILL\.md/, /\.\.\/\.\.\/delivery-documentation\/SKILL\.md/, /brief_revision/, /strategy_revision/, /## Strategy acceptance/, /## Logo and visual-system acceptance/, /## Guide, applications and delivery acceptance/, /actual vector geometry/, /CMYK.*Unknown/, /trademark clearance/, /asset lifecycle and dependency contract/]);
  needBrand(brandPack, [/existing Project State/, /one pending question/, /strategy_revision/, /logo_revision/, /identity_guide_revision/, /actual_files/, /verified_production_master/, /remaining_Unknown/, /source_revisions/]);
  for (const owner of ['marketing', 'static-graphic-design-creator', 'brief-architect', 'delivery-documentation', 'pipeline-core', 'workflow-orchestrator']) needBrand('skills/' + owner + '/SKILL.md', [/brand-identity-workflow\.md/]);
  needBrand('skills/pipeline-core/references/workflow-blueprints.md', [/brand-identity-workflow\.md/, /logo-only request skips the unrequested stages/]);
  const portable = json('plugin.json'), compatibility = json('.codex-plugin/plugin.json'), registry = json('scripts/studio-contracts.json');
  for (const key of ['name', 'version', 'description', 'author']) if (!portable[key] || !isDeepStrictEqual(portable[key], compatibility[key])) fail('MANIFEST_IDENTITY', key);
  if (!isDeepStrictEqual(portable.keywords, compatibility.keywords)) fail('MANIFEST_IDENTITY', 'keywords');
  if (portable.name !== 'framecore-work-creative-studio') fail('PLUGIN_IDENTITY', String(portable.name));
  const semver = String(portable.version ?? '').match(/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$/);
  if (!semver || semver[4]?.split('.').some(part => /^\d+$/.test(part) && /^0\d/.test(part))) fail('VERSION', String(portable.version));
  if (portable.$schema !== 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json') fail('MANIFEST_SCHEMA', 'Portable schema missing');
  const discovery = compatibility.skills;
  if (typeof discovery !== 'string' || path.isAbsolute(discovery) || discovery.includes('\0') || path.resolve(base, discovery) !== path.join(base, 'skills')) fail('SKILLS_PATH', String(discovery));
  const ui = portable.extensions?.['com.openai']?.interface;
  if (!ui || !isDeepStrictEqual(ui, compatibility.interface)) fail('INTERFACE', 'Portable and compatibility interfaces differ');
  if (ui?.displayName !== 'FrameCore Works Creative Studio') fail('DISPLAY_NAME', 'Unexpected display name');
  if (typeof ui?.shortDescription !== 'string' || !ui.shortDescription.trim() || [...ui.shortDescription].length > 30) fail('SHORT_DESCRIPTION', 'Listing subtitle must have one to thirty characters');
  if (!Array.isArray(ui?.defaultPrompt) || !ui.defaultPrompt.length || ui.defaultPrompt.length > 3 || ui.defaultPrompt.some(item => typeof item !== 'string' || item.length > 128)) fail('STARTERS', 'Expected one to three concise starters');
  for (const name of ['mcp.json', '.mcp.json', 'app.json', '.app.json', 'hooks.json']) if (files.includes(name)) fail('UNPLANNED_INTEGRATION', name);
  for (const key of ['mcpServers', 'apps', 'hooks']) if (key in portable || key in compatibility || key in (portable.extensions?.['com.openai'] ?? {})) fail('UNPLANNED_INTEGRATION', key);
  for (const required of ['NOTICE', 'licenses/Apache-2.0.txt']) if (!files.includes(required)) fail('PROVENANCE', required);
  const staticProvenance = json('skills/static-graphic-design-creator/source-provenance.json');
  if (staticProvenance.immutable_source_commit !== 'cbfc0160333d8605078c9a75508116b678f5af99' || staticProvenance.source_bundle_file_count !== 34 || !Array.isArray(staticProvenance.files) || staticProvenance.files.length !== 34) fail('STATIC_SOURCE_MANIFEST', 'Expected the complete pinned 34-file source bundle');
  for (const sourceFile of staticProvenance.files ?? []) {
    const relative = 'skills/static-graphic-design-creator/' + sourceFile.bundled_path;
    if (!files.includes(relative)) { fail('STATIC_SOURCE_FILE', relative); continue; }
    const digest = createHash('sha256').update(fs.readFileSync(path.join(base, relative))).digest('hex');
    if (digest !== sourceFile.sha256 || sourceFile.sha256_verified_after_transfer !== true) fail('STATIC_SOURCE_HASH', relative);
  }
  for (const relative of files.filter(file => file.endsWith('.md') && !file.startsWith('integrations/workflow-kit/upstream/'))) {
    const text = read(relative); texts.set(relative, text);
    if (relative.startsWith('skills/') && /\/Users\/|\/Volumes\/|turn\d+(?:search|view)\d+|\[TODO:/i.test(text)) fail('RUNTIME_HYGIENE', relative);
    if (relative.endsWith('/SKILL.md')) {
      const frontmatter = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/), name = frontmatter?.[1].match(/^name:\s*(.+)$/m)?.[1].trim(), description = frontmatter?.[1].match(/^description:\s*(.+)$/m)?.[1].trim();
      if (name !== path.basename(path.dirname(relative)) || !description || description.length > 1024) fail('SKILL_METADATA', relative);
      if (text.split('\n').length > 500) fail('SKILL_SIZE', relative);
    }
    if (relative.includes('/references/') && text.trim().length < 500) fail('THIN_REFERENCE', relative);
  }
  for (const [relative, text] of texts) for (const match of text.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    const href = match[1].replace(/^<|>$/g, '');
    if (/^(https?:|mailto:)/i.test(href)) continue;
    try {
      const split = href.indexOf('#'), filePart = decodeURIComponent(split < 0 ? href : href.slice(0, split)), fragment = split < 0 ? '' : decodeURIComponent(href.slice(split + 1));
      const target = filePart ? path.resolve(base, path.dirname(relative), filePart) : path.join(base, relative);
      if (!within(target)) fail('LINK_ESCAPE', relative + ' -> ' + href);
      else if (!fs.existsSync(target)) fail('BROKEN_LINK', relative + ' -> ' + href);
      else if (fragment && target.endsWith('.md') && !anchors(texts.get(path.relative(base, target)) ?? read(path.relative(base, target))).has(fragment)) fail('BROKEN_ANCHOR', relative + ' -> ' + href);
    } catch (error) { fail('LINK_ENCODING', relative + ': ' + error.message); }
  }
  // Host discovery proved recursive in dev.30: scan every SKILL.md, including source mirrors.
  const discovered = files.filter(file => file.endsWith('/SKILL.md')).filter(file => /^---\r?\n/.test(read(file)));
  const expectedEntrypoints = files.filter(file => /^skills\/[^/]+\/SKILL\.md$/.test(file));
  if (!isDeepStrictEqual(discovered.sort(), expectedEntrypoints.sort())) fail('RECURSIVE_DISCOVERY', 'Only canonical active roots may expose skill frontmatter');
  const owners = Array.isArray(registry.owners) ? registry.owners.filter(owner => owner && typeof owner === 'object' && typeof owner.id === 'string') : [];
  const ownerIds = owners.map(owner => owner.id), actualOwners = files.filter(file => /^skills\/[^/]+\/SKILL\.md$/.test(file)).map(file => file.split('/')[1]).sort();
  if (registry.schema_version !== 1 || owners.length !== expectedOwnerCount || new Set(ownerIds).size !== expectedOwnerCount || !isDeepStrictEqual([...ownerIds].sort(), actualOwners)) fail('OWNER_ROSTER', 'Registry must match all thirty-seven installed skill roots');
  // UI names are distinct from stable routing IDs. Check every discovered root,
  // including future additions, rather than only a fixed list of current names.
  const nameSpellings = new Map([['ai', 'AI'], ['ugc', 'UGC'], ['hyperframes', 'HyperFrames'], ['opencut', 'OpenCut']]);
  const displayNames = new Set();
  for (const id of actualOwners) {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) fail('SKILL_ID_FORMAT', id);
    const relative = 'skills/' + id + '/agents/openai.yaml';
    if (!files.includes(relative)) { fail('SKILL_DISPLAY_NAME', relative + ': missing UI metadata'); continue; }
    const config = read(relative);
    // The naming standard uses a double-quoted scalar directly under interface.
    const sections = [...config.matchAll(/^interface:[ \t]*\r?\n((?:[ \t]+[^\r\n]*\r?\n|[ \t]*\r?\n)*)/gm)];
    const entries = [...(sections[0]?.[1] ?? '').matchAll(/^  display_name:[ \t]*("(?:[^"\\\r\n]|\\[^\r\n])*")[ \t]*$/gm)];
    let title;
    try { if (sections.length === 1 && entries.length === 1) title = JSON.parse(entries[0][1]); } catch { /* invalid scalar fails below */ }
    const expected = id.split('-').map(word => nameSpellings.get(word) ?? word[0].toUpperCase() + word.slice(1)).join(' ');
    if (title !== expected) fail('SKILL_DISPLAY_NAME', relative + ': expected interface.display_name ' + JSON.stringify(expected));
    // Included agent metadata also requires a short UI description. Enforce the
    // repository's quoted-scalar format and the 25–64 character authoring range.
    // This checks source compatibility, not registration in an active client.
    const blurbs = [...(sections[0]?.[1] ?? '').matchAll(/^  short_description:[ \t]*("(?:[^"\\\r\n]|\\[^\r\n])*")[ \t]*$/gm)];
    let blurb;
    try { if (sections.length === 1 && blurbs.length === 1) blurb = JSON.parse(blurbs[0][1]); } catch { /* invalid scalar fails below */ }
    if (typeof blurb !== 'string' || !blurb.trim() || [...blurb].length < 25 || [...blurb].length > 64) fail('SKILL_SHORT_DESCRIPTION', relative + ': expected one interface.short_description string of 25–64 characters');
    if (typeof title === 'string') {
      if (displayNames.has(title)) fail('SKILL_DISPLAY_NAME_DUPLICATE', title);
      displayNames.add(title);
    }
  }
  const routing = texts.get('skills/workflow-orchestrator/SKILL.md') ?? '';
  const identityBegin = '<!-- BEGIN PACKAGE IDENTITY -->', identityEnd = '<!-- END PACKAGE IDENTITY -->';
  const start = routing.indexOf(identityBegin), end = routing.indexOf(identityEnd);
  let entryIdentity;
  try {
    if (routing.split(identityBegin).length === 2 && routing.split(identityEnd).length === 2 && start >= 0 && end > start) {
      entryIdentity = JSON.parse(routing.slice(start + identityBegin.length, end));
    }
  } catch { /* malformed projection fails below */ }
  if (!isDeepStrictEqual(entryIdentity, {name: portable.name, version: portable.version})) fail('PACKAGE_IDENTITY', 'Entry identity must match the current manifests exactly');
  if (start < 0 || end < 0 || end >= routing.indexOf('## Immediate complete startup response')) fail('PACKAGE_IDENTITY_PLACEMENT', 'Read package identity before resolving version or startup requests');
  for (const phrase of ['plugin-version/installation-status request', 'Reread this entry through the active host', 'read package version', 'host-supplied skill revision', 'current sources for the same bundle conflict', 'saved hosted release', 'latest GitHub release', 'Never report a version from memory', 'current version cannot be confirmed']) {
    if (!routing.includes(phrase)) fail('VERSION_REPORTING_POLICY', phrase);
  }
  const routeRows = routing.split(/\r?\n/).filter(line => line.startsWith('|') && line.includes('/SKILL.md)'));
  const linkedOwnersByRow = new Map();
  const seenRouteRows = new Set();
  for (const row of routeRows) {
    if (seenRouteRows.has(row)) fail('OWNER_ROUTE', 'Duplicate route row: ' + row.split('|')[1]?.trim());
    seenRouteRows.add(row);
    const linkedOwners = [...row.matchAll(/\(\.\.\/([a-z0-9-]+)\/SKILL\.md\)/g)].map(match => match[1]);
    if (new Set(linkedOwners).size !== linkedOwners.length) fail('OWNER_ROUTE', 'Duplicate owner link in route row: ' + row.split('|')[1]?.trim());
    for (const id of linkedOwners) {
      if (!linkedOwnersByRow.has(id)) linkedOwnersByRow.set(id, []);
      linkedOwnersByRow.get(id).push(row);
    }
  }
  for (const owner of owners) {
    if (owner.entrypoint !== 'skills/' + owner.id + '/SKILL.md' || !texts.has(owner.entrypoint)) { fail('OWNER_ENTRYPOINT', owner.id); continue; }
    const expectedRoute = !['workflow-orchestrator', 'producer-ai-task-builder'].includes(owner.id);
    if (owner.route_required !== expectedRoute) fail('OWNER_ROUTE_CONTRACT', owner.id);
    if (owner.route_required && !linkedOwnersByRow.has(owner.id)) fail('OWNER_ROUTE', owner.id + ': no table route');
    if (owner.id !== 'research-evidence') {
      const instructions = texts.get(owner.entrypoint), index = instructions.indexOf('../research-evidence/SKILL.md');
      if (index < 0) fail('RESEARCH_HANDOFF', owner.id);
      else if (!/\bmandatory\b/i.test(instructions.slice(Math.max(0, index - 220), index))) fail('RESEARCH_MANDATORY', owner.id);
    }
  }
  const operationRoutes = Array.isArray(registry.operation_routes) ? registry.operation_routes : [];
  const requiredOperations = ['Image supplied as a reference for a new asset', 'Approved base image supplied for an edit', 'Existing image explicitly supplied for review'];
  for (const need of requiredOperations) if (operationRoutes.filter(route => route?.need === need).length !== 1) fail('OPERATION_ROUTE_CONTRACT', 'Expected exactly one operation contract: ' + need);
  for (const contract of operationRoutes) {
    if (!contract || typeof contract.need !== 'string' || !Array.isArray(contract.owners) || !contract.owners.length || contract.owners.some(id => !ownerIds.includes(id))) {
      fail('OPERATION_ROUTE_CONTRACT', String(contract?.need ?? 'invalid route'));
      continue;
    }
    const matchingRows = routeRows.filter(row => row.split('|')[1]?.trim() === contract.need);
    if (matchingRows.length !== 1) {
      fail('OPERATION_ROUTE', contract.need + ': expected one row; found ' + matchingRows.length);
      continue;
    }
    const actualOwners = [...matchingRows[0].matchAll(/\(\.\.\/([a-z0-9-]+)\/SKILL\.md\)/g)].map(match => match[1]).sort();
    if (!isDeepStrictEqual(actualOwners, [...contract.owners].sort())) fail('OPERATION_ROUTE', contract.need + ': expected ' + contract.owners.join(', ') + '; found ' + actualOwners.join(', '));
  }
  const upgrade = json('scripts/creative-upgrade-contracts.json');
  if (upgrade.schema_version !== 1 || !Array.isArray(upgrade.owners) || !Array.isArray(upgrade.references) || !Array.isArray(upgrade.source_ids)) fail('CREATIVE_REGISTRY', 'Invalid creative resource registry');
  else {
    const linkedBy = new Map(upgrade.references.map(relative => [relative, []]));
    for (const owner of upgrade.owners) {
      if (!ownerIds.includes(owner)) { fail('CREATIVE_OWNER', String(owner)); continue; }
      const relative = 'skills/' + owner + '/SKILL.md';
      const destinations = [...(texts.get(relative) ?? '').matchAll(/\[[^\]]+\]\(([^)]+)\)/g)].map(match => path.relative(base, path.resolve(base, path.dirname(relative), match[1].split('#')[0])));
      const linked = upgrade.references.filter(reference => destinations.includes(reference));
      if (!linked.length) fail('CREATIVE_OWNER_ROUTE', owner);
      for (const reference of linked) linkedBy.get(reference).push(owner);
    }
    for (const [reference, linked] of linkedBy) if (!texts.has(reference) || !linked.length) fail('CREATIVE_REFERENCE_ROUTE', reference);
    const sources = texts.get('skills/research-evidence/references/creative-upgrade-sources.md') ?? '';
    const sourceIds = [...sources.matchAll(/^### (C\d+):/gm)].map(match => match[1]);
    if (!isDeepStrictEqual([...sourceIds].sort(), [...upgrade.source_ids].sort()) || new Set(sourceIds).size !== sourceIds.length) fail('CREATIVE_SOURCES', 'Source cards must match their registry');
  }
  const contracts = Array.isArray(registry.critical_contracts) ? registry.critical_contracts.filter(item => item && typeof item === 'object' && typeof item.id === 'string') : [];
  if (!isDeepStrictEqual(contracts.map(item => item.id).sort(), [...criticalIds].sort())) fail('CRITICAL_ROSTER', 'Critical contract IDs changed or missing');
  for (const contract of contracts) {
    const text = texts.get(contract.path);
    if (!text || !Array.isArray(contract.required_patterns) || !contract.required_patterns.length) { fail('CRITICAL_CONTRACT', contract.id); continue; }
    for (const pattern of contract.required_patterns) {
      try { if (!new RegExp(pattern, 'i').test(text)) fail('CRITICAL_CONTRACT', contract.id + ': missing ' + pattern); }
      catch { fail('CONTRACT_PATTERN', contract.id); }
    }
  }
  for (const [relative, prefix] of Object.entries(registry.release_documents ?? {})) {
    if (!(texts.get(relative) ?? '').includes(prefix + ' ' + portable.version + '.')) fail('DOC_VERSION', relative);
  }
  if (!isDeepStrictEqual(Object.keys(registry.release_documents ?? {}).sort(), ['README.md', 'docs/migration-status.md'])) fail('RELEASE_DOCS', 'Expected README and migration status markers');
  const migration = texts.get('docs/migration-status.md') ?? '';
  for (const owner of owners) if (!migration.includes(owner.id)) fail('MIGRATION_OWNER', owner.id);
  let evaluations;
  try {
    const effective = loadEffectiveEvals(base);
    for (const item of effective.cases) {
      if (item.status !== 'planned') fail('EVAL_EXECUTION_CLAIM', item.id);
      if (typeof item.user_request !== 'string' || !item.user_request.trim() || !Array.isArray(item.checks) || !item.checks.length || item.checks.some(check => typeof check !== 'string' || !check.trim()) || typeof item.expected_branch !== 'string' || !item.expected_branch.trim() || !item.context || typeof item.context !== 'object' || Array.isArray(item.context) || !Array.isArray(item.available_assets)) fail('EVAL_SCHEMA', item.id);
      if (!['textual_fixture_no_execution', 'planned_fixture_only'].includes(item.tool_state?.mode)) fail('EVAL_TOOL_EXECUTION', item.id);
      if (!webStates.has(item.tool_state?.web_search)) fail('EVAL_WEB_STATE', item.id);
      if (!['required', 'not_applicable', 'prohibited_by_user'].includes(item.research_expectation)) fail('EVAL_RESEARCH', item.id);
      if (item.research_expectation === 'not_applicable' && !item.research_exemption_reason) fail('EVAL_EXEMPTION', item.id);
      if ((item.research_expectation === 'prohibited_by_user') !== (item.tool_state?.web_search === 'prohibited_by_user')) fail('EVAL_BROWSE_BOUNDARY', item.id);
    }
    if (!isDeepStrictEqual([...effective.overrides_applied].sort(), ['S01', 'S18', 'S32', 'S35', 'S45', 'S50', 'S51'])) fail('OVERRIDE_COVERAGE', 'The seven reviewed inherited cases require their effective overrides');
    for (const id of ['S35-CROP', 'S35-PAD', 'S35-CONFLICT', 'S45-FINAL']) if (!effective.cases.some(item => item.id === id)) fail('OVERRIDE_VARIANT', id);
    const hostCases = effective.cases.filter(item => item.provenance.source_file === 'studio-behavior-cases.json');
    if (hostCases.length !== 25 || new Set(hostCases.map(item => item.family)).size !== 25) fail('HOST_SCENARIO_COVERAGE', 'Expected twenty-five distinct planned families');
    for (const state of ['unavailable', 'timeout', 'error']) if (!hostCases.some(item => item.tool_state.web_search === state)) fail('RESEARCH_FAILURE_COVERAGE', state);
    for (const item of hostCases) {
      if (item.execution_status !== 'not_run' || !Array.isArray(item.required_evidence) || !item.required_evidence.length || !Array.isArray(item.expected_owners) || item.expected_owners.some(id => !ownerIds.includes(id))) fail('HOST_EVIDENCE_CONTRACT', item.id);
    }
    const practiceCases = effective.cases.filter(item => item.provenance.source_file === 'knowledge-practice-cases.json');
    if (practiceCases.length !== 12 || new Set(practiceCases.map(item => item.family)).size !== 12) fail('KNOWLEDGE_COVERAGE', 'Expected twelve distinct knowledge-practice families');
    for (const item of practiceCases) if (item.execution_status !== 'not_run' || !Array.isArray(item.required_evidence) || !item.required_evidence.length || !Array.isArray(item.expected_owners) || !item.expected_owners.length || item.expected_owners.some(id => !ownerIds.includes(id))) fail('KNOWLEDGE_EVIDENCE', item.id);
    const integrationCases = effective.cases.filter(item => item.provenance.source_file === 'workflow-kit-cases.json');
    if (integrationCases.length !== 12 || new Set(integrationCases.map(item => item.family)).size !== 12) fail('INTEGRATION_COVERAGE', 'Expected twelve planned integration families');
    for (const item of integrationCases) if (item.execution_status !== 'not_run' || !Array.isArray(item.required_evidence) || !item.required_evidence.length || !Array.isArray(item.expected_owners) || !item.expected_owners.length || item.expected_owners.some(id => !ownerIds.includes(id))) fail('INTEGRATION_EVIDENCE', item.id);
    const activeOwnerIds = owners.filter(owner => owner.route_required || owner.id === 'workflow-orchestrator').map(owner => owner.id);
    if (!isDeepStrictEqual([...new Set([...practiceCases, ...integrationCases].flatMap(item => item.expected_owners ?? []))].sort(), [...activeOwnerIds].sort())) fail('KNOWLEDGE_OWNERS', 'Planned knowledge and integration cases must cover every active owner');
    evaluations = {legacy: effective.legacy_cases, overrides: effective.overrides_applied, added_variants: effective.additional_cases, host_scenarios: effective.host_scenarios, knowledge_scenarios: effective.knowledge_scenarios, integration_scenarios: effective.integration_scenarios, learning_scenarios: effective.learning_scenarios, campaign_scenarios: effective.campaign_scenarios, total_planned: effective.cases.length, executed: 0};
  } catch (error) { fail('EFFECTIVE_EVALS', error.message); }
  warnings.push('Canonical checks do not reproduce all historical fixture-specific assertions or the legacy 67-test suite. Run legacy diagnostics explicitly when needed.');
  const canonical = {...result(), files: files.length, owners: owners.length, evaluations};
  let legacyReport = {status: 'NOT_RUN', scope: 'Historical validator, separate from canonical checks'};
  if (legacy) {
    const run = spawnSync(process.execPath, [path.join(base, 'scripts/validate-package.mjs')], {cwd: base, encoding: 'utf8', timeout: 30000, maxBuffer: 1024 * 1024});
    let report; try { report = JSON.parse(run.stdout); } catch { /* preserve non-JSON output below */ }
    legacyReport = {status: run.error ? 'ERROR' : run.status === 0 ? 'PASS' : 'FAIL', exit_code: run.status, report, stdout: report ? undefined : run.stdout, stderr: run.stderr, error: run.error?.message};
  }
  return {status: canonical.status === 'PASS' && ['NOT_RUN', 'PASS'].includes(legacyReport.status) ? 'PASS' : 'FAIL', canonical, legacy: legacyReport};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), root = args.find(arg => !arg.startsWith('--')) ?? path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const result = validateStudio(root, {legacy: args.includes('--legacy')});
  console.log(JSON.stringify(result, null, 2));
  if (result.status !== 'PASS') process.exitCode = 1;
}
