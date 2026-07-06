# AI 使用說明

本文件說明系統內 AI 的角色、實際送往 Gemini 的 prompt，以及 Gemini 月度用量護欄。

## AI 角色架構圖（文字版）

```text
使用者
  |
  +-- 偵測頁 /api/detect
  |     |
  |     +-- RAG 相似案例檢索
  |     |     - 從 scam_examples 取歷史案例
  |     |     - 以 2-gram Jaccard 找最相似案例，提供 Gemini grounding 與規則判斷參考
  |     |
  |     +-- 規則引擎
  |     |     - 檢查高風險詞、外部連結、相似詐騙案例
  |     |     - 產生 rule_s 與理由
  |     |     - 自訓模型與 Gemini 都不可用時，輸出 rule-fallback
  |     |
  |     +-- 自訓模型
  |     |     - TF-IDF + LogisticRegression
  |     |     - 輸出 P(scam)，作為主要詐騙機率訊號
  |     |     - 若模型檔不存在或 predict_proba 回傳 None，改由規則分數起算
  |     |
  |     +-- Gemini 偵測第二意見
  |           - 只有在 GEMINI_API_KEY 存在且未超過 GEMINI_MONTHLY_CAP 時呼叫
  |           - 使用 RAG 相似案例作 grounding
  |           - 回傳 verdict、confidence、reasoning
  |           - 與自訓模型/規則分數融合，reasoning 併入最終理由
  |
  +-- AI 問答助手 chat
        |
        +-- Gemini 問答
        |     - 以 _SYSTEM 約束角色、語氣、安全提醒與回答長度
        |     - 將最近 6 則 history 加上本次 message 組成 contents
        |
        +-- 無 key 或 Gemini 失敗
              - 回傳固定防詐提醒 _FALLBACK
              - engine 標示為 fallback
```

降級路徑：

1. 偵測流程有 `GEMINI_API_KEY` 且 `_gemini_quota_ok()` 通過時，才會呼叫 Gemini。
2. Gemini 不可用時，偵測仍使用自訓模型、規則引擎與 RAG 相似案例；engine 可能是 `model+rag`。
3. 自訓模型也不可用時，偵測改用純規則 fallback；engine 為 `rule-fallback`。
4. 問答助手無 `GEMINI_API_KEY` 或 Gemini 呼叫失敗時，直接回傳固定 `_FALLBACK` 防詐提醒；engine 為 `fallback`。

## 實際 prompts 轉錄

### 偵測：Gemini 第二意見

來源：`backend-api/app/detect.py:107`

```python
prompt = (
    "你是台灣反詐騙助理。判斷以下『待測訊息』是否為詐騙。\n"
    "參考歷史案例（grounding）：\n" + examples + "\n\n"
    "待測訊息：\n" + text + "\n\n"
    "只輸出 JSON，欄位：verdict(scam|legit|uncertain)、confidence(0~1 數字)、reasoning(中文一兩句理由)。"
)
```

動態欄位來源：

- `examples`：`backend-api/app/detect.py:104` 至 `backend-api/app/detect.py:106`
- `text`：`_gemini_verdict(text, hits)` 的待測訊息參數，來源為 `backend-api/app/detect.py:97`
- Gemini 呼叫：`backend-api/app/detect.py:113`

`examples` 的實際格式：

```python
examples = "\n".join(
    f"- [{h['label']}/{h.get('scam_type') or '一般'}] {h['content']}" for h in hits
)
```

### 問答助手：system instruction

來源：`backend-api/app/assistant.py:9`

```python
_SYSTEM = (
    "你是台灣的反詐騙助理。用繁體中文、同理而清楚的口吻，協助使用者判斷情境是否為詐騙、"
    "說明常見手法與該怎麼自保。重要原則：不保證絕對、提醒可撥 165 查證、勸阻匯款或提供個資；"
    "回答簡潔（3-5 句），必要時條列。"
)
```

送入 Gemini 的位置：`backend-api/app/assistant.py:40`

```python
config=types.GenerateContentConfig(system_instruction=_SYSTEM),
```

### 問答助手：chat contents

來源：`backend-api/app/assistant.py:32`

```python
convo = ""
for h in (history or [])[-6:]:
    who = "使用者" if h.get("role") == "user" else "助理"
    convo += f"{who}：{h.get('content', '')}\n"
convo += f"使用者：{message}\n助理："
```

Gemini 呼叫：`backend-api/app/assistant.py:37`

```python
resp = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=convo,
    config=types.GenerateContentConfig(system_instruction=_SYSTEM),
)
```

## 月度用量護欄：GEMINI_MONTHLY_CAP

來源：`backend-api/app/detect.py:20`

```python
# 月度呼叫上限（成本護欄，顧問建議）：超過就降級不打 Gemini
GEMINI_MONTHLY_CAP = int(os.getenv("GEMINI_MONTHLY_CAP", "1000"))
_gem_calls = {"month": "", "count": 0}
```

護欄邏輯來源：`backend-api/app/detect.py:25`

```python
def _gemini_quota_ok() -> bool:
    import datetime

    m = datetime.date.today().strftime("%Y-%m")
    if _gem_calls["month"] != m:
        _gem_calls["month"], _gem_calls["count"] = m, 0
    if _gem_calls["count"] >= GEMINI_MONTHLY_CAP:
        return False
    _gem_calls["count"] += 1
    return True
```

偵測端的呼叫條件來源：`backend-api/app/detect.py:141`

```python
# Gemini 第二意見 + 理由（有 key 且未超月度上限才打，控制成本）
gem = _gemini_verdict(text, hits) if (GEMINI_API_KEY and _gemini_quota_ok()) else None
```

行為說明：

- `GEMINI_MONTHLY_CAP` 由環境變數設定，預設值為 `1000`。
- `_gem_calls` 是行程記憶體內的簡易計數器，以 `YYYY-MM` 分月統計。
- 每月第一次呼叫或月份切換時，計數歸零。
- 偵測流程每次通過 `_gemini_quota_ok()` 會先遞增計數，再呼叫 Gemini。
- 當計數達到 `GEMINI_MONTHLY_CAP`，偵測流程不再呼叫 Gemini，改走自訓模型、規則引擎與 RAG 的降級路徑。
- 此護欄目前只套用在偵測端；問答助手的 `chat` 流程只檢查 `GEMINI_API_KEY` 與 Gemini 呼叫是否成功。
