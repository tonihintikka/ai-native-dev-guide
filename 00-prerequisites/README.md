# 00 — Prerequisites

Before you build anything with AI agents, you need a working foundation. This section gets you there.

---

## What you need before you start

- A terminal (command-line interface)
- Git and a GitHub account
- Node.js and npm
- Python 3.12+
- An Anthropic account and API key
- VS Code (code editor)

The rest of this section installs each one and shows you how to verify it works.

---

## The terminal

The terminal is a text interface for your computer. Instead of clicking icons, you type commands. Most developer tools are designed to be run from the terminal.

**Mac:** Open the built-in Terminal app. Press `Cmd + Space`, type "Terminal", hit Enter.

**Windows:** Use PowerShell or Windows Terminal. Press `Win + X` and choose "Windows PowerShell", or install [Windows Terminal](https://aka.ms/terminal) from the Microsoft Store.

### Basic commands

| Command | What it does |
|---|---|
| `pwd` | Print working directory — shows where you are |
| `ls` (Mac) / `dir` (Windows) | List files in the current folder |
| `cd folder-name` | Change directory — move into a folder |
| `cd ..` | Go up one level |

Try them. Open your terminal and run `pwd`. You should see a file path like `/Users/yourname` or `C:\Users\yourname`. That's your home directory.

---

## Git

Git is a version control tool. It tracks changes to your code over time. If you break something, you can go back. If you want to collaborate, everyone works from the same history.

GitHub is a website where your Git repositories (projects) live in the cloud. It's where you store your work, share it, and deploy from.

You need both.

### Install Git

Download from [https://git-scm.com/downloads](https://git-scm.com/downloads) and follow the installer for your OS.

Verify it works:

```
git --version
```

You should see something like `git version 2.43.0`.

### Set your identity

Git needs to know who you are before you make your first commit (a saved snapshot of changes):

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Core commands

| Command | What it does |
|---|---|
| `git init` | Start tracking a folder with Git |
| `git add .` | Stage all changes (mark them for saving) |
| `git commit -m "message"` | Save a snapshot with a description |
| `git push` | Upload your commits to GitHub |

### Create a GitHub account

Go to [https://github.com](https://github.com) and sign up. It's free.

Full getting started guide: [https://docs.github.com/en/get-started](https://docs.github.com/en/get-started)

---

## Node.js and npm

Node.js is a JavaScript runtime — it lets you run JavaScript outside of a browser, directly in the terminal. Most web development tools are built on it.

npm (Node Package Manager) comes bundled with Node.js. It installs JavaScript libraries and tools with a single command.

### Install Node.js

Go to [https://nodejs.org](https://nodejs.org) and download the **LTS** version. LTS stands for Long Term Support — it's the stable version recommended for most users.

Run the installer, then verify:

```
node --version
npm --version
```

You should see version numbers for both. If you do, Node.js and npm are ready.

---

## Python

Python is a programming language used widely for scripting, data work, and AI tooling. Many agent frameworks — including the Anthropic SDK — have Python support. You will need it.

### Install Python

Go to [https://python.org](https://python.org) and download version **3.12 or newer**.

**Mac:** The system Python is outdated. Always install from python.org.

**Windows:** During installation, check the box that says "Add Python to PATH." This lets you run Python from any terminal window.

Verify:

```
python --version
```

You should see `Python 3.12.x` or newer.

### Virtual environments

A virtual environment (venv) is an isolated folder where a project's Python packages are installed. Without it, packages from different projects can conflict. With it, each project manages its own dependencies cleanly.

Create a virtual environment in a project folder:

```
python -m venv venv
```

Activate it:

```
source venv/bin/activate      # Mac
venv\Scripts\activate         # Windows
```

When active, your terminal prompt shows `(venv)`. Any packages you install with `pip install` go into that environment only.

You will use this every time you work on a Python-based agent project.

---

## An Anthropic account and API key

To use Claude — Anthropic's AI model — you need an account and an API key.

### Create an account

Go to [https://console.anthropic.com](https://console.anthropic.com) and sign up.

### Get an API key

Inside the console, navigate to **API Keys** and create a new key. It will look like a long string starting with `sk-ant-...`. Copy it somewhere safe. You will only see it once.

An API key proves to Anthropic's servers that the requests come from you. It is tied to your account and your billing.

### Costs

**Claude Code** (the AI coding agent covered in this guide) requires either a [claude.ai Pro](https://claude.ai) subscription ($20/month) or Anthropic API credits.

If you are just getting started, API credits are the cheaper path. A $5–10 credit top-up is enough to experiment. You can add credits in the console under **Billing**.

### Set the key as an environment variable

Never put your API key directly in your code. Never commit it to GitHub. If it ends up in a public repository, anyone can use it at your expense.

The right way is to store it as an environment variable — a value your operating system holds in memory that programs can read.

**Mac (temporary — current session only):**

```
export ANTHROPIC_API_KEY=sk-ant-...
```

**Mac (permanent — add to your shell config):**

```
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc
source ~/.zshrc
```

**Windows (permanent):**

```
setx ANTHROPIC_API_KEY "sk-ant-..."
```

Restart your terminal after running `setx` on Windows.

To verify the variable is set on Mac:

```
echo $ANTHROPIC_API_KEY
```

It should print your key.

---

## A code editor

You need a code editor — software built specifically for writing and reading code.

The recommended choice is **VS Code** (Visual Studio Code). It is free, runs on Mac and Windows, and has strong support for every language in this guide.

Download: [https://code.visualstudio.com](https://code.visualstudio.com)

Install it and open a folder. That's all you need for now.

Later sections cover AI-assisted editors like Cursor and Windsurf. Those are built on top of VS Code. You should be comfortable with a plain editor before adding AI features on top of it.

---

## Signs you're ready

Work through this checklist before moving on. Each item should pass without errors.

- [ ] Terminal opens and you can run `pwd`
- [ ] `git --version` prints a version number
- [ ] `node --version` prints a version number
- [ ] `npm --version` prints a version number
- [ ] `python --version` prints 3.12 or newer
- [ ] VS Code is installed and opens a folder
- [ ] Anthropic account created at console.anthropic.com
- [ ] API key generated and stored as an environment variable

If something fails, go back to that section and follow the install steps again. Don't skip errors — they will surface later at a worse time.

---

Next: [01 — What Changed](../01-what-changed/)
