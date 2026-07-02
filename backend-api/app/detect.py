"""詐騙偵測核心（D006：自訓模型 + Gemini + RAG ensemble；逐層降級）。

流程：
1. RAG — 從 scam_examples 用關鍵詞重疊找最相似的歷史案例（baseline；可升級 pgvector）。
2. 自訓模型 — TF-IDF + LogisticRegression 給 P(scam)（模型檔存在才有）。
3. Gemini — 有 key 時給 verdict + 理由（RAG grounding）。
4. ensemble — 合併模型機率與 Gemini 信心；都沒有則規則 fallback。
engine 標示：model+gemini+rag / model+rag / gemini+rag / rule-fallback。
"""
from __future__ import annotations

import os
import re

from .data import get_scam_examples
from .model import predict_proba

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
# 月度呼叫上限（成本護欄，顧問建議）：超過就降級不打 Gemini
GEMINI_MONTHLY_CAP = int(os.getenv("GEMINI_MONTHLY_CAP", "1000"))
_gem_calls = {"month": "", "count": 0}


def _gemini_quota_ok() -> bool:
    import datetime

    m = datetime.date.today().strftime("%Y-%m")
    if _gem_calls["month"] != m:
        _gem_calls["month"], _gem_calls["count"] = m, 0
    if _gem_calls["count"] >= GEMINI_MONTHLY_CAP:
        return False
    _gem_calls["count"] += 1
    return True

# 規則 fallback 用的高風險訊號詞
_RED_FLAGS = [
    "保證獲利", "穩賺不賠", "穩賺", "獲利", "帶單", "內線", "飆股", "漲停",
    "安全帳戶", "洗錢", "通緝", "地檢署", "檢警",
    "解除分期", "操作ATM", "操作atm", "ATM",
    "先匯款", "先付款", "匯款到", "指定帳戶", "手續費",
    "限時", "名額有限", "要買要快", "速加", "點選連結", "更新資料",
]
_URL_RE = re.compile(r"https?://\S+")


def _tokens(s: str) -> set[str]:
    # 中文無空白，用 2-gram 粗略切詞做關鍵詞重疊
    s = re.sub(r"\s+", "", s)
    return {s[i : i + 2] for i in range(len(s) - 1)} if len(s) >= 2 else {s}


def rag_search(text: str, k: int = 3) -> list[dict]:
    """以 2-gram Jaccard 相似度找最相近的歷史案例。"""
    q = _tokens(text)
    scored = []
    for ex in get_scam_examples():
        t = _tokens(ex["content"])
        inter = len(q & t)
        union = len(q | t) or 1
        score = inter / union
        scored.append({**ex, "score": round(score, 3)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]


def _rule_score(text: str, hits: list[dict]) -> tuple[float, list[str]]:
    """回傳 (規則風險分 0~1, 理由列表)。"""
    matched = [w for w in _RED_FLAGS if w.lower() in text.lower()]
    has_url = bool(_URL_RE.search(text))
    top = hits[0] if hits else None
    sim_scam = bool(top and top["label"] == "scam" and top["score"] >= 0.12)

    score = min(1.0, 0.18 * len(matched) + (0.25 if has_url else 0) + (0.3 if sim_scam else 0))
    reasons = []
    if matched:
        reasons.append(f"出現高風險詞：{'、'.join(matched[:6])}")
    if has_url:
        reasons.append("含外部連結，留意釣魚風險")
    if sim_scam:
        reasons.append(f"與歷史「{top['scam_type']}」話術相似（{top['score']}）")
    return score, reasons


def _rule_verdict(text: str, hits: list[dict]) -> dict:
    score, reasons = _rule_score(text, hits)
    if not reasons:
        reasons.append("未偵測到明顯詐騙訊號，但仍請保持警覺")
    return {
        "verdict": _verdict_from_conf(score) if score >= 0.3 else "legit",
        "confidence": round(score, 2),
        "reasoning": "；".join(reasons) + "。",
        "engine": "rule-fallback",
    }


def _gemini_verdict(text: str, hits: list[dict]) -> dict | None:
    try:
        from google import genai
    except Exception:
        return None
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        examples = "\n".join(
            f"- [{h['label']}/{h.get('scam_type') or '一般'}] {h['content']}" for h in hits
        )
        prompt = (
            "你是台灣反詐騙助理。判斷以下『待測訊息』是否為詐騙。\n"
            "參考歷史案例（grounding）：\n" + examples + "\n\n"
            "待測訊息：\n" + text + "\n\n"
            "只輸出 JSON，欄位：verdict(scam|legit|uncertain)、confidence(0~1 數字)、reasoning(中文一兩句理由)。"
        )
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        import json as _json

        raw = re.sub(r"^```json|```$", "", resp.text.strip(), flags=re.M).strip()
        data = _json.loads(raw)
        return {
            "verdict": data.get("verdict", "uncertain"),
            "confidence": float(data.get("confidence", 0.5)),
            "reasoning": data.get("reasoning", ""),
            "engine": "gemini+rag",
        }
    except Exception as e:  # noqa: BLE001 — Gemini 失敗時退回規則
        print(f"[detect] Gemini failed, falling back to rules: {e}")
        return None


def _verdict_from_conf(conf: float) -> str:
    if conf >= 0.5:
        return "scam"
    if conf >= 0.3:
        return "uncertain"
    return "legit"


def detect(text: str) -> dict:
    hits = rag_search(text)
    rule_s, rule_reasons = _rule_score(text, hits)
    model_p = predict_proba(text)                                  # 自訓模型 P(scam)
    # Gemini 第二意見 + 理由（有 key 且未超月度上限才打，控制成本）
    gem = _gemini_verdict(text, hits) if (GEMINI_API_KEY and _gemini_quota_ok()) else None

    if model_p is None and gem is None:
        # 都沒有 → 純規則 fallback
        result = _rule_verdict(text, hits)
    else:
        # 模型為主訊號（held-out 已驗證 Recall 高、FPR 低）；規則只能「往上加分」不拖累；
        # Gemini 在線時與當前分數對半融合（第二意見）。
        reasons = list(rule_reasons)
        engine = ["rule"]
        if model_p is not None:
            conf = model_p
            reasons.append(f"自訓模型詐騙機率 {model_p:.0%}")
            engine.insert(0, "model")
        else:
            conf = rule_s
        # 規則「強烈」命中（多個紅旗詞，rule_s>=0.5）時才往上加分，避免弱訊號誤推正常訊息
        if rule_s >= 0.5:
            conf = conf + 0.5 * rule_s * (1 - conf)
        if gem is not None:
            conf = 0.6 * conf + 0.4 * gem["confidence"]
            if gem.get("reasoning"):
                reasons.append(gem["reasoning"].rstrip("。"))
            engine.insert(0, "gemini")
        conf = round(min(1.0, conf), 2)
        if not reasons:
            reasons.append("未偵測到明顯詐騙訊號，但仍請保持警覺")
        result = {
            "verdict": _verdict_from_conf(conf),
            "confidence": conf,
            "reasoning": "；".join(reasons) + "。",
            "engine": "+".join(engine) + "+rag",
        }

    result["similar_examples"] = [
        {"scam_type": h.get("scam_type"), "content": h["content"], "score": h["score"]}
        for h in hits
        if h["score"] > 0
    ]
    return result
