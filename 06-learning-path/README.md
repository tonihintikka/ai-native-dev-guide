# 06 — Learning Path

What to learn next, and in what order. Roughly three stages.

---

## Stage 1: Get comfortable (weeks 1–4)

The goal is building the habit. Not mastery — daily familiarity.

**Do these things:**

- [ ] Use Claude Code (or Cursor) on one real task every workday
- [ ] Write a `CLAUDE.md` for every project you touch
- [ ] Practice the architecture-first pattern on your next feature
- [ ] Review the agent's output critically — don't just accept it

**Understand these things:**

- What a context window is and why it matters
- The difference between prompting a chatbot and tasking an agent
- How to tell when an agent is going off track

**Signs you're through Stage 1:**

- You naturally reach for Claude Code when starting a task
- You notice when your prompts are too vague and can fix them
- You've caught at least one significant agent mistake in code review

---

## Stage 2: Deepen the practice (months 2–4)

The goal is developing real skill, not just using the tools.

**Skills to build:**

**Better prompting.** Learn to write prompts that give agents the right constraints. Specificity, scope, definition of done. Study your own prompt history — what worked and what didn't?

**Context management.** Understand how to structure long-running tasks so the agent doesn't lose track. CLAUDE.md, handoff summaries, incremental commits.

**Agent evaluation.** Get sharper at reviewing AI-generated code. What patterns indicate the agent misunderstood? Where does it typically make mistakes? (Usually: error handling, edge cases, and tests.)

**MCP basics.** Set up at least one MCP server — GitHub, Linear, or a database connector. Experience firsthand what it means for an agent to have access to external tools.

**Things to build:**

- A complete feature, from planning to PR, using agents throughout
- A simple custom tool or script using the Claude API
- A `CLAUDE.md` template you use across all new projects

**Resources to go deeper:**

See [RESOURCES.md](../RESOURCES.md) for specific links.

---

## Stage 3: Expand your capabilities (months 4+)

The goal is building things others can't — not just using agents on your own work, but architecting systems with agents at the core.

**Advanced topics:**

**Multi-agent systems.** How do you coordinate multiple agents on a single complex task? How do you handle failures in one agent without losing the whole pipeline? Start with the parallel agents pattern from [05 — Workflows](../05-workflows/) and push further.

**Evals.** How do you know if your agent is working well? Evaluation (evals) means building test cases for agent behavior — not just "did it run" but "did it do the right thing." This is where production AI systems diverge from prototypes.

**Building with the API.** Move from using agents to building products that include agents. Learn the Anthropic SDK, tool use, streaming, and how to structure agent loops properly.

**Prompt engineering at depth.** Chain-of-thought, few-shot examples, structured outputs, system prompts, prompt caching. These become important when you're building something that needs to work reliably.

**Security.** Prompt injection, data leakage, unauthorized actions. When you build agents that take real actions in real systems, security stops being theoretical. Understand the risks before you're in production.

**Domain-specific agents.** The highest value comes from agents that know your domain deeply — your codebase, your APIs, your internal processes. This means custom CLAUDE.md files, custom MCP servers, and tuned prompts.

---

## Career path

This guide covers the technical skills. But at some point, those skills need to translate into work. Here is what that looks like.

### Freelancer vs. employment

Both are viable. They have different tradeoffs.

**Freelancing** gives you a fast start. You can pick up your first client before you would ever get a junior job offer. Typical clients are small businesses and early-stage startups — they need someone to build or automate something specific. You do not need a degree. You need to show you can deliver.

The challenge: you are also responsible for finding clients, selling yourself, and keeping the pipeline full. That is a separate skill from building software.

**Employment** is more stable, but the junior market is competitive. Most roles are listed as "AI engineer" or "software engineer" — not "agentic developer." Search for companies that explicitly mention LLMs, agentic systems, Claude, Anthropic, OpenAI, or similar in their job descriptions. Those companies understand what you are building toward.

In both cases: your portfolio matters more than your degree.

---

### What to build for your portfolio

Three projects is enough. You do not need ten.

A strong portfolio project has four qualities:

1. It solves a real problem — not a toy example
2. It is deployed and accessible online — not just running on your laptop
3. The code is on GitHub
4. It has a README that explains what it does and how you built it with agents

**Example project types:**

- A web application with an AI feature (summarization, Q&A, generation)
- A data pipeline that processes and extracts insight from real inputs
- An automated tool for a specific industry (scheduling, research, document handling)

The demo projects in this guide — `aidemo` and `pythonaidemo` — are good starting points. Build on them, extend them, or use the same structure for something you care about.

---

### Where to find work

**If you are freelancing:**

- Upwork — search "AI automation" or "LLM integration." Volume is high, competition is real, but clients are actively looking.
- Toptal — higher bar to get in, but higher rates and better clients.
- Direct outreach — email small businesses directly. Many do not know what is possible. A short, concrete message describing what you could automate for them gets more responses than a generic pitch.

**If you are looking for employment:**

- LinkedIn — search "AI engineer," "LLM developer," "agentic." Filter for companies that mention the tools you know.
- RemoteOK.com and WeWorkRemotely.com — remote-first job boards with tech-heavy listings.
- Hacker News "Who is Hiring" — posted monthly. Search the thread for "LLM," "agent," "Claude," "Anthropic." These postings often come from smaller companies that move faster.

**Networking:**

- Reddit: r/ClaudeAI, r/LocalLLaMA
- Twitter/X: follow Anthropic, Cursor, and AI startup accounts. The community is active and visible.
- Discord: many AI tool communities have servers with job channels and direct access to people building in the space.

---

### Realistic timeline

Six to twelve months of consistent practice is a realistic estimate for landing your first freelance project or junior interview. Not four weeks.

That timeline shortens if you do these things:

1. Build and deploy a public portfolio project
2. Write about it — a LinkedIn post or a short blog explaining what you built and how
3. Reach out directly to small businesses, not just job boards

The noisiest path is also the slowest. Building something real, making it public, and telling people about it is faster than sending 200 applications.

---

## The skill that compounds most

Every stage has one skill that makes everything else better:

**Precision of thought.**

The better you can specify what you want — unambiguously, with the right constraints, clear scope, concrete success criteria — the better your agents perform. This isn't a new skill. It's the same clarity that makes you a good engineer, a good writer, a good manager.

Agents amplify what you bring. Sharp thinking produces sharp output. Vague instructions produce vague code.

The best investment is getting better at thinking clearly about what you actually want.

---

## Avoid these traps

**Over-relying on agents for decisions you should make.** An agent can explore options. You choose.

**Skipping code review.** Agents make mistakes. The volume they produce makes review more important, not less.

**Optimizing tools before optimizing practice.** Don't switch tools every time you hit friction. Most friction is prompting, not the tool.

**Building custom frameworks too early.** Use off-the-shelf tools until they genuinely don't fit. The overhead of custom solutions is real.

---

Next: [Resources](../RESOURCES.md) — the best external material to go deeper.
