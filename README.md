# 安心盾 · 反詐平台（Scam Detection Platform）

> 🌐 **線上 Demo**：https://frontend-lvy6.onrender.com/#/ （render 免費方案，首次開啟需等 ~30–50 秒喚醒後端）
> 📦 **繳交資料**：見 `繳交資料/`（PDF）


偵測詐騙（模型 + Google Gemini）＋模擬遊戲教學＋詐騙統計視覺化（2021–2025）的網站。期末專題。

## 系統架構

```
[ Vue.js 前端 (MPA) ]
        │
        ├──────────────► [ Node.js Microservice ]  模擬遊戲路由 / 問答對查詢
        │
        └──────────────► [ Python FastAPI ]        詐騙偵測模型 / 統計 / Google Gemini
                                   │
                          [ PostgreSQL ]            訓練資料 / 問答字典 / 歷史詐騙資料 2021–2025
```

全部部署於 **render**（前端 Static Site + Node/FastAPI 各一 Web Service + render PostgreSQL）。

## 目錄結構（monorepo）

| 目錄 | 內容 | 技術 |
|---|---|---|
| `frontend/` | Vue.js 多頁前端 | Vue 3 + Vite |
| `backend-node/` | 模擬遊戲路由 + 問答對 API | Node.js + Express |
| `backend-api/` | 偵測（自訓模型 + Gemini）/ 統計 | Python + FastAPI + scikit-learn |
| `backend-api/model/` | 自訓詐騙分類器（TF-IDF + LogReg） | scikit-learn |
| `crawler/` | 爬蟲 + 165 官方開放資料載入 | Python + Selenium/Playwright |
| `analysis/` | 資料分析與視覺化 | Python (pandas/matplotlib) |
| `edge-jetson/` | Jetson 攝像頭 → OCR → 偵測（加分） | Python + OpenCV/pytesseract |
| `deploy/` `docs/DEPLOY.md` | render + AWS 部署設定/指南 | Docker / render.yaml |
| `docs/` | 專題計畫書、架構圖、API 契約、繳交物 | — |

## 功能（一站式反詐工具箱）

1. **偵測中心** — 四合一：訊息偵測（自訓模型+Gemini+RAG）、網址檢查（165 官方涉詐網站黑名單 58k 筆+仿冒 heuristics）、電話查詢（社群回報+風險規則）、截圖偵測（瀏覽器 OCR）。
2. **AI 問答助手** — 對話式防詐諮詢（Gemini，可追問）。
3. **模擬遊戲** — 情境問答教學。
4. **詐騙情報** — 最新手法警示牆（165 官方即時）、官方年度統計、手法圖鑑。
5. **我被騙了** — 受害當下行動步驟 + 165/110 求助管道。
6. **社群回報迴路** — 使用者回報可疑號碼 → 累積黑名單。
7. **資料收集** — 爬蟲收集 165 官方開放資料入庫（闢謠案例 + 涉詐網站）。

## 本機快速啟動（不需 render / Gemini 金鑰即可整套跑）

未設定 `DATABASE_URL` 時，後端自動 fallback 用 `db/fixtures.json`；未設定 `GEMINI_API_KEY` 時，偵測走規則 fallback。三個服務各開一個終端機：

```bash
# 1) FastAPI 後端（偵測 / 統計）
cd backend-api && pip install -r requirements.txt
uvicorn app.main:app --reload          # → http://localhost:8000

# 2) Node 後端（模擬遊戲）
cd backend-node && npm install
node src/server.js                      # → http://localhost:3000

# 3) Vue 前端
cd frontend && npm install
npm run dev                             # → http://localhost:5173
```

接真實資料時：用 `docker compose up -d db` 起本機 Postgres（或填 render 連線字串到各服務的 `.env`），再 `db/schema.sql` + `db/seed.sql`，並設 `GEMINI_API_KEY` 啟用 Gemini 偵測。

## 開發

各子專案的啟動方式見各自的 `README.md`。本專案以 agent-os 管理（`.claude/agent-os/`）—— 規劃、決策、分工見該目錄。

## 文件

- 專題計畫書：`docs/`（原始檔 `專題計畫書.docx`）
- 架構決策：`.claude/agent-os/DECISIONS.md`
- 開發計畫：`.claude/agent-os/ROADMAP.md`
- 成員分工：`TEAM.md`
