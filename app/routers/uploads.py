import uuid
from datetime import date
from typing import List

from fastapi import APIRouter, File, Query, UploadFile

from app.schemas.upload import UploadRecord, UploadResponse, UploadsResponse

router = APIRouter(tags=["uploads"])


# ── Mock dataset ──────────────────────────────────────────────────────────────
# Remove this once the database is connected.
# Mirrors the mock data used in the frontend UploadsListTile component.
MOCK_UPLOADS: List[UploadRecord] = [
    UploadRecord(id="1",  name="screenshot_001.png",    status="approved", submittedAt="2026-05-23"),
    UploadRecord(id="2",  name="capture_dashboard.jpg", status="pending",  submittedAt="2026-05-23"),
    UploadRecord(id="3",  name="report_page2.png",      status="rejected", submittedAt="2026-05-22"),
    UploadRecord(id="4",  name="invoice_scan.jpg",      status="approved", submittedAt="2026-05-22"),
    UploadRecord(id="5",  name="form_filled.png",       status="pending",  submittedAt="2026-05-21"),
    UploadRecord(id="6",  name="receipt_may21.jpg",     status="approved", submittedAt="2026-05-21"),
    UploadRecord(id="7",  name="passport_scan.jpg",     status="approved", submittedAt="2026-05-20"),
    UploadRecord(id="8",  name="bank_statement.png",    status="pending",  submittedAt="2026-05-20"),
    UploadRecord(id="9",  name="utility_bill.jpg",      status="rejected", submittedAt="2026-05-19"),
    UploadRecord(id="10", name="id_card_front.png",     status="approved", submittedAt="2026-05-19"),
    UploadRecord(id="11", name="id_card_back.png",      status="approved", submittedAt="2026-05-18"),
    UploadRecord(id="12", name="selfie_verify.jpg",     status="pending",  submittedAt="2026-05-18"),
]


# ── GET /api/uploads ──────────────────────────────────────────────────────────
@router.get("/uploads", response_model=UploadsResponse)
async def list_uploads(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int  = Query(4, ge=1, le=50, description="Max records to return"),
):
    """
    Return a paginated list of uploads.

    Mock behaviour: slices the in-memory dataset.
    Replace with a real DB query when the database is connected:
        SELECT * FROM uploads ORDER BY submitted_at DESC LIMIT limit OFFSET offset
    """

    # ── TODO: replace with real DB query ─────────────────────────────────────
    # results = await db.execute(
    #     select(Upload)
    #     .where(Upload.user_id == user.id)
    #     .order_by(Upload.submitted_at.desc())
    #     .offset(offset).limit(limit)
    # )
    # ─────────────────────────────────────────────────────────────────────────

    total  = len(MOCK_UPLOADS)
    sliced = MOCK_UPLOADS[offset : offset + limit]

    return UploadsResponse(
        uploads=sliced,
        hasMore=offset + limit < total,
        total=total,
    )


# ── POST /api/uploads ─────────────────────────────────────────────────────────
@router.post("/uploads", response_model=UploadResponse, status_code=201)
async def create_upload(file: UploadFile = File(...)):
    """
    Accept a single image file upload.

    Mock behaviour: acknowledges the file without storing it.
    Replace with the real pipeline when storage is ready:
        1. Validate MIME type server-side
        2. Stream file to S3 / Cloudflare R2
        3. Insert metadata record into the uploads DB table
        4. Return the saved record
    """

    # ── TODO: replace with real upload pipeline ───────────────────────────────
    # s3_key  = await upload_to_s3(file)
    # record  = await db.insert(Upload(user_id=user.id, s3_key=s3_key, name=file.filename))
    # ─────────────────────────────────────────────────────────────────────────

    return UploadResponse(
        id=str(uuid.uuid4()),
        name=file.filename or "unknown",
        status="pending",
        submittedAt=str(date.today()),
    )
