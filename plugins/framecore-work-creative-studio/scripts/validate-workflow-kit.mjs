import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual as equal} from 'node:util';

// Called after the canonical validator rejects symlinks. Reads data only.
export function validateWorkflowKit(root, packageFiles) {
  const errors = [], fail = (code, detail) => errors.push({code, detail});
  const read = relative => {
    if (typeof relative !== 'string' || path.isAbsolute(relative) || relative.split('/').includes('..') || !packageFiles.includes(relative)) throw new Error('Invalid or missing package path: ' + relative);
    return fs.readFileSync(path.join(root, relative));
  };
  const text = relative => read(relative).toString('utf8');
  const json = relative => JSON.parse(text(relative));
  const refs = 'skills/pipeline-core/references/';
  const rows = relative => text(relative).split(/\r?\n/).filter(line => line.startsWith('|')).map(line => line.split('|').slice(1, -1).map(cell => cell.trim()));
  const tokens = cell => [...cell.matchAll(/`([^`]+)`/g)].map(match => match[1]);
  try {
    const manifest = json('integrations/workflow-kit/source-manifest.json');
    if (manifest.schema_version !== 2 || manifest.source_commit !== '55c8bf19962c7bf7fb43648637ee433d990eb2a9' || manifest.source_file_count !== 359 || manifest.source_skill_count !== 35 || manifest.source_version !== '1.1.0' || manifest.snapshot_activation !== 'source_only_no_automatic_install_or_execution') fail('KIT_PROVENANCE', 'Unexpected source identity, scope or inventory');
    const sourceFiles = manifest.source_files;
    if (!Array.isArray(sourceFiles) || sourceFiles.length !== 359) throw new Error('Expected 359 source files');
    const stubPaths = new Set((manifest.discovery_stubs ?? []).map(item => item.path));
    if (stubPaths.size !== 35) fail('KIT_DISCOVERY_STUBS', 'Expected 35 inert source pointers');
    for (const stub of manifest.discovery_stubs ?? []) {
      const body = text(stub.path);
      if (body.startsWith('---') || /^name:/m.test(body) || !packageFiles.includes(stub.target) || createHash('sha256').update(body).digest('hex') !== stub.sha256) fail('KIT_DISCOVERY_STUB', stub.path);
    }
    const archive = read(manifest.archive?.path);
    if (archive.length !== manifest.archive?.bytes || createHash('sha256').update(archive).digest('hex') !== manifest.archive?.sha256) fail('KIT_SOURCE_ARCHIVE', 'Pinned archive differs');
    const snapshotFiles = packageFiles.filter(file => file.startsWith('integrations/workflow-kit/upstream/') && !stubPaths.has(file)).sort();
    if (!equal(sourceFiles.map(item => item.bundled_path).sort(), snapshotFiles)) fail('KIT_SOURCE_INVENTORY', 'Snapshot has missing, duplicated or unlisted files');
    for (const item of sourceFiles) {
      if (item.bundled_path !== 'integrations/workflow-kit/upstream/' + item.source_path.replace(/\/SKILL\.md$/, '/SKILL.source.md')) fail('KIT_SOURCE_PATH', String(item.source_path));
      const content = read(item.bundled_path);
      if (content.length !== item.bytes || createHash('sha256').update(content).digest('hex') !== item.sha256) fail('KIT_SOURCE_HASH', item.source_path);
    }
    const sourceSkills = sourceFiles.filter(item => /^\.agents\/skills\/[^/]+\/SKILL.md$/.test(item.source_path)).map(item => item.source_path.split('/')[2]).sort();
    const mappings = manifest.skill_map;
    if (!Array.isArray(mappings) || !equal(mappings.map(item => item.source_skill).sort(), sourceSkills) || mappings.filter(item => item.mode === 'new').length !== 20 || mappings.filter(item => item.mode === 'merged').length !== 15) fail('KIT_SKILL_MAP', 'Every source skill must have exactly one active owner');
    const remaps = {'onboarding-preference-tuning':'studio-workstyle-profile', 'storyboard-director':'storyboard-sequence-architect', 'producer-ai-task-builder':'audio-production-director'};
    const sourcePaths = new Set(sourceFiles.map(item => item.source_path));
    const resources = manifest.active_resources;
    if (!Array.isArray(resources) || new Set(resources.map(item => item.active_path)).size !== resources.length) throw new Error('Invalid active resource inventory');
    const expectedResources = [];
    for (const mapping of mappings) {
      const owner = remaps[mapping.source_skill] ?? mapping.source_skill;
      if (mapping.target_skill !== owner) fail('KIT_OWNER', mapping.source_skill);
      const entrypoint = 'skills/' + owner + '/SKILL.md';
      const method = mapping.mode === 'new' ? entrypoint : 'skills/' + owner + '/kit/method.md';
      if (mapping.active_method !== method) fail('KIT_METHOD', mapping.source_skill);
      const body = text(entrypoint);
      if (mapping.mode === 'merged' && !body.includes('(kit/method.md)')) fail('KIT_METHOD_ROUTE', owner);
      text(method);
      const prefix = '.agents/skills/' + mapping.source_skill + '/';
      for (const item of sourceFiles.filter(item => item.source_path.startsWith(prefix))) {
        const suffix = item.source_path.slice(prefix.length);
        if (mapping.mode === 'merged' && suffix.startsWith('agents/')) continue;
        expectedResources.push(item.source_path);
      }
    }
    if (!equal(expectedResources.sort(), resources.map(item => item.source_path).sort())) fail('KIT_RESOURCE_COVERAGE', 'All skill knowledge, templates and helpers must be active; only merged agent metadata is omitted');
    for (const resource of resources) {
      if (!sourcePaths.has(resource.source_path) || !resource.active_path.startsWith('skills/')) fail('KIT_ACTIVE_RESOURCE', String(resource.source_path));
      read(resource.active_path);
    }
    for (const resource of manifest.supporting_resources ?? []) {
      if (!sourcePaths.has(resource.source_path)) fail('KIT_SUPPORT_SOURCE', resource.source_path);
      read(resource.active_path);
    }
    const schema = json('skills/pipeline-core/assets/artifact-schemas.json');
    if (schema.path_base !== 'plugin_root') fail('KIT_SCHEMA_PATH', 'Schema examples must resolve from the plugin root');
    for (const artifact of Object.values(schema.artifacts)) for (const example of artifact.example_paths ?? []) read(example);
    const routes = json('scripts/workflow-kit-routes.json');
    const roles = Object.fromEntries(rows(refs + 'role-skill-map.md').filter(c => c.length === 4 && c[0].startsWith('`')).map(c => [tokens(c[0])[0], tokens(c[3])]));
    if (Object.keys(roles).length !== 21 || !equal(roles, routes.roles)) fail('KIT_ROLE_MAP', 'Role documentation and runtime contract differ');
    for (const [role, owners] of Object.entries(routes.roles)) {
      if (!Array.isArray(owners) || !owners.length) { fail('KIT_ROLE_OWNER', role); continue; }
      for (const owner of owners) if (!packageFiles.includes('skills/' + owner + '/SKILL.md')) fail('KIT_ROLE_OWNER', role + ': ' + owner);
    }
    const handoffs = rows(refs + 'handoff-matrix.md').filter(c => c.length === 3 && c[0] !== 'From' && !c[0].startsWith('-')).map(c => ({from:c[0], to:c[1], required_fields:c[2]}));
    const gates = rows(refs + 'gate-registry.md').filter(c => c.length === 3 && c[0].startsWith('`')).map(c => ({id:tokens(c[0])[0], owners:tokens(c[1]), artifact:c[2]}));
    if (handoffs.length !== 53 || !equal(handoffs, routes.handoffs)) fail('KIT_HANDOFF_MAP', 'Handoff documentation and runtime contract differ');
    if (gates.length !== 19 || !equal(gates, routes.gates)) fail('KIT_GATE_MAP', 'Gate documentation and runtime contract differ');
    for (const handoff of routes.handoffs) if (!roles[handoff.from] || !roles[handoff.to] || !handoff.required_fields?.trim()) fail('KIT_HANDOFF_TARGET', JSON.stringify(handoff));
    for (const gate of routes.gates) if (!gate.id || !gate.artifact || !gate.owners.length || gate.owners.some(owner => !roles[owner])) fail('KIT_GATE_OWNER', gate.id);
    const reachable = new Set(['intent-confirmation','workflow-orchestrator']);
    let changed = true;
    while (changed) {
      changed = false;
      for (const handoff of routes.handoffs) if (reachable.has(handoff.from) && !reachable.has(handoff.to)) { reachable.add(handoff.to); changed = true; }
    }
    for (const role of Object.keys(roles)) if (!reachable.has(role)) fail('KIT_ROLE_REACHABILITY', role);
    for (const target of ['storyboard-architect', 'video-prompting', 'audio-production']) {
      if (!routes.handoffs.some(item => item.from === 'music-video-direction' && item.to === target)) fail('KIT_MUSIC_HANDOFF', 'music-video-direction -> ' + target);
    }
    const researchPolicy = routes.research_policy;
    if (!researchPolicy || researchPolicy.scope !== 'every_new_substantive_creative_request' || researchPolicy.role !== 'research-evidence' || researchPolicy.gate !== 'evidence_fit' || !Array.isArray(researchPolicy.triggers) || researchPolicy.triggers.length !== 6 || !researchPolicy.untriggered_rule || !researchPolicy.unavailable_rule || !researchPolicy.reuse_rule || !researchPolicy.no_browse_rule) fail('KIT_RESEARCH_POLICY', 'Conditional triggers, untriggered, unavailable, reuse and no-browse behavior must be explicit');
    if (!routes.handoffs.some(item => item.from === 'workflow-orchestrator' && item.to === 'research-evidence') || !routes.handoffs.some(item => item.from === 'research-evidence' && item.to === 'workflow-orchestrator')) fail('KIT_RESEARCH_ROUTE', 'Research must receive the request from and return evidence to the orchestrator');
    const evidenceGate = routes.gates.find(item => item.id === 'evidence_fit');
    if (!evidenceGate || !evidenceGate.owners.includes('research-evidence') || !/Evidence Note/.test(evidenceGate.artifact)) fail('KIT_RESEARCH_GATE', 'Research output must be gated or record an explicit no-browse receipt');
    const blueprints = text(refs + 'workflow-blueprints.md');
    const blueprintOwners = {
      'Static Campaign Or E-Commerce Graphic': 'static-direction',
      'Video Campaign Or Storyboard': 'motion-direction',
      'Artist-led Music Video': 'music-video-direction',
      'Standalone Audio Planning Or Review': 'audio-production'
    };
    const sharedGates = ['intent_lock', 'workflow_route', 'evidence_fit', 'brief_completeness', 'reference_authority_fit', 'post_execution_fit', 'delivery_fit'];
    const blueprintGates = {
      'Static Campaign Or E-Commerce Graphic': [...sharedGates, 'loop_control_fit', 'direction_fit', 'copy_fit', 'promptability_fit', 'asset_manifest_fit'],
      'Video Campaign Or Storyboard': [...sharedGates, 'loop_control_fit', 'direction_fit', 'structure_fit', 'copy_fit', 'promptability_fit', 'asset_manifest_fit'],
      'Artist-led Music Video': [...sharedGates, 'direction_fit', 'structure_fit', 'promptability_fit'],
      'Standalone Audio Planning Or Review': sharedGates
    };
    const sections = new Map([...blueprints.matchAll(/^## ([^\n]+)\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)].map(match => [match[1], match[2]]));
    for (const [heading, block] of sections) {
      if (!block.includes('Route:')) continue;
      const routeText = block.split('Route:')[1].split('Required gates:')[0];
      const routeRoles = [...routeText.matchAll(/^\d+\. (`[^`]+`(?: or `[^`]+`)*)/gm)].flatMap(match => tokens(match[1]));
      const gateIds = [...(block.split('Required gates:')[1] ?? '').matchAll(/^- `([^`]+)`/gm)].map(match => match[1]);
      for (const role of routeRoles) {
        if (!roles[role] && !packageFiles.includes('skills/' + role + '/SKILL.md')) fail('KIT_BLUEPRINT_ROLE', heading + ': ' + role);
      }
      for (const id of blueprintGates[heading] ?? []) if (!gateIds.includes(id)) fail('KIT_BLUEPRINT_GATE', heading + ': missing gate ' + id);
      for (const id of gateIds) if (!routes.gates.some(gate => gate.id === id)) fail('KIT_BLUEPRINT_GATE', heading + ': unknown gate ' + id);
    }
    for (const [heading, owner] of Object.entries(blueprintOwners)) {
      const block = sections.get(heading) ?? '';
      if (!/^Route:$/m.test(block) || !/^Required gates:$/m.test(block)) fail('KIT_BLUEPRINT_STRUCTURE', heading + ': missing route or gate section');
      const route = block.split('Required gates:')[0];
      if (!route.split('\n').some(line => /^\d+\. /.test(line) && tokens(line)[0] === owner)) fail('KIT_BLUEPRINT_ROLE', heading + ': missing owner ' + owner);
    }
    const staticStart = blueprints.indexOf('## Static Campaign Or E-Commerce Graphic');
    const staticBlock = blueprints.slice(staticStart, blueprints.indexOf('## Video Campaign Or Storyboard', staticStart));
    if (!staticBlock.includes('`static-graphic-design-creator` as the integrated owner') || /^\d+\. `(?:copy-voice|image-prompting)`/m.test(staticBlock)) fail('KIT_STATIC_OWNER', 'Static-only work must keep copy and prompt compilation inside the integrated static owner');
    const core = text('skills/pipeline-core/SKILL.md');
    if (!/For static-only work[\s\S]*?integrated owner/.test(core) || !core.includes('Do not add a second Copy Voice')) fail('KIT_STATIC_OWNER', 'Pipeline Core must preserve the integrated static owner');
    for (const relative of ['skills/pipeline-core/SKILL.md', 'skills/copy-voice/SKILL.md', refs + 'loop-protocol.md', refs + 'human-voice-and-copy-delivery.md', refs + 'humanizer-routing.md']) {
      const body = text(relative);
      if (/review-and-revision\s+cycle/i.test(body) || !/no\s+repair needed/.test(body) || !/stop_sufficient/.test(body)) fail('KIT_COPY_REVIEW_POLICY', relative + ': review is required, revision is conditional, and a passing draft may stop unchanged');
    }
    if (!blueprints.includes('research-evidence') || !blueprints.includes('evidence_fit') || !blueprints.includes('Every new substantive creative route')) fail('KIT_RESEARCH_BLUEPRINT', 'All substantive routes inherit the targeted research preflight and evidence gate');
    for (const [heading,next] of [['## Static Campaign Or E-Commerce Graphic','## Video Campaign Or Storyboard'],['## Video Campaign Or Storyboard','## Artist-led Music Video']]) {
      const start=blueprints.indexOf(heading), end=blueprints.indexOf(next,start+heading.length), block=blueprints.slice(start,end);
      if (!block.includes('`research-evidence`') || !block.includes('`evidence_fit`')) fail('KIT_ROUTE_RESEARCH_STAGE', heading);
    }
    for (const heading of ['## Artist-led Music Video','## Standalone Audio Planning Or Review']) {
      const start=blueprints.indexOf(heading), end=blueprints.indexOf('\n## ',start+heading.length), block=blueprints.slice(start,end<0?blueprints.length:end);
      if (!block.includes('`research-evidence`') || !block.includes('`evidence_fit`')) fail('KIT_ROUTE_RESEARCH_STAGE', heading);
    }
    const policy = text(refs + 'studio-integration-policy.md');
    if (!policy.includes('every substantive creative task') || !policy.includes('only when a research trigger applies') || !policy.includes('No-Browse Receipt')) fail('KIT_RESEARCH_AUTHORITY', 'Conditional research and explicit no-browse handling must be active policy');
    const workflowCases = json('evals/workflow-kit-cases.json').cases;
    for (const item of workflowCases) {
      if (item.research_expectation === 'required' && !item.expected_owners?.includes('research-evidence')) fail('KIT_RESEARCH_OWNER', item.id);
      if (['not_applicable', 'not_triggered'].includes(item.research_expectation) && !item.research_exemption_reason) fail('KIT_RESEARCH_EXEMPTION', item.id);
    }
    const capabilities = text('skills/workflow-orchestrator/references/capabilities-and-handoffs.md');
    for (const phrase of ['Image supplied as a reference for a new asset','Approved base image supplied for an edit','Existing image explicitly supplied for review']) if (!capabilities.includes(phrase)) fail('KIT_IMAGE_OPERATION_ROUTE', phrase);
    if (!equal(routes.qa_by_modality, {still:'output-critic-iteration',video:'video-prompt-architect',audio:'audio-production-director',captions:'caption-studio',motion:'hyperframes-workflow'})) fail('KIT_MEDIA_QA', 'Review must route by inspected modality');
    const authority = text(refs + 'studio-integration-policy.md');
    for (const phrase of ['Missing carriers do not lower a strict requirement', 'If the first draft satisfies them', 'Tool availability is discovered from the actual host', 'Hipson Adapter supplies bounded packets', 'A clear request already establishes intent', 'After an unexplained rejection ask one specific direction question']) if (!authority.includes(phrase)) fail('KIT_AUTHORITY', phrase);
    for (const item of resources.filter(item => item.active_path.endsWith('.md'))) if (/Name the carrier or mark continuity approximate|at least one review-and-revision cycle|must use GPT Image 2/.test(text(item.active_path))) fail('KIT_STALE_POLICY', item.active_path);
  } catch (error) { fail('KIT_PACKAGE', error.message); }
  return errors;
}
