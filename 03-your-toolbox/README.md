# 03 — Your Toolbox

There are a lot of AI dev tools. This section cuts through the noise: what each major tool actually is, what it's good at, and when to reach for it.

---

## The landscape (as of early 2026)

Four categories:

1. **Terminal-based agents** — Claude Code, Codex CLI, OpenCode
2. **Editor-integrated agents** — Cursor, Windsurf
3. **In-editor assistants** — GitHub Copilot
4. **API + SDK** — Claude API, OpenAI API (for building your own)

---

## Claude Code

**What it is:** A terminal-based agentic coding tool from Anthropic. You run it in your shell, give it tasks in plain language, and it operates directly on your filesystem and codebase.

**Strengths:**
- Works in any project, any language, any editor
- Runs commands, reads files, edits code, runs tests — full agentic loop
- Transparent: you see every action it takes before it runs
- Tightly integrated with Claude's models (Claude 4 Sonnet, Claude 4 Opus)
- Supports MCP for extending capabilities
- `CLAUDE.md` file for persistent project context

**Best for:**
- Complex, multi-step tasks ("refactor this module, update the tests, fix what breaks")
- Working across many files at once
- Tasks that require running commands and seeing results
- When you want an agent, not an assistant

**Not ideal for:**
- Quick single-line edits where your editor is faster
- Teams where everyone needs a GUI

**How to start:** `npm install -g @anthropic-ai/claude-code` then `claude` in your project directory. Requires a claude.ai Pro plan ($20/month) or Anthropic API credits. Check current pricing at [anthropic.com/pricing](https://anthropic.com/pricing).

---

## Codex CLI

**What it is:** A terminal-based agentic coding tool from OpenAI. Similar to Claude Code in concept — you run it in your shell and give it tasks in plain language.

**Strengths:**
- Works with OpenAI models (GPT-4o, o3) and others
- Full agentic loop: reads files, runs commands, edits code
- Open source — you can inspect and modify the tool itself
- Option to bring your own model via API

**Best for:**
- Developers already in the OpenAI ecosystem
- When you want a Claude Code alternative with OpenAI models
- Experimenting with different model backends

**Not ideal for:**
- Teams who want the tightest Claude integration (use Claude Code)
- Complete beginners — setup requires comfort with the terminal

**How to start:** `npm install -g @openai/codex` then `codex` in your project directory. Requires an OpenAI API key.

---

## OpenCode

**What it is:** An open-source terminal-based coding agent. The key difference: you choose your own model. Claude, GPT-4o, local models via Ollama — OpenCode doesn't care.

**Strengths:**
- Model-agnostic: run any model that has an API
- Fully open source — no vendor lock-in
- Can run entirely locally with local models (no API costs)
- Active community development

**Best for:**
- Developers who want to experiment with different models without switching tools
- Privacy-conscious setups where data shouldn't leave your machine
- When you want to run local models (Llama, Mistral, etc.) with an agentic interface
- Teams that don't want to commit to a single model vendor

**Not ideal for:**
- Beginners — more configuration required than Claude Code or Codex CLI
- Production workflows that need consistent, well-supported tooling

**How to start:** See [opencode.ai](https://opencode.ai) for installation. Supports Anthropic, OpenAI, and Ollama backends.

---

## Cursor

**What it is:** A fork of VS Code with deep AI integration. Looks and feels like VS Code, but AI is baked into the editing experience.

**Strengths:**
- Familiar VS Code interface — low switching cost if you're already there
- Inline edits: select code, describe the change, apply it
- Chat panel with codebase awareness
- Agent mode for autonomous multi-file changes
- Works with multiple models (Claude, GPT-4o, etc.)

**Best for:**
- Developers who live in VS Code and want AI inside the editor
- Interactive, back-and-forth editing sessions
- When you want to stay in the editor and not switch to a terminal

**Not ideal for:**
- Fully autonomous long-running tasks
- Teams that need fine-grained control over every agent action

---

## Windsurf

**What it is:** An AI-first editor built around an agentic "Cascade" system. Originally from Codeium — check current ownership at [codeium.com/windsurf](https://codeium.com/windsurf) as the company has changed hands.

**Strengths:**
- Cascade agent is designed for multi-step autonomous tasks
- Strong at understanding codebase context automatically
- Integrated chat, edit, and run loop
- Good for greenfield projects or large refactors

**Best for:**
- Developers who want an agentic editor and don't have a strong VS Code attachment
- Longer autonomous workflows within the editor

**Not ideal for:**
- Teams with heavy VS Code extension dependencies (compatibility isn't 100%)

---

## GitHub Copilot

**What it is:** Microsoft/GitHub's AI assistant. Available in VS Code, JetBrains, and other editors.

**Strengths:**
- Extremely low setup friction — available in editors you already use
- Good inline completions as you type
- Copilot Chat for asking questions about code
- Copilot agent mode for autonomous coding tasks in VS Code
- Enterprise-friendly: data stays within GitHub's trust boundary

**Best for:**
- Teams already in the GitHub/Microsoft ecosystem
- Developers who want "AI that doesn't get in the way"
- Enterprise environments with compliance requirements

**Not ideal for:**
- Complex multi-file agentic tasks (Copilot is stronger as an assistant than an autonomous agent)
- When you need full transparency into agent actions
- Open-source projects where you want full control over the model

---

## Claude API / Anthropic SDK

**What it is:** Direct API access to Claude models. You build your own tools, agents, or integrations.

**Strengths:**
- Full control over behavior
- Build custom agents for your specific domain
- Integrate AI into your own products
- Access to tool use, vision, extended thinking

**Best for:**
- Building AI features into your own software
- Custom internal tools
- When off-the-shelf agents don't fit your workflow

**Not ideal for:**
- Quick development tasks (too much setup overhead)
- Non-developers (requires coding)

See [04 — First Agent](../04-first-agent/) for a hands-on example using the SDK.

---

## How to choose

**Starting out?** Pick one tool and go deep before trying others. Recommendation: Claude Code for agentic tasks, Cursor if you want to stay in an editor.

**Already using VS Code?** Cursor is the lowest-friction upgrade. You keep your extensions and muscle memory.

**Need autonomy?** Claude Code handles the most complex multi-step work with the most transparency.

**Building a product?** Claude API.

**Enterprise/compliance first?** GitHub Copilot.

**Want model flexibility or open source?** OpenCode.

**Already in the OpenAI ecosystem?** Codex CLI.

---

## The honest take

These tools are converging. What Cursor does today, Windsurf will do tomorrow, and vice versa. The model matters, but so does the tooling around it. Two tools using the same model can produce very different results depending on how they manage context and structure the agent loop.

What doesn't change: the better you get at directing agents — writing clear goals, managing context, reviewing output — the more value you get from any of these tools.

---

Next: [04 — First Agent](../04-first-agent/) — build something real.
