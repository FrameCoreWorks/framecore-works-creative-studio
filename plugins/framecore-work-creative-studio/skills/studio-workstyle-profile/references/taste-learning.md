# Taste from explicit choices

Use for creative feedback, repeated preferences or a requested taste profile. Keep the existing expertise/workstyle profile distinct from taste. Skill with camera vocabulary does not imply a preference for complex camera movement. Evidence: [profile research sources](../../research-evidence/references/creative-upgrade-sources.md). The following contract is a Studio design proposal, not a trained preference model.

## Three scopes

| Scope | What belongs here | Example of a synthetic record |
|---|---|---|
| User | A stated reusable working or aesthetic preference | Prefers a physical cause for product movement when asking for realism. |
| Client | A supplied brand guideline or explicit client decision | This brand permits playful illustration but requires exact pack colours. |
| Project | A decision for the current task | This reel uses a locked camera; a later reel may use handheld motion. |

Resolve a concrete conflict in this order: the current explicit request, applicable supplied project/brand locks, then relevant preferences. If two explicit requirements conflict, identify that conflict rather than silently assigning priority. Never promote a project exception into a global user preference or apply one client's constraints to another.

## Record observations without inventing motives

For each useful record retain a neutral preference statement, scope and scope ID, medium, status, evidence type, source decision/revision, stated reason or Unknown, confidence and whether the user confirmed reuse. Accepted and rejected are decisions about exact proposals. A rejected render may have the right concept and a broken hand; preserve that distinction.

- An explicit preference can be applied immediately within its stated scope.
- Repeated behaviour supports a tentative hypothesis; it does not make a motive confirmed. Count distinct decisions, not repeated assistant summaries of one decision.
- A single “I don't like it” establishes rejection only. Ask one useful directional question before a new batch. Do not infer minimalism, matte surfaces or dislike of a genre.
- When the user explains the defect, apply that instruction. Do not demand another confirmation question.
- Distinguish aesthetic rejection, factual error, continuity defect, execution failure and scope mismatch. Repair with the owner responsible for that layer.

## Preserve freedom to change

Show a concise explanation of a relevant preference if asked. Let the user correct, retire, export or forget it. Record contradictory observations as unresolved until context explains them. Do not erase an older preference merely because a new project deliberately differs.

Do not infer demographics, personality, identity, mental state or private history from taste. Avoid statements such as “you always like” without explicit evidence. Taste is not a universal quality standard; preserve a deliberate surreal, decorative or maximalist brief even if another project favoured restraint.

## Persistence

Apply session-local corrections without forcing a save flow. Persist only through an actually available, authorised private profile/project mechanism. A user request to remember a preference authorises that scoped save; it does not create a storage capability. Confirm success only after a real write result. Without persistence, identify the session-local scope and include the relevant records in a requested handoff.

Shared plugin assets contain empty templates and synthetic examples only. Never write a user's or a client's actual choices into a distributable default. Keep client records in the authorised client/project store. Do not include raw conversations, images, private links or secrets in a taste record. Export only the relevant scope when asked; do not assume cross-host synchronization.

## Assets and bounded evaluation

The [profile template](../assets/profile.template.json) now includes a taste-memory section. The [synthetic taste example](../assets/taste-profile.example.json) demonstrates scope and evidence. The [read-only checker](../../../scripts/review-creative-plan.mjs) checks record structure and rejects inferred preferences labelled as confirmed; it does not infer a person's preferences.

After a real project, inspect at most the useful decisions: which proposals were selected, what was rejected and why, and whether a correction improved the next attempt. Use that record to reduce repeated mistakes. Do not optimise for acceptance by withholding fresh alternatives or repeating an old idea under new styling.
