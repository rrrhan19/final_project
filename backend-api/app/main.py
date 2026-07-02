"""詐騙偵測 API：偵測 / 統計 / Gemini（D006）。

上線安全（顧問 permission-architect 建議）：
- CORS 由 ALLOWED_ORIGINS 環境變數控制（預設只開本機 dev），不再 *。
- /api/detect 加 per-IP 簡易限流，避免公開後被濫用、放大 Gemini 費用。
"""
import os
import time
from collections import deque

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .data import get_stats, using_db
from .detect import detect
from .urlcheck import check_url, blocklist_size
from .community import check_phone, add_report
from .assistant import chat
from .alerts import get_alerts
from .init_db import init_db

# 允許的前端來源（逗號分隔）；預設只開本機開發。上線時設成你的前端網域。
ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if o.strip()
]
# 限流：每 IP 在 WINDOW 秒內最多 LIMIT 次 /api/detect
RATE_LIMIT = int(os.getenv("DETECT_RATE_LIMIT", "30"))
RATE_WINDOW = int(os.getenv("DETECT_RATE_WINDOW", "60"))

app = FastAPI(title="Scam Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()


_hits: dict[str, deque] = {}


def _rate_ok(ip: str) -> bool:
    now = time.time()
    dq = _hits.setdefault(ip, deque())
    while dq and now - dq[0] > RATE_WINDOW:
        dq.popleft()
    if len(dq) >= RATE_LIMIT:
        return False
    dq.append(now)
    return True


class DetectIn(BaseModel):
    text: str


class UrlIn(BaseModel):
    url: str


class PhoneIn(BaseModel):
    phone: str


class ReportIn(BaseModel):
    kind: str
    value: str
    note: str = ""


class ChatIn(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok", "service": "backend-api", "db": using_db()}


@app.post("/api/detect")
def api_detect(body: DetectIn, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _rate_ok(ip):
        return JSONResponse(
            status_code=429,
            content={"error": f"請求過於頻繁，請稍候再試（每 {RATE_WINDOW} 秒上限 {RATE_LIMIT} 次）。"},
        )
    return detect(body.text)


@app.post("/api/url-check")
def api_url_check(body: UrlIn, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _rate_ok(ip):
        return JSONResponse(status_code=429, content={"error": "請求過於頻繁，請稍候再試。"})
    return {**check_url(body.url), "blocklist_size": blocklist_size()}


@app.post("/api/phone-check")
def api_phone_check(body: PhoneIn, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _rate_ok(ip):
        return JSONResponse(status_code=429, content={"error": "請求過於頻繁，請稍候再試。"})
    return check_phone(body.phone)


@app.post("/api/report")
def api_report(body: ReportIn, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _rate_ok(ip):
        return JSONResponse(status_code=429, content={"error": "請求過於頻繁，請稍候再試。"})
    return add_report(body.kind, body.value, body.note)


@app.post("/api/chat")
def api_chat(body: ChatIn, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _rate_ok(ip):
        return JSONResponse(status_code=429, content={"error": "請求過於頻繁，請稍候再試。"})
    return chat(body.message, body.history)


@app.get("/api/alerts")
def api_alerts(limit: int = 10):
    return get_alerts(limit)


@app.get("/api/stats")
def api_stats(year_from: int = Query(2020, alias="from"), to: int = 2025):
    return get_stats(year_from, to)
