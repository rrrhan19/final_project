-- 反詐平台 PostgreSQL schema
-- 設計依 D004：偵測用 Gemini 一發 + RAG，故 scam_examples 保留「話術原文/特徵文本」供向量化檢索。
-- 適用 render PostgreSQL 與本機 docker Postgres。

-- ── 1. 歷史詐騙統計（2021–2025）：給統計視覺化用，可 SQL 聚合 ──
CREATE TABLE IF NOT EXISTS scam_reports (
    id          SERIAL PRIMARY KEY,
    year        INT  NOT NULL,            -- 年度
    month       INT,                      -- 1–12，可為 NULL（只有年資料時）
    category    TEXT,                     -- 類型；'全部' 表年度總計
    channel     TEXT,                     -- 管道：簡訊 / 社群 / 電話 / 假網站 …
    region      TEXT,                     -- 地區（縣市），可 NULL
    case_count  INT  NOT NULL DEFAULT 0,  -- 案件數
    loss_amount BIGINT DEFAULT 0,         -- 財損金額（新台幣元）；未取得官方數字者為 0
    source      TEXT,                     -- 資料來源（出處/機關）
    created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_scam_reports_year ON scam_reports(year);
CREATE INDEX IF NOT EXISTS idx_scam_reports_category ON scam_reports(category);

-- ── 2. 詐騙話術樣本：給偵測的 RAG grounding + few-shot 用（含原文文本）──
CREATE TABLE IF NOT EXISTS scam_examples (
    id          SERIAL PRIMARY KEY,
    label       TEXT NOT NULL CHECK (label IN ('scam','legit')),  -- 詐騙 / 正常
    scam_type   TEXT,                     -- 若 scam：屬於哪種話術
    content     TEXT NOT NULL,            -- 話術/訊息原文（RAG 檢索的核心文本）
    features    TEXT,                     -- 特徵描述（人工標註的判斷依據）
    source      TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_scam_examples_label ON scam_examples(label);
-- 全文檢索（簡易 RAG 的 baseline；要語意檢索可日後加 pgvector）
CREATE INDEX IF NOT EXISTS idx_scam_examples_content_trgm ON scam_examples USING gin (to_tsvector('simple', content));

-- ── 3. 模擬遊戲問答字典 ──
CREATE TABLE IF NOT EXISTS qa_questions (
    id           SERIAL PRIMARY KEY,
    scam_type    TEXT,                    -- 對應詐騙類型
    difficulty   INT DEFAULT 1,           -- 1 易 – 3 難
    prompt       TEXT NOT NULL,           -- 題目（情境訊息）
    options      JSONB NOT NULL,          -- ["選項A","選項B",...]
    correct_idx  INT  NOT NULL,           -- 正解在 options 的索引
    explanation  TEXT NOT NULL,           -- 解說（預存，非 LLM 生成）
    created_at   TIMESTAMPTZ DEFAULT now()
);

-- ── 4. 偵測紀錄（選用，預設不啟用）──
-- ⚠️ PDPA/個資：input_text 可能含第三人個資。預設不寫入；若要啟用紀錄，
--    務必先過 crawler.base.scrub_pii() 去識別化，或只存 verdict/confidence 與雜湊，並於前端告知。
CREATE TABLE IF NOT EXISTS detections (
    id          SERIAL PRIMARY KEY,
    input_type  TEXT NOT NULL,            -- 'text' | 'url'
    input_text  TEXT NOT NULL,
    verdict     TEXT,                     -- 'scam' | 'legit' | 'uncertain'
    confidence  REAL,                     -- 0.0–1.0
    reasoning   TEXT,
    used_rag    BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT now()
);
