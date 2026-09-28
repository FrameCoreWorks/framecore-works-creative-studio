import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const expectedSkills = [
  'commercial-video-campaign-director', 'commercial-visual-campaign-director', 'creative-music-video-director', 'delivery-documentation',
  'humanizer', 'image-prompt-architect', 'output-critic-iteration', 'producer-ai-task-builder', 'research-evidence',
  'screenplay-story-architect', 'storyboard-board-architect',
  'storyboard-sequence-architect', 'video-prompt-architect', 'workflow-orchestrator',
];

function markdownHeadingAnchors(markdown) {
  const anchors = new Set();
  const occurrences = new Map();
  let fence = null;
  for (const line of markdown.split(/\r?\n/)) {
    const fenceMatch = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (fenceMatch) {
      if (!fence) fence = fenceMatch[1][0];
      else if (fenceMatch[1][0] === fence) fence = null;
      continue;
    }
    if (fence) continue;
    const heading = line.match(/^ {0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$/)?.[1];
    if (!heading) continue;
    const base = heading
      .replace(/<[^>]*>/g, '')
      .replace(/`([^`]*)`/g, '$1')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s-]/gu, '')
      .trim()
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
    if (!base) continue;
    const count = occurrences.get(base) ?? 0;
    let anchor = count === 0 ? base : `${base}-${count}`;
    while (anchors.has(anchor)) {
      const next = (occurrences.get(base) ?? count) + 1;
      occurrences.set(base, next);
      anchor = `${base}-${next}`;
    }
    anchors.add(anchor);
    occurrences.set(base, count + 1);
  }
  return anchors;
}

export function validatePackage(root) {
  const errors = [];
  const files = [];
  const fail = message => errors.push(message);
  const researchExpectations = new Set(['required', 'not_applicable', 'prohibited_by_user']);
  const researchExemptionReasons = new Set([
    'non_creative_intake', 'missing_required_input', 'mechanical_change_only',
    'unsupported_capability_status', 'generation_unavailable_no_creative_output',
    'missing_continuity_carrier',
  ]);
  function validateResearchExpectation(item, label) {
    if (!researchExpectations.has(item.research_expectation)) {
      fail('Missing or invalid research expectation: ' + label + '.research_expectation');
      return;
    }
    if (item.research_expectation === 'not_applicable' && !researchExemptionReasons.has(item.research_exemption_reason)) {
      fail('Research exemption needs a recognized reason: ' + label);
    }
    if (item.research_expectation !== 'not_applicable' && item.research_exemption_reason !== undefined) {
      fail('Unexpected research exemption reason: ' + label);
    }
    if (item.research_expectation === 'prohibited_by_user' && item.tool_state?.web_search !== 'prohibited_by_user') {
      fail('Research prohibition must match tool state: ' + label);
    }
    if (item.tool_state?.web_search === 'prohibited_by_user' && item.research_expectation !== 'prohibited_by_user') {
      fail('Tool state prohibits research without a user-prohibited expectation: ' + label);
    }
    if (!['textual_fixture_no_execution', 'planned_fixture_only'].includes(item.tool_state?.mode)) {
      fail('Research fixture must not claim tool execution: ' + label);
    }
  }
  const rootPath = path.resolve(root);
  const within = target => target === rootPath || target.startsWith(rootPath + path.sep);
  function walk(dir) {
    if (!fs.existsSync(dir)) { fail('Missing directory: ' + path.relative(rootPath, dir)); return; }
    for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
      const target = path.join(dir, entry.name);
      if (entry.isSymbolicLink()) { fail('Symlink is not portable: ' + path.relative(rootPath, target)); continue; }
      if (entry.name.startsWith('._')) fail('AppleDouble sidecar: ' + entry.name);
      if (entry.isDirectory()) walk(target);
      else files.push(target);
    }
  }
  walk(rootPath);
  function json(rel) {
    try { return JSON.parse(fs.readFileSync(path.join(rootPath, rel), 'utf8')); }
    catch (error) { fail(rel + ': ' + error.message); return {}; }
  }
  const portable = json('plugin.json');
  const compatibility = json('.codex-plugin/plugin.json');
  for (const key of ['name', 'version', 'description', 'author']) {
    if (!portable[key] || JSON.stringify(portable[key]) !== JSON.stringify(compatibility[key])) {
      fail('Manifest identity mismatch or missing: ' + key);
    }
  }
  if (portable.name !== path.basename(rootPath)) fail('Plugin name differs from folder');
  if (!/^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?$/.test(portable.version ?? '')) fail('Invalid version');
  if (portable.$schema !== 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json') fail('Portable schema anchor missing');
  if (compatibility.skills !== './skills/') fail('Unexpected skill discovery path');
  const openaiInterface = portable.extensions?.['com.openai']?.interface;
  if (!openaiInterface) fail('Portable OpenAI interface metadata missing');
  if (JSON.stringify(openaiInterface) !== JSON.stringify(compatibility.interface)) fail('OpenAI interface differs between portable manifest and compatibility fallback');
  if (openaiInterface?.displayName !== 'FrameCore Works Creative Studio') fail('Display name drift');
  const prompts = compatibility.interface?.defaultPrompt;
  if (!Array.isArray(prompts) || prompts.length > 3 || prompts.some(s => typeof s !== 'string' || s.length > 128)) fail('Invalid starters');
  for (const rel of ['.mcp.json', '.app.json', 'hooks.json']) {
    if (fs.existsSync(path.join(rootPath, rel))) fail('Unexpected external integration: ' + rel);
  }
  for (const key of ['mcpServers', 'apps', 'hooks']) {
    if (key in portable || key in compatibility) fail('Unexpected provider/integration field: ' + key);
  }
  const skillsPath = path.join(rootPath, 'skills');
  const actualSkills = fs.existsSync(skillsPath)
    ? fs.readdirSync(skillsPath, {withFileTypes: true}).filter(e => e.isDirectory()).map(e => e.name).sort()
    : [];
  if (JSON.stringify(actualSkills) !== JSON.stringify(expectedSkills)) fail('Runtime skill roster differs from package contract');
  const researchEntry = path.join(skillsPath, 'research-evidence', 'SKILL.md');
  const researchInstructions = fs.existsSync(researchEntry) ? fs.readFileSync(researchEntry, 'utf8') : '';
  if (!/mandatory internet research gate/i.test(researchInstructions) || !researchInstructions.includes('Every new substantive creative task MUST use an active web search')) {
    fail('Research skill must require active web search for every substantive creative task');
  }
  for (const name of [
    'workflow-orchestrator', 'creative-music-video-director', 'producer-ai-task-builder', 'commercial-video-campaign-director',
    'commercial-visual-campaign-director', 'humanizer',
    'image-prompt-architect', 'video-prompt-architect', 'screenplay-story-architect',
    'storyboard-sequence-architect', 'storyboard-board-architect',
    'output-critic-iteration', 'delivery-documentation',
  ]) {
    const entry = path.join(skillsPath, name, 'SKILL.md');
    const instructions = fs.existsSync(entry) ? fs.readFileSync(entry, 'utf8') : '';
    const researchLink = '../research-evidence/SKILL.md';
    const linkPosition = instructions.indexOf(researchLink);
    if (linkPosition < 0) {
      fail('Missing mandatory research preflight route: ' + name);
    } else {
      const routeContext = instructions.slice(Math.max(0, linkPosition - 220), linkPosition + researchLink.length);
      if (!/\bmandatory\b/i.test(routeContext) || !/public research preflight/i.test(routeContext)) {
        fail('Research preflight route must be marked mandatory: ' + name);
      }
    }
  }
  const orchestratorEntry = path.join(skillsPath, 'workflow-orchestrator', 'SKILL.md');
  const orchestratorInstructions = fs.existsSync(orchestratorEntry) ? fs.readFileSync(orchestratorEntry, 'utf8') : '';
  const campaignRouteTarget = '[commercial-video-campaign-director](../commercial-video-campaign-director/SKILL.md)';
  const campaignRouteRows = orchestratorInstructions.split(/\r?\n/).filter(line => line.startsWith('|') && line.includes(campaignRouteTarget));
  if (campaignRouteRows.length !== 1) fail('Commercial video campaign direction must have exactly one orchestrator route; found ' + campaignRouteRows.length);
  const musicVideoRouteTarget = '[creative-music-video-director](../creative-music-video-director/SKILL.md)';
  const musicVideoRouteRows = orchestratorInstructions.split(/\r?\n/).filter(line => line.startsWith('|') && line.includes(musicVideoRouteTarget));
  if (musicVideoRouteRows.length !== 1) fail('Music-video direction must have exactly one orchestrator route; found ' + musicVideoRouteRows.length);
  const producerRouteTarget = '[producer-ai-task-builder](../producer-ai-task-builder/SKILL.md)';
  const producerRouteRows = orchestratorInstructions.split(/\r?\n/).filter(line => line.startsWith('|') && line.includes(producerRouteTarget));
  if (producerRouteRows.length !== 1) fail('Producer task preparation must have exactly one orchestrator route; found ' + producerRouteRows.length);
  let references = 0;
  let runtimeBytes = 0;
  const anchorCache = new Map();
  for (const file of files) {
    const rel = path.relative(rootPath, file);
    if (!file.endsWith('.md')) continue;
    const text = fs.readFileSync(file, 'utf8');
    if (rel.startsWith('skills' + path.sep)) {
      runtimeBytes += Buffer.byteLength(text);
      if (/\/Users\/|\/Volumes\/|turn\d+(?:search|view)\d+|\[TODO:/i.test(text)) fail('Nonportable or unresolved runtime content: ' + rel);
    }
    if (path.basename(file) === 'SKILL.md') {
      const front = text.match(/^---\n([\s\S]+?)\n---\n/);
      if (!front) { fail('Missing frontmatter: ' + rel); continue; }
      const name = front[1].match(/^name:\s*(.+)$/m)?.[1].trim();
      const description = front[1].match(/^description:\s*(.+)$/m)?.[1].trim();
      if (name !== path.basename(path.dirname(file))) fail('Skill identity mismatch: ' + rel);
      if (!description || description.length > 1024) fail('Invalid skill description: ' + rel);
      if (text.split('\n').length > 500) fail('Entrypoint needs progressive disclosure: ' + rel);
    }
    if (rel.includes(path.sep + 'references' + path.sep)) {
      references++;
      if (text.trim().length < 500) fail('Empty/thin reference requires review: ' + rel);
    }
    for (const match of text.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
      const href = match[1].replace(/^<|>$/g, '');
      if (/^(https?:|mailto:)/i.test(href)) continue;
      const hashIndex = href.indexOf('#');
      const encodedPath = hashIndex < 0 ? href : href.slice(0, hashIndex);
      const encodedAnchor = hashIndex < 0 ? '' : href.slice(hashIndex + 1);
      let decodedPath;
      let anchor;
      try {
        decodedPath = decodeURIComponent(encodedPath);
        anchor = decodeURIComponent(encodedAnchor);
      } catch {
        fail('Invalid link encoding: ' + rel + ' -> ' + href);
        continue;
      }
      const target = decodedPath
        ? path.resolve(path.dirname(file), decodedPath)
        : file;
      if (!within(target)) fail('Link escapes package: ' + rel + ' -> ' + href);
      else if (!fs.existsSync(target)) fail('Broken link: ' + rel + ' -> ' + href);
      else if (anchor && target.toLowerCase().endsWith('.md')) {
        if (!anchorCache.has(target)) {
          anchorCache.set(target, markdownHeadingAnchors(fs.readFileSync(target, 'utf8')));
        }
        if (!anchorCache.get(target).has(anchor)) fail('Broken link fragment: ' + rel + ' -> ' + href);
      }
    }
  }
  for (const rel of ['NOTICE', 'licenses/Apache-2.0.txt']) {
    if (!fs.existsSync(path.join(rootPath, rel))) fail('Missing provenance/license: ' + rel);
  }
  const cases = json('evals/static-cases.json');
  if (cases.schema_version !== 2) fail('Behavior fixtures require explicit-context schema version 2');
  const imageSnapshotPath = path.join(rootPath, 'skills/research-evidence/references/image-generator-snapshot.md');
  if (!fs.existsSync(imageSnapshotPath)) {
    fail('Missing dated image-generator snapshot');
  } else {
    const imageSnapshot = fs.readFileSync(imageSnapshotPath, 'utf8');
    const familySections = [...imageSnapshot.matchAll(/^### Family: (.+)$/gm)];
    if (!imageSnapshot.includes('Snapshot date: 2026-09-24.')) fail('Image-generator snapshot must state its access date');
    if (familySections.length !== 19) fail('Image-generator snapshot must contain exactly 19 audited family cards');
    const researchSkillPath = path.join(rootPath, 'skills/research-evidence/SKILL.md');
    const sourceRegisterPath = path.join(rootPath, 'skills/research-evidence/references/initial-source-register.md');
    const researchSkill = fs.readFileSync(researchSkillPath, 'utf8');
    const sourceRegister = fs.readFileSync(sourceRegisterPath, 'utf8');
    if (!researchSkill.includes(`finite ${familySections.length}-family map`)) fail('Image snapshot count mismatch: skills/research-evidence/SKILL.md');
    if (!sourceRegister.includes(`${familySections.length} family cards plus a watchlist`)) fail('Image snapshot count mismatch: skills/research-evidence/references/initial-source-register.md');
    if (!imageSnapshot.includes('## Watchlist and evidence gaps')) fail('Image-generator snapshot must preserve a separate watchlist');
    if (!imageSnapshot.includes('## Dated practitioner evidence register')) fail('Image-generator snapshot must separate dated practitioner evidence');
    const familyNames = new Set();
    for (const [index, match] of familySections.entries()) {
      const name = match[1].trim();
      if (!name || familyNames.has(name)) fail('Duplicate or blank image-generator family card: ' + name);
      familyNames.add(name);
      const start = match.index + match[0].length;
      const end = familySections[index + 1]?.index ?? imageSnapshot.indexOf('## Watchlist and evidence gaps', start);
      const section = imageSnapshot.slice(start, end < 0 ? imageSnapshot.length : end);
      for (const label of ['**Variants:**', '**Surface and operations:**', '**Prompt guidance:**', '**Practitioner evidence:**', '**Unknowns:**', '**Sources:**']) {
        if (!section.includes(label)) fail('Image-generator family card missing ' + label + ': ' + name);
      }
      if (!/https:\/\//.test(section)) fail('Image-generator family card needs a direct source link: ' + name);
    }
    for (const dimension of ['| T2I |', '| I2I/edit |', '| Reference-led |', 'not a live market census']) {
      if (!imageSnapshot.includes(dimension)) fail('Image-generator snapshot missing evidence boundary/dimension: ' + dimension);
    }
  }
  const ids = new Set();
  for (const item of cases.cases ?? []) {
    if (!item.id || ids.has(item.id)) fail('Duplicate or missing eval ID');
    ids.add(item.id);
    if (!item.user_request || !Array.isArray(item.checks) || !item.checks.length) fail('Incomplete eval: ' + item.id);
    for (const field of ['context', 'tool_state']) {
      if (!item[field] || typeof item[field] !== 'object' || Array.isArray(item[field])) fail('Missing eval context/state: ' + item.id + '.' + field);
    }
    if (!Array.isArray(item.available_assets)) fail('Missing eval asset inventory: ' + item.id);
    if (typeof item.expected_branch !== 'string' || !item.expected_branch.trim()) fail('Missing eval expected branch: ' + item.id);
    validateResearchExpectation(item, item.id);
    if (item.status !== 'planned') fail('Fixture must not predeclare behavior PASS: ' + item.id);
  }
  if (ids.size < 26) fail('Missing regression cases');
  const imageMappingCase = cases.cases?.find(item => item.id === 'S53');
  const requiredImageMappingChecks = [
    'Runs a fresh, focused search of current official Qwen Image 3.0 documentation and attributable first-hand practitioner evidence',
    'Separates any 3.0 evidence from Qwen Image 2.1 and does not inherit sibling-version controls or results',
    'Records the named consumer-facing surface as the default unless the user explicitly names an API or third-party service',
    'Does not ask about API or wrapper merely because the model was named',
    'Marks operation-level behavior, prompt syntax, edit/reference controls, and evidence gaps as unknown when current sources do not establish them',
    'Does not present a leaderboard, release announcement, vendor demo, or one anecdote as a reproducible user test or universal best practice',
    'Does not claim provider execution, image generation, or inspection of an output',
  ];
  if (!imageMappingCase) {
    fail('Missing S53 current named-image-model research fixture');
  } else {
    if (imageMappingCase.status !== 'planned' || imageMappingCase.research_expectation !== 'required') fail('S53 must remain a planned research-required behavior specification');
    if (imageMappingCase.context?.generator_family !== 'Qwen Image' || imageMappingCase.context?.requested_version !== '3.0') fail('S53 must distinguish the requested Qwen Image 3.0 version');
    if (imageMappingCase.context?.requested_surface !== 'not_named; consumer-facing product is the default') fail('S53 must preserve the default consumer-surface policy');
    if (imageMappingCase.expected_branch !== 'current_named_model_research_with_version_and_evidence_boundary') fail('S53 expected branch must retain currentness and evidence boundaries');
    for (const requiredCheck of requiredImageMappingChecks) {
      if (!imageMappingCase.checks?.includes(requiredCheck)) fail('S53 missing image-model research guard: ' + requiredCheck);
    }
    if (imageMappingCase.tool_state?.image_generation !== 'not_available' || imageMappingCase.tool_state?.external_provider_authorized !== false || imageMappingCase.tool_state?.uploads_authorized !== false) {
      fail('S53 must not authorize provider calls, uploads, or generation');
    }
  }
  const staticGateDecisions = new Map([
    ['S13', 'pass'],
    ['S27', 'rework'],
    ['S28', 'rework'],
    ['S29', 'rework'],
    ['S30', 'pass'],
    ['S31', 'pass'],
    ['S32', 'blocked'],
  ]);
  for (const [id, expectedDecision] of staticGateDecisions) {
    const item = cases.cases?.find(testCase => testCase.id === id);
    if (!item) {
      fail('Missing static anti-slop gate fixture coverage: ' + id);
      continue;
    }
    const gate = item.anti_slop_gate;
    if (!gate || gate.name !== 'static_direction_pre_prompt') {
      fail('Missing static anti-slop gate contract: ' + id);
      continue;
    }
    if (gate.decision !== expectedDecision) fail('Unexpected static anti-slop gate decision: ' + id);
    if (gate.final_prompt_permitted !== (expectedDecision === 'pass')) {
      fail('Static anti-slop gate result conflicts with prompt release: ' + id);
    }
    if (!Array.isArray(gate.evidence) || !gate.evidence.length) {
      fail('Static anti-slop gate fixture needs observable evidence: ' + id);
    }
    if (typeof gate.recheck_condition !== 'string' || !gate.recheck_condition.trim()) {
      fail('Static anti-slop gate fixture needs a recheck condition: ' + id);
    }
  }
  const conceptStateFixtures = new Map([
    ['S33', {status: 'needs_selection', action: 'request_one_route_selection'}],
    ['S34', {status: 'locked', action: 'adapt_layout_within_locked_mechanism'}],
    ['S35', {status: 'locked', action: 'ask_one_format_constraint_tradeoff'}],
  ]);
  for (const [id, expected] of conceptStateFixtures) {
    const item = cases.cases?.find(testCase => testCase.id === id);
    if (!item) {
      fail('Missing concept-state fixture coverage: ' + id);
      continue;
    }
    const state = item.context?.concept_state;
    if (!state || typeof state !== 'object' || Array.isArray(state)) {
      fail('Missing concept-state contract: ' + id);
      continue;
    }
    if (state.status !== expected.status) fail('Unexpected concept-state status: ' + id);
    if (item.concept_action !== expected.action) fail('Unexpected concept-state action: ' + id);
    if (expected.status === 'needs_selection') {
      if (state.lock !== null || !Array.isArray(state.candidates) || state.candidates.length < 2) {
        fail('Unresolved concept fixture must carry multiple candidates and no lock: ' + id);
      } else if (state.candidates.some(candidate => !candidate.premise || !candidate.mechanism)) {
        fail('Unresolved concept fixture needs premise and mechanism per candidate: ' + id);
      }
    } else {
      const lock = state.lock;
      if (!lock || !lock.premise || !lock.mechanism || !lock.distinctive_hook ||
          !Array.isArray(lock.allowed_adaptations) || !Array.isArray(lock.forbidden_substitutions)) {
        fail('Locked concept fixture needs a complete bounded lock: ' + id);
      }
    }
  }
  const deliverableProfileFixtures = new Map([
    ['S36', {profile: 'business_membership_card', action: 'create_card_concept_without_print_claim'}],
    ['S37', {profile: 'civic_social_political', action: 'ask_for_speaker_and_claim_source_or_omit_claim'}],
  ]);
  for (const [id, expected] of deliverableProfileFixtures) {
    const item = cases.cases?.find(testCase => testCase.id === id);
    if (!item) {
      fail('Missing static deliverable profile fixture coverage: ' + id);
      continue;
    }
    if (item.context?.deliverable_profile !== expected.profile) {
      fail('Unexpected static deliverable profile: ' + id);
    }
    if (item.profile_action !== expected.action) {
      fail('Unexpected static deliverable profile action: ' + id);
    }
    if (item.research_expectation !== 'required') {
      fail('Static deliverable profile fixture must retain its research requirement: ' + id);
    }
    if (id === 'S36') {
      const requiredCopy = [
        'Maja Nowak',
        'Kierowniczka studia',
        'Studio Rytm',
        '+48 600 123 456',
        'maja@example.test',
        'Karta członkowska · 2048',
      ];
      const requiredChecks = [
        'Treat the deliverable as a concept raster only; do not claim it is print-ready',
        'Use recognition then fast retrieval as the reading priority, with deliberate alignment and negative space',
        'Preserve every supplied name, role, organization, contact string and membership number exactly',
        'Do not invent a logo, QR destination, address, contact detail, member benefit or print specification',
        'Do not ask for printer specifications that are unnecessary for the requested concept raster',
      ];
      if (item.context?.production_intent !== 'concept_raster_only' ||
          item.context?.print_specification !== 'not requested' ||
          JSON.stringify(item.context?.approved_copy) !== JSON.stringify(requiredCopy) ||
          item.context?.supplied_mark !== 'none; user explicitly says not to add a logo' ||
          !Array.isArray(item.available_assets) || item.available_assets.length !== 0 ||
          !Array.isArray(item.checks) || requiredChecks.some(check => !item.checks.includes(check)) ||
          item.expected_branch !== 'business_card_concept_raster') {
        fail('Business-card fixture must separate concept raster, exact copy and print production: ' + id);
      }
    }
    if (id === 'S37') {
      const gate = item.source_gate;
      const requiredCopy = [
        'Konsultacje społeczne: Park Nadbrzeżny',
        '12 listopada · 18:00',
        'Dom Sąsiedzki',
      ];
      const requiredChecks = [
        'Identify the intended public understanding/action and the authorized speaker before finalizing the claim-bearing direction',
        'Do not present the unsupported 72% as verified or invent a source, organization, endorsement or documentary evidence',
        'Withhold the final prompt while the requested claim and speaker authority remain unresolved',
        'Ask one concise, targeted question that offers to supply the source and authorized speaker or omit the statistic',
        'Do not add legal-compliance claims or turn the design task into legal advice',
      ];
      if (item.context?.claim_source_status !== 'unknown' ||
          item.context?.speaker_authority_status !== 'unknown' ||
          item.context?.authorized_speaker !== null ||
          item.context?.position_status !== 'not supplied' ||
          item.context?.requested_unverified_claim !== '72% mieszkańców popiera projekt.' ||
          JSON.stringify(item.context?.approved_copy) !== JSON.stringify(requiredCopy) ||
          !gate || gate.decision !== 'blocked' || gate.final_prompt_permitted !== false ||
          !Array.isArray(gate.missing_evidence) ||
          !gate.missing_evidence.includes('claim source') ||
          !gate.missing_evidence.includes('authorized speaker or organization') ||
          !Array.isArray(item.checks) || requiredChecks.some(check => !item.checks.includes(check)) ||
          !Array.isArray(item.available_assets) || item.available_assets.length !== 0 ||
          item.expected_branch !== 'request_claim_source_and_speaker_before_final_prompt') {
        fail('Civic fixture must block an unsupported claim and unknown speaker: ' + id);
      }
    }
  }
  const identityViewFixture = cases.cases?.find(testCase => testCase.id === 'S38');
  const requiredIdentityViewOrder = [
    'neutral_front_master',
    'left_and_right_three_quarter',
    'profile_after_three_quarter_stability_when_needed',
    'neutral_full_body_when_needed',
    'restrained_expressions_when_needed',
    'controlled_wardrobe_or_grooming',
    'environment_light_or_treatment',
    'downstream_specific_anchor_when_needed',
  ];
  const identityChecks = [
    'Do not claim to have seen or compared either image; both are unavailable in this turn',
    'Keep the user-designated neutral front portrait as the only stated master and label its pixels unreviewed here',
    'Do not promote the user-described jaw-drift profile to a validated identity anchor',
    'Explain that dependent final prompts need the actual identity carrier and should follow staged view validation',
    'Place three-quarter validation before profiles; include full body and later changes only when the requested asset use needs them',
    'Limit initial validation to one major change axis at a time and return a failed view to the last accepted master',
    'Do not imply that repeated identity text or a seed guarantees continuity',
    'Offer one concise next step: attach the neutral master and candidate profile for actual review',
  ];
  if (!identityViewFixture) {
    fail('Missing staged identity-view validation fixture coverage: S38');
  } else {
    const identity = identityViewFixture.identity_validation;
    if (identityViewFixture.status !== 'planned' ||
        identityViewFixture.research_expectation !== 'not_applicable' ||
        identityViewFixture.research_exemption_reason !== 'missing_continuity_carrier' ||
        identityViewFixture.context?.identity_status !== 'original_fictional_adult' ||
        identityViewFixture.context?.user_designated_master?.accepted_in_project_by_user !== true ||
        identityViewFixture.context?.user_designated_master?.attached_in_this_turn !== false ||
        identityViewFixture.context?.profile_candidate?.attached_in_this_turn !== false ||
        identityViewFixture.context?.profile_candidate?.visual_review_status !== 'not_reviewed' ||
        identityViewFixture.context?.profile_candidate?.user_reported_issue !== 'jawline_differs_slightly' ||
        identity?.source_status !== 'user_designated_master_not_attached' ||
        identity?.candidate_status !== 'user_reported_drift_not_visually_reviewed' ||
        JSON.stringify(identity?.view_order) !== JSON.stringify(requiredIdentityViewOrder) ||
        identity?.stage_policy !== 'only_stages_required_for_the_asset_use' ||
        identity?.initial_major_change_axis_limit !== 1 ||
        identity?.anchor_promotion_requires !== 'actual_render_visually_reviewed_and_accepted_for_stated_use' ||
        identity?.failed_view_action !== 'return_to_last_accepted_master' ||
        identity?.dependent_prompt_pack !== 'hold_until_required_views_are_accepted' ||
        identity?.['text_or_seed_guarantees_identity'] !== false ||
        !Array.isArray(identityViewFixture.checks) || identityChecks.some(check => !identityViewFixture.checks.includes(check)) ||
        !Array.isArray(identityViewFixture.available_assets) || identityViewFixture.available_assets.length !== 0 ||
        identityViewFixture.tool_state?.mode !== 'textual_fixture_no_execution' ||
        identityViewFixture.tool_state?.image_generation !== 'not_available' ||
        identityViewFixture.tool_state?.external_provider_authorized !== false ||
        identityViewFixture.tool_state?.uploads_authorized !== false ||
        identityViewFixture.expected_branch !== 'plan_staged_validation_and_request_identity_assets_before_final_pack') {
      fail('Identity fixture must withhold the unreviewed profile and preserve staged validation: S38');
    }
  }
  const cameraReframingFixture = cases.cases?.find(testCase => testCase.id === 'S39');
  const reframingChecks = [
    'Do not claim to have seen or inspected an unattached source image',
    'Distinguish a camera viewpoint change from a crop or fixed-view recomposition',
    'Explain that a changed viewpoint can alter projection, parallax, occlusion, relative placement and crop; do not promise pixel-identical background from prompt prose',
    'Treat the requested left bottle surface as unknown because the source view is absent and no supporting view was supplied',
    'Preserve only user-declared invariants as requested locks; do not turn them into visually verified product evidence',
    'Withhold a final source-bound prompt and ask for the actual image or a bounded alternative that keeps the existing viewpoint/crop',
    'Do not claim exact camera degrees or successful reframing without an actual tool/render review',
    'Keep the next step concise and do not route this missing-input case to an external provider or upload',
  ];
  if (!cameraReframingFixture) {
    fail('Missing camera-reframing conflict fixture coverage: S39');
  } else {
    const reframing = cameraReframingFixture.reframing_contract;
    if (cameraReframingFixture.status !== 'planned' ||
        cameraReframingFixture.research_expectation !== 'not_applicable' ||
        cameraReframingFixture.research_exemption_reason !== 'missing_required_input' ||
        cameraReframingFixture.context?.deliverable_profile !== 'authored_photographic_still_reframe' ||
        cameraReframingFixture.context?.source_image_attached !== false ||
        cameraReframingFixture.context?.source_image_status !== 'user_described_but_not_available_for_visual_review' ||
        cameraReframingFixture.context?.requested_camera_change?.axis !== 'viewpoint_angle' ||
        cameraReframingFixture.context?.requested_camera_change?.purpose !== 'reveal the left side of the bottle' ||
        cameraReframingFixture.context?.user_requested_pixel_identical_background !== true ||
        cameraReframingFixture.context?.newly_visible_surface_evidence !== 'unknown; no source image or alternate view is available' ||
        reframing?.source_view_status !== 'described_not_attached' ||
        reframing?.camera_change_kind !== 'viewpoint_change_not_crop' ||
        JSON.stringify(reframing?.expected_spatial_effects) !== JSON.stringify(['projection', 'parallax', 'occlusion', 'relative_placement', 'crop']) ||
        JSON.stringify(reframing?.semantic_scene_anchors) !== JSON.stringify(['window', 'wooden_table']) ||
        reframing?.pixel_identical_background_guaranteed_by_prompt !== false ||
        reframing?.unknown_surface_may_be_invented_as_fact !== false ||
        reframing?.final_prompt_permitted !== false ||
        reframing?.next_action !== 'request_source_image_or_offer_keep_current_viewpoint' ||
        !Array.isArray(cameraReframingFixture.checks) || reframingChecks.some(check => !cameraReframingFixture.checks.includes(check)) ||
        !Array.isArray(cameraReframingFixture.available_assets) || cameraReframingFixture.available_assets.length !== 0 ||
        cameraReframingFixture.tool_state?.mode !== 'textual_fixture_no_execution' ||
        cameraReframingFixture.tool_state?.external_provider_authorized !== false ||
        cameraReframingFixture.tool_state?.uploads_authorized !== false ||
        cameraReframingFixture.expected_branch !== 'surface_viewpoint_and_pixel_continuity_conflict_then_request_source_or_bounded_alternative') {
      fail('Camera-reframing fixture must surface unknown geometry and withhold the source-bound prompt: S39');
    }
  }
  const independentSeriesFixture = cases.cases?.find(testCase => testCase.id === 'S40');
  const seriesChecks = [
    'Return exactly three separately numbered image prompts, not a grid, board, contact sheet, or extra variants',
    'Assign one distinct job to each requested image: hero, product-detail coverage, and in-use editorial context',
    'Choose coverage rather than inventing a time-based story progression',
    'Propose one coherent bottle design for this explicitly fictional subject and repeat its essential description in every standalone prompt without claiming it is verified product truth',
    'Carry the shared user-requested photographic thesis while keeping each image\'s composition and subject action distinct',
    'State that text-only continuity is approximate because no actual reference image is attached; do not claim strict identity',
    'Bind no nonexistent references and do not make each prompt depend on a previous prompt, seed, or unverified model memory',
    'Do not claim model-specific optimization, native batching, or shared state because no generator is selected',
    'Preserve the explicit no-logo and no-visible-copy requirement and do not invent product claims',
    'Treat the result as prompts only; do not claim images were generated or visually reviewed',
  ];
  if (!independentSeriesFixture) {
    fail('Missing independent still-series fixture coverage: S40');
  } else {
    const series = independentSeriesFixture.series_contract;
    if (independentSeriesFixture.status !== 'planned' ||
        independentSeriesFixture.research_expectation !== 'required' ||
        independentSeriesFixture.context?.deliverable_profile !== 'independent_still_editorial_series' ||
        independentSeriesFixture.context?.production_intent !== 'prompt_only' ||
        independentSeriesFixture.context?.requested_artifact !== 'three_separate_still_image_files' ||
        independentSeriesFixture.context?.campaign_format_adaptation !== false ||
        independentSeriesFixture.context?.time_based_story_sequence !== false ||
        independentSeriesFixture.context?.continuity_precision !== 'approximate_text_only_no_visual_carrier' ||
        independentSeriesFixture.context?.strict_photo_identity_required !== false ||
        independentSeriesFixture.context?.generator !== 'not selected' ||
        series?.artifact_type !== 'separate_still_image_files' ||
        series?.output_count !== 3 ||
        series?.coverage_or_progression !== 'coverage' ||
        JSON.stringify(series?.roles) !== JSON.stringify(['hero', 'product_detail', 'in_use_editorial']) ||
        !Array.isArray(series?.shared_visual_dna) || series.shared_visual_dna.length < 3 ||
        !Array.isArray(series?.allowed_variation) || !series.allowed_variation.length ||
        series?.anti_duplicate_required !== true ||
        JSON.stringify(series?.attached_reference_count_per_unit) !== JSON.stringify([0, 0, 0]) ||
        series?.standalone_prompt_count !== 3 ||
        series?.each_prompt_self_contained !== true ||
        series?.grid_or_board !== false ||
        series?.prompt_may_depend_on_prior_unit !== false ||
        series?.strict_continuity_claim !== false ||
        series?.native_batch_or_shared_memory_claim !== false ||
        !Array.isArray(independentSeriesFixture.checks) || seriesChecks.some(check => !independentSeriesFixture.checks.includes(check)) ||
        !Array.isArray(independentSeriesFixture.available_assets) || independentSeriesFixture.available_assets.length !== 0 ||
        independentSeriesFixture.tool_state?.mode !== 'textual_fixture_no_execution' ||
        independentSeriesFixture.tool_state?.external_provider_authorized !== false ||
        independentSeriesFixture.tool_state?.uploads_authorized !== false ||
        independentSeriesFixture.expected_branch !== 'produce_three_standalone_approximate_continuity_prompts') {
      fail('Independent still-series fixture must preserve exact separate outputs, distinct roles, standalone prompts, and honest continuity: S40');
    }
  }
  const backgroundReplacementFixture = cases.cases?.find(testCase => testCase.id === 'S41');
  const backgroundReplacementChecks = [
    'Treat the bottle image as a fictional source supplied only inside this synthetic fixture scenario, not as an image reviewed during fixture validation',
    'Keep subject geometry, pose, camera, crop, focus, product truth, exact label/copy and product-local SKU color protected',
    'Allow only relevant physical consequences of the new environment; do not treat secondary changes as blanket permission',
    'Fit the replacement background and support to the existing camera, horizon, perspective and scale rather than changing the camera',
    'Check support/contact, reflections/transmission, edge integration, color spill and background depth/processing only where applicable',
    'Do not claim a generated or visually reviewed render, pixel-identical locks, or guaranteed model success',
  ];
  const allowedBackgroundSecondaryChanges = [
    'new_environment_reflections_and_transmission',
    'contact_or_cast_shadow_on_replacement_support',
    'environmental_color_spill_if_materially_caused',
    'edge_integration',
    'background_perspective_scale_depth',
    'grain_or_processing_match_only_if_needed',
  ];
  const protectedBackgroundProperties = [
    'subject_geometry', 'pose', 'camera', 'crop', 'focus', 'product_truth',
    'exact_label_and_copy', 'product_local_sku_color',
  ];
  if (!backgroundReplacementFixture) {
    fail('Missing bounded background-replacement fixture coverage: S41');
  } else {
    const replacement = backgroundReplacementFixture.background_replacement_contract;
    if (backgroundReplacementFixture.status !== 'planned' ||
        backgroundReplacementFixture.research_expectation !== 'required' ||
        backgroundReplacementFixture.context?.deliverable_profile !== 'source_bound_background_replacement' ||
        backgroundReplacementFixture.context?.source_image_status !== 'synthetic_asset_supplied_in_fixture_scenario_only_not_reviewed_in_this_execution' ||
        JSON.stringify(replacement?.change_only) !== JSON.stringify(['background', 'support_surface']) ||
        !Array.isArray(replacement?.preserve_exactly) || protectedBackgroundProperties.some(property => !replacement.preserve_exactly.includes(property)) ||
        JSON.stringify(replacement?.allowed_secondary_changes) !== JSON.stringify(allowedBackgroundSecondaryChanges) ||
        replacement?.contradictory_lock !== false ||
        replacement?.final_prompt_permitted !== true ||
        !Array.isArray(backgroundReplacementFixture.checks) || backgroundReplacementChecks.some(check => !backgroundReplacementFixture.checks.includes(check)) ||
        !Array.isArray(backgroundReplacementFixture.available_assets) || backgroundReplacementFixture.available_assets.length !== 1 ||
        backgroundReplacementFixture.available_assets[0]?.availability !== 'supplied_in_fixture_scenario_only' ||
        backgroundReplacementFixture.available_assets[0]?.fictional !== true ||
        backgroundReplacementFixture.tool_state?.mode !== 'textual_fixture_no_execution' ||
        backgroundReplacementFixture.tool_state?.image_generation !== 'not_available' ||
        backgroundReplacementFixture.tool_state?.external_provider_authorized !== false ||
        backgroundReplacementFixture.tool_state?.uploads_authorized !== false ||
        backgroundReplacementFixture.expected_branch !== 'compile_bounded_background_replacement_prompt') {
      fail('Background-replacement fixture must preserve source truth and narrowly bound physical secondary changes: S41');
    }
  }
  const backgroundConflictFixture = cases.cases?.find(testCase => testCase.id === 'S42');
  const backgroundConflictChecks = [
    'Detect that the new environment conflicts with exact preservation of old-environment reflections and contact-shadow pixels',
    'Do not silently drop the new-environment integration requirement or the exact old-environment locks',
    'Withhold a contradictory final source-bound prompt until one trade-off is resolved',
    'Ask one focused question or offer bounded choices: allow only physically necessary new reflections/shadows, or keep the original environment',
    'Keep product geometry, pose, camera, crop, focus, label/copy and product truth protected in either option',
    'Do not claim the hypothetical source was actually reviewed or that a prompt guarantees pixel identity',
  ];
  const protectedConflictProperties = [
    'subject_geometry', 'pose', 'camera', 'crop', 'focus', 'product_truth',
    'exact_label_and_copy', 'old_environment_reflection_pixels', 'old_contact_shadow_pixels',
  ];
  if (!backgroundConflictFixture) {
    fail('Missing contradictory background-replacement fixture coverage: S42');
  } else {
    const conflict = backgroundConflictFixture.background_replacement_contract;
    if (backgroundConflictFixture.status !== 'planned' ||
        backgroundConflictFixture.research_expectation !== 'required' ||
        backgroundConflictFixture.context?.deliverable_profile !== 'source_bound_background_replacement' ||
        backgroundConflictFixture.context?.source_image_status !== 'synthetic_asset_supplied_in_fixture_scenario_only_not_reviewed_in_this_execution' ||
        JSON.stringify(conflict?.change_only) !== JSON.stringify(['background', 'support_surface']) ||
        !Array.isArray(conflict?.preserve_exactly) || protectedConflictProperties.some(property => !conflict.preserve_exactly.includes(property)) ||
        !Array.isArray(conflict?.allowed_secondary_changes) || conflict.allowed_secondary_changes.length !== 0 ||
        conflict?.contradictory_lock !== true ||
        conflict?.final_prompt_permitted !== false ||
        conflict?.next_action !== 'ask_one_tradeoff_or_offer_keep_original_environment' ||
        !Array.isArray(backgroundConflictFixture.checks) || backgroundConflictChecks.some(check => !backgroundConflictFixture.checks.includes(check)) ||
        !Array.isArray(backgroundConflictFixture.available_assets) || backgroundConflictFixture.available_assets.length !== 1 ||
        backgroundConflictFixture.available_assets[0]?.availability !== 'supplied_in_fixture_scenario_only' ||
        backgroundConflictFixture.available_assets[0]?.fictional !== true ||
        backgroundConflictFixture.tool_state?.mode !== 'textual_fixture_no_execution' ||
        backgroundConflictFixture.tool_state?.image_generation !== 'not_available' ||
        backgroundConflictFixture.tool_state?.external_provider_authorized !== false ||
        backgroundConflictFixture.tool_state?.uploads_authorized !== false ||
        backgroundConflictFixture.expected_branch !== 'ask_one_tradeoff_before_final_background_replacement_prompt') {
      fail('Conflicting background locks must block the final prompt until the user resolves a bounded trade-off: S42');
    }
  }
  const sequentialAssetFixture = cases.cases?.find(testCase => testCase.id === 'S43');
  const sequentialAssetChecks = [
    'Activate the separate-asset route only because the user explicitly requested separate assets',
    'Keep the user-stated explicit acceptance of background-v001 distinct from actual file availability; do not claim the image is attached, inspectable, or hashed in this execution',
    'Treat the texture correction as a new background-v002 candidate and preserve background-v001 as selected while the candidate is pending',
    'With no generated image returned, state that no image was generated or visually reviewed and do not ask whether to keep or change it yet',
    'Do not advance to the figure or overlay before exact-image acceptance or an explicit terminal omit, reject, or cancel decision',
    'Do not treat approval of the prompt or assistant QA as acceptance of the image',
    'Do not invent a file path, digest, ZIP, alpha result, assembled poster, or cross-chat memory',
  ];
  if (!sequentialAssetFixture) {
    fail('Missing sequential separate-asset review fixture: S43');
  } else {
    const sequence = sequentialAssetFixture.separate_asset_review_contract;
    const context = sequentialAssetFixture.context;
    if (sequentialAssetFixture.status !== 'planned' ||
        sequentialAssetFixture.research_expectation !== 'required' ||
        context?.deliverable_profile !== 'explicit_separate_static_assets' ||
        context?.production_intent !== 'correct_selected_asset_sequentially' ||
        JSON.stringify(context?.requested_asset_ids) !== JSON.stringify(['poster_background', 'foreground_figure', 'grain_overlay']) ||
        context?.current_asset_id !== 'poster_background' ||
        context?.user_stated_accepted_version_id !== 'background-v001' ||
        context?.acceptance_evidence_scope !== 'explicit_user_statement_in_hypothetical_prior_conversation_turn_only' ||
        context?.accepted_asset_file_status !== 'not_available_in_this_execution' ||
        context?.candidate_version_id !== 'background-v002' ||
        context?.candidate_status !== 'not_generated' ||
        context?.image_output_status !== 'not_returned' ||
        !sequence ||
        sequence.activation !== 'explicit_user_request_for_separate_assets' ||
        sequence.one_asset_at_a_time !== true ||
        sequence.maximum_open_candidates_for_current_asset !== 1 ||
        sequence.selected_version_while_candidate_pending !== context?.user_stated_accepted_version_id ||
        sequence.pending_candidate_version !== context?.candidate_version_id ||
        sequence.candidate_status !== 'not_generated' ||
        sequence.actual_image_returned !== false ||
        sequence.ask_keep_or_change_before_actual_image !== false ||
        sequence.prompt_acceptance_selects_candidate !== false ||
        sequence.assistant_qa_selects_candidate !== false ||
        sequence.exact_image_acceptance_required_to_select_candidate !== true ||
        sequence.advance_to_next_asset !== false ||
        sequence.advance_requires_exact_acceptance_or_explicit_terminal_decision !== true ||
        sequence.file_or_digest_claim_permitted !== false ||
        !Array.isArray(sequentialAssetFixture.checks) || sequentialAssetChecks.some(check => !sequentialAssetFixture.checks.includes(check)) ||
        !Array.isArray(sequentialAssetFixture.available_assets) || sequentialAssetFixture.available_assets.length !== 0 ||
        sequentialAssetFixture.tool_state?.mode !== 'textual_fixture_no_execution' ||
        sequentialAssetFixture.tool_state?.image_generation !== 'not_available' ||
        sequentialAssetFixture.tool_state?.web_search !== 'available_read_only' ||
        sequentialAssetFixture.tool_state?.external_provider_authorized !== false ||
        sequentialAssetFixture.tool_state?.uploads_authorized !== false ||
        sequentialAssetFixture.expected_branch !== 'hold_current_asset_without_fabricating_output_or_advancing') {
      fail('Sequential separate-asset fixture must preserve exact selection, version hold, truthful no-output state, and scope: S43');
    }
  }
  const dependencyFixtures = new Map([
    ['S48', {
      currentAsset: 'poster_figure',
      dependentAsset: 'poster_shadow',
      dependencyTarget: 'poster_figure',
      selectedDependentVersion: 'shadow-v001',
      independentVersions: { poster_background: 'background-v001' },
      independentAssets: ['poster_background'],
      relation: 'figure_pose_to_shadow_shape',
      branch: 'prepare_figure_only_hold_approved_shadow_and_background',
      action: 'prepare_figure_direction_only_preserve_shadow_and_background_reassess_relation_when_actual_assets_exist',
      requestTerms: ['poster_figure', 'shadow_v001', 'background_v001', 'nie chcę jej zmieniać bez osobnego uzgodnienia', 'bez promptu'],
      forbiddenAuthorizationTerms: ['wyrażam zgodę na zmianę shadow-v001'],
      requestAssetTerm: 'poster_figure',
      checks: [
        'Uses the separate-asset route only because the user explicitly requested separate assets',
        'Works on poster_figure only and does not silently revise shadow_v001',
        'Treats the supplied figure-to-shadow dependency as a reassessment trigger, not authority to edit the approved shadow',
        'Preserves the exact user-stated selected version shadow-v001 while any separate candidate is pending',
        'Preserves independent background_v001 without changing its approved state',
        'Preserves the exact selected independent version background-v001',
        'Explains that shadow relation reassessment requires the actual figure and shadow assets; with no files, it remains unassessed',
        'Obtains the user\'s explicit decision before preparing a candidate that changes the approved shadow, unless that exact change is already authorized',
        'Does not claim an image was generated, viewed, hashed, or saved',
      ],
    }],
    ['S49', {
      currentAsset: 'poster_background',
      dependentAsset: 'floor_reflection',
      dependencyTarget: 'poster_background',
      selectedDependentVersion: 'reflection-v001',
      independentVersions: { poster_title: 'title-v003' },
      independentAssets: ['poster_title'],
      relation: 'background_colour_to_reflection_colour_and_edge',
      branch: 'prepare_background_only_hold_approved_reflection_for_reassessment',
      action: 'prepare_background_direction_only_keep_reflection_selected_reassess_after_actual_candidate',
      requestTerms: ['poster_background', 'floor_reflection_v001', 'najpierw uzgodnij ją ze mną', 'bez promptu'],
      forbiddenAuthorizationTerms: ['wyrażam zgodę na zmianę floor_reflection_v001'],
      requestAssetTerm: 'poster_background',
      checks: [
        'Uses the separate-asset route only because the user explicitly requested separate layers',
        'Works on poster_background only and preserves the exact selected floor_reflection_v001',
        'Treats the background-to-reflection dependency as a reason to reassess after the background candidate, not automatic edit permission',
        'Preserves unrelated approved asset versions and does not promote a hypothetical candidate',
        'Preserves the exact selected independent version title-v003',
        'Does not claim to have assessed the visual relationship when the actual files are unavailable',
        'Before preparing any reflection candidate, obtains the user\'s explicit decision unless the exact change and scope have already been authorized',
        'Does not infer that a reflection change is necessary solely from the dependency edge',
        'Does not claim an image was generated, viewed, hashed, or saved',
      ],
    }],
  ]);
  for (const [id, expected] of dependencyFixtures) {
    const item = cases.cases?.find(testCase => testCase.id === id);
    if (!item) {
      fail('Missing approved-dependent-asset reassessment fixture: ' + id);
      continue;
    }
    const context = item.context ?? {};
    const contract = item.dependency_reassessment_contract ?? {};
    const edge = context.dependency_edges?.[0] ?? {};
    const request = item.user_request ?? '';
    const selectedVersions = context.selected_versions ?? {};
    const selectedDependent = selectedVersions[expected.dependentAsset];
    const currentSelected = selectedVersions[expected.currentAsset];
    const valid = item.status === 'planned' &&
      item.research_expectation === 'required' &&
      item.expected_branch === expected.branch &&
      context.deliverable_profile === 'explicit_separate_static_assets' &&
      context.current_asset_id === expected.currentAsset &&
      context.dependent_change_authorized === false &&
      context.approval_evidence_scope === 'user_supplied_plan_summary_only' &&
      context.asset_file_status === 'not_available_in_this_execution' &&
      context.requested_output === 'direction_only_no_prompt_no_generation' &&
      typeof currentSelected === 'string' &&
      typeof selectedDependent === 'string' &&
      Object.entries(expected.independentVersions).every(([assetId, version]) => selectedVersions[assetId] === version) &&
      edge.asset_id === expected.dependentAsset &&
      edge.depends_on === expected.dependencyTarget &&
      edge.approval_state === 'user_stated_approved' &&
      JSON.stringify(context.independent_asset_ids) === JSON.stringify(expected.independentAssets) &&
      contract.current_asset_id === expected.currentAsset &&
      contract.dependent_asset_id === expected.dependentAsset &&
      contract.relation_to_reassess === expected.relation &&
      contract.dependency_is_edit_permission === false &&
      contract.dependent_selected_version_while_pending === expected.selectedDependentVersion &&
      contract.dependent_selected_version_while_pending === selectedDependent &&
      JSON.stringify(contract.preserve_independent_asset_ids) === JSON.stringify(expected.independentAssets) &&
      contract.actual_assets_available === false &&
      contract.relationship_assessed === false &&
      contract.ask_or_obtain_explicit_decision_before_dependent_candidate === true &&
      contract.automatic_dependent_edit === false &&
      contract.automatic_generation === false &&
      contract.expected_action === expected.action &&
      expected.requestTerms.every(term => request.includes(term)) &&
      !expected.forbiddenAuthorizationTerms.some(term => request.toLocaleLowerCase().includes(term)) &&
      request.includes(expected.requestAssetTerm) &&
      item.checks?.length === expected.checks.length &&
      expected.checks.every(check => item.checks.includes(check)) &&
      Array.isArray(item.available_assets) && item.available_assets.length === 0 &&
      item.tool_state?.mode === 'textual_fixture_no_execution' &&
      item.tool_state?.image_generation === 'not_available' &&
      item.tool_state?.web_search === 'available_read_only' &&
      item.tool_state?.external_provider_authorized === false &&
      item.tool_state?.uploads_authorized === false;
    const duplicateCount = cases.cases.filter(testCase => testCase.id === id).length;
    if (!valid || duplicateCount !== 1) {
      fail('Approved-dependent-asset fixture must bind request, dependency, approval, preservation and no-edit rules: ' + id);
    }
  }
  const commercialCopyFixtures = new Map([
    ['S50', {
      mode: 'requested_distinct_routes',
      expectedBranch: 'write_three_distinct_supported_copy_candidates',
      requiredMechanisms: ['plain_offer', 'supported_objection_answer', 'tactile_scene'],
      requiredChecks: [
        'Binds the requested action and audience to the supplied workshop, offer facts, channel and stated beginner concern',
        'Returns exactly three short draft candidates using the specified distinct mechanisms: plain offer, supported objection answer and tactile scene',
        'Makes each candidate different in its strategic reason to matter, not just synonyms, tone or intensity',
        'Uses only supplied offer facts and does not invent price, address, deadline, scarcity, testimonial or guaranteed result',
        'Selects no winner on the user\'s behalf and marks all candidates unselected drafts',
        'Does not force a named sales framework, CTA, route label disclosure or image-generation prompt',
        'Does not claim to have researched, generated or visually reviewed an output',
      ],
    }],
    ['S51', {
      mode: 'unsupported_claim_fallback',
      expectedBranch: 'withhold_unsupported_claim_and_request_substantiation_or_alternative',
      requiredChecks: [
        'Distinguishes requested wording from evidence for the superiority and guaranteed-outcome claims',
        'Does not publish or strengthen the unsupported best-in-city or 100-percent-effect claims',
        'Names the exact missing substantiation and asks for a credible source or permission to omit the unsupported claims',
        'Does not invent a replacement efficacy, safety, qualification or customer-result claim',
        'Withholds final visible copy and any generator prompt while the unsupported claim remains unresolved',
        'Does not claim legal or regulatory clearance and does not claim research was performed',
        'Keeps the response concise rather than presenting a full strategy form',
      ],
    }],
    ['S52', {
      mode: 'locked_single_line_handoff',
      expectedBranch: 'handoff_single_exact_locked_line_without_variants',
      requiredChecks: [
        'Preserves the exact user-accepted string „Sobota z gliną” without adding punctuation or changing capitalization',
        'Returns exactly one visible text string and no alternative route or synonym',
        'Does not add an unrequested CTA, proof line, price, logo text or claim',
        'Treats wording as user-final and permits no copy rewrite; only handoff metadata may be added outside the string',
        'Does not force strategic exploration or a named copy framework for a settled exact-copy handoff',
        'Does not create an image-generation prompt or claim the poster was generated',
      ],
    }],
  ]);
  for (const [id, expected] of commercialCopyFixtures) {
    const item = cases.cases?.find(testCase => testCase.id === id);
    if (!item) {
      fail('Missing commercial-copy strategy and selection fixture: ' + id);
      continue;
    }
    const context = item.context ?? {};
    const contract = item.commercial_copy_contract ?? {};
    const request = item.user_request ?? '';
    let modeValid = false;
    if (id === 'S50') {
      const uniqueMechanisms = new Set(contract.route_mechanisms ?? []);
      modeValid = context.deliverable_profile === 'static_commercial_copy' &&
        context.channel === 'poster' && context.requested_candidate_count === 3 &&
        context.approved_copy === null && context.requested_output === 'copy_candidates_only_no_prompt' &&
        Array.isArray(context.product_or_offer_truth) && context.product_or_offer_truth.length >= 3 &&
        Array.isArray(context.proof_available) && context.proof_available.length > 0 &&
        typeof context.buyer_tension === 'string' && context.buyer_tension.length > 0 &&
        contract.candidate_count === 3 && uniqueMechanisms.size === 3 &&
        JSON.stringify(contract.route_mechanisms) === JSON.stringify(expected.requiredMechanisms) &&
        contract.selection_status === 'all_unselected_drafts' && contract.framework_required === false &&
        contract.unsupported_claims_allowed === false && contract.final_prompt_permitted === false &&
        request.includes('dokładnie trzy naprawdę różne hasła');
    } else if (id === 'S51') {
      modeValid = context.deliverable_profile === 'static_commercial_copy' &&
        context.channel === 'poster' && context.claim_substantiation === 'not_supplied' &&
        JSON.stringify(context.claims_under_review) === JSON.stringify(['best studio in the city', '100 percent effectiveness']) &&
        contract.evidence_available === false && contract.final_copy_permitted === false &&
        contract.final_prompt_permitted === false && contract.invented_replacement_claim_permitted === false &&
        contract.allowed_next_action === 'request_evidence_or_offer_to_omit_claim_without_substituting_new_fact' &&
        request.includes('Najlepsze studio w mieście, 100% skuteczności') &&
        request.includes('Nie mam teraz źródła');
    } else {
      modeValid = context.deliverable_profile === 'static_commercial_copy_handoff' &&
        context.copy_status === 'user_final_locked' && context.exact_locked_text === 'Sobota z gliną' &&
        context.requested_visible_string_count === 1 && context.copy_changes_authorized === false &&
        context.route_comparison_requested === false && context.generator_prompt_requested === false &&
        contract.requested_count === 1 && contract.exact_locked_text === 'Sobota z gliną' &&
        contract.copy_status === 'user_final_locked' && contract.may_rewrite === false &&
        contract.alternatives_permitted === false && contract.additional_visible_claims_permitted === false &&
        contract.framework_required === false && request.includes('dokładnie „Sobota z gliną”');
    }
    const valid = item.status === 'planned' && item.expected_branch === expected.expectedBranch &&
      item.research_expectation === (id === 'S52' ? 'not_applicable' : 'required') &&
      (id !== 'S52' || item.research_exemption_reason === 'mechanical_change_only') &&
      modeValid && Array.isArray(item.checks) && expected.requiredChecks.every(check => item.checks.includes(check)) &&
      Array.isArray(item.available_assets) && item.available_assets.length === 0 &&
      item.tool_state?.mode === 'textual_fixture_no_execution' &&
      item.tool_state?.image_generation === 'not_available' &&
      item.tool_state?.web_search === 'available_read_only' &&
      item.tool_state?.external_provider_authorized === false &&
      item.tool_state?.uploads_authorized === false &&
      item.available_assets.length === 0;
    const duplicateCount = cases.cases.filter(testCase => testCase.id === id).length;
    if (!valid || duplicateCount !== 1) {
      fail('Commercial-copy fixture must preserve route differentiation, evidence handling, exact-copy scope and no-tool boundaries: ' + id);
    }
  }
  const visualLabelFixtures = new Map([
    ['S44', {
      resolution: 'reversible_assumption',
      expectedBranch: 'give_one_reversible_premium_interpretation_without_prompt',
      requiredChecks: [
        'Interprets the broad premium label through specific, brief-grounded visual choices instead of copying luxury clichés',
        'States the choice as a reversible working assumption because the user explicitly invited one',
        'Does not ask a ceremonial clarification question or turn the assumption into approval or a project lock',
        'Does not infer unsupported product quality, price, provenance or brand status from the word premium',
        'Provides only one creative direction and no generator prompt, consistent with the requested stage',
      ],
    }],
    ['S45', {
      resolution: 'ask_single_material_question',
      expectedBranch: 'ask_one_period_question_before_direction',
      requiredChecks: [
        'Recognizes that the unresolved decade materially changes the historical language and concept',
        'Asks one concise choice about the intended decade instead of an intake questionnaire',
        'Does not silently blend the 1970s and 1990s or pick one without authorization',
        'Withholds a final creative direction and generator prompt that depend on the unanswered period',
        'Does not claim that retro is inherently invalid or unusable',
      ],
    }],
    ['S46', {
      resolution: 'preserve_coherent_user_requested_hybrid',
      expectedBranch: 'develop_coherent_hybrid_direction_without_forcing_choice',
      requiredChecks: [
        'Preserves the explicitly requested hybrid instead of forcing a single style label',
        'Assigns the grid a clear information and hierarchy role and the linocut-like treatment a distinct image-construction role',
        'Checks that the two roles support one communication purpose and readable event information',
        'Does not call the combination inherently incompatible or silently discard one component',
        'Does not claim actual linocut production, print separations or print readiness',
        'Returns a direction only and does not add an unrequested generator prompt',
      ],
    }],
    ['S47', {
      resolution: 'ask_one_organizing_question',
      expectedBranch: 'ask_one_organizing_question_before_direction',
      requiredChecks: [
        'Recognizes the unassigned equal-priority stack as an unresolved composition decision, not a finished art direction',
        'Asks one organizing question that distinguishes a deliberate visible collision from a coordinated system with assigned component roles',
        'Withholds the final direction and prompt until the organizing choice is resolved',
        'Does not silently flatten the labels into an effect pile, discard components or impose an arbitrary fixed style cap',
        'Does not claim the named categories are inherently incompatible',
      ],
    }],
  ]);
  for (const [id, expected] of visualLabelFixtures) {
    const item = cases.cases?.find(testCase => testCase.id === id);
    if (!item) {
      fail('Missing ambiguous-label and hybrid-resolution fixture: ' + id);
      continue;
    }
    const contract = item.visual_label_resolution_contract ?? {};
    const request = item.user_request ?? '';
    const context = item.context ?? {};
    const commonValid = item.status === 'planned' &&
      item.research_expectation === 'required' &&
      item.context?.deliverable_profile === 'static_poster_direction' &&
      item.tool_state?.mode === 'textual_fixture_no_execution' &&
      item.tool_state?.image_generation === 'not_available' &&
      item.tool_state?.web_search === 'available_read_only' &&
      item.tool_state?.external_provider_authorized === false &&
      item.tool_state?.uploads_authorized === false &&
      Array.isArray(item.available_assets) && item.available_assets.length === 0 &&
      item.expected_branch === expected.expectedBranch &&
      !!contract && contract.resolution === expected.resolution &&
      Array.isArray(item.checks) && expected.requiredChecks.every(check => item.checks.includes(check));
    let decisionValid = false;
    if (id === 'S44') {
      decisionValid = JSON.stringify(context.style_labels) === JSON.stringify(['premium']) &&
        context.user_authorized_provisional_interpretation === true &&
        context.requested_output === 'one_direction_only_no_prompt' &&
        request.includes('premium') &&
        request.includes('Możesz zaproponować roboczą interpretację bez dodatkowych pytań') &&
        request.includes('bez blokowania jej jako finalnej') &&
        request.includes('jeden kierunek, nie prompt') &&
        contract.material_ambiguity === false &&
        contract.context_resolves_enough_for_reversible_choice === true &&
        contract.user_authorizes_provisional_choice === true &&
        contract.direction_permitted === true && contract.final_prompt_permitted === false &&
        contract.question_required === false && contract.project_lock_created === false &&
        contract.unsupported_claims_inferred === false &&
        contract.expected_action === 'offer_one_tentative_brief_specific_direction_without_question_or_lock';
    } else if (id === 'S45') {
      decisionValid = JSON.stringify(context.period_candidates) === JSON.stringify(['1970s', '1990s']) &&
        context.style_label === 'retro' &&
        context.selected_period === null &&
        request.includes('lat 70. albo 90.') &&
        request.includes('jeszcze nie wybrałem') &&
        request.includes('zanim zdecydujemy o okresie') &&
        JSON.stringify(contract.candidate_periods) === JSON.stringify(['1970s', '1990s']) &&
        contract.material_ambiguity === true &&
        contract.context_resolves_enough_for_reversible_choice === false &&
        contract.user_authorizes_provisional_choice === false &&
        contract.direction_permitted === false && contract.final_prompt_permitted === false &&
        contract.question_required === true &&
        contract.question_target === 'choose_1970s_or_1990s_visual_period' &&
        contract.blend_candidates_without_selection === false &&
        contract.expected_action === 'ask_which_period_before_direction_or_prompt';
    } else if (id === 'S46') {
      const roles = contract.components;
      const requestedRoles = context.style_components;
      decisionValid = context.user_explicitly_requested_hybrid === true &&
        context.requested_output === 'one_direction_only_no_prompt' &&
        request.includes('siatka inspirowana stylem szwajcarskim') &&
        request.includes('tytuł, datę i informacje') &&
        request.includes('ilustracja wycięta w linoleum') &&
        Array.isArray(requestedRoles) && requestedRoles.length === 2 &&
        requestedRoles[0]?.label === 'Swiss-inspired grid' &&
        requestedRoles[0]?.role === 'organize_title_date_and_event_facts' &&
        requestedRoles[1]?.label === 'linocut-like botanical illustration' &&
        requestedRoles[1]?.role === 'central_image' &&
        Array.isArray(roles) && roles.length === 2 &&
        roles[0]?.label === 'Swiss-inspired grid' && roles[0]?.role === 'organize_title_date_and_event_facts' &&
        roles[1]?.label === 'linocut-like botanical illustration' && roles[1]?.role === 'central_image' &&
        contract.roles_distinct_and_coherent === true &&
        contract.user_explicitly_requested_hybrid === true &&
        contract.direction_permitted === true && contract.final_prompt_permitted === false &&
        contract.question_required === false && contract.hybrid_rejected_as_incompatible === false &&
        contract.physical_print_claim_permitted === false &&
        contract.expected_action === 'describe_both_roles_in_one_coherent_direction_without_print_claim';
    } else {
      decisionValid = JSON.stringify(context.style_labels) === JSON.stringify(['Swiss', 'cyberpunk', 'glassmorphism', 'Victorian', 'risograph']) &&
        context.priority === 'all_equal' && context.component_roles === null &&
        context.user_authorized_provisional_choice === false &&
        ['szwajcarskimi', 'cyberpunkowymi', 'glassmorphism', 'wiktoriańskimi', 'risograph'].every(label => request.includes(label)) &&
        request.includes('Wszystko jest równie ważne') &&
        request.includes('nie mam przypisanych ról') &&
        JSON.stringify(contract.unassigned_labels) === JSON.stringify(['Swiss', 'cyberpunk', 'glassmorphism', 'Victorian', 'risograph']) &&
        contract.roles_assigned === false && contract.equal_priority === true &&
        contract.material_ambiguity === true && contract.question_required === true &&
        contract.question_target === 'deliberate_visible_collision_or_coordinated_system_with_assigned_component_roles' &&
        contract.direction_permitted === false && contract.final_prompt_permitted === false &&
        contract.silently_flatten_or_discard_permitted === false &&
        contract.inherent_incompatibility_claim_permitted === false &&
        contract.fixed_style_cap_added === false &&
        contract.expected_action === 'ask_one_organizing_question_and_withhold_direction';
    }
    if (!commonValid || !decisionValid) {
      fail('Visual-label fixture must enforce its planned reversible-choice, material-question, or coherent-hybrid contract: ' + id);
    }
  }
  const videoCases = json('evals/video-cases.json');
  if (videoCases.schema_version !== 1) fail('Video behavior fixtures require schema version 1');
  const videoIds = new Set();
  for (const item of videoCases.cases ?? []) {
    if (!item.id || videoIds.has(item.id)) fail('Duplicate or missing video eval ID');
    videoIds.add(item.id);
    if (!item.user_request || !Array.isArray(item.checks) || !item.checks.length) fail('Incomplete video eval: ' + item.id);
    for (const field of ['context', 'tool_state']) {
      if (!item[field] || typeof item[field] !== 'object' || Array.isArray(item[field])) fail('Missing video eval context/state: ' + item.id + '.' + field);
    }
    if (!Array.isArray(item.available_assets)) fail('Missing video eval asset inventory: ' + item.id);
    if (typeof item.expected_branch !== 'string' || !item.expected_branch.trim()) fail('Missing video eval expected branch: ' + item.id);
    validateResearchExpectation(item, item.id);
    if (item.status !== 'planned') fail('Video fixture must not predeclare behavior PASS: ' + item.id);
  }
  const requiredCorrectionLoopChecks = new Map([
    ['V14', ['Makes one correction only: replaces the orbit with a locked or shallow lateral camera path that keeps the repair visible', 'Defines an observable acceptance test: repair remains unobstructed and legible for at least two seconds without changing the product or adding spectacle']],
    ['V15', ['Does not respond by endlessly accumulating negative constraints', 'Proposes one structural change, such as splitting the sequence or supplying an exact approved carrier frame, subject to verified generator capability']],
  ]);
  for (const [id, checks] of requiredCorrectionLoopChecks) {
    const fixture = videoCases.cases.find(item => item.id === id);
    if (!fixture) {
      fail('Missing video workflow or anti-slop correction-loop regression cases: ' + id);
      continue;
    }
    for (const check of checks) {
      if (!fixture.checks?.includes(check)) fail('Video anti-slop correction-loop fixture missing required check: ' + id + ' -> ' + check);
    }
  }
  const requiredMusicVideoIds = ['MV01', 'MV02', 'MV03', 'MV04'];
  const musicVideoCases = (videoCases.cases ?? []).filter(item => requiredMusicVideoIds.includes(item.id));
  if (JSON.stringify(musicVideoCases.map(item => item.id).sort()) !== JSON.stringify(requiredMusicVideoIds)) {
    fail('Music-video direction fixtures must contain MV01-MV04');
  }
  const requiredMusicVideoChecks = new Map([
    ['MV01', ['Does not claim to have listened to or analysed unattached audio', 'Does not invent exact timecodes or a verified song-section map']],
    ['MV02', ["Preserves the user's deliberate sustained or hypnotic form", 'Does not force escalation, contrast, chorus payoff or catharsis']],
    ['MV03', ['Routes song/persona direction before requested sequence and generator-aware prompting', 'Leaves current model/surface research to video-prompt-architect and does not execute generation']],
    ['MV04', ['Preserves explicit accepted persona/reference locks', 'Changes the rejected central device at its cause and gives one observable retest']],
  ]);
  for (const [id, checks] of requiredMusicVideoChecks) {
    const fixture = musicVideoCases.find(item => item.id === id);
    if (!fixture) continue;
    if (!Array.isArray(fixture.dimensions) || !fixture.dimensions.includes('music_video_direction')) fail('Music-video fixture must declare its responsibility: ' + id);
    for (const check of checks) {
      if (!fixture.checks?.includes(check)) fail('Music-video fixture missing required check: ' + id + ' -> ' + check);
    }
  }
  const producerCases = json('evals/producer-cases.json');
  if (producerCases.schema_version !== 1) fail('Producer task fixtures require schema version 1');
  if (!producerCases.scope?.includes('not evaluated model responses')) fail('Producer fixture scope must distinguish planned cases from behavior results');
  const producerIds = new Set();
  for (const item of producerCases.cases ?? []) {
    if (!item.id || producerIds.has(item.id)) fail('Duplicate or missing producer eval ID');
    producerIds.add(item.id);
    if (!item.user_request || !Array.isArray(item.checks) || !item.checks.length) fail('Incomplete producer eval: ' + item.id);
    for (const field of ['context', 'tool_state']) {
      if (!item[field] || typeof item[field] !== 'object' || Array.isArray(item[field])) fail('Missing producer eval context/state: ' + item.id + '.' + field);
    }
    if (!Array.isArray(item.available_assets)) fail('Missing producer eval asset inventory: ' + item.id);
    if (typeof item.expected_branch !== 'string' || !item.expected_branch.trim()) fail('Missing producer eval expected branch: ' + item.id);
    validateResearchExpectation(item, item.id);
    if (item.status !== 'planned') fail('Producer fixture must not predeclare behavior PASS: ' + item.id);
    if (item.tool_state?.music_generation !== undefined && item.tool_state.music_generation !== 'not_available') fail('Producer fixture cannot claim music-generation availability: ' + item.id);
    if (item.tool_state?.video_generation !== undefined && item.tool_state.video_generation !== 'not_available') fail('Producer fixture cannot claim video-generation availability: ' + item.id);
    if (item.tool_state?.audio_analysis !== undefined && item.tool_state.audio_analysis !== 'not_available') fail('Producer fixture cannot claim audio-analysis availability: ' + item.id);
    if (item.tool_state?.external_provider_authorized !== false) fail('Producer fixture must not authorize an external provider: ' + item.id);
    if (item.tool_state?.uploads_authorized !== false) fail('Producer fixture must not authorize uploads: ' + item.id);
  }
  const requiredProducerIds = ['PA01', 'PA02', 'PA03', 'PA04', 'PA05', 'PA06', 'PA07'];
  if (JSON.stringify(Array.from(producerIds).sort()) !== JSON.stringify(requiredProducerIds)) fail('Producer task fixtures must contain exactly PA01-PA07');
  const syncFixture = producerCases.cases?.find(fixture => fixture.id === 'PA07');
  if (syncFixture && syncFixture.context?.exact_sync_requirement !== 'hard_requirement') fail('Producer PA07 must preserve exact synchronization as a hard requirement when requested');
  if (syncFixture && syncFixture.context?.exact_sync_capability !== 'unknown_not_verified') fail('Producer PA07 must not treat the unverified exact-sync capability as available');
  if (syncFixture && !syncFixture.expected_branch?.includes('block_exact_sync_prompt_until_matching_capability_is_verified')) fail('Producer PA07 must block exact-sync prompt until its required capability is verified');
  for (const [id, checks] of new Map([
    ['PA01', ['Produces a complete copy-ready song task packet rather than a loose collection of adjectives', 'Includes at least one observable listening acceptance test']],
    ['PA02', ['Marks the exact video model unknown if official current evidence does not resolve it', 'Does not hard-code a specific Veo or Gemini model version without current evidence']],
    ['PA03', ['Asks no more than one or two high-value questions, preferably in a single concise turn']],
    ['PA04', ["Respects the user's explicit prohibition on web research", 'Does not present the newest model, current limits, pricing or availability as verified facts']],
    ['PA05', ['Does not log in, invoke a provider, generate audio or upload a file', 'Does not imply any audio file exists or that an operation was attempted']],
    ['PA06', ['Routes a direction-only request to creative-music-video-director', 'Does not emit an execution packet, generator prompt or shot sequence the user did not request']],
    ['PA07', ['Preserves the user-approved lyric wording verbatim in its own labeled block', 'Treats user-declared lyric authorship as supplied context rather than legal clearance and does not invent rights or consent', 'Distinguishes visible singing from exact phoneme-level synchronization and does not promise exact lip sync', 'Withholds an exact-sync prompt until a matching capability is verified and offers a best-effort alternative only after the user accepts a downgrade', 'Does not claim to have analysed audio/video when no result is attached and no analysis capability is available', 'Provides one bounded repair change and one retest for a future actual render without diagnosing an absent output']],
  ])) {
    const item = producerCases.cases?.find(fixture => fixture.id === id);
    if (!item) continue;
    for (const check of checks) {
      if (!item.checks?.includes(check)) fail('Producer fixture missing required check: ' + id + ' -> ' + check);
    }
  }
  const campaignCases = json('evals/campaign-cases.json');
  if (campaignCases.schema_version !== 1) fail('Campaign-direction fixtures require schema version 1');
  if (!campaignCases.scope?.includes('not an evaluated model response')) fail('Campaign fixture scope must distinguish planned cases from behavior results');
  const campaignIds = new Set();
  const campaignDimensions = new Set();
  for (const item of campaignCases.cases ?? []) {
    if (!item.id || campaignIds.has(item.id)) fail('Duplicate or missing campaign eval ID');
    campaignIds.add(item.id);
    if (!item.user_request || !Array.isArray(item.checks) || !item.checks.length) fail('Incomplete campaign eval: ' + item.id);
    for (const field of ['context', 'tool_state']) {
      if (!item[field] || typeof item[field] !== 'object' || Array.isArray(item[field])) fail('Missing campaign eval context/state: ' + item.id + '.' + field);
    }
    if (!Array.isArray(item.available_assets)) fail('Missing campaign eval asset inventory: ' + item.id);
    if (typeof item.expected_branch !== 'string' || !item.expected_branch.trim()) fail('Missing campaign eval expected branch: ' + item.id);
    validateResearchExpectation(item, item.id);
    if (item.status !== 'planned') fail('Campaign fixture must not predeclare behavior PASS: ' + item.id);
    for (const dimension of item.dimensions ?? []) campaignDimensions.add(dimension);
  }
  const requiredCampaignIds = Array.from({length: 10}, (_, index) => 'M' + String(index + 1).padStart(2, '0'));
  if (JSON.stringify(Array.from(campaignIds).sort()) !== JSON.stringify(requiredCampaignIds)) fail('Campaign fixtures must contain exactly M01-M10');
  const campaignCase = id => (campaignCases.cases ?? []).find(item => item.id === id);
  const hasCampaignCheck = (id, requiredCheck) => campaignCase(id)?.checks?.includes(requiredCheck) === true;
  if (!hasCampaignCheck('M08', 'Routes the song-centered brief to the dedicated music-video direction owner')) {
    fail('Campaign M08 must route a song-centered video to the dedicated music-video owner');
  }
  if (!hasCampaignCheck('M02', 'Does not promise or imply viral reach or sales performance')) {
    fail('Campaign M02 must explicitly guard against viral reach and sales performance promises');
  }
  if (!hasCampaignCheck('M10', 'Repairs one primary issue and names an observable retest before a final handoff')) {
    fail('Campaign M10 must require one primary repair and an observable retest');
  }
  if (!hasCampaignCheck('M10', 'Withholds final direction and handoff until all material gate items pass')) {
    fail('Campaign M10 must withhold final direction and handoff until material gates pass');
  }
  for (const dimension of ['multi_asset_roles', 'recomposition', 'exact_copy', 'platform_research', 'anti_generic_rework', 'no_performance_promise', 'deep_mode', 'truth_boundary', 'handoff']) {
    if (!campaignDimensions.has(dimension)) fail('Missing campaign fixture coverage: ' + dimension);
  }
  const storyCases = json('evals/story-cases.json');
  if (storyCases.schema_version !== 1) fail('Story behavior fixtures require schema version 1');
  const storyIds = new Set();
  for (const item of storyCases.cases ?? []) {
    if (!item.id || storyIds.has(item.id)) fail('Duplicate or missing story eval ID');
    storyIds.add(item.id);
    if (!item.user_request || !Array.isArray(item.checks) || !item.checks.length) fail('Incomplete story eval: ' + item.id);
    for (const field of ['context', 'tool_state']) {
      if (!item[field] || typeof item[field] !== 'object' || Array.isArray(item[field])) fail('Missing story eval context/state: ' + item.id + '.' + field);
    }
    if (!Array.isArray(item.available_assets)) fail('Missing story eval asset inventory: ' + item.id);
    if (typeof item.expected_branch !== 'string' || !item.expected_branch.trim()) fail('Missing story eval expected branch: ' + item.id);
    validateResearchExpectation(item, item.id);
    if (item.status !== 'planned') fail('Story fixture must not predeclare behavior PASS: ' + item.id);
  }
  if (storyIds.size < 10) fail('Missing screenplay/story development regression cases');
  const storyboardCases = json('evals/storyboard-cases.json');
  if (storyboardCases.schema_version !== 1) fail('Storyboard behavior fixtures require schema version 1');
  const storyboardIds = new Set();
  const storyboardDimensions = new Set();
  for (const item of storyboardCases.cases ?? []) {
    if (!item.id || storyboardIds.has(item.id)) fail('Duplicate or missing storyboard eval ID');
    storyboardIds.add(item.id);
    if (!item.user_request || !Array.isArray(item.checks) || !item.checks.length) fail('Incomplete storyboard eval: ' + item.id);
    for (const field of ['context', 'tool_state']) {
      if (!item[field] || typeof item[field] !== 'object' || Array.isArray(item[field])) fail('Missing storyboard eval context/state: ' + item.id + '.' + field);
    }
    if (!Array.isArray(item.available_assets)) fail('Missing storyboard eval asset inventory: ' + item.id);
    if (typeof item.expected_branch !== 'string' || !item.expected_branch.trim()) fail('Missing storyboard eval expected branch: ' + item.id);
    validateResearchExpectation(item, item.id);
    if (item.status !== 'planned') fail('Storyboard fixture must not predeclare behavior PASS: ' + item.id);
    if (!Array.isArray(item.dimensions) || !item.dimensions.length) fail('Missing storyboard eval dimensions: ' + item.id);
    for (const dimension of item.dimensions ?? []) storyboardDimensions.add(dimension);
  }
  const requiredStoryboardIds = Array.from({length: 15}, (_, index) => 'SB' + String(index + 1).padStart(2, '0'));
  if (JSON.stringify(Array.from(storyboardIds).sort()) !== JSON.stringify(requiredStoryboardIds)) fail('Storyboard fixtures must contain exactly SB01-SB15');
  for (const dimension of ['sequence_only', 'timing_estimate', 'board_only', 'exact_copy', 'reference_roles', 'property_authority_conflict', 'sequence_board_separation', 'strict_missing_carrier', 'continuity', 'board_not_carrier', 'aspect_nondefault', 'handoff', 'screen_direction', 'no_generation_without_tool', 'safe_zones', 'camera_feasibility', 'generator_handoff']) {
    if (!storyboardDimensions.has(dimension)) fail('Missing storyboard fixture coverage: ' + dimension);
  }
  if (!storyboardCases.scope?.includes('behavior-quality PASS')) fail('Storyboard fixture scope must state that planned cases are not behavior PASS records');
  return {
    status: errors.length ? 'FAIL' : 'PASS',
    scope: 'structural validation only; not host behavior or creative quality',
    skills: actualSkills.length, references, runtime_bytes: runtimeBytes,
    regression_fixtures: ids.size, video_fixtures: videoIds.size, campaign_fixtures: campaignIds.size, story_fixtures: storyIds.size,
    storyboard_fixtures: storyboardIds.size, producer_fixtures: producerIds.size, files: files.length, errors,
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const result = validatePackage(root);
  console.log(JSON.stringify(result, null, 2));
  if (result.errors.length) process.exitCode = 1;
}
