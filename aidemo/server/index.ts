import cors from "cors";
import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = Number(process.env.PORT ?? 3001);

let highScore = 0;

app.use(cors());
app.use(express.json());

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, uptime: process.uptime() });
});

app.get("/api/highscore", (_req, res) => {
  res.json({ highScore });
});

app.post("/api/highscore", (req, res) => {
  const score = Number(req.body?.score);

  if (!Number.isFinite(score) || score < 0) {
    res.status(400).json({ error: "Score must be a non-negative number" });
    return;
  }

  if (score > highScore) {
    highScore = Math.floor(score);
  }

  res.json({ highScore });
});

if (process.env.NODE_ENV === "production") {
  const clientDist = path.resolve(__dirname, "../dist");
  app.use(express.static(clientDist));

  app.get("*", (_req, res) => {
    res.sendFile(path.join(clientDist, "index.html"));
  });
}

app.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}`);
});
