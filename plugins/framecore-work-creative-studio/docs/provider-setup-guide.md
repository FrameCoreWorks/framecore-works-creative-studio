# Optional tools: ChatGPT, Work and Codex

Knowledge snapshot: **2026-09-29**. Studio helps select and configure a chosen route. Installing Studio supplies knowledge and instructions, not provider accounts or credits. Work can remain limited to concepts, storyboards and prompts.

## 1. Choose the access route

| Route | What you connect | Where it can be used |
|---|---|---|
| Available app/plugin | An existing catalog integration and, when required, a provider account | ChatGPT Chat, Work or a supported Codex client, depending on the integration and account |
| Custom MCP | A documented tool server and its authorization | MCP-capable Codex; ChatGPT only when custom-app configuration is available and permitted |
| CLI | A provider program in a terminal-capable environment | Usually local Codex; installation in a transient Work environment does not provide permanent phone access |
| API/SDK | Code integration, a key and API billing | Codex or another suitable runtime; a key alone does not create a ChatGPT app |
| Provider website | Manual work with prompts and files | The user's browser |

Check capabilities in the actual client; ChatGPT is not limited to plugins, nor Codex to APIs. See [OpenAI's overview](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex), [Codex MCP](https://developers.openai.com/codex/mcp) and [custom MCP in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt).

## 2. Services covered by Studio

The following integrations were confirmed in the catalog or official documentation for this dated snapshot. This is a selection, not the complete catalog. Verify availability for the actual plan, region, phone and conversation surface. The [source record](../skills/tool-routing-cost/references/provider-sources.md) documents evidence and limitations.

| Service | Main integration use | Account and costs |
|---|---|---|
| fal | Image, video, audio, 3D and media processing | fal account; paid model execution. A ChatGPT subscription does not fund it. |
| Higgsfield | Image/video generation and creative workflows | Higgsfield account; consumer-account conditions are described below. |
| Runway | Image, video and audio generation/editing | Runway account/workspace; verify the relevant plan and credits. |
| OpenArt | Image/video generation | OpenArt account and credits; required plan: **Unknown**. |
| HeyGen | Avatar, voice and translation video | Account entitlements and operation costs: **Unknown**. |
| Descript | Editing, transcription, captions and short clips | Plan and operation limits: **Unknown**. |
| Adobe | Image processing, graphic materials, video and documents | The catalog describes guest access and additional signed-in features; verify operation conditions. |
| Adobe Express | Template-based designs and editing | The catalog describes a free start; this does not make every asset/export free. |
| Canva | Graphics and presentations | Account, plan and feature requirements: **Unknown**. |
| Figma | Editable designs and design workflows | Access scope and costs: **Unknown**. |
| Replit | Application and website building | A separate category; do not assume video-shot generation. Verify build/hosting costs. |

**ElevenLabs:** official API/MCP tools and skills were confirmed. An available ChatGPT catalog app is **Unknown** in this review. A missing search result does not prove that an app does not exist; search again when selecting it. The same applies to other new services, such as MuAPI and POYO.

## 3. fal: available plugin or developer integration

The [official fal plugin](https://chatgpt.com/plugins/fal) is described for ChatGPT and Codex. Install it in a supported surface, connect a fal account and select it in the conversation. Begin verification with model discovery without generation. Selecting a fal OAuth account through **Use for MCP** is independent of the website account switcher. An API key identifies its associated account. See [fal's instructions](https://fal.ai/docs/documentation/setting-up/codex-plugin).

Codex can instead use inference MCP, API/SDK or a documented CLI. Avoid installing multiple routes without a need. Verify the model, input schema and rate for the specific task. See [Run MCP](https://fal.ai/docs/documentation/setting-up/mcp) and [pricing](https://fal.ai/pricing). Generation MCP and administrative/deployment Platform MCP are different servers.

Signing in does not purchase a subscription. fal bills model usage and also offers optional credit plans. Entitlements, balance and discounts depend on the account and route, not the model name alone. Do not assume website discounts cover API usage. See [fal plans](https://fal.ai/docs/documentation/agent/access-and-pricing).

## 4. Higgsfield: two separate billing routes

| Route | Authentication | Billing |
|---|---|---|
| Available ChatGPT plugin / MCP / official CLI | Higgsfield account sign-in | Consumer-account route; the guide requires an active paid plan. Verify any current trial/free exceptions. |
| Higgsfield API, **open.higgsfield.ai** console | Separate API credentials | Separate USD balance and usage billing; a website subscription is not required and does not replace the API balance. |

See [plugin/MCP connection](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent), [official CLI](https://higgsfield.ai/cli) and [API explanation](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-the-higgsfield-api).

**Open Higgsfield** above means the official API console. Projects named `wide-trace/open-higgsfield`, `openhiggsfield.ai` and `openhiggsfield.com` are not that console. Identify an external project's exact URL before using it; launching an interface does not grant free model access.

Sources conflict: an older Higgsfield guide limits audio, websites and free execution in ChatGPT, while currently exposed tool descriptions include those features and trial/free entitlement fields. Studio checks the specific tool and account entitlement instead of promising execution. Do not automatically transfer website “Unlimited” claims to the plugin or API.

## 5. Step-by-step setup

**ChatGPT Chat / Work, available integration:**

1. Open the **Plugins** or **Apps** catalog available to the account. Find the service and check its publisher, scope and requirements.
2. Select installation/connection and complete provider sign-in if required.
3. Select the integration through `@` or the available conversation menu. A pasted name does not establish activation.
4. Request a supported read without generation. Then establish the model, references and cost for the actual task.

**Codex, API/MCP/CLI:**

1. Identify the exact Codex client and preferred route. If an available plugin is sufficient, an API integration is unnecessary.
2. For MCP/CLI, verify the official endpoint/package and authentication. For API access, identify the product, billing account and private secret-storage location.
3. Configure only the selected integration after a user request. Preserve existing settings; never enter keys into chat or the repository.
4. Verify the connection through a read, then separately authorize any paid operation and reference transfer. Installation and generation are separate outcomes.

During Studio setup, the user can choose an existing account, request a guide or skip. A preference does not install additional software or authorize a purchase, trial activation, upload or generation. Private settings do not enter the shared plugin.

## 6. Common blockers

| Problem | Next step |
|---|---|
| Plugin is listed but its tool is unavailable | Check installation, conversation selection and support for the feature in this client. |
| Sign-in works but generation is rejected | Check the account/workspace, plan, balance and model access. Do not switch account or route without authorization. |
| Reference exists in ChatGPT but is inaccessible to the service | Establish a supported transfer. A local path or attachment ID is not a public URL. |
| The call timed out | Check the existing job ID; resubmission may incur a second charge. |
| No integration is available or the user skips setup | Continue concept work and prepare a complete prompt for manual use. |

Some pricing tools import reference files. Check operation effects before using them. A model name shared by multiple providers does not establish identical controls, pricing or output rights.
