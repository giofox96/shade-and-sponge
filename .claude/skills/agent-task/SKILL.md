---
name: agent-task
description: Take one GitHub issue labelled `agent-ready`, do it with the matching subagent, fact-check the result and open a PR. Use when the user or a scheduled routine says "/agent-task" or "/agent-task <issue number>".
---

# One issue → one PR

Repo: `giofox96/shade-and-sponge`. GitHub: in cloud sessions use the GitHub MCP tools (`mcp__github__*`, load them with ToolSearch); locally use `gh` if it is installed.

1. **Pick.** If an issue number was given, use it. Otherwise take the open issues labelled `agent-ready` and not `in-progress`, and choose `priority-1` before `priority-2` before `priority-3`, oldest first. If there are none, reply "queue empty" and stop.
2. **Claim.** Add the label `in-progress` and comment "Picked up by an agent session."
3. **Gate.** If the issue asks to build the design tool (runoff/heat module, optimiser, Grasshopper component) and CLAUDE.md does not say `Methodology status: DEFINED`, do not start. Comment why, swap `agent-ready` for `needs-user`, and stop.
4. **Branch.** Use the branch the session was given; otherwise create `claude/issue-<n>-<slug>` from the latest `main`. Never commit to `main`.
5. **Do.** Read the issue's comments and, if it exists, its section in `notes/agent_backlog_status.md`. A later rescope (a "Rescoped" comment, or that section) overrides the issue body where they differ. Delegate to the subagent on the issue's `Agent role:` line (`lit-scout`, `data-scout` or `method-critic`) and pass it the issue body plus the rescope. Independent parts of one issue may go to several subagents in parallel.
6. **Check.** Run the `fact-checker` subagent on `git diff main`. Fix every ❌ and ⚠️ or remove the claim. Keep "(abs)" marks.
7. **Deliver.** Commit (message ends with `Refs #<n>`), push the branch, and open a PR titled like the issue, with "Closes #<n>". In the PR body: what was found, what is still missing, the fact-check summary, and at most one question for the user.
8. **Release.** Remove `in-progress`. If the task is blocked (needs a user decision, a blocked host, a paywalled paper, data on request), add `needs-user` and say exactly what is needed in an issue comment.

One issue per run. If the "Done when" criterion cannot be met, deliver what is verified and say so; never fill a gap with invented values.
