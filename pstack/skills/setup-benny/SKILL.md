---
name: setup-benny
description: Prepare Benny when a human asks to install it or change its Slack, tracker, repository, routing, control, model, or budget settings. Use for "set up benny", "configure benny", or an edit to `.dsh/benny/`. There is no scheduler.
---

# Set up Benny

A human asked you to prepare Benny. Run this procedure. Do not create a Slack automation, a cron job, or a goal that watches a channel.

DeepSeek Harness has no Cursor Slack automation and no settings-file plugin switch. Do not merge this pack into a Cursor automations directory. Do not enable a Cursor plugin. Shared skills load with the `skill` tool.

If a step needs Slack and no Slack tool is connected, stop and say so. Do not invent a Slack client.

Never put a secret in a skill file, a prompt, or committed configuration.

## 1. Pick the repository

Ask which repository will hold the configuration if the human has not named one. Write user-owned files under `<target>/.dsh/benny/`. Do not write them inside this skill directory. A later pstack refresh must not overwrite `.dsh/benny/`.

Create the directory when it is absent. Preserve files already there. If an existing file differs from an example and you cannot tell who owns the edit, stop and ask before replacing it.

## 2. Copy examples

Copy these only when the destination file is absent:

- `references/configuration.example.yaml` to `.dsh/benny/configuration.yaml`
- the feature-map example from the `benny-reproduce` skill, `references/feature-map.example.md`, to `.dsh/benny/feature-map.md`
- the routing example from the `benny-triage` skill, `references/routing.example.md`, to `.dsh/benny/routing.md` when the human wants reroutes

Point `routing.map_path` and `control.feature_map_path` at those copies. Do not edit the examples inside the skill directories.

## 3. Load shared skills

Call the `skill` tool for each name below, then continue. Do not write a settings file to make them visible.

- `how`
- `why`
- `tdd`
- `unslop`
- `principle-separate-before-serializing-shared-state`
- `principle-minimize-reader-load`
- `principle-guard-the-context-window`
- `principle-sequence-verifiable-units`
- `principle-fix-root-causes`
- `principle-prove-it-works`

If a name does not resolve, stop and say which one failed.

## 4. Fill the required choices

Ask for or confirm:

- Source Slack channel ID, or an explicit statement that reports will be pasted into chat
- Optional operations channel ID
- Repository URL and default branch
- Triage identity, only if Slack posting will be used
- Issue tracker type, team, project, labels, and intake status
- Tracker adapter this session can actually call
- Optional routing map path
- Control driver: a project verify skill, Playwright MCP, or the shell
- Feature-map path
- Status strings
- Pull request URL format
- Budgets
- Model role names, not invented slugs

Read `~/.dsh/pstack-models.md` when a role is named. Record a slug only when this session has shown it. A missing role inherits the parent model. Do not guess.

The repository, tracker adapter, control driver, and feature map must be explicit. Stop if any of those stays ambiguous. Slack channel and triage identity are required only when the human wants Slack posts. If they want Slack and no Slack tool is connected, stop and say so.

Call the `skill` tool with `unslop` before saving names and descriptions the human will read.

## 5. Check tools

When the human asked for Slack, triage needs a connected Slack read tool and a thread-reply tool. Repro needs repository history and a draft pull-request command that is already available (`gh` or `origin`). Do not call undocumented endpoints. Do not invent a bot token flow.

`BENNY_SLACK_BOT_TOKEN` may be used only when the human already stored it in the environment and a connected Slack tool documents that it reads that variable. Never write the token into YAML.

## 6. Routing map

If the human wants reroutes, fill `.dsh/benny/routing.md` from the `benny-triage` example. Replace every placeholder. Keep owner pings off by default. A ping is allowed only for a configured feature owner or a confirmed likely regression author, and only when a Slack tool can post it. Otherwise record the destination in the verdict and do not ping.

If no routing map is configured, triage may classify a report but must not guess a destination or owner.

## 7. Control driver

Load `benny-reproduce` and read its `references/control-adapter.md`, then read the completed feature map.

- Browser and web UI proof uses Playwright MCP when that server is connected.
- CLI proof uses the shell.
- A project skill at `.dsh/skills/verify-<app>/` is the preferred driver when it exists.

If the reported surface has no connected driver, leave repro disabled and say what is missing. Do not claim a reproduction that was not performed.

Run one harmless check before telling the human repro is ready: bring the app up, open one mapped feature, capture evidence, clean up. Say repro is ready only when that check succeeds.

## 8. Hand back

Do not schedule a watcher. Tell the human:

- Configuration lives at `.dsh/benny/`.
- Ask for `benny-triage` when a report is ready.
- Ask for `benny-reproduce` after a bug or performance verdict.
- Commit `.dsh/benny/` only if they ask, and never commit secrets.

There is nothing to enable in a settings file.
