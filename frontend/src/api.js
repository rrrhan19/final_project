// 兩個後端的 fetch 封裝
const API = import.meta.env.VITE_API_URL || "http://localhost:8000"; // FastAPI
const NODE = import.meta.env.VITE_NODE_URL || "http://localhost:3000"; // Express

async function jget(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
}
async function jpost(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
}

export const detect = (text) => jpost(`${API}/api/detect`, { text });
export const checkUrl = (url) => jpost(`${API}/api/url-check`, { url });
export const checkPhone = (phone) => jpost(`${API}/api/phone-check`, { phone });
export const report = (kind, value, note = "") => jpost(`${API}/api/report`, { kind, value, note });
export const chat = (message, history = []) => jpost(`${API}/api/chat`, { message, history });
export const getAlerts = (limit = 10) => jget(`${API}/api/alerts?limit=${limit}`);
export const getStats = (from = 2020, to = 2025) =>
  jget(`${API}/api/stats?from=${from}&to=${to}`);
export const getQuestions = (limit = 5) =>
  jget(`${NODE}/api/games/questions?limit=${limit}`);
export const answer = (question_id, choice_idx) =>
  jpost(`${NODE}/api/games/answer`, { question_id, choice_idx });
