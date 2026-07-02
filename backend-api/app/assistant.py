"""AI 防詐問答助手（功能D）。對話式，用 Gemini；無 key 時給規則化指引 fallback。"""
from __future__ import annotations

import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

_SYSTEM = (
    "你是台灣的反詐騙助理。用繁體中文、同理而清楚的口吻，協助使用者判斷情境是否為詐騙、"
    "說明常見手法與該怎麼自保。重要原則：不保證絕對、提醒可撥 165 查證、勸阻匯款或提供個資；"
    "回答簡潔（3-5 句），必要時條列。"
)

_FALLBACK = (
    "（目前未連接 AI，以下為通用防詐提醒）\n"
    "1. 任何「保證獲利」「穩賺不賠」幾乎都是投資詐騙。\n"
    "2. 要求你操作 ATM、匯款到「安全帳戶」、提供簡訊驗證碼或個資的，請直接掛斷。\n"
    "3. 陌生連結先別點，回到官方 App/網站查詢。\n"
    "4. 不確定就撥 165 反詐騙專線查證，或與家人討論再決定。"
)


def chat(message: str, history: list[dict] | None = None) -> dict:
    if not GEMINI_API_KEY:
        return {"reply": _FALLBACK, "engine": "fallback"}
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        convo = ""
        for h in (history or [])[-6:]:
            who = "使用者" if h.get("role") == "user" else "助理"
            convo += f"{who}：{h.get('content', '')}\n"
        convo += f"使用者：{message}\n助理："
        resp = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=convo,
            config=types.GenerateContentConfig(system_instruction=_SYSTEM),
        )
        return {"reply": resp.text.strip(), "engine": "gemini"}
    except Exception as e:  # noqa: BLE001
        print(f"[assistant] gemini failed: {e}")
        return {"reply": _FALLBACK, "engine": "fallback"}
