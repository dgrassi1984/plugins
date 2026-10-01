---
name: benny-reproduce
description: Reproduce a triaged bug through the real UI when a human asks, verify an existing fix if one exists, and open a bounded draft pull request only after before-and-after proof. Use after a bug or performance verdict. There is no scheduler.
---

# Reproduce and maybe fix

A human asked you to reproduce one triaged report. Do not watch Slack for a marker. The human, or the verdict already in this conversation, is the trigger.

Load `.dsh/benny/configuration.yaml`. If the config, the control driver, or the completed feature map is missing, stop and say what is missing.

If a step needs Slack and no Slack tool is connected, stop and say so when a post is required. You may still reproduce and report in chat. Do not invent a Slack client.

## Hard safety rules

- If Slack coordinates are in play, freeze them before any other work.
- Never post a root message in the source channel.
- Preflight the source parent before every source-thread post.
- You are the only Slack poster, and only when a Slack tool is connected.
- A `subagent` used for analysis is read-only and returns findings. Load `pstack-runtime` before you spawn one. Its prompt must forbid Slack writes and must not receive Slack credentials.
- A code edit stays in this session unless the child environment provably has no Slack credentials and no Slack write tool. If that is uncertain, edit here.
- Utility bots are evidence. They do not own the fix unless a person explicitly delegated the fix to them.
- The discriminating symptom must appear twice through real UI interaction.
- State inspection may confirm an observation. It must not inject or force the symptom.
- No confirmed repro means no authored fix.
- An existing pull request or commit switches the run to verify mode. Do not author over it.
- Use `github.com` pull request links. Draft only. Never merge or deploy.
- Keep captures, recordings, logs, and tokens out of source control.
- Call the `skill` tool for `principle-guard-the-context-window` before delegating a large read.
- Call the `skill` tool for `principle-sequence-verifiable-units`, `principle-fix-root-causes`, and `principle-prove-it-works` through repro, fix, and verification.

## 1. Freeze the source

When the human pasted the report and the verdict, that paste is the source. Record it.

When a Slack tool is connected and the human named a thread:

1. Require the channel to equal the configured source channel.
2. Store a nonempty `SOURCE_THREAD_TS` and `SOURCE_CHANNEL_ID`.
3. Read the thread and verify the root.
4. Fetch the permalink.

Never replace those values with a reply timestamp. If a preflight fails, post nothing.

## 2. Accept the verdict the human already has

Proceed only for a bug or performance verdict from the configured triage identity, or from the human when they pasted the marker themselves. Stop for `other`, conflicting markers, or no verdict. Do not poll.

Public marker forms:

```text
[benny:bug]
[benny:bug] tracker=https://tracker.example/issue/123
[benny:performance]
[benny:performance] tracker=https://tracker.example/issue/123
[benny:other]
```

Capture the optional tracker URL.

## 3. Ownership and existing fixes

Stop when a person clearly claims the fix, gives a concrete implementation plan, or asks another agent to implement it. Do not treat a bot summary, a log lookup, or a request to diagnose as ownership.

If an open pull request or merged commit plausibly fixes the report, follow `references/verify-existing-fix.md`. A claim without a commit or pull request is not a fix artifact. If a person owns the work but has not produced an artifact, stop. Do not race them.

## 4. Status

If an operations channel is configured and a Slack tool can post there, one root status message in that channel is allowed. Store its coordinates separately from the source. Never confuse them.

If no operations channel is configured, or no Slack tool is connected, keep status in chat. Do not substitute a source-channel root message.

Use the configured status strings: Reproducing, Could not reproduce, Blocked, Reproduced, Verifying existing fix, Attempting bounded fix, Draft pull request opened, Fix did not land.

## 5. Load the driver

Read `references/control-adapter.md` and the map at `control.feature_map_path`. The example map is `references/feature-map.example.md`. Do not edit the example.

Find the feature-map section that matches the reported user path. If no section covers it, mark the run blocked. Do not invent a path or selector.

On this harness the driver is, in order:

1. The project verify skill named in config, if it exists.
2. Playwright MCP, when the server is connected, for a browser or web UI.
3. The shell, for a CLI.

Do not wait on a Cursor control plugin. If none of those can drive the reported surface, mark the run blocked and stop. A screenshot you did not take, a unit test, or a source reading is not a UI repro.

Require the adapter capabilities the surface needs: bring up, drive the real UI, inspect state without mutating it, capture evidence, and clean up. If a required capability is missing, stop.

## 6. Study the report

Read the source and the tracker issue when present. Collect the action path, expected and observed behavior, the state where they diverge, frequency, version, attachments, and the candidate code area.

Call the `skill` tool for `how` to trace the action through the repository. Call `why` for regression history. Form competing hypotheses and name the evidence that would separate them.

## 7. Reproduce

Bring up the target through the driver. Confirm the app, workspace, account, data set, and feature state before acting.

Drive the reported path through real UI actions.

Before calling it reproduced:

1. Name the correct final state.
2. Name the broken final state.
3. Reach the point where they diverge.
4. Observe the broken state.
5. Reset enough state to make the second attempt independent.
6. Repeat the same path and observe the same broken state again.
7. Cross-check a real state value when possible.

An expected dialog or loading state is not the bug. Use the configured repro budget. If the symptom does not appear twice, report `Could not reproduce`. If the environment cannot provide a required capability, report `Blocked` and state what was missing.

## 8. Evidence

For a successful repro, record the path, capture the broken final state, and keep artifacts in the configured temporary directory, outside the repository.

If you cannot show the discriminating broken state, the repro is not confirmed.

Post detailed evidence to an operations thread only when a Slack tool and that channel are both available. Otherwise put it in chat. Keep a source-channel update concise, and skip it when you cannot post.

## 9. Report the outcome

For `Could not reproduce` or `Blocked`, do not post in the source thread. Chat or the operations thread carries the result.

For a confirmed repro, post at most one source reply when a Slack tool is connected and the preflight passes. Otherwise return the same text in chat. Say the issue reproduced, link evidence, include at most three short findings, and link the tracker issue when one exists. Do not ping an owner by default.

Do not wait out a rejection window. If the human says the setup was wrong, correct the repro once. Do not start a fix until they accept the repro or the conversation already treats it as accepted.

## 10. Verify an existing fix

When a fix artifact exists, follow `references/verify-existing-fix.md`. Show the symptom on the baseline and its absence on the patched build. Both paths use the real UI twice. Do not edit the existing fix or open a replacement pull request.

## 11. Qualify a bounded fix

Attempt a fix only when all of these hold:

- The outcome is a plain confirmed repro.
- Evidence shows the broken final state.
- No existing fix artifact appeared.
- No person claimed the fix.
- Runtime evidence identifies the root cause.
- The likely change fits the configured fix budget and repository scope.
- The driver can run both baseline and patched builds.

If any condition fails, keep the repro report and stop without a pull request.

## 12. Root-cause and implement

You own the final diff review, commits, and the pull request.

Confirm the mechanism with runtime evidence. Eliminate competing hypotheses before editing. Fix the root cause with the smallest justified change.

Call the `skill` tool for `tdd` when there is a cheap local test target, and write the failing test before the fix. State why TDD was skipped when the path is expensive, unclear, or integration-heavy. Keep unrelated cleanup out. Stop if the change grows beyond the configured budget.

## 13. Prove the fix

Keep the original baseline evidence. On the patched build, run the same real UI path twice, show the broken state is gone, show the expected state, capture after evidence, and cross-check the same state value. A compile, unit test, or plausible diff is not after evidence.

Run focused tests, then smoke the blast radius. Stop without a pull request if a regression remains.

## 14. Open a draft pull request

Only after before-and-after proof:

- Review the diff for unrelated changes and secrets.
- Run the repository's required checks.
- Create small ordered commits when the repository workflow allows it.
- Open a draft pull request. Never merge or deploy.
- Link the tracker issue using the tracker's supported syntax.
- Use the configured public URL form, normally `https://github.com/{owner}/{repo}/pull/{number}`.
- Include the repro steps, root cause, test result, before and after evidence, and blast-radius checks.
- Call the `skill` tool for `unslop` on the pull request text and any Slack update.

If pull request creation fails, do not claim success. Say the branch state and mark status `Fix did not land`.

On success, mark status `Draft pull request opened` and give the link in chat, or in the operations thread when a Slack tool can post there. Do not create a source-channel root message.

## 15. Clean up

Call the driver's cleanup. Keep artifacts only as long as the configured retention policy allows. Do not watch a thread after you hand back. There is no scheduler.
