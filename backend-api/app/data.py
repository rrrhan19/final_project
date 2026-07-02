"""資料存取層：有 DATABASE_URL 走 PostgreSQL，否則 fallback 用 db/fixtures.json。

讓整套不需任何 DB 也能 demo（D004 fallback 精神）。
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL")
_FIXTURES = Path(__file__).resolve().parents[2] / "db" / "fixtures.json"


_INGESTED = Path(__file__).resolve().parents[2] / "db" / "ingested.jsonl"


@lru_cache(maxsize=1)
def _fixtures() -> dict:
    return json.loads(_FIXTURES.read_text(encoding="utf-8"))


def _ingested_examples() -> list[dict]:
    """爬蟲收集的真實資料（無 DB 時的累積檔）。"""
    if not _INGESTED.exists():
        return []
    out = []
    for line in _INGESTED.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


@lru_cache(maxsize=1)
def _engine():
    """延遲建立 SQLAlchemy engine；失敗則回 None 觸發 fallback。"""
    if not DATABASE_URL:
        return None
    try:
        from sqlalchemy import create_engine

        url = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        eng = create_engine(url, pool_pre_ping=True)
        with eng.connect():  # 連線測試
            pass
        return eng
    except Exception as e:  # noqa: BLE001 — DB 不可用時優雅退回 fixtures
        print(f"[data] DB unavailable, falling back to fixtures: {e}")
        return None


def using_db() -> bool:
    return _engine() is not None


def get_scam_examples() -> list[dict]:
    eng = _engine()
    if eng is None:
        return _fixtures()["scam_examples"] + _ingested_examples()
    from sqlalchemy import text

    with eng.connect() as c:
        rows = c.execute(text("SELECT label, scam_type, content FROM scam_examples")).mappings()
        return [dict(r) for r in rows]


def get_stats(year_from: int = 2020, year_to: int = 2025) -> dict:
    """回傳：
    - by_year：官方年度詐騙統計（真實、帶出處）
    - by_sample_type：我們實際收集的官方案例樣本之類型分布（真實，由 scam_examples 計算）
    - note：資料口徑與限制說明（誠信揭露）
    """
    eng = _engine()
    if eng is None:
        rows = [r for r in _fixtures()["scam_reports"] if year_from <= r["year"] <= year_to]
        note = _fixtures().get("_scam_reports_note", "")
    else:
        from sqlalchemy import text

        with eng.connect() as c:
            rows = [
                dict(r)
                for r in c.execute(
                    text(
                        "SELECT year, case_count, loss_amount, source FROM scam_reports "
                        "WHERE year BETWEEN :a AND :b ORDER BY year"
                    ),
                    {"a": year_from, "b": year_to},
                ).mappings()
            ]
        note = "年度數字為刑事局/165打詐儀錶板公開統計；2024起新口徑，不宜逐年直接比較。"

    by_year = sorted(
        (
            {
                "year": r["year"],
                "case_count": r["case_count"],
                "loss_amount": r.get("loss_amount", 0),
                "source": r.get("source", ""),
            }
            for r in rows
        ),
        key=lambda x: x["year"],
    )

    # 真實收集樣本的類型分布（只算標為 scam 且有 scam_type 的）
    type_count: dict[str, int] = {}
    for ex in get_scam_examples():
        if ex.get("label") == "scam":
            t = ex.get("scam_type") or "未分類"
            type_count[t] = type_count.get(t, 0) + 1
    by_sample_type = sorted(
        ({"scam_type": k, "count": v} for k, v in type_count.items()),
        key=lambda x: -x["count"],
    )

    return {"by_year": by_year, "by_sample_type": by_sample_type, "note": note}
