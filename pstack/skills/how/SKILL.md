---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Call `skill` on `pstack-runtime` before the first spawn.

Each spawn names a role line in `~/.dsh/pstack-models.md`. A missing file or missing line means `inherit-parent`. `inherit-parent` and `auto` omit `provider` and `model`. Pass `provider` and `model` only when the `subagent` tool schema exposes those fields and `list_subagent_models` lists that exact route. Otherwise omit them and say the child inherited the parent. When the schema exposes `reasoning_effort`, pass the effort recorded for that role only if the selected model advertises it.

Spawn with `subagent`. The child does not see this conversation, so the prompt is the filled reference template. The next step needs the result, so set `run_in_background: false`. Tell the child not to write files.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Decompose the question into 2 to 4 exploration angles, each a distinct slice of the subsystem. Spawn all explorers in a single message:

- role line: `how explorer`
- the child must not write files

Each explorer gets the prompt in `references/explorer-prompt.md` with its angle filled in. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

Spawn one `subagent` that explores and explains in one pass:

- role line: `how explainer`
- the child must not write files

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers have returned, spawn one `subagent` to synthesize their findings into one explanation:

- role line: `how explainer`
- the child must not write files

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Present the explainer's output to the user. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
