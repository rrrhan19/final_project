# backend-node (Express) — AWS Elastic Beanstalk / 容器部署（D005）
# ⚠️ 從 repo 根 build（保留 monorepo 目錄結構，讓 db/ 相對路徑成立）：
#     docker build -f backend-node/Dockerfile -t scam-node .
FROM node:20-slim
WORKDIR /app
COPY backend-node/package*.json backend-node/
RUN cd backend-node && npm install --omit=dev
COPY backend-node/ backend-node/
COPY db/ db/
WORKDIR /app/backend-node
EXPOSE 3000
CMD ["sh", "-c", "node src/server.js"]
