# backend-api (FastAPI) — AWS Elastic Beanstalk / 容器部署（D005）
# ⚠️ 從 repo 根 build（保留 monorepo 目錄結構，讓 db/ 相對路徑成立）：
#     docker build -f backend-api/Dockerfile -t scam-api .
FROM python:3.12-slim
WORKDIR /app
COPY backend-api/requirements.txt backend-api/requirements.txt
RUN pip install --no-cache-dir -r backend-api/requirements.txt
COPY backend-api/ backend-api/
COPY db/ db/
WORKDIR /app/backend-api
# build 階段訓練模型（與 render 一致）；無資料時不讓 build 失敗
RUN python -m model.train || echo "train skipped (no data yet)"
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
