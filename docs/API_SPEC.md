# API 契約（前端 / 後端共用合約）

單一 Flask 後端與前端依此規格對接。所有回應為 JSON。

## backend-api（Flask）— 偵測 / 統計 / 網址 / 電話 / 警示牆 / AI問答 / 模擬遊戲

base: `VITE_API_URL`（本機預設 `http://localhost:8000`）

### `GET /health`
→ `{ "status": "ok", "service": "backend" }`

### `POST /api/detect`
偵測訊息/網址是否為詐騙（D004：Gemini 一發 + RAG，無 key 走規則 fallback）。
```jsonc
// request
{ "text": "老師帶單保證獲利30%，加LINE進VIP群" }
// response
{
  "verdict": "scam",          // scam | legit | uncertain
  "confidence": 0.92,          // 0.0–1.0
  "reasoning": "出現『保證獲利』等投資詐騙典型話術，且與歷史假投資案例高度相似。",
  "similar_examples": [        // RAG 命中的歷史案例（可空）
    { "scam_type": "假投資", "content": "老師帶單穩賺不賠…", "score": 0.81 }
  ],
  "engine": "gemini+rag"       // gemini+rag | rule-fallback
}
```

### `GET /api/stats`
詐騙統計（給前端繪圖；SQL 聚合，非 LLM）。年度為官方真實數據(帶出處)，類型分布為實際收集樣本。
```jsonc
// query: ?from=2020&to=2025
{
  "by_year": [ { "year": 2024, "case_count": 122805, "loss_amount": 50200000000, "source": "刑事局/165打詐儀錶板2024" }, ... ],
  "by_sample_type": [ { "scam_type": "釣魚簡訊", "count": 9 }, ... ],   // 由真實收集的 scam_examples 計算
  "note": "資料口徑與限制說明（誠信揭露）"
}
```

### `GET /api/games/questions?limit=5`
→ 隨機問答（不回傳 `correct_idx` 與 `explanation`，避免前端作弊）
```jsonc
[ { "id": 1, "scam_type": "假投資", "difficulty": 1, "prompt": "…", "options": ["…","…","…"] } ]
```

### `POST /api/games/answer`
```jsonc
// request
{ "question_id": 1, "choice_idx": 1 }
// response
{ "correct": true, "correct_idx": 1, "explanation": "「保證獲利」是投資詐騙典型話術…" }
```
