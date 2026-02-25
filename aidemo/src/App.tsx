import { useCallback, useEffect, useRef, useState } from "react";

type GamePhase = "ready" | "running" | "gameover";

type Pipe = {
  x: number;
  gapY: number;
  scored: boolean;
};

const WORLD = {
  width: 420,
  height: 640,
  groundHeight: 96,
  birdX: 100,
  birdRadius: 16,
  gravity: 1450,
  flapVelocity: -420,
  pipeWidth: 72,
  pipeGap: 180,
  pipeSpeed: 185,
  pipeSpawnSeconds: 1.35,
  minGapCenter: 140,
  maxGapCenter: 390
};

const createPipe = (): Pipe => ({
  x: WORLD.width + 48,
  gapY:
    WORLD.minGapCenter + Math.random() * (WORLD.maxGapCenter - WORLD.minGapCenter),
  scored: false
});

function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const phaseRef = useRef<GamePhase>("ready");
  const birdYRef = useRef(WORLD.height * 0.45);
  const birdVelocityRef = useRef(0);
  const pipesRef = useRef<Pipe[]>([createPipe()]);
  const spawnTimerRef = useRef(0);
  const scoreRef = useRef(0);
  const rafRef = useRef<number>();
  const lastTimeRef = useRef<number>();

  const [phase, setPhase] = useState<GamePhase>("ready");
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);
  const [serverStatus, setServerStatus] = useState("Connecting...");

  const resetGame = useCallback(() => {
    phaseRef.current = "ready";
    birdYRef.current = WORLD.height * 0.45;
    birdVelocityRef.current = 0;
    pipesRef.current = [createPipe()];
    spawnTimerRef.current = 0;
    scoreRef.current = 0;

    setPhase("ready");
    setScore(0);
  }, []);

  const submitScore = useCallback(async (finalScore: number) => {
    try {
      const response = await fetch("/api/highscore", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ score: finalScore })
      });

      if (!response.ok) {
        throw new Error("Failed to submit score");
      }

      const data = (await response.json()) as { highScore: number };
      setHighScore(data.highScore);
      setServerStatus("Server online");
    } catch {
      setServerStatus("Server offline (local play still works)");
    }
  }, []);

  const endRun = useCallback(() => {
    if (phaseRef.current !== "running") {
      return;
    }

    phaseRef.current = "gameover";
    setPhase("gameover");
    void submitScore(scoreRef.current);
  }, [submitScore]);

  const flap = useCallback(() => {
    if (phaseRef.current === "gameover") {
      resetGame();
      phaseRef.current = "running";
      setPhase("running");
      birdVelocityRef.current = WORLD.flapVelocity;
      return;
    }

    if (phaseRef.current === "ready") {
      phaseRef.current = "running";
      setPhase("running");
    }

    birdVelocityRef.current = WORLD.flapVelocity;
  }, [resetGame]);

  const loadHighScore = useCallback(async () => {
    try {
      const response = await fetch("/api/highscore");
      if (!response.ok) {
        throw new Error("Failed to load high score");
      }

      const data = (await response.json()) as { highScore: number };
      setHighScore(data.highScore);
      setServerStatus("Server online");
    } catch {
      setServerStatus("Server offline (local play still works)");
    }
  }, []);

  const updateGame = useCallback(
    (deltaTime: number) => {
      birdVelocityRef.current += WORLD.gravity * deltaTime;
      birdYRef.current += birdVelocityRef.current * deltaTime;

      spawnTimerRef.current += deltaTime;
      if (spawnTimerRef.current >= WORLD.pipeSpawnSeconds) {
        spawnTimerRef.current = 0;
        pipesRef.current.push(createPipe());
      }

      pipesRef.current = pipesRef.current
        .map((pipe) => ({
          ...pipe,
          x: pipe.x - WORLD.pipeSpeed * deltaTime
        }))
        .filter((pipe) => pipe.x + WORLD.pipeWidth > -16);

      const birdTop = birdYRef.current - WORLD.birdRadius;
      const birdBottom = birdYRef.current + WORLD.birdRadius;
      const birdLeft = WORLD.birdX - WORLD.birdRadius;
      const birdRight = WORLD.birdX + WORLD.birdRadius;

      if (birdTop < 0 || birdBottom > WORLD.height - WORLD.groundHeight) {
        endRun();
        return;
      }

      for (const pipe of pipesRef.current) {
        const pipeLeft = pipe.x;
        const pipeRight = pipe.x + WORLD.pipeWidth;

        if (birdRight > pipeLeft && birdLeft < pipeRight) {
          const gapTop = pipe.gapY - WORLD.pipeGap / 2;
          const gapBottom = pipe.gapY + WORLD.pipeGap / 2;

          if (birdTop < gapTop || birdBottom > gapBottom) {
            endRun();
            return;
          }
        }

        if (!pipe.scored && pipeRight < WORLD.birdX) {
          pipe.scored = true;
          scoreRef.current += 1;
          setScore(scoreRef.current);
        }
      }
    },
    [endRun]
  );

  const draw = useCallback(
    (ctx: CanvasRenderingContext2D) => {
      ctx.clearRect(0, 0, WORLD.width, WORLD.height);

      const sky = ctx.createLinearGradient(0, 0, 0, WORLD.height);
      sky.addColorStop(0, "#9ad9ff");
      sky.addColorStop(1, "#d8f5ff");
      ctx.fillStyle = sky;
      ctx.fillRect(0, 0, WORLD.width, WORLD.height);

      ctx.fillStyle = "#f7f3b8";
      ctx.beginPath();
      ctx.arc(360, 92, 38, 0, Math.PI * 2);
      ctx.fill();

      for (const pipe of pipesRef.current) {
        const gapTop = pipe.gapY - WORLD.pipeGap / 2;
        const gapBottom = pipe.gapY + WORLD.pipeGap / 2;

        ctx.fillStyle = "#3aa45a";
        ctx.fillRect(pipe.x, 0, WORLD.pipeWidth, gapTop);
        ctx.fillRect(
          pipe.x,
          gapBottom,
          WORLD.pipeWidth,
          WORLD.height - WORLD.groundHeight - gapBottom
        );

        ctx.fillStyle = "#2a8144";
        ctx.fillRect(pipe.x - 6, gapTop - 16, WORLD.pipeWidth + 12, 16);
        ctx.fillRect(pipe.x - 6, gapBottom, WORLD.pipeWidth + 12, 16);
      }

      ctx.fillStyle = "#dfc06f";
      ctx.fillRect(0, WORLD.height - WORLD.groundHeight, WORLD.width, WORLD.groundHeight);

      ctx.fillStyle = "#f7c529";
      ctx.beginPath();
      ctx.arc(WORLD.birdX, birdYRef.current, WORLD.birdRadius, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(WORLD.birdX + 5, birdYRef.current - 4, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#1f1f1f";
      ctx.beginPath();
      ctx.arc(WORLD.birdX + 6, birdYRef.current - 4, 2.3, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#202e45";
      ctx.font = "700 42px 'Trebuchet MS', sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(String(scoreRef.current), WORLD.width / 2, 64);

      if (phaseRef.current === "ready") {
        ctx.fillStyle = "rgba(10, 20, 40, 0.7)";
        ctx.fillRect(40, 238, WORLD.width - 80, 118);

        ctx.fillStyle = "#ffffff";
        ctx.font = "700 30px 'Trebuchet MS', sans-serif";
        ctx.fillText("Flappy Bird", WORLD.width / 2, 282);
        ctx.font = "500 18px 'Trebuchet MS', sans-serif";
        ctx.fillText("Press Space / Tap to fly", WORLD.width / 2, 315);
      }

      if (phaseRef.current === "gameover") {
        ctx.fillStyle = "rgba(10, 20, 40, 0.78)";
        ctx.fillRect(48, 210, WORLD.width - 96, 186);

        ctx.fillStyle = "#ffffff";
        ctx.font = "700 34px 'Trebuchet MS', sans-serif";
        ctx.fillText("Game Over", WORLD.width / 2, 258);

        ctx.font = "500 20px 'Trebuchet MS', sans-serif";
        ctx.fillText(`Score: ${scoreRef.current}`, WORLD.width / 2, 296);
        ctx.fillText(`High Score: ${highScore}`, WORLD.width / 2, 326);
        ctx.fillText("Space / Tap to restart", WORLD.width / 2, 362);
      }
    },
    [highScore]
  );

  useEffect(() => {
    void loadHighScore();
  }, [loadHighScore]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.code === "Space") {
        event.preventDefault();
        flap();
        return;
      }

      if ((event.code === "Enter" || event.code === "KeyR") && phaseRef.current === "gameover") {
        resetGame();
      }
    };

    window.addEventListener("keydown", onKeyDown, { passive: false });

    return () => {
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [flap, resetGame]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }

    const tick = (timestamp: number) => {
      if (lastTimeRef.current === undefined) {
        lastTimeRef.current = timestamp;
      }

      const deltaTime = Math.min((timestamp - lastTimeRef.current) / 1000, 0.045);
      lastTimeRef.current = timestamp;

      if (phaseRef.current === "running") {
        updateGame(deltaTime);
      }

      draw(ctx);
      rafRef.current = window.requestAnimationFrame(tick);
    };

    rafRef.current = window.requestAnimationFrame(tick);

    return () => {
      if (rafRef.current) {
        window.cancelAnimationFrame(rafRef.current);
      }
      lastTimeRef.current = undefined;
    };
  }, [draw, updateGame]);

  return (
    <main className="page">
      <section className="panel">
        <h1>Flappy Bird Demo</h1>
        <p className="subtitle">TypeScript + React + Node</p>

        <canvas
          ref={canvasRef}
          width={WORLD.width}
          height={WORLD.height}
          onPointerDown={flap}
          className="game-canvas"
        />

        <div className="meta-row">
          <span>State: {phase}</span>
          <span>Score: {score}</span>
          <span>High Score: {highScore}</span>
        </div>

        <p className="server-status">{serverStatus}</p>
      </section>
    </main>
  );
}

export default App;
