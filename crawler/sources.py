"""來源轉接器（adapters）。

每個來源實作 parse(html) -> list[dict]，回傳標準化的 scam_examples 列。
⚠️ 真實來源待使用者指定（例如 165 反詐騙公布欄、防詐達人、新聞）。
請確認該站 robots.txt 與使用條款允許後再啟用，並填入正確的選擇器。
"""
from __future__ import annotations

from bs4 import BeautifulSoup

from .base import scrub_pii


def parse_generic_list(html: str, item_selector: str, source: str, scam_type: str | None = None) -> list[dict]:
    """通用解析：抓出符合 item_selector 的每個區塊文字當作一筆話術樣本。

    使用方式：到目標站找出「每則案例」的 CSS selector，傳進來即可。
    """
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict] = []
    for el in soup.select(item_selector):
        content = scrub_pii(el.get_text(" ", strip=True))
        if len(content) < 8:  # 過短略過
            continue
        rows.append(
            {
                "label": "scam",
                "scam_type": scam_type,
                "content": content,
                "features": None,
                "source": source,
            }
        )
    return rows


# 範例：示範 parse pipeline（用內嵌 HTML，不連外，供 self-test）
DEMO_HTML = """
<ul class="cases">
  <li class="case">投資老師保證獲利，誘導加入私人群組匯款，聯絡 0912-345-678</li>
  <li class="case">假冒物流簡訊，要求點選短網址更新個資並登入</li>
</ul>
"""


def parse_demo(html: str = DEMO_HTML) -> list[dict]:
    return parse_generic_list(html, "li.case", source="demo", scam_type="示範")
