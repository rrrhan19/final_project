"""網址安全檢查（功能A）。

兩層：
1. 官方黑名單命中：165/刑事局「遭停止解析涉詐網站」開放資料（db/scam_urls.txt，或 fixtures 樣本）。
2. heuristics：可疑 TLD、純 IP、punycode、過多數字/連字號、仿冒知名品牌的相似網域。
"""
from __future__ import annotations

import ipaddress
import json
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

_ROOT = Path(__file__).resolve().parents[2]
_URLS_TXT = _ROOT / "db" / "scam_urls.txt"
_FIXTURES = _ROOT / "db" / "fixtures.json"

# 詐騙站常見的高風險 TLD
_RISKY_TLDS = {"cc", "top", "xyz", "store", "vip", "mom", "cfd", "icu", "tk", "gq", "buzz", "click", "rest", "sbs"}
# 常被仿冒的品牌關鍵詞（出現在非官方網域時可疑）
_BRANDS = ["paypal", "line", "google", "apple", "facebook", "momo", "shopee", "pchome", "binance", "metamask", "post", "gov", "165", "esun", "cathay", "ctbc"]


@lru_cache(maxsize=1)
def _blocklist() -> set[str]:
    if _URLS_TXT.exists():
        return {d.strip().lower() for d in _URLS_TXT.read_text(encoding="utf-8").splitlines() if d.strip()}
    sample = json.loads(_FIXTURES.read_text(encoding="utf-8")).get("scam_url_sample", [])
    return {d.lower() for d in sample}


def blocklist_size() -> int:
    return len(_blocklist())


def _extract_domain(raw: str) -> str:
    raw = raw.strip()
    if "://" not in raw:
        raw = "http://" + raw
    host = (urlparse(raw).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def check_url(raw: str) -> dict:
    domain = _extract_domain(raw)
    if not domain:
        return {"verdict": "uncertain", "matched": False, "domain": "", "reasons": ["無法解析網址"], "risk": 0.0}

    bl = _blocklist()
    # 1) 官方黑名單（完整網域或其父網域命中）
    parts = domain.split(".")
    for i in range(len(parts) - 1):
        cand = ".".join(parts[i:])
        if cand in bl:
            return {
                "verdict": "scam",
                "matched": True,
                "domain": domain,
                "risk": 1.0,
                "reasons": [f"命中官方涉詐網站清單（{cand}）— 已遭停止解析或經機關認定涉詐"],
            }

    # 2) heuristics
    reasons: list[str] = []
    risk = 0.0
    tld = parts[-1] if parts else ""
    if tld in _RISKY_TLDS:
        risk += 0.35; reasons.append(f"使用高風險頂級網域 .{tld}（詐騙站常見）")
    try:
        ipaddress.ip_address(domain)
        risk += 0.4; reasons.append("直接以 IP 位址當網址（正常網站少見）")
    except ValueError:
        pass
    if domain.startswith("xn--") or "xn--" in domain:
        risk += 0.4; reasons.append("含 punycode 編碼，可能假冒近似網域")
    if len(re.findall(r"\d", domain)) >= 5:
        risk += 0.2; reasons.append("網域含大量數字（隨機產生特徵）")
    if domain.count("-") >= 3:
        risk += 0.15; reasons.append("網域含大量連字號")
    host_no_tld = ".".join(parts[:-1]) if len(parts) > 1 else domain
    for b in _BRANDS:
        if b in host_no_tld and not host_no_tld.endswith(b):
            risk += 0.3; reasons.append(f"網域含知名品牌字「{b}」但非其官方網域，疑似仿冒"); break

    risk = min(1.0, risk)
    if risk >= 0.5:
        verdict = "scam"
    elif risk >= 0.25:
        verdict = "uncertain"
    else:
        verdict = "legit"
    if not reasons:
        reasons.append("未命中官方黑名單，也無明顯可疑特徵；但仍請留意，無法保證絕對安全")
    return {"verdict": verdict, "matched": False, "domain": domain, "risk": round(risk, 2), "reasons": reasons}
