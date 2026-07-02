"""訓練詐騙文字分類器（D006：計畫書「scam detection model」）。

特徵：字元 n-gram TF-IDF（適合中文無空白）。模型：LogisticRegression。
資料：有 DATABASE_URL 讀 scam_examples，否則讀 db/fixtures.json。
輸出：backend-api/model/scam_clf.joblib

    python -m model.train          # 從 backend-api/ 目錄執行
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = Path(__file__).resolve().parent / "scam_clf.joblib"


def load_training_data() -> "tuple[list[str], list[int]]":
    url = os.getenv("DATABASE_URL")
    if url:
        from app.init_db import init_db
        from sqlalchemy import create_engine, text

        init_db()
        u = url.replace("postgres://", "postgresql+psycopg://", 1).replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
        eng = create_engine(u)
        with eng.connect() as c:
            rows = [
                dict(r)
                for r in c.execute(text("SELECT label, content FROM scam_examples")).mappings()
            ]
    else:
        rows = json.loads((ROOT / "db" / "fixtures.json").read_text(encoding="utf-8"))[
            "scam_examples"
        ]
        # 合併爬蟲收集的真實資料
        ingested = ROOT / "db" / "ingested.jsonl"
        if ingested.exists():
            for line in ingested.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    texts = [r["content"] for r in rows]
    labels = [1 if r["label"] == "scam" else 0 for r in rows]
    return texts, labels


def train() -> None:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    import joblib

    texts, labels = load_training_data()
    n_scam, n_legit = sum(labels), len(labels) - sum(labels)
    print(f"訓練樣本：{len(texts)} 筆（詐騙 {n_scam} / 正常 {n_legit}）")
    if n_scam == 0 or n_legit == 0:
        print("⚠️ 資料缺少其中一類，無法訓練。請先補資料（爬蟲入庫）。")
        sys.exit(1)

    clf = Pipeline(
        [
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1)),
            ("lr", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    clf.fit(texts, labels)
    joblib.dump(clf, MODEL_PATH)
    print(f"模型已存：{MODEL_PATH}")
    # ⚠️ 不在此印『訓練集準確率』——小資料會接近 100% 但毫無意義。
    #    真實表現請跑 `python -m model.evaluate`（held-out 測試集的 Precision/Recall/F1）。
    print("→ 評估真實表現請執行：python -m model.evaluate")


if __name__ == "__main__":
    train()
