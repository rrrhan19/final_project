"""政府開放資料來源（D007）。

警政署 165「詐騙闢謠專區」開放資料（政府資料開放授權條款-第1版，免費）。
資料集：https://data.gov.tw/dataset/38262
欄位：編號 / 標題 / 發佈時間 / 發佈內容

這些是官方對真實詐騙手法的描述/闢謠，作為偵測模型的「詐騙樣態」參考與 RAG grounding。
（屬開放資料下載，非網頁爬蟲；動態頁爬蟲見 sources.py 的 Playwright 路徑。）
"""
from __future__ import annotations

import csv
import io
import urllib.request

from .base import scrub_pii

# 165 詐騙闢謠專區 CSV
GOV_DEBUNK_CSV = (
    "https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/"
    "4F4DF9A5-DF4C-4EE8-A50D-869347D38D9E/resource/"
    "0180F4A7-335D-4D69-A8D8-16E3EDEE617D/download"
)
# 165/刑事局「遭停止解析涉詐網站」CSV（欄位：民國年月/網域/網站性質/法律依據/聲請單位）
GOV_SCAM_URLS_CSV = (
    "https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/"
    "29E8E643-88ED-4952-B21E-BD42A3B7108C/resource/"
    "CFA7A42B-3E8B-478E-9227-A627E7816D97/download"
)
UA = "ScamPlatformBot/0.1 (academic project)"


def fetch_scam_domains() -> list[str]:
    """下載官方涉詐網站清單，回傳去重後的網域列表。"""
    req = urllib.request.Request(GOV_SCAM_URLS_CSV, headers={"User-Agent": UA})
    raw = urllib.request.urlopen(req, timeout=90).read()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    seen, out = set(), []
    for rec in reader:
        d = (rec.get("網域") or "").strip().lower().lstrip("www.")
        if d and d not in seen:
            seen.add(d)
            out.append(d)
    return out


def _classify_type(text: str) -> str:
    """從標題+內容粗略歸類詐騙類型（涵蓋常見手法，盡量減少未分類）。"""
    rules = [
        ("假投資", ["投資", "飆股", "帶單", "虛擬貨幣", "博弈", "股票", "獲利", "理財", "外匯", "基金", "老師"]),
        ("假網拍購物", ["購物", "網拍", "賣家", "拍賣", "電商", "代購", "賣場", "蝦皮", "面交", "貨到付款", "團購"]),
        ("假冒公務機關", ["檢警", "地檢", "公務", "健保", "監理", "稅", "法院", "戶政", "警察", "市府", "勞保", "郵局"]),
        ("解除分期付款", ["分期", "ATM", "解除", "扣款", "客服", "刷卡", "重複", "升級會員"]),
        ("假交友愛情", ["交友", "愛情", "感情", "約會", "男友", "女友", "曖昧", "婚"]),
        ("釣魚簡訊連結", ["簡訊", "連結", "包裹", "物流", "釣魚", "個資", "網址", "點選", "貨運", "ETC", "電子發票", "登入"]),
        ("假貸款", ["貸款", "借款", "信貸", "周轉", "代辦"]),
        ("中獎詐騙", ["中獎", "抽獎", "贈品", "免費領"]),
        ("假冒親友", ["猜猜我是誰", "急用", "借錢", "幫我", "換號碼"]),
        ("遊戲/點數", ["遊戲", "點數", "寶物", "代儲", "序號"]),
    ]
    for label, kws in rules:
        if any(k in text for k in kws):
            return label
    return "其他"


def fetch_gov_debunk(limit: int | None = None) -> list[dict]:
    """下載並解析 165 闢謠開放資料，回傳標準化 scam_examples 列。"""
    req = urllib.request.Request(GOV_DEBUNK_CSV, headers={"User-Agent": UA})
    raw = urllib.request.urlopen(req, timeout=60).read()
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    rows: list[dict] = []
    for i, rec in enumerate(reader):
        if limit and i >= limit:
            break
        title = (rec.get("標題") or "").strip()
        body = (rec.get("發佈內容") or "").strip()
        content = scrub_pii(f"{title}：{body}" if title else body)
        if len(content) < 10:
            continue
        rows.append(
            {
                "label": "scam",  # 官方詐騙樣態描述，作為詐騙參考文本
                "scam_type": _classify_type(f"{title}{body}"),
                "content": content,
                "features": "官方闢謠/詐騙手法描述",
                "source": "data.gov.tw/dataset/38262 (165闢謠)",
            }
        )
    return rows
