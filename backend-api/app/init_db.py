"""啟動時自動初始化資料庫（讓 render 免費方案免手動 psql）。

有 DATABASE_URL 時：確保 schema 存在；若 scam_examples 為空則灌入 fixtures 種子。
全程 try/except，DB 出問題不會讓服務啟動失敗（會降級用 fixtures）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


def _sql_statements(sql: str) -> list[str]:
    cleaned = "\n".join(
        line for line in sql.splitlines() if not line.lstrip().startswith("--")
    )
    return [stmt.strip() for stmt in cleaned.split(";") if stmt.strip()]


def init_db() -> None:
    url = os.getenv("DATABASE_URL")
    if not url:
        return
    try:
        from sqlalchemy import create_engine, text

        u = url.replace("postgres://", "postgresql+psycopg://", 1).replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
        eng = create_engine(u, pool_pre_ping=True)

        # 1) 確保 schema（schema.sql 全用 IF NOT EXISTS，可重複執行）
        schema = (_ROOT / "db" / "schema.sql").read_text(encoding="utf-8")
        with eng.begin() as c:
            for stmt in _sql_statements(schema):
                c.execute(text(stmt))

        # 2) 若空則灌種子
        with eng.begin() as c:
            n = c.execute(text("SELECT count(*) FROM scam_examples")).scalar() or 0
            if n == 0:
                fx = json.loads((_ROOT / "db" / "fixtures.json").read_text(encoding="utf-8"))
                for e in fx["scam_examples"]:
                    c.execute(
                        text("INSERT INTO scam_examples(label,scam_type,content,source) VALUES(:l,:t,:c,'seed')"),
                        {"l": e["label"], "t": e.get("scam_type"), "c": e["content"]},
                    )
                for q in fx["qa_questions"]:
                    c.execute(
                        text("INSERT INTO qa_questions(scam_type,difficulty,prompt,options,correct_idx,explanation) "
                             "VALUES(:t,:d,:p,CAST(:o AS jsonb),:ci,:e)"),
                        {"t": q.get("scam_type"), "d": q.get("difficulty", 1), "p": q["prompt"],
                         "o": json.dumps(q["options"], ensure_ascii=False), "ci": q["correct_idx"], "e": q["explanation"]},
                    )
                for r in fx["scam_reports"]:
                    c.execute(
                        text("INSERT INTO scam_reports(year,category,case_count,loss_amount,source) "
                             "VALUES(:y,:cat,:cc,:la,:s)"),
                        {"y": r["year"], "cat": r.get("category"), "cc": r["case_count"],
                         "la": r.get("loss_amount", 0), "s": r.get("source", "seed")},
                    )
                print(f"[init_db] seeded {len(fx['scam_examples'])} examples")
        print("[init_db] ready")
    except Exception as e:  # noqa: BLE001
        print(f"[init_db] skipped ({e}); 服務改用 fixtures fallback")
