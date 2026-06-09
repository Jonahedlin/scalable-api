from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.config import ALLOWED_ORIGINS
from app.routers import auth, submissions, uploads

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Scalable API",
    description="Backend for the Scalable image ingestion platform.",
    version="0.1.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allows the React dev server (localhost:5173) to call this API.
# Update FRONTEND_ORIGIN in .env for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router,        prefix="/api")
app.include_router(uploads.router,     prefix="/api")
app.include_router(submissions.router, prefix="/api")


# ── Root redirect ────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# ── Health check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
