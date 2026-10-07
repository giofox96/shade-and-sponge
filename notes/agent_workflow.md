# Multi-agent workflow (set up 7 Oct 2026)

**Goal:** agents keep the research and data work moving while you are away. You stay the decision-maker: you write and label issues, review PRs, and take the methodology decisions.

```
GitHub Issue (agent-ready)
  → /agent-task (one cloud or local session)
      → subagent: lit-scout | data-scout | method-critic
      → fact-checker on the diff
  → PR on a claude/* branch  →  you review and merge (or comment)
  → blocked? label needs-user + a comment saying what is missing
```

## Pieces
| Piece | File | Role |
|---|---|---|
| Runner | `.claude/skills/agent-task/SKILL.md` | Picks one issue, claims it, delegates it, fact-checks it, opens the PR |
| `lit-scout` | `.claude/agents/lit-scout.md` | Answers one methodology question from the literature (uses `/lit-review`) |
| `data-scout` | `.claude/agents/data-scout.md` | Opens and checks one dataset and updates the data inventory |
| `method-critic` | `.claude/agents/method-critic.md` | Writes an options memo for one decision; you decide |
| `fact-checker` | `.claude/agents/fact-checker.md` | Read-only: checks every new number, citation and dataset claim |
| Issue template | `.github/ISSUE_TEMPLATE/agent-task.md` | Goal, why, files, steps, done-when |
| Cloud setup | `.claude/hooks/session-start.sh` + `requirements.txt` | Installs the Python deps in cloud sessions only |
| Gate | CLAUDE.md, `Methodology status:` line | `NOT DEFINED`: no design-tool code. Change it to `DEFINED` yourself |

**Labels:** `agent-ready`, `needs-user`, `in-progress`, `lit`, `data`, `analysis`, `tutor-question`, `priority-1` (for 20 Oct), `priority-2` (before tool building), `priority-3`.

## How to run it
1. **One task now:** in any session (cloud or local), type `/agent-task` (next in the queue) or `/agent-task 7` (a given issue).
2. **Several in parallel:**
   - Cloud: open one session per issue at claude.ai/code on this repo, each with `/agent-task <n>`.
   - Local (Windows): use one git worktree per task, so the sessions don't overwrite each other: `git worktree add ..\wt-7 -b claude/issue-7` then `cd ..\wt-7` and `claude "/agent-task 7"`.
3. **Unattended:** a scheduled routine that starts a fresh cloud session each night with the prompt `/agent-task`. Two or three routines at different times run up to three tasks a night.
4. **Your part, about 15 minutes a day:** merge or comment on the PRs, answer the `needs-user` issues, and add or relabel issues.

## One-time setup still needed
- [ ] **Merge the setup PR into `main`.** New sessions and routines start from `main`, so they only see the agents, skill and hook after the merge.
- [ ] **Allow the research hosts in the cloud environment.** The current network policy blocks them (tested 7 Oct). Edit the environment (session title bar → environment → Edit → Network access) and add these hosts: `api.openalex.org`, `api.semanticscholar.org`, `api.crossref.org`, `doi.org`, `opendata-ajuntament.barcelona.cat`, `urbisadmin.carto.com`, `planetarycomputer.microsoft.com`, `*.blob.core.windows.net` (Planetary Computer data), `www.icgc.cat`, `bcnroc.ajuntament.barcelona.cat`, `climate.onebuilding.org`, `freidok.uni-freiburg.de`, `data.comune.fi.it`. Alternatively, choose full network access. Web search and page fetches by the agents themselves still work without this.
- [ ] Create the first issues (backlog: `notes/agent_backlog.md`).

## What stays with you
Rhino / Grasshopper / Ladybug runs (`exchange/`), Zotero, paywalled PDFs (`notes/lit/to_get_manually.md`), sending data requests (`notes/data_requests.md`), methodology decisions (`notes/decisions/`), and the tutor.
