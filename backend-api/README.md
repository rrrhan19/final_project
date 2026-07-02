# backend-api — Python FastAPI

詐騙偵測模型、詐騙統計（資料視覺化資料源）、Google Gemini 串接。

## 技術
Python + FastAPI + uvicorn + SQLAlchemy/psycopg + google-genai。

## 啟動
```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 環境變數
- `DATABASE_URL` — render PostgreSQL 連線字串
- `GEMINI_API_KEY` — Google Gemini 金鑰（勿入庫，放 `.env` / render 後台）

## 端點（規劃）
| Method | Path | 說明 |
|---|---|---|
| GET | `/health` | 健康檢查 |
| POST | `/api/detect` | 輸入訊息/網址 → 模型 + Gemini 判斷是否詐騙 + 解釋 |
| GET | `/api/stats` | 2021–2025 詐騙統計（給前端繪圖） |

## 部署
render Web Service（見根目錄 `render.yaml`）。
