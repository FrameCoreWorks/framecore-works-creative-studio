# Provider setup and host boundaries

Use for installation onboarding, choosing an additional provider, explaining subscriptions, or diagnosing a missing connector. Load [the dated catalog](../assets/provider-catalog.json), [source evidence](provider-sources.md), and the user-facing [setup guide](../../../docs/provider-setup-guide.md) only when relevant. This is routing knowledge, not an installed integration or a live entitlement database.

## Resolve the surface before the service

Keep five routes distinct: `native_app`, `custom_mcp`, `cli`, `direct_api`, and `manual_web`. A host-native generator is a sixth, independent route: `host_builtin`. A service can support several routes with different authentication, operations, inputs and billing. A plugin packages instructions and possibly connected apps; an app supplies specific actions; MCP is a protocol; an API or CLI is not automatically a ChatGPT app.

Identify ChatGPT Chat, ChatGPT Work, Codex desktop/task view, Codex CLI or IDE extension from observed host information; otherwise record `Unknown`. Inspect available tools and current provider documentation. Do not assert that ChatGPT is limited to directory apps, that Codex is limited to APIs, or that all Codex clients support the same plugins. Do not install a local CLI in a temporary Work shell and present it as a durable phone integration. A reachable custom MCP endpoint is only usable when that host exposes the supported setup, authentication and permissions.

Treat the catalog as a dated shortlist. Before recommending installation, search the active plugin directory by the exact provider name when discovery is available. Negative search results are not proof of nonexistence: fal was documented and exposed in the authoring session despite an empty exact-name search. Prefer current directory results and official provider setup instructions; do not infer global or mobile availability from one Work session. More entries may exist in the directory.

## Optional installation question

Complete the already authorized Studio installation first. Then offer one optional question, in the user's language, without blocking successful installation or repeating existing answers:

> Czy chcesz teraz dobrać narzędzia do generowania? Możesz wskazać posiadane konta i wybrać gotowy plugin, konfigurację API/MCP/CLI w obsługiwanym środowisku albo pracę bez dodatkowych integracji. Możesz też pominąć ten krok.

Do not ask for a key, balance, login or plan merely to install Studio. If the user skips or does not answer, finish in prompt/planning mode with no provider setup. If the user asks for advice, present at most three suitable services with route, account requirement, billing basis, evidence and unresolved fields. Use Replit for websites/apps, not as a presumed video renderer. Offer a setup guide before any separately requested connection. Do not turn selection of a preferred provider into installation, authorization, spending or an upload.

On updates, preserve the user's selections and permissions. Offer setup again only if requested, a chosen route is blocked, or a relevant host/provider fact changed. Keep preferences private and editable; the catalog must never contain one user's installed apps, account details, credit balance or consent history.

## Verify separate facts

For each chosen route track independently: publicly documented, found in this host, installed, selected for this conversation, account authorized, billing checked, operation schema available, and this task authorized. Each fact is `confirmed`, `not_confirmed`, `blocked`, `not_applicable` or `Unknown`, with dated evidence. Visible tool metadata is evidence of a declared operation, not a successful provider call. A paid plan is not permission to run anything.

Use [the connection-profile template](../assets/provider-profile.template.json) only for requested private persistence or a handoff. Defaults carry no authorization. Do not automatically copy preferences or credentials between hosts, accounts or projects. Store only non-secret route preferences and verification status, never tokens, key values, balances, signed URLs or client assets in shared plugin files.

## Billing and conflicts

Read billing for the exact route. Higgsfield's ChatGPT plugin, MCP and CLI use the consumer-account route; Open Higgsfield at `open.higgsfield.ai` is the separate API route. API access does not establish consumer-plan entitlement or vice versa. Similar names at other domains or GitHub repositories are separate projects; resolve their exact identity before discussing installation.

The older Higgsfield help article requires a paid subscription and says external generations always consume credits; the observed tool contracts also expose trial/free allowances, audio and website actions. Report this conflict. Do not guarantee either unlimited use or universal unavailability. Only an authorized live entitlement read and the specific operation's schema can resolve a user's actual case. Do not activate a trial or auto-refill to verify access.

For fal, distinguish OAuth account selection from the account encoded in an API key, and distinguish inference MCP from Platform MCP. A model sold by fal is not proof that the original model vendor has a ChatGPT app. Never promise transferable credits or equal catalogs across routes without evidence. Prices, plan thresholds, durations, model names and quotas must be refreshed for the intended operation; a saved table is not a quote.

## Safe setup and execution handoff

Follow the user's actual setup authorization and current host workflow. OAuth/login occurs in the supported provider flow. For API work, use a secret manager or private local environment configuration; do not request pasted keys or put secrets into prompts, code, Git, plugin archives or screenshots. Review exact official endpoints/package identities before configuring them. Preserve unrelated configuration and existing connections.

Verify setup using an authorized, non-generating read when available. The read proves only what it returns. Do not test a connection with a paid render. Some operations named `estimate` also import HTTPS reference images: inspect side effects and input mapping before calling them. A local path, Library ID or ChatGPT attachment is not automatically a provider-readable URL. Use an available authorized transfer; a Drive bridge requires its own scoped transfer/access/cleanup approval and is not a universal requirement.

Pass an approved operation to [the execution adapter contract](execution-adapter-contract.md): exact schema, actual inputs/reference roles, destination, billing account label without secrets, cost cap, output count, bounded retries and verification. For 401/403 inspect authorization without switching accounts; for billing failures stop; for 422 repair inputs; for transient 429/5xx respect documented backoff. A submit timeout leaves state uncertain: poll the existing request ID before any resubmission. Never silently switch from free allowance to paid credits, from plugin to API, or to another provider.
