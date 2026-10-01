# Triage prompt sketch

This file is not a scheduler prompt. On DeepSeek Harness, ask the agent to load the `benny-triage` skill.

The skill reads `.dsh/benny/configuration.yaml` when that file exists. Otherwise it asks for the missing values. It does not watch Slack. If a post is required and no Slack tool is connected, it stops and returns the verdict in chat.
