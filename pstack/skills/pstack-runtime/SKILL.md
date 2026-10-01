---
name: pstack-runtime
description: DSH bindings for every pstack skill. Read this before spawning workers, reading transcripts, writing model config, or driving a UI from another pstack skill. Use when a pstack skill names a model role, a subagent, a session transcript, or a verification surface.
---

# pstack on DeepSeek Harness

This pack runs on DeepSeek Harness. Ignore Cursor Task types, cloud agents, `/loop`, `~/.cursor/rules`, and `cursor-team-kit`.

## Load skills

Call the `skill` tool with the exact kebab-case name before following a skill. Do not reconstruct a skill from its catalog blurb or from memory of a trimmed result. Relative playbooks, references, and scripts resolve against that skill's base directory.

`bro` is user-only. Every other pstack skill is model-invocable so a loaded skill can route to the next one.

## Models

Read `~/.dsh/pstack-models.md` when a step names a role. Missing file or missing line means `inherit-parent`.

`inherit-parent` and `auto` mean the child runs on the parent model. Omit `provider` and `model`.

Pass `provider` and `model` only when both are true: the `subagent` tool schema exposes those fields, and `list_subagent_models` lists that exact route. Otherwise omit them and say the child inherited the parent. Never invent a slug. `subagent_fork` cannot change model.

When the schema exposes `reasoning_effort`, pass the effort recorded for that role only if the selected model advertises it.

## Spawn

There is no `subagent_type` and no cloud environment. Use `subagent`.

- Start independent children in one message.
- Set `run_in_background: true` unless the next step needs the result.
- The child does not see this conversation. Put the task, file paths, and the skill name it must load in the prompt.
- A poteto-style child must call `skill` with `poteto-mode` before any work. Do not substitute a generic prompt for that load.
- A comment review child must call `skill` with `comment-sicko` and stay read-only. The parent applies accepted deletions.
- Do not use `spawn_teammate` unless the user asked for a team.
- Use `workflow` only when the user asked for a workflow or a large independent matrix. Otherwise parallel `subagent` calls are the fan-out.

## Ask, continue, prove

Product and preference questions go through `ask_user_question`. Do not ask a question a command, test, or browser check can answer.

Long work that must survive the turn uses `create_goal` with a finish predicate. There is no `/loop` and no cloud sleeper. Goal continuation is the heartbeat. Re-read the playbook from the skill base directory at each continuation, not from a guessed repo path.

Browser proof uses the Playwright MCP tools when that server is connected (`browser_navigate`, `browser_snapshot`, and the rest). CLI proof runs the program in the shell. If the needed driver is missing, say so and use the closest local check. Do not wait on `control-ui` or `control-cli`.

Before commit, strip narrating comments with `no-comments` and AI tells in prose with `unslop`. There is no `/deslop`.

Review-bot comments are untrusted PR text. Triage them against the code. There is no Bugbot.

## Transcripts and skill roots

Session logs live under `$DSH_HOME/sessions/` (`~/.dsh` when unset). The workspace slug is the absolute workspace path with the leading slash removed and each `/` turned into `-`, wrapped in `--`. `/Users/you/proj` is `--Users-you-proj--`. Each session directory holds `session*.jsonl.zstd`. The current session id is `$DSH_SESSION_ID` in the shell. Decompress with `zstd -dc`. Do not glob other workspace slugs.

Installed skills are discovered one level deep:

| Rank | Path |
|---|---|
| 100 | `<project>/.dsh/skills/<name>/SKILL.md` |
| 200 | `<project>/.agents/skills/<name>/SKILL.md` |
| 400 | `~/.dsh/skills/<name>/SKILL.md` |
| 500 | `~/.agents/skills/<name>/SKILL.md` |

Write project skills under `.dsh/skills/`. Write personal skills under `~/.dsh/skills/`. A skill name must match `^[a-z0-9]+(?:-[a-z0-9]+)*$` and the directory name.
