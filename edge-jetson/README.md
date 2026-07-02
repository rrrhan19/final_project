# edge-jetson — Jetson Orin Nano 邊緣端（D008，作業加分 #7）

軟硬結合：攝像頭擷取可疑訊息畫面 → OCR → 呼叫平台 `/api/detect` → 顯示判定。

```
[攝像頭] → [OCR 取文字] → POST /api/detect → [⚠️詐騙 / ✅正常 + 信心 + 理由]
```

## 無硬體測試（任何電腦）
```bash
# 需後端在跑（backend-api）；用文字略過攝像頭
PLATFORM_API_URL=http://localhost:8000 python scam_cam.py --mock "老師帶單保證獲利30%速加LINE"
```

## Jetson 實機
```bash
sudo apt install tesseract-ocr tesseract-ocr-chi-tra
pip install -r requirements.txt
PLATFORM_API_URL=https://<your-render-api> python scam_cam.py   # 開攝像頭即時偵測
```

## 設計
- 偵測本身仍在平台後端（模型 + Gemini），Jetson 負責**擷取 + OCR + 串接**，符合「軟硬結合」。
- 進階可改成端側推論（把 `model/scam_clf.joblib` 下放 Jetson 離線判斷），此處先採雲端 API 最單純。
- `--mock` 與離線錯誤處理讓無硬體/無後端時仍能驗證流程。
