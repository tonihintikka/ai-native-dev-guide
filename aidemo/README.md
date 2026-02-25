# Flappy Bird Demo (TypeScript + Node + React)

A small Flappy Bird clone using:
- React + TypeScript + Vite for the frontend
- Node.js + Express + TypeScript for backend API

The backend exposes `/api/highscore`, and the frontend submits your score after each run.

## Run locally

1. Install dependencies:

```bash
npm install
```

2. Start both frontend and backend:

```bash
npm run dev
```

3. Open:

- `http://localhost:5173` for the game UI
- `http://localhost:3001/api/health` for server health

## Controls

- `Space` or tap/click canvas to flap
- `Space` after game over to restart
- `Enter` or `R` to reset after game over
