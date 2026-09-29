# Provider evidence ledger

Checked: 2026-09-29. Public documentation and active-host catalog/tool descriptions only. No generation, account-entitlement inspection or provider setup was performed. This is a selected catalog, not a complete global inventory. Recheck relevant claims before setup or spending.

| ID | Primary evidence | Scope |
|---|---|---|
| OAI-PLUGINS | [OpenAI: Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex) | Apps, plugin packages, host-dependent availability, installation and authentication are distinct. |
| OAI-APPS | [OpenAI: Connected apps](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt) | Account and action permissions. |
| OAI-MCP | [OpenAI: Codex MCP](https://developers.openai.com/codex/mcp) | MCP client configuration and OAuth; verify installed client version. |
| OAI-CUSTOM | [OpenAI: Developer mode and MCP apps](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) | Custom MCP is a separate, eligibility-dependent path. Do not generalize older blanket read-only claims to current apps. |
| DIRECTORY | Active Plugin Management directory search on 2026-09-29; [directory](https://chatgpt.com/plugins) | Returned Higgsfield, Runway, OpenArt, HeyGen, Descript, Adobe, Adobe Express, Canva, Figma and Replit. Descriptions establish advertised scope, not successful execution or universal availability. No private installation/account state is published. |
| FAL-PLUGIN | [fal for ChatGPT and Codex](https://fal.ai/docs/documentation/setting-up/codex-plugin) | Official directory route and OAuth, including Codex; IDE-extension limitations require rechecking. The exact-name directory search returned no fal result in this research, but this page and exposed tools independently confirm the integration. |
| FAL-MCP | [fal Run MCP](https://fal.ai/docs/documentation/setting-up/mcp) | Inference endpoint, auth alternatives, account selection and transfer constraints. |
| FAL-PRICING | [fal pricing](https://fal.ai/pricing) | Model usage pricing, separate from a ChatGPT subscription. |
| FAL-PLANS | [fal access and pricing](https://fal.ai/docs/documentation/agent/access-and-pricing) | Optional credit plans; API discount rules differ from UI/CLI rules. Retrieved via fal's public documentation search. |
| FAL-FAQ | [fal API FAQ](https://fal.ai/docs/documentation/model-apis/faq) | Billing errors, model-specific rights, file retention and public-URL defaults. Retrieved via fal's public documentation search. |
| HF-CONNECT | [Higgsfield: connect an AI agent](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent) | Official ChatGPT directory connection and consumer-account requirements. Some capability/billing statements conflict with the current tool contracts below. |
| HF-CLI | [Higgsfield CLI](https://higgsfield.ai/cli) | Official CLI package and browser sign-in. |
| HF-API | [Higgsfield API guide](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-the-higgsfield-api) | `open.higgsfield.ai` is the official API console; API uses a separate prepaid dollar balance with no consumer subscription requirement. |
| HF-API-REF | [Higgsfield API reference](https://docs.higgsfield.ai/docs) | Server-side authentication, model-specific JSON, asynchronous job lifecycle and output retrieval. |
| HF-API-TERMS | [Higgsfield API terms](https://open.higgsfield.ai/terms-of-service) | API is separate from consumer subscriptions and credits. Check current terms for an actual project. |
| HF-TOOLS | Higgsfield tool contracts exposed in this authoring Work session on 2026-09-29 | `balance` describes credits, plan and optional free/trial allowances; audio/website tools are exposed. `estimate_image_cost` and `estimate_video_cost` can import HTTPS reference images. None was executed here. |
| RUNWAY-API | [Runway API setup](https://docs.dev.runwayml.com/guides/setup/) | API project, project key and project credits. No assumption that web-plan credits fund the API. |
| ELEVEN-TOOLS | [ElevenLabs agent tooling](https://elevenlabs.io/docs/eleven-api/resources/agent-tooling) | Official skills and hosted MCP; not evidence of a ChatGPT directory app. |
| ELEVEN-MCP | [ElevenLabs hosted MCP](https://elevenlabs.io/docs/eleven-agents/operate/hosted-mcp) | OAuth service with agent-management and TTS permissions; do not infer every music/audio feature is exposed. |
| OPEN-LOOKALIKE | [wide-trace/open-higgsfield](https://github.com/wide-trace/open-higgsfield), [openhiggsfield.com](https://openhiggsfield.com/) | Other projects with similar names. They are not identifiers for the official API console. No third-party wrapper was installed or security-reviewed. |

## Evidence precedence

Use provider documentation for product/billing distinctions, current host discovery for installability, actual schemas for exposed operations, and authorized live responses for connection/entitlements. These answer different questions. A runtime description can establish that a field exists but cannot prove a user's allowance. Keep unresolved conflicts explicit rather than selecting the convenient claim.

Recheck only the relevant sources when the user chooses a route or asks for current prices. Do not browse every source on every Studio request. Do not retain an empty search as a permanent `not_available` flag. API-only or unverified examples such as MuAPI, POYO and ElevenLabs must not be presented as native ChatGPT apps without fresh directory evidence.
