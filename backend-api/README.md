# backend-api — Python Flask（單一後端）

詐騙偵測模型、統計、Gemini 問答、警示牆、回報、模擬遊戲——全部功能由單一 Flask 服務提供（D010）。

## 技術
Python + Flask + gunicorn + psycopg + scikit-learn + google-genai。

## 啟動
```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python -m model.train                             # 訓練偵測模型（產生 scam_clf.joblib）
python -m flask --app app.flask_app run --port 8000
```

## 環境變數
- `DATABASE_URL` — render PostgreSQL 連線字串（不設則走內建 fixtures，本機可跑）
- `GEMINI_API_KEY` — Google Gemini 金鑰（勿入庫，放 `.env` / render 後台；不設則偵測降級為 model+rule+rag）
- `ALLOWED_ORIGINS` — CORS 白名單（逗號分隔）

## 端點（10）
| Method | Path | 說明 |
|---|---|---|
| GET | `/health` | 健康檢查（含 DB 連線狀態） |
| POST | `/api/detect` | 訊息/網址 → 模型+Gemini+RAG ensemble 判斷是否詐騙＋解釋 |
| POST | `/api/url-check` | 網址風險查詢（官方涉詐網域黑名單） |
| POST | `/api/phone-check` | 電話風險查詢 |
| POST | `/api/report` | 民眾回報疑似詐騙 |
| POST | `/api/chat` | Gemini 防詐問答 |
| GET | `/api/alerts` | 警示牆（近期回報） |
| GET | `/api/stats` | 詐騙統計（官方年度數據帶出處＋樣本類型分布） |
| GET | `/api/games/questions` | 模擬遊戲出題（不外洩答案） |
| POST | `/api/games/answer` | 模擬遊戲批改＋解說 |

完整請求/回應格式見 `docs/API_SPEC.md`。

## 部署
render Web Service，`gunicorn app.flask_app:app`（見根目錄 `render.yaml`）。
