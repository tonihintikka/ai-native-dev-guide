# 04 — First Agent

Two paths. Pick the one that matches where you are.

- **Path A** — Use Claude Code to build something with an agent (no coding required beyond normal dev work)
- **Path B** — Call the Claude API directly to build a minimal agent from scratch (requires Python or TypeScript)

Both are valuable. Path A teaches you to direct agents. Path B teaches you how agents work under the hood.

---

## Path A: Use Claude Code on a real project

### Prerequisites
- Node.js installed
- An Anthropic account (claude.ai)
- A project directory with some code in it (or start fresh)

### Step 1: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 2: Set up your project context

Create a `CLAUDE.md` file in your project root. This is your standing brief to the agent — it reads this every session.

Example `CLAUDE.md`:

```markdown
# Project context

This is a Node.js + TypeScript REST API for [describe what it does].

## Stack
- Runtime: Node.js 20
- Language: TypeScript
- Framework: Express
- Database: PostgreSQL via Prisma

## Key conventions
- All new endpoints go in `/src/routes/`
- Business logic lives in `/src/services/`
- Run tests with: `npm test`
- Lint with: `npm run lint`

## What not to touch
- `/src/legacy/` — do not modify, it will be replaced
```

Adapt this to your actual project. The more specific, the better.

### Step 3: Start Claude Code

```bash
cd your-project
claude
```

### Step 4: Give it a real task

Don't start with "hello world." Give it something genuine.

Examples of good first tasks:

```
Add input validation to the POST /users endpoint.
The request body should require email (valid format) and name (non-empty string).
Return 400 with a clear error message if validation fails.
Add a test for the happy path and both failure cases.
```

```
Read the README and the /src directory, then find all the places
where we're using console.log for debugging. Replace them with
the logger utility in /src/utils/logger.ts. Run the tests when done.
```

```
Look at the database schema in /prisma/schema.prisma and the existing
routes in /src/routes/. We need a new endpoint: GET /users/:id/posts
that returns all posts for a user. Follow the same patterns you see
in the existing routes.
```

### Step 5: Watch, review, correct

Claude Code shows you every action before taking it. Watch what it does:

- Does it read the right files first?
- Does its plan make sense?
- When it writes code, does the output match what you intended?

This review step is the job now. Not writing the code — reading the agent's work and catching what needs adjusting.

If it goes wrong, say so directly:

```
That's not quite right. The validation should happen in middleware,
not inside the route handler. Undo those changes and try again
using the existing auth middleware in /src/middleware/auth.ts as a pattern.
```

### What you'll learn

By the end of a real session:
- How to write task-oriented prompts instead of question prompts
- How to give the agent enough context to work independently
- How to review agent output critically
- How `CLAUDE.md` changes the quality of agent work

---

## Path B: Build a minimal agent with the Claude API

This is a simple Python agent that reads a file, analyzes it, and reports findings. Under 50 lines. It shows the core agentic loop clearly.

### Prerequisites

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
```

### The code

Create `agent.py`:

```python
import anthropic
import subprocess

client = anthropic.Anthropic()

tools = [
    {
        "name": "read_file",
        "description": "Read the contents of a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "run_command",
        "description": "Run a shell command and return output",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to run"}
            },
            "required": ["command"]
        }
    }
]

def handle_tool(name, inputs):
    if name == "read_file":
        try:
            with open(inputs["path"]) as f:
                return f.read()
        except FileNotFoundError:
            return f"File not found: {inputs['path']}"
    elif name == "run_command":
        # WARNING: shell=True is a security risk in production — never use this pattern
        # with untrusted input. For learning purposes only.
        result = subprocess.run(inputs["command"], shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr

def run_agent(task):
    messages = [{"role": "user", "content": task}]
    print(f"Task: {task}\n")

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Add assistant response to message history
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Extract final text response
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"Result: {block.text}")
            break

        # Handle tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  -> {block.name}({block.input})")
                result = handle_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

# Run it
run_agent("Read the file README.md and summarize what this project does in one sentence.")
```

### Run it

```bash
python agent.py
```

You'll see the agent:
1. Decide to call `read_file`
2. Receive the file contents
3. Reason over them
4. Return a summary

### Extend it

Now give it a harder task:

```python
run_agent(
    "Look at the files in the current directory. "
    "Find any Python files and count how many functions each one defines. "
    "Report the results."
)
```

This forces the agent to chain multiple tool calls: list files, read each one, count functions, synthesize results.

### What you're seeing

The `while True` loop is the agent loop. Each iteration:
- Model responds with either a final answer or tool calls
- You execute the tool calls
- Results go back into the conversation
- Model decides what to do next

This is the pattern every agentic framework (LangChain, LlamaIndex, Claude Code itself) is built on. Now you've seen it raw.

---

## Real examples: one prompt, real projects

Both demo projects in this repo were built in a single agent session. Neither is polished. Both are instructive.

---

### Example 1: Finnish city population analytics

**The prompt (verbatim):**

> I am planning to do python analytics script about finnish city inhabitants. Could you please check where you can get this information with. And please gather that one to SQLite database such way that you can make very nice looking graphics about data to generated HTML report. Use VENV for python libraries.

**What the agent did — without being asked:**

1. Found the official data source (Statistics Finland PXWeb API)
2. Drilled into the exact table and its dimensions
3. Validated the API query shape before writing any fetch code
4. Scaffolded the full project: `scripts/`, `data/`, `output/`, `requirements.txt`, `.gitignore`, `README.md`
5. Wrote a Python ETL pipeline pulling all 308 Finnish municipalities, 1990–2024
6. Normalized data into three SQLite tables
7. Built an interactive Plotly HTML report with multiple chart types
8. Ran it end-to-end and validated the output

**The result:**

- 308 municipalities loaded
- 10,780 rows in `population_metrics`
- Full project, runnable locally, in one session

No schema decisions from the user. No API docs handed over. No library choices specified. The prompt described an outcome — the agent resolved every implementation detail.

Code: [`pythonaidemo/`](../pythonaidemo/)

---

### Example 2: React expense tracker with auth and persistence

**The prompt:**

> Build a React + TypeScript expense tracker app. Users should be able to log in (use simple JWT auth), add expenses with a category and amount, see a monthly summary chart, and export to CSV. Backend in Node/Express, data in SQLite. Use Vite for the frontend. Wire it up so npm run dev starts both.

**Why this is a good agent prompt:**

It specifies the stack (not left to the agent), names the features concretely (JWT auth, category + amount, monthly chart, CSV export), and defines the dev workflow expectation (`npm run dev`). The agent has no ambiguity about what done looks like.

**What the agent has to figure out independently:**

- JWT token structure and where to store it (httpOnly cookie vs localStorage — a real decision with security implications)
- SQLite schema: users, expenses, sessions
- How to structure a monorepo with separate `client/` and `server/` packages under one `package.json` dev script
- Which charting library to use and how to wire it to the expense data
- CSV export: server-side endpoint or client-side generation

**What to watch during the session:**

- Does it handle JWT expiry and refresh, or just issue tokens with no rotation?
- Does it sanitize inputs before writing to SQLite?
- Does the chart re-render when you add a new expense, or only on page load?

These are the review questions. The agent writes the code. You verify the decisions.

---

### Example 3: Python data pipeline with scheduling and alerting

**The prompt:**

> I want a Python script that pulls our website's daily visitor data from the Plausible Analytics API, stores it in SQLite, and emails me a weekly summary report every Monday morning. The report should include a chart of the last 4 weeks and flag any week where traffic dropped more than 20% from the previous week. Use a venv. Schedule it with cron or APScheduler — whichever is cleaner.

**Why this is a good agent prompt:**

It names the external API (Plausible), specifies the storage (SQLite), defines the output format (email with chart), gives a concrete business rule (20% drop threshold), and even asks the agent to make a judgment call on scheduling — but bounds that decision ("cron or APScheduler, whichever is cleaner").

**What the agent has to figure out independently:**

- Plausible API authentication and which endpoints return daily aggregate data
- SQLite schema for storing timeseries visitor data idempotently (re-runs shouldn't duplicate rows)
- How to generate a chart in a format that embeds cleanly in an HTML email
- Email sending via SMTP (with credentials handled via env vars, not hardcoded)
- Whether cron + a standalone script or APScheduler in a long-running process is the better fit

**What to watch during the session:**

- Does it store API credentials safely (env vars, not in the script)?
- Is the 20% drop comparison week-over-week or against a rolling average?
- Does it handle missing data days gracefully (API downtime, etc.)?
- Will the email render correctly in Gmail or does the chart break?

**The pattern this illustrates:**

External API + storage + scheduled execution + notification is one of the most common real-world automation shapes. The agent handles the integration details — API structure, chart generation, email formatting — while you define the business logic and review the output.

---

### What makes a prompt work at this level

Looking across the Finnish analytics example and these two:

| What good prompts include | Why it matters |
|---|---|
| Named tech stack | Agent doesn't waste time on choices you've already made |
| Concrete features, not vibes | "Monthly summary chart" > "nice dashboard" |
| A definition of done | "npm run dev starts both" is testable |
| One or two judgment calls left open | Gives the agent room to apply real expertise |
| No micromanagement of implementation | Let it decide how to structure the SQLite schema |

The worst prompts are either too vague ("build me an expense tracker") or too prescriptive ("create a file called `db.js` with a function called `initDatabase` that..."). Too vague, and the agent makes assumptions you'll disagree with. Too prescriptive, and you're writing the code in English.

The sweet spot: clear outcome, named constraints, room to execute.

---

## What to do next

You've built or used your first agent. The natural next questions:

- How do I handle longer tasks that need more context?
- How do I use multiple agents together?
- What are the workflows that actually work in production?

That's [05 — Workflows](../05-workflows/).
