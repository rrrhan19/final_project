# frontend — Vue.js 前端

動態多頁應用（MPA）：偵測頁、模擬遊戲頁、統計視覺化頁、Gemini 問答頁。

## 技術
Vue 3 + Vite。透過環境變數指向單一 Flask 後端（D010）：
- `VITE_API_URL` → Flask（偵測 / 統計 / Gemini / 模擬遊戲 / 警示牆）

## 啟動
```bash
npm install
npm run dev
```

## 部署
render Static Site，`npm run build` → `dist/`（見根目錄 `render.yaml`）。
