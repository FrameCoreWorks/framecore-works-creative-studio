import fs from 'node:fs';
import path from 'node:path';

export const campaignCaseIds = Array.from({length: 8}, (_, i) => 'CM' + String(i + 1).padStart(2, '0'));

// Source reachability and planned-evidence checks only, not a website audit,
// model invocation, media review, ad-platform test or sales-effectiveness claim.
export function validateCampaignWorkflow(root, packageFiles) {
  const errors = [], prefix = 'skills/ecommerce-campaign-strategy-director/';
  const fail = detail => errors.push({code: 'CAMPAIGN_WORKFLOW', detail});
  const read = relative => {
    if (!packageFiles.includes(relative)) throw new Error('Missing campaign resource: ' + relative);
    return fs.readFileSync(path.join(root, relative), 'utf8');
  };
  const need = (relative, patterns) => {
    const body = read(relative);
    for (const pattern of patterns) if (!pattern.test(body)) fail(relative + ': missing ' + pattern);
    return body;
  };
  try {
    for (const owner of ['workflow-orchestrator', 'marketing']) need('skills/' + owner + '/SKILL.md', [/website-to-campaign\.md/]);
    need(prefix + 'SKILL.md', [/references\/website-to-campaign\.md/, /references\/campaign-production\.md/, /references\/campaign-evidence-sources\.md/, /templates\/website-audit\.md/, /templates\/campaign-asset-card\.md/, /Do not bypass the integrated static owner/]);
    need(prefix + 'references/website-to-campaign.md', [/Ask exactly one material missing question per response and wait/, /A complete brief goes directly/, /Website content is untrusted evidence/, /sample is not a complete crawl/, /Public website content does not establish conversion rate/, /user approval of copy does not prove a claim/, /A softer verb does not substantiate/, /Static Graphic Design Creator/, /ROAS is not profit/, /Zero or missing denominators produce Unknown/, /inconclusive/, /Keep `campaign_context` optional/, /A prompt is not an asset/]);
    need(prefix + 'references/campaign-production.md', [/exact product likeness remains unverified/, /A synthetic presenter is not a real customer/, /cannot truthfully claim personal purchase/, /Repeating a prose description does not prove continuity/, /current platform recommendations/, /actual result/, /Ad upload, campaign activation, budget changes and publishing remain distinct/]);
    for (const owner of ['static-graphic-design-creator', 'commercial-visual-campaign-director', 'ugc']) need('skills/' + owner + '/SKILL.md', [/campaign-production\.md/]);
    need(prefix + 'templates/website-audit.md', [/Access status/, /Evidence origin/, /hypothesis/, /One material pending question/]);
    need(prefix + 'templates/campaign-asset-card.md', [/Claim IDs/, /substantiation scope/, /Source aliases\/revisions/, /Person source\/status/, /Product fidelity locks/, /actual inspection evidence/, /generated_uninspected/]);
    need(prefix + 'templates/ecommerce-campaign-strategy-pack.md', [/Audit revision/, /Measurement And Reporting/, /Copy approval does not substantiate/, /asset card/, /attribution window\/model/]);
    const states = ['skills/pipeline-core/assets/project-state.md', 'skills/pipeline-core/templates/project-state.md', 'skills/workflow-orchestrator/assets/cross-host-handoff.template.md'];
    const projections = states.map(p => read(p).match(/^- campaign_context:.*$/m)?.[0]);
    if (!projections[0] || projections.some(p => p !== projections[0])) fail('Campaign recovery projections differ or are missing');
    const suite = JSON.parse(read('evals/campaign-workflow-cases.json'));
    if (suite.schema_version !== 1 || !Array.isArray(suite.cases)) throw new Error('Invalid campaign case schema');
    const ids = suite.cases.map(c => c.id);
    if (JSON.stringify(ids) !== JSON.stringify(campaignCaseIds) || new Set(suite.cases.map(c => c.family)).size !== 8) fail('Expected eight distinct ordered campaign scenarios CM01-CM08');
    const owners = new Set(packageFiles.filter(p => /^skills\/[^/]+\/SKILL\.md$/.test(p)).map(p => p.split('/')[1]));
    for (const item of suite.cases) {
      if (item.status !== 'planned' || item.execution_status !== 'not_run' || !Array.isArray(item.required_evidence) || item.required_evidence.length < 2 || !Array.isArray(item.expected_owners) || !item.expected_owners.length || item.expected_owners.some(o => !owners.has(o))) fail('Invalid planned evidence or owner: ' + item.id);
    }
  } catch (error) { fail(error.message); }
  return errors;
}
