# db — 資料庫 schema 與種子資料

| 檔案 | 內容 |
|---|---|
| `schema.sql` | 4 張表：`scam_reports`（統計）、`scam_examples`（RAG 話術樣本）、`qa_questions`（遊戲）、`detections`（偵測紀錄） |
| `seed.sql` | 示意性種子資料，供本機測試/demo（真實資料由 crawler 覆蓋） |

## 本機起 DB（不需 render）
```bash
docker compose up -d db          # 首次啟動會自動套用 schema + seed
# 連線字串：postgresql://scam:scam@localhost:5432/scam
```

## 套用到 render PostgreSQL
```bash
psql "<render External Database URL>" -f db/schema.sql
psql "<render External Database URL>" -f db/seed.sql
```

> 設計依 DECISIONS **D004**：`scam_examples.content` 保留話術原文供偵測 RAG 檢索。
> 要升級語意檢索可加 pgvector 擴充並對 `content` 建向量索引。
