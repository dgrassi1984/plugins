---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill, then runs unslop, optionally pulling fresh evidence from recent session logs."
---

# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (e.g. `jay-mode`, `priya-mode`).

This skill orchestrates an inline mining pass (see step 1), direct authoring of the mode skill, and the **unslop** skill (prose discipline). It sequences them. It doesn't replace them.

Call `skill` on `pstack-runtime` before the first spawn.

## Flow

### 0. Check for an existing skill

Look for `<project>/.dsh/skills/<handle>-mode/SKILL.md` and `~/.dsh/skills/<handle>-mode/SKILL.md`. Discovery is one level deep. If one exists, confirm intent with `ask_user_question` (unless they already said "update my skill" or similar):

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Locate this workspace's session logs before fanning out. Use `$DSH_HOME/sessions/--<workspace-slug>--/` only. Decompress `session*.jsonl.zstd` with `zstd -dc`. Do not glob other workspace slugs.

Survey recent agent conversations within that scope for recurring patterns. Spawn parallel `subagent` children across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Step 2 needs every slice, so set `run_in_background: false`. A missing model line means `inherit-parent`: omit `provider` and `model`. Pass them only when the tool exposes those fields and `list_subagent_models` lists the route. The child does not see this conversation. Each prompt names the workspace slug, tells the child to decompress `session*.jsonl.zstd` with `zstd -dc`, and forbids reading other workspace slugs. Each slice returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Use the `ask_user_question` tool (structured multi-choice) rather than asking the user to type from scratch.

Shape: one or two questions with 4-6 options each, `allow_multiple: true` for category questions. Start broad ("Which areas matter most?"), then follow up on selected areas with specific options. After the structured rounds, one free-form chat question catches anything the options missed.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **poteto-mode** skill shows the shape. Read it for granularity. Don't copy its content. The user's rules are not the same as poteto-mode's.

### 4. Draft the skill

Write the skill file directly. Placement:

- Path: `<project>/.dsh/skills/<handle>-mode/SKILL.md`, or `~/.dsh/skills/<handle>-mode/SKILL.md` if the user prefers a personal skill. Do not nest another directory under the skill name.
- Handle: the user's first name or chosen identifier. `name` is `<handle>-mode` and matches `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- Frontmatter `description`: trigger on their name + `/<handle>-mode` + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- New mode skills are model-invocable. Set `disable-model-invocation: true` only when the user asks for a user-only skill. DeepSeek Harness will not load a `disable-model-invocation` skill via the `skill` tool.

### 5. Iterate on prose

Apply the **unslop** skill to every line. Keep the skill operational: short imperatives, no pasted excerpts of other skills.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

Work in a worktree off main. Commit and open a PR. Don't push to main directly.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-mode` skill is subjective output. A benchmark loop isn't useful here. Vibe-check with the user: does it read like them? Did it miss anything? Then ship.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): write that skill directly under a skill root from `pstack-runtime`. No mining required.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a mode skill.

