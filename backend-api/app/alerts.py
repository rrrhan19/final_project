"""最新詐騙手法警示牆（功能C）。即時抓 165 闢謠開放資料（記憶體快取）；離線用 fixtures 樣本。"""
from __future__ import annotations

import csv
import io
import json
import urllib.request
from functools import lru_cache
from pathlib import Path

_FIXTURES = Path(__file__).resolve().parents[2] / "db" / "fixtures.json"
_CSV = (
    "https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/"
    "4F4DF9A5-DF4C-4EE8-A50D-869347D38D9E/resource/"
    "0180F4A7-335D-4D69-A8D8-16E3EDEE617D/download"
)


@lru_cache(maxsize=1)
def _fetch_official() -> tuple:
    """回傳 (alerts list, source)；抓不到回 ([], '')。tuple 以便 lru_cache。"""
    try:
        req = urllib.request.Request(_CSV, headers={"User-Agent": "ScamPlatformBot/0.1"})
        raw = urllib.request.urlopen(req, timeout=20).read()
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
        items = []
        for rec in reader:
            title = (rec.get("標題") or "").strip()
            body = (rec.get("發佈內容") or "").strip()
            d = (rec.get("發佈時間") or "").strip()[:10]
            if title:
                items.append({"date": d, "title": title, "summary": body[:200],
                              "link": "https://165.npa.gov.tw/"})
        items.sort(key=lambda x: x["date"], reverse=True)
        return (tuple(json.dumps(i) for i in items), "165 反詐騙闢謠專區（官方即時）")
    except Exception as e:  # noqa: BLE001
        print(f"[alerts] fetch failed, using fixture: {e}")
        return ((), "")


def get_alerts(limit: int = 10) -> dict:
    packed, source = _fetch_official()
    if packed:
        items = [json.loads(s) for s in packed][:limit]
        return {"alerts": items, "source": source}
    sample = json.loads(_FIXTURES.read_text(encoding="utf-8")).get("alerts_sample", [])
    return {"alerts": sample[:limit], "source": "示意樣本（離線）"}
