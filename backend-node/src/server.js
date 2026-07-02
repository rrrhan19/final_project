// 模擬遊戲 microservice：取題 + 批改（非 LLM，DB/字典查表）。
import express from "express";
import cors from "cors";
import { getQuestions, getQuestion, usingDb } from "./db.js";

const app = express();
app.use(cors());
app.use(express.json());

app.get("/health", (_req, res) =>
  res.json({ status: "ok", service: "backend-node", db: usingDb() }),
);

// 取遊戲題目（不含答案）
app.get("/api/games/questions", async (req, res) => {
  const limit = Math.min(Number(req.query.limit) || 5, 20);
  try {
    res.json(await getQuestions(limit));
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// 提交答案 → 批改
app.post("/api/games/answer", async (req, res) => {
  const { question_id, choice_idx } = req.body || {};
  if (question_id == null || choice_idx == null) {
    return res.status(400).json({ error: "question_id 與 choice_idx 為必填" });
  }
  try {
    const q = await getQuestion(question_id);
    if (!q) return res.status(404).json({ error: "找不到題目" });
    res.json({
      correct: Number(choice_idx) === q.correct_idx,
      correct_idx: q.correct_idx,
      explanation: q.explanation,
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`backend-node listening on ${port} (db=${usingDb()})`));
