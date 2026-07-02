# deploy/aws — AWS 部署設定（計畫書原案，D005）

完整步驟見 [`docs/DEPLOY.md` 的 B 節](../../docs/DEPLOY.md)。本目錄放 AWS 專屬輔助檔。

- 前端：Amplify Hosting（app root = `frontend`）
- 後端 ×2：Elastic Beanstalk（Docker，各自的 `Dockerfile`，**從 repo 根 build**）
- 資料庫：RDS (PostgreSQL)

## EB Dockerrun 範例（backend-api）
若用預建映像（先 push 到 ECR）：
```json
{
  "AWSEBDockerrunVersion": "1",
  "Image": { "Name": "<account>.dkr.ecr.<region>.amazonaws.com/scam-api:latest", "Update": "true" },
  "Ports": [{ "ContainerPort": 8000 }]
}
```
環境變數 `DATABASE_URL`、`GEMINI_API_KEY` 在 EB 環境設定填入（勿入庫）。

> render 為主交付（`render.yaml`）；AWS 為「計畫書完整實現」備援，需注意免費額度與成本。
