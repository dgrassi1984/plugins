---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

Fan out N parallel workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

Call `skill` on `pstack-runtime` before the first spawn.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is the total number of workers.
4. Pick the worker model from the `swarm workers` line in `~/.dsh/pstack-models.md`. A missing file or missing line means `inherit-parent`. `inherit-parent` and `auto` omit `provider` and `model`. Pass `provider` and `model` only when the `subagent` tool schema exposes those fields and `list_subagent_models` lists that exact route. Otherwise omit them and say the child inherited the parent. When the schema exposes `reasoning_effort`, pass the effort recorded for that role only if the selected model advertises it. For a model race, name each arm's confirmed route up front. If a race arm has no confirmed route, that arm inherits the parent and you say so.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result. When a worker must start from a non-default branch, name that branch in its brief and tell it to check the branch out.

## Phase B: Fan out

Spawn all N workers in one message with `subagent` and the step 4 route, omitted when the child inherits the parent. The next step needs every result, so set `run_in_background: false`. The child does not see this conversation.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and rerun that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
