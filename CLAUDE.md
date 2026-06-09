# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

FastAPI backend for the **Scalable** image ingestion platform. Receives image uploads from the React frontend, stores them in S3/R2, records metadata in PostgreSQL, and exposes data to the ML pipeline. Frontend lives at `../react-app/`.

---

## Commands

```bash
# Activate the virtual environment (always do this first)
source venv/bin/activate

# Start the dev server with auto-reload
uvicorn app.main:app --reload

# Server runs at http://localhost:8000
# Interactive API docs at http://localhost:8000/docs
```

---

## Stack

- **FastAPI 0.115** + **Python 3.9**
- **Pydantic v2** for request/response schema validation
- **python-dotenv** for environment config
- **uvicorn** as the ASGI server
- **python-multipart** for file upload handling

Not yet added (future phases):
- **SQLAlchemy + Alembic** — ORM and migrations (Phase 5)
- **boto3** — AWS S3 / Cloudflare R2 file storage (Phase 4)
- **python-jose + passlib** — JWT auth and password hashing

---

## Project Structure

```
scalable-api/
├── app/
│   ├── main.py              # App entry point, CORS, router registration
│   ├── core/
│   │   └── config.py        # Env vars loaded from .env
│   ├── schemas/
│   │   ├── auth.py          # LoginRequest, TokenResponse
│   │   └── upload.py        # UploadRecord, UploadsResponse, UploadResponse, SubmissionCountResponse
│   └── routers/
│       ├── auth.py          # POST /api/auth/login
│       ├── uploads.py       # GET /api/uploads, POST /api/uploads
│       └── submissions.py   # GET /api/submissions/count
├── venv/                    # Virtual environment — never commit
├── requirements.txt
├── .env.example
└── CLAUDE.md
```

---

## API Endpoints

All routes are prefixed with `/api`. A `/health` endpoint is available at the root for uptime checks.

### `POST /api/auth/login`
**Schema:** `LoginRequest { identifier: str, password: str }` → `TokenResponse { token: str, token_type: str }`

Validates that both fields are non-empty. Currently returns `"mock-jwt-token"` for any credentials.
**TODO:** DB user lookup + bcrypt password verify + JWT issuance via `python-jose`.

---

### `GET /api/uploads?offset=N&limit=N`
**Schema:** → `UploadsResponse { uploads: UploadRecord[], hasMore: bool, total: int }`

Offset-based pagination. Default `limit=4`, max `limit=50`.
Currently slices a 12-record in-memory mock list.
**TODO:** Replace `MOCK_UPLOADS` slice with SQLAlchemy query ordered by `submitted_at DESC`.

---

### `POST /api/uploads`
**Body:** `multipart/form-data` with a single `file` field → `UploadResponse { id, name, status, submittedAt }`

Returns HTTP 201. Currently acknowledges the file without storing it.
**TODO:** Validate MIME type → stream to S3/R2 → insert DB record → return saved record.

---

### `GET /api/submissions/count`
**Schema:** → `SubmissionCountResponse { count: int }`

Currently returns hardcoded `24`.
**TODO:** `SELECT COUNT(*) FROM uploads WHERE user_id = current_user.id`.

---

## Configuration

Copy `.env.example` to `.env` before running:

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key-…` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token lifetime (24 h) |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | CORS allowed origin |

`FRONTEND_ORIGIN` accepts a comma-separated list for multiple origins.

---

## CORS

Configured in `main.py` via `CORSMiddleware`. Reads `ALLOWED_ORIGINS` from `config.py`, which parses `FRONTEND_ORIGIN`. The React dev server runs on `localhost:5173` by default — this is the value set in `.env.example`.

---

## Mock → Real Transition

Every endpoint has a clearly marked `# ── TODO` block showing the exact DB/storage code that replaces the mock. Search for `# ── TODO` across the routers to find all pending swap-outs.
