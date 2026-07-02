# 系統架構

> GitHub 會自動渲染下方 mermaid 圖。需要 .drawio/png 版可再轉製。

```mermaid
flowchart TD
  U([使用者]) -->|貼訊息/玩遊戲/看統計| FE[Vue 3 前端<br/>偵測/遊戲/統計/關於]

  FE -->|/api/detect, /api/stats| API[Python FastAPI<br/>偵測 + 統計]
  FE -->|/api/games/*| NODE[Node.js Express<br/>模擬遊戲路由]

  subgraph 偵測 ensemble（逐層降級）
    API --> MODEL[自訓分類器<br/>TF-IDF + LogReg]
    API --> RAG[RAG 相似歷史案例]
    API --> GEM[Google Gemini<br/>理由解釋 第二意見]
  end

  API --> DB[(PostgreSQL<br/>scam_examples / qa_questions / scam_reports)]
  NODE --> DB
  MODEL -. 訓練資料 .-> DB

  CRAWLER[爬蟲<br/>Selenium/Playwright + 165開放資料] -->|去個資後入庫| DB
  JETSON[Jetson Orin Nano<br/>攝像頭 → OCR] -->|/api/detect| API

  subgraph 部署（render 主 / AWS 備）
    FE -.-> RENDER[(render Static + Web Service + PostgreSQL)]
  end
```

## 元件職責
| 元件 | 職責 |
|---|---|
| Vue 前端 | 四頁互動、呈現結果 |
| FastAPI | 偵測（模型+Gemini+RAG ensemble）、統計聚合 |
| Node Express | 模擬遊戲取題與批改（伺服端判分） |
| PostgreSQL | 話術樣本、問答字典、官方年度統計 |
| 爬蟲 | 收集官方開放資料、去個資入庫 |
| Jetson | 邊緣端攝像頭擷取 → OCR → 呼叫偵測 API |

決策理由見 `.claude/agent-os/DECISIONS.md`（D001–D008）。
