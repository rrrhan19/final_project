"""資料分析（升級版，顧問建議撐起作業 #4『π型人』）。

兩個縱深 + 橫向連結：
  (縱深A) 官方年度統計：YoY 成長、每案平均財損趨勢
  (縱深B) 真實收集樣本的文字分析：高頻話術 2-gram、紅旗詞頻率、類型分布
  (橫向) 把文字分析結論連回偵測模型『學到什麼』

純標準庫即可跑（不需 pandas）；有 matplotlib 才額外輸出圖。
    python analysis/analyze.py
輸出：終端洞察 + docs/ANALYSIS.md（+ analysis/output/*.png 若有 matplotlib）
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

try:  # Windows 終端機(cp950)印 emoji 會炸，強制 UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "output"
DOCS = ROOT / "docs" / "ANALYSIS.md"


def load_reports() -> list[dict]:
    return json.loads((ROOT / "db" / "fixtures.json").read_text(encoding="utf-8"))["scam_reports"]


def load_examples() -> list[dict]:
    rows = json.loads((ROOT / "db" / "fixtures.json").read_text(encoding="utf-8"))["scam_examples"]
    ing = ROOT / "db" / "ingested.jsonl"
    if ing.exists():
        for line in ing.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def bigrams(s: str) -> list[str]:
    s = re.sub(r"[^一-鿿]", "", s)  # 只留中文
    return [s[i : i + 2] for i in range(len(s) - 1)]


def main() -> None:
    reports = load_reports()
    examples = load_examples()
    scam = [e for e in examples if e.get("label") == "scam"]

    lines: list[str] = ["# 資料分析報告（自動產生）\n"]

    # ── 縱深A：官方年度趨勢 ──
    lines.append("## 一、官方年度趨勢（刑事局 / 165 打詐儀錶板）\n")
    ry = sorted(reports, key=lambda r: r["year"])
    lines.append("| 年度 | 案件數 | 財損 | 每案平均財損 | 來源 |")
    lines.append("|---|---|---|---|---|")
    for r in ry:
        loss = r.get("loss_amount", 0)
        per = f"{loss / r['case_count'] / 1e4:.1f} 萬/件" if loss and r["case_count"] else "—"
        lines.append(f"| {r['year']} | {r['case_count']:,} | {('%.0f 億' % (loss/1e8)) if loss else '—'} | {per} | {r.get('source','')} |")
    # YoY（有相鄰年）
    if len(ry) >= 2:
        first, last = ry[0], ry[-1]
        growth = (last["case_count"] / first["case_count"] - 1) * 100
        lines.append(f"\n**洞察**：{first['year']}→{last['year']} 案件數成長 **{growth:.0f}%**。"
                     f"⚠️ 2024 起採打詐儀錶板新口徑，與前期不可直接比較。\n")

    # ── 縱深B：真實樣本文字分析 ──
    lines.append("## 二、真實收集樣本的話術文字分析\n")
    lines.append(f"樣本：{len(scam)} 筆（含 165 官方詐騙闢謠案例 + 種子）。\n")

    # 類型分布
    types = Counter(e.get("scam_type") or "未分類" for e in scam)
    lines.append("**類型分布：** " + "、".join(f"{k} {v}" for k, v in types.most_common()) + "\n")

    # 高頻 2-gram（過濾無意義）
    stop = {"我們", "您的", "如果", "可以", "進行", "以及", "這個", "一個", "請您", "通知"}
    bg = Counter()
    for e in scam:
        bg.update(set(b for b in bigrams(e["content"]) if b not in stop))
    top_bg = [f"{w}({c})" for w, c in bg.most_common(15)]
    lines.append("**高頻話術詞（2-gram，去重計篇數）：** " + "、".join(top_bg) + "\n")

    # 紅旗詞命中率
    red = ["匯款", "投資", "帳號", "點選", "連結", "保證", "獲利", "客服", "解除", "個資", "中獎", "貸款"]
    hits = {w: sum(1 for e in scam if w in e["content"]) for w in red}
    hits = {k: v for k, v in sorted(hits.items(), key=lambda x: -x[1]) if v}
    lines.append("**關鍵紅旗詞出現篇數：** " + "、".join(f"{k} {v}" for k, v in hits.items()) + "\n")

    # ── 橫向連結 ──
    lines.append("## 三、橫向連結：分析如何回饋偵測模型\n")
    top_word = bg.most_common(1)[0][0] if bg else "—"
    lines.append(
        f"- 偵測模型（TF-IDF 字元 n-gram）正是從這些高頻話術學特徵；最常見詞如「{top_word}」"
        f"與紅旗詞清單高度重疊，解釋了模型為何能辨識詐騙。\n"
        f"- 類型分布顯示「{types.most_common(1)[0][0]}」案例最多，與官方『假投資為財損最大宗』的趨勢呼應。\n"
        f"- 啟示：補強樣本較少的類型可提升模型平衡性（呼應 EVAL 的類別不平衡發現）。\n"
    )

    DOCS.parent.mkdir(exist_ok=True)
    DOCS.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n→ 已寫入 {DOCS}")

    # 選配圖表
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False
        OUT.mkdir(exist_ok=True)
        yrs = [r["year"] for r in ry]
        cnts = [r["case_count"] for r in ry]
        plt.figure(); plt.bar([str(y) for y in yrs], cnts, color="#1e4fd6")
        plt.title("全台詐騙案件數（官方）"); plt.tight_layout(); plt.savefig(OUT / "by_year.png"); plt.close()
        tt = types.most_common(8)
        plt.figure(); plt.barh([k for k, _ in tt][::-1], [v for _, v in tt][::-1], color="#c0392b")
        plt.title("收集樣本類型分布"); plt.tight_layout(); plt.savefig(OUT / "sample_types.png"); plt.close()
        print(f"圖表輸出至 {OUT}")
    except ImportError:
        print("（未裝 matplotlib，略過圖表；pip install matplotlib 後可產圖）")


if __name__ == "__main__":
    main()
