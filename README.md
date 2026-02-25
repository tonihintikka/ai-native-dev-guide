# AI-Native Dev Guide

A practical guide for anyone who wants to build AI-powered applications and work in agentic engineering.

> Not theory. Not hype. What you actually need to start building with AI agents today.

---

## Who this is for

You want to build web applications and potentially work in the agentic engineering field. You might be a student, self-taught, or changing careers. You may have done some online courses — but you haven't shipped a production app yet, and the AI tooling landscape feels overwhelming.

This guide starts from the beginning.

**If you need to set up your environment first** (terminal, Git, Node.js, Python, API keys), start at [00 — Prerequisites](./00-prerequisites/).

**If your environment is ready**, start at [01 — What Changed](./01-what-changed/).

---

## What's inside

| Section | What you'll get |
|---|---|
| [00 — Prerequisites](./00-prerequisites/) | Terminal, Git, Node.js, Python, API keys. Everything you need before you start. |
| [01 — What Changed](./01-what-changed/) | The shift from coding to orchestrating. Why this moment is different. |
| [02 — Core Concepts](./02-core-concepts/) | Agents, tools, context, MCP, prompting. No fluff. |
| [03 — Your Toolbox](./03-your-toolbox/) | Claude Code, Cursor, Windsurf, Copilot, Codex CLI, OpenCode. When to use what. |
| [04 — First Agent](./04-first-agent/) | Build your first working agent. Step by step. |
| [05 — Workflows](./05-workflows/) | Real patterns: parallel agents, architecture-first, context management. |
| [06 — Learning Path](./06-learning-path/) | What to learn next, in what order, and how to turn it into a career. |
| [Resources](./RESOURCES.md) | Best links, docs, people to follow. |

---

## Demo projects

The repo includes two working examples you can run locally. Both were built in single agent sessions — one prompt each.

- [`aidemo/`](./aidemo/) — Flappy Bird in React + TypeScript + Node/Express. A quick one-prompt scaffold: full-stack structure, combined dev workflow, highscore API. Useful as a baseline for what a minimal agentic project looks like out of the box.
- [`pythonaidemo/`](./pythonaidemo/) — Finnish city population analytics. One prompt, no hand-holding: the agent found the official Statistics Finland API, designed the SQLite schema, wrote the ETL pipeline, and built an interactive Plotly HTML report. 308 municipalities, 10,780 rows, 35 years of data. See the full story in [04 — First Agent](./04-first-agent/).

These aren't polished products. They're honest examples of what a well-directed agent produces in a single session — no spec documents, no scaffolding help, just a clear goal.

---

## How to use this guide

Read sections in order if you're new to this. Jump around if you know what you're looking for.

Every section follows the same rule: if it doesn't help you do something, it doesn't belong here.

---

## Contributing

Open an issue or PR. The guide improves by staying close to what practitioners actually run into.

---

## Built with Claude Code

This guide was written and maintained using [Claude Code](https://claude.ai/code) — Anthropic's agentic coding tool. The content, structure, and demo projects were produced through agent sessions, not manually typed line by line.

That's intentional. A guide about agentic development should be built with agentic tools.
