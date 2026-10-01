---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own session log before fanning out. Logs live at `$DSH_HOME/sessions/--<workspace-slug>--/$DSH_SESSION_ID/session*.jsonl.zstd` (`~/.dsh` when `DSH_HOME` is unset). The slug is the absolute workspace path with the leading slash removed and each `/` turned into `-`, wrapped in `--`. Decompress with `zstd -dc`. Do not glob other workspace slugs.

```bash
dsh_home="${DSH_HOME:-$HOME/.dsh}"
slug=$(printf '%s' "$PWD" | sed 's#^/##; s#/#-#g')
find "$dsh_home/sessions/--${slug}--/${DSH_SESSION_ID:-}" -name 'session*.jsonl.zstd' 2>/dev/null
```

The current session is `$DSH_SESSION_ID`. Child sessions, when present, are separate directories under the same workspace slug. Decompress the matching `session*.jsonl.zstd` with `zstd -dc`. If no file resolves, write a tight digest of the session and pass that instead.

### 2. Spawn three reviewers in parallel

Call `skill` on `pstack-runtime` before the first spawn. One message, three `subagent` calls. Step 3 needs every review, so set `run_in_background: false`. The child keeps its tools, including MCP. The prompt forbids edits. The child does not see this conversation, so the prompt carries the decompressed session log path or digest, and tells the child to follow the template. Read `~/.dsh/pstack-models.md` for the named role. A missing line means `inherit-parent`: omit `provider` and `model`. Pass them only when the tool exposes those fields and `list_subagent_models` lists the route. When the schema exposes `reasoning_effort`, pass the effort recorded for that role only if the selected model advertises it.

| Lens | Role line | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

A missing role line inherits the parent model.

Pass each template verbatim, substituting the session-log path or digest where marked. Reviewers return findings as the `subagent` result.

### 3. Synthesize

One `subagent` call, role `reflect judgment, divergent, synthesizer`, inheriting the parent when that line is missing. The child keeps its tools so it can spot-verify citations. The prompt forbids edits. Step 4 needs the list, so set `run_in_background: false`. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): parent edits that `SKILL.md` in place. Keep `name` kebab-case and matching the directory. Keep `description` as one YAML scalar.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): parent rewrites that skill's `description` so the next catalog match fires. Quote it or use `description: >-` when punctuation requires it.
- `new skill: <kebab-name>`: parent writes `<root>/<kebab-name>/SKILL.md` under a skill root from `pstack-runtime`. `name` matches the directory. `description` says when to load it. Do not set `disable-model-invocation` unless the user asked for a user-only skill.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
