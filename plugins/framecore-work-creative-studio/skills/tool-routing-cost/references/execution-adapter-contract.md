# Capability-bound execution handoff

Use when the user requests a concrete run or wants a reusable production handoff. This chapter implements the fourth development direction as a provider-neutral contract. It adds no credentials, API connection, hosted endpoint, provider subscription or implicit permission.

## Adapter record

Use [the execution template](../assets/execution-plan.template.json). Identify the exact exposed tool and operation, selected surface/model if verified, source/version/date of its documented fields, user authorisation scope, input alias to actual attachment mapping, required output, cost unit/cap, retry policy and review method. Unknown fields stay Unknown. A provider mention or available connector is not permission to use it.

Before a call, verify the current operation's actual schema. Translate the approved prompt contract into those fields without changing its meaning. Bind reference roles to real inputs; a filename in text is not an uploaded attachment. Check the actual source count, supported editing/reference operation, duration and output controls for that surface. Do not turn API parameters into native UI controls or guess a native renderer model.

## State transitions

Planning becomes ready only when capability, authorisation, required inputs and any material cost boundary are resolved. A ready plan becomes submitted only after an actual call returns submission evidence. Record running, completed, failed or unknown from observed tool/job results. A timeout leaves the remote state unknown unless the provider confirms otherwise.

For a timeout, inspect status using the existing job ID if available before retrying. Use an idempotency key only when the actual provider documents it. Do not resubmit an ambiguous job blindly or pay for a duplicate. Bound transient retries by the task's remaining cost/attempt cap; authentication, billing, invalid-input and unsupported-capability failures require diagnosis rather than repeated calls. A fallback provider or new destination needs its own applicable user authorisation.

## Output and review

Record the actual returned output reference, accessible file, job ID and available technical properties. Do not save tokens, credentials or signed URLs into reusable handoffs. A URL is not proof of successful download; a completed provider job is not creative acceptance.

Route still inspection to Output Critic, motion/adjacency to Video Prompt Architect, audio to Audio Production Director and subtitle timing to Caption Studio. Verify the actual combined artifact where synchronization matters. If only a thumbnail or transcript is available, report that inspection scope. Preserve the selected version and make a rejected result a new candidate, not an overwrite of an accepted asset.

Pass outputs to Asset Manifest and Delivery after the applicable checks. With no exposed execution tool, return the requested portable prompt/plan and identify the actual missing capability. Do not simulate a job, ask for keys in chat or install infrastructure as a hidden workaround.

## Initial supported routes

The contract can describe a host-native image operation, a user-connected provider operation, a local Remotion composition, an HTML/GSAP HyperFrames composition or an OpenCut editing handoff. Each route remains unverified until its actual surface is inspected for this task. No built-in registry claims these providers are connected. Pick one requested route and validate it before expanding to more integrations.

## Provider route binding

Bind the [provider setup record](provider-setup.md) to this adapter using the exact host/client, provider product, route and billing basis. Do not treat a preference or catalog row as `ready`. A change from consumer plugin/MCP/CLI to API may change account, balance, supported models and upload destination; re-evaluate those fields within the user's authorization. Inspect non-generating tools for transfer side effects, especially cost estimators accepting reference URLs.
