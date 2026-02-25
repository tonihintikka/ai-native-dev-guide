# 01 — What Changed

## The old model

For most of software development's history, the job looked like this:

1. Understand the problem
2. Write code to solve it
3. Test it
4. Fix what's broken
5. Ship it

You were the author. Every line had to pass through your hands and your head.

AI tools entered as autocomplete — smarter IntelliSense. They helped you type faster. The mental model stayed the same: you write code, the tool assists.

---

## What's different now

The shift isn't that AI writes code faster. The shift is that **you no longer have to be the one writing the code at all**.

You describe what you want. An agent reads your codebase, plans an approach, writes the code, runs the tests, hits an error, adjusts, and tries again — without you driving each step.

This is not autocomplete. This is delegation.

The developer's job is moving upstream:
- From writing implementations to defining requirements clearly
- From debugging line by line to reviewing agent output
- From knowing every API to knowing which agents to use and how to direct them

---

## Why 2025–2026 is the inflection point

A few things converged:

**Models got capable enough.** Claude 4, GPT-4o, and similar models can hold large codebases in context, reason about multi-file changes, and catch their own mistakes. Earlier models couldn't.

**Tool use became real.** Agents can now run shell commands, read files, call APIs, browse the web, and interact with your dev environment. They're not just generating text — they're taking actions.

**The tooling caught up.** Claude Code, Cursor, Windsurf, and others are built around agentic loops, not just chat. The workflow has matured enough to be learnable and repeatable.

**Context windows expanded.** 200k tokens means an agent can read your entire codebase, your error logs, your documentation, and still have room to reason. This changes what's possible.

---

## What this looks like in practice

Here's a real example from this repo. One person, one prompt:

> "I am planning to do a Python analytics script about Finnish city inhabitants. Could you please check where you can get this information. And please gather that to a SQLite database such way that you can make very nice looking graphics about data to a generated HTML report. Use VENV for Python libraries."

One prompt. The agent found the official Statistics Finland PXWeb API, validated the correct table and dimensions, scaffolded a complete project structure, wrote an ETL pipeline, normalized the data into three SQLite tables, built an interactive Plotly HTML report, ran it, and validated: 308 municipalities, 10,780 rows, 35 years of data.

No schema decisions. No API documentation handed over. No library choices specified. The prompt described an outcome. The agent resolved every detail.

That's the shift. See the result in [`pythonaidemo/`](../pythonaidemo/).

---

## What this means for you

You don't need to stop writing code. Some things you'll always want to write yourself — the tricky bits, the parts that encode business logic only you understand, the places where taste matters.

But the ratio shifts. A developer who works well with agents produces output that would have taken a team. Not because they're smarter, but because they've learned to orchestrate.

The developers who adapt fastest aren't the ones who know the most about AI. They're the ones who are clear thinkers and clear communicators — because that's what directing an agent requires.

---

## The mental model shift

| Old model | New model |
|---|---|
| You write code | You direct agents that write code |
| You debug failures | You review agent work and catch mistakes |
| You know every detail | You define intent and verify output |
| Productivity = typing speed | Productivity = quality of direction |
| Tools assist you | Agents work alongside you |

---

## What hasn't changed

- Bad requirements produce bad software, whether a human or agent builds it
- You still need to understand what you're building and why
- Code review still matters — maybe more, because the volume is higher
- Security, correctness, and maintainability are still your responsibility

The agent doesn't own the outcome. You do.

---

Next: [02 — Core Concepts](../02-core-concepts/) — what agents, tools, and context actually mean in practice.
