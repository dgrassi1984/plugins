# Reproduce prompt sketch

This file is not a scheduler prompt. On DeepSeek Harness, ask the agent to load the `benny-reproduce` skill after a bug or performance verdict.

The skill reads `.dsh/benny/configuration.yaml` and the feature map it names. It does not watch Slack. If a post is required and no Slack tool is connected, it stops and returns the result in chat. A fix, when one is allowed, is a draft pull request only.
