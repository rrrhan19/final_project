# model — 自訓詐騙偵測模型（D006）

計畫書 v2「Flask 後端承載自訓詐騙偵測模型」的實現。

| 檔案 | 內容 |
|---|---|
| `train.py` | 訓練：字元 n-gram TF-IDF + LogisticRegression，讀 `scam_examples`（DB 或 fixtures），輸出 `scam_clf.joblib` |
| `scam_clf.joblib` | 訓練產物（`.gitignore`，部署/本機由 train.py 產生） |

## 訓練
```bash
cd backend-api
python -m model.train     # 產生 scam_clf.joblib
```

## 與 Gemini 的關係（ensemble）
偵測時 `app/detect.py` 合併三個訊號（逐層降級）：
- **自訓模型** → 詐騙機率 P(scam)
- **Gemini**（有 key 時）→ 第二意見 + 理由解釋
- **規則 + RAG** → 高風險詞 / 歷史相似案例

engine 欄位顯示實際用到哪些：`gemini+model+rule+rag` → `model+rule+rag` → `rule-fallback`。

> ⚠️ 目前種子資料僅 10 筆，模型會過擬合、預測不準（這就是為何要接真實爬蟲資料）。
> 接真實資料後重跑 `train.py`，模型才有意義。規則訊號的加權可避免小模型過度自信。
