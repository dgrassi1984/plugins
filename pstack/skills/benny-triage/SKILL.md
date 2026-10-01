---
name: benny-triage
description: Triage one issue report when a human asks. Classify it, review evidence, trace the likely cause, dedupe a tracker ticket, and return one verdict. Use for a pasted report or a Slack thread the human names. There is no scheduler.
---

# Triage one issue report

A human asked you to triage one report. Do not watch a channel. Do not reproduce or fix the bug here.

Load `.dsh/benny/configuration.yaml` from the repository the human named. If that file is missing, malformed, or incomplete for a required field, stop and say what is missing. Do not post and do not write to the tracker.

If the report lives in Slack and no Slack tool is connected, stop and say so. Ask the human to paste the report. Do not invent a Slack client.

## Hard safety rules

- If Slack coordinates are in play, the source channel and root thread timestamp are immutable.
- Never post a root message in the source channel.
- Never post to another channel, broadcast a reply, send a DM, or start a replacement thread.
- If you will post, preflight the source parent before any tracker write and again immediately before the post.
- If the parent is missing, deleted, inaccessible, or uncertain, stop with no writes.
- One substantive verdict. Do not narrate progress.
- You are the only Slack poster, and only when a Slack tool is connected.
- A `subagent` may help. Load `pstack-runtime` before you spawn one. Its prompt must forbid Slack writes and must not receive Slack credentials. It returns findings only.
- If that isolation is uncertain, do the work yourself.
- Never create an issue that cannot link back to the source the human gave you.
- Prefer no ticket over a guessed or duplicate ticket.
- Call the `skill` tool for `principle-separate-before-serializing-shared-state` before you treat source coordinates as shared state.
- Call the `skill` tool for `principle-minimize-reader-load` and `unslop` before the final verdict.

## 1. Freeze the source

When the human pasted the report, the source is that paste. Record it. Do not invent a channel or timestamp.

When a Slack tool is connected and the human named a thread:

1. Read `source_channel_id` from the tool result.
2. Require it to equal the configured source channel.
3. Set `SOURCE_THREAD_TS` from the thread timestamp. Require it nonempty.
4. Store `SOURCE_CHANNEL_ID` and `SOURCE_THREAD_TS` as immutable values.
5. Read the thread and verify the root has those coordinates.
6. Fetch a stable permalink.

Every later read or post uses those stored values. Never replace them with a reply timestamp.

## 2. Read the whole report

Read the root and current replies, or the full paste, before deciding.

Capture reporter wording, version, environment, platform, expected behavior, observed behavior, frequency, trigger, error text, existing issue or pull request links, and any statement that someone is already fixing it.

Inspect attachments you can actually read. If an attachment cannot be read, say so. Do not invent what it shows.

## 3. Trace cause before routing

Call the `skill` tool for `how` and trace the path from the reported action to the observed result. Call `why` when the report looks like a regression or touches defensive code.

1. Identify the likely code path.
2. Check whether the visible symptom belongs to that path or a dependency below it.
3. Check recent changes when the report looks like a regression.
4. Check whether a merged commit or open pull request already addresses the same symptom.
5. Separate confirmed facts from hypotheses.

This pass does not need a complete root cause. It must be strong enough to avoid routing a visible symptom to the wrong owner.

If the repository cannot be read, do not guess a code owner. Continue with a conservative classification and say that cause tracing was unavailable.

## 4. Classify

Choose one category.

- **Bug.** Intended behavior is violated: wrong output, broken state, error, crash, hang, silent no-op, or regression.
- **Performance.** Measurable slowness, excess memory, battery drain, jank, or another resource problem. Treat it as a bug and keep the measurements.
- **Feature request.** Current behavior looks intentional and the reporter wants a different affordance.
- **Question or feedback.** How something works, a preference without a defect, or general feedback.
- **Reroute.** Cause tracing shows another configured destination owns it.

When the bug versus feature line is unclear, do not file. The verdict may ask one focused question and use the `other` marker.

## 5. Apply configured routing

Read the optional routing map from `routing.map_path` (usually `.dsh/benny/routing.md`). The example is `references/routing.example.md`.

- Match on confirmed product area, code path, or error signature.
- A visible symptom alone is not enough when cause tracing points elsewhere.
- If no route matches, say the owner is unclear. Do not guess.
- Do not cross-post. Tell the reporter where to take the issue in the verdict.

Owner pings are off by default. A ping is allowed only when a Slack tool is connected and all of these hold: the routing map names the owner, the config allows that ping type, the item needs that owner, and the owner is not a broad on-call group. Otherwise name the destination in the verdict and do not ping.

## 6. Use the tracker the session can call

The tracker is an adapter, not a required vendor. It must search, read, create, update without clobbering unrelated fields, add a source link, and cancel an issue this run created if the handoff fails.

If a required operation is unavailable, fail closed for that write. Do not invent IDs, labels, owners, or priority unless the config explicitly requires them.

## 7. Dedupe

If this source is already linked to a tracker issue or a prior triage reply, do not post or create a duplicate.

For bugs and performance reports, search by error signature, product area, trigger, symptom, version or date window, suspected regression commit, and source link.

- Confident duplicate: same signature, or the same area, trigger, and symptom, or a confirmed shared cause. Update the existing issue with the source link and one short recurrence note. Do not reopen or reassign it unless the config says to.
- Possibly related: link it in the verdict as uncertain and create nothing.
- Weak resemblance or no match: continue.

A long-closed issue is a regression lead, not automatically a live duplicate.

## 8. Decide whether to create

Create only when all of these are true:

1. The classification is bug or performance.
2. The behavior is clearly broken.
3. The issue is still live or not known to be fixed.
4. Dedupe found no confident or plausible live match.
5. The source passed preflight.
6. The tracker target fields resolved.
7. The adapter can compensate if a required Slack post fails.

Never create for a feature request, question, feedback item, reroute, possible duplicate, confident duplicate, or already-fixed issue.

The new issue must be self-contained: plain title, reporter quote, expected and observed behavior, version or `unknown`, trigger and frequency, source link, cause-tracing findings with hypotheses labeled as hypotheses, and the configured intake status and labels. Do not put a guessed root cause in the title.

## 9. One verdict

If a Slack post is required and no Slack tool is connected, stop and return the verdict in chat.

If a Slack tool is connected, preflight the source parent, then post exactly one reply with the stored channel and thread timestamp. Never post without a nonempty thread timestamp. After posting, read the thread and verify the reply landed under that timestamp. If it did not, do not retry at the root. If this run created a tracker issue and the verdict did not land, compensate and verify the compensation. If compensation cannot be verified, report that only to the human.

The verdict:

- Leads with the outcome.
- Links the tracker issue when there is one.
- Mentions a reroute or one missing fact when needed.
- Includes at most one allowed owner ping.
- Ends with exactly one configured marker line.

```text
[benny:bug]
[benny:bug] tracker=https://tracker.example/issue/123
[benny:performance]
[benny:performance] tracker=https://tracker.example/issue/123
[benny:other]
```

Use only the configured marker strings.

## 10. Stop

Do not watch the thread for a follow-up window. There is no scheduler. If the human pastes a correction later, triage that correction as a new request. Do not emit a second marker in this run.
