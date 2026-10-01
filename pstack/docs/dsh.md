# pstack on DeepSeek Harness

This branch is a DSH port of [cursor/plugins](https://github.com/cursor/plugins) `pstack` at `2eb7ed4` (plugin 0.15.5). The engineering playbooks are unchanged. The runtime bindings are not.

Cursor's plugin loader, Task `subagent_type`, cloud agents, `/loop`, `~/.cursor/rules`, and `cursor-team-kit` are not part of this fork. Agents follow [`skills/pstack-runtime/SKILL.md`](../skills/pstack-runtime/SKILL.md).

## Install

DSH discovers `<root>/<name>/SKILL.md` one level deep. `pstack/skills` is already that shape.

User install, without touching skills that are not in this pack:

```bash
src=pstack/skills
dest="${DSH_HOME:-$HOME/.dsh}/skills"
for d in "$src"/*; do
  name=$(basename "$d")
  rm -rf "$dest/$name"
  cp -R "$d" "$dest/$name"
done
```

A project can instead point `customSkillDirs` at `pstack/skills`, or copy the same directories into `.dsh/skills`. Nested trees are not discovered, so do not install the repo root as a skill root.

Reload is automatic: the filesystem provider watches the skill roots.

## What changed

- Skill `name` values are kebab-case and match their directories (`poteto-mode`, `make-bot-ui`, `comment-sicko`).
- Cursor agent files are skill bundles: `skills/poteto-agent` and `skills/comment-sicko`.
- `disable-model-invocation` remains only on `bro`. Every other skill can be loaded with the `skill` tool, which is how playbooks route.
- Model roles are read from `~/.dsh/pstack-models.md`. Missing roles inherit the parent model. `/setup-pstack` writes that file and will not record a slug it has not seen.
- Fan-out uses `subagent`. Model overrides are passed only when that tool exposes them and `list_subagent_models` confirms the route.
- Overnight runs use `create_goal`, not `/loop`.
- Browser checks use Playwright MCP when it is connected. CLI checks use the shell.
- Comment and prose cleanup use `no-comments` and `unslop`.
- Session logs are `$DSH_HOME/sessions/--<workspace-slug>--/<id>/session*.jsonl.zstd`.

## Not portable

Benny's Slack-trigger automations have no DSH scheduler. The procedures in `skills/benny-*` run when asked. They do not post to Slack by themselves and they do not write `.cursor/settings.json`.

`origin` and `gh` forge commands are unchanged where the playbooks already treated them as optional CLIs.
