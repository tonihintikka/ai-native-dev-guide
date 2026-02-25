# 02 — Core Concepts

Five concepts. Everything else builds on these.

---

## 1. Agents

An agent is an AI model that doesn't just respond — it takes actions in a loop.

The basic loop:
1. Receive a goal
2. Decide what to do next
3. Use a tool (read a file, run a command, call an API)
4. See the result
5. Decide what to do next
6. Repeat until done

The key difference from a chatbot: an agent keeps going autonomously. You give it a task, not a prompt. It works until it finishes or gets stuck.

**What makes a good agent?**
- A clear, specific goal
- Access to the right tools
- Enough context to understand the environment it's working in

---

## 2. Tools

Tools are what give agents the ability to act, not just respond.

Common tools in software development agents:

| Tool | What it does |
|---|---|
| `read_file` | Read a file from the filesystem |
| `write_file` | Create or modify a file |
| `bash` / `execute_command` | Run shell commands |
| `web_search` | Look something up |
| `web_fetch` | Read a specific URL |
| `list_files` / `glob` | Explore directory structure |
| `grep` / `search` | Find patterns in code |

An agent without tools is just a chatbot. Tools are what make agents useful in a real dev environment.

When you're evaluating an agentic tool, the first question is: what tools does it have access to? That determines what it can actually do.

---

## 3. Context

Context is everything the agent can see when it's making a decision.

This includes:
- Your instructions
- The conversation so far
- File contents it has read
- Tool results it has received
- Any documents or context you've explicitly provided

**Context windows** are finite. Today's models handle anywhere from 200k to 1M+ tokens depending on the model, which is large but not unlimited. A token is roughly ¾ of a word in English — less for other languages.

What this means in practice:
- Long conversations eventually push early context out
- Large codebases need to be navigated selectively, not loaded wholesale
- Good context management is a skill — knowing what to include and what to leave out

**CLAUDE.md** (specific to Claude Code) is a file you put in your project root. The agent reads it at the start of every session. Use it to give standing instructions: code style, project structure, what not to touch, how to run tests. This is one of the highest-leverage things you can do.

---

## 4. MCP (Model Context Protocol)

MCP is an open protocol that lets agents connect to external tools and data sources in a standardized way.

Think of it like a plugin system for agents. Instead of each AI tool building its own integrations, MCP lets you connect any agent to any tool that has an MCP server.

Examples of what MCP enables:
- Give your agent access to your GitHub repo
- Connect to a database and let the agent query it
- Integrate with Slack, Notion, Linear, or any other tool
- Build your own MCP server to expose internal systems

**Why it matters:** MCP is becoming the standard. If you're evaluating agents or building with the Claude API, understanding MCP means you can extend what agents can do rather than being limited to what the tool ships with.

You don't need to build MCP servers to use this guide. But knowing the concept explains why some agents are dramatically more capable than others.

---

## 5. Prompting (for agents)

Prompting an agent is different from prompting a chatbot.

Chatbot prompting: "Explain this code to me."

Agent prompting: "Read the files in `/src/auth/`, find the session handling logic, and refactor it to use the new token format defined in `/docs/auth-spec.md`. Run the tests when you're done and fix any failures."

The difference:
- **Specific goal** — not a question, a task
- **Grounded in actual files** — not abstract, concrete locations
- **Defines done** — the agent knows when to stop
- **Handles failure** — tells the agent what to do if things break

**Principles for agent prompting:**

1. **Be specific about what you want, flexible about how.** Don't micromanage the approach, but be clear about the outcome.

2. **Reference real things.** File paths, function names, error messages. The more grounded your prompt, the better.

3. **Define the scope.** "Refactor the auth module" is too vague. "Refactor `/src/auth/session.ts` to use the new `TokenManager` class" is actionable.

4. **Say what done looks like.** "Tests pass" or "the API returns 200 on this endpoint" gives the agent a target to hit.

5. **Iterate.** Your first prompt won't be perfect. Review the agent's work, correct course, continue.

---

## How these fit together

```
You give the agent a goal (prompting)
    ↓
Agent uses tools to take actions
    ↓
Tools return results that become context
    ↓
Agent reasons over context and takes next action
    ↓
MCP lets agents access tools beyond what's built in
    ↓
Repeat until done
```

That's the whole loop. Everything else is variations on this pattern.

---

Next: [03 — Your Toolbox](../03-your-toolbox/) — which tools to use and when.
