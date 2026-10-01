---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects subagent models and writes ~/.dsh/pstack-models.md. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.dsh/pstack-models.md` as plain markdown. Skills read it when a step names a role. A missing file or missing line means `inherit-parent`.

## Steps

### 1. Detect available models

If the `list_subagent_models` tool exists, call it. That list is the detected set. If it does not exist, the detected set is the session's current model only. If nothing was detected, ask the user with `ask_user_question` and do not invent a slug. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs.

### 2. Load current state

If `~/.dsh/pstack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise every role starts as `inherit-parent`. A line whose role is not in step 5 is retired. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Use `ask_user_question`. Offer these four options with these exact labels, and name the current budget when the file records one.

- `unlimited — keep max`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Do not rewrite a slug to encode effort. `inherit-parent` and `auto` stay as they are. When a role's value is a confirmed real slug, record the budget's reasoning effort only as a trailing comment the skills can pass if the `subagent` tool exposes `reasoning_effort`:

- `unlimited — keep max` → `# reasoning_effort: max`
- `large — xhigh reasoning` → `# reasoning_effort: xhigh`
- `medium — high reasoning` → `# reasoning_effort: high`
- `small — medium reasoning` → `# reasoning_effort: medium`

No comment on an `inherit-parent` or `auto` line. On a re-run, keep any role the user already set to a confirmed slug, a list of confirmed slugs, or an alias.

**(c) Show the roles and confirm.** Show every role with its model. Every role is `inherit-parent` until the user picks a confirmed slug. Mark any real slug not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles. Offer the detected models plus `inherit-parent` and `auto` (both mean this role runs on the parent model). Use `ask_user_question`. For panel roles (`arena runners`, `architect runners`, `interrogate reviewers`) the value is a list, and one child runs per entry, alias entries included, so the list length sets the count. Until the user adds confirmed slugs, that list is a single `inherit-parent`. `arena cross-judge pool` is also a list. Arena selects one value from it whose model family differs from the parent's when `list_subagent_models` lists such a route. Otherwise the judge inherits the parent. `swarm workers` is the model for every worker unless a race or comparison assigns another confirmed route per arm.

### 4. Validate

Every real slug written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen real slug is not available, stop and ask again. Do not write a slug you have not confirmed.

### 5. Write the file

Write `~/.dsh/pstack-models.md` as plain markdown. No YAML frontmatter. Overwrite the whole file so re-runs stay idempotent. One line per role, using the same labels the skills read. Shape, with every role at `inherit-parent` until the user picks a confirmed slug:

```
# pstack model configuration. One line per role. A missing line means inherit-parent.
# inherit-parent or auto: omit provider and model. The child runs on the parent model.
# A trailing reasoning_effort comment is passed only when the subagent tool exposes reasoning_effort and the selected model advertises it.
# budget: medium (high)
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: inherit-parent
arena cross-judge pool: inherit-parent
swarm workers: inherit-parent
architect runners: inherit-parent
interrogate reviewers: inherit-parent
```

A confirmed slug replaces `inherit-parent` on that line and, when a budget was chosen, gains the matching `# reasoning_effort:` comment. Panel lines are comma-separated when the user confirms more than one entry.

### 6. Confirm

Tell the user the file was written. Skills read it when a step names a role. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, call `skill` on `create-verification-skill`. On no, move on without pushing.
