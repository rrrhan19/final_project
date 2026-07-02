"""社群回報 + 電話/帳號查詢（功能B，誠實版）。

⚠️ 官方詐騙電話/LINE ID 開放資料已於 2024/11 因新法規下架，故本功能不宣稱官方資料，
   改以「使用者社群回報 + 風險規則提示」運作，介面明確標示。回報會累積成黑名單（回饋迴路）。
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

_REPORTS = Path(__file__).resolve().parents[2] / "db" / "reported.jsonl"


def _load_reports() -> list[dict]:
    if not _REPORTS.exists():
        return []
    out = []
    for line in _REPORTS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def add_report(kind: str, value: str, note: str = "") -> dict:
    value = value.strip()
    if not value:
        return {"ok": False, "error": "內容為空"}
    _REPORTS.parent.mkdir(exist_ok=True)
    with _REPORTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"kind": kind, "value": value, "note": note, "date": date.today().isoformat()}, ensure_ascii=False) + "\n")
    return {"ok": True}


def _norm_phone(p: str) -> str:
    return re.sub(r"[\s\-()]", "", p.strip())


def check_phone(raw: str) -> dict:
    p = _norm_phone(raw)
    reports = [r for r in _load_reports() if r["kind"] == "phone"]
    report_count = sum(1 for r in reports if _norm_phone(r["value"]) == p)

    reasons: list[str] = []
    risk = 0.0
    if report_count:
        risk += min(0.8, 0.4 + 0.1 * report_count)
        reasons.append(f"曾被社群回報 {report_count} 次為可疑號碼")
    if p.startswith("+886") or (p.startswith("002") and "886" in p[:8]):
        risk += 0.45; reasons.append("顯示為「+886」回撥本國號碼，常見於境外詐騙竄改來電顯示")
    elif p.startswith("+") or p.startswith("00"):
        risk += 0.3; reasons.append("國際來電，若非預期請提高警覺")
    if re.match(r"^09\d{8}$", p):
        reasons.append("一般台灣手機格式；號碼本身無法判定，請看內容是否要求匯款/個資")

    risk = min(1.0, risk)
    verdict = "scam" if risk >= 0.5 else ("uncertain" if risk >= 0.25 else "legit")
    if not reasons:
        reasons.append("查無社群回報、格式無明顯異常；號碼正常不代表內容安全，請看對方是否要求匯款/操作ATM")
    return {
        "verdict": verdict,
        "risk": round(risk, 2),
        "report_count": report_count,
        "reasons": reasons,
        "disclaimer": "本查詢基於社群回報與規則提示，非官方資料（官方電話開放資料已下架）。可疑請撥 165 查證。",
    }
