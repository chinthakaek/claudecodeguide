# Claude Code: A Beginner's Guide and Best Practices

> A hands-on guide for people new to **Claude Code**, Anthropic's AI coding assistant that runs in your terminal.
> Checked against Claude Code **v2.1.x**. Features change often. Run `claude --help` or `/help` to see what your version has.

---

## Table of Contents

1. [What is Claude Code?](#1-what-is-claude-code)
2. [Installation & First Run](#2-installation--first-run)
3. [Your First Session](#3-your-first-session)
4. [Core Concepts](#4-core-concepts)
5. [Essential Keyboard Shortcuts & Input Tricks](#5-essential-keyboard-shortcuts--input-tricks)
6. [Slash Commands You'll Actually Use](#6-slash-commands-youll-actually-use)
7. [Permission Modes: Staying in Control](#7-permission-modes-staying-in-control)
8. [Memory: CLAUDE.md & Auto-Memory](#8-memory-claudemd--auto-memory)
9. [Command-Line Usage (Flags & Scripting)](#9-command-line-usage-flags--scripting)
10. [Managing Context & Sessions](#10-managing-context--sessions)
11. [Extending Claude Code](#11-extending-claude-code)
12. [Best Practices](#12-best-practices)
13. [Effective Prompting Patterns](#13-effective-prompting-patterns)
14. [Safety & Security](#14-safety--security)
15. [Troubleshooting](#15-troubleshooting)
16. [Quick Reference Cheat Sheet](#16-quick-reference-cheat-sheet)

---

## 1. What is Claude Code?

Claude Code is an **agentic** coding tool. It is more than a chatbot that hands you snippets. It can:

- **Read and search** your codebase to understand how it works
- **Edit files** directly, across many files at once
- **Run commands** such as tests, builds, linters, and git
- **Plan and carry out** multi-step tasks, checking its own work as it goes
- **Connect to outside tools** (GitHub, Jira, databases, browsers) through MCP servers

Think of it as a capable pair programmer who works in your terminal, with your files, and with your permission.

It also runs in an IDE (VS Code, JetBrains), the desktop app, and on the web (claude.ai/code). This guide covers the **CLI**, but most of the ideas apply everywhere.

---

## 2. Installation & First Run

### Install

**Native installer (recommended):**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Or with npm** (needs Node.js 18+):
```bash
npm install -g @anthropic-ai/claude-code
```

### Verify and log in
```bash
claude --version     # confirm it's installed
claude doctor        # check your install is healthy
cd ~/my-project      # go to a project folder
claude               # start; the first run walks you through login
```

You can log in with a Claude subscription (Pro/Max/Team/Enterprise) or an Anthropic Console (API) account. Your organization may also set it up to use Amazon Bedrock, Google Vertex AI, or Microsoft Foundry.

### Keep it updated
```bash
claude update
```

> 💡 **Tip:** Always start Claude Code **from your project's root folder**. Claude can only see that folder (and any folders you add) by default.

---

## 3. Your First Session

Here is a good first ten minutes in a new project:

```text
> what does this project do? give me a high-level overview

> where is the main entry point, and how is the code organized?

> /init
```

`/init` looks at your codebase and writes a `CLAUDE.md` file, which is Claude's notes about your project (see [Section 8](#8-memory-claudemd--auto-memory)). Read it, fix anything wrong, and commit it.

Then try a small, real task:

```text
> the README's setup instructions are out of date. check package.json and update them
```

Watch what Claude does. It reads files, proposes edits, and **asks permission** before changing anything or running commands. You approve, reject, or redirect it.

---

## 4. Core Concepts

| Concept | What it means |
|---|---|
| **Session** | One conversation. Claude remembers everything said in it. |
| **Context window** | How much Claude can "hold in mind" at once. Long sessions fill it up. |
| **Tools** | Actions Claude can take: Read, Edit, Write, Bash, search, web fetch, and so on. |
| **Permissions** | Rules for which tools Claude may use without asking you. |
| **CLAUDE.md** | An instructions file you write. It's loaded at the start of every session. |
| **Auto-memory** | Notes Claude saves for itself (your preferences, corrections) that carry across sessions. |
| **Subagents** | Helper agents Claude can start for focused side tasks, each with its own context. |
| **Skills / slash commands** | Saved, reusable instructions, run with `/name`. |
| **MCP servers** | Plugins that connect Claude to outside systems. |
| **Hooks** | Shell commands that run automatically at set points (for example, after every file edit). |

---

## 5. Essential Keyboard Shortcuts & Input Tricks

| Key / Syntax | What it does |
|---|---|
| `Enter` | Send message |
| `Shift+Enter` or `\` + `Enter` | New line (multi-line prompt). Run `/terminal-setup` if Shift+Enter doesn't work. |
| `Esc` | **Stop Claude** mid-action. Nothing is lost, so you can redirect it. |
| `Esc` `Esc` | **Rewind**: jump back to an earlier message (and optionally undo code changes) |
| `Shift+Tab` | Cycle permission modes (normal → auto-accept edits → plan mode …) |
| `Ctrl+C` | Cancel current input. Press twice to exit. |
| `Ctrl+R` | Search prompt history |
| `↑` / `↓` | Scroll through previous prompts |
| `@path/to/file` | **Mention a file or folder** so Claude reads it (with tab-completion) |
| `!command` | **Run a shell command yourself**; the output goes into the conversation |
| `/` | Open the slash-command and skill menu |
| Drag & drop / paste | Add **images** (screenshots, mockups, diagrams) |

> 💡 `Esc` is your best friend. If Claude heads the wrong way, interrupt early. Don't wait for it to finish.

---

## 6. Slash Commands You'll Actually Use

Type `/` in a session to see every command. These are the main ones:

| Command | Purpose |
|---|---|
| `/help` | List commands and help |
| `/init` | Create a `CLAUDE.md` for the project |
| `/clear` | **Start fresh**: wipe the conversation context |
| `/compact [focus]` | Summarize the conversation to free up context, e.g. `/compact keep the API design decisions` |
| `/context` | See what's filling your context window |
| `/model` | Switch model (e.g. Opus for hard problems, Sonnet/Haiku for speed) |
| `/resume` | Pick up a previous session |
| `/rewind` | Go back to an earlier point in the conversation or code |
| `/permissions` | View and edit which tools are allowed |
| `/memory` | Edit your CLAUDE.md memory files |
| `/config` | Open settings (theme, model, and more) |
| `/cost` / `/usage` | See token usage and spend |
| `/mcp` | Manage MCP server connections |
| `/agents` | Create and manage custom subagents |
| `/hooks` | Configure hooks |
| `/code-review` | Review your current changes for bugs |
| `/security-review` | Security-focused review of pending changes |
| `/doctor` | Diagnose installation problems |
| `/bug` | Report a problem to Anthropic |

---

## 7. Permission Modes: Staying in Control

By default, Claude **asks before** editing files or running commands. You can change this.

| Mode | Behavior | When to use it |
|---|---|---|
| **Default (manual)** | Asks before edits and most commands | Learning, unfamiliar code, risky work |
| **Accept Edits** | Edits files without asking; still asks before shell commands | You trust the direction and want speed |
| **Plan Mode** | **Read-only.** Claude explores and writes a plan but changes nothing | Big or unclear tasks. Agree on the plan first. |
| **Auto** | Claude decides when to proceed, with safety checks | Experienced users on routine work |
| **Bypass Permissions** | Never asks | **Only** in throwaway sandboxes or containers |

Switch modes with **`Shift+Tab`** during a session, or at launch:
```bash
claude --permission-mode plan
```

### Allow-listing trusted commands
When Claude asks to run something, you can choose "always allow". You can also set rules in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint)",
      "Bash(git status)",
      "Bash(git diff:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Read(./.env)",
      "Read(./secrets/**)"
    ]
  }
}
```

> 💡 Run `/fewer-permission-prompts` to build an allow-list automatically from commands you approve often.

### Settings file locations
| File | Scope | Commit to git? |
|---|---|---|
| `~/.claude/settings.json` | You, across all projects | n/a |
| `.claude/settings.json` | This project, shared with the team | ✅ Yes |
| `.claude/settings.local.json` | This project, just you | ❌ No |

---

## 8. Memory: CLAUDE.md & Auto-Memory

Every session starts with a blank slate. Claude Code has two ways to carry knowledge from one session to the next:

| | **CLAUDE.md** | **Auto-memory** |
|---|---|---|
| Who writes it | **You** (Claude can help) | **Claude**, as it learns |
| What it holds | Instructions: commands, rules, architecture | Facts: your preferences, corrections, project context |
| Shared with team? | Yes (project CLAUDE.md is committed) | No, it's private to you and stored on your machine |
| Loaded | In full, every session | An index every session; the details when relevant |

### 8.1 CLAUDE.md: Teaching Claude About Your Project

`CLAUDE.md` is loaded into **every session** automatically. Use it to tell Claude what it can't easily work out from the code.

#### Where it can live
| Location | Applies to |
|---|---|
| `~/.claude/CLAUDE.md` | All your projects (personal preferences) |
| `./CLAUDE.md` (project root) | Everyone on this project (commit it) |
| `./CLAUDE.local.md` | Just you, this project (git-ignore it) |
| `./some/subfolder/CLAUDE.md` | Loaded when Claude works in that folder |

#### What to put in it
```markdown
# Project: Payments Service

## Commands
- Build: `make build`
- Test all: `make test`
- Test one file: `pytest tests/test_x.py -k name`
- Lint: `make lint` (must pass before committing)

## Architecture
- `api/` – FastAPI routes; `core/` – business logic; `db/` – SQLAlchemy models
- Never call the DB directly from routes; go through `core/` services

## Conventions
- Python 3.12, type hints required, use `pydantic` v2 models
- Tests use pytest fixtures in `tests/conftest.py`, not unittest
- Branch names: `feature/<ticket>-short-desc`

## Gotchas
- `settings.py` reads from env; tests need `ENV=test`
- The `legacy/` folder is frozen. Do not modify.
```

#### Importing other files
CLAUDE.md can pull in other files with `@`, so it stays short while you keep detail elsewhere:
```markdown
See @README.md for an overview and @docs/api-conventions.md for API rules.
- Git workflow: @docs/git-workflow.md
```

#### Tips
- ✅ **Keep it short and specific.** Bullet points beat paragraphs. It costs context every session.
- ✅ Include **exact commands** for build, test, and lint. This helps Claude check its own work.
- ✅ Write down **gotchas** and "don't do X" rules.
- ✅ Update it whenever you catch yourself correcting Claude about the same thing twice.
- ✅ Use `/memory` to open and edit any of your memory files quickly.
- ❌ Don't paste whole docs or describe what's obvious from the code.
- ❌ Never put secrets in it.

### 8.2 Auto-Memory: What Claude Learns Over Time

Claude Code also keeps its own **persistent memory**. When you tell it something worth remembering, or it learns something non-obvious, it saves a small note that it can recall in future sessions.

#### How it works
- Memories are stored per project, on your machine, under `~/.claude/projects/<project>/memory/`.
- Each memory is **one small Markdown file holding one fact**.
- A `MEMORY.md` file acts as an **index** (one line per memory). The index is loaded at the start of each session, and Claude reads the full note when it's relevant.
- Memories can link to each other with `[[memory-name]]`.

#### Types of memory
| Type | Example |
|---|---|
| **user** | "Prefers TypeScript; is a backend engineer, new to React" |
| **feedback** | "Don't add docstrings to test functions. **Why:** team style. **How to apply:** only for public APIs" |
| **project** | "Code freeze for the v3 release starts 2026-12-15" |
| **reference** | "Bugs are tracked in Jira project PAY; dashboards at grafana.internal/payments" |

#### Example memory file
```markdown
---
name: prefer-pytest-fixtures
description: User wants pytest fixtures, never unittest-style setUp
metadata:
  type: feedback
---
Use pytest fixtures from tests/conftest.py instead of unittest setUp/tearDown.
**Why:** the team migrated off unittest in 2025; mixed styles fail review.
**How to apply:** any new or edited test file. See also [[test-commands]].
```

#### Using it
- **Ask directly:** *"remember that I prefer small PRs under 300 lines"* or *"forget what you saved about the staging URL."*
- **Correct Claude:** when you correct it, it may save that as feedback so it doesn't repeat the mistake.
- **Review it now and then:** open the memory folder (or ask *"what do you remember about me and this project?"*) and delete anything stale or wrong. Memories show what was true *when they were written*.
- **Turning it off:** auto-memory can be disabled in settings. Check `/config` or the docs for your version.

#### What does *not* belong in auto-memory
- Things the repo already records: code structure, git history, CLAUDE.md content
- Details that only matter for the current conversation
- Secrets or credentials

### 8.3 Which Mechanism Should I Use?

| You want… | Use |
|---|---|
| The whole team to follow a rule | **Project CLAUDE.md** (committed) |
| Your personal preferences in every project | **`~/.claude/CLAUDE.md`** or **auto-memory** |
| Claude to remember a correction or a fact it learned | **Auto-memory** ("remember that…") |
| A repeatable, multi-step procedure on demand | **A skill** ([Section 11.1](#111-skills)) |
| Something that must happen **every time**, no exceptions | **A hook** ([Section 11.4](#114-hooks)) |
| A focused helper with its own context and tools | **A subagent** ([Section 11.2](#112-subagents)) |

> 💡 **Memory and CLAUDE.md are guidance.** Claude reads them and usually follows them, but nothing enforces them. If something *must* happen (formatting, blocking a command), use a hook or a permission rule.

---

## 9. Command-Line Usage (Flags & Scripting)

### Starting sessions
```bash
claude                              # interactive session
claude "explain the auth flow"      # interactive, with a starting prompt
claude -c                           # continue the most recent session here
claude -r                           # pick a past session to resume
claude --model opus                 # choose a model
claude --effort high                # more thinking (low|medium|high|xhigh|max)
claude --add-dir ../shared-lib      # give access to another folder
claude -w my-feature                # work in an isolated git worktree
claude -n "bugfix-123"              # give the session a name
```

### Non-interactive / scripting mode (`-p`)
`-p` (print) runs one prompt, prints the result, and exits. It works well in scripts, CI, and pipes.

```bash
# One-off question
claude -p "what does src/utils/retry.ts do?"

# Pipe data in
cat error.log | claude -p "what's the root cause of this error?"
git diff | claude -p "write a concise commit message for this diff"

# Machine-readable output
claude -p "list all TODOs in src/" --output-format json

# Limit what it can do (good for CI)
claude -p "fix the lint errors" --allowedTools "Edit" "Bash(npm run lint)"

# Cap the spend
claude -p "triage these test failures" --max-budget-usd 2
```

### Useful subcommands
```bash
claude mcp add ...       # add an MCP server
claude mcp list          # list configured MCP servers
claude plugin ...        # manage plugins
claude doctor            # health check
claude update            # update to the latest version
claude agents            # list background sessions
```

---

## 10. Managing Context & Sessions

The context window is limited. As it fills, responses can get slower and less focused. **Managing context is the most important habit to build.**

| Situation | Do this |
|---|---|
| Starting an unrelated task | `/clear` |
| Long task, want to keep going | `/compact` (optionally with a focus) |
| Curious what's using space | `/context` |
| Coming back tomorrow | `claude -c` or `/resume` |
| Claude went down a wrong path | `Esc Esc` / `/rewind` to an earlier point |
| Need a big side investigation | Ask Claude to **use a subagent**, which keeps the main context clean |

> 💡 **Rule of thumb:** one task per session. `/clear` between tasks is cheap, and it beats dragging old, unrelated context along.

### 10.1 Saving work across sessions
For long projects, ask Claude to keep a progress file:
```text
> write our plan and progress so far to PLAN.md so we can pick up later
```
Next session: `> read PLAN.md and continue from where we left off`.

### 10.2 Before You Exit: End-of-Session Checklist

A minute spent wrapping up saves you from lost work, stray processes, and having to rebuild context next time.

| # | Step | How |
|---|---|---|
| 1 | **Check the work** | Review changes with `!git status` / `!git diff`, or ask *"summarize everything you changed this session"* |
| 2 | **Run tests and lint** | *"Run the tests and confirm they pass."* Don't leave the code half-broken. |
| 3 | **Check for leaked secrets** | Make sure no keys, passwords, or debug files were written into the project |
| 4 | **Save the work** | Commit, or at least `git stash`. Changes stay on disk, but a commit is a checkpoint you can return to. |
| 5 | **Leave a handoff note** | Have Claude write what was done and what's next (see below) |
| 6 | **Keep what you learned** | Add repeated corrections to `CLAUDE.md`; say *"remember that…"* for personal preferences (auto-memory) |
| 7 | **Stop background processes** | Dev servers or watchers Claude started, background sessions (`claude agents`, then `claude stop <id>`), recurring `/loop` tasks |
| 8 | **Tidy worktrees** | If you used `claude -w`, merge or remove the worktree so forgotten copies don't pile up |
| 9 | **Check usage** *(optional)* | `/cost` shows what the session used |
| 10 | **Exit** | `/exit`, `Ctrl+C` twice, or `Ctrl+D`. The conversation is saved, so you can resume it with `claude -c` / `claude -r`. |

#### Handoff note prompt
```text
> write a handoff to PLAN.md: what we did, decisions made and why, what's left,
  and any open questions or known issues
```
Next time: `> read PLAN.md and continue`. A written note is more dependable than a resumed session. It survives `/clear` and compaction, and teammates can read it.

#### Capturing lessons
```text
> add a rule to CLAUDE.md: we use pnpm, not npm
> remember that I prefer small PRs under 300 lines
```

> 💡 **Quick version:** review → test → commit → handoff note → update CLAUDE.md → stop background processes → `/exit`.

---

## 11. Extending Claude Code

You don't need any of this on day one. Come back once you're comfortable with the basics.

| Extension | What it is | Who triggers it |
|---|---|---|
| **Skills** | Saved instructions (plus optional scripts or reference files) | You (`/name`) or Claude, when the task matches |
| **Subagents** | Helper agents with their own context, prompt, and tools | Claude, or you on request |
| **MCP servers** | Connections to outside systems (GitHub, Jira, databases…) | Claude, through tools |
| **Hooks** | Shell commands run automatically on events | The harness. Guaranteed to run. |
| **Plugins** | Installable bundles of all of the above | Installed once, then always available |

### 11.1 Skills

A **skill** is a packaged set of instructions for a particular kind of task, such as "fix a GitHub issue", "write release notes", or "deploy to staging". Skills replace and extend the older "custom slash commands".

#### Where skills live
| Location | Scope |
|---|---|
| `~/.claude/skills/<name>/SKILL.md` | Personal: available in all your projects |
| `.claude/skills/<name>/SKILL.md` | Project: commit it to share with your team |
| Inside a plugin | Comes with the plugin ([11.5](#115-plugins)) |

#### Anatomy of a skill
A skill is a **folder**. `SKILL.md` is required; everything else is optional:
```text
.claude/skills/release-notes/
├── SKILL.md            # instructions + frontmatter (required)
├── template.md         # reference material Claude can read when needed
└── scripts/
    └── collect_prs.sh  # helper script Claude can run
```

#### SKILL.md example
```markdown
---
name: release-notes
description: Draft release notes from merged PRs since the last tag. Use when the user asks for release notes, a changelog, or "what shipped".
argument-hint: "[since-tag]"
allowed-tools: Bash(git log:*), Bash(gh pr list:*), Read, Write
---
Draft release notes for changes since $ARGUMENTS (default: the latest git tag).

1. Run `scripts/collect_prs.sh $ARGUMENTS` to list merged PRs.
2. Group them into Features, Fixes, and Internal, following `template.md`.
3. Write user-facing wording; skip purely internal refactors.
4. Save the result to `RELEASE_NOTES.md` and show me a summary.
```

#### Frontmatter fields
| Field | Purpose |
|---|---|
| `name` | The command name, run as `/release-notes` |
| `description` | **The most important field.** Claude reads it to decide when to use the skill on its own. |
| `argument-hint` | Shown in the `/` menu to suggest arguments |
| `allowed-tools` | Tools the skill may use without asking for permission |
| `disable-model-invocation` | `true` = only *you* can run it (good for deploys and other risky actions) |
| `model` | Run the skill on a specific model |

Inside the body, `$ARGUMENTS` is replaced with whatever you type after the command.

#### Two ways a skill runs
1. **You call it:** `/release-notes v2.3.0`
2. **Claude picks it:** you say *"what shipped this week?"* and Claude recognizes from the `description` that `release-notes` fits, then loads it.

#### Writing good skills
- ✅ **Write the description for Claude.** Say *what* it does and *when* to use it, using the words people actually say ("changelog", "what shipped").
- ✅ Keep `SKILL.md` focused. Put long reference material in separate files that Claude reads only when needed.
- ✅ Bundle **scripts** for steps that must be exact. A script is more reliable than prose instructions.
- ✅ Number the steps, and finish with a verification step (run tests, show a summary).
- ✅ Set `disable-model-invocation: true` on anything with side effects (deploys, sending messages).
- ❌ Don't make one giant "do everything" skill. Several small, well-described skills work better.

> 💡 Type `/` to see every skill available in the session. Built-in skills include `/code-review`, `/security-review`, `/simplify`, `/init`, and `/loop`.

### 11.2 Subagents

A **subagent** is a separate Claude instance that Claude can hand a focused task to. It works in **its own context window** and returns only a summary, so your main conversation stays clean.

#### When subagents help
- ✅ Broad research: *"find every place we call the payments API"* (many files, but you only need the answer)
- ✅ Independent tasks run **in parallel**
- ✅ A **fresh-eyes review** that isn't biased by the main conversation
- ❌ Not worth it for small lookups you could do in one or two steps. Each subagent costs extra tokens, and some detail is lost in the handoff.

#### Using them
Just ask: *"use a subagent to investigate how session caching works and report back."* Built-in types include a general-purpose agent, a read-only **Explore** agent for searching, and a **Plan** agent for designing implementations.

#### Defining your own
Create one with `/agents` (interactive), or add a file to `.claude/agents/` (project) or `~/.claude/agents/` (personal):

```markdown
---
name: test-writer
description: Writes thorough unit tests for a given module. Use after implementing new code or when coverage is missing.
tools: Read, Grep, Glob, Write, Bash(npm test:*)
model: sonnet
---
You are a meticulous test engineer.
- Read the target module and its existing tests first.
- Cover happy paths, edge cases, and error handling.
- Follow the conventions in tests/README.md. No mocking of internal modules.
- Run the tests and make sure they pass before reporting.
- Report: files created, cases covered, and any bugs you found.
```

| Field | Purpose |
|---|---|
| `name` | How you and Claude refer to it |
| `description` | When Claude should use it (Claude reads this to decide) |
| `tools` | **Limit** what it can do. A reviewer might only get read-only tools. |
| `model` | Use a cheaper or faster model for simple roles, a stronger one for hard ones |

You can also start a whole session as an agent: `claude --agent test-writer`.

### 11.3 MCP Servers

**MCP (Model Context Protocol)** servers give Claude new tools that connect to outside systems.

```bash
# Add a remote (HTTP) server
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Add a local server that runs as a process
claude mcp add my-db -- npx -y @example/postgres-mcp postgresql://localhost/dev

# Manage
claude mcp list
claude mcp remove my-db
```

- Inside a session, `/mcp` shows server status and handles login (OAuth).
- Share servers with your team through a project `.mcp.json` file.
- **Only add servers you trust.** They can read data and take actions for you.

### 11.4 Hooks

Hooks are shell commands the harness runs **automatically** at set points. Unlike CLAUDE.md, they always run.

#### Common events
| Event | Fires when | Example use |
|---|---|---|
| `PreToolUse` | Before a tool runs (can **block** it) | Block edits to `legacy/`, or block `git push --force` |
| `PostToolUse` | After a tool runs | Auto-format edited files, run the linter |
| `UserPromptSubmit` | When you send a prompt | Add context, such as the current ticket |
| `Stop` | When Claude finishes responding | Play a sound, or send a desktop notification |
| `SessionStart` | When a session starts | Load environment info |

#### Example: auto-format after edits
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write" }]
      }
    ]
  }
}
```
Hooks receive event details as **JSON on stdin** (tool name, inputs, and so on). A hook can block an action by exiting with a specific error code. See the docs for details.

Set hooks up with `/hooks`, or in any `settings.json` file. You can also just ask Claude: *"whenever you edit a Python file, run ruff on it."* It will configure the hook for you.

> ⚠️ Hooks run with **your** permissions. Review any hook before you enable it, especially ones from other people.

### 11.5 Plugins

A **plugin** bundles skills, subagents, hooks, and MCP servers into one installable package. Plugins come from **marketplaces** (a GitHub repo, a URL, or a local folder that lists plugins).

```bash
# Add a marketplace, then install from it
claude plugin marketplace add <github-org/repo or URL>
claude plugin install <plugin-name>@<marketplace>

# Manage
claude plugin list
claude plugin details <plugin>     # what's inside + estimated context cost
claude plugin disable <plugin>
claude plugin update <plugin>
claude plugin uninstall <plugin>

# Build your own
claude plugin init my-plugin       # scaffold a new plugin
claude plugin validate ./my-plugin
```
In a session, `/plugin` offers the same functions through menus.

**When to make a plugin:** once you have skills, agents, or hooks that several projects or teammates should share, bundle them so everyone installs one thing and stays in sync.

> ⚠️ Plugins can include hooks and MCP servers that run code on your machine. Install only from sources you trust.

---

## 12. Best Practices

### 🎯 1. Give Claude a way to check its own work
This is the **biggest** factor in quality. Claude does far better when it can verify results:
- Tell it how to run tests, the linter, and the type-checker (put this in CLAUDE.md)
- Ask it to **write tests first**, then make them pass
- For UI work, give it a screenshot target, or let it look at the page through a browser tool

### 🗺️ 2. Explore → Plan → Code → Commit
For anything bigger than a small fix:
1. **Explore**: "Read the auth module and related tests. Don't write code yet."
2. **Plan**: switch to **Plan Mode** (`Shift+Tab`) or say "make a plan." Review it and push back.
3. **Code**: "Go ahead and implement the plan. Run tests as you go."
4. **Commit**: "Commit this with a descriptive message" (and open a PR if you want).

Skipping the plan step on complex work is the most common beginner mistake.

### 📝 3. Be specific
| ❌ Vague | ✅ Specific |
|---|---|
| "fix the bug" | "Login fails with a 500 when the email has a `+`. Reproduce it with a test, then fix it." |
| "add tests" | "Add tests for `parseDate` in `utils/date.ts` covering invalid input, timezones, and leap years. Don't use mocks." |
| "make it better" | "Refactor `OrderService` to cut duplication between `create` and `update`. Keep the public API unchanged." |

### 📎 4. Give rich context
- Point to files with `@`: *"follow the pattern in @src/routes/users.ts"*
- Paste error messages, stack traces, and logs in full
- Drop in screenshots and mockups
- Share URLs to docs or issues
- Pipe data in: `cat data.csv | claude`

### 🛑 5. Course-correct early and often
- Press **`Esc`** as soon as it goes the wrong way
- Use **`Esc Esc`** to rewind and try a different prompt
- If you've corrected it twice on the same thing, `/clear` and start over with a better prompt. A clean start usually beats a cluttered context.

### 🧹 6. Keep context clean
- `/clear` between unrelated tasks
- Use subagents for broad research
- Keep CLAUDE.md short

### 🔁 7. Review everything
Claude is capable but can make mistakes. **You own the code you ship.**
- Read the diffs before you accept them
- Run `/code-review` before committing
- Be extra careful with security, data deletion, migrations, and money-related code

### 🌿 8. Use git as your safety net
- Work on a branch, and commit often so there's a checkpoint to return to
- Use **worktrees** (`claude -w name`) to run several Claude sessions on different tasks in parallel without clashes

### 🧠 9. Pick the right model and effort
- Hard design or debugging problems: a stronger model (`/model opus`) or higher `--effort`
- Simple or repetitive edits: a faster, cheaper model
- Watch spend with `/cost`

### 📚 10. Let Claude teach you
Claude Code is also a great way to learn a codebase:
- *"How does a request flow from the router to the database?"*
- *"Why was this written this way? Check git blame and history."*
- *"What are the edge cases in this function?"*

---

## 13. Effective Prompting Patterns

Copy and adapt these:

**Understand code**
```text
> explain how authentication works in this app. trace a login request end to end, with file references
```

**Fix a bug (test-first)**
```text
> users report <symptom>. first write a failing test that reproduces it, then fix it. don't change the test to make it pass
```

**Plan a feature**
```text
> I want to add CSV export to the reports page. explore the relevant code and propose a plan with the files you'd change. don't write code yet
```

**Refactor safely**
```text
> refactor @src/billing.ts to split it into smaller modules. behaviour must stay identical. run the tests before and after
```

**Code review**
```text
> review my uncommitted changes for bugs, edge cases, and anything that doesn't match the project's conventions
```

**Git workflow**
```text
> look at my changes, write a good commit message, and commit. then open a PR with a summary
```

**Ask for options**
```text
> what are 2–3 ways to implement rate limiting here? give pros and cons and your recommendation
```

**Interview me first** (good for vague requirements)
```text
> I want to build a notification system. ask me questions to clarify requirements before planning anything
```

---

## 14. Safety & Security

- 🔐 **Never paste secrets** (API keys, passwords) into prompts or CLAUDE.md. Use `deny` rules to block reading `.env` and secrets files.
- 👀 **Read commands before approving them**, especially ones that delete, push, deploy, or touch production.
- 🚫 **Avoid `--dangerously-skip-permissions`** except in isolated, disposable containers with no access to sensitive systems.
- 🧪 **Be wary of untrusted content.** Files, web pages, or issues from unknown sources can contain hidden instructions (prompt injection). Review what Claude wants to do after it reads them.
- 🌿 **Work on branches** and review diffs before merging.
- 🏢 **Follow your organization's policies** on which code and data can be shared with AI tools.

---

## 15. Troubleshooting

| Problem | Try |
|---|---|
| Something seems broken | `claude doctor` or `/doctor` |
| Claude is slow or losing focus | `/context` to check usage, then `/compact` or `/clear` |
| Claude keeps making the same mistake | Add a rule to CLAUDE.md, or `/clear` and re-prompt more clearly |
| Too many permission prompts | Add allow rules with `/permissions`, or use Accept Edits mode |
| Shift+Enter doesn't add a new line | `/terminal-setup` |
| MCP server not working | `/mcp` to check status and re-authenticate; `claude --debug mcp` |
| Login or auth problems | `claude auth` / `/login` / `/logout` |
| Outdated version | `claude update` |
| Want to report a bug | `/bug` |

---

## 16. Quick Reference Cheat Sheet

```text
┌──────────────────────────────── STARTING ────────────────────────────────┐
│ claude                  start interactive session                        │
│ claude -c               continue last session                            │
│ claude -r               resume a past session                            │
│ claude -p "prompt"      one-shot, print and exit (scripts/CI)            │
│ claude -w name          isolated git worktree session                    │
├──────────────────────────────── BEFORE EXIT ─────────────────────────────┤
│ review → test → commit → handoff note → update CLAUDE.md → /exit         │
├──────────────────────────────── IN-SESSION ──────────────────────────────┤
│ Esc                     stop Claude                                      │
│ Esc Esc                 rewind to earlier message                        │
│ Shift+Tab               cycle modes (normal / accept edits / plan)       │
│ @file                   reference a file                                 │
│ !cmd                    run shell command yourself                       │
│ Shift+Enter             new line                                         │
├──────────────────────────────── COMMANDS ────────────────────────────────┤
│ /init      create CLAUDE.md        /clear     reset context              │
│ /compact   summarize context       /context   view context usage         │
│ /model     switch model            /resume    resume session             │
│ /permissions  tool rules           /memory    edit CLAUDE.md             │
│ /code-review  review changes       /cost      usage & spend              │
│ /mcp       integrations            /agents    subagents                  │
│ /hooks     automation              /plugin    install plugins            │
│ /          list skills & commands  /help      everything else            │
├──────────────────────────────── GOLDEN RULES ────────────────────────────┤
│ 1. Give Claude a way to verify (tests, lint, screenshots)                │
│ 2. Explore → Plan → Code → Commit                                        │
│ 3. Be specific; give context with @files, errors, images                 │
│ 4. Interrupt early; /clear often                                         │
│ 5. Keep CLAUDE.md short; review auto-memory now and then                 │
│ 6. Review every diff. You own the code.                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Further Reading

- Official docs: https://docs.claude.com/en/docs/claude-code/overview
- Best practices (Anthropic engineering blog): https://www.anthropic.com/engineering/claude-code-best-practices
- In the CLI: `claude --help` and `/help`
- Or just ask Claude Code: *"how do I set up a hook that runs tests after edits?"* It can answer questions about itself.
