"""爬蟲 CLI 進入點。

示範（不連外，驗證 parse→去個資→入庫 pipeline）：
    python -m crawler.run --demo

真實來源（待設定 sources.py 的 selector 與 URL 後）：
    python -m crawler.run --url https://example.org/cases --selector "li.case" --type 假投資
"""
from __future__ import annotations

import argparse

from .sources import parse_demo, parse_generic_list
from .store import save_examples


def main() -> None:
    ap = argparse.ArgumentParser(description="反詐平台爬蟲")
    ap.add_argument("--demo", action="store_true", help="跑內建示範（不連外）")
    ap.add_argument("--gov", action="store_true", help="抓 165 詐騙闢謠開放資料（話術樣本）")
    ap.add_argument("--urls", action="store_true", help="抓 165 涉詐網站開放資料（網址黑名單）")
    ap.add_argument("--limit", type=int, help="最多抓幾筆（gov 模式）")
    ap.add_argument("--url", help="目標頁面 URL")
    ap.add_argument("--selector", help="每則案例的 CSS selector")
    ap.add_argument("--type", dest="scam_type", help="詐騙類型標註")
    ap.add_argument("--wait", help="等待出現的 selector（動態頁）")
    args = ap.parse_args()

    if args.demo:
        rows = parse_demo()
        print(f"[demo] parsed {len(rows)} rows（已去個資）：")
        for r in rows:
            print("  -", r["content"])
        save_examples(rows)
        return

    if args.gov:
        from .sources_gov import fetch_gov_debunk

        rows = fetch_gov_debunk(limit=args.limit)
        print(f"[gov] 抓到 {len(rows)} 筆 165 官方詐騙闢謠資料")
        save_examples(rows)
        return

    if args.urls:
        from pathlib import Path
        from .sources_gov import fetch_scam_domains

        doms = fetch_scam_domains()
        out = Path(__file__).resolve().parents[1] / "db" / "scam_urls.txt"
        out.write_text("\n".join(doms), encoding="utf-8")
        print(f"[urls] 抓到 {len(doms)} 筆官方涉詐網域 → {out}")
        return

    if not (args.url and args.selector):
        ap.error("非 --demo 模式需提供 --url 與 --selector")

    from .base import fetch_dynamic  # 延遲匯入，demo 不需 Playwright

    html = fetch_dynamic(args.url, wait_selector=args.wait)
    rows = parse_generic_list(html, args.selector, source=args.url, scam_type=args.scam_type)
    print(f"[crawl] parsed {len(rows)} rows from {args.url}")
    save_examples(rows)


if __name__ == "__main__":
    main()
