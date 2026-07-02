# 繳交檢查清單（對照作業 9 條）

| # | 作業要求 | 狀態 | 對應產出 |
|---|---|---|---|
| 1 | GitHub repo + 專題計畫書 + 專案架構 | ✅ 程式/架構；計畫書待回填 | repo、`docs/`、`PROPOSAL_DRAFT.md`、架構圖待補 |
| 2 | 資料庫用 render PostgreSQL | 🟡 設定就緒待部署 | `render.yaml`、`db/schema.sql` |
| 3 | 爬蟲收集資料入庫 | ✅ 完成（165 官方真實資料） | `crawler/`、`db/ingested.jsonl` |
| 4 | 資料分析 + 部署在 render | 🟡 分析✅、部署待執行 | `analysis/`、`docs/ANALYSIS.md`、`docs/DEPLOY.md` |
| 5 | GitHub連結 / 1080p錄影 / 動機 / 講解 / 程式碼 / 人文 / 心得 / 說故事 | 🟡 腳本+心得✅、錄影待錄 | `docs/DEMO_SCRIPT.md`、`docs/REFLECTION.md`、About 頁 |
| 6 | AI 是能力放大器 / 作品集可落地 | ✅ | 自訓模型+Gemini、`REFLECTION.md` |
| 7 | 加分：Jetson + 攝像頭 | 🟡 程式✅、實機待硬體 | `edge-jetson/` |
| 8 | 每位成員都貢獻功能程式碼 | ⚠️ 需釐清團隊/個人 | `TEAM.md` |
| 9 | 想到再補充 | — | — |

## 繳交前最終動作
- [ ] **部署 render** 拿公開 URL，寫進 README 頂部
- [ ] 後台填 `GEMINI_API_KEY`、`ALLOWED_ORIGINS`（鎖前端網域）
- [ ] 灌資料：`schema.sql` + `seed.sql` + `python -m crawler.run --gov`
- [ ] **錄製 1080p mp4**（照 `DEMO_SCRIPT.md`）
- [ ] 回填計畫書四章（用 `PROPOSAL_DRAFT.md` 草稿）
- [ ] 補一張系統架構圖放 `docs/`
- [ ] 釐清 `TEAM.md` 分工（個人或團隊，誠實交代 #8）
- [ ] 跑一次 `docs/EVAL.md` 的 20-trace 走查，確認 demo 不翻車
- [ ] README 頂部放：公開 URL、錄影連結、一句產品介紹
