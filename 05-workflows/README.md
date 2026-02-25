# 05 — Workflows

Patterns that work in practice. Each one is a repeatable approach to a type of problem.

---

## 1. Architecture-first

**The pattern:** Before writing a single line of code, have the agent produce a plan. Review the plan. Then build.

**Why it works:** Agents are fast at generating code and bad at recovering from wrong architectural decisions. Catching a wrong assumption in a plan costs nothing. Catching it after 300 lines of code costs a lot.

**How to do it:**

```
Before writing any code, I want you to read the existing codebase —
start with the README, then /src — and produce a plan for adding
[feature]. The plan should cover:
- What files need to change
- What new files/modules you'll create and why
- What the data flow looks like
- Any tradeoffs in your approach

Don't write code yet. Just the plan.
```

Review the plan. Ask questions. Push back on anything that doesn't look right. Then:

```
The plan looks good. One change: use Redis for the session store
instead of in-memory. Now build it.
```

**When to use it:** Any feature that touches more than 2–3 files. New API endpoints, new modules, refactors.

---

## 2. Context handoff

**The pattern:** When a task is long enough that context degrades, give the agent an explicit summary to start fresh.

**Why it works:** Agents work from what's in their context window. As a conversation gets long, early instructions and decisions get pushed out. A fresh context with a good summary is often more effective than a degraded long one.

**How to do it:**

Midway through a long task, before starting a new session:

```
Before we end this session, write a summary of:
- What we were building and why
- What's been completed
- What's still left to do
- Any decisions we made and why
- The exact next step to take

Write it as if you're briefing yourself for the next session.
```

Save that output. Start a new Claude Code session:

```
Here's the context from our last session: [paste summary]

Continue from where we left off. The next step is [X].
```

**When to use it:** Long refactors, multi-day projects, complex features. Any time you notice the agent losing track of earlier decisions.

---

## 3. Parallel agents (subagents)

**The pattern:** Split a large task into independent subtasks and run agents on each simultaneously.

**Why it works:** Many tasks are parallelizable. Writing tests for module A doesn't depend on writing tests for module B. Analyzing three different files can happen at once. Parallel agents multiply throughput.

**How to do it with Claude Code:**

Claude Code supports subagents natively. In a task prompt:

```
Split this work across parallel subagents:
- Subagent 1: Write unit tests for /src/auth/
- Subagent 2: Write unit tests for /src/payments/
- Subagent 3: Write unit tests for /src/notifications/

Each should follow the test patterns in /src/__tests__/example.test.ts.
Run all tests when done and report results.
```

**How to do it with the API:**

Use Python's `asyncio` or `concurrent.futures` to run multiple agent calls simultaneously, then synthesize their outputs.

```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()

async def analyze_file(filepath):
    response = await client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Read {filepath} and identify any security issues."
        }]
    )
    return filepath, response.content[0].text

async def main():
    files = ["src/auth.py", "src/payments.py", "src/api.py"]
    results = await asyncio.gather(*[analyze_file(f) for f in files])
    for filepath, findings in results:
        print(f"\n{filepath}:\n{findings}")

asyncio.run(main())
```

**When to use it:** Test generation across modules, code review of many files, documentation generation, any task where subtasks are independent.

---

## 4. Review loop

**The pattern:** Agent writes, you review, agent revises. Explicit cycles rather than one-shot generation.

**Why it works:** One-shot prompts rarely produce production-ready output on complex tasks. Building in a review cycle catches issues before they compound.

**How to do it:**

```
Write the implementation for [X]. Don't add tests yet.
```

Review the output. Then:

```
Two issues with this implementation:
1. The error handling in getUserById doesn't cover the case where
   the database is unreachable — it'll throw an unhandled exception
2. The caching logic will cause stale reads if the cache TTL is
   longer than the session TTL

Fix both of those, then add the tests.
```

**The review checklist (quick):**
- Does it match what I actually asked for?
- Does it handle errors properly?
- Does it follow existing patterns in the codebase?
- Is there anything I wouldn't want to ship?

**When to use it:** Anything going to production. Security-sensitive code. Public APIs. Database migrations.

---

## 5. Exploration before change

**The pattern:** Before modifying anything, have the agent map the territory.

**Why it works:** Agents that dive straight into editing often miss how things connect. A read-first phase produces much better edits.

**How to do it:**

```
Don't make any changes yet. First, explore the codebase and tell me:
- Where is the user authentication logic?
- What happens to a user session after login?
- What touches the session object?
- Where are sessions invalidated?
```

Use the map to refine your task before the agent touches a file.

**When to use it:** Unfamiliar codebases, large refactors, bug hunting, anything where you're not sure what connects to what.

---

## 6. Incremental commits

**The pattern:** Commit working code frequently during a long agent session.

**Why it works:** Agent sessions can go sideways. A commit is a checkpoint. If the agent makes a mess of step 4, you can revert to step 3 and try differently — without losing the good work.

**How to do it:**

Give the agent explicit commit instructions:

```
After each major step, commit the working code with a descriptive message.
If tests break, fix them before committing. Don't batch everything into one commit at the end.
```

Or manage it yourself: after each phase of agent work, review and commit before continuing.

**When to use it:** Always on tasks that will touch many files. Essential for anything that takes more than a single short session.

---

## Combining patterns

These aren't mutually exclusive. A typical session on a real feature might look like:

1. **Exploration** → understand the codebase
2. **Architecture-first** → plan before building
3. **Parallel agents** → generate tests and docs simultaneously
4. **Review loop** → iterate on the implementation
5. **Incremental commits** → checkpoint as you go
6. **Context handoff** → pick up cleanly in the next session

You don't apply all of them every time. You reach for the ones that fit the task.

---

Next: [06 — Learning Path](../06-learning-path/) — what to learn next.
