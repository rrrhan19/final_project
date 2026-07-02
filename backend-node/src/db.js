// 資料存取：有 DATABASE_URL 走 PostgreSQL，否則 fallback 用 db/fixtures.json。
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const FIXTURES = join(__dirname, "..", "..", "db", "fixtures.json");

let pool = null;
if (process.env.DATABASE_URL) {
  try {
    const { Pool } = await import("pg");
    pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await pool.query("SELECT 1"); // 連線測試
  } catch (e) {
    console.error("[db] DB unavailable, falling back to fixtures:", e.message);
    pool = null;
  }
}

export const usingDb = () => pool !== null;

const fixtures = () => JSON.parse(readFileSync(FIXTURES, "utf-8"));

// 取題目（不含答案）
export async function getQuestions(limit = 5) {
  if (!pool) {
    const qs = fixtures().qa_questions;
    return shuffle(qs)
      .slice(0, limit)
      .map(({ id, scam_type, difficulty, prompt, options }) => ({
        id,
        scam_type,
        difficulty,
        prompt,
        options,
      }));
  }
  const { rows } = await pool.query(
    "SELECT id, scam_type, difficulty, prompt, options FROM qa_questions ORDER BY random() LIMIT $1",
    [limit],
  );
  return rows;
}

// 取單題完整資料（含答案），用於批改
export async function getQuestion(id) {
  if (!pool) {
    return fixtures().qa_questions.find((q) => q.id === Number(id)) || null;
  }
  const { rows } = await pool.query(
    "SELECT id, correct_idx, explanation FROM qa_questions WHERE id = $1",
    [id],
  );
  return rows[0] || null;
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
