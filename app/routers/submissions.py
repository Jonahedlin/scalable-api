from fastapi import APIRouter
from app.schemas.upload import SubmissionCountResponse

router = APIRouter(tags=["submissions"])


@router.get("/submissions/count", response_model=SubmissionCountResponse)
async def get_submission_count():
    """
    Return the total number of uploads submitted by the authenticated user.

    Mock behaviour: returns a hardcoded count.
    Replace with a real DB query when the database is connected:
        SELECT COUNT(*) FROM uploads WHERE user_id = current_user.id
    """

    # ── TODO: replace with real DB query ─────────────────────────────────────
    # count = await db.execute(select(func.count()).where(Upload.user_id == user.id))
    # return SubmissionCountResponse(count=count.scalar())
    # ─────────────────────────────────────────────────────────────────────────

    return SubmissionCountResponse(count=24)
