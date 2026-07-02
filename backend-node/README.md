# backend-node — Node.js Microservice

模擬遊戲路由 + 問答對（Q&A）查詢 API。

## 技術
Node.js + Express + `pg`（PostgreSQL）。

## 啟動
```bash
npm install
node src/server.js   # 預設讀 PORT、DATABASE_URL 環境變數
```

## 端點（規劃）
| Method | Path | 說明 |
|---|---|---|
| GET | `/health` | 健康檢查 |
| GET | `/api/games/questions` | 取模擬遊戲問答清單 |
| POST | `/api/games/answer` | 提交答案、回傳對錯與解說 |

## 部署
render Web Service（見根目錄 `render.yaml`）。
