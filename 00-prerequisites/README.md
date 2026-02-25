# 00 - Prerequisites

Before you build anything with AI agents, you need a working foundation. This section gets you there.

---

## Pick your OS path first

Everything in this section works on:

- macOS
- Windows
- Linux

Use the instructions for your operating system in each section.

---

## What you need before you start

- A terminal (command-line interface)
- Git and a GitHub account
- Node.js and npm
- Python 3.12+ (recommended)
- VS Code (or another code editor)
- Access to at least one AI assistant (Claude, Gemini, ChatGPT, Copilot, or similar)
- Optional: an API key (only needed when you call model APIs from code)

The rest of this section installs each one and shows you how to verify it works.

---

## Use AI as your setup copilot

Do not set up your environment alone. Use AI while you install each tool.

Example prompt you can paste into any assistant:

```text
I am setting up a dev environment on <macOS/Windows/Linux>.
Help me install <tool> step by step.
After each step, ask me for the command output before we continue.
If there is an error, explain the fix in plain language.
```

Use this pattern for terminal setup, Git, Node.js, Python, and editor setup. It saves time and helps you troubleshoot quickly.

---

## The terminal

The terminal is a text interface for your computer. Instead of clicking icons, you type commands. Most developer tools are designed to be run from the terminal.

**macOS:** Open the built-in Terminal app. Press `Cmd + Space`, type "Terminal", press Enter.

**Windows:** Use PowerShell or Windows Terminal. Press `Win + X` and choose PowerShell, or install [Windows Terminal](https://aka.ms/terminal).

**Linux:** Open your distro terminal app (for example, GNOME Terminal, Konsole, or Alacritty).

### Basic commands

| Command | What it does |
|---|---|
| `pwd` | Print working directory - shows where you are |
| `ls` | List files in current folder (macOS, Linux, PowerShell) |
| `dir` | List files in current folder (Windows cmd, PowerShell) |
| `cd folder-name` | Move into a folder |
| `cd ..` | Go up one level |

Try them. Open your terminal and run `pwd`. You should see a path like `/Users/yourname`, `/home/yourname`, or `C:\Users\yourname`.

---

## Git

Git is version control. It tracks changes to your code over time.

GitHub is where your Git repositories live in the cloud.

You need both.

### Install Git

**macOS**

```bash
xcode-select --install
```

Or install from [https://git-scm.com/downloads](https://git-scm.com/downloads).

**Windows**

Install Git for Windows from [https://git-scm.com/downloads](https://git-scm.com/downloads).

**Linux**

Install with your package manager:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y git

# Fedora
sudo dnf install -y git
```

Verify:

```bash
git --version
```

You should see something like `git version 2.43.0`.

### Set your identity

Git needs to know who you are before your first commit:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Core commands

| Command | What it does |
|---|---|
| `git init` | Start tracking a folder with Git |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save a snapshot with a description |
| `git push` | Upload commits to GitHub |

### Create a GitHub account

Go to [https://github.com](https://github.com) and sign up. It is free.

Full getting-started guide: [https://docs.github.com/en/get-started](https://docs.github.com/en/get-started)

---

## Node.js and npm

Node.js lets you run JavaScript in the terminal. npm installs JavaScript libraries and tools.

### Install Node.js (LTS)

**macOS / Windows**

Download and install the LTS version from [https://nodejs.org](https://nodejs.org).

**Linux**

Install from your distro repositories or NodeSource (LTS). Example:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y nodejs npm

# Fedora
sudo dnf install -y nodejs npm
```

Verify:

```bash
node --version
npm --version
```

If both print versions, Node.js and npm are ready.

---

## Python

Python is widely used for scripting and AI tooling. You will use it in later sections.

### Install Python 3.12+

**macOS**

Download from [https://python.org](https://python.org). Do not rely on the system Python.

**Windows**

Download from [https://python.org](https://python.org) and check "Add Python to PATH" during installation.

**Linux**

Install with your package manager:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y python3 python3-venv python3-pip

# Fedora
sudo dnf install -y python3 python3-pip
```

Verify:

```bash
python3 --version
```

If `python3` is not available on Windows, try:

```bash
python --version
```

You should see `Python 3.12.x` or newer.

### Virtual environments

A virtual environment isolates project dependencies so packages from different projects do not conflict.

Create:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

When active, your prompt usually shows `(venv)`.

---

## AI tools and optional API keys

You do **not** need an Anthropic API key to start learning.

You can begin with free tiers and browser tools, for example:

- Claude (web chat)
- Gemini (web chat)
- ChatGPT (web chat)

Use whichever you prefer while setting up your environment.

### API key vs subscription (February 2026 snapshot)

You usually have two ways to access AI coding tools:

- API key (pay per use)
- Subscription (fixed monthly plan)

For many beginners, a subscription is the simpler place to start, and often competitive in price for daily use.

Examples:

- OpenAI ChatGPT subscription plans can include Codex-style coding workflows.
- Anthropic has multiple plan tiers that can include Claude Code usage.
- Google has Gemini plans for interactive use.
- Cursor has license tiers with different agent usage limits.

For many people, around a 20 EUR/month tier is enough to get moving. Pick based on your usage pattern and compare current limits before committing.

### When do you need an API key?

Only when you run code that calls a model provider API directly.

This guide includes Claude-specific sections later. For those sections, use an Anthropic account/API key. For setup and early learning, any assistant is fine.

### Environment variable examples (only if needed)

Never hardcode API keys in code and never commit them to GitHub.

**macOS/Linux**

```bash
export ANTHROPIC_API_KEY=...
export GEMINI_API_KEY=...
export OPENAI_API_KEY=...
```

**Windows**

```bash
setx ANTHROPIC_API_KEY "..."
setx GEMINI_API_KEY "..."
setx OPENAI_API_KEY "..."
```

Restart terminal after `setx`.

---

## A code editor

Use any editor you like. Recommended: **VS Code**.

Download: [https://code.visualstudio.com](https://code.visualstudio.com)

Install it and open a folder. That is enough for now.

---

## Signs you are ready

Work through this checklist before moving on:

- [ ] Terminal opens and `pwd` works
- [ ] `git --version` prints a version
- [ ] `node --version` and `npm --version` print versions
- [ ] `python3 --version` (or `python --version` on Windows) prints 3.12+
- [ ] VS Code is installed and can open a folder
- [ ] You can use at least one AI assistant (Claude, Gemini, ChatGPT, or similar)
- [ ] Optional: you added an API key environment variable for the provider you plan to use in code

If something fails, fix it now. Setup errors get more expensive later.

---

Next: [01 - What Changed](../01-what-changed/)
