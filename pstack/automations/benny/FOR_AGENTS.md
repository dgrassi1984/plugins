# benny on DeepSeek Harness

Cursor Slack automations do not exist on DeepSeek Harness. `.cursor/settings.json` plugin enablement does not exist on DeepSeek Harness. Do not merge this pack into a Cursor automations directory, do not enable a Cursor plugin, and do not invent a Slack client or a scheduler.

The procedures are discoverable skills. A human asks for them. They run once, in this session.

- `setup-benny` writes configuration in the target repository at `.dsh/benny/`.
- `benny-triage` classifies one report and returns one verdict.
- `benny-reproduce` reproduces a confirmed bug and may open a bounded draft pull request.

Load shared pstack skills with the `skill` tool: `how`, `why`, `tdd`, `unslop`, and the principle skills those procedures name. Do not enable a plugin to make them visible.

If a step needs Slack and no Slack tool is connected, stop and say so. Return the verdict in chat. Do not post a root message, and do not guess a Slack API.

Draft pull requests only. Do not merge or deploy.

Start from [`templates/configuration.example.yaml`](./templates/configuration.example.yaml) only as a shape. The live copy belongs at `.dsh/benny/configuration.yaml`, outside this pack, so a skill refresh cannot overwrite it. Keep secrets in the environment, not in the file.

The files under `skills/` in this directory are the archived Cursor procedures. Do not follow them. Each one points at the discoverable skill name.
