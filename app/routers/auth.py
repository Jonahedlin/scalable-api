from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    """
    Authenticate a user and return an access token.

    Mock behaviour: accepts any non-empty credentials and returns a
    placeholder token. Replace the body with real DB lookup +
    password verification (passlib bcrypt) + JWT issuance (python-jose)
    when the database is connected.
    """
    if not body.identifier.strip() or not body.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identifier and password are required.",
        )

    # ── TODO: replace with real auth ─────────────────────────────────────────
    # user = await get_user_by_identifier(body.identifier)
    # if not user or not verify_password(body.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Invalid credentials.")
    # token = create_access_token({"sub": str(user.id)})
    # ─────────────────────────────────────────────────────────────────────────

    return TokenResponse(token="mock-jwt-token")
