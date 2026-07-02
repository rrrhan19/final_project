"""爬蟲基礎建設：robots.txt 守則 + 動態網頁抓取（Playwright）+ 去個資。

遵守 PROJECT.md Hard Rule #5：只收公開資料、遵守 robots.txt、不存個資。
"""
from __future__ import annotations

import re
import urllib.robotparser
from urllib.parse import urlparse

UA = "ScamPlatformBot/0.1 (academic project; respectful crawl)"

# 粗略遮蔽常見個資（手機、Email、身分證），入庫前一律去識別化
_PII_PATTERNS = [
    (re.compile(r"09\d{2}[- ]?\d{3}[- ]?\d{3}"), "[手機]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[Email]"),
    (re.compile(r"[A-Z][12]\d{8}"), "[身分證]"),
]


def allowed_by_robots(url: str) -> bool:
    """檢查目標 URL 是否被 robots.txt 允許爬取。"""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        # 讀不到 robots.txt 視為保守拒絕，避免誤爬
        return False
    return rp.can_fetch(UA, url)


def scrub_pii(text: str) -> str:
    for pat, repl in _PII_PATTERNS:
        text = pat.sub(repl, text)
    return text


def fetch_dynamic(url: str, wait_selector: str | None = None, timeout_ms: int = 15000) -> str:
    """用 Playwright 抓動態網頁，回傳渲染後的 HTML。需先 `playwright install chromium`。"""
    if not allowed_by_robots(url):
        raise PermissionError(f"robots.txt 不允許爬取：{url}")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=UA)
        page.goto(url, timeout=timeout_ms)
        if wait_selector:
            page.wait_for_selector(wait_selector, timeout=timeout_ms)
        html = page.content()
        browser.close()
    return html
