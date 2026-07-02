# crawler — 動態網頁爬蟲

收集 2021–2025 詐騙案例資料 → 寫入 PostgreSQL（作業需求 #3）。

## 技術
Python + Selenium / Playwright（動態網頁）+ psycopg。

## 啟動
```bash
pip install -r requirements.txt

# 1) 真實資料（推薦）：警政署 165 官方詐騙闢謠開放資料 → db/ingested.jsonl（無 DB）或 DB
python -m crawler.run --gov                 # 抓全部；--limit N 限制筆數

# 2) 動態網頁爬蟲（自訂來源，需確認該站 robots/條款）
playwright install chromium
python -m crawler.run --url https://example.org/cases --selector "li.case" --type 假投資

# 3) 內建示範（不連外，驗證 pipeline + 去個資）
python -m crawler.run --demo
```

## 資料流（閉環）
`--gov`/`--url` 收集 → 無 DB 時寫 `db/ingested.jsonl`（去重）→ backend-api 的偵測/RAG 與
`model/train.py` 訓練都會**自動合併 fixtures + ingested**。所以：抓真資料 → 重跑 `python -m model.train`
→ 偵測立刻變準，全程不需 DB。有 `DATABASE_URL` 時則直接進 PostgreSQL。

## 來源（D007）
- **統計/話術**：data.gov.tw `dataset/38262` 165 詐騙闢謠專區（政府開放授權，免費）→ `sources_gov.py`
- **動態頁**：165 全民防騙網等（`sources.py` 的 Playwright 通用解析）

## 規範（Hard Rule #5）
- 只收公開資料，遵守 `robots.txt` 與來源站條款。
- 詐騙資料不得含個資。
- 可重複執行、有去重。

## 資料流
來源站 → 解析 → 正規化 → 寫入 `scam-db`（見 `analysis/` 與 `backend-api/` 共用 schema）。
