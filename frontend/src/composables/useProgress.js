// 跨遊戲進度/成就（localStorage 持久化）
const KEY = "scamguard_progress_v1";

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || { best: {}, played: {}, badges: [] }; }
  catch { return { best: {}, played: {}, badges: [] }; }
}
function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch {} }

export function recordGame(key, score, total) {
  const p = load();
  p.played[key] = (p.played[key] || 0) + 1;
  const pct = total ? score / total : 0;
  p.best[key] = Math.max(p.best[key] || 0, Math.round(pct * 100));
  // 成就
  const add = (b) => { if (!p.badges.includes(b)) p.badges.push(b); };
  if (p.played[key] === 1) add("初次出擊");
  if (p.best[key] >= 100) add("滿分高手");
  const totalPlayed = Object.values(p.played).reduce((a, b) => a + b, 0);
  if (totalPlayed >= 5) add("勤學不倦");
  if (Object.keys(p.played).length >= 4) add("全能玩家");
  save(p);
  return p;
}

export function getProgress() { return load(); }

export const ALL_BADGES = ["初次出擊", "滿分高手", "勤學不倦", "全能玩家"];
