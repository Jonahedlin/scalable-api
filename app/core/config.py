import os
from dotenv import load_dotenv

load_dotenv()

# Auth
SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# CORS — comma-separated list of allowed origins
# e.g. FRONTEND_ORIGIN=http://localhost:5173,https://yourapp.com
FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
ALLOWED_ORIGINS: list = [o.strip() for o in FRONTEND_ORIGIN.split(",")]
