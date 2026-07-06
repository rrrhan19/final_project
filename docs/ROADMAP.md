# 開發計畫（ROADMAP）

> 本專題的 7 階段開發計畫與完成狀態。架構層級的變更一律先記錄於 `DECISIONS.md` 再更新本檔。

---

## 階段總覽

| Phase | 內容 | 狀態 |
|---|---|---|
| 0 | 立案：架構、決策、分工、repo 骨架 | ✅ 完成 |
| 1 | 資料層：爬蟲 + PostgreSQL schema + 種子/真實資料 | ✅ 完成 |
| 2 | 後端：偵測模型 + API + Gemini + 統計（D010 後為單一 Flask） | ✅ 完成 |
| 3 | 前端：Vue 3 多頁應用（偵測/遊戲/統計/問答/警示牆） | ✅ 完成 |
| 4 | 資料分析與視覺化（ANALYSIS.md + 前端統計頁） | ✅ 完成 |
| 5 | 部署：render 上線（AWS 指南另附） | ✅ 完成（<https://frontend-lvy6.onrender.com>） |
| 6 | 加分：Jetson Orin Nano 邊緣端程式 | ✅ 程式完成（待硬體實跑） |
| 7 | 繳交：1080p 錄影 + 心得 + 收尾 | 🟡 進行中（錄影腳本已備，待錄製） |

---

## 各階段內容

### Phase 0 — 立案
架構與平台決策（D001–D003）、GitHub monorepo 骨架（`frontend/` `backend-api/` `crawler/` `analysis/` `docs/`）。

### Phase 1 — 資料層
- Playwright/requests 爬蟲，鎖定台灣公開反詐來源（D007），遵守 robots.txt。
- PostgreSQL schema：`scam_reports`（統計）、`scam_examples`（話術案例，供訓練與 RAG）、`qa_questions`（遊戲題庫）、`detections`（偵測紀錄，僅存去識別化文字）。
- 種子資料 + `python -m crawler.run --gov` 匯入真實資料。

### Phase 2 — 後端
- 自訓詐騙文字分類器（TF-IDF + LogisticRegression，held-out 測試集評估）。
- 單一 Flask 服務 10 個端點：健康檢查、偵測、網址/電話查詢、回報、AI 問答、警示牆、統計、遊戲出題/批改（D010）。
- 偵測 ensemble：自訓模型 + Gemini + 規則 + RAG，逐層降級（D004/D006）。

### Phase 3 — 前端
Vue 3 + Vite，hash routing 七頁；RWD；環境變數 `VITE_API_URL` 指向 Flask 後端。

### Phase 4 — 資料分析與視覺化
官方年度統計（帶出處）＋ 實際收集樣本的類型分布；分析結論見 `ANALYSIS.md`，圖表上前端統計頁。

### Phase 5 — 部署
render Blueprint（`render.yaml`）：PostgreSQL + Flask Web Service + 前端 Static Site；AWS（Amplify + Elastic Beanstalk + RDS）完整指南見 `DEPLOY.md` 作為計畫書原案佐證（D005）。

### Phase 6 — 加分（軟硬結合）
`edge-jetson/`：攝像頭擷取 → 端側推論 → 呼叫平台 API；無硬體時以 mock 攝像頭驗證流程（D008）。

### Phase 7 — 繳交
1080p 錄影（動機＋程式碼講解＋render 展示）、心得、計畫書 v2、GitHub 連結。

---

## 變更紀錄

| 日期 | 變更 | 決策編號 |
|---|---|---|
| 2026-06-26 | 建立 7 階段計畫 | D001 |
| 2026-06-26 | 後端定 Node+FastAPI、部署定 render | D002 / D003 |
| 2026-06-26 | 偵測改自訓模型+Gemini ensemble；上線前品質總檢 | D006 / D009 |
| 2026-07-04 | 雙後端全併為單一 Flask（回應教授回饋） | D010 |
