"""入庫：有 DATABASE_URL 寫 PostgreSQL，否則寫 output/scam_examples.jsonl。"""
from __future__ import annotations

import json
import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL")
# 無 DB 時的真實資料累積檔；backend-api 的 data 層與 model 訓練都會合併讀取它
INGESTED = Path(__file__).resolve().parents[1] / "db" / "ingested.jsonl"


def save_examples(rows: list[dict]) -> int:
    """rows: [{label, scam_type, content, features, source}]"""
    if not rows:
        return 0
    if not DATABASE_URL:
        # 以 content 去重後追加
        seen = set()
        if INGESTED.exists():
            for line in INGESTED.open(encoding="utf-8"):
                try:
                    seen.add(json.loads(line)["content"])
                except Exception:
                    pass
        added = 0
        with INGESTED.open("a", encoding="utf-8") as fh:
            for r in rows:
                if r["content"] in seen:
                    continue
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                seen.add(r["content"])
                added += 1
        print(f"[store] no DB → appended {added} new rows to {INGESTED}（去重後）")
        return added

    from sqlalchemy import create_engine, text

    url = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1).replace(
        "postgresql://", "postgresql+psycopg://", 1
    )
    eng = create_engine(url)
    with eng.begin() as c:
        for r in rows:
            c.execute(
                text(
                    "INSERT INTO scam_examples (label, scam_type, content, features, source) "
                    "VALUES (:label, :scam_type, :content, :features, :source)"
                ),
                {
                    "label": r.get("label", "scam"),
                    "scam_type": r.get("scam_type"),
                    "content": r["content"],
                    "features": r.get("features"),
                    "source": r.get("source", "crawler"),
                },
            )
    print(f"[store] inserted {len(rows)} rows into PostgreSQL")
    return len(rows)
