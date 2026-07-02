"""Jetson Orin Nano 邊緣端：攝像頭 → OCR → 呼叫平台偵測（D008，作業加分 #7）。

軟硬結合流程：
  攝像頭擷取可疑訊息畫面（如詐騙簡訊/海報）
  → OCR 取出文字（pytesseract，支援繁中）
  → POST 平台 /api/detect
  → 在畫面/終端顯示「是否詐騙 + 信心 + 理由」

無 Jetson/攝像頭時：用 --mock "文字" 直接走後段流程驗證；
無後端時：自動以離線提示替代，仍印出擷取到的文字。

實機需求：opencv-python、pytesseract（+系統 tesseract-ocr 與 chi_tra 語言包）、requests。
"""
from __future__ import annotations

import argparse
import os
import sys

try:  # Windows 終端機(cp950)印 emoji 會炸，強制 UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API_URL = os.getenv("PLATFORM_API_URL", "http://localhost:8000")


def capture_frame_text(mock: str | None) -> str:
    """擷取一張畫面並 OCR 出文字；mock 模式直接回傳給定文字。"""
    if mock is not None:
        return mock

    try:
        import cv2  # noqa: F401
    except ImportError:
        print("[edge] 找不到 opencv，請用 --mock 測試或在 Jetson 安裝 opencv-python", file=sys.stderr)
        sys.exit(2)

    import cv2

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[edge] 無法開啟攝像頭（0 號裝置）", file=sys.stderr)
        sys.exit(2)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        print("[edge] 擷取畫面失敗", file=sys.stderr)
        sys.exit(2)

    try:
        import pytesseract

        return pytesseract.image_to_string(frame, lang="chi_tra").strip()
    except Exception as e:  # noqa: BLE001
        print(f"[edge] OCR 失敗（檢查 tesseract 與 chi_tra）：{e}", file=sys.stderr)
        return ""


def call_detect(text: str) -> dict | None:
    try:
        import urllib.request
        import json

        req = urllib.request.Request(
            f"{API_URL}/api/detect",
            data=json.dumps({"text": text}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:  # noqa: BLE001
        print(f"[edge] 呼叫平台失敗（後端是否啟動？{API_URL}）：{e}", file=sys.stderr)
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Jetson 邊緣端詐騙偵測")
    ap.add_argument("--mock", help="略過攝像頭，直接用這段文字（無硬體測試）")
    args = ap.parse_args()

    text = capture_frame_text(args.mock)
    print(f"[edge] 擷取文字：{text or '(空)'}")
    if not text:
        return

    result = call_detect(text)
    if result is None:
        return
    label = {"scam": "⚠️ 疑似詐騙", "legit": "✅ 看起來正常", "uncertain": "❓ 無法確定"}
    print(f"[edge] 判定：{label.get(result['verdict'], result['verdict'])}"
          f"（信心 {round(result['confidence'] * 100)}%，引擎 {result['engine']}）")
    print(f"[edge] 理由：{result['reasoning']}")


if __name__ == "__main__":
    main()
