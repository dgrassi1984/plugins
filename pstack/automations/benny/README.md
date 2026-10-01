# benny

benny triages an issue report, then reproduces a confirmed bug and may prepare a small draft fix.

DeepSeek Harness has no Cursor Slack automation and no plugin enablement file. These procedures run when you ask. They do not watch a channel by themselves.

## set it up

1. ask for [`setup-benny`](../../skills/setup-benny/SKILL.md) and name the target repository.
2. let it write configuration under `.dsh/benny/` in that repository. it must not overwrite files you already own there.
3. shared skills (`how`, `why`, `tdd`, `unslop`, and the principle skills) load with the `skill` tool. nothing is enabled in a settings file.
4. adapt [`configuration.example.yaml`](./templates/configuration.example.yaml) and the feature-map example from [`benny-reproduce`](../../skills/benny-reproduce/SKILL.md). keep secrets out of the repo.
5. commit `.dsh/benny/` only if you want the config in git, and never commit a token.
6. when a report is ready, ask for [`benny-triage`](../../skills/benny-triage/SKILL.md). after a bug or performance verdict, ask for [`benny-reproduce`](../../skills/benny-reproduce/SKILL.md).

if a step needs Slack and no Slack tool is connected, the agent stops and says so.
